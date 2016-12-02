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
        self.picture.setPixmap(QtGui.QPixmap(consts.START_LOGO_PATH))
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


class DefeatWindow(QtWidgets.QWidget):
    def __init__(self, screen, parent):
        super(DefeatWindow, self).__init__()
        self.screen = screen
        self.parent = parent
        self.setWindowTitle('Defeat')
        self.setWindowIcon(QtGui.QIcon(consts.ICON_PATH))
        self.setMinimumSize(screen.height() / 3, screen.height() / 3)
        self.setMaximumSize(screen.height() / 3, screen.height() / 3)

        layout = QtWidgets.QVBoxLayout()
        self.picture = QtWidgets.QLabel()
        self.picture.setScaledContents(True)
        self.picture.setPixmap(QtGui.QPixmap(consts.DEFEAT_LOGO_PATH))
        layout.addWidget(self.picture)

        self.retry_button = QtWidgets.QPushButton('Try Again', self)
        self.retry_button.clicked.connect(self.try_again)
        layout.addWidget(self.retry_button)

        self.quit_button = QtWidgets.QPushButton('Quit', self)
        self.quit_button.clicked.connect(self.quit)
        layout.addWidget(self.quit_button)

        self.setLayout(layout)

    def try_again(self):
        self.hide()
        self.parent.close()
        subprocess.call(consts.PROCESS_NAME, shell=True)

    def quit(self):
        self.parent.close()
        self.close()


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
        self.defeat_window = None
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

    def game_over(self):
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtGui.QPixmap(consts.CURSOR_PATH), 0, 0))

        self.defeat_window = DefeatWindow(self.screen, self)
        self.defeat_window.setWindowFlags(
            QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.defeat_window.show()


class Button(QtWidgets.QPushButton):
    def __init__(self, name, parent, cell_size):
        super().__init__('', parent)
        self.name = name
        self._names = {}
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
    def __init__(self, name, parent, cell_size):
        super().__init__(name, parent, cell_size)
        self._names = {'ArcaneTower': towers.ArcaneTower,
                       'CanonTower': towers.CanonTower,
                       'GuardTower': towers.GuardTower,
                       'MagicTower': towers.MagicTower}

    def react(self):
        if self.parent.widget.paused:
            return
        self.parent.reset_buttons()
        image = '{0}/{1}.png'.format(consts.TEXTURES_FOLDER, self.name)
        self.setIcon(QtGui.QIcon(self.create_border(image)))
        self.setIconSize(QtCore.QSize(self.button_size, self.button_size))
        self.parent.widget.choose_tower(self._names[self.name])

    @staticmethod
    def create_border(name):
        image = QtGui.QPixmap(name)
        overlay = QtGui.QPixmap(consts.BORDER_PATH)
        painter = QtGui.QPainter()
        painter.begin(image)
        painter.drawPixmap(0, 0, overlay)
        painter.end()
        return image


class MagicButton(Button):
    def __init__(self, name, parent, cell_size):
        super().__init__(name, parent, cell_size)
        self._names = {'FireMagic': self.parent.widget.cast_fire_magic,
                       'IceMagic': self.parent.widget.cast_ice_magic}

    def react(self):
        if self.parent.widget.paused:
            return
        self._names[self.name]()


class ControlButton(Button):
    def __init__(self, name, parent, cell_size):
        super().__init__(name, parent, cell_size)
        self._names = {'Reset': self.parent.widget.reset_speed,
                       'Pause': self.pause,
                       'Slower': self.parent.widget.decrease_speed,
                       'Faster': self.parent.widget.increase_speed,
                       'Restart': self.restart}

    def react(self):
        self._names[self.name]()

    def restart(self):
        self.parent.close()
        subprocess.call(consts.PROCESS_NAME, shell=True)

    def pause(self):
        path = consts.PLAY_PATH
        if self.parent.widget.paused:
            path = consts.PAUSE_PATH
        self.setIcon(QtGui.QIcon(path))
        self.setIconSize(QtCore.QSize(self.image_size, self.image_size))
        if self.parent.widget.paused:
            self.parent.widget.resume()
        else:
            self.parent.widget.pause()
        self.parent.widget.paused = not self.parent.widget.paused


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


class Timer(QtCore.QTimer):
    def __init__(self, func, time):
        super().__init__()
        self.func = func
        self.time = time
        self.remaining = 0
        self.onetime = False

    def start_timer(self):
        self.timeout.connect(self.func)
        self.start(self.time)

    def launch_once(self):
        self.onetime = True
        self.singleShot(self.time, self.func)

    def pause(self):
        self.remaining = self.remainingTime()
        self.stop()

    def resume(self):
        if self.remaining < 0:
            return
        if self.onetime:
            QtCore.QTimer.singleShot(self.remaining, self.func)
        else:
            QtCore.QTimer.singleShot(self.remaining, self.start_timer)


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
        self.auras = {}
        self.magic = {}
        self.attack_timers = {}
        self.creep_timers = {}
        self.attack_deletions = []
        self.magic_deletions = []
        self.debuff_deletions = []

        self.chosen_tower = None

        self.spawn_timer = None
        self.wave_timer = None
        self.draw_timer = None
        self.count = 0
        self.multiplier = consts.DEFAULT_MULTIPLIER
        self.multiplier_index = consts.DEFAULT_MULTIPLIER_INDEX
        self.paused = False
        self.over = False

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

        self.start_spawn()

        self.draw_timer = Timer(self.update, consts.REDRAW_TIME)
        self.draw_timer.start_timer()

        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

    def paintGL(self):
        if self.over:
            return
        if self.game.end:
            self.game_over()

        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        self.field_quad.draw(self.shader.handles)

        for tower in self.towers:
            tower.draw(self.shader.handles)

        for creep in self.creeps:
            self.creeps[creep].draw(self.shader.handles)
            self.healths[creep].draw(self.shader.handles)

        for spell in self.magic:
            self.magic[spell].draw(self.shader.handles)

        for attack in self.attacks:
            self.attacks[attack].draw(self.shader.handles)

        for aura in self.auras:
            self.auras[aura].draw(self.shader.handles)

    def mousePressEvent(self, event):
        if not self.chosen_tower or self.paused:
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

    def start_spawn(self):
        spawn_wave_time = consts.SPAWN_WAVE_TIME * self.multiplier
        self.spawn_timer = Timer(self.spawn_wave, spawn_wave_time)
        self.spawn_timer.start_timer()

    def spawn_wave(self):
        creep_types = [creeps.Peon(0, 0),
                       creeps.Grunt(0, 0),
                       creeps.Raider(0, 0),
                       creeps.Blademaster(0, 0),
                       creeps.Shaman(0, 0)]
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

        next_type = random.choice(types)
        spawn_creep_time = consts.SPAWN_CREEP_TIME / self.multiplier
        self.wave_timer = Timer(lambda: self.spawn(next_type, amount, types), round(spawn_creep_time / creep.speed))
        self.wave_timer.start_timer()

    def move_creep(self, creep):
        self.creeps.pop(creep, None)
        self.creep_timers.pop(creep, None)
        stop = creep.move(self.game)
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
        if creep.name == 'Shaman':
            self.set_aura(creep)
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
            self.auras.pop(creep, None)
            return
        move_creep_time = consts.MOVE_CREEP_TIME / self.multiplier
        timer = Timer(lambda: self.move_creep(creep), round(move_creep_time / creep.speed))
        timer.start_timer()
        self.creep_timers[creep] = timer

    def set_aura(self, creep):
        row = creep.row + 0.5
        col = creep.col + 0.5
        priority = 0.7
        aura = Mesh.get_quad(
            -1 + (col + 1) * self.cell_width,
            1 - (row - 1) * self.cell_height,
            -1 + (col - 1) * self.cell_width,
            1 - (row + 1) * self.cell_height,
            priority)
        aura.set_texture(Image.open(consts.AURA_PATH))
        self.auras[creep] = aura

    def attack(self, tower):
        enemy = tower.attack(self.game)
        if enemy:
            self.add_attack(tower, enemy)
        attack_delete_time = consts.ATTACK_DELETE_TIME / self.multiplier
        delete_timer = Timer(lambda: self.delete_attack(tower), attack_delete_time)
        delete_timer.launch_once()
        self.attack_deletions.append(delete_timer)
        tower_attack_time = consts.TOWER_ATTACK_TIME / self.multiplier
        timer = Timer(lambda: self.attack(tower), round(tower_attack_time / tower.speed))
        timer.start_timer()
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
        priority = 0.19
        self.attacks[Point(tower.row, tower.col)] = Mesh.get_quad(
            -1 + (col + tower.range) * self.cell_width,
            1 - (row - tower.range) * self.cell_height,
            -1 + (col - tower.range) * self.cell_width,
            1 - (row + tower.range) * self.cell_height,
            priority)
        self.attacks[Point(tower.row, tower.col)].set_texture(
            Image.open('{0}/{1}.png'.format(
                consts.TEXTURES_FOLDER, 'Wave')))

    def delete_attack(self, tower):
        self.attacks.pop(Point(tower.row, tower.col), None)

    def reset_speed(self):
        self.multiplier = consts.DEFAULT_MULTIPLIER
        self.multiplier_index = consts.DEFAULT_MULTIPLIER_INDEX

    def decrease_speed(self):
        if self.multiplier == consts.MIN_MULTIPLIER:
            return
        self.multiplier_index -= 1
        self.multiplier = consts.MULTIPLIERS[self.multiplier_index]

    def increase_speed(self):
        if self.multiplier == consts.MAX_MULTIPLIER:
            return
        self.multiplier_index += 1
        self.multiplier = consts.MULTIPLIERS[self.multiplier_index]

    def pause(self):
        if self.spawn_timer:
            self.spawn_timer.pause()
        if self.wave_timer:
            self.wave_timer.pause()
        for key in self.attack_timers:
            self.attack_timers[key].pause()
        for key in self.creep_timers:
            self.creep_timers[key].pause()
        for timer in self.attack_deletions:
            timer.pause()
        for timer in self.magic_deletions:
            timer.pause()
        for timer in self.debuff_deletions:
            timer.pause()

    def resume(self):
        if self.spawn_timer:
            self.spawn_timer.resume()
        if self.wave_timer:
            self.wave_timer.resume()
        for key in self.attack_timers:
            self.attack_timers[key].resume()
        for key in self.creep_timers:
            self.creep_timers[key].resume()
        for timer in self.attack_deletions:
            timer.resume()
        for timer in self.magic_deletions:
            timer.resume()
        for timer in self.debuff_deletions:
            timer.resume()

    def cast_fire_magic(self):
        point = self.game.cast_fire()
        if not point:
            return
        row = point.row + 0.5
        col = point.col + 0.5
        priority = 0.04
        fire = Mesh.get_quad(
            -1 + (col + consts.FIRE_RADIUS) * self.cell_width,
            1 - (row - consts.FIRE_RADIUS) * self.cell_height,
            -1 + (col - consts.FIRE_RADIUS) * self.cell_width,
            1 - (row + consts.FIRE_RADIUS) * self.cell_height,
            priority)
        fire.set_texture(Image.open(consts.FIRE_PATH))
        self.magic[point] = fire
        magic_delete = Timer(lambda: self.magic.pop(point, None), consts.FIRE_DURATION)
        magic_delete.launch_once()
        self.magic_deletions.append(magic_delete)

    def cast_ice_magic(self):
        point = self.game.cast_ice()
        if not point:
            return
        row = point.row + 0.5
        col = point.col + 0.5
        priority = 0.8
        wind = Mesh.get_quad(
            -1 + (col + consts.ICE_RADIUS) * self.cell_width,
            1 - (row - consts.ICE_RADIUS) * self.cell_height,
            -1 + (col - consts.ICE_RADIUS) * self.cell_width,
            1 - (row + consts.ICE_RADIUS) * self.cell_height,
            priority)
        wind.set_texture(Image.open(consts.WIND_PATH))
        self.magic[point] = wind
        magic_delete = Timer(lambda: self.magic.pop(point, None), consts.ICE_DURATION)
        magic_delete.launch_once()
        self.magic_deletions.append(magic_delete)
        debuff_delete = Timer(lambda: self.game.disable_ice_debuff(), consts.ICE_DURATION)
        debuff_delete.launch_once()
        self.magic_deletions.append(debuff_delete)

    def game_over(self):
        self.over = True
        self.parent.game_over()