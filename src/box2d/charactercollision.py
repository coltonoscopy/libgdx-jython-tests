import sys
sys.path.append('..')

from utils.imp import imp2d
imp2d('../../lib/')

from java.lang import Math

from com.badlogic.gdx.math import Vector2
from com.badlogic.gdx.physics.box2d import Body, BodyDef, CircleShape, EdgeShape, FixtureDef, PolygonShape, World
from com.badlogic.gdx.physics.box2d.BodyDef import BodyType
from com.badlogic.gdx.backends.lwjgl import LwjglApplication, LwjglApplicationConfiguration, LwjglFiles, LwjglPreferences
from box2dtest import Box2DTest

class CharacterCollision(Box2DTest):
    def createWorld(self, world):
        bd = BodyDef()
        ground = world.createBody(bd)

        shape = EdgeShape()
        shape.set(Vector2(-20, 0), Vector2(20, 0))
        ground.createFixture(shape, 0)
        shape.dispose()

        bd = BodyDef()
        ground = world.createBody(bd)

        shape = EdgeShape()
        shape.setRadius(0)
        shape.set(Vector2(-8, 1), Vector2(-6, 1))
        ground.createFixture(shape, 0)
        shape.set(Vector2(-6, 1), Vector2(-4, 1))
        ground.createFixture(shape, 0)
        shape.set(Vector2(-4, 1), Vector2(-2, 1))
        ground.createFixture(shape, 0)
        shape.dispose()

        bd = BodyDef()
        ground = world.createBody(bd)

        shape = PolygonShape()
        shape.setAsBox(1, 1, Vector2(4, 3), 0)
        ground.createFixture(shape, 0)
        shape.setAsBox(1, 1, Vector2(6, 3), 0)
        ground.createFixture(shape, 0)
        shape.setAsBox(1, 1, Vector2(8, 3), 0)
        ground.createFixture(shape, 0)
        shape.dispose()

        bd = BodyDef()
        ground = world.createBody(bd)

        shape = EdgeShape()
        d = 2 * 2 * 0.005
        shape.setRadius(0)
        shape.set(Vector2(-1 + d, 3), Vector2(1 - d, 3))
        ground.createFixture(shape, 0)
        shape.set(Vector2(1, 3 + d), Vector2(1, 5 - d))
        ground.createFixture(shape, 0)
        shape.set(Vector2(1 - d, 5), Vector2(-1 + d, 5))
        ground.createFixture(shape, 0)
        shape.set(Vector2(-1, 5 - d), Vector2(-1, 3 + d))
        ground.createFixture(shape, 0)
        shape.dispose()

        bd = BodyDef()
        bd.position.set(-3, 5)
        bd.type = BodyType.DynamicBody
        bd.fixedRotation = True
        bd.allowSleep = False

        body = world.createBody(bd)

        shape = PolygonShape()
        shape.setAsBox(0.5, 0.5)

        fd = FixtureDef()
        fd.shape = shape
        fd.density = 20.0
        body.createFixture(fd)
        shape.dispose()

        bd = BodyDef()
        bd.position.set(-5, 5)
        bd.type = BodyType.DynamicBody
        bd.fixedRotation = True
        bd.allowSleep = False

        body = world.createBody(bd)

        angle = 0.0
        delta = Math.PI / 3
        vertices = []
        for i in range(6):
            vertices.append(Vector2(0.5 * Math.cos(angle), 0.5 * Math.sin(angle)))
            angle += delta

        shape = PolygonShape()
        shape.set(vertices)

        fd = FixtureDef()
        fd.shape = shape
        fd.density = 20.0
        body.createFixture(fd)
        shape.dispose()

        bd = BodyDef()
        bd.position.set(3, 5)
        bd.type = BodyType.DynamicBody
        bd.fixedRotation = True
        bd.allowSleep = False

        body = world.createBody(bd)

        shape = CircleShape()
        shape.setRadius(0.5)

        fd = FixtureDef()
        fd.shape = shape
        fd.density = 20.0
        body.createFixture(fd)
        shape.dispose()

if __name__ == '__main__':
    config = LwjglApplicationConfiguration()
    config.width = 1280
    config.height = 960
    config.title = 'Character Collision Test'
    config.forceExit = False
    LwjglApplication(CharacterCollision(), config)
