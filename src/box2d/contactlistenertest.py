import sys
sys.path.append('..')

from utils.imp import imp2d
imp2d('../../lib/')

from java.lang import Math

from com.badlogic.gdx.math import Vector2
from com.badlogic.gdx.physics.box2d import Body, BodyDef, CircleShape, Contact, ContactImpulse, ContactListener, EdgeShape, FixtureDef, Manifold, PolygonShape, World
from com.badlogic.gdx.physics.box2d.BodyDef import BodyType
from com.badlogic.gdx.backends.lwjgl import LwjglApplication, LwjglApplicationConfiguration, LwjglFiles, LwjglPreferences
from box2dtest import Box2DTest

class ContactListenerTest(Box2DTest, ContactListener):
    def createWorld(self, world):
        world.setContactListener(self)
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
