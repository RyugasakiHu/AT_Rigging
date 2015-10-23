import pymel.core as pm
from subModules import fkChain,ikChain,boneChain
from Utils import nameUtils
from Modules import control,hierarchy,legModule

class HeadModule(object):

    #single array
    neckPosArray = [[0,14.25,-0.1],[0,14.77,0],[0,15,0.07],[0,15.355,0.236]]
    neckRotArray = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    jawPosArray = [[0,15,1.25],[0,15.5,0.45]]
    jawRotArray = [[0,0,0],[0,0,0]]    
    muzzlePosArray = [0,16.174,1.091]
    muzzleRotArray = [0,0,0]
    nosePosArray = [[0,16.16,1.16],[0,15.794,1.529]]
    noseRotArray = [[0,0,0],[0,0,0]]
    upTeethPosArray = [0,15.56,1.215]
    upTeethRotArray = [0,0,0]
    loTeethPosArray = [0,15.28,1.157]
    loTeethRotArray = [0,0,0]
    tonguePosArray = [[0,15.219,0.251],[0,15.395,0.512,],[0,15.409,0.837],[0,15.391,1.18]]
    tongueRotArray = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    
    #mirror array
    eyePosArray = [[0.368,16.184,0.882],[0.368,16.184,1.132]]
    eyeRotArray = [[0,0,0],[0,0,0]]
    earPosArray = [[0.947,15.739,0.154],[1.187,16.263,-0.08]]
    earRotArray = [[0,0,0],[0,0,0]]
    nostrilPosArray = [[0,16.16,1.16],[0,15.794,1.529]]
    nostrilRotArray = [[0,0,0],[0,0,0]]
    
    def __init__(self, baseName = 'head',size = 1.5,
                 controlOrient = [0,0,0]):
        
        self.baseName = baseName
        self.side = ['r','m','l']
        self.size = size
        
        #jj
        self.neckFkChain = None
        self.sklGrp = None
        
        #cc 
#         self.footCtrl = None
        
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
        self.eyeGuides = None
        self.earGuides = None
        self.nostrilGuides = None
        self.guideGrp = None        
        
        #namelist
        self.nameList = ['neck','head','jaw','eye','muzzle','nose','upTeeth',
                         'loTeeth','tongue','ear','nostril']
        self.micoCtrlList = ['','']
        
    def buildGuides(self):
        
        self.neckGuides = []
        self.jawGuides = []
        self.eyeGuides = []
        self.muzzleGuides = []
        self.noseGuides = []
        self.upTeethGuides = []
        
        
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
        for num,pos in enumerate(self.eyePosArray):
            locName = nameUtils.getUniqueName(self.side[1],self.nameList[3],'gud')
            loc = pm.spaceLocator(n = locName)
            loc.t.set(pos)
            self.eyeGuides.append(loc)        
         
        tempEyeGuides = list(self.eyeGuides)
        tempEyeGuides.reverse()
         
        for i in range(len(tempEyeGuides)):
            if i != (len(tempEyeGuides) - 1):
                pm.parent(tempEyeGuides[i],tempEyeGuides[i + 1])                             
    
        #build muzzle guide
        muzzleLocName = nameUtils.getUniqueName(self.side[1],self.nameList[4],'gud')
        muzzleLoc = pm.spaceLocator(n = muzzleLocName)
        muzzleLoc.t.set(self.muzzlePosArray)
        self.muzzleGuides.append(muzzleLoc)
        
        #build upTeeth guide
        upTeethLocName = nameUtils.getUniqueName(self.side[1],self.nameList[6],'gud')
        upTeethLoc = pm.spaceLocator(n = upTeethLocName)
        upTeethLoc.t.set(self.upTeethPosArray)
        self.upTeethGuides.append(upTeethLoc)
        self.upTeethGuides[0].setParent(self.muzzleGuides[0])
    
        #clean up
        self.guideGrp = pm.group(self.neckGuides[0],self.jawGuides[0],self.eyeGuides[0],self.muzzleGuides[0],
                                 n = nameUtils.getUniqueName(self.side[1],self.baseName + 'Gud','grp'))
         
    def build(self):
        
        #get pos info
        #neck pos
        self.neckGuidePos = [x.getTranslation(space = 'world') for x in self.neckGuides]
        self.neckGuideRot = [x.getRotation(space = 'world') for x in self.neckGuides]

        #neck jj set
        self.neckFkChain = fkChain.FkChain(self.nameList[0],self.side[1],self.size,fkCcType = 'cc',type = 'jj')
        self.neckFkChain.fromList(self.neckGuidePos,self.neckGuideRot,skipLast = 1)
 
        for num,joint in enumerate(self.neckFkChain.chain):
            if num == (self.neckFkChain.chainLength() - 1):
                jjName = nameUtils.getUniqueName(self.side[1],self.nameList[1],'jj')
                ccName = nameUtils.getUniqueName(self.side[1],self.nameList[1],'cc')
                ccGrpName = nameUtils.getUniqueName(self.side[1],self.nameList[1],'grp')
                pm.rename(self.neckFkChain.chain[-1],jjName)
                
        headCtrl = control.Control(self.side[1],self.nameList[1],self.size) 
        headCtrl.circleCtrl()
        pm.xform(headCtrl.controlGrp,ws = 1,matrix = self.neckFkChain.chain[-1].worldMatrix.get())
        headCtrl.controlGrp.setParent(self.neckFkChain.controlsArray[-1].control)
        pm.orientConstraint(headCtrl.control,self.neckFkChain.chain[-1],mo = 0)
        
        #jaw jj set

#         self.footChain.chain[-1].setParent(self.footChain.chain[0])
#         self.__addCtrl()
#         self.__connectAttr()
#         self.__cleanUp()

    def __addCtrl(self):
        pass
    
    def __connectAttr(self):
        
        pass
    
    def __cleanUp(self):
        
        pass

        
        
        
        
# from Modules import legModule,footModule
# hg = headModule.HeadModule()
# hg.buildGuides()
# hg.build()
