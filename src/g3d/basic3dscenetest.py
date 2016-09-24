import sys
sys.path.append('..')

from utils.imp import imp
imp('../../lib/')

from com.badlogic.gdx import ApplicationListener, Gdx
from com.badlogic.gdx.assets import AssetManager
from com.badlogic.gdx.graphics import GL20, PerspectiveCamera
from com.badlogic.gdx.graphics.g3d import Environment, Model, ModelBatch, ModelInstance
from com.badlogic.gdx.graphics.g3d.attributes import ColorAttribute
from com.badlogic.gdx.graphics.g3d.environment import DirectionalLight
from com.badlogic.gdx.graphics.g3d.model import Node
from com.badlogic.gdx.graphics.g3d.utils import CameraInputController
from com.badlogic.gdx.backends.lwjgl import LwjglApplication, LwjglApplicationConfiguration, LwjglFiles, LwjglPreferences
from utils.gdxtest import GdxTest
from com.badlogic.gdx.utils import Array

class Basic3DSceneTest(GdxTest, ApplicationListener):
    def __init__(self):
        self.cam = None
        self.camController = None
        self.modelBatch = None
        self.assets = None
        self.instances = []
        self.lights = None
        self.loading = None

        self.blocks = []
        self.invaders = []
        self.ship = None
        self.space = None

    def create(self):
        self.modelBatch = ModelBatch()
        self.lights = Environment()
        self.lights.set(ColorAttribute(ColorAttribute.AmbientLight, 0.4, 0.4, 0.4, 1.0))
        self.lights.add(DirectionalLight().set(0.8, 0.8, 0.8, -1.0, -0.8, -0.2))

        self.cam = PerspectiveCamera(67, Gdx.graphics.getWidth(), Gdx.graphics.getHeight())
        self.cam.position.set(0.0, 7.0, 10.0)
        self.cam.lookAt(0, 0, 0)
        self.cam.near = 0.1
        self.cam.far = 300.0
        self.cam.update()

        self.camController = CameraInputController(self.cam)
        Gdx.input.setInputProcessor(self.camController)

        self.assets = AssetManager()
        self.assets.load('../../data/g3d/invaders.g3dj', Model)
        self.loading = True

    def doneLoading(self):
        model = self.assets.get('../../data/g3d/invaders.g3dj', Model)
        for i in range(model.nodes.size):
            id = model.nodes.get(i).id
            instance = ModelInstance(model, [id])
            node = instance.getNode(id)

            instance.transform.set(node.globalTransform)
            node.translation.set(0, 0, 0)
            node.scale.set(1, 1, 1)
            node.rotation.idt()
            instance.calculateTransforms()

            if id == 'space':
                self.space = instance
                continue

            self.instances.append(instance)

            if id == 'ship':
                self.ship = instance
            elif id.startswith('block'):
                self.blocks.append(instance)
            elif id.startswith('invader'): self.invaders.append(instance)

        self.loading = False

    def render(self):
        if self.loading and self.assets.update(): self.doneLoading()
        self.camController.update()

        Gdx.gl.glViewport(0, 0, Gdx.graphics.getBackBufferWidth(), Gdx.graphics.getBackBufferHeight())
        Gdx.gl.glClear(GL20.GL_COLOR_BUFFER_BIT | GL20.GL_DEPTH_BUFFER_BIT)

        self.modelBatch.begin(self.cam)
        for instance in self.instances:
            self.modelBatch.render(instance, self.lights)
        if self.space: self.modelBatch.render(self.space)
        self.modelBatch.end()

    def dispose(self):
        self.modelBatch.dispose()
        self.assets.dispose()

if __name__ == '__main__':
    config = LwjglApplicationConfiguration()
    config.width = 1280
    config.height = 960
    config.title = 'Basic 3D Scene Test'
    config.forceExit = False
    LwjglApplication(Basic3DSceneTest(), config)
