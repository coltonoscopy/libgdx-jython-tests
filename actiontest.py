import sys

sys.path.append('lib/gdx.jar')
sys.path.append('lib/gdx-backend-lwjgl.jar')
sys.path.append('lib/gdx-backend-lwjgl-natives.jar')
sys.path.append('lib/gdx-sources.jar')

from com.badlogic.gdx import Gdx
from com.badlogic.gdx.graphics import GL20, Texture
from com.badlogic.gdx.graphics.g2d import TextureRegion
from com.badlogic.gdx.scenes.scene2d import Stage
from com.badlogic.gdx.scenes.scene2d.actions import Actions
from com.badlogic.gdx.scenes.scene2d.ui import Image
from utils.gdxtest import GdxTest

if __name__ == '__main__':
    print 'Action Test'
