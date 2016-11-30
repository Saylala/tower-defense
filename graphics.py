import sys
import math
import collections
import random
import subprocess
from PyQt5 import QtOpenGL, QtGui, QtWidgets, QtCore
from PIL import Image
import OpenGL.GL as GL
import game
import towers
import consts
import game_field
import creeps
from shader import Shader
from mesh import Mesh

Point = collections.namedtuple('Point', 'row, col')


def start():
    app = QtWidgets.QApplication(sys.argv)

    window = StartWindow(app.desktop().screenGeometry())
    window.setWindowFlags(
        QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
    window.show()

    sys.exit(app.exec_())


class StartWindow(QtWidgets.QWidget):
    def __init__(self, screen):
        super(StartWindow, self).__init__()
        self.screen = screen
        self.setWindowTitle(consts.TITLE)
        self.setWindowIcon(QtGui.QIcon(consts.ICON_PATH))
        self.setMinimumSize(screen.height() / 3, screen.height() / 3)
        self.setMaximumSize(screen.height() / 3, screen.height() / 3)

        layout = QtWidgets.QVBoxLayout()
        self.picture = QtWidgets.QLabel()
        self.picture.setScaledContents(True)
        self.picture.setPixmap(QtGui.QPixmap(consts.LOGO_PATH))
        layout.addWidget(self.picture)

        self.start_button = QtWidgets.QPushButton('Launch', self)
        self.start_button.clicked.connect(self.start_game)
        layout.addWidget(self.start_button)
        self.setLayout(layout)

    def start_game(self):
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtGui.QPixmap(consts.CURSOR_PATH), 0, 0))

        window = MainWindow(self.screen)
        window.setWindowFlags(
            QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        window.show()

        self.hide()


class MainWindow(QtWidgets.QWidget):
    def __init__(self, screen):
        super(MainWindow, self).__init__()
        self.setMinimumSize(screen.width(), screen.height())
        self.setMaximumSize(screen.width(), screen.height())

        self.setWindowTitle(consts.TITLE)
        self.setWindowIcon(QtGui.QIcon(consts.ICON_PATH))

        self.screen = screen
        self.start_button = None
        self.game = None
        self.widget = None
        self.labels = None
        self.tower_buttons = None
        self.magic_buttons = None
        self.control_buttons = None

        self.start_game()

        self.showMaximized()

    def start_game(self):
        self.game = game.Game()

        self.widget = Graphics(
            self, self.screen.width(), self.screen.height(), self.game)

        cell_size = self.screen.width() / len(self.game.field[0])

        self.labels = []
        button_bias = self.set_elements(
            cell_size, 0, consts.LABEL_NAMES, Label, self.labels)

        self.tower_buttons = []
        self.magic_buttons = []
        self.control_buttons = []
        self.set_all_buttons(cell_size, button_bias)

    def set_all_buttons(self, cell_size, x_bias):
        bias = self.set_elements(cell_size, x_bias, consts.TOWERS_NAMES,
                                 TowerButton, self.tower_buttons)
        bias = self.set_elements(cell_size, bias, consts.MAGIC_NAMES,
                                 MagicButton, self.magic_buttons)
        return self.set_elements(cell_size, bias, consts.CONTROL_NAMES,
                                 ControlButton, self.control_buttons)

    def set_elements(self, cell_size, x_bias, names, element_type, elements):
        button_width = 0
        for i, name in enumerate(names):
            button = element_type(name, self, cell_size)
            button_width = button.size().width()
            button.move(button_width * i + x_bias, 0)
            elements.append(button)
        return button_width * len(elements) + x_bias

    def reset_buttons(self):
        for button in self.tower_buttons:
            button.set_button()


class Button(QtWidgets.QPushButton):
    def __init__(self, name, parent, cell_size):
        super().__init__('', parent)
        self.name = name
        self.parent = parent
        image_ratio = 1.125
        button_ratio = 1.5
        self.image_size = cell_size * image_ratio
        self.button_size = cell_size * button_ratio
        self.setMaximumSize(self.button_size, self.button_size)
        self.setMinimumSize(self.button_size, self.button_size)

        self.set_button()

        self.clicked.connect(self.react)

    def set_button(self):
        self.setIcon(QtGui.QIcon('{0}/{1}.png'.format(
            consts.TEXTURES_FOLDER, self.name)))
        self.setIconSize(QtCore.QSize(self.image_size, self.image_size))


class TowerButton(Button):
    _names = {'ArcaneTower': towers.ArcaneTower,
              'CanonTower': towers.CanonTower,
              'GuardTower': towers.GuardTower}

    def react(self):
        self.parent.reset_buttons()
        image = '{0}/{1}.png'.format(consts.TEXTURES_FOLDER, self.name)
        self.setIcon(QtGui.QIcon(self.create_border(image)))
        self.setIconSize(QtCore.QSize(self.button_size, self.button_size))
        self.parent.widget.choose_tower(TowerButton._names[self.name])

    def create_border(self, name):
        image = QtGui.QPixmap(name)
        overlay = QtGui.QPixmap(consts.BORDER_PATH)
        painter = QtGui.QPainter()
        painter.begin(image)
        painter.drawPixmap(0, 0, overlay)
        painter.end()
        return image


class MagicButton(Button):
    _names = {'LightningMagic': towers.CanonTower,
              'SwordMagic': towers.GuardTower}

    def react(self):
        pass


class ControlButton(Button):
    _names = {'Reset': towers.CanonTower,
              'Play': towers.GuardTower,
              'Pause': towers.CanonTower,
              'Slower': towers.GuardTower,
              'Faster': towers.CanonTower,
              'Restart': lambda: self.restart()}

    def react(self):
        if self.name == 'Restart':
            self.restart()

    def restart(self):
        self.parent.close()
        subprocess.call(consts.PROCESS_NAME, shell=True)


class Label(QtWidgets.QFrame):
    _names = {'Gold': lambda x: x.game.get_gold_number(),
              'Enemies': lambda x: x.game.get_remaining_enemies()}

    def __init__(self, name, parent, cell_size):
        super().__init__(parent)
        width_rate = 3
        height_rate = 1.5
        width = cell_size * width_rate
        height = cell_size * height_rate
        self.setMaximumSize(width, height)
        self.setMinimumSize(width, height)

        self.parent = parent
        self.text = name

        self.get_number = Label._names[name]

        self.label = QtWidgets.QLabel(
            '{0}: {1}'.format(name, self.get_number(self.parent)), self)
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
        self.label.setText('{0}: {1}'.format(self.text, self.get_number(self.parent)))


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
        self.attack_timers = {}
        self.creep_timers = {}

        self.chosen_tower = None

        self.spawn_timer = None
        self.wave_timer = None
        self.draw_timer = None
        self.count = 0
        self.multiplier = 1

    def initializeGL(self):
        self.cell_width = (2 * self.screen_width /
                           len(self.game.field[0]) / self.screen_width)
        self.cell_height = (2 * self.screen_height /
                            len(self.game.field) / self.screen_height)

        self.shader = Shader('shader.vs', 'shader.fs')
        self.shader.save_attr_locations(
            ['aVertexPosition', 'aVertexTexCoord'])
        self.shader.save_uniform_locations(['uTexture'])
        self.shader.bind()

        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glClearColor(255, 255, 255, 1)

        GL.glViewport(0, 0, self.screen_width, self.screen_height)
        self.setGeometry(0, 0, self.screen_width, self.screen_height)

        self.set_field()

        spawn_wave_time = consts.SPAWN_WAVE_TIME * self.multiplier
        self.spawn_timer = QtCore.QTimer()
        self.spawn_timer.timeout.connect(self.spawn_wave)
        self.spawn_timer.start(spawn_wave_time)

        self.draw_timer = QtCore.QTimer()
        self.draw_timer.timeout.connect(self.update)
        self.draw_timer.start(consts.REDRAW_TIME)

        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

    def paintGL(self):
        if self.game.end:
            return

        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

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
        if event.buttons() == QtCore.Qt.RightButton:
            self.parent.reset_buttons()
            self.chosen_tower = None
        if event.buttons() == QtCore.Qt.LeftButton:
            self.parent.reset_buttons()
            cell_width = math.floor(
                self.screen_width / len(self.game.field[0]))
            cell_height = math.floor(
                self.screen_height / len(self.game.field))
            cursor_pos = self.mapFromGlobal(QtGui.QCursor().pos())
            row = math.floor(cursor_pos.y() / cell_height)
            col = math.floor(cursor_pos.x() / cell_width)
            if not game_field.in_field(self.game.field, Point(row, col)):
                return
            if (not isinstance(self.game.field[row][col], game.Map) or
                    self.game.field[row][col].type != game_field.CellType.Grass):
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
            Image.open('{0}/{1}.png'.format(
                consts.TEXTURES_FOLDER, unit_type.__name__)))
        return quad

    def spawn_wave(self):
        creep_types = [creeps.Peon(0, 0),
                       creeps.Grunt(0, 0),
                       creeps.Raider(0, 0)]
        self.count = 0
        self.spawn(random.choice(creep_types), 5, creep_types)

    def spawn(self, creep, amount, types):
        if self.count == amount or self.game.end:
            self.wave_timer.stop()
            return
        self.count += 1
        point = self.game.portal

        unit = self.game.place_unit(point.row, point.col, type(creep))
        self.creeps[unit] = self.get_unit(
            point.row, point.col, type(creep))
        self.move_creep(unit)

        spawn_creep_time = consts.SPAWN_CREEP_TIME * self.multiplier
        self.wave_timer = QtCore.QTimer()
        next_type = random.choice(types)
        self.wave_timer.timeout.connect(
            lambda: self.spawn(next_type, amount, types))
        self.wave_timer.start(round(spawn_creep_time / creep.speed))

    def move_creep(self, creep):
        self.creeps.pop(creep, None)
        timer = self.creep_timers.pop(creep, None)
        stop = creep.move(self.game.field, self.game)
        bias = self.cell_height * 0.025
        row = creep.row
        col = creep.col
        priority = 0.2
        self.creeps[creep] = Mesh.get_quad(
            -1 + col * self.cell_width + bias,
            1 - row * self.cell_height - bias,
            -1 + (col + 1) * self.cell_width - bias,
            1 - (row + 1) * self.cell_height + bias,
            priority)
        health = consts.MAX_HEALTH[type(creep).__name__]
        rate = creep.health / health
        self.healths[creep] = Mesh.get_line(
            Point(row + 0.6, col - 0.4),
            Point(row + 0.6, col - 0.4 + rate),
            0.15,
            self.cell_width,
            self.cell_height)
        self.creeps[creep].set_texture(
            Image.open('{0}/{1}.png'.format(
                consts.TEXTURES_FOLDER, type(creep).__name__)))
        if stop is True:
            self.creeps.pop(creep, None)
            return
        if timer is None:
            move_creep_time = consts.MOVE_CREEP_TIME * self.multiplier
            timer = QtCore.QTimer()
            timer.timeout.connect(lambda: self.move_creep(creep))
            timer.start(round(move_creep_time / creep.speed))
        self.creep_timers[creep] = timer

    def attack(self, tower):
        enemy = tower.attack(self.game)
        if enemy:
            self.add_attack(tower, enemy)
        attack_delete_time = consts.ATTACK_DELETE_TIME * self.multiplier
        QtCore.QTimer.singleShot(
            attack_delete_time, lambda: self.delete_attack(tower))
        tower_attack_time = consts.TOWER_ATTACK_TIME * self.multiplier
        timer = QtCore.QTimer()
        timer.timeout.connect(lambda: self.attack(tower))
        timer.start(round(tower_attack_time / tower.speed))
        self.attack_timers[Point(tower.row, tower.col)] = timer

    def add_attack(self, tower, enemy):
        if tower.name != 'CanonTower':
            point1 = tower if tower.col < enemy.col else enemy
            point2 = tower if tower.col > enemy.col else enemy
            attack = Mesh.get_line(point1,
                                   point2,
                                   0.1,
                                   self.cell_width,
                                   self.cell_height)
            self.attacks[Point(tower.row, tower.col)] = attack
            return
        row = enemy.row + 0.5
        col = enemy.col + 0.5
        priority = 0.1
        self.attacks[Point(tower.row, tower.col)] = Mesh.get_quad(
            -1 + (col + tower.range) * self.cell_width,
            1 - (row - tower.range) * self.cell_height ,
            -1 + (col - tower.range) * self.cell_width,
            1 - (row + tower.range) * self.cell_height,
            priority)
        self.attacks[Point(tower.row, tower.col)].set_texture(
            Image.open('{0}/{1}.png'.format(
                consts.TEXTURES_FOLDER, 'Wave')))

    def delete_attack(self, tower):
        self.attacks.pop(Point(tower.row, tower.col), None)