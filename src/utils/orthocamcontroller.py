from imp import imp
imp('../../lib/')

from com.badlogic.gdx import InputAdapter
from com.badlogic.gdx.graphics import OrthographicCamera
from com.badlogic.gdx.math import Vector3

class OrthoCamController(InputAdapter):
    def __init__(self, camera):
        self.camera = None
        self.curr = Vector3()
        self.last = Vector3(-1, -1, -1)
        self.delta = Vector3()
        self.camera = camera

    def touchDragged(self, x, y, pointer):
        self.camera.unproject(self.curr.set(x, y, 0))
        if not (self.last.x == -1 and self.last.y == -1 and self.last.z == -1):
            self.camera.unproject(self.delta.set(self.last.x, self.last.y, 0))
            self.delta.sub(self.curr)
            self.camera.position.add(self.delta.x, self.delta.y, 0)
        self.last.set(x, y, 0)
        return False

    def touchUp(self, x, y, pointer, button):
        self.last.set(-1, -1, -1)
        return False
