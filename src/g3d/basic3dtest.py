import sys
sys.path.append('..')

from utils.imp import imp
imp('../../lib/')

from com.badlogic.gdx import Gdx, InputMultiplexer
from com.badlogic.gdx.graphics import Color, GL20, PerspectiveCamera
from com.badlogic.gdx.graphics.VertexAttributes import Usage
from com.badlogic.gdx.graphics.g3d import Environment, Material, Model, ModelBatch, ModelInstance
from com.badlogic.gdx.graphics.g3d.attributes import ColorAttribute
from com.badlogic.gdx.graphics.g3d.environment import DirectionalLight
from com.badlogic.gdx.graphics.g3d.utils import CameraInputController, DefaultShaderProvider, ModelBuilder
from com.badlogic.gdx.backends.lwjgl import LwjglApplication, LwjglApplicationConfiguration, LwjglFiles, LwjglPreferences
from utils.gdxtest import GdxTest

class Basic3DTest(GdxTest):
    def __init__(self):
        self.cam = None
        self.inputController = None
        self.modelBatch = None
        self.model = None
        self.instance = None
        self.environment = None

    def create(self):
        self.modelBatch = ModelBatch(DefaultShaderProvider())

        self.environment = Environment()
        self.environment.set(ColorAttribute(ColorAttribute.AmbientLight, .4, .4, .4, 1.0))
        self.environment.add(DirectionalLight().set(0.8 ,0.8, 0.8, -1.0, -0.8, -0.2))

        self.cam = PerspectiveCamera(67, Gdx.graphics.getWidth(), Gdx.graphics.getHeight())
        self.cam.position.set(10.0, 10.0, 10.0)
        self.cam.lookAt(0, 0, 0)
        self.cam.near = 1.0
        self.cam.far = 30.0
        self.cam.update()

        modelBuilder = ModelBuilder()
        self.model = modelBuilder.createBox(5.0, 5.0, 5.0, Material([ColorAttribute.createDiffuse(Color.GREEN)]), Usage.Position | Usage.Normal)
        self.instance = ModelInstance(self.model)

        self.inputController = CameraInputController(self.cam)
        Gdx.input.setInputProcessor(InputMultiplexer([self, self.inputController]))

    def render(self):
        self.inputController.update()

        Gdx.gl.glViewport(0, 0, Gdx.graphics.getBackBufferWidth(), Gdx.graphics.getBackBufferHeight())
        Gdx.gl.glClear(GL20.GL_COLOR_BUFFER_BIT | GL20.GL_DEPTH_BUFFER_BIT)

        self.modelBatch.begin(self.cam)
        self.modelBatch.render(self.instance, self.environment)
        self.modelBatch.end()

    def dispose(self):
        self.modelBatch.dispose()
        self.model.dispose()

    def needsGl20(self):
        return True

    def resume(self):
        pass

    def resize(self, width, height):
        pass

    def pause(self):
        pass

if __name__ == '__main__':
    config = LwjglApplicationConfiguration()
    config.width = 1280
    config.height = 960
    config.title = 'Basic 3D Test'
    config.forceExit = False
    LwjglApplication(Basic3DTest(), config)
