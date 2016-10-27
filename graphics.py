import math
import collections
import random
from PyQt5 import QtOpenGL, QtGui, QtWidgets, QtCore
from PIL import Image
import OpenGL.GL as gl
import game
import towers
import consts
import game_logic
import creeps
from shader import Shader
from mesh import Mesh


Point = collections.namedtuple('Point', 'row, col')


class MainWindow(QtWidgets.QWidget):
    def __init__(self, screen):
        super(MainWindow, self).__init__()
        self.setMinimumSize(screen.width(), screen.height())
        self.setMaximumSize(screen.width(), screen.height())

        self.setWindowTitle('Tower Defense')
        self.setWindowIcon(QtGui.QIcon('field/icon.png'))

        self.game = game.Game()

        self.widget = Graphics(
            self, screen.width(), screen.height(), self.game)

        self.buttons = []
        self.set_buttons(screen.width(), self.game.field)

        self.labels = []
        self.set_labels(screen.width(), self.game)

        self.showMaximized()

    def set_buttons(self, width, field):
        cell_size = width / len(field[0])
        names = ['ArcaneTower', 'CanonTower', 'GuardTower']
        button_rate = 1.5
        button_size = cell_size * button_rate
        image_rate = 1.125
        image_size = cell_size * image_rate
        for i, name in enumerate(names):
            button = Button(
                name, self, image_size, button_size, self.widget.choose_tower)
            button.move(button_size * i, 0)
            self.buttons.append(button)

    def set_labels(self, width, state):
        cell_size = width / len(state.field[0])
        width_rate = 3
        width = cell_size * width_rate
        height_rate = 1.5
        height = cell_size * height_rate
        bias = 3 * height
        numbers = {'Gold': state.get_gold_number,
                   'Enemies': state.get_remaining_enemies}
        for i, name in enumerate(numbers):
            label = Label(name, self, width, height, numbers[name])
            label.move(width * i + bias, 0)
            self.labels.append(label)


class Button(QtWidgets.QPushButton):
    _names = {'ArcaneTower': towers.ArcaneTower,
              'CanonTower': towers.CanonTower,
              'GuardTower': towers.GuardTower}

    def __init__(self, name, parent, image_size, button_size, func):
        super().__init__('', parent)
        self.name = name
        self.setMaximumSize(button_size, button_size)
        self.setMinimumSize(button_size, button_size)
        self.setIcon(QtGui.QIcon('field/{}.png'.format(name)))
        self.setIconSize(QtCore.QSize(image_size, image_size))
        self.func = func
        self.clicked.connect(self.react)

    def react(self):
        self.func(Button._names[self.name])


class Label(QtWidgets.QFrame):
    def __init__(self, text, parent, width, height, get_number):
        super().__init__(parent)
        self.setMaximumSize(width, height)
        self.setMinimumSize(width, height)

        self.text = text
        self.label = QtWidgets.QLabel(
            '{0}: {1}'.format(text, get_number()), self)
        self.get_number = get_number
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.setStyleSheet(
            'QFrame { background-color: lightgrey;'
            ' border: 1px solid black }')
        self.label.setStyleSheet(
            'QLabel { background-color : lightgrey;'
            ' color : black; border: none}')

        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.update)
        update_time = math.ceil(100)
        self.update_timer.start(update_time)

    def update(self):
        self.label.setText('{0}: {1}'.format(self.text, self.get_number()))


