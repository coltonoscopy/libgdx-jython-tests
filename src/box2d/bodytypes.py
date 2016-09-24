import sys
sys.path.append('..')

from utils.imp import imp2d
imp2d('../../lib/')

from java.lang import Math

from com.badlogic.gdx.Input import Keys
from com.badlogic.gdx.math import Vector2
from com.badlogic.gdx.physics.box2d import Body, BodyDef, EdgeShape, FixtureDef, PolygonShape, World
from com.badlogic.gdx.physics.box2d.BodyDef import BodyType
from com.badlogic.gdx.physics.box2d.joints import PrismaticJointDef
from com.badlogic.gdx.physics.box2d.joints import RevoluteJointDef
from com.badlogic.gdx.backends.lwjgl import LwjglApplication, LwjglApplicationConfiguration, LwjglFiles, LwjglPreferences
from box2dtest import Box2DTest

class BodyTypes(Box2DTest):
    def __init__(self):
        self.m_attachment = None
        self.m_platform = None
        self.m_speed = None
        self.tmp = Vector2()

    def createWorld(self, world):
        ground = None

        bd = BodyDef()
        ground = world.createBody(bd)

        shape = EdgeShape()
        shape.set(Vector2(-20, 0), Vector2(20, 0))

        fd = FixtureDef()
        fd.shape = shape
        ground.createFixture(fd)
        shape.dispose()

        bd = BodyDef()
        bd.type = BodyType.DynamicBody
        bd.position.set(0, 3.0)
        self.m_attachment = world.createBody(bd)

        shape = PolygonShape()
        shape.setAsBox(0.5, 2.0)
        self.m_attachment.createFixture(shape, 2.0)
        shape.dispose()

        bd = BodyDef()
        bd.type = BodyType.DynamicBody
        bd.position.set(-4.0, 5.0)
        self.m_platform = world.createBody(bd)

        shape = PolygonShape()
        shape.setAsBox(0.5, 4.0, Vector2(4.0, 0), 0.5 * Math.PI)

        fd = FixtureDef()
        fd.shape = shape
        fd.friction = 0.6
        fd.density = 2.0

        self.m_platform.createFixture(fd)
        shape.dispose()

        rjd = RevoluteJointDef()
        rjd.initialize(self.m_attachment, self.m_platform, Vector2(0, 5.0))
        rjd.maxMotorTorque = 50.0
        rjd.enableMotor = True
        world.createJoint(rjd)

        pjd = PrismaticJointDef()
        pjd.initialize(ground, self.m_platform, Vector2(0, 5.0), Vector2(1, 0))

        pjd.maxMotorForce = 1000.0
        pjd.enableMotor = True
        pjd.lowerTranslation = -10.0
        pjd.upperTranslation = 10.0
        pjd.enableLimit = True

        world.createJoint(pjd)

        self.m_speed = 3.0

        bd = BodyDef()
        bd.type = BodyType.DynamicBody
        bd.position.set(0, 8.0)
        body = world.createBody(bd)

        shape = PolygonShape()
        shape.setAsBox(0.75, 0.75)

        fd = FixtureDef()
        fd.shape = shape
        fd.friction = 0.6
        fd.density = 2.0

        body.createFixture(fd)
        shape.dispose()

    def keyDown(self, keyCode):
        if keyCode == Keys.D: self.m_platform.setType(BodyType.DynamicBody)
        if keyCode == Keys.S: self.m_platform.setType(BodyType.StaticBody)
        if keyCode == Keys.K:
            self.m_platform.setType(BodyType.KinematicBody)
            self.m_platform.setLinearVelocity(self.tmp.set(-self.m_speed, 0))
            self.m_platform.setAngularVelocity(0)

        return False

    def render(self):
        if type(self.m_platform) == BodyType.KinematicBody:
            p = self.m_platform.getTransform().getPosition()
            v = self.m_platform.getLinearVelocity()

            if (p.x < -10 and v.x > 0) or (p.x > 10 and v.x > 0):
                v.x = -v.x
                self.m_platform.setLinearVelocity(v)

        super(BodyTypes, self).render()

if __name__ == '__main__':
    config = LwjglApplicationConfiguration()
    config.width = 640
    config.height = 480
    config.title = 'Action Test'
    config.forceExit = False
    LwjglApplication(BodyTypes(), config)
