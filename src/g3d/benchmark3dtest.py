import sys
sys.path.append('..')

from utils.imp import imp, frange
imp('../../lib/')

from com.badlogic.gdx import Gdx
from com.badlogic.gdx.Input import Buttons, Keys
from com.badlogic.gdx.graphics import Camera, Color
from com.badlogic.gdx.graphics.g3d import Environment, Model, ModelBatch, ModelInstance, Renderable
from com.badlogic.gdx.graphics.g3d.attributes import ColorAttribute, DirectionalLightsAttribute, PointLightsAttribute
from com.badlogic.gdx.graphics.g3d.environment import DirectionalLight, PointLight
from com.badlogic.gdx.graphics.g3d.model import Animation
from com.badlogic.gdx.graphics.g3d.shaders import DefaultShader
from com.badlogic.gdx.graphics.g3d.shaders.DefaultShader import Config
from com.badlogic.gdx.graphics.g3d.utils import AnimationController, DefaultShaderProvider, ShaderProvider
from com.badlogic.gdx.graphics.profiling import GLProfiler, GL20Profiler, GL30Profiler
from com.badlogic.gdx.backends.lwjgl import LwjglApplication, LwjglApplicationConfiguration, LwjglFiles, LwjglPreferences
from com.badlogic.gdx.math import MathUtils, Matrix4, Quaternion, Vector3
from com.badlogic.gdx.math.collision import BoundingBox
from com.badlogic.gdx.scenes.scene2d import Actor
from com.badlogic.gdx.scenes.scene2d.ui import CheckBox, Label
from com.badlogic.gdx.scenes.scene2d.utils import ChangeListener
from com.badlogic.gdx.scenes.scene2d.utils.ChangeListener import ChangeEvent
from com.badlogic.gdx.utils import Array, ObjectMap, StringBuilder
from baseg3dhudtest import BaseG3dHudTest

# @author Daniel Holderbaum
class Benchmark3DTest(BaseG3dHudTest):
    def __init__(self):
        self.environment = environment
        self.vertexCountLabel = None
        self.textureBindsLabel = None
        self.shaderSwitchesLabel = None
        self.drawCallsLabel = None
        self.glCallsLabel = None
        self.lightsLabel = None

        self.lightingCheckBox = None
        self.lightsCheckBox = None

        self.lighting = None

    def create(self):
        super(Benchmark3DTest, self).create()

        GLProfiler.enable()

        self.randomizeLights()

        self.cam.position.set(10, 10, 10)
        self.cam.lookAt(0, 0, 0)
        self.cam.update()
        self.showAxes = True
        self.lighting = True

        self.vertexCountLabel = Label('Vertices: 999', self.skin)
        self.vertexCountLabel.setPosition(0, self.fpsLabel.getTop())
        self.hud.addActor(self.vertexCountLabel)

        self.textureBindsLabel = Label('Texture bindings: 999', self.skin)
        self.textureBindsLabel.setPosition(0, self.vertexCountLabel.getTop())
        self.hud.addActor(self.textureBindsLabel)

        self.shaderSwitchesLabel = Label('Shader switches: 999', self.skin)
        self.shaderSwitchesLabel.setPosition(0, self.textureBindsLabel.getTop())
        self.hud.addActor(self.shaderSwitchesLabel)

        self.drawCallsLabel = Label('Draw calls: 999', self.skin)
        self.drawCallsLabel.setPosition(0, self.shaderSwitchesLabel.getTop())
        self.hud.addActor(self.drawCallsLabel)

        self.glCallsLabel = Label('GL calls: 999', self.skin)
        self.glCallsLabel.setPosition(0, self.drawCallsLabel.getTop())
        self.hud.addActor(self.glCallsLabel)

        self.lightsLabel = Label('Lights: 999', self.skin)
        self.lightsLabel.setPosition(0, self.glCallsLabel.getTop())
        self.hud.addActor(self.lightsLabel)

        self.lightingCheckBox = CheckBox('Lighting', self.skin)
        self.lightingCheckBox.setChecked(self.lighting)

        class ChangeListenerNew(ChangeListener):
            def __init__(self, test):
                self.test = test
            def changed(self, event, actor):
                self.test.lighting = test.lighting.lightingCheckBox.isChecked()

        self.lightingCheckBox.addListener(ChangeListenerNew(self))
        self.lightingCheckBox.setPosition(self.hudWidth - self.lightingCheckBox.getWidth(), self.gridCheckBox.getTop())
