import sys

sys.path.append('../lib/gdx.jar')
sys.path.append('../lib/gdx-backend-lwjgl.jar')
sys.path.append('../lib/gdx-backend-lwjgl-natives.jar')
sys.path.append('../lib/gdx-sources.jar')
sys.path.append('../lib/lwjgl-natives.jar')
sys.path.append('../lib/gdx-natives.jar')

from com.badlogic.gdx import Gdx
from com.badlogic.gdx.graphics import GL20, Texture
from com.badlogic.gdx.graphics.Texture import TextureFilter
from com.badlogic.gdx.graphics.g2d import TextureRegion
from com.badlogic.gdx.scenes.scene2d import Stage
from com.badlogic.gdx.scenes.scene2d.actions import Actions
from com.badlogic.gdx.scenes.scene2d.ui import Image
from com.badlogic.gdx.backends.lwjgl import LwjglApplication, LwjglApplicationConfiguration, LwjglFiles, LwjglPreferences
from utils.gdxtest import GdxTest

class ActionTest(GdxTest):
    def __init__(self):
        self.stage = None
        self.texture = None

    def create(self):
        self.stage = Stage()
        self.texture = Texture(Gdx.files.internal('../data/badlogic.jpg'), False)
        self.texture.setFilter(TextureFilter.Linear, TextureFilter.Linear)
        img = Image(TextureRegion(self.texture))
        img.setSize(100, 100)
        img.setOrigin(50, 50)
        img.setPosition(100, 100)

        img.addAction(Actions.moveBy(100, 0, 2))
        img.addAction(Actions.after(Actions.scaleTo(2, 2, 2)))

        self.stage.addActor(img)

    def render(self):
        Gdx.gl.glClear(GL20.GL_COLOR_BUFFER_BIT)
        self.stage.act(min(Gdx.graphics.getDeltaTime(), 1 / 30.0))
        self.stage.draw()

    def dispose(self):
        self.stage.dispose()
        self.texture.dispose()

if __name__ == '__main__':
    config = LwjglApplicationConfiguration()
    config.width = 640
    config.height = 480
    config.title = 'Action Test'
    config.forceExit = False
    LwjglApplication(ActionTest(), config)
