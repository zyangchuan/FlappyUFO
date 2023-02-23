from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from panda3d.core import AmbientLight
from panda3d.core import DirectionalLight
from panda3d.core import Vec4, Vec3
from panda3d.core import Point3
from panda3d.core import CollisionTraverser
from panda3d.core import CollisionBox, CollisionNode, CollisionHandlerEvent
import math
from random import randrange

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.disableMouse()
        properties = WindowProperties()
        properties.setSize(1920, 960)
        self.win.requestProperties(properties)
        render.setShaderAuto()

        # Before the game starts
        self.started = False
        self.pipeNumber = 0
        self.checkpoint = 0
        self.interval = 7
        self.velocityZ = 0
        self.locationX = 0
        self.gravity = 0
        self.jumpHeight = 0
        self.velocityX = 0

        # The functions added to the task manager are called every frame
        self.taskMgr.add(self.checkStarted, "checkStartedTask")
        self.taskMgr.add(self.addPipe, "addPipeTask")
        self.taskMgr.add(self.falling, "fallingTask")
        self.taskMgr.add(self.panningRight, "panningTask")



        # Loading models
        self.pipes = self.loader.loadModel("pipes")
        pipetex = loader.loadTexture("pipeTex.png")
        self.pipes.setTexture(pipetex)
        self.pipes.setScale(1, 1, 1)
        self.pipes.setPos(-8, 42, 0)

        self.ufo = self.loader.loadModel("ufo")
        ufotex = loader.loadTexture("ufoTex.png")
        self.ufo.setTexture(ufotex)
        self.ufo.reparentTo(self.render)
        self.ufo.setScale(0.65, 0.65, 0.65)
        self.ufo.setPos(-20, 42, 0)

        # Adding colliders to models
        base.cTrav = CollisionTraverser()
        collisionHandler = CollisionHandlerEvent()

        colliderUfoNode = CollisionNode('ufo')
        colliderUfo = self.ufo.attachNewNode(colliderUfoNode)
        colliderUfo.node().addSolid(CollisionBox(Point3(-1.5, -1, -1),Point3(1.5, 1, 0.8)))
        base.cTrav.addCollider(colliderUfo, collisionHandler)
        #colliderUfo.show()

        colliderPipesNode = CollisionNode('pipes')
        colliderPipes = self.pipes.attachNewNode(colliderPipesNode)
        colliderPipes.node().addSolid(CollisionBox(Point3(-1, -1, -23),Point3(1, 1, -3)))
        colliderPipes.node().addSolid(CollisionBox(Point3(-1, -1, 3),Point3(1, 1, 23)))
        #colliderPipes.show()

        # Collision Detection
        collisionHandler.addInPattern('%fn-into-%in')
        self.accept('ufo-into-pipes', self.endGame)

        # Camera position
        self.camera.setPos(-15, 5, 1)
        self.camera.setHpr(0, 0, 0)


        # Generating the first 5 pipes
        for i in range(5):
            placeholder = render.attachNewNode("pipe-placeholder")
            placeholder.setPos(i * self.interval, 0, randrange(-5, 5))
            self.pipes.instanceTo(placeholder)




    def endGame(self, entry):

        self.velocityX = 0
        self.velocityZ = 0
        self.jumpHeight = 0
        self.gravity = 0


    def startGame (self):
        # Edit the game properties here
        self.gravity = -35
        self.jumpHeight = 5
        self.velocityX = 4
        self.started = True
        self.jump()


    def jumpInput(self):
        self.accept("mouse1", self.jump)


    def startInput(self):
        self.accept("mouse1", self.startGame)


    def checkStarted(self, task):
        if self.started == True:
            self.jumpInput()

        else:
            self.startInput()

        return task.cont


    def jump(self):
        dt = globalClock.getDt()
        self.velocityZ = math.sqrt(self.jumpHeight * -self.gravity)
        self.ufo.setPos(self.ufo.getPos() + Vec3(0, 0, self.velocityZ * dt))


    def falling(self, task):
        dt = globalClock.getDt()
        self.velocityZ += self.gravity * dt
        self.ufo.setPos(self.ufo.getPos() + Vec3(0, 0, self.velocityZ * dt))


        return task.cont

    def panningRight(self, task):
        dt = globalClock.getDt()
        self.locationX = self.velocityX * dt
        self.ufo.setPos(self.ufo.getPos() + Vec3(self.locationX, 0, 0))
        self.camera.setPos(self.camera.getPos() + Vec3(self.locationX, 0, 0))


        return task.cont


    def addPipe(self, task):
        if self.ufo.getPos() >= self.checkpoint:
            self.pipeNumber += 1
            self.checkpoint += self.interval
            placeholder = render.attachNewNode("pipe-placeholder")
            placeholder.setPos(28 + self.pipeNumber * 7, 0, randrange(-5, 5))
            self.pipes.instanceTo(placeholder)

        return task.cont

app = MyApp()
app.run()
