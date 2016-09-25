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
        super(Benchmark3DTest, self).__init__()
        self.environment = None
        self.vertexCountLabel = None
        self.textureBindsLabel = None
        self.shaderSwitchesLabel = None
        self.drawCallsLabel = None
        self.glCallsLabel = None
        self.lightsLabel = None

        self.lightingCheckBox = None
        self.lightsCheckBox = None

        self.lighting = None

        self.tmpV = Vector3()
        self.tmpQ = Quaternion()
        self.bounds = BoundingBox()

        self.currentlyLoading = None

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
        self.hud.addActor(self.lightingCheckBox)

        self.lightsCheckBox = CheckBox('Randomize lights', self.skin)
        self.lightsCheckBox.setChecked(False)

        class ChangeListenerNew2(ChangeListener):
            def __init__(self, test):
                self.test = test
            def changed(self, event, actor):
                self.test.lightsCheckBox.setChecked(False)
                self.test.randomizeLights()

        self.lightsCheckBox.addListener(ChangeListenerNew2(self))
        self.lightsCheckBox.setPosition(self.hudWidth - self.lightsCheckBox.getWidth(), self.lightingCheckBox.getTop())
        self.hud.addActor(self.lightsCheckBox)

        self.moveCheckBox.remove()
        self.rotateCheckBox.remove()

    def randomizeLights(self):
        pointLights = MathUtils.random(5)
        directionalLights = MathUtils.random(5)

        config = Config()
        config.numDirectionalLights = directionalLights
        config.numPointLights = pointLights
        config.numSpotLights = 0

        self.modelBatch.dispose()
        self.modelBatch = ModelBatch(DefaultShaderProvider(config))

        self.environment = Environment()
        self.environment.set(ColorAttribute(ColorAttribute.AmbientLight, 0.4, 0.4, 0.4, 1.0))

        for i in range(pointLights):
            self.environment.add(PointLight().set(self.randomColor(), self.randomPosition(), MathUtils.random(10.0)))

        for i in range(directionalLights):
            self.environment.add(DirectionalLight().set(self.randomColor(), self.randomPosition()))

    def randomColor(self):
        return Color(MathUtils.random(1.0), MathUtils.random(1.0), MathUtils.random(1.0), MathUtils.random(1.0))

    def randomPosition(self):
        return Vector3(MathUtils.random(-10.0, 10.0), MathUtils.random(-10.0, 10.0), MathUtils.random(-10.0, 10.0))

    def getStatus(self, stringBuilder):
        stringBuilder.setLength(0)
        stringBuilder.append('GL calls: ')
        stringBuilder.append(GLProfiler.calls)
        self.glCallsLabel.setText(stringBuilder)

        stringBuilder.setLength(0)
        stringBuilder.append('Draw calls: ')
        stringBuilder.append(GLProfiler.drawCalls)
        self.drawCallsLabel.setText(stringBuilder)

        stringBuilder.setLength(0)
        stringBuilder.append('Shader switches: ')
        stringBuilder.append(GLProfiler.shaderSwitches)
        self.shaderSwitchesLabel.setText(stringBuilder)

        stringBuilder.setLength(0)
        stringBuilder.append('Texture bindings: ')
        stringBuilder.append(GLProfiler.textureBindings)
        self.textureBindsLabel.setText(stringBuilder)

        stringBuilder.setLength(0)
        stringBuilder.append('Vertices: ')
        stringBuilder.append(GLProfiler.vertexCount.total)
        self.vertexCountLabel.setText(stringBuilder)

        dirLights = self.environment.get(DirectionalLightsAttribute.Type)
        pointLights = self.environment.get(PointLightsAttribute.Type)

        stringBuilder.setLength(0)
        stringBuilder.append('Lights: ')

        stringBuilder.append((0 if not dirLights else dirLights.lights.size) + (0 if not pointLights else pointLights.lights.size))
        stringBuilder.append(', Directional: ')
        stringBuilder.append(0 if not dirLights else dirLights.lights.size)
        stringBuilder.append(', Point: ')
        stringBuilder.append(0 if not pointLights else pointLights.lights.size)
        self.lightsLabel.setText(stringBuilder)

        GLProfiler.reset()

        stringBuilder.setLength(0)
        super(Benchmark3DTest, self).getStatus(stringBuilder)

    def render_3(self, batch, instances):
        batch.render(instances, self.environment) if self.lighting else batch.render(instances)

    def onModelClicked(self, name):
        if not name: return

        self.currentlyLoading = '../../data/' + name
        self.assets.load(self.currentlyLoading, Model)
        self.loading = True

    def onLoaded(self):
        if not self.currentlyLoading or len(self.currentlyLoading) == 0: return

        instance = ModelInstance(self.assets.get(self.currentlyLoading, Model))
        instance.transform = Matrix4().idt()
        instance.transform.setToTranslation(MathUtils.random(-10, 10), MathUtils.random(-10, 10), MathUtils.random(-10, 10))
        instance.transform.rotate(Vector3.X, MathUtils.random(-180, 180))
        instance.transform.rotate(Vector3.Y, MathUtils.random(-180, 180))
        instance.transform.rotate(Vector3.Z, MathUtils.random(-180, 180))
        self.instances.append(instance)

    def keyUp(self, keycode):
        if keycode == Keys.SPACE or keycode == Keys.MENU:
            self.onLoaded()
        return super(Benchmark3DTest, self).keyUp(keycode)

    def touchUp(self, screenX, screenY, pointer, button):
        self.onModelClicked(self.models[MathUtils.random(len(self.models) - 1)])
        return False

    def dispose(self):
        super(Benchmark3DTest, self).dispose()
        GLProfiler.disable()

if __name__ == '__main__':
    config = LwjglApplicationConfiguration()
    config.width = 1280
    config.height = 960
    config.title = 'Benchmark 3D Test'
    config.forceExit = False
    LwjglApplication(Benchmark3DTest(), config)
