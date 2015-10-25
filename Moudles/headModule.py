import pymel.core as pm
from subModules import fkChain,ikChain,boneChain
from Utils import nameUtils
from Modules import control,hierarchy,legModule

class HeadModule(object):

    #single array
    neckPosArray = [[0,14.25,-0.1],[0,14.77,0],[0,15,0.07],[0,15.355,0.236]]
    neckRotArray = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    jawPosArray = [[0,15.5,0.45],[0,15,1.25]]
    jawRotArray = [[0,0,0],[0,0,0]]    
    muzzlePosArray = [0,16.174,1.091]
    muzzleRotArray = [0,0,0]
    nosePosArray = [[0,16.16,1.16],[0,15.794,1.529]]
    noseRotArray = [[0,0,0],[0,0,0]]
    upTeethPosArray = [0,15.56,1.215]
    upTeethRotArray = [0,0,0]
    loTeethPosArray = [0,15.28,1.157]
    loTeethRotArray = [0,0,0]
    tonguePosArray = [[0,15.356,0.462],[0,15.409,0.837],[0,15.391,1.18]]
    tongueRotArray = [[0,0,0],[0,0,0],[0,0,0]]
    
    #mirror array
    eyePosArray = [[0.368,16.184,0.882],[0.368,16.184,1.132]]
    eyeRotArray = [[0,0,0],[0,0,0]]
    earPosArray = [[0.947,15.739,0.154],[1.187,16.263,-0.08]]
    earRotArray = [[0,0,0],[0,0,0]]
    nostrilPosArray = [0.166,15.749,1.354]
    nostrilRotArray = [0,0,0]
    
    def __init__(self, baseName = 'head',size = 1.5,
                 controlOrient = [0,0,0]):
        
        self.baseName = baseName
        self.side = ['l','m','r']
        self.size = size
        
        #jj
        self.neckFkChain = None
        self.sklGrp = None
        
        #guides 
        #single guides
        self.neckGuides = None
        self.jawGuides = None
        self.muzzleGuides = None
        self.noseGuides = None
        self.upTeethGuides = None
        self.loTeethGuides = None
        self.tongueGuides = None
        
        #mirror guides
        self.eyeRightGuides = None
        self.eyeRightGuides = None
        self.earLeftGuides = None
        self.earRightGuides = None
        self.nostrilLeftGuides = None
        self.nostrilRightGuides = None
        self.guideGrp = None
        
        #cc 
        self.tongueDis = None
        self.neckDis = None
        self.eyeRad = None
        self.headCtrl = None
        self.jawCtrl = None
        self.eyeLeftCtrl = None
        self.eyeRightCtrl = None
        self.eyeAimCtrl = None
        self.muzzleCtrl = None        
        self.noseCtrl = None    
        self.nostrilLeftCtrl = None              
        self.nostrilRightCtrl = None
        self.upTeethCtrl = None
        self.loTeethCtrl = None        
        self.earLeftCtrl = None       
        self.earRightCtrl = None
        
        #namelist
        self.nameList = ['neck','head','jaw','eye','muzzle','nose','nostril','upTeeth',
                         'loTeeth','tongue','ear']
        self.micoCtrlList = ['','']
        
    def buildGuides(self):
        
        self.neckGuides = []
        self.jawGuides = []
        self.muzzleGuides = []
        self.noseGuides = []
        self.nostrilLeftGuides = []
        self.nostrilRightGuides = []
        self.upTeethGuides = []
        self.loTeethGuides = []
        self.tongueGuides = []
        
        self.eyeLeftGuides = []
        self.eyeRightGuides = []
        self.earLeftGuides = []
        self.earRightGuides = []
        
        #build neck guides
        #set loc pos
        for num,pos in enumerate(self.neckPosArray):
            if num != len(self.neckPosArray) - 1:
                locName = nameUtils.getUniqueName(self.side[1],self.nameList[0],'gud')
            else :
                locName = nameUtils.getUniqueName(self.side[1],self.nameList[1],'gud')
            loc = pm.spaceLocator(n = locName)
            loc.t.set(pos)
            self.neckGuides.append(loc)        
         
        tempNeckGuides = list(self.neckGuides)
        tempNeckGuides.reverse()
         
        for i in range(len(tempNeckGuides)):
            if i != (len(tempNeckGuides) - 1):
                pm.parent(tempNeckGuides[i],tempNeckGuides[i + 1])
        
        #build jaw guides
        #set loc pos
        for num,pos in enumerate(self.jawPosArray):
            locName = nameUtils.getUniqueName(self.side[1],self.nameList[2],'gud')
            loc = pm.spaceLocator(n = locName)
            loc.t.set(pos)
            self.jawGuides.append(loc)        
         
        tempJawGuides = list(self.jawGuides)
        tempJawGuides.reverse()
         
        for i in range(len(tempJawGuides)):
            if i != (len(tempJawGuides) - 1):
                pm.parent(tempJawGuides[i],tempJawGuides[i + 1])
                
        #build eye guides
        #set loc pos
        #left
        for num,pos in enumerate(self.eyePosArray):
            locName = nameUtils.getUniqueName(self.side[0],self.nameList[3],'gud')
            loc = pm.spaceLocator(n = locName)
            loc.t.set(pos)
            self.eyeLeftGuides.append(loc)        
         
        tempEyeLeftGuides = list(self.eyeLeftGuides)
        tempEyeLeftGuides.reverse()
         
        for i in range(len(tempEyeLeftGuides)):
            if i != (len(tempEyeLeftGuides) - 1):
                pm.parent(tempEyeLeftGuides[i],tempEyeLeftGuides[i + 1])
        
        #build muzzle structure
        #build muzzle guide
        muzzleLocName = nameUtils.getUniqueName(self.side[1],self.nameList[4],'gud')
        muzzleLoc = pm.spaceLocator(n = muzzleLocName)
        muzzleLoc.t.set(self.muzzlePosArray)
        self.muzzleGuides.append(muzzleLoc)
        
        #build nose guide
        #nose mid
        for num,pos in enumerate(self.nosePosArray):
            locName = nameUtils.getUniqueName(self.side[1],self.nameList[5],'gud')
            loc = pm.spaceLocator(n = locName)
            loc.t.set(pos)
            self.noseGuides.append(loc)        
         
        tempNoseGuides = list(self.noseGuides)
        tempNoseGuides.reverse()
         
        for i in range(len(tempNoseGuides)):
            if i != (len(tempNoseGuides) - 1):
                pm.parent(tempNoseGuides[i],tempNoseGuides[i + 1])     
        
        #nostril
        #left loc
        nostrilLeftLocName = nameUtils.getUniqueName(self.side[0],self.nameList[6],'gud')
        nostrilLeftLoc = pm.spaceLocator(n = nostrilLeftLocName)
        nostrilLeftLoc.t.set(self.nostrilPosArray)
        self.nostrilLeftGuides.append(nostrilLeftLoc)
        self.nostrilLeftGuides[0].setParent(self.noseGuides[0])
         
        self.noseGuides[0].setParent(self.muzzleGuides[0])        
        
        #build upTeeth guide
        upTeethLocName = nameUtils.getUniqueName(self.side[1],self.nameList[7],'gud')
        upTeethLoc = pm.spaceLocator(n = upTeethLocName)
        upTeethLoc.t.set(self.upTeethPosArray)
        self.upTeethGuides.append(upTeethLoc)
        self.upTeethGuides[0].setParent(self.muzzleGuides[0])
        
        #build loTeeth guide
        loTeethLocName = nameUtils.getUniqueName(self.side[1],self.nameList[8],'gud')
        loTeethLoc = pm.spaceLocator(n = loTeethLocName)
        loTeethLoc.t.set(self.loTeethPosArray)
        self.loTeethGuides.append(loTeethLoc)
        self.loTeethGuides[0].setParent(self.jawGuides[0])        
        
        #build tongue guides
        #set loc pos
        for num,pos in enumerate(self.tonguePosArray):
            locName = nameUtils.getUniqueName(self.side[1],self.nameList[9],'gud')
            loc = pm.spaceLocator(n = locName)
            loc.t.set(pos)
            self.tongueGuides.append(loc)        
         
        tempTongueGuides = list(self.tongueGuides)
        tempTongueGuides.reverse()
         
        for i in range(len(tempTongueGuides)):
            if i != (len(tempTongueGuides) - 1):
                pm.parent(tempTongueGuides[i],tempTongueGuides[i + 1])
                
        self.tongueGuides[0].setParent(self.jawGuides[0])
        
        #build ear guides
        #set loc pos
        for num,pos in enumerate(self.earPosArray):
            locName = nameUtils.getUniqueName(self.side[0],self.nameList[10],'gud')
            loc = pm.spaceLocator(n = locName)
            loc.t.set(pos)
            self.earLeftGuides.append(loc)        
         
        tempearLeftGuides = list(self.earLeftGuides)
        tempearLeftGuides.reverse()
         
        for i in range(len(tempearLeftGuides)):
            if i != (len(tempearLeftGuides) - 1):
                pm.parent(tempearLeftGuides[i],tempearLeftGuides[i + 1])
                
        self.earLeftGuides[0].setParent(self.neckGuides[-1])        
        
        #clean up
        self.guideGrp = pm.group(self.neckGuides[0],self.jawGuides[0],self.eyeLeftGuides[0],self.muzzleGuides[0],
                                 n = nameUtils.getUniqueName(self.side[1],self.baseName + 'Gud','grp'))
         
    def build(self):
        
        self.guideGrp.v.set(0)
        '''
        this part perpare for the neck tongue fk cc size 
        '''
        #create distance node:
        neckDistanceBetweenNodeName = nameUtils.getUniqueName(self.side[1],self.baseName + 'neck','dist')
        tongueDistanceBetweenNodeName = nameUtils.getUniqueName(self.side[1],self.baseName + 'tongue','dist')
        
        #create Node
        neckDistBetweenNode = pm.createNode('distanceBetween',n = neckDistanceBetweenNodeName)
        tongueDistBetweenNode = pm.createNode('distanceBetween',n = tongueDistanceBetweenNodeName)
        
        #dis get
        #neck
        self.neckGuides[0].worldPosition[0].connect(neckDistBetweenNode.point1) 
        self.neckGuides[1].worldPosition[0].connect(neckDistBetweenNode.point2) 
        self.neckDis = neckDistBetweenNode.distance.get()
        
        #tongue
        self.tongueGuides[0].worldPosition[0].connect(tongueDistBetweenNode.point1) 
        self.tongueGuides[1].worldPosition[0].connect(tongueDistBetweenNode.point2) 
        self.tongueDis = tongueDistBetweenNode.distance.get()
        
        '''
        this part create the basic joint 
        '''
        #get pos info
        #neck pos
        self.neckGuidePos = [x.getTranslation(space = 'world') for x in self.neckGuides]
        self.neckGuideRot = [x.getRotation(space = 'world') for x in self.neckGuides]
        
        #neck jj set
        self.neckFkChain = fkChain.FkChain(self.nameList[0],self.side[1],size = self.neckDis,
                                           fkCcType = 'cc',type = 'jj',pointCnst = 1)
        self.neckFkChain.fromList(self.neckGuidePos,self.neckGuideRot,skipLast = 1)
 
        for num,joint in enumerate(self.neckFkChain.chain):
            if num == (self.neckFkChain.chainLength() - 1):
                jjName = nameUtils.getUniqueName(self.side[1],self.nameList[1],'jj')
                ccName = nameUtils.getUniqueName(self.side[1],self.nameList[1],'cc')
                ccGrpName = nameUtils.getUniqueName(self.side[1],self.nameList[1],'grp')
                pm.rename(self.neckFkChain.chain[-1],jjName)
                
        self.headCtrl = control.Control(self.side[1],self.nameList[1],size = self.neckDis * 1.75) 
        self.headCtrl.circleCtrl()
        pm.xform(self.headCtrl.controlGrp,ws = 1,matrix = self.neckFkChain.chain[-1].worldMatrix.get())
        self.headCtrl.controlGrp.setParent(self.neckFkChain.controlsArray[-1].control)
        pm.orientConstraint(self.headCtrl.control,self.neckFkChain.chain[-1],mo = 0)
        
        #jaw pos get
        self.jawGuidePos = [x.getTranslation(space = 'world') for x in self.jawGuides]
        self.jawGuideRot = [x.getRotation(space = 'world') for x in self.jawGuides]

        #jaw jj set and clean
        self.jawChains = boneChain.BoneChain(self.nameList[2],self.side[1],type = 'jj')
        self.jawChains.fromList(self.jawGuidePos,self.jawGuideRot)
        self.jawChains.chain[0].setParent(self.neckFkChain.chain[-1])

        #eye pos get
        self.eyeLeftGuidePos = [x.getTranslation(space = 'world') for x in self.eyeLeftGuides]
        self.eyeLeftGuideRot = [x.getRotation(space = 'world') for x in self.eyeLeftGuides]

        #eye jj set and clean
        self.eyeLeftChain = boneChain.BoneChain(self.nameList[3],self.side[0],type = 'jj')
        self.eyeLeftChain.fromList(self.eyeLeftGuidePos,self.eyeLeftGuideRot)
        self.eyeLeftChain.chain[0].setParent(self.neckFkChain.chain[-1])
        
        #eye right side:
        #get pos info
        self.eyeRightPosArray = self.eyePosArray
        for num,pos in enumerate(self.eyeRightPosArray):
            rightValue = -(self.eyeRightPosArray[num][0])
            self.eyeRightPosArray[num][0] = rightValue
            
        #set right guide
        for num,pos in enumerate(self.eyeRightPosArray):
            locName = nameUtils.getUniqueName(self.side[-1],self.nameList[3],'gud')
            loc = pm.spaceLocator(n = locName)
            loc.t.set(pos)
            self.eyeRightGuides.append(loc)        
          
        tempEyeRightGuides = list(self.eyeRightGuides)
        tempEyeRightGuides.reverse()
        
        for i in range(len(tempEyeRightGuides)):
            if i != (len(tempEyeRightGuides) - 1):
                pm.parent(tempEyeRightGuides[i],tempEyeRightGuides[i + 1])
        
        self.eyeRightGuides[0].setParent(self.guideGrp)
        
        #right pos get
        #eye pos get
        self.eyeRightGuidePos = [x.getTranslation(space = 'world') for x in self.eyeRightGuides]
        self.eyeRightGuideRot = [x.getRotation(space = 'world') for x in self.eyeRightGuides]        
        
        #set right eye jj
        self.eyeRightChain = boneChain.BoneChain(self.nameList[3],self.side[-1],type = 'jj')
        self.eyeRightChain.fromList(self.eyeRightGuidePos,self.eyeRightGuideRot)
        self.eyeRightChain.chain[0].setParent(self.neckFkChain.chain[-1])        
        
        #muzzle pos get
        self.muzzleGuidePos = [x.getTranslation(space = 'world') for x in self.muzzleGuides]
        self.muzzleGuideRot = [x.getRotation(space = 'world') for x in self.muzzleGuides]
        
        #muzzle jj set and clean
        pm.select(cl = 1)
        self.muzzleChain = pm.joint(p = self.muzzleGuidePos[0],n = nameUtils.getUniqueName(self.side[1],self.nameList[4],'jj'))
        self.muzzleChain.setParent(self.neckFkChain.chain[-1])
        
        #nose pos get
        self.nostrilLeftGuidePos = [x.getTranslation(space = 'world') for x in self.nostrilLeftGuides]
        self.nostrilLeftGuideRot = [x.getRotation(space = 'world') for x in self.nostrilLeftGuides]        
        
        self.noseGuidePos = [x.getTranslation(space = 'world') for x in self.noseGuides]
        self.noseGuideRot = [x.getRotation(space = 'world') for x in self.noseGuides]
        
        #nose jj set and clean
        self.noseChain = boneChain.BoneChain(self.nameList[5],self.side[1],type = 'jj')
        self.noseChain.fromList(self.noseGuidePos,self.noseGuideRot)
        self.noseChain.chain[0].setParent(self.muzzleChain)
        
        #nostril jj
        #left nostril jj
        pm.select(cl = 1)
        self.nostrilLeftChain = pm.joint(p = self.nostrilLeftGuidePos[0],
                                     n = nameUtils.getUniqueName(self.side[0],self.nameList[6],'jj'))
        self.nostrilLeftChain.setParent(self.noseChain.chain[0])
        
        #right nosetril loc
        self.nostrilRightPosArray = self.nostrilPosArray
        for pos in self.nostrilRightPosArray:
            rightValue = -self.nostrilRightPosArray[0]
            self.nostrilRightPosArray[0] = rightValue
            
        nostrilRightLocName = nameUtils.getUniqueName(self.side[-1],self.nameList[6],'gud')
        nostrilRightLoc = pm.spaceLocator(n = nostrilRightLocName)
        nostrilRightLoc.t.set(self.nostrilRightPosArray)
        self.nostrilRightGuides.append(nostrilRightLoc)
        self.nostrilRightGuides[0].setParent(self.noseGuides[0])
        
        #right nostril pos get
        self.nostrilRightGuidePos = [x.getTranslation(space = 'world') for x in self.nostrilRightGuides]
        self.nostrilRightGuideRot = [x.getRotation(space = 'world') for x in self.nostrilRightGuides]
        
        #right nostril jj
        pm.select(cl = 1)
        self.nostrilRightChain = pm.joint(p = self.nostrilRightGuidePos[0],
                                     n = nameUtils.getUniqueName(self.side[-1],self.nameList[6],'jj'))
        self.nostrilRightChain.setParent(self.noseChain.chain[0])   
        
        #left ear pos get
        self.earLeftGuidePos = [x.getTranslation(space = 'world') for x in self.earLeftGuides]
        self.earLeftGuideRot = [x.getRotation(space = 'world') for x in self.earLeftGuides]

        #left ear jj set and clean
        self.earLeftChain = boneChain.BoneChain(self.nameList[10],self.side[0],type = 'jj')
        self.earLeftChain.fromList(self.earLeftGuidePos,self.earLeftGuideRot)
        self.earLeftChain.chain[0].setParent(self.neckFkChain.chain[-1])
        
        #ear right side:
        #get pos info
        self.earRightPosArray = self.earPosArray
        for num,pos in enumerate(self.earRightPosArray):
            rightValue = -(self.earRightPosArray[num][0])
            self.earRightPosArray[num][0] = rightValue
            
        #set right guide
        for num,pos in enumerate(self.earRightPosArray):
            locName = nameUtils.getUniqueName(self.side[-1],self.nameList[10],'gud')
            loc = pm.spaceLocator(n = locName)
            loc.t.set(pos)
            self.earRightGuides.append(loc)        
          
        tempEarRightGuides = list(self.earRightGuides)
        tempEarRightGuides.reverse()
        
        for i in range(len(tempEarRightGuides)):
            if i != (len(tempEarRightGuides) - 1):
                pm.parent(tempEarRightGuides[i],tempEarRightGuides[i + 1])
        
        self.earRightGuides[0].setParent(self.guideGrp)
        
        #right pos get
        #ear pos get
        self.earRightGuidePos = [x.getTranslation(space = 'world') for x in self.earRightGuides]
        self.earRightGuideRot = [x.getRotation(space = 'world') for x in self.earRightGuides]        
        
        #set right ear jj
        self.earRightChain = boneChain.BoneChain(self.nameList[10],self.side[-1],type = 'jj')
        self.earRightChain.fromList(self.earRightGuidePos,self.earRightGuideRot)
        self.earRightChain.chain[0].setParent(self.neckFkChain.chain[-1])    
        
        #upTeeth pos get
        self.upTeethGuidePos = [x.getTranslation(space = 'world') for x in self.upTeethGuides]
        self.upTeethGuideRot = [x.getRotation(space = 'world') for x in self.upTeethGuides]           
        
        #set upTeeth jj
        pm.select(cl = 1)
        self.upTeethChain = pm.joint(p = self.upTeethGuidePos[0],
                                     n = nameUtils.getUniqueName(self.side[1],self.nameList[7],'jj')) 
        self.upTeethChain.setParent(self.muzzleChain)      
        
        #loTeeth pos get
        self.loTeethGuidePos = [x.getTranslation(space = 'world') for x in self.loTeethGuides]
        self.loTeethGuideRot = [x.getRotation(space = 'world') for x in self.loTeethGuides]             
        
        #set loTeeth jj
        pm.select(cl = 1)
        self.loTeethChain = pm.joint(p = self.loTeethGuidePos[0],
                                     n = nameUtils.getUniqueName(self.side[1],self.nameList[8],'jj')) 
        self.loTeethChain.setParent(self.jawChains.chain[0])             
        
        #set tongue         
        #get pos info
        self.tongueGuidePos = [x.getTranslation(space = 'world') for x in self.tongueGuides]
        self.tongueGuideRot = [x.getRotation(space = 'world') for x in self.tongueGuides]

        #tongue jj set
        pm.select(cl = 1)
