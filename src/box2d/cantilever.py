import sys
sys.path.append('..')

from utils.imp import imp2d
imp2d('../../lib/')

from java.lang import Math

from com.badlogic.gdx.math import Vector2
from com.badlogic.gdx.physics.box2d import Body, BodyDef, CircleShape, EdgeShape, FixtureDef, PolygonShape, World
from com.badlogic.gdx.physics.box2d.BodyDef import BodyType
from com.badlogic.gdx.physics.box2d.joints import WeldJointDef
from com.badlogic.gdx.backends.lwjgl import LwjglApplication, LwjglApplicationConfiguration, LwjglFiles, LwjglPreferences
from box2dtest import Box2DTest

class Cantilever(Box2DTest):
    def __init__(self):
        self.m_middle = None
        self.e_count = 8

    def createWorld(self, world):
        bd = BodyDef()
        ground = world.createBody(bd)

        shape = EdgeShape()
        shape.set(Vector2(-40, 0), Vector2(40, 0))
        ground.createFixture(shape, 0)
        shape.dispose()

        shape = PolygonShape()
        shape.setAsBox(0.5, 0.125)

        fd = FixtureDef()
        fd.shape = shape
        fd.density = 20.0

        jd = WeldJointDef()

        prevBody = ground
        for i in range(self.e_count):
            bd = BodyDef()
            bd.type = BodyType.DynamicBody
            bd.position.set(-14.5 + 1.0 * i, 5.0)
            body = world.createBody(bd)
            body.createFixture(fd)

            anchor = Vector2(-15.0 + 1 * i, 5.0)
            jd.initialize(prevBody, body, anchor)
            world.createJoint(jd)
            prevBody = body

        shape.dispose()

        shape = PolygonShape()
        shape.setAsBox(0.5, 0.125)

        fd = FixtureDef()
        fd.shape = shape
        fd.density = 20.0

        jd = WeldJointDef()

        prevBody = ground
        for i in range(self.e_count):
            bd = BodyDef()
            bd.type = BodyType.DynamicBody
            bd.position.set(-14.5 + 1.0 * i, 15.0)
            bd.gravityScale = 10.0
            body = world.createBody(bd)
            body.createFixture(fd)

            anchor = Vector2(-15.0 + 1.0 * i, 15.0)
            jd.initialize(prevBody, body, anchor)
            world.createJoint(jd)

            prevBody = body

        shape.dispose()

        shape = PolygonShape()
        shape.setAsBox(0.5, 0.125)

        fd = FixtureDef()
        fd.shape = shape
        fd.density = 20.0

        jd = WeldJointDef()

        prevBody = ground
        for i in range(self.e_count):
            bd = BodyDef()
            bd.type = BodyType.DynamicBody
            bd.position.set(-4.5 + 1.0 * i, 5.0)
            body = world.createBody(bd)
            body.createFixture(fd)

            if i > 0:
                anchor = Vector2(-5.0 + 1.0 * i, 5.0)
                jd.initialize(prevBody, body, anchor)
                world.createJoint(jd)

            prevBody = body

        shape.dispose()

        shape = PolygonShape()
        shape.setAsBox(0.5, 0.125)

        fd = FixtureDef()
        fd.shape = shape
        fd.density = 20.0

        jd = WeldJointDef()

        prevBody = ground
        for i in range(self.e_count):
            bd = BodyDef()
            bd.type = BodyType.DynamicBody
            bd.position.set(5.5 + 1.0 * i, 10.0)
            bd.gravityScale = 10.0
            body = world.createBody(bd)
            body.createFixture(fd)

            if i > 0:
                anchor = Vector2(5.0 + 1.0 * i, 10.0)
                jd.initialize(prevBody, body, anchor)
                world.createJoint(jd)

            prevBody = body

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

        for i in range(2):
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
    config.title = 'Cantilever Test'
    config.forceExit = False
    LwjglApplication(Cantilever(), config)
