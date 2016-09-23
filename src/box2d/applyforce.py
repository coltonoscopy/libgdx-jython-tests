import sys
sys.path.append('..')

from utils.imp import imp2d
imp2d('../../lib/')

from java.lang import Math

from com.badlogic.gdx import Gdx
from com.badlogic.gdx.Input import Keys
from com.badlogic.gdx.math import Vector2
from com.badlogic.gdx.physics.box2d import Body, BodyDef, EdgeShape, FixtureDef, PolygonShape, Transform, World
from com.badlogic.gdx.physics.box2d.BodyDef import BodyType
from com.badlogic.gdx.physics.box2d.joints import FrictionJointDef
from com.badlogic.gdx.backends.lwjgl import LwjglApplication, LwjglApplicationConfiguration, LwjglFiles, LwjglPreferences
from box2dtest import Box2DTest

class ApplyForce(Box2DTest):
    def __init__(self):
        super(ApplyForce, self).__init__()
        self.m_body = None
        self.tmp = Vector2()

    def createWorld(self, world):
        world.setGravity(Vector2(0, 0))

        k_restitution = 0.4

        bd = BodyDef()
        bd.position.set(0, 20)
        ground = world.createBody(bd)

        shape = EdgeShape()

        sd = FixtureDef()
        sd.shape = shape
        sd.density = 0
        sd.restitution = k_restitution

        shape.set(Vector2(-20, -20), Vector2(-20, 20))
        ground.createFixture(sd)

        shape.set(Vector2(20, -20), Vector2(20, 20))
        ground.createFixture(sd)

        shape.set(Vector2(-20, 20), Vector2(20, 20))
        ground.createFixture(sd)

        shape.set(Vector2(-20, -20), Vector2(20, -20))
        ground.createFixture(sd)

        shape.dispose()

        xf1 = Transform(Vector2(), 0.3524 * Math.PI)
        xf1.setPosition(xf1.mul(Vector2(1, 0)))

        vertices = [None, None, None]
        vertices[0] = xf1.mul(Vector2(-1, 0))
        vertices[1] = xf1.mul(Vector2(1, 0))
        vertices[2] = xf1.mul(Vector2(0, 0.5))

        poly1 = PolygonShape()
        poly1.set(vertices)

        sd1 = FixtureDef()
        sd1.shape = poly1
        sd1.density = 4.0

        xf2 = Transform(Vector2(), -0.3524 * Math.PI)
        xf2.setPosition(xf2.mul(Vector2(-1, 0)))

        vertices[0] = xf2.mul(Vector2(-1, 0))
        vertices[1] = xf2.mul(Vector2(1, 0))
        vertices[2] = xf2.mul(Vector2(0, 0.5))

        poly2 = PolygonShape()
        poly2.set(vertices)

        sd2 = FixtureDef()
        sd2.shape = poly2
        sd2.density = 2.0

        bd = BodyDef()
        bd.type = BodyType.DynamicBody
        bd.angularDamping = 5.0
        bd.linearDamping = 0.1

        bd.position.set(0, 2)
        bd.angle = Math.PI
        bd.allowSleep = False
        self.m_body = world.createBody(bd)
        self.m_body.createFixture(sd1)
        self.m_body.createFixture(sd2)
        poly1.dispose()
        poly2.dispose()

        shape = PolygonShape()
        shape.setAsBox(0.5, 0.5)

        fd = FixtureDef()
        fd.shape = shape
        fd.density = 1.0
        fd.friction = 0.3

        for i in range(10):
            bd = BodyDef()
            bd.type = BodyType.DynamicBody

            bd.position.set(0, 5 + 1.54 * i)
            body = world.createBody(bd)

            body.createFixture(fd)

            gravity = 10.0
            I = body.getInertia()
            mass = body.getMass()

            radius = Math.sqrt(2 * I / mass)

            jd = FrictionJointDef()
            jd.localAnchorA.set(0, 0)
            jd.localAnchorB.set(0, 0)
            jd.bodyA = ground
            jd.bodyB = body
            jd.collideConnected = True
            jd.maxForce = mass * gravity
            jd.maxTorque = mass * radius * gravity

            world.createJoint(jd)

        shape.dispose()

    def keyDown(self, keyCode):
        if keyCode == Keys.W:
            print 'Hit W!'
            f = self.m_body.getWorldVector(self.tmp.set(0, -200))
            p = self.m_body.getWorldPoint(self.tmp.set(0, 2))
            self.m_body.applyForce(f, p, True)
        if keyCode == Keys.A: self.m_body.applyTorque(50, True)
        if keyCode == Keys.D: self.m_body.applyTorque(-50, True)

        return False


if __name__ == '__main__':
    config = LwjglApplicationConfiguration()
    config.width = 640
    config.height = 480
    config.title = 'Apply Force Test'
    config.forceExit = False
    LwjglApplication(ApplyForce(), config)