#         self.tongueChain = boneChain.BoneChain(self.nameList[9],self.side[1],type = 'jj')
#         self.tongueChain.fromList(self.tongueGuidePos,self.tongueGuideRot)
#         self.tongueChain.chain[0].setParent(self.jawChains.chain[0])        
        self.tongueFkChain = fkChain.FkChain(self.nameList[9],self.side[1],size = self.tongueDis * 0.75,
                                             fkCcType = 'cc',type = 'jj',pointCnst = 1)
        self.tongueFkChain.fromList(self.tongueGuidePos,self.tongueGuideRot,skipLast = 1)
        self.tongueFkChain.chain[0].setParent(self.jawChains.chain[0])
#         self.tongueFkChain.controlsArray[0].control.setParent(self.jawCtrl.control)

        #correct jj orient
        pm.select(self.muzzleChain)
        pm.joint(e = 1,oj = 'xyz',secondaryAxisOrient = 'zdown',ch = 1)
        
        self.upTeethChain.jointOrientX.set(0)
        self.upTeethChain.jointOrientY.set(0)
        self.upTeethChain.jointOrientZ.set(0)
        
        self.loTeethChain.jointOrientX.set(0)
        self.loTeethChain.jointOrientY.set(0)
        self.loTeethChain.jointOrientZ.set(0)
        
        self.nostrilLeftChain.jointOrientX.set(0)
        self.nostrilLeftChain.jointOrientY.set(0)
        self.nostrilLeftChain.jointOrientZ.set(0)
        
        self.nostrilRightChain.jointOrientX.set(0)
        self.nostrilRightChain.jointOrientY.set(0)
        self.nostrilRightChain.jointOrientZ.set(0)

        self.__addCtrl()
