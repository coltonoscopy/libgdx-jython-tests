import sys
sys.path.append('..')

from utils.imp import imp, frange
imp('../../lib/')

from com.badlogic.gdx import Gdx
from com.badlogic.gdx.Input import Keys
from com.badlogic.gdx.graphics import GL20, Texture
from com.badlogic.gdx.graphics.VertexAttributes import Usage
from com.badlogic.gdx.graphics.g3d import Environment, Material, Model, ModelBatch, ModelInstance
from com.badlogic.gdx.graphics.g3d.attributes import BlendingAttribute, ColorAttribute, FloatAttribute, TextureAttribute
from com.badlogic.gdx.graphics.g3d.environment import DirectionalShadowLight
from com.badlogic.gdx.graphics.g3d.model import Animation, Node
from com.badlogic.gdx.graphics.g3d.utils import AnimationController, DepthShaderProvider, MeshBuilder, MeshPartBuilder, ModelBuilder
from com.badlogic.gdx.backends.lwjgl import LwjglApplication, LwjglApplicationConfiguration, LwjglFiles, LwjglPreferences
from com.badlogic.gdx.math import Matrix4, Vector3
from com.badlogic.gdx.math.collision import BoundingBox
from com.badlogic.gdx.utils import Array, StringBuilder
from baseg3dhudtest import BaseG3dHudTest

