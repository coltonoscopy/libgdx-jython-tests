import sys
sys.path.append('..')

from utils.imp import imp2d
imp2d('../../lib/')

from java.lang import Math

from com.badlogic.gdx.math import Vector2
from com.badlogic.gdx.physics.box2d import Body, BodyDef, CircleShape, EdgeShape, FixtureDef, PolygonShape, World
from com.badlogic.gdx.physics.box2d.BodyDef import BodyType
from com.badlogic.gdx.physics.box2d.joints import RevoluteJointDef
from com.badlogic.gdx.backends.lwjgl import LwjglApplication, LwjglApplicationConfiguration, LwjglFiles, LwjglPreferences
from box2dtest import Box2DTest

class Bridge(Box2DTest):
    def __init__(self):
        self.e_count = 30

    def createWorld(self, world):
        bd = BodyDef()
        ground = world.createBody(bd)

        shape = EdgeShape()
        shape.set(Vector2(-40, 0), Vector2(40.0, 0))

        ground.createFixture(shape, 0)
        shape.dispose()

        shape = PolygonShape()
        shape.setAsBox(0.5, 0.125)
        fd = FixtureDef()
        fd.shape = shape
        fd.density = 20.0
        fd.friction = 0.2

        jd = RevoluteJointDef()

        prevBody = ground

        for i in range(self.e_count):
            bd = BodyDef()
            bd.type = BodyType.DynamicBody
            bd.position.set(-14.5 + 1.0 * i, 5.0)
            body = world.createBody(bd)
            body.createFixture(fd)

            anchor = Vector2(-15.0 + 1.0 * i, 5.0)
            jd.initialize(prevBody, body, anchor)
            world.createJoint(jd)
            prevBody = body

        anchor = Vector2(-15.0 + 1.0 * self.e_count, 5.0)
        jd.initialize(prevBody, ground, anchor)
        world.createJoint(jd)
        shape.dispose()

        for i in range(2):
            vertices = []
            vertices.append(Vector2(-0.5, 0))
            vertices.append(Vector2(0.5, 0))
            vertices.append(Vector2(0, 1.5))

            shape = PolygonShape()
            shape.set(vertices)

            fd = FixtureDef()
            fd.shape = shape
            fd.density = 1.0

            bd = BodyDef()
            bd.type = BodyType.DynamicBody
            bd.position.set(-8.0 + 8.0 * i, 12.0)
            body = world.createBody(bd)
            body.createFixture(fd)

            shape.dispose()

        for i in range(3):
            shape = CircleShape()
            shape.setRadius(0.5)

            fd = FixtureDef()
            fd.shape = shape
            fd.density = 1.0

            bd = BodyDef()
            bd.type = BodyType.DynamicBody
            bd.position.set(-6.0 + 6.0 * i, 10.0)

            body = world.createBody(bd)
            body.createFixture(fd)

            shape.dispose()

if __name__ == '__main__':
    config = LwjglApplicationConfiguration()
    config.width = 640
    config.height = 480
    config.title = 'Bridge Test'
    config.forceExit = False
    LwjglApplication(Bridge(), config)