#         self.__connectAttr()
#         self.__cleanUp()

    def __addCtrl(self):
#         self.nameList = ['neck','head','jaw','eye','muzzle','nose','nostril','upTeeth',
#                          'loTeeth','tongue','ear']
        #create jawCtrl
        self.jawCtrl = control.Control(self.side[1],self.nameList[2],size = self.neckDis * 2) 
        self.jawCtrl.cubeCtrl()
        control.lockAndHideAttr(self.jawCtrl.control,['sx','sy','sz','v'])
        
        #align
        pm.xform(self.jawCtrl.controlGrp,ws = 1,matrix = self.jawChains.chain[0].worldMatrix.get())
        pm.orientConstraint(self.jawCtrl.control,self.jawChains.chain[0],mo = 0)
        pm.pointConstraint(self.jawCtrl.control,self.jawChains.chain[0],mo = 0)
        self.tongueFkChain.controlsArray[0].controlGrp.setParent(self.jawCtrl.control)
        self.jawCtrl.controlGrp.setParent(self.headCtrl.control)
        
        #create eyeCtrl
        self.eyeRad = float(self.eyePosArray[1][-1] - self.eyePosArray[0][-1])
        self.eyeLeftCtrl = control.Control(self.side[0],self.nameList[3],size = self.eyeRad * 0.65) 
        self.eyeLeftCtrl.sphereCtrl()
        control.lockAndHideAttr(self.eyeLeftCtrl.control,['sx','sy','sz','v'])
        pm.xform(self.eyeLeftCtrl.controlGrp,ws = 1,matrix = self.eyeLeftChain.chain[0].worldMatrix.get())
        pm.orientConstraint(self.eyeLeftCtrl.control,self.eyeLeftChain.chain[0],mo = 0)
        pm.pointConstraint(self.eyeLeftCtrl.control,self.eyeLeftChain.chain[0],mo = 0)
        self.eyeLeftCtrl.controlGrp.setParent(self.headCtrl.control)
        
        self.eyeRightCtrl = control.Control(self.side[2],self.nameList[3],size = self.eyeRad * 0.65) 
        self.eyeRightCtrl.sphereCtrl()
        control.lockAndHideAttr(self.eyeRightCtrl.control,['sx','sy','sz','v'])     
        pm.xform(self.eyeRightCtrl.controlGrp,ws = 1,matrix = self.eyeRightChain.chain[0].worldMatrix.get())
        pm.orientConstraint(self.eyeRightCtrl.control,self.eyeRightChain.chain[0],mo = 0)
        pm.pointConstraint(self.eyeRightCtrl.control,self.eyeRightChain.chain[0],mo = 0)
        self.eyeRightCtrl.controlGrp.setParent(self.headCtrl.control)        
        
        #create eye aim create
        self.eyeAimCtrl = control.Control(self.side[1],self.nameList[3] + 'Aim',size = self.eyeRad * 5) 
        self.eyeAimCtrl.plusCtrl()
        
        #create muzzle cc
        self.muzzleCtrl = control.Control(self.side[1],self.nameList[4],size = self.tongueDis,aimAxis = 'y') 
        self.muzzleCtrl.circleCtrl()
        pm.xform(self.muzzleCtrl.controlGrp,ws = 1,matrix = self.muzzleChain.worldMatrix.get())
        pm.orientConstraint(self.muzzleCtrl.control,self.muzzleChain,mo = 0)
        pm.pointConstraint(self.muzzleCtrl.control,self.muzzleChain,mo = 0) 
        self.muzzleCtrl.controlGrp.setParent(self.headCtrl.control)       
                
        self.noseCtrl = control.Control(self.side[1],self.nameList[5],size = self.tongueDis,aimAxis = 'y') 
        self.noseCtrl.circleCtrl()
        pm.xform(self.noseCtrl.controlGrp,ws = 1,matrix = self.noseChain.chain[0].worldMatrix.get())
        pm.orientConstraint(self.noseCtrl.control,self.noseChain.chain[0],mo = 0)
        pm.pointConstraint(self.noseCtrl.control,self.noseChain.chain[0],mo = 0) 
        self.noseCtrl.controlGrp.setParent(self.muzzleCtrl.control)               
        
        #create nostril cc    
        self.nostrilLeftCtrl = control.Control(self.side[0],self.nameList[6],size = self.tongueDis / 2) 
        self.nostrilLeftCtrl.cubeCtrl()
        control.lockAndHideAttr(self.nostrilLeftCtrl.control,['sx','sy','sz','v'])
        pm.xform(self.nostrilLeftCtrl.controlGrp,ws = 1,matrix = self.nostrilLeftChain.worldMatrix.get())
        pm.orientConstraint(self.nostrilLeftCtrl.control,self.nostrilLeftChain,mo = 0)
        pm.pointConstraint(self.nostrilLeftCtrl.control,self.nostrilLeftChain,mo = 0) 
        self.nostrilLeftCtrl.controlGrp.setParent(self.noseCtrl.control)       
                      
        self.nostrilRightCtrl = control.Control(self.side[2],self.nameList[6],size = self.tongueDis / 2) 
        self.nostrilRightCtrl.cubeCtrl()
        control.lockAndHideAttr(self.nostrilRightCtrl.control,['sx','sy','sz','v'])
        pm.xform(self.nostrilRightCtrl.controlGrp,ws = 1,matrix = self.nostrilRightChain.worldMatrix.get())
        pm.orientConstraint(self.nostrilRightCtrl.control,self.nostrilRightChain,mo = 0)
        pm.pointConstraint(self.nostrilRightCtrl.control,self.nostrilRightChain,mo = 0)
        self.nostrilRightCtrl.controlGrp.setParent(self.noseCtrl.control)    
        
        #create upTeethCtrl
        self.upTeethCtrl = control.Control(self.side[1],self.nameList[7],size = float(self.tongueDis * 1.5),aimAxis = 'y') 
        self.upTeethCtrl.circleCtrl()
        control.lockAndHideAttr(self.upTeethCtrl.control,['sx','sy','sz','v'])
        pm.xform(self.upTeethCtrl.controlGrp,ws = 1,matrix = self.upTeethChain.worldMatrix.get())
        pm.orientConstraint(self.upTeethCtrl.control,self.upTeethChain,mo = 0)
        pm.pointConstraint(self.upTeethCtrl.control,self.upTeethChain,mo = 0)
        self.upTeethCtrl.controlGrp.setParent(self.noseCtrl.control)            
        
        #create loTeethCtrl
        self.loTeethCtrl = control.Control(self.side[1],self.nameList[8],size = float(self.tongueDis * 1.5),aimAxis = 'y') 
        self.loTeethCtrl.circleCtrl()
        control.lockAndHideAttr(self.loTeethCtrl.control,['sx','sy','sz','v'])
        pm.xform(self.loTeethCtrl.controlGrp,ws = 1,matrix = self.loTeethChain.worldMatrix.get())
        pm.orientConstraint(self.loTeethCtrl.control,self.loTeethChain,mo = 0)
        pm.pointConstraint(self.loTeethCtrl.control,self.loTeethChain,mo = 0)
        self.loTeethCtrl.controlGrp.setParent(self.jawCtrl.control)               
                
        #create earCrl
        self.earLeftCtrl = control.Control(self.side[0],self.nameList[10],size = float(self.tongueDis * 1.5)) 
        self.earLeftCtrl.circleCtrl()
        control.lockAndHideAttr(self.earLeftCtrl.control,['sx','sy','sz','v'])
        pm.xform(self.earLeftCtrl.controlGrp,ws = 1,matrix = self.earLeftChain.chain[0].worldMatrix.get())
        pm.orientConstraint(self.earLeftCtrl.control,self.earLeftChain.chain[0],mo = 0)
        pm.pointConstraint(self.earLeftCtrl.control,self.earLeftChain.chain[0],mo = 0)
        self.earLeftCtrl.controlGrp.setParent(self.headCtrl.control)
               
        self.earRightCtrl = control.Control(self.side[2],self.nameList[10],size = float(self.tongueDis * 1.5)) 
        self.earRightCtrl.circleCtrl()
        control.lockAndHideAttr(self.earRightCtrl.control,['sx','sy','sz','v'])
        pm.xform(self.earRightCtrl.controlGrp,ws = 1,matrix = self.earRightChain.chain[0].worldMatrix.get())
        pm.orientConstraint(self.earRightCtrl.control,self.earRightChain.chain[0],mo = 0)
        pm.pointConstraint(self.earRightCtrl.control,self.earRightChain.chain[0],mo = 0) 
        self.earRightCtrl.controlGrp.setParent(self.headCtrl.control)
    
    def __connectAttr(self):
        
        pass
    
    def __cleanUp(self):
        
        pass

        
        
        
        
# from Modules import legModule,footModule
# hg = headModule.HeadModule()
# hg.buildGuides()
# hg.build()
