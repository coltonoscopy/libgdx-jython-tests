import sys

sys.path.append('lib/gdx.jar')
sys.path.append('lib/gdx-sources.jar')

from com.badlogic.gdx import ApplicationListener
from com.badlogic.gdx import InputAdapter

class GdxTest(InputAdapter, ApplicationListener):
    def create(self):
        raise NotImplementedError()

    def resume(self):
        raise NotImplementedError()

    def render(self):
        raise NotImplementedError()

    def resize(self, width, height):
        raise NotImplementedError()

    def pause(self):
        raise NotImplementedError()

    def dispose(self):
        raise NotImplementedError()