class Graphics(QtOpenGL.QGLWidget):
    def __init__(self, parent, width, height, state):
        super().__init__(parent)
        self.game = state
        self.parent = parent
        self.screen_width = width
        self.screen_height = height
        self.cell_width = 0
        self.cell_height = 0
        self.shader = None

        self.field_quad = None
        self.towers = []
        self.creeps = {}
        self.attacks = {}
        self.healths = {}

        self.chosen_tower = None

        self.spawn_timer = None
        self.draw_timer = None
        self.count = 0

    def initializeGL(self):
        self.cell_width = (2 * self.screen_width /
                           len(self.game.field[0]) / self.screen_width)
        self.cell_height = (2 * self.screen_height /
                            len(self.game.field) / self.screen_height)

        self.shader = Shader('shader.vs', 'shader.fs')
        self.shader.save_attr_locations(
            ['aVertexPosition', 'aVertexTexCoord'])
        self.shader.save_uniform_locations(
            ['uModelMatrix', 'uViewMatrix', 'uProjectionMatrix', 'uTexture'])
        self.shader.bind()

        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glClearColor(255, 255, 255, 1)

        gl.glViewport(0, 0, self.screen_width, self.screen_height)
        self.setGeometry(0, 0, self.screen_width, self.screen_height)

        self.set_field()

        self.spawn_timer = QtCore.QTimer()
        self.spawn_timer.timeout.connect(self.start_creep_spawn)
        self.start_creep_spawn()
        spawn_time = 35000
        self.spawn_timer.start(spawn_time)

        self.draw_timer = QtCore.QTimer()
        self.draw_timer.timeout.connect(self.update)
        redraw_time = math.ceil(1000/60)
        self.draw_timer.start(redraw_time)
        # self.test()

    # def test(self):
    #     start = Point(10, 21)
    #     points = []
    #     for i in range(10):
    #         for j in range(10):
    #             points.append(Point(start.row - 5 + i, start.col - 5 + j))
    #     for i, point in enumerate(points):
    #         self.attacks[points[i]] = Mesh.get_line(
    #             start,
    #             points[i],
    #             0.1,
    #             self.cell_width,
    #             self.cell_height)

    def paintGL(self):
        if self.game.end:
            return

        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        self.field_quad.draw(self.shader.handles)

        for tower in self.towers:
            tower.draw(self.shader.handles)

        for creep in self.creeps:
            self.creeps[creep].draw(self.shader.handles)
            self.healths[creep].draw(self.shader.handles)

        for attack in self.attacks:
            self.attacks[attack].draw(self.shader.handles)

    def mousePressEvent(self, event):
        if not self.chosen_tower:
            return
        if event.buttons() == QtCore.Qt.LeftButton:
            cell_width = math.floor(
                self.screen_width / len(self.game.field[0]))
            cell_height = math.floor(
                self.screen_height / len(self.game.field))
            row = math.floor(event.globalY() / cell_height)
            col = math.floor(event.globalX() / cell_width)
            if not game_logic.in_field(self.game.field, Point(row, col)):
                return
            if (not isinstance(self.game.field[row][col], game.Map) or
                    self.game.field[row][col].type != game_logic.Type.Grass):
                return
            self.place_tower(row, col, self.chosen_tower)
            self.chosen_tower = None

    def choose_tower(self, tower_type):
        self.chosen_tower = tower_type

    def place_tower(self, row, col, tower_type):
        fail = self.game.place_unit(row, col, tower_type)
        if fail:
            return
        self.towers.append(self.get_unit(row, col, tower_type))
        self.attack(self.game.field[row][col])

    def set_field(self):
        field = Image.new('RGBA', (self.screen_width, self.screen_width))
        images = {'Grass': Image.open('field/Grass.png'),
                  'Path': Image.open('field/Path.png'),
                  'Portal': Image.open('field/Portal.png'),
                  'Castle': Image.open('field/Castle.png')}
        width = math.floor(self.screen_width / len(self.game.field[0]))
        height = math.floor(self.screen_width / len(self.game.field))
        for k in images:
            images[k] = images[k].resize((width, height))
        for row, line in enumerate(self.game.field):
            for col, figure in enumerate(line):
                if not isinstance(figure, game.Map):
                    continue
                image = images[self.game.field[row][col].type.name]
                field.paste(image, (col * width, row * height))
        priority = 0.9
        self.field_quad = Mesh.get_quad(-1, 1, 1, -1, priority)
        self.field_quad.set_texture(field)

    def get_unit(self, row, col, unit_type):
        bias = self.cell_height * 0.025
        priority = 0.2
        quad = Mesh.get_quad(-1 + col * self.cell_width + bias,
                             1 - row * self.cell_height - bias,
                             -1 + (col + 1) * self.cell_width - bias,
                             1 - (row + 1) * self.cell_height + bias,
                             priority)
        quad.set_texture(
            Image.open('field/{}.png'.format(unit_type.__name__)))
        return quad

    def start_creep_spawn(self):
        creep_types = [creeps.Peon(0, 0),
                       creeps.Grunt(0, 0),
                       creeps.Raider(0, 0)]
        self.spawn_wave(random.choice(creep_types), 5)

    def spawn_wave(self, creep, amount):
        def spawn():
            if self.count == amount:
                return
            self.count += 1
            point = self.game.portal

            self.game.place_unit(point.row, point.col, type(creep))
            self.creeps[point] = self.get_unit(
                point.row, point.col, type(creep))
            self.move_creep(self.game.field[point.row][point.col])
            spawn_time = 15000
            QtCore.QTimer.singleShot(round(spawn_time / creep.speed), spawn)

        if self.game.end:
            return

        self.count = 0
        spawn()

    def move_creep(self, creep):
        self.creeps.pop(Point(creep.row, creep.col), None)
        stop = creep.move(self.game.field, self.game)
        bias = self.cell_height * 0.025
        row = creep.row
        col = creep.col
        priority = 0.2
        self.creeps[Point(row, col)] = Mesh.get_quad(
            -1 + col * self.cell_width + bias,
            1 - row * self.cell_height - bias,
            -1 + (col + 1) * self.cell_width - bias,
            1 - (row + 1) * self.cell_height + bias,
            priority)
        health = consts.MAX_HEALTH[type(creep).__name__]
        rate = creep.health / health
        self.healths[Point(row, col)] = Mesh.get_line(
            Point(row+0.6, col-0.4),
            Point(row+0.6, col-0.4+rate),
            0.15,
            self.cell_width,
            self.cell_height)
        self.creeps[Point(row, col)].set_texture(
            Image.open('field/{}.png'.format(type(creep).__name__)))
        if stop is True:
            self.creeps.pop(Point(row, col), None)
            return
        spawn_time = 5000
        QtCore.QTimer.singleShot(round(spawn_time / creep.speed),
                                 lambda: self.move_creep(creep))

    def attack(self, tower):
        enemy = tower.attack(self.game)
        if enemy:
            point1 = tower if tower.col < enemy.col else enemy
            point2 = tower if tower.col > enemy.col else enemy
            attack = Mesh.get_line(point1,
                                   point2,
                                   0.1,
                                   self.cell_width,
                                   self.cell_height)
            self.attacks[Point(tower.row, tower.col)] = attack
        delete_time = 200
        QtCore.QTimer.singleShot(
            delete_time, lambda: self.attacks.pop(
                Point(tower.row, tower.col), None))
        spawn_time = 5000
        QtCore.QTimer.singleShot(round(spawn_time / tower.speed),
                                 lambda: self.attack(tower))
