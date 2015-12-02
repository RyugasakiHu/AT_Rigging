import pymel.core as pm
from Modules.subModules import fkChain,ikChain,boneChain
from Utils import nameUtils,metaUtils
from Modules import control,hierarchy,legModule
from maya import OpenMaya

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
    
    #array for the micro ctrl
    browPosArray = [0,16.556,1.334]
    inBrowLeftPosArray = [0.298,16.556,1.334]
    outBrowLeftPosArray = [0.69,16.556,1.229]
    upCheekLeftPosArray = [0.614,15.913,1.214]
    cheekLeftPosArray = [0.79,15.482,0.869]
    mouthCornerLeftPosArray = [0.423,15.389,1.233]
    upLipMidPosArray = [0,15.474,1.464]
    upLipLeftPosArray = [0.221,15.474,1.464]
    loLipMidPosArray = [0,15.318,1.464]
    loLipLeftPosArray = [0.221,15.318,1.389]
    
    def __init__(self, baseName = 'head',size = 1.5,
                 controlOrient = [0,0,0], metaMain = None,metaSpine = None):
        
        self.baseName = baseName
        self.side = ['l','m','r']
        self.size = size
        
        #jj
        self.neckFkChain = None
#         self.sklGrp = None
        
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
        self.eyeLeftGuides = None
        self.earLeftGuides = None
        self.nostrilLeftGuides = None

        self.earRightGuides = None
        self.eyeRightGuides = None        
        self.nostrilRightGuides = None     
        
        self.jointRightGuideGrp = None
        self.jointLeftGuideGrp = None
        self.jointGuideGrp = None

        #Micro Guides
        self.browCtrlGuides = None
        self.inBrowLeftCtrlGuides = None
        self.outBrowLeftCtrlGuides = None
        self.upCheekCtrlLeftGuides = None
        self.cheekCtrlLeftGuides = None
        self.mouthCornerLeftCtrlGuides = None
        self.upLipMidCtrlGuides = None
        self.loLipMidCtrlGuides = None    
        
        self.microCtrlLeftGuideGrp = None           
        self.tempMirrorMicroGuides = None            
        self.mirrorMicroGuides = None
        self.mirrorMicroCtrlList = None
        self.microCtrlTotalGuideGrp = None        
        
        #control
        #main cc 
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
        self.tongueCtrls = None
        self.earLeftCtrl = None       
        self.earRightCtrl = None
        self.eyeWorldGrp = None
        self.eyeHeadGrp = None
        self.eyeCnstGrp = None   
        self.mainCtrl = None             
        
        #micro cc
        self.browCtrl = None
        self.inBrowLeftCtrl = None
        self.outBrowLeftCtrl = None
        self.upCheekLeftCtrl = None
        self.cheekLeftCtrl = None
        self.mouthCornerLeftCtrl = None      
        self.upLipLeftCtrl = None
        self.loLipLeftCtrl = None
        
        self.upLipMidCtrl = None
        self.loLipMidCtrl = None     
        self.microCtrlGrp = None  
        self.microCtrlList = None
        
        #namelist
        self.nameList = ['neck','head','jaw','eye','muzzle','nose','nostril','upTeeth','loTeeth','tongue','ear','beam']
        self.microCtrlNameList = ['brow','inBrow','outBrow','upCheek','cheek','mouthCorner','upLip','loLip']
        
        #metanode
        self.metaMain = None
        self.metaSpine = None
        self.meta = metaUtils.createMeta(self.side[1],self.baseName,0)
        
    def buildGuides(self):
        
        self.neckGuides = []
        self.jawGuides = []
        self.muzzleGuides = []
        self.noseGuides = []
        self.nostrilLeftGuides = []
        self.upTeethGuides = []
        self.loTeethGuides = []
        self.tongueGuides = []
        self.eyeLeftGuides = []
        self.earLeftGuides = []
        
        self.tempMirrorJointGuideList = []
        self.mirrorJointGuideList = []
        
        self.jointGuideGrp = pm.group(em = 1,n = nameUtils.getUniqueName(self.side[1],self.baseName + 'TotalGud','grp'))
        self.jointMidGuideGrp = pm.group(em = 1,n = nameUtils.getUniqueName(self.side[1],self.baseName + 'Gud','grp'))
        self.jointLeftGuideGrp = pm.group(em = 1,n = nameUtils.getUniqueName(self.side[0],self.baseName + 'Gud','grp'))
        self.jointRightGuideGrp = pm.group(em = 1,n = nameUtils.getUniqueName(self.side[-1],self.baseName + 'Gud','grp'))
        
        self.jointMidGuideGrp.setParent(self.jointGuideGrp)
        self.jointLeftGuideGrp.setParent(self.jointGuideGrp)
        self.jointRightGuideGrp.setParent(self.jointGuideGrp)
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
                
        self.neckGuides[0].setParent(self.jointMidGuideGrp)
        
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
                
        self.jawGuides[0].setParent(self.jointMidGuideGrp)
                
        #build eye guides
        #set loc pos
        #left
        for num,pos in enumerate(self.eyePosArray):
            locName = nameUtils.getUniqueName(self.side[0],self.nameList[3],'gud')
            loc = pm.spaceLocator(n = locName)
            loc.t.set(pos)
            self.eyeLeftGuides.append(loc)

        for eyeLeftGuide in self.eyeLeftGuides:
            eyeLeftGuide.setParent(self.jointLeftGuideGrp)
          
        #build muzzle structure
        #build muzzle guide
        muzzleLocName = nameUtils.getUniqueName(self.side[1],self.nameList[4],'gud')
        muzzleLoc = pm.spaceLocator(n = muzzleLocName)
        muzzleLoc.t.set(self.muzzlePosArray)
        self.muzzleGuides.append(muzzleLoc)
        
        self.muzzleGuides[0].setParent(self.jointMidGuideGrp)
        
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
                     
        self.noseGuides[0].setParent(self.jointMidGuideGrp)
        
        #nostril
        #left loc
        nostrilLeftLocName = nameUtils.getUniqueName(self.side[0],self.nameList[6],'gud')
        nostrilLeftLoc = pm.spaceLocator(n = nostrilLeftLocName)
        nostrilLeftLoc.t.set(self.nostrilPosArray)
        self.nostrilLeftGuides.append(nostrilLeftLoc)
        self.nostrilLeftGuides[0].setParent(self.jointLeftGuideGrp)
        
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
     
        for earLeftGuide in self.earLeftGuides:
            earLeftGuide.setParent(self.jointLeftGuideGrp)
     
        self.__buildMicroCtrlGuides()
        
    def __buildMicroCtrlGuides(self):
        
        self.browCtrlGuides = []
        self.inBrowLeftCtrlGuides = []
        self.outBrowLeftCtrlGuides = []
        self.upCheekCtrlLeftGuides = []
        self.cheekCtrlLeftGuides = []
        self.mouthCornerLeftCtrlGuides = []
        self.upLipMidCtrlGuides = []
        self.upLipLeftCtrlGuides = []
        self.loLipMidCtrlGuides = []
        self.loLipLeftCtrlGuides = []
        
        self.tempMirrorMicroGuides = []
        self.mirrorMicroGuides = []
        
        #brow
        browLocName = nameUtils.getUniqueName(self.side[1],self.microCtrlNameList[0],'gud')
        browLoc = pm.spaceLocator(n = browLocName)
        browLoc.t.set(self.browPosArray)
