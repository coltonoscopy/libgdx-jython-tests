import sys
sys.path.append('..')

from utils.imp import imp
imp('../../lib/')

from java.lang import Math

from com.badlogic.gdx import Gdx
from com.badlogic.gdx.assets import AssetManager
from com.badlogic.gdx.graphics import GL20
from com.badlogic.gdx.graphics import OrthographicCamera, Texture
from com.badlogic.gdx.graphics.g2d import BitmapFont, SpriteBatch, TextureRegion
from com.badlogic.gdx.maps import MapLayers
from com.badlogic.gdx.maps.tiled import TiledMap, TiledMapRenderer, TiledMapTileLayer
from com.badlogic.gdx.maps.tiled.TiledMapTileLayer import Cell
from com.badlogic.gdx.maps.tiled.renderers import OrthogonalTiledMapRenderer
from com.badlogic.gdx.maps.tiled.tiles import StaticTiledMapTile
from com.badlogic.gdx.backends.lwjgl import LwjglApplication, LwjglApplicationConfiguration, LwjglFiles, LwjglPreferences
from utils.gdxtest import GdxTest
from utils.orthocamcontroller import OrthoCamController

class TiledMapBench(GdxTest):
    def __init__(self):
        self.map = None
        self.renderer = None
        self.camera = None
        self.cameraController = None
        self.assetManager = None
        self.tiles = None
        self.texture = None
        self.font = None
        self.batch = None

    def create(self):
        w = Gdx.graphics.getWidth()
        h = Gdx.graphics.getHeight()

        self.camera = OrthographicCamera()
        self.camera.setToOrtho(False, (w / h) * 320, 320)
        self.camera.update()

        self.cameraController = OrthoCamController(self.camera)
        Gdx.input.setInputProcessor(self.cameraController)

        self.font = BitmapFont()
        self.batch = SpriteBatch()

        self.tiles = Texture(Gdx.files.internal('../../data/maps/tiled/tiles.png'))
        splitTiles = TextureRegion.split(self.tiles, 32, 32)
        self.map = TiledMap()
        layers = self.map.getLayers()
        for l in range(20):
            layer = TiledMapTileLayer(150, 100, 32, 32)
            for x in range(150):
                for y in range(100):
                    ty = int(Math.random() * len(splitTiles))
                    tx = int(Math.random() * len(splitTiles[ty]))
                    cell = Cell()
                    cell.setTile(StaticTiledMapTile(splitTiles[ty][tx]))
                    layer.setCell(x, y, cell)
            layers.add(layer)

        self.renderer = OrthogonalTiledMapRenderer(self.map)

    def render(self):
        Gdx.gl.glClearColor(100.0 / 255.0, 100.0 / 255.0, 250.0 / 255.0, 1.0)
        Gdx.gl.glClear(GL20.GL_COLOR_BUFFER_BIT)
        self.camera.update()
        self.renderer.setView(self.camera)
        self.renderer.render()
        self.batch.begin()
        self.font.draw(self.batch, 'FPS: ' + str(Gdx.graphics.getFramesPerSecond()), 10, 20)
        self.batch.end()

if __name__ == '__main__':
    config = LwjglApplicationConfiguration()
    config.width = 640
    config.height = 480
    config.title = 'Tiled Map Bench Test'
    config.forceExit = False
    LwjglApplication(TiledMapBench(), config)
