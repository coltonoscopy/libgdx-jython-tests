import sys
sys.path.append('..')

from utils.imp import imp, frange
imp('../../lib/')

from com.badlogic.gdx import Gdx
from com.badlogic.gdx.assets import AssetManager
from com.badlogic.gdx.graphics import Color, GL20, PerspectiveCamera
from com.badlogic.gdx.graphics.VertexAttributes import Usage
from com.badlogic.gdx.graphics.g3d import Material, Model, ModelBatch, ModelInstance
from com.badlogic.gdx.graphics.g3d.utils import CameraInputController, MeshPartBuilder, ModelBuilder
from com.badlogic.gdx.utils import Array
from utils.gdxtest import GdxTest

class BaseG3dTest(GdxTest):
    def __init__(self):
        self.assets = None

        self.cam = None
        self.inputController = None
        self.modelBatch = None
        self.axesModel = None
        self.axesInstance = None
        self.showAxes = True
        self.instances = []
        self.bgColor = Color(0, 0, 0, 1)

        self.GRID_MIN = -10.0
        self.GRID_MAX = 10.0
        self.GRID_STEP = 1.0

        self.loading = False

    def create(self):
        if not self.assets: self.assets = AssetManager()

        self.modelBatch = ModelBatch()

        self.cam = PerspectiveCamera(67, Gdx.graphics.getWidth(), Gdx.graphics.getHeight())
        self.cam.position.set(10.0, 10.0, 10.0)
        self.cam.lookAt(0, 0, 0)
        self.cam.near = 0.1
        self.cam.far = 1000.0
        self.cam.update()

        self.createAxes()

        self.inputController = CameraInputController(self.cam)
        Gdx.input.setInputProcessor(self.inputController)

    def createAxes(self):
        self.modelBuilder = ModelBuilder()
        self.modelBuilder.begin()
        self.builder = self.modelBuilder.part('grid', GL20.GL_LINES, Usage.Position | Usage.ColorUnpacked, Material())
        self.builder.setColor(Color.LIGHT_GRAY)
        for t in frange(self.GRID_MIN, self.GRID_MAX + 1, self.GRID_STEP):
            self.builder.line(t, 0, self.GRID_MIN, t, 0, self.GRID_MAX)
            self.builder.line(self.GRID_MIN, 0, t, self.GRID_MAX, 0, t)
        self.builder = self.modelBuilder.part('axes', GL20.GL_LINES, Usage.Position | Usage.ColorUnpacked, Material())
        self.builder.setColor(Color.RED)
        self.builder.line(0, 0, 0, 100, 0, 0)
        self.builder.setColor(Color.GREEN)
        self.builder.line(0, 0, 0, 0, 100, 0)
        self.builder.setColor(Color.BLUE)
        self.builder.line(0, 0, 0, 0, 0, 100)
        self.axesModel = self.modelBuilder.end()
        self.axesInstance = ModelInstance(self.axesModel)

    def render_3(self, batch, instances):
        raise NotImplementedError()

    def onLoaded(self):
        pass

    def render_2(self, instances):
        self.modelBatch.begin(self.cam)
        if self.showAxes: self.modelBatch.render(self.axesInstance)
        if self.instances: self.render_3(self.modelBatch, self.instances)
        self.modelBatch.end()

    def render(self):
        if self.loading and self.assets.update():
            self.loading = False
            self.onLoaded()

        self.inputController.update()

        Gdx.gl.glClear(GL20.GL_COLOR_BUFFER_BIT | GL20.GL_DEPTH_BUFFER_BIT)
        Gdx.gl.glClearColor(self.bgColor.r, self.bgColor.g, self.bgColor.b, self.bgColor.a)

        self.render_2(self.instances)

    def dispose(self):
        self.modelBatch.dispose()
        self.assets.dispose()
        self.assets = None
        self.axesModel.dispose()
        self.axesModel = None