#         browLoc.r.set(self.browRotArray)
        self.browCtrlGuides.append(browLoc)
        
        #inBrow left
        inBrowLeftLocName = nameUtils.getUniqueName(self.side[0],self.microCtrlNameList[1],'gud')
        inBrowLeftLoc = pm.spaceLocator(n = inBrowLeftLocName)
        inBrowLeftLoc.t.set(self.inBrowLeftPosArray)
#         inBrowLoc.r.set(self.inBrowRotArray)
        self.inBrowLeftCtrlGuides.append(inBrowLeftLoc)
        self.tempMirrorMicroGuides.append(inBrowLeftLoc)
        
        #outBrow left
        outBrowLeftLocName = nameUtils.getUniqueName(self.side[0],self.microCtrlNameList[2],'gud')
        outBrowLeftLoc = pm.spaceLocator(n = outBrowLeftLocName)
        outBrowLeftLoc.t.set(self.outBrowLeftPosArray)
#         outBrowLoc.r.set(self.outBrowRotArray)
        self.outBrowLeftCtrlGuides.append(outBrowLeftLoc)
        self.tempMirrorMicroGuides.append(outBrowLeftLoc)          
            
        #upCheek left 
        upCheekLeftLocName = nameUtils.getUniqueName(self.side[0],self.microCtrlNameList[3],'gud')
        upCheekLeftLoc = pm.spaceLocator(n = upCheekLeftLocName)
        upCheekLeftLoc.t.set(self.upCheekLeftPosArray)
#         upCheekLoc.r.set(self.upCheekRotArray)
        self.upCheekCtrlLeftGuides.append(upCheekLeftLoc)    
        self.tempMirrorMicroGuides.append(upCheekLeftLoc)
        
        #cheek left
        cheekLeftLocName = nameUtils.getUniqueName(self.side[0],self.microCtrlNameList[4],'gud')
        cheekLeftLoc = pm.spaceLocator(n = cheekLeftLocName)
        cheekLeftLoc.t.set(self.cheekLeftPosArray)
#         cheekLoc.r.set(self.browRotArray)
        self.cheekCtrlLeftGuides.append(cheekLeftLoc)
        self.tempMirrorMicroGuides.append(cheekLeftLoc)        
        
        #mouthCorner left
        mouthCornerLeftLocName = nameUtils.getUniqueName(self.side[0],self.microCtrlNameList[5],'gud')
        mouthCornerLeftLoc = pm.spaceLocator(n = mouthCornerLeftLocName)
        mouthCornerLeftLoc.t.set(self.mouthCornerLeftPosArray)
#         cheekLoc.r.set(self.browRotArray)
        self.mouthCornerLeftCtrlGuides.append(mouthCornerLeftLoc)    
        self.tempMirrorMicroGuides.append(mouthCornerLeftLoc)
        
        #upLip
        #mid
        upLipMidLocName = nameUtils.getUniqueName(self.side[1],self.microCtrlNameList[6],'gud')
        upLipMidLoc = pm.spaceLocator(n = upLipMidLocName)
        upLipMidLoc.t.set(self.upLipMidPosArray)
#         cheekLoc.r.set(self.browRotArray)
        self.upLipMidCtrlGuides.append(upLipMidLoc)    
        
        #left
        upLipLeftLocName = nameUtils.getUniqueName(self.side[0],self.microCtrlNameList[6],'gud')
        upLipLeftLoc = pm.spaceLocator(n = upLipLeftLocName)
        upLipLeftLoc.t.set(self.upLipLeftPosArray)
#         cheekLoc.r.set(self.browRotArray)
        self.upLipLeftCtrlGuides.append(upLipLeftLoc)       
        self.tempMirrorMicroGuides.append(upLipLeftLoc)     
        
        #loLip
        #mid
        loLipMidLocName = nameUtils.getUniqueName(self.side[1],self.microCtrlNameList[7],'gud')
        loLipMidLoc = pm.spaceLocator(n = loLipMidLocName)
        loLipMidLoc.t.set(self.loLipMidPosArray)
#         cheekLoc.r.set(self.browRotArray)
        self.loLipMidCtrlGuides.append(loLipMidLoc)
        
        #left
        loLipLeftLocName = nameUtils.getUniqueName(self.side[0],self.microCtrlNameList[7],'gud')
        loLipLeftLoc = pm.spaceLocator(n = loLipLeftLocName)
        loLipLeftLoc.t.set(self.loLipLeftPosArray)
