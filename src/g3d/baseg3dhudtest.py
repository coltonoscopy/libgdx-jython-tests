import sys
sys.path.append('..')

from utils.imp import imp, dump
imp('../../lib/')

from com.badlogic.gdx import Gdx, InputMultiplexer
from com.badlogic.gdx.math import MathUtils, Matrix4, Vector3
from com.badlogic.gdx.scenes.scene2d import Actor, InputEvent, Stage
from com.badlogic.gdx.scenes.scene2d.ui import CheckBox, Label, List, ScrollPane, Skin, Window
from com.badlogic.gdx.scenes.scene2d.utils import ChangeListener, ClickListener
from com.badlogic.gdx.utils import Scaling, StringBuilder
from com.badlogic.gdx.utils.viewport import ScalingViewport
from baseg3dtest import BaseG3dTest

class BaseG3dHudTest(BaseG3dTest):
    def __init__(self):
        super(BaseG3dHudTest, self).__init__()
        self.PREF_HUDWIDTH = 640
        self.PREF_HUDHEIGHT = 480
        self.rotationSpeed = 0.02 * 360.0   # degrees per second
        self.moveSpeed = 0.25               # cycles per second

        self.hud = None
        self.hudWidth = None
        self.hudHeight = None
        self.skin = None
        self.fpsLabel = None
        self.modelsWindow = None
        self.gridCheckBox = None
        self.rotateCheckBox = None
        self.moveCheckBox = None
        self.stringBuilder = StringBuilder()
        self.transform = Matrix4()
        self.moveRadius = 2.0

        self.models = [
            'car.obj', 'cube.obj', 'scene.obj', 'scene2.obj', 'wheel.obj', 'g3d/invaders.obj',
            'g3d/head.g3db', 'g3d/knight.g3dj', 'g3d/knight.g3db', 'g3d/monkey.g3db', 'g3d/ship.obj', 'g3d/shapes/cube_1.0x1.0.g3dj',
            'g3d/shapes/cube_1.5x1.5.g3dj', 'g3d/shapes/sphere.g3dj', 'g3d/shapes/teapot.g3dj', 'g3d/shapes/torus.g3dj'
        ]

        self.rotation = 0
        self.movement = 0

    def create(self):
        super(BaseG3dHudTest, self).create()

        self.createHUD()

        Gdx.input.setInputProcessor(InputMultiplexer([self.hud, self, self.inputController]))

    def createHUD(self):
        self.hud = Stage(ScalingViewport(Scaling.fit, self.PREF_HUDWIDTH, self.PREF_HUDHEIGHT))
        self.hudWidth = self.hud.getWidth()
        self.hudHeight = self.hud.getHeight()
        self.skin = Skin(Gdx.files.internal('../../data/uiskin.json'))

        modelsList = List(self.skin)
        modelsList.setItems(self.models)

        class ClickListenerNew(ClickListener):
            def __init__(self, test):
                self.test = test
            def clicked(self, event, x, y):
                if (self.test.modelsWindow.isCollapsed() and self.getTapCount() == 2):
                    self.test.onModelClicked(modelsList.getSelected())
                    self.test.modelsWindow.collapse()
        modelsList.addListener(ClickListenerNew(self))

        self.modelsWindow = self.addListWindow('Models', modelsList, 0, -1)

        self.fpsLabel = Label('FPS: 999', self.skin)
        self.hud.addActor(self.fpsLabel)
        self.gridCheckBox = CheckBox('Show grid', self.skin)
        self.gridCheckBox.setChecked(self.showAxes)

        class ChangeListenerNew(ChangeListener):
            def __init__(self, test):
                self.test = test
            def change(self, event, actor):
                self.test.showAxes = self.gridCheckBox.isChecked()

        self.gridCheckBox.addListener(ChangeListenerNew(self))
        self.gridCheckBox.setPosition(self.hudWidth - self.gridCheckBox.getWidth(), 0)
        self.hud.addActor(self.gridCheckBox)

        self.rotateCheckBox = CheckBox('Rotate', self.skin)
        self.rotateCheckBox.setChecked(True)
        self.rotateCheckBox.setPosition(self.hudWidth - self.rotateCheckBox.getWidth(), self.gridCheckBox.getHeight())
        self.hud.addActor(self.rotateCheckBox)

        self.moveCheckBox = CheckBox('Move', self.skin)
        self.moveCheckBox.setChecked(False)
        self.moveCheckBox.setPosition(self.hudWidth - self.moveCheckBox.getWidth(), self.rotateCheckBox.getTop())
        self.hud.addActor(self.moveCheckBox)

    def addListWindow(self, title, list, x, y):
        window = CollapsableWindow(title, self.skin)
        window.row()
        pane = ScrollPane(list, self.skin)
        pane.setFadeScrollBars(False)
        window.add(pane)
        window.pack()
        window.pack()
        if window.getHeight() > self.hudHeight:
            window.setHeight(self.hudHeight)
        window.setX(self.hudWidth - (window.getWidth() - (x + 1)) if x < 0 else x)
        window.setY(self.hudHeight - (window.getHeight() - (y + 1)) if y < 0 else y)
        window.layout()
        window.collapse()
        self.hud.addActor(window)
        pane.setScrollX(0)
        pane.setScrollY(0)
        return window

    def onModelClicked(self, name):
        raise NotImplementedError()

    def getStatus(self, stringBuilder):
        stringBuilder.append('FPS: ').append(Gdx.graphics.getFramesPerSecond())
        if self.loading: stringBuilder.append(' loading...')

    def render(self):
        self.transform.idt()
        if self.rotateCheckBox.isChecked():
            self.rotation = (self.rotation + self.rotationSpeed * Gdx.graphics.getRawDeltaTime()) % 360
            self.transform.rotate(Vector3.Y, self.rotation)
        if self.moveCheckBox.isChecked():
            self.movement = (self.movement + self.moveSpeed * Gdx.graphics.getRawDeltaTime()) % 1.0
            sm = MathUtils.sin(self.movement * MathUtils.PI2)
            cm = MathUtils.cos(self.movement * MathUtils.PI2)
            self.transform.trn(0, self.moveRadius * cm, self.moveRadius * sm)

        super(BaseG3dHudTest, self).render()

        self.stringBuilder.setLength(0)
        self.getStatus(self.stringBuilder)
        self.fpsLabel.setText(self.stringBuilder)
        self.hud.act(Gdx.graphics.getDeltaTime())
        self.hud.draw()

    def resize(self, width, height):
        super(BaseG3dHudTest, self).resize(width, height)
        self.hud.getViewport().update(width, height, True)
        self.hudWidth = self.hud.getWidth()
        self.hudHeight = self.hud.getHeight()

    def dispose(self):
        super(BaseG3dHudTest, self).dispose()
        self.skin.dispose()
        self.skin = None

