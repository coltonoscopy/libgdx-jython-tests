import sys
sys.path.append('..')

from utils.imp import imp2d
imp2d('../../lib/')

from com.badlogic.gdx import ApplicationListener, Gdx, InputProcessor
from com.badlogic.gdx.graphics import GL20, OrthographicCamera
from com.badlogic.gdx.graphics.g2d import BitmapFont, SpriteBatch
from com.badlogic.gdx.math import Vector2, Vector3
from com.badlogic.gdx.physics.box2d import Body, BodyDef, Box2DDebugRenderer, Fixture, QueryCallback, World
from com.badlogic.gdx.physics.box2d.BodyDef import BodyType
from com.badlogic.gdx.physics.box2d.joints import MouseJoint, MouseJointDef
from com.badlogic.gdx.utils import TimeUtils

class Box2DTest(ApplicationListener, InputProcessor):
    '''
    Base class for all Box2D Testbed tests, all subclasses must implement
    the createWorld() method.
    '''
    def __init__(self):
        # the camera
        self.camera = None

        # the renderer
        self.renderer = None

        self.batch = None
        self.font = None

        # our box2D world
        self.world = None

        # ground body to connect the mouse joint to
        self.groundBody = None

        # our mouse joint
        self.mouseJoint = None

        # a hit body
        self.hitBody = None

        self.testPoint = Vector3()
        self.callback = Box2DTest.QueryCallbackNew(self)

        # temp vector
        self.tmp = Vector2()

        # another temporary vector
        self.target = Vector2()

    def createWorld(self, world):
        raise NotImplementedError()

    def render(self):
        # update the world with a fixed time step
        startTime = TimeUtils.nanoTime()
        self.world.step(Gdx.app.getGraphics().getDeltaTime(), 3, 3)
        updateTime = (TimeUtils.nanoTime() - startTime) / 1000000000.0

        startTime = TimeUtils.nanoTime()
        # clear the screen and set up the projection matrix
        Gdx.gl.glClear(GL20.GL_COLOR_BUFFER_BIT)
        self.camera.update()

        # render the world using the debug renderer
        self.renderer.render(self.world, self.camera.combined)
        renderTime = (TimeUtils.nanoTime() - startTime) / 1000000000.0

        self.batch.begin()
        self.font.draw(self.batch, 'fps:' + str(Gdx.graphics.getFramesPerSecond()) + ', update: ' + str(updateTime) + ', render: ' + str(renderTime), 0, 20)
        self.batch.end()

    def create(self):
        '''
        setup the camera. In Box2D we operate on a
        meter scale, pixels won't do it. So we use
        an orthographic camera with a viewport of
        48 meters in width and 32 meters in height.
        we also position the camera so that it
        looks at (0, 16) (that's where the middle of the
        screen will be located).
        '''
        self.camera = OrthographicCamera(48, 32)
        self.camera.position.set(0, 15, 0)

        # create the debug renderer
        self.renderer = Box2DDebugRenderer()

        # create the world
        self.world = World(Vector2(0, -10), True)

        # we also need an invisible zero size ground body
        # to which we can connect the mouse joint
        bodyDef = BodyDef()
        self.groundBody = self.world.createBody(bodyDef)

        # call abstract method to populate the world
        self.createWorld(self.world)

        self.batch = SpriteBatch()
        self.font = BitmapFont(Gdx.files.internal('../data/arial-15.fnt'), False)

        Gdx.input.setInputProcessor(self)

    def dispose(self):
        self.renderer.dispose()
        self.world.dispose()

        self.renderer = None
        self.world = None
        self.mouseJoint = None
        self.hitBody = None

    def keyDown(self, keycode):
        return False

    def keyTyped(self, character):
        return False

    def keyUp(self, keycode):
        return False

    class QueryCallbackNew(QueryCallback):
        def __init__(self, test):
            self.test = test

        def reportFixture(self, fixture):
            # if the hit point is inside the fixture of the body
            # we report it
            if fixture.testPoint(self.test.testPoint.x, self.test.testPoint.y):
                self.test.hitBody = fixture.getBody()
                return False
            else:
                return True

    def touchDown(self, x, y, pointer, button):
        print 'Touch down!'
        # translate the mouse coordinates to world coordinates
        self.camera.unproject(self.testPoint.set(x, y, 0))
        # ask the world which bodies are within the given
        # bounding box around the mouse pointer
        self.hitBody = None
        self.world.QueryAABB(self.callback, self.testPoint.x - 0.0001, self.testPoint.y - 0.0001, self.testPoint.x + 0.0001, self.testPoint.y + 0.0001)

        if self.hitBody == self.groundBody: self.hitBody = None

        # ignore kinematic bodies, they don't work with the mouse joint
        if self.hitBody != None and self.hitBody.getType() == BodyType.KinematicBody: return False

        # if we hit something we create a new mouse joint
        # and attach it to the hit body
        if self.hitBody != None:
            deff = MouseJointDef()
            deff.bodyA = self.groundBody
            deff.bodyB = self.hitBody
            deff.collideConnected = True
            deff.target.set(self.testPoint.x, self.testPoint.y)
            deff.maxForce = 1000 * self.hitBody.getMass()

            self.mouseJoint = self.world.createJoint(deff)
            self.hitBody.setAwake(True)

        return False

    def touchDragged(self, x, y, pointer):
        '''
        if a mouse joint exists we simply update
        the target of the joint based on the new
        mouse coordinates
        '''
        print 'Touch dragged!'
        if self.mouseJoint:
            self.camera.unproject(self.testPoint.set(x, y, 0))
            self.mouseJoint.setTarget(self.target.set(self.testPoint.x, self.testPoint.y))
        return False

    def touchUp(self, x, y, pointer, button):
        # if a mouse joint exists we simply destroy it
        print 'Touch up!'
        if self.mouseJoint:
            self.world.destroyJoint(self.mouseJoint)
            self.mouseJoint = None
        return False

    def mouseMoved(self, x, y):
        return False

    def scrolled(self, amount):
        return False

    def pause(self):
        pass

    def resume(self):
        pass

    def resize(self, width, height):
        pass
