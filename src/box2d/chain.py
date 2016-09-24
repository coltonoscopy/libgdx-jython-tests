import sys
sys.path.append('..')

from utils.imp import imp2d
imp2d('../../lib/')

from java.lang import Math

from com.badlogic.gdx.math import Vector2
from com.badlogic.gdx.physics.box2d import Body, BodyDef, EdgeShape, FixtureDef, PolygonShape, World
from com.badlogic.gdx.physics.box2d.BodyDef import BodyType
from com.badlogic.gdx.physics.box2d.joints import RevoluteJointDef
from com.badlogic.gdx.backends.lwjgl import LwjglApplication, LwjglApplicationConfiguration, LwjglFiles, LwjglPreferences
from box2dtest import Box2DTest

class Chain(Box2DTest):
    def createWorld(self, world):
        bd = BodyDef()
        ground = world.createBody(bd)

        shape = EdgeShape()
        shape.set(Vector2(-40, 0), Vector2(40, 0))

        ground.createFixture(shape, 0.0)
        shape.dispose()

        shape = PolygonShape()
        shape.setAsBox(0.6, 0.125)

        fd = FixtureDef()
        fd.shape = shape
        fd.density = 20.0
        fd.friction = 0.2

        jd = RevoluteJointDef()
        jd.collideConnected = False

        y = 25.0
        prevBody = ground

        for i in range(30):
            bd = BodyDef()
            bd.type = BodyType.DynamicBody
            bd.position.set(0.5 + i, y)
            body = world.createBody(bd)
            body.createFixture(fd)

            anchor = Vector2(i, y)
            jd.initialize(prevBody, body, anchor)
            world.createJoint(jd)
            prevBody = body

        shape.dispose()

if __name__ == '__main__':
    config = LwjglApplicationConfiguration()
    config.width = 640
    config.height = 480
    config.title = 'Chain Test'
    config.forceExit = False
    LwjglApplication(Chain(), config)