class CollapsableWindow(Window):
    '''
    double click title to expand/collapse
    '''
    def __init__(self, title, skin):
        Window.__init__(self, title, skin)
        # super(CollapsableWindow, self).__init__(title, skin)
        self.collapsed = None
        self.collapseHeight = 20.0
        self.expandHeight = None

        class ClickListenerNew(ClickListener):
            def __init__(self, window):
                super(ClickListenerNew, self).__init__()
                self.window = window
            def clicked(self, event, x, y):
                if self.getTapCount() == 2 and self.window.getHeight() - y <= self.window.getPadTop() and y < self.window.getHeight() and x > 0 and x < self.window.getWidth():
                    self.window.toggleCollapsed()

        self.addListener(ClickListenerNew(self))

    def expand(self):
        if not self.collapsed: return
        self.setHeight(self.expandHeight)
        self.setY(self.getY() - self.expandHeight + self.collapseHeight)
        self.collapsed = False

    def collapse(self):
        if self.collapsed: return
        self.expandHeight = self.getHeight()
        self.setHeight(self.collapseHeight)
        self.setY(self.getY() + self.expandHeight - self.collapseHeight)
        self.collapsed = True
        if self.getStage(): self.getStage().setScrollFocus(None)

    def toggleCollapsed(self):
        self.expand() if self.collapsed else self.collapse()

    def isCollapsed(self):
        return self.collapsed