class Animation3DTest(BaseG3dHudTest):
    def __init__(self):
        super(Animation3DTest, self).__init__()
        self.skydome = None
        self.floorModel = None
        self.character = None
        self.ship = None
        self.tree = None
        self.animation = None
        self.shadowLight = None
        self.shadowBatch = None

        self.lights = None

        self.trTmp = AnimationController.Transform()
        self.trForward = AnimationController.Transform()
        self.trBackward = AnimationController.Transform()
        self.trRight = AnimationController.Transform()
        self.trLeft = AnimationController.Transform()
        self.tmpMatrix = Matrix4()
        self.tmpVector = Vector3()
        self.status = 0
        self.idle = 1
        self.walk = 2
        self.back = 3
        self.attack = 4
        self.angle = 0.0

    def create(self):
        super(Animation3DTest, self).create()
        self.lights = Environment()
        self.lights.set(ColorAttribute(ColorAttribute.AmbientLight, 0.4, 0.4, 0.4, 1.0))
        self.shadowLight = DirectionalShadowLight(1024, 1024, 30.0, 30.0, 1.0, 100.0)
        self.lights.add(self.shadowLight)
        self.shadowLight.set(0.8, 0.8, 0.8, -.4, -.4, -.4)
        self.lights.shadowMap = self.shadowLight
        self.inputController.rotateLeftKey = self.inputController.rotateRightKey = self.inputController.forwardKey = self.inputController.backwardKey = 0
        self.cam.position.set(25, 25, 25)
        self.cam.lookAt(0, 0, 0)
        self.cam.update()
        self.modelsWindow.setVisible(False)
        self.assets.load('../../data/g3d/skydome.g3db', Model)
        self.assets.load('../../data/g3d/concrete.png', Texture)
        self.assets.load('../../data/tree.png', Texture)
        self.assets.load('../../data/g3d/ship.obj', Model)
        self.loading = True
        self.trForward.translation.set(0, 0, 8.0)
        self.trBackward.translation.set(0, 0, -8.0)
        self.trLeft.rotation.setFromAxis(Vector3.Y, 90)
        self.trRight.rotation.setFromAxis(Vector3.Y, -90)

        builder = ModelBuilder()
        builder.begin()
        builder.node().id = 'floor'
        part = builder.part('floor', GL20.GL_TRIANGLES, Usage.Position | Usage.TextureCoordinates | Usage.Normal, Material('concrete'))
        part.ensureRectangles(1600)
        for x in frange(-200.0, 200.0, 10.0):
            for z in frange(-200.0, 200.0, 10.0):
                part.rect(x, 0, z + 10.0, x + 10.0, 0, z + 10.0, x + 10.0, 0, z, x, 0, z, 0, 1, 0)
        builder.node().id = 'tree'
        part = builder.part('tree', GL20.GL_TRIANGLES, Usage.Position | Usage.TextureCoordinates | Usage.Normal, Material('tree'))
        part.rect(0.0, 0.0, -10.0, 10.0, 0.0, -10.0, 10.0, 10.0, -10.0, 0.0, 10.0, -10.0, 0, 0, 1.0)
        part.setUVRange(1, 0, 0, 1)
        part.rect(10.0, 0.0, -10.0, 0.0, 0.0, -10.0, 0.0, 10.0, -10.0, 10.0, 10.0, -10.0, 0, 0, -1.0)
        self.floorModel = builder.end()

        self.shadowBatch = ModelBatch(DepthShaderProvider())

    def render(self):
        if self.character:
            self.animation.update(Gdx.graphics.getDeltaTime())
            if Gdx.input.isKeyPressed(Keys.UP):
                if not self.animation.inAction:
                    self.trTmp.idt().lerp(self.trForward, Gdx.graphics.getDeltaTime() / self.animation.current.animation.duration)
                    self.character.transform.mul(self.trTmp.toMatrix4(self.tmpMatrix))
                if self.status != self.walk:
                    self.animation.animate('Walk', -1, -1.0, None, 0.2)
                    self.status = self.walk
            elif Gdx.input.isKeyPressed(Keys.DOWN):
                if not self.animation.inAction:
                    self.trTmp.idt().lerp(self.trBackward, Gdx.graphics.getDeltaTime() / self.animation.current.animation.duration)
                    self.character.transform.mul(self.trTmp.toMatrix4(self.tmpMatrix))
                if self.status != self.back:
                    self.animation.animate('Walk', -1, -1.0, None, 0.2)
                    self.status = self.back
            elif self.status != self.idle:
                self.animation.animate('Idle', -1, -1.0, None, 0.2)
                self.status = self.idle
            if Gdx.input.isKeyPressed(Keys.RIGHT) and (self.status == self.walk or self.status == self.back) and not self.animation.inAction:
                self.trTmp.idt().lerp(self.trRight, Gdx.graphics.getDeltaTime() / self.animation.current.animation.duration)
                self.character.transform.mul(self.trTmp.toMatrix4(self.tmpMatrix))
            elif Gdx.input.isKeyPressed(Keys.LEFT) and (self.status == self.walk or self.status == self.back) and not self.animation.inAction:
                self.trTmp.idt().lerp(self.trLeft, Gdx.graphics.getDeltaTime() / self.animation.current.animation.duration)
                self.character.transform.mul(self.trTmp.toMatrix4(self.tmpMatrix))
            if Gdx.input.isKeyPressed(Keys.SPACE) and not self.animation.inAction:
                self.animation.action('Attack', 1, 1.0, None, 0.2)
            if Gdx.input.isKeyJustPressed(Keys.Z):
                self.ship.parts.get(0).enabled = not self.ship.parts.get(0).enabled

        if self.character:
            self.shadowLight.begin(self.character.transform.getTranslation(self.tmpVector), self.cam.direction)
            self.shadowBatch.begin(self.shadowLight.getCamera())
            if self.character: self.shadowBatch.render(self.character)
            if self.tree: self.shadowBatch.render(self.tree)
            self.shadowBatch.end()
            self.shadowLight.end()

        super(Animation3DTest, self).render()

    def render_3(self, batch, instances):
        batch.render(instances, self.lights)
        if self.skydome: batch.render(self.skydome)

    def getStatus(self, stringBuilder):
        super(Animation3DTest, self).getStatus(stringBuilder)
        stringBuilder.append(' use arrow keys to walk around, space to attack, Z to toggle attached node.')

    def onModelClicked(name):
        pass

    def onLoaded(self):
        if not self.skydome:
            self.skydome = ModelInstance(self.assets.get('../../data/g3d/skydome.g3db', Model))
            self.floorModel.getMaterial('concrete').set(TextureAttribute.createDiffuse(self.assets.get('../../data/g3d/concrete.png', Texture)))
            self.floorModel.getMaterial('tree').set(
                TextureAttribute.createDiffuse(self.assets.get('../../data/tree.png', Texture)),
                BlendingAttribute()
            )
            self.instances.append(ModelInstance(self.floorModel, ['floor']))
            self.tree = ModelInstance(self.floorModel, ['tree'])
            self.instances.append(self.tree)
            self.assets.load('../../data/g3d/knight.g3db', Model)
            self.loading = True
        elif not self.character:
            self.character = ModelInstance(self.assets.get('../../data/g3d/knight.g3db', Model))
            bbox = BoundingBox()
            self.character.calculateBoundingBox(bbox)
            self.character.transform.setToRotation(Vector3.Y, 180).trn(0, -bbox.min.y, 0)
            self.instances.append(self.character)
            self.animation = AnimationController(self.character)
            self.animation.animate('Idle', -1, 1.0, None, 0.2)
            self.status = self.idle
            for anim in self.character.animations:
                Gdx.app.log('Test', anim.id)
            self.ship = self.assets.get('../../data/g3d/ship.obj', Model).nodes.get(0).copy()
            self.ship.detach()
            self.ship.translation.x = 10.0
            self.ship.rotation.set(Vector3.Z, 90.0)
            self.ship.scale.scl(5.0)
            self.ship.parts.get(0).enabled = False
            self.character.getNode('sword').addChild(self.ship)

    def dispose(self):
        super(Animation3DTest, self).dispose()
        self.floorModel.dispose()
        self.shadowLight.dispose()

if __name__ == '__main__':
    config = LwjglApplicationConfiguration()
    config.width = 1280
    config.height = 960
    config.title = 'Animation 3D Test'
    config.forceExit = False
    LwjglApplication(Animation3DTest(), config)
