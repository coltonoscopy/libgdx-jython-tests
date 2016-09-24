import sys
sys.path.append('..')

from utils.imp import imp2d
imp2d('../../lib/')

from java.lang import Math

from com.badlogic.gdx.math import Vector2
from com.badlogic.gdx.physics.box2d import Body, BodyDef, CircleShape, EdgeShape, FixtureDef, PolygonShape, World
from com.badlogic.gdx.physics.box2d.BodyDef import BodyType
from com.badlogic.gdx.physics.box2d.joints import PrismaticJointDef
from com.badlogic.gdx.backends.lwjgl import LwjglApplication, LwjglApplicationConfiguration, LwjglFiles, LwjglPreferences
from box2dtest import Box2DTest

class CollisionFiltering(Box2DTest):
    def __init__(self):
        self.k_smallGroup = 1
        self.k_largeGroup = -1

        self.k_defaultCategory = 0x0001
        self.k_triangleCategory = 0x0002
        self.k_boxCategory = 0x0004
        self.k_circleCategory = 0x0008

        self.k_triangleMask = -1
        self.k_boxMask = -1 ^ self.k_triangleCategory
        self.k_circleMask = -1

    def createWorld(self, world):
        shape = EdgeShape()
        shape.set(Vector2(-40.0, 0), Vector2(40, 0))

        fd = FixtureDef()
        fd.shape = shape
        fd.friction = 0.3

        bd = BodyDef()
        ground = world.createBody(bd)
        ground.createFixture(fd)
        shape.dispose()

        vertices = []
        vertices.append(Vector2(-1, 0))
        vertices.append(Vector2(1, 0))
        vertices.append(Vector2(0, 2))
        polygon = PolygonShape()
        polygon.set(vertices)

        triangleShapeDef = FixtureDef()
        triangleShapeDef.shape = polygon
        triangleShapeDef.density = 1.0

        triangleShapeDef.filter.groupIndex = self.k_smallGroup
        triangleShapeDef.filter.categoryBits = self.k_triangleCategory
        triangleShapeDef.filter.maskBits = self.k_triangleMask

        triangleBodyDef = BodyDef()
        triangleBodyDef.type = BodyType.DynamicBody
        triangleBodyDef.position.set(-5, 2)

        body1 = world.createBody(triangleBodyDef)
        body1.createFixture(triangleShapeDef)

        vertices[0].scl(2)
        vertices[1].scl(2)
        vertices[2].scl(2)

        polygon.set(vertices)
        triangleShapeDef.filter.groupIndex = self.k_largeGroup
        triangleBodyDef.position.set(-5, 6)
        triangleBodyDef.fixedRotation = True

        body2 = world.createBody(triangleBodyDef)
        body2.createFixture(triangleShapeDef)

        bd = BodyDef()
        bd.type = BodyType.DynamicBody
        bd.position.set(-5, 10)
        body = world.createBody(bd)

        p = PolygonShape()
        p.setAsBox(0.5, 1.0)
        body.createFixture(p, 1)

        jd = PrismaticJointDef()
        jd.bodyA = body2
        jd.bodyB = body
        jd.enableLimit = True
        jd.localAnchorA.set(0, 4)
        jd.localAnchorB.set(0, 0)
        jd.localAxisA.set(0, 1)
        jd.lowerTranslation = -1
        jd.upperTranslation = 1

        world.createJoint(jd)

        p.dispose()

        polygon.setAsBox(1, 0.5)
        boxShapeDef = FixtureDef()
        boxShapeDef.shape = polygon
        boxShapeDef.density = 1
        boxShapeDef.restitution = 0.1

        boxShapeDef.filter.groupIndex = self.k_smallGroup
        boxShapeDef.filter.categoryBits = self.k_boxCategory
        boxShapeDef.filter.maskBits = self.k_boxMask

        boxBodyDef = BodyDef()
        boxBodyDef.type = BodyType.DynamicBody
        boxBodyDef.position.set(0, 2)

        body3 = world.createBody(boxBodyDef)
        body3.createFixture(boxShapeDef)

        polygon.setAsBox(2, 1)
        boxShapeDef.filter.groupIndex = self.k_largeGroup
        boxBodyDef.position.set(0, 6)

        body4 = world.createBody(boxBodyDef)
        body4.createFixture(boxShapeDef)

        circle = CircleShape()
        circle.setRadius(1)

        circleShapeDef = FixtureDef()
        circleShapeDef.shape = circle
        circleShapeDef.density = 1.0

        circleShapeDef.filter.groupIndex = self.k_smallGroup
        circleShapeDef.filter.categoryBits = self.k_circleCategory
        circleShapeDef.filter.maskBits = self.k_circleMask

        circleBodyDef = BodyDef()
        circleBodyDef.type = BodyType.DynamicBody
        circleBodyDef.position.set(5, 2)

        body5 = world.createBody(circleBodyDef)
        body5.createFixture(circleShapeDef)

        circle.setRadius(2)
        circleShapeDef.filter.groupIndex = self.k_largeGroup
        circleBodyDef.position.set(5, 6)

        body6 = world.createBody(circleBodyDef)
        body6.createFixture(circleShapeDef)

if __name__ == '__main__':
    config = LwjglApplicationConfiguration()
    config.width = 1280
    config.height = 960
    config.title = 'Collision Filtering Test'
    config.forceExit = False
    LwjglApplication(CollisionFiltering(), config)