#         cheekLoc.r.set(self.browRotArray)
        self.loLipLeftCtrlGuides.append(loLipLeftLoc)
        self.tempMirrorMicroGuides.append(loLipLeftLoc)
                
        self.microCtrlLeftGuideGrp = pm.group(self.inBrowLeftCtrlGuides[0],self.outBrowLeftCtrlGuides[0],
                                                 self.upCheekCtrlLeftGuides[0],self.cheekCtrlLeftGuides[0],
                                                 self.loLipLeftCtrlGuides[0],self.upLipLeftCtrlGuides[0],
                                                 self.mouthCornerLeftCtrlGuides[0],n = nameUtils.getUniqueName(self.side[0],self.baseName + 'McGud','grp'))
        
        self.microCtrlTotalGuideGrp = pm.group(self.browCtrlGuides[0],self.loLipMidCtrlGuides[0],
                                               self.upLipMidCtrlGuides[0],self.microCtrlLeftGuideGrp,
                                               n = nameUtils.getUniqueName(self.side[1],self.baseName + 'McGud','grp'))        
                         
    def __mirrorJointGuide(self):  
        
        self.eyeRightGuides = [] 
        self.nostrilRightGuides = []            
        self.earRightGuides = []

        #right eyes
        for leftGuide in self.eyeLeftGuides:
            mirrorJointGuide = pm.duplicate(leftGuide)
            mirrorJointGuideTranslation = mirrorJointGuide[0].getTranslation(space = 'world')
            mirrorJointGuide[0].tx.set(-mirrorJointGuideTranslation[0])
             
            mirrorJointGuideRotate = mirrorJointGuide[0].getRotation()
            mirrorJointGuide[0].rx.set(mirrorJointGuideRotate[0])
            mirrorJointGuide[0].ry.set(-mirrorJointGuideRotate[1])
            mirrorJointGuide[0].rz.set(-mirrorJointGuideRotate[2])            
             
            #rename
            oriName = mirrorJointGuide[0].name()
            temp = oriName.split('_')
            mirrorName = nameUtils.getUniqueName(self.side[-1], temp[1], 'gud')
            pm.rename(oriName,mirrorName)
            self.eyeRightGuides.append(mirrorJointGuide)            
            mirrorJointGuide[0].setParent(self.jointRightGuideGrp)
            
        #nostril
        for leftGuide in self.nostrilLeftGuides:
            mirrorJointGuide = pm.duplicate(leftGuide)
            mirrorJointGuideTranslation = mirrorJointGuide[0].getTranslation(space = 'world')
            mirrorJointGuide[0].tx.set(-mirrorJointGuideTranslation[0])
             
            mirrorJointGuideRotate = mirrorJointGuide[0].getRotation()
            mirrorJointGuide[0].rx.set(mirrorJointGuideRotate[0])
            mirrorJointGuide[0].ry.set(-mirrorJointGuideRotate[1])
            mirrorJointGuide[0].rz.set(-mirrorJointGuideRotate[2])            
             
            #rename
            oriName = mirrorJointGuide[0].name()
            temp = oriName.split('_')
            mirrorName = nameUtils.getUniqueName(self.side[-1], temp[1], 'gud')
            pm.rename(oriName,mirrorName)
            self.nostrilRightGuides.append(mirrorJointGuide)
            mirrorJointGuide[0].setParent(self.jointRightGuideGrp)

        #ear
        for leftGuide in self.earLeftGuides:
            mirrorJointGuide = pm.duplicate(leftGuide)
            mirrorJointGuideTranslation = mirrorJointGuide[0].getTranslation(space = 'world')
            mirrorJointGuide[0].tx.set(-mirrorJointGuideTranslation[0])
             
            mirrorJointGuideRotate = mirrorJointGuide[0].getRotation()
            mirrorJointGuide[0].rx.set(mirrorJointGuideRotate[0])
            mirrorJointGuide[0].ry.set(-mirrorJointGuideRotate[1])
            mirrorJointGuide[0].rz.set(-mirrorJointGuideRotate[2])            
             
            #rename
            oriName = mirrorJointGuide[0].name()
            temp = oriName.split('_')
            mirrorName = nameUtils.getUniqueName(self.side[-1], temp[1], 'gud')
            pm.rename(oriName,mirrorName)
            self.earRightGuides.append(mirrorJointGuide)
            mirrorJointGuide[0].setParent(self.jointRightGuideGrp)
                                   
    def build(self):
        
        self.__mirrorJointGuide()   
        
        self.jointGuideGrp.v.set(0)
        self.mainCtrl = []
        
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
        self.neckFkChain = fkChain.FkChain(self.nameList[0],self.side[1],size = self.size[0],
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
        
        for neckCc in self.neckFkChain.controlsArray:
            self.mainCtrl.append(neckCc.control)
        self.mainCtrl.append(self.headCtrl.control)        
        
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
        self.eyeRightGuidePos = [x[0].getTranslation(space = 'world') for x in self.eyeRightGuides]
        self.eyeRightGuideRot = [x[0].getRotation(space = 'world') for x in self.eyeRightGuides]        

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
        
        #right nostril jj
        self.nostrilRightGuidePos = [x[0].getTranslation(space = 'world') for x in self.nostrilRightGuides]
        self.nostrilRightGuideRot = [x[0].getRotation(space = 'world') for x in self.nostrilRightGuides]
        
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
        
        #right ear pos get
        self.earRightGuidePos = [x[0].getTranslation(space = 'world') for x in self.earRightGuides]
        self.earRightGuideRot = [x[0].getRotation(space = 'world') for x in self.earRightGuides]

        #left ear jj set and clean
        self.earRightChain = boneChain.BoneChain(self.nameList[10],self.side[0],type = 'jj')
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
        self.tongueChain = boneChain.BoneChain(self.nameList[9],self.side[1],type = 'jj')
        self.tongueChain.fromList(self.tongueGuidePos,self.tongueGuideRot)
        self.tongueChain.chain[0].setParent(self.jawChains.chain[0])
#         self.tongueFkChain = fkChain.FkChain(self.nameList[9],self.side[1],size = self.tongueDis * 0.75,
#                                              fkCcType = 'cc',type = 'jj',pointCnst = 1)
#         self.tongueFkChain.fromList(self.tongueGuidePos,self.tongueGuideRot,skipLast = 1,autoOrient = 1)
#         self.tongueFkChain.chain[0].setParent(self.jawChains.chain[0])
#         self.tongueFkChain.controlsArray[0].control.setParent(self.jawCtrl.control)

        #correct jj orient
        pm.select(self.muzzleChain)
        pm.joint(e = 1,oj = 'xyz',secondaryAxisOrient = 'zdown',ch = 1)
        
        pm.select(self.tongueChain.chain[0])
        pm.joint(e = 1,oj = 'xzy',secondaryAxisOrient = 'xdown',ch = 1,zso = 1)       
        
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

        self.__mirrorMicroGuides()
        self.__addMainCtrl()
        self.__addMicroCtrl()
        self.__cleanUp()
        
    def __mirrorMicroGuides(self):        
        
        #mirror to right
        for gud in self.tempMirrorMicroGuides:
            #duplicate and set pos
            mirror = pm.duplicate(gud)
            mirrorValueTx = gud.tx.get()
            mirror[0].tx.set(-mirrorValueTx)
            
            mirrorValueRx = gud.rx.get()
            mirror[0].rx.set(mirrorValueRx)
            
            mirrorValueRy = gud.ry.get()
            mirror[0].ry.set(-mirrorValueRy)
            
            mirrorValueRz = gud.rz.get()
            mirror[0].rz.set(-mirrorValueRz)
                
            #rename
            oriName = mirror[0].name()
            temp = oriName.split('_')
            mirrorName = nameUtils.getUniqueName(self.side[-1], temp[1], 'gud')
            pm.rename(oriName,mirrorName)
            self.mirrorMicroGuides.append(mirror)             
        
        self.microCtrlRightGuideGrp = pm.group(em = 1,n = nameUtils.getUniqueName(self.side[-1],self.baseName + 'McGud','grp')) 
        
        for loc in self.mirrorMicroGuides:
            loc[0].setParent(self.microCtrlRightGuideGrp)
            
        #clean

        self.microCtrlRightGuideGrp.setParent(self.microCtrlTotalGuideGrp)
        self.microCtrlTotalGuideGrp.v.set(0)

    def __addMainCtrl(self):

        
        #create jawCtrl
        self.jawCtrl = control.Control(self.side[1],self.nameList[2],size = self.neckDis * 2) 
        self.jawCtrl.cubeCtrl()
        control.lockAndHideAttr(self.jawCtrl.control,['sx','sy','sz','v'])
        
        #align
        pm.xform(self.jawCtrl.controlGrp,ws = 1,matrix = self.jawChains.chain[0].worldMatrix.get())
        pm.orientConstraint(self.jawCtrl.control,self.jawChains.chain[0],mo = 0)
        pm.pointConstraint(self.jawCtrl.control,self.jawChains.chain[0],mo = 0)
#         self.tongueFkChain.controlsArray[0].controlGrp.setParent(self.jawCtrl.control)
        self.jawCtrl.controlGrp.setParent(self.headCtrl.control)
        self.mainCtrl.append(self.jawCtrl.control)        
        
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
                
        self.mainCtrl.append(self.eyeRightCtrl.control)
        self.mainCtrl.append(self.eyeLeftCtrl.control)
        
        #create muzzle cc
        self.muzzleCtrl = control.Control(self.side[1],self.nameList[4],size = self.tongueDis,aimAxis = 'y') 
        self.muzzleCtrl.circleCtrl()
        pm.xform(self.muzzleCtrl.controlGrp,ws = 1,matrix = self.muzzleChain.worldMatrix.get())
        pm.orientConstraint(self.muzzleCtrl.control,self.muzzleChain,mo = 0)
        pm.pointConstraint(self.muzzleCtrl.control,self.muzzleChain,mo = 0) 
        self.muzzleCtrl.controlGrp.setParent(self.headCtrl.control)
        self.mainCtrl.append(self.muzzleCtrl.control)       
                
        self.noseCtrl = control.Control(self.side[1],self.nameList[5],size = self.tongueDis,aimAxis = 'y') 
        self.noseCtrl.circleCtrl()
        pm.xform(self.noseCtrl.controlGrp,ws = 1,matrix = self.noseChain.chain[0].worldMatrix.get())
        pm.orientConstraint(self.noseCtrl.control,self.noseChain.chain[0],mo = 0)
        pm.pointConstraint(self.noseCtrl.control,self.noseChain.chain[0],mo = 0) 
        self.noseCtrl.controlGrp.setParent(self.muzzleCtrl.control)
        self.mainCtrl.append(self.noseCtrl.control)               
        
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
        
        self.mainCtrl.append(self.nostrilRightCtrl.control)
        self.mainCtrl.append(self.nostrilLeftCtrl.control)    
        
        #create upTeethCtrl
        self.upTeethCtrl = control.Control(self.side[1],self.nameList[7],size = float(self.tongueDis * 1.5),aimAxis = 'y') 
        self.upTeethCtrl.circleCtrl()
        control.lockAndHideAttr(self.upTeethCtrl.control,['sx','sy','sz','v'])
        pm.xform(self.upTeethCtrl.controlGrp,ws = 1,matrix = self.upTeethChain.worldMatrix.get())
        pm.orientConstraint(self.upTeethCtrl.control,self.upTeethChain,mo = 0)
        pm.pointConstraint(self.upTeethCtrl.control,self.upTeethChain,mo = 0)
        self.upTeethCtrl.controlGrp.setParent(self.noseCtrl.control)
        self.mainCtrl.append(self.upTeethCtrl.control)            
        
        #create loTeethCtrl
        self.loTeethCtrl = control.Control(self.side[1],self.nameList[8],size = float(self.tongueDis * 1.5),aimAxis = 'y') 
        self.loTeethCtrl.circleCtrl()
        control.lockAndHideAttr(self.loTeethCtrl.control,['sx','sy','sz','v'])
        pm.xform(self.loTeethCtrl.controlGrp,ws = 1,matrix = self.loTeethChain.worldMatrix.get())
        pm.orientConstraint(self.loTeethCtrl.control,self.loTeethChain,mo = 0)
        pm.pointConstraint(self.loTeethCtrl.control,self.loTeethChain,mo = 0)
        self.loTeethCtrl.controlGrp.setParent(self.jawCtrl.control)
        self.mainCtrl.append(self.loTeethCtrl.control)               
                
        #create tongueCtrl                
        self.tongueCtrls = []
        for num,chain in enumerate(self.tongueChain.chain):
            if num != len(self.tongueChain.chain) - 1:
                #create cc
                self.tongueCtrl = control.Control(self.side[1],self.nameList[9],size = float(self.tongueDis * 1.0),aimAxis = 'x') 
                self.tongueCtrl.circleCtrl()
                pm.xform(self.tongueCtrl.controlGrp,ws = 1,matrix = chain.worldMatrix.get())
                pm.orientConstraint(self.tongueCtrl.control,chain,mo = 0)
                pm.pointConstraint(self.tongueCtrl.control,chain,mo = 0)
                self.tongueCtrls.append(self.tongueCtrl.controlGrp)
                self.mainCtrl.append(self.tongueCtrl.control)

        self.tongueCtrls.reverse()            
        for num,ctrlGrp in enumerate(self.tongueCtrls):
            if num != len(self.tongueCtrls) - 1:
                ctrlGrp.setParent(self.tongueCtrls[num + 1].getChildren())
        
        self.tongueCtrls[-1].setParent(self.loTeethCtrl.control)
             
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
        
        self.mainCtrl.append(self.earRightCtrl.control)
        self.mainCtrl.append(self.earLeftCtrl.control)
        
        #create eyeCtrl
        #create eye aim create
        self.eyeAimCtrl = control.Control(self.side[1],self.nameList[3] + 'Aim',size = self.eyeRad) 
        self.eyeAimCtrl.plusCtrl()
        pcn = pm.pointConstraint(self.eyeLeftChain.chain[0],self.eyeRightChain.chain[0],
                                 self.eyeAimCtrl.controlGrp,mo = 0)
        pm.delete(pcn)
        pm.move(self.eyeAimCtrl.controlGrp,0,self.eyeAimCtrl.controlGrp.ty.get(),self.neckDis * 5)
        control.lockAndHideAttr(self.eyeAimCtrl.control,['sx','sy','sz','v'])
        self.mainCtrl.append(self.eyeAimCtrl.control)
        
        #left ctrl set and pos
        self.eyeLeftAimCtrl = control.Control(self.side[0],self.nameList[3] + 'Aim',size = float(self.tongueDis * 1)) 
        self.eyeLeftAimCtrl.circleCtrl()
        pm.xform(self.eyeLeftAimCtrl.controlGrp,ws = 1,matrix = self.eyeLeftChain.chain[0].worldMatrix.get())
        pm.move(self.eyeLeftAimCtrl.controlGrp,self.eyeLeftAimCtrl.controlGrp.tx.get(),
                self.eyeLeftAimCtrl.controlGrp.ty.get(),self.neckDis * 5)
        self.eyeLeftAimCtrl.controlGrp.setParent(self.eyeAimCtrl.control)
        control.lockAndHideAttr(self.eyeLeftAimCtrl.control,['sx','sy','sz','v'])
        self.mainCtrl.append(self.eyeLeftAimCtrl.control)
        
        #aim curve
        leftAimCurve = pm.curve(d = 1,p = [self.eyeLeftChain.chain[0].getTranslation(space = 'world'),
                                           self.eyeLeftAimCtrl.controlGrp.getTranslation(space = 'world')],k = [0,1],
                                n = nameUtils.getUniqueName(self.side[0],self.nameList[11],'cc'))
        leftAimCurve.overrideEnabled.set(1)
        leftAimCurve.overrideDisplayType.set(1)
        
        #cls
        leftClusterStart = pm.cluster(leftAimCurve.cv[0])
        pm.rename(leftClusterStart[1].name(),nameUtils.getUniqueName(self.side[0],self.nameList[11] + 'Start','cls'))
        leftClusterStart[1].setParent(self.eyeLeftCtrl.control)
        leftClusterStart[1].v.set(0)
        
        leftClusterEnd = pm.cluster(leftAimCurve.cv[1])
        pm.rename(leftClusterEnd[1].name(),nameUtils.getUniqueName(self.side[0],self.nameList[11] + 'End','cls'))
        leftClusterEnd[1].setParent(self.eyeLeftAimCtrl.control)
        leftClusterEnd[1].v.set(0)
        
        #eye ball grp
        eyeLeftBallGrp = pm.group(em = 1,n = nameUtils.getUniqueName(self.side[0],self.nameList[3] + 'Ball','grp'))
        pm.xform(eyeLeftBallGrp,ws = 1,matrix = self.eyeLeftChain.chain[0].worldMatrix.get())
        pm.aimConstraint(self.eyeLeftAimCtrl.control,eyeLeftBallGrp,w = 1,offset = [0,0,0],
                         aimVector = [1,0,0],upVector = [0,1,0],worldUpType = 'scene')
        
        eyeLeftBallGrp.setParent(self.eyeLeftCtrl.controlGrp)
        self.eyeLeftCtrl.control.setParent(eyeLeftBallGrp)

        pm.orientConstraint(self.eyeLeftCtrl.control,self.eyeLeftChain.chain[0],mo = 0)
        pm.pointConstraint(self.eyeLeftCtrl.control,self.eyeLeftChain.chain[0],mo = 0)
    
        #right ctrl set and pos
        self.eyeRightAimCtrl = control.Control(self.side[2],self.nameList[3] + 'Aim',size = float(self.tongueDis * 1)) 
        self.eyeRightAimCtrl.circleCtrl()
        
        pm.xform(self.eyeRightAimCtrl.controlGrp,ws = 1,matrix = self.eyeRightChain.chain[0].worldMatrix.get())
        pm.move(self.eyeRightAimCtrl.controlGrp,self.eyeRightAimCtrl.controlGrp.tx.get(),
                self.eyeRightAimCtrl.controlGrp.ty.get(),self.neckDis * 5)        
        self.eyeRightAimCtrl.controlGrp.setParent(self.eyeAimCtrl.control)
        control.lockAndHideAttr(self.eyeRightAimCtrl.control,['sx','sy','sz','v'])
        self.mainCtrl.append(self.eyeRightAimCtrl.control)
            
        #aim curve    
        rightAimCurve = pm.curve(d = 1,p = [self.eyeRightChain.chain[0].getTranslation(space = 'world'),
                                            self.eyeRightAimCtrl.controlGrp.getTranslation(space = 'world')],k = [0,1],
                                n = nameUtils.getUniqueName(self.side[2],self.nameList[11],'cc'))
        rightAimCurve.overrideEnabled.set(1)
        rightAimCurve.overrideDisplayType.set(1)        
        
        #cls
        rightClusterStart = pm.cluster(rightAimCurve.cv[0])
        pm.rename(rightClusterStart[1].name(),nameUtils.getUniqueName(self.side[2],self.nameList[11] + 'Start','cls'))
        rightClusterStart[1].setParent(self.eyeRightCtrl.control)
        rightClusterStart[1].v.set(0)
        
        rightClusterEnd = pm.cluster(rightAimCurve.cv[1])
        pm.rename(rightClusterEnd[1].name(),nameUtils.getUniqueName(self.side[2],self.nameList[11] + 'End','cls'))
        rightClusterEnd[1].setParent(self.eyeRightAimCtrl.control)   
        rightClusterEnd[1].v.set(0)   
        
        #eye ball grp
        eyeRightBallGrp = pm.group(em = 1,n = nameUtils.getUniqueName(self.side[2],self.nameList[3] + 'Ball','grp'))
        pm.xform(eyeRightBallGrp,ws = 1,matrix = self.eyeRightChain.chain[0].worldMatrix.get())
        pm.aimConstraint(self.eyeRightAimCtrl.control,eyeRightBallGrp,w = 1,offset = [0,0,0],
                         aimVector = [1,0,0],upVector = [0,1,0],worldUpType = 'scene')
        
        eyeRightBallGrp.setParent(self.eyeRightCtrl.controlGrp)
        self.eyeRightCtrl.control.setParent(eyeRightBallGrp)        
           
        pm.orientConstraint(self.eyeRightCtrl.control,self.eyeRightChain.chain[0],mo = 0)
        pm.pointConstraint(self.eyeRightCtrl.control,self.eyeRightChain.chain[0],mo = 0)  
        
        #clean up
        #beam
        eyeBeamGrp = pm.group(em = 1,n = nameUtils.getUniqueName(self.side[1],self.nameList[3] + 'Beam','grp'))
        leftAimCurve.setParent(eyeBeamGrp)
        rightAimCurve.setParent(eyeBeamGrp)
        #Beam UNDER EXTRA GRP
        
        #aim grp under IK grp
        
    def __addMicroCtrl(self):
        
        self.microCtrlGrp = pm.group(em = 1,n = nameUtils.getUniqueName(self.side[1],'microCtrl','grp'))
        self.mirrorMicroCtrlList = []
        self.microCtrlList = []
        
        #brow
        self.browCtrl = control.Control(self.side[1],self.microCtrlNameList[0],self.size) 
        self.browCtrl.microCtrl()
        pm.xform(self.browCtrl.controlGrp,ws = 1,matrix = self.browCtrlGuides[0].worldMatrix.get())
        self.browCtrl.controlGrp.s.set(self.tongueDis / 2,self.tongueDis / 2,self.tongueDis / 2)
        self.browCtrl.controlGrp.setParent(self.microCtrlGrp)
        self.microCtrlList.append(self.browCtrl.control)
        
        #inBrowLeft
        self.inBrowLeftCtrl = control.Control(self.side[0],self.microCtrlNameList[1],self.size) 
        self.inBrowLeftCtrl.microCtrl()
        pm.xform(self.inBrowLeftCtrl.controlGrp,ws = 1,matrix = self.inBrowLeftCtrlGuides[0].worldMatrix.get())
        self.inBrowLeftCtrl.controlGrp.s.set(self.tongueDis / 2,self.tongueDis / 2,self.tongueDis / 2)
        self.inBrowLeftCtrl.controlGrp.setParent(self.microCtrlGrp)
        self.microCtrlList.append(self.inBrowLeftCtrl.control)
        
        #outBrowLeft
        self.outBrowLeftCtrl = control.Control(self.side[0],self.microCtrlNameList[2],self.size) 
        self.outBrowLeftCtrl.microCtrl()
        pm.xform(self.outBrowLeftCtrl.controlGrp,ws = 1,matrix = self.outBrowLeftCtrlGuides[0].worldMatrix.get())
        self.outBrowLeftCtrl.controlGrp.s.set(self.tongueDis / 2,self.tongueDis / 2,self.tongueDis / 2)
        self.outBrowLeftCtrl.controlGrp.setParent(self.microCtrlGrp)
        self.microCtrlList.append(self.outBrowLeftCtrl.control)
        
        #upCheekLeft
        self.upCheekLeftCtrl = control.Control(self.side[0],self.microCtrlNameList[3],self.size) 
        self.upCheekLeftCtrl.microCtrl()
        pm.xform(self.upCheekLeftCtrl.controlGrp,ws = 1,matrix = self.upCheekCtrlLeftGuides[0].worldMatrix.get())
        self.upCheekLeftCtrl.controlGrp.s.set(self.tongueDis / 2,self.tongueDis / 2,self.tongueDis / 2)
        self.upCheekLeftCtrl.controlGrp.setParent(self.microCtrlGrp)
        self.microCtrlList.append(self.upCheekLeftCtrl.control)
        
        #cheekLeft
        self.cheekLeftCtrl = control.Control(self.side[0],self.microCtrlNameList[4],self.size) 
        self.cheekLeftCtrl.microCtrl()
        pm.xform(self.cheekLeftCtrl.controlGrp,ws = 1,matrix = self.cheekCtrlLeftGuides[0].worldMatrix.get())
        self.cheekLeftCtrl.controlGrp.s.set(self.tongueDis / 2,self.tongueDis / 2,self.tongueDis / 2)
        self.cheekLeftCtrl.controlGrp.setParent(self.microCtrlGrp)
        self.microCtrlList.append(self.cheekLeftCtrl.control)
        
        #mouthCornerLeft
        self.mouthCornerLeftCtrl = control.Control(self.side[0],self.microCtrlNameList[5],self.size) 
        self.mouthCornerLeftCtrl.microCtrl()
        pm.xform(self.mouthCornerLeftCtrl.controlGrp,ws = 1,matrix = self.mouthCornerLeftCtrlGuides[0].worldMatrix.get())
        self.mouthCornerLeftCtrl.controlGrp.s.set(self.tongueDis / 2,self.tongueDis / 2,self.tongueDis / 2)
        self.mouthCornerLeftCtrl.controlGrp.setParent(self.microCtrlGrp)
        self.microCtrlList.append(self.mouthCornerLeftCtrl.control)
        
        #upLipLeft        
        self.upLipLeftCtrl = control.Control(self.side[0],self.microCtrlNameList[6],self.size) 
        self.upLipLeftCtrl.microCtrl()
        pm.xform(self.upLipLeftCtrl.controlGrp,ws = 1,matrix = self.upLipLeftCtrlGuides[0].worldMatrix.get())
        self.upLipLeftCtrl.controlGrp.s.set(self.tongueDis / 2,self.tongueDis / 2,self.tongueDis / 2)
        self.upLipLeftCtrl.controlGrp.setParent(self.microCtrlGrp)
        self.microCtrlList.append(self.upLipLeftCtrl.control)
        
        #loLipLeft
        self.loLipLeftCtrl = control.Control(self.side[0],self.microCtrlNameList[7],self.size) 
        self.loLipLeftCtrl.microCtrl()
        pm.xform(self.loLipLeftCtrl.controlGrp,ws = 1,matrix = self.loLipLeftCtrlGuides[0].worldMatrix.get())
        self.loLipLeftCtrl.controlGrp.s.set(self.tongueDis / 2,self.tongueDis / 2,self.tongueDis / 2)
        self.loLipLeftCtrl.controlGrp.setParent(self.microCtrlGrp)
        self.microCtrlList.append(self.loLipLeftCtrl.control)          
        
        #upLipMid
        self.upLipMidCtrl = control.Control(self.side[1],self.microCtrlNameList[6],self.size) 
        self.upLipMidCtrl.microCtrl()
        pm.xform(self.upLipMidCtrl.controlGrp,ws = 1,matrix = self.upLipMidCtrlGuides[0].worldMatrix.get())
        self.upLipMidCtrl.controlGrp.s.set(self.tongueDis / 2,self.tongueDis / 2,self.tongueDis / 2)
        self.upLipMidCtrl.controlGrp.setParent(self.microCtrlGrp)
        self.microCtrlList.append(self.upLipMidCtrl.control)              
        
        #loLipMid
        self.loLipMidCtrl = control.Control(self.side[1],self.microCtrlNameList[7],self.size) 
        self.loLipMidCtrl.microCtrl()
        pm.xform(self.loLipMidCtrl.controlGrp,ws = 1,matrix = self.loLipMidCtrlGuides[0].worldMatrix.get())
        self.loLipMidCtrl.controlGrp.s.set(self.tongueDis / 2,self.tongueDis / 2,self.tongueDis / 2)
        self.loLipMidCtrl.controlGrp.setParent(self.microCtrlGrp)
        self.microCtrlList.append(self.loLipMidCtrl.control)
        
        #add mirror microList
        for num,loc in enumerate(self.mirrorMicroGuides):
            self.mirrorMicroCtrl = control.Control(self.side[2],self.microCtrlNameList[num + 1],self.size) 
            self.mirrorMicroCtrl.microCtrl()
             
            pm.xform(self.mirrorMicroCtrl.controlGrp,ws = 1,matrix = self.mirrorMicroGuides[num][0].worldMatrix.get())
            self.mirrorMicroCtrl.controlGrp.s.set(self.tongueDis / 2,self.tongueDis / 2,self.tongueDis / 2)
            self.mirrorMicroCtrl.controlGrp.setParent(self.microCtrlGrp)            
            
            self.mirrorMicroCtrlList.append(self.mirrorMicroCtrl.controlGrp)
            self.mirrorMicroCtrl.controlGrp.setParent(self.microCtrlGrp)
            self.microCtrlList.append(self.mirrorMicroCtrl.control)   
            
        self.microCtrlGrp.setParent(self.headCtrl.control)
        
        #aim follow world and head
        self.eyeWorldGrp = pm.group(em = 1,n = nameUtils.getUniqueName(self.side[1],self.nameList[3] + 'MoveParent2World','grp')) 
        pm.xform(self.eyeWorldGrp,ws = 1,matrix = self.eyeAimCtrl.controlGrp.worldMatrix.get())

        self.eyeHeadGrp = pm.group(em = 1,n = nameUtils.getUniqueName(self.side[1],self.nameList[3] + 'MoveParent2Head','grp'))
        pm.xform(self.eyeHeadGrp,ws = 1,matrix = self.eyeAimCtrl.controlGrp.worldMatrix.get())
        
        self.eyeCnstGrp = pm.group(em = 1,n = nameUtils.getUniqueName(self.side[1],self.nameList[3] + 'Cnst','grp'))
        pm.xform(self.eyeCnstGrp,ws = 1,matrix = self.eyeAimCtrl.controlGrp.worldMatrix.get())

        #create cnst
        oriCnst = pm.orientConstraint(self.eyeWorldGrp,self.eyeHeadGrp,self.eyeCnstGrp,mo = 0)
        pntCnst = pm.pointConstraint(self.eyeWorldGrp,self.eyeHeadGrp,self.eyeCnstGrp,mo = 0)
        
        self.eyeCnstGrp.setParent(self.eyeAimCtrl.controlGrp)
        self.eyeAimCtrl.control.setParent(self.eyeCnstGrp)
        control.addFloatAttr(self.eyeAimCtrl.control,['cnst2Head'],0,1)
        
        #connect
        pm.connectAttr(self.eyeAimCtrl.control + '.cnst2Head',pntCnst + '.' + self.eyeHeadGrp.name() + 'W1')
        pm.connectAttr(self.eyeAimCtrl.control + '.cnst2Head',oriCnst + '.' + self.eyeHeadGrp.name() + 'W1')
#         self.eyeWorldGrp.setParent(self.eyeCnstGrp) pallera
        self.eyeHeadGrp.setParent(self.headCtrl.control)

        #create node name
        reverseNodeName = nameUtils.getUniqueName(self.side[1],self.nameList[3] + 'cnst2Head','REV')
        reverseNode = pm.createNode('reverse',n = reverseNodeName)
        
        self.eyeAimCtrl.control.cnst2Head.connect(reverseNode.inputX)
        pm.connectAttr(reverseNode.outputX,pntCnst + '.' + self.eyeWorldGrp.name() + 'W0')
        pm.connectAttr(reverseNode.outputX,oriCnst + '.' + self.eyeWorldGrp.name() + 'W0')
        
    def __cleanUp(self):
        
#         metaUtils.addToMeta(self.meta,, objs)
#         metaUtils.addToMeta(self.meta,'moduleGrp', [self.ALL])  
        metaUtils.addToMeta(self.meta,'controls', self.microCtrlList + self.mainCtrl)

    def buildConnections(self):
        pass

class LidClass(object):

    def __init__(self,eyeBall,lidSide):
        
        #initial
        self.eyeBall = eyeBall
        self.lidSide = None
        self.lidPos = None
        
        #list
        self.upVertexes = None
        self.downVertexes = None
        self.upJj = None
        self.downJj = None
        self.upLocList = None
        self.downLocList = None
        
        #curve
        self.eyeUpHiCur = None
        self.eyeDnHiCur = None
        
        #grp
        self.upJointGrp = None
        self.downJointGrp = None
        self.upLocGrp = None
        self.downLocGrp = None
        
        #loc
        self.aimLoc = None
        
        #name
        self.nameList = ['lid','Base','Hi','Lo','Blink','Up','Dn','Aim','Loc']
        
        if lidSide == 1:
            self.lidSide = 'l'
         
        elif lidSide == 2:
            self.lidSide =  'r'

    def createLid(self,*arg):
 
        self.__createLoc()
        self.__createJj()
        self.__createAimCnst()
        self.__createHiCurve()
        self.__locToCurve()
    
    def loadUpVertex(self):
        
        self.upVertexes = []
        upVertexes = pm.ls(os = 1,fl = 1)
        
        for upVertex in upVertexes:
            self.upVertexes.append(upVertex)
        
        print self.upVertexes
        return self.upVertexes
        
    def loadDnVertex(self):
        
        self.downVertexes = []
        downVertexes = pm.ls(os = 1,fl = 1)
        
        for downVertex in downVertexes:
            self.downVertexes.append(downVertex)

        return self.downVertexes
    
    def __createLoc(self):
        
        #create base loc make center
        pm.select(self.eyeBall)
        self.eyeBall = pm.selected()
        self.baseLoc = pm.spaceLocator(n = nameUtils.getUniqueName(self.lidSide,self.nameList[0] + self.nameList[1],'loc'))
        pm.xform(self.baseLoc,ws = 1,matrix = self.eyeBall[0].worldMatrix.get())
        pm.select(cl = 1)
        
    def __createJj(self):
        
        self.upJj = []
        self.downJj = []
        
        self.upJointGrp = pm.group(em = 1,n = nameUtils.getUniqueName(self.lidSide,self.nameList[0] + self.nameList[5],'grp'))
        self.downJointGrp = pm.group(em = 1,n = nameUtils.getUniqueName(self.lidSide,self.nameList[0] + self.nameList[6],'grp'))
        
        #up 
        for upVertex in self.upVertexes:
             
            #create je and align
            je = pm.joint(n = nameUtils.getUniqueName(self.lidSide,self.nameList[0] + self.nameList[5],'je'))
            pos = pm.xform(upVertex, q=1, ws=1, t=1)
            pm.xform(je, ws=1, t=pos)
             
            #create jj
            pm.select(cl=1)
            jj=pm.joint(n = nameUtils.getUniqueName(self.lidSide,self.nameList[0] + self.nameList[5],'jj'))
            alginCnst = pm.pointConstraint(self.eyeBall[0],jj,mo = 0)
            pm.delete(alginCnst)
             
            pm.parent(je, jj)
            self.upJj.append(jj)
             
            #orient joints
            pm.joint (jj, e=1, oj='xyz', secondaryAxisOrient='yup', ch=1, zso=1)
             
            #clean up
            jj.setParent(self.upJointGrp)
        
        #down
        for downVertex in self.downVertexes:
             
            #create je and align
            je = pm.joint(n = nameUtils.getUniqueName(self.lidSide,self.nameList[0] + self.nameList[6],'je'))
            pos = pm.xform(downVertex, q=1, ws=1, t=1)
            pm.xform(je, ws=1, t=pos)
             
            #create jj
            pm.select(cl=1)
            jj=pm.joint(n = nameUtils.getUniqueName(self.lidSide,self.nameList[0] + self.nameList[6],'jj'))
            alginCnst = pm.pointConstraint(self.eyeBall[0],jj,mo = 0)
            pm.delete(alginCnst)
             
            pm.parent(je, jj)
            self.downJj.append(jj)
             
            #orient joints
            pm.joint (jj, e=1, oj='xyz', secondaryAxisOrient='yup', ch=1, zso=1)
            
            #clean up
            jj.setParent(self.downJointGrp)
        
    def __createAimCnst(self):
        
        #init   
        self.upLocList = []
        self.downLocList = []
        self.upLocGrp = pm.group(em = 1,n = nameUtils.getUniqueName(self.lidSide,self.nameList[0] + self.nameList[5] + self.nameList[8],'grp'))
        self.downLocGrp = pm.group(em = 1,n = nameUtils.getUniqueName(self.lidSide,self.nameList[0] + self.nameList[6] + self.nameList[8],'grp'))
           
        #create aim loc
        aimLocName = nameUtils.getUniqueName(self.lidSide,self.nameList[0] + self.nameList[7],'loc')
        self.aimLoc = pm.spaceLocator(n = aimLocName)
        eyeBallPos = pm.xform(self.upJj[0], q=1, ws=1, t=1)
        pm.xform(self.aimLoc,ws = 1,t = (eyeBallPos[0],eyeBallPos[1] + self.upJj[len(self.upJj) / 2].getChildren()[0].tx.get(),eyeBallPos[2]))
        
        #up 
        for upJj in self.upJj:
            locName = nameUtils.getUniqueName(self.lidSide,self.nameList[0] + self.nameList[5],'loc')
            loc = pm.spaceLocator(n = locName)
            self.upLocList.append(loc)
            pos = pm.xform(upJj.getChildren(), q=1, ws=1, t=1)
            pm.xform(loc, ws=1, t=pos)
            loc.setParent(self.upLocGrp)
            
            pm.aimConstraint(loc, upJj, mo=1, weight=1, aimVector= (1,0,0), upVector = (0,1,0),
                            worldUpType='object', worldUpObject=self.aimLoc)
            
        #down
        for downJj in self.downJj:
            locName = nameUtils.getUniqueName(self.lidSide,self.nameList[0] + self.nameList[6],'loc')
            loc = pm.spaceLocator(n = locName)
            self.downLocList.append(loc)
            pos = pm.xform(downJj.getChildren(), q=1, ws=1, t=1)
            pm.xform(loc, ws=1, t=pos)
            loc.setParent(self.downLocGrp)
            
            pm.aimConstraint(loc, downJj, mo=1, weight=1, aimVector= (1,0,0), upVector = (0,1,0),
                            worldUpType='object', worldUpObject=self.aimLoc)            

    def __createHiCurve(self):
        
        tempUpPos = []
        tempDownPos = []
        
        #up
        #get pos        
        for loc in self.upLocList:
            pos = pm.xform(loc, q=1, ws=1, t=1)
            tempUpPos.append(pos)
#         print self.upLocList

        self.eyeUpHiCur = pm.curve(d = 1,p = [x for x in tempUpPos],
                                   k = [n for n in range(0,len(tempUpPos))],
                                   n = nameUtils.getUniqueName(self.lidSide,self.nameList[0] + self.nameList[5] + self.nameList[2],'cur'))
        pm.select(cl = 1)
        
        #down
        #get pos        
        for loc in self.downLocList:
            pos = pm.xform(loc, q=1, ws=1, t=1)
            tempDownPos.append(pos)
#         print self.downLocList
        
        self.eyeDnHiCur = pm.curve(d = 1,p = [x for x in tempDownPos],
                                   k = [n for n in range(0,len(tempDownPos))],
                                   n = nameUtils.getUniqueName(self.lidSide,self.nameList[0] + self.nameList[6] + self.nameList[2],'cur'))
        pm.select(cl = 1)
        
    def __locToCurve(self):
        
        for upLoc in self.upLocList:
            pos = pm.xform(upLoc, q=1, ws=1, t=1)
            print pos
            print upLoc
            print self.eyeUpHiCur.getShape()
            u = self.__getUParam(pos, self.eyeUpHiCur.getShape())
            #create point on curve node. Make sure Locators have suffix of _LOX
            name= upLoc.replace('_loc', '_PCI')
            pci= pm.createNode('pointOnCurveInfo', n=name)
            pm.connectAttr(self.eyeUpHiCur +'.worldSpace', pci+'.inputCurve')
            pm.setAttr(pci+'.parameter', u)
            pm.connectAttr(pci+'.position', upLoc +'.t')
        
    def __getUParam(self,pnt = [], crv = None):

        point = OpenMaya.MPoint(pnt[0],pnt[1],pnt[2])
        print pnt[0]
        curveFn = OpenMaya.MFnNurbsCurve(self.__getDagPath(crv))
        paramUtill=OpenMaya.MScriptUtil()
        paramPtr=paramUtill.asDoublePtr()
        isOnCurve = curveFn.isPointOnCurve(point)
        if isOnCurve == True:
            
            curveFn.getParamAtPoint(point , paramPtr,0.001,OpenMaya.MSpace.kObject )
        else :
            point = curveFn.closestPoint(point,paramPtr,0.001,OpenMaya.MSpace.kObject)
            curveFn.getParamAtPoint(point , paramPtr,0.001,OpenMaya.MSpace.kObject )
        
        param = paramUtill.getDouble(paramPtr)  
        return param

    def __getDagPath(self,objectName):
        
        if isinstance(objectName, list)==True:
            oNodeList=[]
            print objectName
            for o in objectName:
                selectionList = OpenMaya.MSelectionList()
                selectionList.add(o)
                oNode = OpenMaya.MDagPath()
                selectionList.getDagPath(0, oNode)
                oNodeList.append(oNode)
            return oNodeList
        else:
            selectionList = OpenMaya.MSelectionList()
            selectionList.add(objectName)
            oNode = OpenMaya.MDagPath()
            selectionList.getDagPath(0, oNode)
            return oNode    
        
def getUi(parent,mainUi):
    
    return HeadModuleUi(parent,mainUi)

class HeadModuleUi(object):

    def __init__(self,parent,mainUi):
        
        self.mainUi = mainUi
        self.__popuItems = []
        
        pm.setParent(parent)
        self.mainL = pm.columnLayout(adj = 1)
        pm.separator(h = 10)
        
        #main part
        self.name = pm.text(l = '**** Head Module ****')       
        self.baseNameT = pm.textFieldGrp(l = 'baseName : ',cl2 = ['left','left'],
                                         ad2 = 1,text = 'head')
        self.cntSizeF = pm.floatFieldGrp(l = 'ctrl Size : ',cl2 = ['left','left'],
                                         ad2 = 1,numberOfFields = 1,value1 = 1.5)
        self.metaSpineNodeN = pm.textFieldGrp(l = 'spineMeta :',cl2 = ['left','left'],
                                              ad2 = 1,text = 'spineMeta')   
        self.mainMetaNodeN = pm.textFieldGrp(l = 'mainMeta :',ad2 = 1,cl2 = ['left','left'],
                                             text = 'mainMeta')        
        pm.separator(h = 10)

        #lid part        
        self.lidTool = pm.text(l = '**** Lid Tool ****')
        self.eyeBallT = pm.textFieldGrp('eyeBall',l='eyeBall :',cl2 = ['left','left'],
                                         ad2 = 1,text = 'eyeBall')
        self.eyeBallR = pm.radioButtonGrp('lid_side',nrb = 2,label = 'eyeBall side :',
                                          cal = [1,'left'],la2 = ['left','right'],sl = 1)
#         self.eyeLidR = pm.radioButtonGrp('lid_pos',nrb = 2,label = 'eyeBall position :',
#                                           cal = [1,'left'],la2 = ['up','dowm'],sl = 1)
        pm.columnLayout(adjustableColumn = True)
        
        self.lidLoadB = pm.button(l = 'load Lid Class',c = self.getLidInstance)
        pm.columnLayout(adjustableColumn=True)
        
        self.vexUpSelB = pm.button(l = 'load Up Vertex',c = self.__loadUpVertex)
        pm.columnLayout(adjustableColumn=True)
        
        self.vexDnSelB = pm.button(l = 'load Dn Vertex',c = self.__loadDnVertex)
        pm.columnLayout(adjustableColumn=True)
        
        self.lidCreateB = pm.button(l = 'create Lid Setting',c = self.__createLid)
        pm.columnLayout(adjustableColumn=True)
        
        #erase button
        pm.separator(h = 10)
        self.name = pm.text(l = '**** Remove This Panel ****')       
        self.removeB = pm.button(l = 'remove',c = self.__removeInstance)
        self.__pointerClass = None
        
    def __removeInstance(self,*arg):
        
        pm.deleteUI(self.mainL)
        self.mainUi.modulesUi.remove(self)
        
    def getModuleInstance(self):
        
        baseNameT = pm.textFieldGrp(self.baseNameT,q = 1,text = 1)
        sizeF = pm.floatFieldGrp(self.cntSizeF,q = 1,v = 1)
        mainMetaNode = pm.textFieldGrp(self.mainMetaNodeN,q = 1,text = 1)
        spineMetaNode = pm.textFieldGrp(self.metaSpineNodeN,q = 1,text = 1)
        
        self.__pointerClass = HeadModule(baseName = baseNameT,size = sizeF,
                                         metaMain = mainMetaNode,metaSpine = spineMetaNode)
        return self.__pointerClass                     

    def getLidInstance(self,*arg):
        
        eyeBallR = pm.textFieldGrp('eyeBall',q = 1,text = 1)
        eyeLidR = pm.radioButtonGrp('lid_side',q = 1,sl = 1)
#         eyeLidP =  pm.radioButtonGrp('lid_pos',q = 1,sl = 1)
        self.lidClass = LidClass(eyeBall = eyeBallR,lidSide = eyeLidR)
#         self.lidClass = LidClass(eyeBall = eyeBallR,lidSide = eyeLidR,lidPos = eyeLidP)
        pm.selectPref(tso = 1)
        print 'LidClass ready to roll'
        return self.lidClass
    
    def __loadUpVertex(self,*arg):
        
        self.lidClass.loadUpVertex()
        print 'Up Vertex loaded'
        
    def __loadDnVertex(self,*arg):
        
        self.lidClass.loadDnVertex()
        print 'Down Vertex loaded'        
        pm.selectPref(tso = 0)
        
    def __createLid(self,*arg):
        
        self.lidClass.createLid()
        
        
# from Modules import legModule,footModule
# hg = headModule.HeadModule()
# hg.buildGuides()
# hg.build()
