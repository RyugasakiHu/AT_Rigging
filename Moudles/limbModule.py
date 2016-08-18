import pymel.core as pm
import math 
from Modules.subModules import fkChain,ikChain,boneChain,ribbon
from Utils import nameUtils,hookUtils,metaUtils
from Modules import control,toolModule
from maya import OpenMaya

class LimbModule(object):
    
    posLimbArray = [[2,14,-0.2],[4,14,-0.3],[6.15,14,-0.2]]
    rotLimbArray = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    posShoulderArray = [[0.2,13.95,-0.25],[1.45,14.25,-0.17]]
    rotShoulderArray = [[0,0,0],[0,0,0]]
    posShoulderBladeArray = [[0.65,14,-0.6],[0.65,12.5,-0.6]]
    rotShoulderBladeArray = [[0,0,0],[0,0,0]]
    posElbowSplitArray = [[3.75,14,-0.4],[4.25,14,-0.4]]
    rotElbowSplitArray = [[0,0,0],[0,0,0]]
    posElbowPartialArray = [[4,14,-1.5]]
    rotElbowPartialArray = [[0,0,0]]
    
    def __init__(self,baseName = 'arm',side = 'l',size = 1.5,
                 solver = 'ikRPsolver',controlOrient = [0,0,0],
                 metaSpine = None,metaMain = None,mirror = None,
                 shoulder = 0,elbow = 'no',twist = None,
                 upperTwistNum = None,lowerTwistNum = None,
                 metaMirror = None): 
        #init
        self.baseName = baseName
        self.side = side
        self.size = size
        self.solver = solver
        self.controlOrient = controlOrient
        self.mirror = mirror
        self.twist = twist
        self.upperTwistNum = upperTwistNum 
        self.lowerTwistNum = lowerTwistNum
        
        #jj
        self.fkChain = None
        self.ikChain = None
        self.limbBlendChain = None
        self.shoulderChain = None
        self.shoulderAtChain = None
        self.shoulderBladeChain = None
        self.blendData = None
        self.limbGrp = None
        self.chestGrp = None
        self.shoulderBladeGrp = None
        self.upperJointLentgh = None
        self.lowerJointLentgh = None
            
        #cc
        self.distance = None
        self.shoulderCtrl = None
        self.handSettingCtrl = None
        self.ccDefGrp = None
        self.cntsGrp = None
        self.shoulderBriGrp = None
        
        #guides 
        self.limbGuides = None        
        self.shoulderGuides = None
        self.shoulderBladeGuides = None
        self.elbowPartialGuides = None
        self.totalGuides = None
        self.guideGrp = None
        
        #non_flip
        self.upperArmTwistStart = None
        self.upperArmTwistEnd = None
        self.upperArmTwistChain = None
        self.upperArmTwistIk = None
        self.upperArmTwistIkEffector = None
        self.upperArmTwistIkCurve = None
        
        #ribbon
        self.ribon = None
        self.ribon45hp = None
        self.subMidCtrlShoulderElbow = None
        self.subMidCtrlElbowWrist = None
        self.subMidCtrlElbow = None
        self.ribbonData = ['ShoulderElbow','EblowWrist','Elbow']
        
        #nameList
        self.splitNameList = ['SplitUp','SplitDown']
        
        #AT
        self.ikAtHandle = None
        self.ikAtEffector  = None
        self.shoulderAtGrp = None
        self.poseReadorGrp = None
        
        #Hook
        self.shoulder = shoulder
        self.elbowMethod = elbow
        self.__tempSpaceSwitch = None
        self.locLocal = None
        self.locWorld = None
        self.hookData = {}

        #metanode
        self.meta = metaUtils.createMeta(self.side,self.baseName,0)
        self.metaMain = metaMain
        self.metaSpine = metaSpine
        self.metaMirror = metaMirror

    def buildGuides(self):
                
        self.shoulderGuides = []
        self.shoulderBladeGuides = []        
        self.limbGuides = []
        self.elbowPartialGuides = []
        self.elbowSplitGuides = []
        
        #limb Guides
        for num,pos in enumerate(self.posLimbArray):
            name = nameUtils.getUniqueName(self.side,self.baseName,'gud')
            loc = pm.spaceLocator(n = name)
            loc.t.set(pos)
            loc.r.set(self.rotLimbArray[num])
            loc.localScale.set(self.size,self.size,self.size)
            self.limbGuides.append(loc)
        
        #elbow partial
        if self.elbowMethod == 'split':
            #set pos loc
            for i,p in enumerate(self.posElbowSplitArray):
                name = nameUtils.getUniqueName(self.side,self.baseName + self.splitNameList[i],'gud')
                loc = pm.spaceLocator(n = name)
                loc.t.set(p)
                loc.r.set(self.rotElbowSplitArray[i])
                loc.localScale.set(self.size,self.size,self.size)
                self.elbowSplitGuides.append(loc)
            
        if self.elbowMethod == 'partial':    
            for num,pos in enumerate(self.posElbowPartialArray):
                name = nameUtils.getUniqueName(self.side,self.baseName + 'Partial','gud')
                loc = pm.spaceLocator(n = name)
                loc.t.set(pos)
                loc.r.set(self.rotElbowPartialArray[num])
                loc.localScale.set(self.size,self.size,self.size)
                self.elbowPartialGuides.append(loc)
                loc.setParent(self.limbGuides[0])                    
        
#         if self.elbowMethod == 'nope':
#             
#             pass
        
        #shoulder guides
        if self.shoulder == 'yes':            
            
            #shoulder Guides:        
            for num,pos in enumerate(self.posShoulderArray):
                name = nameUtils.getUniqueName(self.side,self.baseName + 'Shoulder','gud')
                loc = pm.spaceLocator(n = name)
                loc.t.set(pos)
                loc.r.set(self.rotShoulderArray[num])
                loc.localScale.set(self.size,self.size,self.size)
                self.shoulderGuides.append(loc)                
                    
            #shoulder Blade
            for num,pos in enumerate(self.posShoulderBladeArray):
                name = nameUtils.getUniqueName(self.side,self.baseName + 'ShoulderBlade','gud')
                loc = pm.spaceLocator(n = name)
                loc.t.set(pos)
                loc.r.set(self.rotShoulderBladeArray[num])
                loc.localScale.set(self.size,self.size,self.size)
                self.shoulderBladeGuides.append(loc)                 
        
        ###
        #mirror
        if self.mirror == 'yes':
            
            mirrorMetaNode = pm.ls(self.metaMirror)[0]            
            leftGuideLocMetaList = pm.connectionInfo(mirrorMetaNode.guideLocator, destinationFromSource=True)
            
            for guideLoc in leftGuideLocMetaList:
                destnation = guideLoc.split('_')
                 
                #arm
                if str(destnation[1]) + str(destnation[2]) == 'armElbowEBlockStart':
                    armLocStr = guideLoc.split('.')[0]
                    pm.select(armLocStr)
                    armLoc = pm.ls(sl = 1)[0] 
                    
                elif str(destnation[1]) == 'arm':
                    armElbowLocStr = guideLoc.split('.')[0]
                    pm.select(armElbowLocStr)
                    armElbowLoc = pm.ls(sl = 1)[0]  
                    
                elif str(destnation[1]) + str(destnation[2]) == 'elbowWristEBlockEnd':
                    elbowWristLocStr = guideLoc.split('.')[0]
                    pm.select(elbowWristLocStr)
                    elbowWristLoc = pm.ls(sl = 1)[0]
            
                #shoulder
                elif str(destnation[1]) + str(destnation[2]) == 'armShoulder0':
                    shoulderStartLocStr = guideLoc.split('.')[0]
                    pm.select(shoulderStartLocStr)
                    shoulderStartLoc = pm.ls(sl = 1)[0]
                    
                elif str(destnation[1]) + str(destnation[2]) == 'armShoulder1':
                    shoulderEndLocStr = guideLoc.split('.')[0]
                    pm.select(shoulderEndLocStr)
                    shoulderEndLoc = pm.ls(sl = 1)[0]    
                
                elif str(destnation[1]) + str(destnation[2]) == 'armShoulderBlade0':
                    shoulderBladeStartLocStr = guideLoc.split('.')[0]
                    pm.select(shoulderBladeStartLocStr)
                    shoulderBladeStartLoc = pm.ls(sl = 1)[0]
                
                elif str(destnation[1]) + str(destnation[2]) == 'armShoulderBlade1':
                    shoulderBladeEndLocStr = guideLoc.split('.')[0]
                    pm.select(shoulderBladeEndLocStr)
                    shoulderBladeEndLoc = pm.ls(sl = 1)[0]
                    
                #elbowSplit    
                elif str(destnation[1]) == 'armSplitUp':
                    elbowSplitUpLocStr = guideLoc.split('.')[0]
                    pm.select(elbowSplitUpLocStr)
                    elbowSplitUpLoc = pm.ls(sl = 1)[0]  
                    
                elif str(destnation[1]) == 'armSplitDown':
                    elbowSplitDownLocStr = guideLoc.split('.')[0]
                    pm.select(elbowSplitDownLocStr)
                    elbowSplitDownLoc = pm.ls(sl = 1)[0]  
                    
            #arm
            armLocPos = armLoc.getTranslation(space = 'world')
            armLocRot = armLoc.getRotation(space = 'world')
            self.limbGuides[0].t.set(-armLocPos[0],armLocPos[1],armLocPos[2])         
            self.limbGuides[0].r.set(armLocRot[0],-armLocRot[1],-armLocRot[2])   
            
            armElbowLocPos = armElbowLoc.getTranslation(space = 'world')
            armElbowLocRot = armElbowLoc.getRotation(space = 'world')
            self.limbGuides[1].t.set(-armElbowLocPos[0],armElbowLocPos[1],armElbowLocPos[2])         
            self.limbGuides[1].r.set(armElbowLocRot[0],-armElbowLocRot[1],-armElbowLocRot[2])
            
            elbowWristPos = elbowWristLoc.getTranslation(space = 'world')
            elbowWristRot = elbowWristLoc.getRotation(space = 'world')
            self.limbGuides[2].t.set(-elbowWristPos[0],elbowWristPos[1],elbowWristPos[2])
            self.limbGuides[2].r.set(elbowWristRot[0],-elbowWristRot[1],-elbowWristRot[2])
            
            #shoulder
            if self.shoulder == 'yes':
                shoulderStartLocPos = shoulderStartLoc.getTranslation(space = 'world')
                shoulderStartLocRot = shoulderStartLoc.getRotation(space = 'world')
                self.shoulderGuides[0].t.set(-shoulderStartLocPos[0],shoulderStartLocPos[1],shoulderStartLocPos[2])         
                self.shoulderGuides[0].r.set(shoulderStartLocRot[0],-shoulderStartLocRot[1],-shoulderStartLocRot[2])   
                
                shoulderEndPos = shoulderEndLoc.getTranslation(space = 'world')
                shoulderEndRot = shoulderEndLoc.getRotation(space = 'world')
                self.shoulderGuides[1].t.set(-shoulderEndPos[0],shoulderEndPos[1],shoulderEndPos[2])         
                self.shoulderGuides[1].r.set(shoulderEndRot[0],-shoulderEndRot[1],-shoulderEndRot[2])
                
                shoulderBladeStartPos = shoulderBladeStartLoc.getTranslation(space = 'world')
                shoulderBladeStartRot = shoulderBladeStartLoc.getRotation(space = 'world')
                self.shoulderBladeGuides[0].t.set(-shoulderBladeStartPos[0],shoulderBladeStartPos[1],shoulderBladeStartPos[2])
                self.shoulderBladeGuides[0].r.set(shoulderBladeStartRot[0],-shoulderBladeStartRot[1],-shoulderBladeStartRot[2])
                
                shoulderBladeEndPos = shoulderBladeEndLoc.getTranslation(space = 'world')
                shoulderBladeEndRot = shoulderBladeEndLoc.getRotation(space = 'world')
                self.shoulderBladeGuides[1].t.set(-shoulderBladeEndPos[0],shoulderBladeEndPos[1],shoulderBladeEndPos[2])
                self.shoulderBladeGuides[1].r.set(shoulderBladeEndRot[0],-shoulderBladeEndRot[1],-shoulderBladeEndRot[2])                
            
            #split
            if self.elbowMethod == 'split':
                elbowSplitUpLocPos = elbowSplitUpLoc.getTranslation(space = 'world')
                elbowSplitUpLocRot = elbowSplitUpLoc.getRotation(space = 'world')
                self.elbowSplitGuides[0].t.set(-elbowSplitUpLocPos[0],elbowSplitUpLocPos[1],elbowSplitUpLocPos[2])         
                self.elbowSplitGuides[0].r.set(elbowSplitUpLocRot[0],-elbowSplitUpLocRot[1],-elbowSplitUpLocRot[2])
                
                elbowSplitDownLocPos = elbowSplitDownLoc.getTranslation(space = 'world')
                elbowSplitDownLocRot = elbowSplitDownLoc.getRotation(space = 'world')
                self.elbowSplitGuides[1].t.set(-elbowSplitDownLocPos[0],elbowSplitDownLocPos[1],elbowSplitDownLocPos[2])         
                self.elbowSplitGuides[1].r.set(elbowSplitDownLocRot[0],-elbowSplitDownLocRot[1],-elbowSplitDownLocRot[2])
                        
        #regroup
        #arm loc
        tempLimbGuides = list(self.limbGuides)
        tempLimbGuides.reverse()
        for i in range(len(tempLimbGuides)):
            if i != (len(tempLimbGuides) - 1):
                pm.parent(tempLimbGuides[i],tempLimbGuides[i + 1])    
        
        #shoulder loc
        if self.shoulder == 'yes':    
            tempShoulderGuides = list(self.shoulderGuides)
            tempShoulderGuides.reverse()
            for i in range(len(tempShoulderGuides)):
                if i != (len(tempShoulderGuides) - 1):
                    pm.parent(tempShoulderGuides[i],tempShoulderGuides[i + 1])      
                 
            tempShoulderBladeGuides = list(self.shoulderBladeGuides)
            tempShoulderBladeGuides.reverse()
            for i in range(len(tempShoulderBladeGuides)):
                if i != (len(tempShoulderBladeGuides) - 1):
                    pm.parent(tempShoulderBladeGuides[i],tempShoulderBladeGuides[i + 1])
        
        #split loc        
        if self.elbowMethod == 'split':
            #set loc grp
            pm.parent(self.elbowSplitGuides[1],self.elbowSplitGuides[0])
            self.elbowSplitGuides.reverse()
            
            self.elbowSplitGuides[1].setParent(self.limbGuides[1])
            self.elbowSplitGuides.reverse()
                    
        #clean up
        name = nameUtils.getUniqueName(self.side,self.baseName + '_Gud','grp')
        self.guideGrp = pm.group(em = 1,n = name)        
        self.limbGuides[0].setParent(self.guideGrp)
        
        if self.shoulder == 'yes':
            
            self.shoulderGuides[0].setParent(self.guideGrp)
            self.shoulderBladeGuides[0].setParent(self.guideGrp)      
                     
        if self.mirror == 'no':
            
            for limbGuide in self.limbGuides:
                oriTx = limbGuide.tx.get()
                oriTy = limbGuide.ty.get()
                oriTz = limbGuide.tz.get()
                limbGuide.t.set(self.size * oriTx,self.size * oriTy,self.size * oriTz)
                
            for shoulderGuide in self.shoulderGuides:     
                oriTx = shoulderGuide.tx.get()
                oriTy = shoulderGuide.ty.get()
                oriTz = shoulderGuide.tz.get()
                shoulderGuide.t.set(self.size * oriTx,self.size * oriTy,self.size * oriTz)
                
            for shoulderBladeGuide in self.shoulderBladeGuides:
                oriTx = shoulderBladeGuide.tx.get()
                oriTy = shoulderBladeGuide.ty.get()
                oriTz = shoulderBladeGuide.tz.get()
                shoulderBladeGuide.t.set(self.size * oriTx,self.size * oriTy,self.size * oriTz)  
                
            for elbowSplitGuide in self.elbowSplitGuides: 
                oriTx = elbowSplitGuide.tx.get()
                oriTy = elbowSplitGuide.ty.get()
                oriTz = elbowSplitGuide.tz.get()
                elbowSplitGuide.t.set(self.size * oriTx,self.size * oriTy,self.size * oriTz)
                    
    def build(self):
        
        #mirror
        self.mirrorGuideGrp = pm.group(em = 1,n = nameUtils.getUniqueName(self.side,self.baseName + '_Gud','grp'))
        self.mirrorGuideList = []
        self.mirrorGuideGrp.v.set(0)
        
        for limbGuide in self.limbGuides:
            mirrorLimbGuide = pm.duplicate(limbGuide)
            child = pm.listRelatives(mirrorLimbGuide,c = 1,typ = 'transform')
            if child != None:
                pm.delete(child)
            newName = str(limbGuide) + 'Mirror' 
            renameGuide = pm.rename(mirrorLimbGuide,newName)
            mirrorLimbGuide[0].setParent(self.mirrorGuideGrp)
            self.mirrorGuideList.append(renameGuide)
        
        for shoulderGuide in self.shoulderGuides:
            mirrorShoulderGuide = pm.duplicate(shoulderGuide)
            child = pm.listRelatives(mirrorShoulderGuide,c = 1,typ = 'transform')
            if child != None:
                pm.delete(child)
            newName = str(shoulderGuide) + 'Mirror' 
            renameGuide = pm.rename(mirrorShoulderGuide,newName)
            mirrorShoulderGuide[0].setParent(self.mirrorGuideGrp)
            self.mirrorGuideList.append(renameGuide)
        
        for shoulderBladeGuide in self.shoulderBladeGuides:
            mirrorShoulderBladeGuide = pm.duplicate(shoulderBladeGuide)
            child = pm.listRelatives(mirrorShoulderBladeGuide,c = 1,typ = 'transform')
            if child != None:
                pm.delete(child)
            newName = str(shoulderBladeGuide) + 'Mirror' 
            renameGuide = pm.rename(mirrorShoulderBladeGuide,newName)
            mirrorShoulderBladeGuide[0].setParent(self.mirrorGuideGrp)
            self.mirrorGuideList.append(renameGuide)
        
        for elbowSplitGuide in self.elbowSplitGuides: 
            mirrorElbowSplitGuide = pm.duplicate(elbowSplitGuide)
            child = pm.listRelatives(mirrorElbowSplitGuide,c = 1,typ = 'transform')
            if child != None:
                pm.delete(child)
            newName = str(elbowSplitGuide) + 'Mirror' 
            renameGuide = pm.rename(mirrorElbowSplitGuide,newName)
            mirrorElbowSplitGuide[0].setParent(self.mirrorGuideGrp)
            self.mirrorGuideList.append(renameGuide)

        #really to roll
        self.guideGrp.v.set(0)        
        
        if self.shoulder == 'yes':
            #shoulder set
            #shoulder pos get
            self.shoulderGuidePos = [x.getTranslation(space = 'world') for x in self.shoulderGuides]
            self.shoulderGuideRot = [x.getRotation(space = 'world') for x in self.shoulderGuides]
        
            #shoulder jj set
            self.shoulderChain = boneChain.BoneChain(self.baseName + 'Shoulder',self.side,type = 'jj')
            self.shoulderChain.fromList(self.shoulderGuidePos,self.shoulderGuideRot)
            pm.rename(self.shoulderChain.chain[-1],nameUtils.getUniqueName(self.side,self.baseName + 'Shoulder','je'))
            
            ###########################
            #shoulder Blade set
            #shoulder Blade pos get
            self.shoulderBladeGuidePos = [x.getTranslation(space = 'world') for x in self.shoulderBladeGuides]
            self.shoulderBladeGuideRot = [x.getRotation(space = 'world') for x in self.shoulderBladeGuides]
            
            #shoulder jj set
            self.shoulderBladeChain = boneChain.BoneChain(self.baseName + 'ShoulderBlade',self.side,type = 'jj')
            self.shoulderBladeChain.fromList(self.shoulderBladeGuidePos,self.shoulderBladeGuideRot)
            pm.rename(self.shoulderBladeChain.chain[-1],nameUtils.getUniqueName(self.side,self.baseName + 'ShoulderBlade','je'))
                
        ###########################        
        #limb set
        #limb pos get
        self.limbGuidePos = [x.getTranslation(space = 'world') for x in self.limbGuides]
        self.limbGuideRot = [x.getRotation(space = 'world') for x in self.limbGuides]      
        
        #addBlendCtrl 
        self.handSettingCtrl = control.Control(self.side,self.baseName + 'Settings',self.size) 
        self.handSettingCtrl.ikfkBlender() 
        
        #fk first 
        self.fkChain = fkChain.FkChain(self.baseName,self.side,self.size)
        self.fkChain.fromList(self.limbGuidePos,self.limbGuideRot,skipLast = 0)
        
        for chain in self.fkChain.chain:
            pm.setAttr(chain + ".visibility",k = False,cb=False)
            pm.setAttr(chain + ".radi",k = False,cb=False,l=False)
            pm.setAttr(chain + '.rotateOrder',cb = True)
        
        #then ik
        self.ikChain = ikChain.IkChain(self.baseName,self.side,self.size,self.solver)
        self.ikChain.fromList(self.limbGuidePos,self.limbGuideRot)
        
        #ik cc connect ori
        self.ikChain.ikCtrl.control.rx.connect(self.ikChain.chain[-1].rx)
        self.ikChain.ikCtrl.control.ry.connect(self.ikChain.chain[-1].ry)
        self.ikChain.ikCtrl.control.rz.connect(self.ikChain.chain[-1].rz)
        
        #set cc
        pm.addAttr(self.handSettingCtrl.control,ln = '__',at = 'enum',en = 'ArmCtrl:')
        pm.setAttr(self.handSettingCtrl.control + '.__',k = 1,l = 1)
        
        #ori                
        self.limbBlendChain = boneChain.BoneChain(self.baseName,self.side,type = 'jc')
        self.limbBlendChain.fromList(self.limbGuidePos,self.limbGuideRot)
        
        self.blendData = boneChain.BoneChain.blendTwoChains(self.fkChain.chain,self.ikChain.chain,self.limbBlendChain.chain,
                                                            self.handSettingCtrl.control,'IKFK',self.baseName,self.side)
        
        #elbow method
        if self.elbowMethod == 'partial':
            
            #pos get
            self.elbowPartialGuidePos = [x.getTranslation(space = 'world') for x in self.elbowPartialGuides]
            self.elbowPartialGuideRot = [x.getRotation(space = 'world') for x in self.elbowPartialGuides]
            
            #set joint    
            self.elbowPartialJoint = pm.joint(n = nameUtils.getUniqueName(self.side,self.baseName + 'elbowPartial','jj'),                                   
                                              position = self.elbowPartialGuidePos[0],orientation = self.elbowPartialGuideRot[0]) 
#             boneChain.BoneChain(self.baseName + 'elbowPartial',self.side,type = 'jj')
#             self.elbowPartialJoint.fromList(self.elbowPartialGuidePos,self.elbowPartialGuideRot)
            self.elbowPartialJoint.setParent(self.limbBlendChain.chain[0])
            pm.makeIdentity(self.elbowPartialJoint,apply = True,t=0,r=1,s=0,n=0,pn=1)
            self.elbowPartialJoint.jointOrientX.set(0)
            self.elbowPartialJoint.jointOrientY.set(0)
            self.elbowPartialJoint.jointOrientZ.set(0)

            #cnst
            pm.orientConstraint(self.limbBlendChain.chain[1],self.elbowPartialJoint,mo = 1)
            
        if self.elbowMethod == 'split':
            #all pos
            #split pos
            self.elbowSplitGuidePos = []
            self.elbowSplitGuidePos.append(self.limbGuidePos[1])
            for elbowSplitGuide in self.elbowSplitGuides:
                elbowSplitGuidePos = elbowSplitGuide.getTranslation(space = 'world')
                self.elbowSplitGuidePos.append(elbowSplitGuidePos)                
            
            #split rot
            self.elbowSplitGuideRot = []
            self.elbowSplitGuideRot.append(self.limbGuideRot[1])
            for elbowSplitGuide in self.elbowSplitGuides:
                elbowSplitGuideRot = elbowSplitGuide.getRotation(space = 'world')
                self.elbowSplitGuideRot.append(elbowSplitGuideRot)  
           
            #part pos
            #up chain pos
            self.elbowSplitUpPos = []
            self.elbowSplitUpPos.append(self.limbGuidePos[0])
            self.elbowSplitUpPos.append(self.elbowSplitGuidePos[1])

            self.elbowSplitUpRot = []
            self.elbowSplitUpRot.append(self.limbGuideRot[0])
            self.elbowSplitUpRot.append(self.elbowSplitGuideRot[1])
            
            #down chain pos
            self.elbowSplitDownPos = []
            self.elbowSplitDownPos.append(self.elbowSplitGuidePos[2])
            self.elbowSplitDownPos.append(self.limbGuidePos[2])
            
            self.elbowSplitDownRot = []
            self.elbowSplitDownRot.append(self.elbowSplitGuideRot[2])
            self.elbowSplitDownRot.append(self.limbGuideRot[2])   
            
            #create chain
            self.elbowSplitChain = boneChain.BoneChain('elbowSplit',self.side,type = 'jc')
            self.elbowSplitChain.fromList(self.elbowSplitGuidePos,self.elbowSplitGuideRot)
              
            self.elbowSplitUpChain = boneChain.BoneChain('elbow' + self.splitNameList[0],self.side,type = 'jc')
            self.elbowSplitUpChain.fromList(self.elbowSplitUpPos,self.elbowSplitUpRot)
              
            self.elbowSplitDownChain = boneChain.BoneChain('elbow' + self.splitNameList[1],self.side,type = 'jc')
            self.elbowSplitDownChain.fromList(self.elbowSplitDownPos,self.elbowSplitDownRot)
              
            self.__splitJointSet()
            
        self.__ikfkBlender()
        
        if self.twist == 'ribon45hp': 
            self.__ribonSetUp()
         
        if self.twist == 'non_roll':
            self.__nonRollSetUp() 
        
        if self.shoulder == 'yes':
            if self.solver == 'ikRPsolver': 
                self.__shoulderCtrl() 
            else:
                OpenMaya.MGlobal.displayError('this version shoulder need come up with ikRP for follow')
        
        self.__cleanUp()
        self.__buildHooks()
        
    def __ikfkBlender(self):
        
        #connect visable function 
        reverseNodeName = nameUtils.getUniqueName(self.side,self.baseName + 'IKFK','REV')
        reverseNode = pm.createNode('reverse',n = reverseNodeName)
        
        #connect node
        self.handSettingCtrl.control.IKFK.connect(self.ikChain.ikCtrl.controlGrp.v)
        if self.solver == 'ikRPsolver' :
            self.handSettingCtrl.control.IKFK.connect(self.ikChain.poleVectorCtrl.controlGrp.v)
        self.handSettingCtrl.control.IKFK.connect(self.handSettingCtrl.textObj[1].v)
        self.handSettingCtrl.control.IKFK.connect(reverseNode.inputX)
        reverseNode.outputX.connect(self.fkChain.chain[0].v)
        reverseNode.outputX.connect(self.handSettingCtrl.textObj[0].v)             
        
        #set pos
#         scaleValue = 1 * self.ikChain.length/16
#         size = 1.5 * self.ikChain.length / 16
        pm.xform(self.handSettingCtrl.controlGrp,ws = 1,matrix = self.limbBlendChain.chain[2].worldMatrix.get())
        self.handSettingCtrl.controlGrp.rx.set(0)
        self.handSettingCtrl.controlGrp.ry.set(0)
        self.handSettingCtrl.controlGrp.rz.set(0)
        self.handSettingCtrl.controlGrp.sx.set(self.size / 2)
        self.handSettingCtrl.controlGrp.sy.set(self.size / 2)
        self.handSettingCtrl.controlGrp.sz.set(self.size / 2)
        pm.move(self.limbGuidePos[2][0],self.limbGuidePos[2][1] + 2 * self.size,
                self.limbGuidePos[2][2],self.handSettingCtrl.controlGrp)
        wrist_pos = pm.xform(self.limbBlendChain.chain[2],query=1,ws=1,rp=1)
        pm.move(wrist_pos[0],wrist_pos[1],wrist_pos[2],self.handSettingCtrl.controlGrp + '.rotatePivot')
        pm.move(wrist_pos[0],wrist_pos[1],wrist_pos[2],self.handSettingCtrl.controlGrp + '.scalePivot')
        pm.pointConstraint(self.limbBlendChain.chain[2],self.handSettingCtrl.controlGrp,mo = 1)
#         pm.orientConstraint(self.limbBlendChain.chain[2],self.handSettingCtrl.controlGrp,mo = 1)   
        control.lockAndHideAttr(self.handSettingCtrl.control,['tx','ty','tz','rx','ry','rz','sx','sy','sz','v'])
        self.handSettingCtrl.control.IKFK.set(0)
        
        if self.twist == 'non_roll':
            control.addFloatAttr(self.handSettingCtrl.control,['proxy_vis'],0,1) 
    
    def __splitJointSet(self):
        
        self.elbowSplitChain.chain[0].setParent(self.limbBlendChain.chain[0])
        
        #create node
        #pos
        splitPosMDNodeName = nameUtils.getUniqueName(self.side,'elbowSplitPos','MDN')
        splitPosMDNode = pm.createNode('multiplyDivide',n = splitPosMDNodeName)
           
        #connect
        self.limbBlendChain.chain[1].tx.connect(splitPosMDNode.input1X)
        self.limbBlendChain.chain[1].ty.connect(splitPosMDNode.input1Y)
        self.limbBlendChain.chain[1].tz.connect(splitPosMDNode.input1Z)
           
        splitPosMDNode.outputX.connect(self.elbowSplitChain.chain[0].tx)
        splitPosMDNode.outputY.connect(self.elbowSplitChain.chain[0].ty)
        splitPosMDNode.outputZ.connect(self.elbowSplitChain.chain[0].tz)        
                 
        #rot
        splitRotMDNodeName = nameUtils.getUniqueName(self.side,'elbowSplitRot','MDN')
        splitRotMDNode = pm.createNode('multiplyDivide',n = splitRotMDNodeName)
          
        #connect
        self.limbBlendChain.chain[1].rx.connect(splitRotMDNode.input1X)
        self.limbBlendChain.chain[1].ry.connect(splitRotMDNode.input1Y)
        self.limbBlendChain.chain[1].rz.connect(splitRotMDNode.input1Z)
         
        splitRotMDNode.input2X.set(-0.5)
        splitRotMDNode.input2Y.set(1)
        splitRotMDNode.input2Z.set(-0.5)
          
        splitRotMDNode.outputX.connect(self.elbowSplitChain.chain[0].rx)
        splitRotMDNode.outputY.connect(self.elbowSplitChain.chain[0].ry)
        splitRotMDNode.outputZ.connect(self.elbowSplitChain.chain[0].rz)
         
        #ik handle
        upIkName = nameUtils.getUniqueName(self.side,'elbowSplitUp','iks')
        self.upSplitIkHandle,self.upSplitIkEffector = pm.ikHandle(sj = self.elbowSplitUpChain.chain[0],ee = self.elbowSplitUpChain.chain[1],solver = 'ikSCsolver',n = upIkName)
         
        downIkName = nameUtils.getUniqueName(self.side,'elbowSplitDown','iks')
        self.downSplitIkHandle,self.downSplitIkEffector = pm.ikHandle(sj = self.elbowSplitDownChain.chain[0],ee = self.elbowSplitDownChain.chain[1],solver = 'ikSCsolver',n = downIkName)
         
        #cleanUp
        #ik
        self.upSplitIkHandle.setParent(self.elbowSplitChain.chain[1])
        self.downSplitIkHandle.setParent(self.limbBlendChain.chain[2])
        self.upSplitIkHandle.v.set(0)
        self.downSplitIkHandle.v.set(0)
         
        #joint
        self.elbowSplitUpChain.chain[0].setParent(self.limbBlendChain.chain[0])
        self.elbowSplitDownChain.chain[0].setParent(self.elbowSplitChain.chain[2])     
     
    def __nonRollSetUp(self):
        
        if self.elbowMethod == 'nope':
            #upper arm:
            #create twist arm 
            self.upperArmTwistStart = pm.duplicate(self.limbBlendChain.chain[0],
                                                   n = nameUtils.getUniqueName(self.side,'upperArmTwistS','jj')) 
            self.upperArmTwistEnd = pm.listRelatives(self.upperArmTwistStart,c = 1,typ = 'joint')
            
            tempJoint = pm.listRelatives(self.upperArmTwistEnd,c = 1,typ = 'joint')
            pm.delete(tempJoint)
            pm.rename(self.upperArmTwistEnd,nameUtils.getUniqueName(self.side,'upperArmTwistE','jj'))
             
            self.upperArmTwistJoint = toolModule.SplitJoint(self.upperArmTwistStart,self.upperTwistNum,box = 1,type = 'tool',size = self.size) 
            self.upperArmTwistJoint.splitJointTool()
             
            for cube in self.upperArmTwistJoint.cubeList:
                    self.handSettingCtrl.control.proxy_vis.connect(cube[0].v) 
             
            for twistJoints in self.upperArmTwistJoint.joints:
                pm.rename(twistJoints, nameUtils.getUniqueName(self.side,'upperArmTwist','jj'))  
                 
            #create iks      
            upperArmTwistIkName = nameUtils.getUniqueName(self.side,'upperArmTwist','iks')  
            upperArmTwistIkCurveName = nameUtils.getUniqueName(self.side,'upperArmTwist','ikc')  
            self.upperArmTwistIk,self.upperArmTwistIkEffector,self.upperArmTwistIkCurve = pm.ikHandle(sj = self.upperArmTwistStart[0],
                                                                                                      ee = self.upperArmTwistEnd[0],
                                                                                                      solver = 'ikSplineSolver',
                                                                                                      n = upperArmTwistIkName)
            upperArmSpIkSkinCluster = pm.skinCluster(self.limbBlendChain.chain[0],self.limbBlendChain.chain[1],self.upperArmTwistIkCurve,
                                        n = nameUtils.getSkinName())
            pm.rename(self.upperArmTwistIkCurve,upperArmTwistIkCurveName)
            self.upperArmTwistIk.poleVector.set(0,0,0)
            self.upperArmTwistIk.v.set(0)
            
            #set stretch
            #get last cv:
            pm.select(self.upperArmTwistIkCurve + '.cv[*]')
            upperIkCLastCv = pm.ls(sl = 1)[0][-1]
            pm.skinPercent(upperArmSpIkSkinCluster,upperIkCLastCv,tv = [(self.limbBlendChain.chain[1],1)])
            
            #get cv length
            upperArmTwistIkCurveInfoName = nameUtils.getUniqueName(self.side,'upperArmTwist','cvINFO')
            upperArmTwistIkCurveInfoNode = pm.createNode('curveInfo',n = upperArmTwistIkCurveInfoName)
            self.upperArmTwistIkCurve.getShape().worldSpace[0].connect(upperArmTwistIkCurveInfoNode.inputCurve)
            
            #create main Node
            upperArmTwistCurveMDNName = nameUtils.getUniqueName(self.side,'upperArmTwistCur','MDN')
            upperArmTwistCurveMDNNode = pm.createNode('multiplyDivide',n = upperArmTwistCurveMDNName)
            
            upperArmTwistIkCurveInfoNode.arcLength.connect(upperArmTwistCurveMDNNode.input1.input1X)
            upperArmTwistCurveMDNNode.input2.input2X.set(self.limbBlendChain.chain[1].tx.get())
            upperArmTwistCurveMDNNode.operation.set(2)
            
            for num,twistJoints in enumerate(self.upperArmTwistJoint.joints):
                tempNodeName = nameUtils.getUniqueName(self.side,'upperArmTwistJnt','MDN')
                tempNode = pm.createNode('multiplyDivide',n = tempNodeName)
                if num > 0 :
                    tempNode.input1.input1X.set(twistJoints.tx.get())
                    upperArmTwistCurveMDNNode.outputX.connect(tempNode.input2.input2X)
                    tempNode.outputX.connect(twistJoints.tx)
            
            #create upperTwistGrp
            upperArmTwistGrpName = nameUtils.getUniqueName(self.side,'upperArmTwist','grp')
            self.upperArmTwistGrp = pm.group(em = 1,n = upperArmTwistGrpName) 
            self.upperArmTwistIk.setParent(self.upperArmTwistGrp) 
            self.upperArmTwistIkCurve.setParent(self.upperArmTwistGrp) 
            
            #create upperTwistInfoGrp 
            twistInfoGrpName = nameUtils.getUniqueName(self.side,'upperArmTwistInfo','grp')
            self.upperArmTwistInfoGrp = pm.group(em = 1,n = twistInfoGrpName)
            
            #nonFlip Jnt
            nonFlipStJnt = pm.duplicate(self.limbBlendChain.chain[1],
                                        n = nameUtils.getUniqueName(self.side,'upperArmNonFlip','jc'))
            nonFlipEdJnt = pm.listRelatives(nonFlipStJnt,c = 1,typ = 'joint')
            pm.rename(nonFlipEdJnt,nameUtils.getUniqueName(self.side,self.baseName + 'upperArmNonFlip','je'))
            nonFlipStJnt[0].setParent(self.upperArmTwistInfoGrp)
            nonFlipIks,nonFlipIksEffector = pm.ikHandle(sj = nonFlipStJnt[0],ee = nonFlipEdJnt[0],solver = 'ikRPsolver',
                                                        n = nameUtils.getUniqueName(self.side,'upperArmNonFlip','iks'))
            nonFlipIks.setParent(self.limbBlendChain.chain[1])
            nonFlipIks.poleVector.set(0,0,0)
            nonFlipIks.r.set(0,0,0)
            nonFlipIks.v.set(0)
            pm.pointConstraint(self.limbBlendChain.chain[1],nonFlipStJnt,mo = 1)
            
            #twist info jnt
            twistInfoJnt = pm.joint(n = nameUtils.getUniqueName(self.side,'upperArmTwistInfo','jc'))
            twistInfoJnt.setParent(nonFlipStJnt)
            twistInfoJnt.t.set(0,0,0)
            pm.aimConstraint(nonFlipEdJnt[0],twistInfoJnt,mo = 1,w = 1,aimVector = [1,0,0],upVector = [0,0,1],
                             worldUpType = 'objectrotation',worldUpVector = [0,0,1],
                             worldUpObject = self.limbBlendChain.chain[1])
    #         twistInfoJnt.rx.connect(self.upperArmTwistIk.twist)
    #         pm.parentConstraint(self.shoulderChain.chain[0],twistInfoGrpName,mo = 1)
            
            ###
            #fore arm
            self.foreArmTwistStart = pm.duplicate(self.limbBlendChain.chain[1],
                                                  n = nameUtils.getUniqueName(self.side,'foreArmTwistS','jj'))
            self.foreArmTwistEnd = pm.listRelatives(self.foreArmTwistStart,c = 1,typ = 'joint')
            pm.parent(self.foreArmTwistStart,w = 1)
            
            tempTrashNode = pm.listRelatives(self.foreArmTwistStart,c = 1,typ = 'ikHandle')
            pm.delete(tempTrashNode)
            
            self.foreArmTwistJoint = toolModule.SplitJoint(self.foreArmTwistStart,self.lowerTwistNum,box = 1,type = 'tool',size = self.size) 
            self.foreArmTwistJoint.splitJointTool()
            
            for cube in self.foreArmTwistJoint.cubeList:
                    self.handSettingCtrl.control.proxy_vis.connect(cube[0].v) 
             
            for twistJoints in self.foreArmTwistJoint.joints:
                pm.rename(twistJoints, nameUtils.getUniqueName(self.side,'foreArmTwist','jj'))  
                 
            #create iks      
            foreArmTwistIkName = nameUtils.getUniqueName(self.side,'foreArmTwist','iks')  
            foreArmTwistIkCurveName = nameUtils.getUniqueName(self.side,'foreArmTwist','ikc')  
            self.foreArmTwistIk,self.foreArmTwistIkEffector,self.foreArmTwistIkCurve = pm.ikHandle(sj = self.foreArmTwistStart[0],
                                                                                                   ee = self.foreArmTwistEnd[0],
                                                                                                   solver = 'ikSplineSolver',
                                                                                                   n = foreArmTwistIkName)
            foreSpIkC = pm.skinCluster(self.limbBlendChain.chain[1],self.limbBlendChain.chain[2],self.foreArmTwistIkCurve,n = nameUtils.getSkinName())
            pm.rename(self.foreArmTwistIkCurve,foreArmTwistIkCurveName)
            self.foreArmTwistIk.poleVector.set(0,0,0)
            self.foreArmTwistIk.v.set(0)
            
            #set stretch
            #get First cv:
            pm.select(self.foreArmTwistIkCurve + '.cv[*]')
            foreIkCFristCv = pm.ls(sl = 1)[0][0]
            pm.skinPercent(foreSpIkC,foreIkCFristCv,tv = [(self.limbBlendChain.chain[1],1)])
            
            #get last cv:
            pm.select(self.foreArmTwistIkCurve + '.cv[*]')
            foreIkCLastCv = pm.ls(sl = 1)[0][-1]
            pm.skinPercent(foreSpIkC,foreIkCLastCv,tv = [(self.limbBlendChain.chain[2],1)])
            
            #get cv length
            foreArmTwistIkCurveInfoName = nameUtils.getUniqueName(self.side,'foreArmTwist','cvINFO')
            foreArmTwistIkCurveInfoNode = pm.createNode('curveInfo',n = foreArmTwistIkCurveInfoName)
            self.foreArmTwistIkCurve.getShape().worldSpace[0].connect(foreArmTwistIkCurveInfoNode.inputCurve)
            
            #create main Node
            foreArmTwistCurveMDNName = nameUtils.getUniqueName(self.side,'foreArmTwistCur','MDN')
            foreArmTwistCurveMDNNode = pm.createNode('multiplyDivide',n = foreArmTwistCurveMDNName)
            
            foreArmTwistIkCurveInfoNode.arcLength.connect(foreArmTwistCurveMDNNode.input1.input1X)
            foreArmTwistCurveMDNNode.input2.input2X.set(self.limbBlendChain.chain[2].tx.get())
            foreArmTwistCurveMDNNode.operation.set(2)
            
            for num,twistJoints in enumerate(self.foreArmTwistJoint.joints):
                tempNodeName = nameUtils.getUniqueName(self.side,'foreArmTwistJnt','MDN')
                tempNode = pm.createNode('multiplyDivide',n = tempNodeName)
                if num > 0 :
                    tempNode.input1.input1X.set(twistJoints.tx.get())
                    foreArmTwistCurveMDNNode.outputX.connect(tempNode.input2.input2X)
                    tempNode.outputX.connect(twistJoints.tx)
            
            #create foreTwistGrp
            foreArmTwistGrpName = nameUtils.getUniqueName(self.side,'foreArmTwist','grp')
            self.foreArmTwistGrp = pm.group(em = 1,n = foreArmTwistGrpName) 
            self.foreArmTwistIk.setParent(self.foreArmTwistGrp) 
            self.foreArmTwistIkCurve.setParent(self.foreArmTwistGrp) 
            
            #lowerTwist
            foreArmTwistLocStr = pm.spaceLocator(n = nameUtils.getUniqueName(self.side,'foreArmTwistStart','loc'))
            foreArmTwistLocEd = pm.spaceLocator(n = nameUtils.getUniqueName(self.side,'foreArmTwistEnd','loc'))
            
            foreArmTwistLocStr.setParent(self.limbBlendChain.chain[1])
            foreArmTwistLocEd.setParent(self.limbBlendChain.chain[2])
            foreArmTwistLocStr.t.set(0,0,0)
            foreArmTwistLocStr.r.set(0,0,0)
            foreArmTwistLocEd.t.set(0,0,0)
            foreArmTwistLocEd.r.set(0,0,0)
            foreArmTwistLocStr.v.set(0)
            foreArmTwistLocEd.v.set(0)
            
            self.foreArmTwistIk.dTwistControlEnable.set(1)
            self.foreArmTwistIk.dWorldUpType.set(4)
            self.foreArmTwistIk.dWorldUpAxis.set(3)
            self.foreArmTwistIk.dWorldUpVector.set(0,0,1)
            self.foreArmTwistIk.dWorldUpVectorEnd.set(0,0,1)
            foreArmTwistLocStr.worldMatrix.connect(self.foreArmTwistIk.dWorldUpMatrix)
            foreArmTwistLocEd.worldMatrix.connect(self.foreArmTwistIk.dWorldUpMatrixEnd)
            
            ###
            #clean up
            self.upperArmTwistIkCurve.v.set(0)
            self.foreArmTwistIkCurve.v.set(0)
            
            #upperarm
            #roll custom attr
    #         control.addFloatAttr(self.handSettingCtrl.control,['upperArm_roll'],-180,180)
    #         
    #         #node perpare
    #         upperArmRollFixPMANodeName = nameUtils.getUniqueName(self.side,'upperArmRollFix','PMA')
    #         upperArmRollFixPMANode = pm.createNode('plusMinusAverage',n = upperArmRollFixPMANodeName)
    #         
    #         #connect
    #         twistInfoJnt.rx.connect(upperArmRollFixPMANode.input1D[0])
    #         self.handSettingCtrl.control.upperArm_roll.connect(upperArmRollFixPMANode.input1D[1])
    #         upperArmRollFixPMANode.output1D.connect(self.upperArmTwistIk.roll)              
            
        elif self.elbowMethod == 'split':
            
            #upperArm:
            #non roll up            
            #create twist Leg
            self.upperArmTwistStart = pm.duplicate(self.elbowSplitUpChain.chain[0],
                                                n = nameUtils.getUniqueName(self.side,'upperArmTwistS','jj'))
            tempElbowTrashEffNode = pm.listRelatives(self.upperArmTwistStart,c = 1,typ = 'ikEffector')
            pm.delete(tempElbowTrashEffNode)
            self.upperArmTwistEnd = pm.listRelatives(self.upperArmTwistStart,c = 1,typ = 'joint')
            
            tempJoint = pm.listRelatives(self.upperArmTwistEnd,c = 1,typ = 'joint')
            pm.delete(tempJoint)
            pm.rename(self.upperArmTwistEnd,nameUtils.getUniqueName(self.side,'upperArmTwistE','jj'))
             
            self.upperArmTwistJoint = toolModule.SplitJoint(self.upperArmTwistStart,self.upperTwistNum,box = 1,type = 'tool',size = self.size) 
            self.upperArmTwistJoint.splitJointTool()
            
            for cube in self.upperArmTwistJoint.cubeList:
                self.handSettingCtrl.control.proxy_vis.connect(cube[0].v)
             
            for twistJoints in self.upperArmTwistJoint.joints:
                pm.rename(twistJoints, nameUtils.getUniqueName(self.side,'upperArmTwist','jj'))
        
            #create iks
            upperArmTwistIkName = nameUtils.getUniqueName(self.side,'upperArmTwist','iks')  
            upperArmTwistIkCurveName = nameUtils.getUniqueName(self.side,'upperArmTwist','ikc')  
            self.upperArmTwistIk,self.upperArmTwistIkEffector,self.upperArmTwistIkCurve = pm.ikHandle(sj = self.upperArmTwistStart[0],
                                                                                             ee = self.upperArmTwistEnd[0],
                                                                                             solver = 'ikSplineSolver',
                                                                                             n = upperArmTwistIkName)
            self.upperArmTwistIk.setParent(self.elbowSplitUpChain.chain[0])
            pm.parent(self.upperArmTwistIkCurve,w = 1)
            pm.parent(self.upperArmTwistStart,w = 1)
            upperArmSpIkSkinCluster = pm.skinCluster(self.elbowSplitUpChain.chain[0],self.elbowSplitUpChain.chain[1],self.upperArmTwistIkCurve,n = nameUtils.getSkinName())
            pm.rename(self.upperArmTwistIkCurve,upperArmTwistIkCurveName)
            self.upperArmTwistIk.poleVector.set(0,0,0)            
             
            #set stretch
            #get last cv:
            pm.select(self.upperArmTwistIkCurve + '.cv[*]')
            upperIkCLastCv = pm.ls(sl = 1)[0][-1]
            pm.skinPercent(upperArmSpIkSkinCluster,upperIkCLastCv,tv = [(self.elbowSplitChain.chain[1],1)])
              
            #get cv length
            upperArmTwistIkCurveInfoName = nameUtils.getUniqueName(self.side,'upperArmTwist','cvINFO')
            upperArmTwistIkCurveInfoNode = pm.createNode('curveInfo',n = upperArmTwistIkCurveInfoName)
            self.upperArmTwistIkCurve.getShape().worldSpace[0].connect(upperArmTwistIkCurveInfoNode.inputCurve)
               
            #create main Node
            upperArmTwistCurveMDNName = nameUtils.getUniqueName(self.side,'upperArmTwistCur','MDN')
            upperArmTwistCurveMDNNode = pm.createNode('multiplyDivide',n = upperArmTwistCurveMDNName)
               
            upperArmTwistIkCurveInfoNode.arcLength.connect(upperArmTwistCurveMDNNode.input1.input1X)
            upperArmTwistCurveMDNNode.input2.input2X.set(self.elbowSplitUpChain.chain[1].tx.get())
            upperArmTwistCurveMDNNode.operation.set(2)
               
            for num,twistJoints in enumerate(self.upperArmTwistJoint.joints):
                tempNodeName = nameUtils.getUniqueName(self.side,'upperArmTwistJnt','MDN')
                tempNode = pm.createNode('multiplyDivide',n = tempNodeName)
                if num > 0 :
                    tempNode.input1.input1X.set(twistJoints.tx.get())
                    upperArmTwistCurveMDNNode.outputX.connect(tempNode.input2.input2X)
                    tempNode.outputX.connect(twistJoints.tx)
                    
            #create upperTwistGrp
            upperArmTwistGrpName = nameUtils.getUniqueName(self.side,'upperArmTwist','grp')
            self.upperArmTwistGrp = pm.group(em = 1,n = upperArmTwistGrpName) 
            self.upperArmTwistIk.setParent(self.upperArmTwistGrp) 
            self.upperArmTwistIkCurve.setParent(self.upperArmTwistGrp) 
             
            #create upperTwistInfoGrp 
            twistInfoGrpName = nameUtils.getUniqueName(self.side,'upperArmTwistInfo','grp')
            self.upperArmTwistInfoGrp = pm.group(em = 1,n = twistInfoGrpName)
             
            #nonFlip Jnt
            nonFlipStJnt = pm.duplicate(self.limbBlendChain.chain[1],
                                        n = nameUtils.getUniqueName(self.side,'upperArmNonFlip','jc'))
            nonFlipEdJnt = pm.listRelatives(nonFlipStJnt,c = 1,typ = 'joint')
            tempTrashJnt = pm.listRelatives(nonFlipEdJnt,c = 1,typ = 'joint')
            pm.delete(tempTrashJnt)
            pm.rename(nonFlipEdJnt,nameUtils.getUniqueName(self.side,self.baseName + 'upperArmNonFlip','je'))
            nonFlipStJnt[0].setParent(self.upperArmTwistInfoGrp)
            nonFlipIks,nonFlipIksEffector = pm.ikHandle(sj = nonFlipStJnt[0],ee = nonFlipEdJnt[0],solver = 'ikRPsolver',
                                                        n = nameUtils.getUniqueName(self.side,'upperArmNonFlip','iks'))
            nonFlipIks.setParent(self.limbBlendChain.chain[1])
            nonFlipIks.poleVector.set(0,0,0)
            nonFlipIks.r.set(0,0,0)
            nonFlipIks.v.set(0)
            pm.pointConstraint(self.limbBlendChain.chain[1],nonFlipStJnt,mo = 1)
               
            #twist info jnt
            twistInfoJnt = pm.joint(n = nameUtils.getUniqueName(self.side,'upperArmTwistInfo','jc'))
            twistInfoJnt.setParent(nonFlipStJnt)
            twistInfoJnt.t.set(0,0,0)
            pm.aimConstraint(nonFlipEdJnt[0],twistInfoJnt,mo = 1,w = 1,aimVector = [1,0,0],upVector = [0,0,1],
                             worldUpType = 'objectrotation',worldUpVector = [0,0,1],
                             worldUpObject = self.limbBlendChain.chain[1])
        
            ###
            #foreArm
            self.foreArmTwistStart = pm.duplicate(self.elbowSplitDownChain.chain[0],
                                               n = nameUtils.getUniqueName(self.side,'foreArmTwistS','jj'))
            tempforeArmTrashEffNode = pm.listRelatives(self.foreArmTwistStart,c = 1,typ = 'ikEffector')
            pm.delete(tempforeArmTrashEffNode) 
            self.foreArmTwistEnd = pm.listRelatives(self.foreArmTwistStart,c = 1,typ = 'joint')
            pm.parent(self.foreArmTwistStart,w = 1)
             
            self.foreArmTwistJoint = toolModule.SplitJoint(self.foreArmTwistStart,self.lowerTwistNum,box = 1,type = 'tool',size = self.size) 
            self.foreArmTwistJoint.splitJointTool()
            
            for cube in self.foreArmTwistJoint.cubeList:
                self.handSettingCtrl.control.proxy_vis.connect(cube[0].v)
              
            for twistJoints in self.foreArmTwistJoint.joints:
                pm.rename(twistJoints, nameUtils.getUniqueName(self.side,'foreArmTwist','jj'))  
                  
            #create iks      
            foreArmTwistIkName = nameUtils.getUniqueName(self.side,'foreArmTwist','iks')  
            foreArmTwistIkCurveName = nameUtils.getUniqueName(self.side,'foreArmTwist','ikc')  
            self.foreArmTwistIk,self.foreArmTwistIkEffector,self.foreArmTwistIkCurve = pm.ikHandle(sj = self.foreArmTwistStart[0],
                                                                                          ee = self.foreArmTwistEnd[0],
                                                                                          solver = 'ikSplineSolver',
                                                                                          n = foreArmTwistIkName)
            
            self.foreArmTwistIk.setParent(self.elbowSplitDownChain.chain[0])
            pm.parent(self.foreArmTwistIkCurve,w = 1)
            pm.parent(self.foreArmTwistStart,w = 1)
            foreArmSpIkCurveSkinCluster = pm.skinCluster(self.elbowSplitDownChain.chain[0],self.limbBlendChain.chain[2],self.foreArmTwistIkCurve,n = nameUtils.getSkinName())
            pm.rename(self.foreArmTwistIkCurve,foreArmTwistIkCurveName)
            self.foreArmTwistIk.poleVector.set(0,0,0)
        
            #set stretch
            #get last cv:
            pm.select(self.foreArmTwistIkCurve + '.cv[*]')
            foreArmIkCLastCv = pm.ls(sl = 1)[0][-1]
            pm.skinPercent(foreArmSpIkCurveSkinCluster,foreArmIkCLastCv,tv = [(self.limbBlendChain.chain[2],1)])
              
            #get cv length
            foreArmTwistIkCurveInfoName = nameUtils.getUniqueName(self.side,'foreArmTwist','cvINFO')
            foreArmTwistIkCurveInfoNode = pm.createNode('curveInfo',n = foreArmTwistIkCurveInfoName)
            self.foreArmTwistIkCurve.getShape().worldSpace[0].connect(foreArmTwistIkCurveInfoNode.inputCurve)
              
            #create main Node
            foreArmTwistCurveMDNName = nameUtils.getUniqueName(self.side,'foreArmTwistCur','MDN')
            foreArmTwistCurveMDNNode = pm.createNode('multiplyDivide',n = foreArmTwistCurveMDNName)
              
            foreArmTwistIkCurveInfoNode.arcLength.connect(foreArmTwistCurveMDNNode.input1.input1X)
            foreArmTwistCurveMDNNode.input2.input2X.set(self.elbowSplitDownChain.chain[1].tx.get())
            foreArmTwistCurveMDNNode.operation.set(2)
              
            for num,twistJoints in enumerate(self.foreArmTwistJoint.joints):
                tempNodeName = nameUtils.getUniqueName(self.side,'foreArmTwistJnt','MDN')
                tempNode = pm.createNode('multiplyDivide',n = tempNodeName)
                if num > 0 :
                    tempNode.input1.input1X.set(twistJoints.tx.get())
                    foreArmTwistCurveMDNNode.outputX.connect(tempNode.input2.input2X)
                    tempNode.outputX.connect(twistJoints.tx)
              
            #create foreTwistGrp
            foreArmTwistGrpName = nameUtils.getUniqueName(self.side,'foreArmTwist','grp')
            self.foreArmTwistGrp = pm.group(em = 1,n = foreArmTwistGrpName) 
            self.foreArmTwistIk.setParent(self.foreArmTwistGrp) 
            self.foreArmTwistIkCurve.setParent(self.foreArmTwistGrp) 
              
            #lowerTwist
            foreArmTwistLocStr = pm.spaceLocator(n = nameUtils.getUniqueName(self.side,'foreArmTwistStart','loc'))
            foreArmTwistLocEd = pm.spaceLocator(n = nameUtils.getUniqueName(self.side,'foreArmTwistEnd','loc'))
              
            foreArmTwistLocStr.setParent(self.limbBlendChain.chain[1])
            foreArmTwistLocEd.setParent(self.limbBlendChain.chain[2])
            foreArmTwistLocStr.t.set(0,0,0)
            foreArmTwistLocStr.r.set(0,0,0)
            foreArmTwistLocEd.t.set(0,0,0)
            foreArmTwistLocEd.r.set(0,0,0)
            foreArmTwistLocStr.v.set(0)
            foreArmTwistLocEd.v.set(0)
              
            self.foreArmTwistIk.dTwistControlEnable.set(1)
            self.foreArmTwistIk.dWorldUpType.set(4)
            self.foreArmTwistIk.dWorldUpAxis.set(3)
            self.foreArmTwistIk.dWorldUpVector.set(0,0,1)
            self.foreArmTwistIk.dWorldUpVectorEnd.set(0,0,1)
            foreArmTwistLocStr.worldMatrix.connect(self.foreArmTwistIk.dWorldUpMatrix)
            foreArmTwistLocEd.worldMatrix.connect(self.foreArmTwistIk.dWorldUpMatrixEnd)               
        
        self.foreArmTwistIkCurve.v.set(0)
        self.upperArmTwistIkCurve.v.set(0)
        self.upperArmTwistIk.v.set(0)
        self.foreArmTwistIk.v.set(0)
        
        #twist custom attr
        #upperArm
        control.addFloatAttr(self.handSettingCtrl.control,['upperArm_twist'],-180,180)
        
        #node perpare
        upperArmTwistFixPMANodeName = nameUtils.getUniqueName(self.side,'upperArmTwistFix','PMA')
        upperArmTwistFixPMANode = pm.createNode('plusMinusAverage',n = upperArmTwistFixPMANodeName)
        
        #connect
        twistInfoJnt.rx.connect(upperArmTwistFixPMANode.input1D[0])
        self.handSettingCtrl.control.upperArm_twist.connect(upperArmTwistFixPMANode.input1D[1])
        upperArmTwistFixPMANode.output1D.connect(self.upperArmTwistIk.twist)
        
        #foreArm
        control.addFloatAttr(self.handSettingCtrl.control,['foreArm_roll'],-180,180) 
        self.handSettingCtrl.control.foreArm_roll.connect(self.foreArmTwistIk.roll)
        control.addFloatAttr(self.handSettingCtrl.control,['foreArm_twist'],-180,180) 
        self.handSettingCtrl.control.foreArm_twist.connect(self.foreArmTwistIk.twist)
          
    def __ribonSetUp(self):
        self.__setRibbonUpper()
        self.__setRibbonLower()
        self.__setRibbonSubMidCc()
         
    def __setRibbonUpper(self):
        
        #add cc ctrl
        control.addFloatAttr(self.handSettingCtrl.control,['CC'],0,1) 
        '''
        this function set ribbon for the Upper 
        '''
        #get length
        self.upperJointLentgh = self.limbBlendChain.chain[1].tx.get()
        
        self.ribon = ribbon.Ribbon(RibbonName = self.baseName + self.ribbonData[0],Length = self.upperJointLentgh,
                                   size = self.size * 0.75,subMid = 1,side = self.side,
                                   midCcName = self.baseName + self.ribbonData[0])
        self.ribon.construction()

        pm.xform(self.ribon.startLoc,ws = 1,matrix = self.limbBlendChain.chain[0].worldMatrix.get())
        pm.xform(self.ribon.endLoc,ws = 1,matrix = self.limbBlendChain.chain[1].worldMatrix.get())
        
        pm.parentConstraint(self.ikChain.chain[0],self.ribon.startLoc,mo = 1)
        
        #flip que fix
        parCnst = pm.parentConstraint(self.limbBlendChain.chain[0],self.limbBlendChain.chain[1],self.ribon.epUploc,mo = 1)
        #print parCnst

        #connect scale for ShoulderElbow jj2
        self.subMidCtrlShoulderElbow = self.ribon.subMidCtrl
        self.subMidCtrlShoulderElbow.control.scaleX.connect(self.ribon.jj[2].scaleX)
        self.subMidCtrlShoulderElbow.control.scaleY.connect(self.ribon.jj[2].scaleY)
        self.subMidCtrlShoulderElbow.control.scaleZ.connect(self.ribon.jj[2].scaleZ)

    def __setRibbonLower(self):
        '''
        this function set ribbon for the ShoulderElbow 
        '''
        self.lowerJointLentgh = self.limbBlendChain.chain[2].tx.get()
        self.ribon45hp = ribbon.Ribbon(RibbonName = self.baseName + self.ribbonData[1],Length = self.lowerJointLentgh,
                                       size = self.size * 0.75,subMid = 1,side = self.side,
                                       midCcName=self.baseName + self.ribbonData[1])
        self.ribon45hp.construction()

        pm.xform(self.ribon45hp.startLoc,ws = 1,matrix = self.limbBlendChain.chain[1].worldMatrix.get())
        pm.xform(self.ribon45hp.endLoc,ws = 1,matrix = self.limbBlendChain.chain[2].worldMatrix.get())
        
        pm.parentConstraint(self.limbBlendChain.chain[2],self.ribon45hp.endLoc,mo = 1)
        
        #flip que fix
        pm.parentConstraint(self.limbBlendChain.chain[2],self.ribon45hp.epUploc,mo = 1)
        pm.parentConstraint(self.limbBlendChain.chain[0],self.limbBlendChain.chain[1],self.ribon45hp.startUploc,mo = 1)

        #connect scale for mid jj
        self.subMidCtrlElbowWrist = self.ribon45hp.subMidCtrl
        self.subMidCtrlElbowWrist.control.scaleX.connect(self.ribon45hp.jj[2].scaleX)
        self.subMidCtrlElbowWrist.control.scaleY.connect(self.ribon45hp.jj[2].scaleY)
        self.subMidCtrlElbowWrist.control.scaleZ.connect(self.ribon45hp.jj[2].scaleZ)
        
    def __setRibbonSubMidCc(self):
        
        self.subMidCtrlElbow = control.Control(size = self.size * 0.75,baseName = self.baseName + self.ribbonData[2] + '_CC',side = self.side) 
        self.subMidCtrlElbow.circleCtrl()
        elbolPos = pm.xform(self.limbBlendChain.chain[1],query=1,ws=1,rp=1)
        pm.move(self.subMidCtrlElbow.controlGrp,elbolPos[0],elbolPos[1],elbolPos[2],a=True)
        
        pm.parentConstraint(self.subMidCtrlElbow.control,self.ribon45hp.startLoc,mo = 1)
        pm.parentConstraint(self.subMidCtrlElbow.control,self.ribon.endLoc,mo = 1)
        pm.parentConstraint(self.limbBlendChain.chain[1],self.subMidCtrlElbow.controlGrp,mo = 1)
        
        #name setting for the scale node for shoulderElbow Jj1
        shoulderElbowScaleNodeNameJj1 = nameUtils.getUniqueName(self.side,self.baseName + 'shoulderElbowScaleJj1','PMA')
        
        #create Node for  shoulderElbow Jj1
        #ribbon name for robin
        shoulderElbowScalePlusMinusAverageNodeJj1 = pm.createNode('plusMinusAverage',n = shoulderElbowScaleNodeNameJj1)
        
        #connect shoulderElbow scale for  shoulderElbow Jj1
        self.subMidCtrlShoulderElbow.control.scaleX.connect(shoulderElbowScalePlusMinusAverageNodeJj1.input3D[0].input3Dx)
        self.subMidCtrlElbow.control.scaleX.connect(shoulderElbowScalePlusMinusAverageNodeJj1.input3D[1].input3Dx)
        self.subMidCtrlShoulderElbow.control.scaleY.connect(shoulderElbowScalePlusMinusAverageNodeJj1.input3D[0].input3Dy)
        self.subMidCtrlElbow.control.scaleY.connect(shoulderElbowScalePlusMinusAverageNodeJj1.input3D[1].input3Dy)  
        self.subMidCtrlShoulderElbow.control.scaleZ.connect(shoulderElbowScalePlusMinusAverageNodeJj1.input3D[0].input3Dz)
        self.subMidCtrlElbow.control.scaleZ.connect(shoulderElbowScalePlusMinusAverageNodeJj1.input3D[1].input3Dz)     
        shoulderElbowScalePlusMinusAverageNodeJj1.operation.set(3)
        
        #output scale to shoulderElbow Jj1
        shoulderElbowScalePlusMinusAverageNodeJj1.output3D.output3Dx.connect(self.ribon.jj[1].scaleX)
        shoulderElbowScalePlusMinusAverageNodeJj1.output3D.output3Dy.connect(self.ribon.jj[1].scaleY)
        shoulderElbowScalePlusMinusAverageNodeJj1.output3D.output3Dz.connect(self.ribon.jj[1].scaleZ)
        
        #name setting for the scale node for shoulderElbow Jj3
        shoulderElbowScaleNodeNameJj3 = nameUtils.getUniqueName(self.side,self.baseName + 'shoulderElbowScaleJj3','PMA')
        
        #create Node for  shoulderElbow Jj3
        shoulderElbowScalePlusMinusAverageNodeJj3 = pm.createNode('plusMinusAverage',n = shoulderElbowScaleNodeNameJj3)
           
        #connect shoulderElbow scale for  shoulderElbow Jj3
        
        self.subMidCtrlShoulderElbow.control.scaleX.connect(shoulderElbowScalePlusMinusAverageNodeJj3.input3D[0].input3Dx)
        self.limbBlendChain.chain[1].scaleX.connect(shoulderElbowScalePlusMinusAverageNodeJj3.input3D[1].input3Dx)
        self.subMidCtrlShoulderElbow.control.scaleY.connect(shoulderElbowScalePlusMinusAverageNodeJj3.input3D[0].input3Dy)
        self.limbBlendChain.chain[1].scaleY.connect(shoulderElbowScalePlusMinusAverageNodeJj3.input3D[1].input3Dy)  
        self.subMidCtrlShoulderElbow.control.scaleZ.connect(shoulderElbowScalePlusMinusAverageNodeJj3.input3D[0].input3Dz)
        self.limbBlendChain.chain[1].scaleZ.connect(shoulderElbowScalePlusMinusAverageNodeJj3.input3D[1].input3Dz)     
        shoulderElbowScalePlusMinusAverageNodeJj3.operation.set(3)
        
        #output scale to shoulderElbow Jj3
        shoulderElbowScalePlusMinusAverageNodeJj3.output3D.output3Dx.connect(self.ribon.jj[3].scaleX)
        shoulderElbowScalePlusMinusAverageNodeJj3.output3D.output3Dy.connect(self.ribon.jj[3].scaleY)
        shoulderElbowScalePlusMinusAverageNodeJj3.output3D.output3Dz.connect(self.ribon.jj[3].scaleZ)
        
        #connect scale to shoulderElbow jj0
        self.subMidCtrlElbow.control.scaleX.connect(self.ribon.jj[0].scaleX)
        self.subMidCtrlElbow.control.scaleY.connect(self.ribon.jj[0].scaleY)
        self.subMidCtrlElbow.control.scaleZ.connect(self.ribon.jj[0].scaleZ)
        
        #connect scale to shoulderElbow jj4
        self.limbBlendChain.chain[0].scaleX.connect(self.ribon.jj[4].scaleX)
        self.limbBlendChain.chain[0].scaleY.connect(self.ribon.jj[4].scaleY)
        self.limbBlendChain.chain[0].scaleZ.connect(self.ribon.jj[4].scaleZ)
        
        #name setting for the scale node for elbowWrist Jj1
        elbowWristScaleNodeNameJj1 = nameUtils.getUniqueName(self.side,self.baseName + 'elbowWristScaleJj1','PMA')
        
        #create Node for  elbowWrist jj1
        elbowWristScalePlusMinusAverageNodeJj1 = pm.createNode('plusMinusAverage',n = elbowWristScaleNodeNameJj1)
               
        #connect elbowWrist scale for elbowWrist jj1
        self.subMidCtrlElbowWrist.control.scaleX.connect(elbowWristScalePlusMinusAverageNodeJj1.input3D[0].input3Dx)
        self.subMidCtrlElbow.control.scaleX.connect(elbowWristScalePlusMinusAverageNodeJj1.input3D[1].input3Dx)
        self.subMidCtrlElbowWrist.control.scaleY.connect(elbowWristScalePlusMinusAverageNodeJj1.input3D[0].input3Dy)
        self.subMidCtrlElbow.control.scaleY.connect(elbowWristScalePlusMinusAverageNodeJj1.input3D[1].input3Dy)  
        self.subMidCtrlElbowWrist.control.scaleZ.connect(elbowWristScalePlusMinusAverageNodeJj1.input3D[0].input3Dz)
        self.subMidCtrlElbow.control.scaleZ.connect(elbowWristScalePlusMinusAverageNodeJj1.input3D[1].input3Dz)     
        elbowWristScalePlusMinusAverageNodeJj1.operation.set(3)
        
        #output scale to elbowWrist jj1
        elbowWristScalePlusMinusAverageNodeJj1.output3D.output3Dx.connect(self.ribon45hp.jj[1].scaleX)
        elbowWristScalePlusMinusAverageNodeJj1.output3D.output3Dy.connect(self.ribon45hp.jj[1].scaleY)
        elbowWristScalePlusMinusAverageNodeJj1.output3D.output3Dz.connect(self.ribon45hp.jj[1].scaleZ)
        
        #name setting for the scale node for elbowWrist Jj3
        elbowWristScaleNodeNameJj3 = nameUtils.getUniqueName(self.side,self.baseName + 'elbowWristScaleJj3','PMA')
        
        #create Node for  elbowWrist jj3
        elbowWristScalePlusMinusAverageNodeJj3 = pm.createNode('plusMinusAverage',n = elbowWristScaleNodeNameJj3)
               
        #connect elbowWrist scale for elbowWrist jj3
        self.subMidCtrlElbowWrist.control.scaleX.connect(elbowWristScalePlusMinusAverageNodeJj3.input3D[0].input3Dx)
        self.subMidCtrlElbow.control.scaleX.connect(elbowWristScalePlusMinusAverageNodeJj3.input3D[1].input3Dx)
        self.subMidCtrlElbowWrist.control.scaleY.connect(elbowWristScalePlusMinusAverageNodeJj3.input3D[0].input3Dy)
        self.subMidCtrlElbow.control.scaleY.connect(elbowWristScalePlusMinusAverageNodeJj3.input3D[1].input3Dy)  
        self.subMidCtrlElbowWrist.control.scaleZ.connect(elbowWristScalePlusMinusAverageNodeJj3.input3D[0].input3Dz)
        self.subMidCtrlElbow.control.scaleZ.connect(elbowWristScalePlusMinusAverageNodeJj3.input3D[1].input3Dz)     
        elbowWristScalePlusMinusAverageNodeJj3.operation.set(3)
        
        #output scale to elbowWrist jj3
        elbowWristScalePlusMinusAverageNodeJj3.output3D.output3Dx.connect(self.ribon45hp.jj[3].scaleX)
        elbowWristScalePlusMinusAverageNodeJj3.output3D.output3Dy.connect(self.ribon45hp.jj[3].scaleY)
        elbowWristScalePlusMinusAverageNodeJj3.output3D.output3Dz.connect(self.ribon45hp.jj[3].scaleZ)
        
        #connect scale to elbowWrist jj4
        self.subMidCtrlElbow.control.scaleX.connect(self.ribon45hp.jj[4].scaleX)
        self.subMidCtrlElbow.control.scaleY.connect(self.ribon45hp.jj[4].scaleY)
        self.subMidCtrlElbow.control.scaleZ.connect(self.ribon45hp.jj[4].scaleZ)
        
        #connect scale to elbowWrist jj0
        self.limbBlendChain.chain[2].scaleX.connect(self.ribon45hp.jj[0].scaleX)
        self.limbBlendChain.chain[2].scaleY.connect(self.ribon45hp.jj[0].scaleY)
        self.limbBlendChain.chain[2].scaleZ.connect(self.ribon45hp.jj[0].scaleZ)
 
    def __shoulderCtrl(self):
        
        #add Ctrl 
        self.shoulderCtrl = control.Control(self.side,self.baseName + 'Shoulder',self.size,aimAxis = 'y') 
        self.shoulderCtrl.pinCtrl() 
        
        #align
        posArraySpJj = self.shoulderChain.chain[0]
        posArrayEpJj = self.shoulderChain.chain[1]
          
        posArraySp = posArraySpJj.worldMatrix.get()
        posArrayEp = posArrayEpJj.worldMatrix.get()
          
        pm.xform(self.shoulderCtrl.controlGrp,ws = 1,matrix = posArraySp)
        self.shoulderCtrl.controlGrp.sx.set(self.size)
        self.shoulderCtrl.controlGrp.sy.set(self.size)
        self.shoulderCtrl.controlGrp.sz.set(self.size)
        pm.makeIdentity(self.shoulderCtrl.controlGrp, apply = 1 ,t = 0, r = 0 ,s = 1,n = 0,pn = 1)
        self.shoulderCtrl.control.sy.set(-1)
          
        sdCvOffset = posArraySp[-1][0] - posArrayEp[-1][0]
           
        for shape in self.shoulderCtrl.control.getShapes():
            pm.move(-sdCvOffset,posArraySp[-1][1],posArraySp[-1][2],shape)
          
        pm.makeIdentity(self.shoulderCtrl.control,apply = True,t = 1,r = 0,s = 1,n = 0,pn = 1)
        control.lockAndHideAttr(self.shoulderCtrl.control,['sx','sy','sz','v'])
          
        #clean
        self.shoulderChain.chain[0].setParent(self.shoulderCtrl.control)
           
        #AT shoulder
        #add attr
        control.addFloatAttr(self.shoulderCtrl.control,['follow_ik'],0,1)
           
        #create AT joint 
        self.shoulderAtChain = boneChain.BoneChain(self.baseName + 'AtSd',self.side,type = 'jc')
        self.shoulderAtChain.fromList(self.limbGuidePos,self.limbGuideRot)
        self.shoulderAtGrp = pm.group(em = 1,n = nameUtils.getUniqueName(self.side,self.baseName + 'AtSd','grp'))
        pm.xform(self.shoulderAtGrp,ws = 1,matrix = posArraySp)
        self.shoulderAtChain.chain[0].setParent(self.shoulderAtGrp)
           
        #create ikHandle:
        atIkName = nameUtils.getUniqueName(self.side,self.baseName + 'AtSd','iks')
        self.ikAtHandle,self.ikAtEffector = pm.ikHandle(sj = self.shoulderAtChain.chain[0],
                                                    ee = self.shoulderAtChain.chain[2],solver = self.solver,n = atIkName)
        self.ikAtHandle.setParent(self.ikChain.ikCtrl.control)
        pm.poleVectorConstraint(self.ikChain.poleVectorCtrl.control,atIkName,w = 1)
        self.ikAtHandle.v.set(0)
           
        #connect to the shoulder
        #node name
        remapColorNodeName = nameUtils.getUniqueName(self.side,self.baseName + 'AtSd','RC')
        multipleNodeName = nameUtils.getUniqueName(self.side,self.baseName + 'AtSd','MDN')
           
        #create node
        remapColorNode = pm.createNode('remapColor',n = remapColorNodeName)
        multipleNode = pm.createNode('multiplyDivide',n = multipleNodeName)
           
        #parpare to connect
        self.shoulderBriGrp = pm.group(self.shoulderCtrl.control,
                                       n = nameUtils.getUniqueName(self.side,self.baseName + 'BriAtSd','grp'))
        briPos = self.shoulderChain.chain[0].getTranslation(space = 'world')
        pm.move(briPos[0],briPos[1],briPos[2],self.shoulderBriGrp + '.rotatePivot')
        pm.move(briPos[0],briPos[1],briPos[2],self.shoulderBriGrp + '.scalePivot')
        pm.move(briPos[0],briPos[1],briPos[2],self.shoulderCtrl.control + '.rotatePivot')
        pm.move(briPos[0],briPos[1],briPos[2],self.shoulderCtrl.control + '.scalePivot')        
        pm.move(briPos[0],briPos[1],briPos[2],self.shoulderCtrl.controlGrp + '.rotatePivot')
        pm.move(briPos[0],briPos[1],briPos[2],self.shoulderCtrl.controlGrp + '.scalePivot')          
           
        self.shoulderBriGrp.setParent(self.shoulderCtrl.controlGrp)        
           
        #connect
        self.shoulderCtrl.control.follow_ik.connect(multipleNode.input2X)
        self.shoulderCtrl.control.follow_ik.connect(multipleNode.input2Y)
        self.shoulderCtrl.control.follow_ik.connect(multipleNode.input2Z)
#         ori connect
#         self.shoulderAtChain.chain[0].rx.connect(multipleNode.input1X)
#         self.shoulderAtChain.chain[0].ry.connect(multipleNode.input1Y)
#         self.shoulderAtChain.chain[0].rz.connect(multipleNode.input1Z)
        multipleNode.outputX.connect(remapColorNode.colorR)
        multipleNode.outputY.connect(remapColorNode.colorG)
        multipleNode.outputZ.connect(remapColorNode.colorB)
           
        remapColorNode.outColor.outColorG.connect(self.shoulderBriGrp.ry)
        remapColorNode.outColor.outColorB.connect(self.shoulderBriGrp.rz)
           
        remapColorNode.inputMin.set(-90)
        remapColorNode.inputMax.set(90)
        remapColorNode.outputMin.set(-45)
        remapColorNode.outputMax.set(45)
           
        remapColorNode.green[0].green_FloatValue.set(0.25)
        remapColorNode.green[0].green_Position.set(0)
        remapColorNode.green[1].green_FloatValue.set(0.6)
        remapColorNode.green[1].green_Position.set(1)        
        remapColorNode.green[2].green_FloatValue.set(0.5)
        remapColorNode.green[2].green_Position.set(0.5)
        remapColorNode.green[2].green_Interp.set(1)
           
        remapColorNode.blue[0].blue_FloatValue.set(0.15)
        remapColorNode.blue[0].blue_Position.set(0)
        remapColorNode.blue[1].blue_FloatValue.set(0.6)
        remapColorNode.blue[1].blue_Position.set(1)        
        remapColorNode.blue[2].blue_FloatValue.set(0.5)
        remapColorNode.blue[2].blue_Position.set(0.5)
        remapColorNode.blue[2].blue_Interp.set(1)  
        remapColorNode.blue[3].blue_FloatValue.set(0.3)
        remapColorNode.blue[3].blue_Position.set(0.25)      
        remapColorNode.blue[3].blue_Interp.set(1)   
           
        #shoulderBlade
        #initial
        pm.select(cl = 1)
         
        self.shoulderBladeGrp = pm.group(n = nameUtils.getUniqueName(self.side,self.baseName + 'ShoulderBlade','grp'))
        pm.xform(self.shoulderBladeGrp,ws = 1,matrix = posArraySp)
        pm.select(cl = 1)
         
        self.shoulderBladeBriGrp = pm.group(n = nameUtils.getUniqueName(self.side,self.baseName + 'ShoulderBlade_Bri','grp'))
        pm.xform(self.shoulderBladeBriGrp,ws = 1,matrix = posArraySp)
        self.shoulderBladeBriGrp.setParent(self.shoulderBladeGrp)
        self.shoulderBladeChain.chain[0].setParent(self.shoulderBladeBriGrp)
#         pm.select(self.shoulderBladeChain.chain[0])
#         pm.move(briPos[0],briPos[1],briPos[2],self.shoulderBladeChain.chain[0] + '.rotatePivot')
#         pm.move(briPos[0],briPos[1],briPos[2],self.shoulderBladeChain.chain[0] + '.scalePivot')
           
        #node name
        remapValueShoulderFBNodeName = nameUtils.getUniqueName(self.side,self.baseName + 'ShoulderFwBk','RV')
        remapValueShoulderUDNodeName = nameUtils.getUniqueName(self.side,self.baseName + 'ShoulderUpDn','RV')
           
        #create Node
        remapValueShoulderFBNode = pm.createNode('remapValue',n = remapValueShoulderFBNodeName)
        remapValueShoulderUDNode = pm.createNode('remapValue',n = remapValueShoulderUDNodeName)
           
        #connect
        #FB
#         self.shoulderCtrl.control.rz.connect(remapValueShoulderFBNode.inputValue)
        remapValueShoulderFBNode.inputMin.set(-90)
        remapValueShoulderFBNode.inputMax.set(90)
        remapValueShoulderFBNode.outputMin.set(-90)
        remapValueShoulderFBNode.outputMax.set(90)
        remapValueShoulderFBNode.outValue.connect(self.shoulderBladeBriGrp.rz)
   
        remapValueShoulderFBNode.value[1].value_FloatValue.set(0.75)
        remapValueShoulderFBNode.value[1].value_Position.set(1)                                                        
        remapValueShoulderFBNode.value[2].value_FloatValue.set(0.5)
        remapValueShoulderFBNode.value[2].value_Position.set(0.5)
        remapValueShoulderFBNode.value[2].value_Interp.set(1)        
           
        #UD
#         self.shoulderCtrl.control.ry.connect(remapValueShoulderUDNode.inputValue)
        remapValueShoulderUDNode.inputMin.set(-90)
        remapValueShoulderUDNode.inputMax.set(90)
        remapValueShoulderUDNode.outputMin.set(float(self.shoulderChain.chain[-1].tx.get() / 4))
        remapValueShoulderUDNode.outputMax.set(-float(self.shoulderChain.chain[-1].tx.get() / 4))
        remapValueShoulderUDNode.outValue.connect(self.shoulderBladeBriGrp.tz)
   
        remapValueShoulderUDNode.value[1].value_FloatValue.set(0.75)
        remapValueShoulderUDNode.value[1].value_Position.set(1)                                                        
        remapValueShoulderUDNode.value[2].value_FloatValue.set(0.5)
        remapValueShoulderUDNode.value[2].value_Position.set(0.5)
        remapValueShoulderUDNode.value[2].value_Interp.set(1)     
           
        #connect to the AT
        #create PMA node
        plusMinusAverageAtSdNodeName = nameUtils.getUniqueName(self.side,self.baseName + 'AtSd','PMA')
           
        #create Node 
        plusMinusAverageAtSdNode = pm.createNode('plusMinusAverage',n = plusMinusAverageAtSdNodeName)
           
        #connect
        self.shoulderCtrl.control.rx.connect(plusMinusAverageAtSdNode.input3D[0].input3Dx)
        self.shoulderCtrl.control.ry.connect(plusMinusAverageAtSdNode.input3D[0].input3Dy)
        self.shoulderCtrl.control.rz.connect(plusMinusAverageAtSdNode.input3D[0].input3Dz)
        self.shoulderBriGrp.ry.connect(plusMinusAverageAtSdNode.input3D[1].input3Dy)
        self.shoulderBriGrp.rz.connect(plusMinusAverageAtSdNode.input3D[1].input3Dz)
           
        plusMinusAverageAtSdNode.output3D.output3Dy.connect(remapValueShoulderUDNode.inputValue)
        plusMinusAverageAtSdNode.output3D.output3Dz.connect(remapValueShoulderFBNode.inputValue)
           
        ##############
        #chest clean 
#         self.chestGrp = pm.group(em = 1,n = nameUtils.getUniqueName('m','chest','grp'))
#         self.chestGrp.setParent(self.hi.SKL)
#         self.shoulderCtrl.controlGrp.setParent(self.chestGrp)
#         self.shoulderAtChain.chain[0].setParent(self.chestGrp)
           
        ############
        #pose Reador
           
        #set main Loc
        poseMain = pm.spaceLocator(n = nameUtils.getUniqueName(self.side,self.baseName + 'PoseReadorMain','loc'))
        poseMain.overrideEnabled.set(1)
        poseMain.overrideColor.set(16)
           
        poseUp = pm.spaceLocator(n = nameUtils.getUniqueName(self.side,self.baseName + 'PoseReadorUp','loc'))
        poseUp.localScale.set(0.5,0.5,0.5)
        poseUp.overrideEnabled.set(1)
        poseUp.overrideColor.set(16)
           
        poseTar = pm.spaceLocator(n = nameUtils.getUniqueName(self.side,self.baseName + 'PoseReadorTar','loc'))
        poseTar.localScale.set(0.25,0.25,0.25)
        poseTar.overrideEnabled.set(1)
        poseTar.overrideColor.set(16)
          
        #set twist loc
        poseTwistMain = pm.spaceLocator(n = nameUtils.getUniqueName(self.side,self.baseName + 'PoseReadorTwistMain','loc'))
        poseTwistMain.overrideEnabled.set(1)
        poseTwistMain.overrideColor.set(4)
          
        poseTwistUp = pm.spaceLocator(n = nameUtils.getUniqueName(self.side,self.baseName + 'PoseReadorTwistUp','loc'))
        poseTwistUp.localScale.set(0.5,0.5,0.5)
        poseTwistUp.overrideEnabled.set(1)
        poseTwistUp.overrideColor.set(4)
          
        poseTwistTar = pm.spaceLocator(n = nameUtils.getUniqueName(self.side,self.baseName + 'PoseReadorTwistTar','loc'))
        poseTwistTar.localScale.set(0.25,0.25,0.25)
        poseTwistTar.overrideEnabled.set(1)
        poseTwistTar.overrideColor.set(4) 
          
        pm.setAttr(poseMain + '.tx',float(-self.shoulderAtChain.chain[1].tx.get() / 4))
        pm.setAttr(poseTar + '.tx',float(self.shoulderAtChain.chain[1].tx.get() / 4))
        pm.setAttr(poseUp + '.tx',float(-self.shoulderAtChain.chain[1].tx.get() / 4))
        pm.setAttr(poseUp + '.ty',float(-self.shoulderAtChain.chain[1].tx.get() / 4))
          
        #create grp
        #main
        self.poseReadorGrp = pm.group(em = 1,n = nameUtils.getUniqueName(self.side,self.baseName + 'PoseReadorMain','grp'))
          
        poseMain.setParent(self.poseReadorGrp)
        poseTar.setParent(self.poseReadorGrp)
        poseUp.setParent(self.poseReadorGrp)
          
        poseTwistUp.setParent(self.poseReadorGrp)
        poseTwistMain.setParent(self.poseReadorGrp)        
        poseTwistTar.setParent(self.poseReadorGrp)
                    
        pm.xform(self.poseReadorGrp,ws = 1,matrix = self.limbBlendChain.chain[0].worldMatrix.get())
        self.poseReadorGrp.setParent(self.shoulderAtChain.chain[0])
        self.poseReadorGrp.t.set(0,0,0)
        self.poseReadorGrp.r.set(0,0,0)
          
        pm.aimConstraint(poseTar,poseMain,offset = [0,0,0],w = 1,aimVector = [1,0,0],upVector = [0,-1,0],
                         worldUpType = 'object',worldUpObject = poseUp)        
  
        #twist
        pm.setAttr(poseTwistTar + '.ty',float(-self.shoulderAtChain.chain[1].tx.get() / 4))
        pm.setAttr(poseTwistUp + '.tx',float(-self.shoulderAtChain.chain[1].tx.get() / 8))
            
        pm.aimConstraint(poseTwistTar,poseTwistMain,offset = [0,0,0],w = 1,aimVector = [0,-1,0],upVector = [-1,0,0],
                        worldUpType = 'object',worldUpObject = poseTwistUp)
            
        #connect 
#         self.poseReadorGrp.setParent(self.chestGrp)
        postTarGrp = pm.group(poseTar,n = nameUtils.getUniqueName(self.side,self.baseName + 'PoseReadorTar','grp'))
            
        pm.move(self.limbBlendChain.chain[0].tx.get(),self.limbBlendChain.chain[0].ty.get(),
                self.limbBlendChain.chain[0].tz.get(),postTarGrp + '.rotatePivot')
        pm.move(self.limbBlendChain.chain[0].tx.get(),self.limbBlendChain.chain[0].ty.get(),
                self.limbBlendChain.chain[0].tz.get(),postTarGrp + '.scalePivot')
            
        postTarGrp.setParent(self.shoulderAtChain.chain[0])
        poseTwistTar.setParent(postTarGrp)
        poseTwistGrp = pm.group(poseTwistUp,poseTwistMain,n = nameUtils.getUniqueName(self.side,self.baseName + 'PoseReadorTwist','grp'))
            
        pm.move(self.limbBlendChain.chain[0].tx.get(),self.limbBlendChain.chain[0].ty.get(),
                self.limbBlendChain.chain[0].tz.get(),poseTwistGrp + '.rotatePivot')
        pm.move(self.limbBlendChain.chain[0].tx.get(),self.limbBlendChain.chain[0].ty.get(),
                self.limbBlendChain.chain[0].tz.get(),poseTwistGrp + '.scalePivot')        
            
        #multiple node name
        prMultipleNodeName = nameUtils.getUniqueName(self.side,self.baseName + 'PoseReadorBri','MDN')
            
        #create Node
        prMultipleNode = pm.createNode('multiplyDivide',n = prMultipleNodeName)
            
        poseMain.ry.connect(prMultipleNode.input1Y)
        poseMain.rz.connect(prMultipleNode.input1Z)
        prMultipleNode.input2Y.set(1.5)
        prMultipleNode.input2Z.set(1.5)
        prMultipleNode.outputY.connect(poseTwistGrp.ry)
        prMultipleNode.outputZ.connect(poseTwistGrp.rz)
            
        control.addFloatAttr(self.shoulderAtChain.chain[0],
                             ['pose_bend','pose_side','pose_twist'],-3600,3600) 
            
        #get correct value
        prMultipleNode.outputY.connect(self.shoulderAtChain.chain[0].pose_bend)
        prMultipleNode.outputZ.connect(self.shoulderAtChain.chain[0].pose_side)
        poseTwistMain.rx.connect(self.shoulderAtChain.chain[0].pose_twist)
            
        #reconnect
        self.shoulderAtChain.chain[0].pose_bend.connect(multipleNode.input1Y)
        self.shoulderAtChain.chain[0].pose_side.connect(multipleNode.input1Z)
#         self.shoulderAtChain.chain[0].pose_twist.connect(multipleNode.input1X)
            
        #clean
        self.poseReadorGrp.v.set(0)
        postTarGrp.v.set(0)  
           
    def __cleanUp(self):
          
        #ccDef grp and v
        self.ccDefGrp = pm.group(empty = 1,n = nameUtils.getUniqueName(self.side,self.baseName + 'Def','grp'))          
        
        if self.twist == 'ribon45hp':
            self.handSettingCtrl.control.CC.set(0)
            self.handSettingCtrl.control.CC.connect(self.ccDefGrp.v)
            self.subMidCtrlShoulderElbow.controlGrp.setParent(self.ccDefGrp)
            self.subMidCtrlElbowWrist.controlGrp.setParent(self.ccDefGrp)
            self.subMidCtrlElbow.controlGrp.setParent(self.ccDefGrp)
          
        #cc hierarchy        
        self.cntsGrp = pm.group(self.ikChain.ikCtrl.controlGrp,
                                n = nameUtils.getUniqueName(self.side,self.baseName + 'CC','grp'))          
  
        self.ccDefGrp.setParent(self.cntsGrp)
        self.handSettingCtrl.controlGrp.setParent(self.cntsGrp)                
          
        #ribbon hierarchy   
#         self.ribon.main.v.set(0)
#         self.ribon45hp.main.v.set(0)
        
        #jj grp
        self.limbGrp = pm.group(em = 1,n = nameUtils.getUniqueName(self.side,self.baseName,'grp'))        
        
        #ik stretch/lock loc vis            
        if self.solver == 'ikRPsolver':
            pm.parent(self.ikChain.poleVectorCtrl.controlGrp,self.cntsGrp)
            self.ikChain.stretchStartLoc.v.set(0)
            self.ikChain.lockUpStartLoc.v.set(0)               
            self.ikChain.lockUpStartLoc.setParent(self.limbGrp)
            self.ikChain.stretchStartLoc.setParent(self.limbGrp)
            
        if self.shoulder == 'yes':
            self.limbGrp.setParent(self.shoulderCtrl.control)
            
        armInitial =  self.limbBlendChain.chain[0].getTranslation(space = 'world')
        pm.move(armInitial[0],armInitial[1],armInitial[2],self.limbGrp + '.rotatePivot')
        pm.move(armInitial[0],armInitial[1],armInitial[2],self.limbGrp + '.scalePivot')
          
        for b in (self.ikChain,self.fkChain,self.limbBlendChain):
            b.chain[0].setParent(self.limbGrp)                 
         
#         for b in (self.ikChain,self.fkChain,self.limbBlendChain):
#             b.chain[0].setParent(self.bonesGrp)
#          
#         self.cntsGrp = pm.group(self.ikChain.ikCtrl.controlGrp,
#                                 n = nameUtils.getUniqueName(self.side,self.baseName + 'CC','grp'))
#              
#         self.mainGrp = pm.group(self.bonesGrp,self.cntsGrp,self.handSettingCtrl,
#                                 n = nameUtils.getUniqueName(self.side,self.baseName,'grp'))   
 
    def __buildHooks(self):
 
        #create and align
        worldName = nameUtils.getUniqueName(self.side,self.baseName + 'World','loc')
        self.locWorld = pm.spaceLocator(n = worldName)
        self.locWorld.v.set(0)
           
        localName = nameUtils.getUniqueName(self.side,self.baseName + 'Local','loc')
        self.locLocal = pm.spaceLocator(n = localName)
        self.locLocal.v.set(0)
           
        pm.xform(self.locWorld,ws = 1,matrix = self.limbBlendChain.chain[0].wm.get())
        pm.xform(self.locLocal,ws = 1,matrix = self.limbBlendChain.chain[0].wm.get())
         
        self.locWorld.r.set(0,0,0)
        self.locLocal.r.set(0,0,0)
          
        if self.shoulder == 'yes':  
            self.locLocal.setParent(self.shoulderChain.chain[-1])
            pm.parentConstraint(self.shoulderCtrl.control,self.locWorld,skipRotate = ['x','y','z'],mo = 1)
           
        self.fkChain.chain[0].addAttr('space',at = 'enum',en = 'world:local:',k = 1)
           
        #add target tester
        targetName = nameUtils.getUniqueName(self.side,self.baseName + 'Tar','loc')
        self.__tempSpaceSwitch = pm.spaceLocator(n = targetName)
        pm.xform(self.__tempSpaceSwitch,ws = 1,matrix = self.limbBlendChain.chain[0].wm.get())
        self.__tempSpaceSwitch.v.set(0)
      
        #final cnst
        finalCnst = pm.parentConstraint(self.locLocal,self.locWorld,self.__tempSpaceSwitch,mo = 0)
        reverseNodeName = nameUtils.getUniqueName(self.side,self.baseName + 'Hook','REV')
        reverseNode = pm.createNode('reverse',n = reverseNodeName)
              
        #fk cnst
        pm.parentConstraint(self.__tempSpaceSwitch,self.limbGrp,mo = 1)
        self.fkChain.chain[0].attr('space').connect(finalCnst.attr(self.locLocal.name() + 'W0'))
        self.fkChain.chain[0].attr('space').connect(reverseNode.inputX)
        reverseNode.outputX.connect(finalCnst.attr(self.locWorld.name() + 'W1'))

    def buildConnections(self):

        #reveice info from incoming package
        if pm.objExists(self.metaMain) and pm.objExists(self.metaSpine) == 1:
            
            print ''
            print 'Package from (' + self.metaMain + ') has been received'
            
            pm.select(self.metaMain) 
            main = pm.selected()[0]
            
            pm.select(self.metaSpine)
            spine = pm.selected()[0]
            
            #meta main
            mainDestinations = []
            moduleGrp = pm.connectionInfo(main.moduleGrp, destinationFromSource=True)
            
            #meta spine
            spineDestinations = []
            transGrp = pm.connectionInfo(spine.transGrp, destinationFromSource=True)
            
            #get linked
            for tempMainDestination in moduleGrp:
                splitTempMainDestination = tempMainDestination.split('.')
                mainDestinations.append(splitTempMainDestination[0])
                
            for tempSpineDestination in transGrp:
                splitTempSpineDestination = tempSpineDestination.split('.')
                spineDestinations.append(splitTempSpineDestination[0])
 
            #to the chest
            if self.solver == 'ikRPsolver' and self.shoulder == 'yes' :
                self.shoulderBladeGrp.setParent(spineDestinations[0])
                self.shoulderAtGrp.setParent(spineDestinations[0])
                self.shoulderCtrl.controlGrp.setParent(spineDestinations[0])
                self.poseReadorGrp.setParent(spineDestinations[0])

            #to the main hierachy
            for grp in mainDestinations:
                destnation = grp.split('_')
                if destnation[1] == 'CC':
                    CC = grp                
                elif destnation[1] == 'SKL':
                    SKL = grp                    
                elif destnation[1] == 'IK':
                    IK = grp                    
                elif destnation[1] == 'LOC':
                    LOC = grp                            
                elif destnation[1] == 'XTR':
                    XTR = grp                             
                elif destnation[1] == 'GUD':
                    GUD = grp                          
                elif destnation[1] == 'GEO':
                    GEO = grp                      
                elif destnation[1] == 'ALL':
                    ALL = grp                      
                elif destnation[1] == 'XTR':
                    XTR = grp                      
                elif destnation[1] == 'TRS':
                    TRS = grp                      
                elif destnation[1] == 'PP':
                    PP = grp      
                
            self.cntsGrp.setParent(CC)   
            self.ikChain.ikHandle.setParent(IK)
            self.ikChain.distTransNode.setParent(XTR) 
            self.guideGrp.setParent(GUD)
            self.locWorld.setParent(GUD)
            self.mirrorGuideGrp.setParent(GUD)
            self.__tempSpaceSwitch.setParent(XTR)
            
            if self.solver == 'ikRPsolver':
                self.ikChain.ikBeamCurve.setParent(XTR)
                self.ikChain.upDistTransNode.setParent(XTR)
                self.ikChain.downDistTransNode.setParent(XTR)
             
            if self.twist == 'ribon45hp':
                self.ribon.main.setParent(XTR)
                self.ribon45hp.main.setParent(XTR) 
             
            print ''
            print 'Info from (' + self.meta + ') has been integrate, ready for next Module'
            print ''
            
        else:
            OpenMaya.MGlobal.displayError('Target :' + self.metaMain + ' is NOT exist')
            
        #create package send for next part
        
        #template:
        #metaUtils.addToMeta(self.meta,'attr', objs)
        metaUtils.addToMeta(self.meta,'controls',[self.ikChain.ikCtrl.control] + [self.handSettingCtrl.control]) 
        metaUtils.addToMeta(self.meta,'moduleGrp',[self.limbGrp])
        metaUtils.addToMeta(self.meta,'chain', [ik for ik in self.ikChain.chain] + [ori for ori in self.limbBlendChain.chain])
        metaUtils.addToMeta(self.meta,'guideLocator',[mirrorGuide for mirrorGuide in self.mirrorGuideList])

         
        if self.twist == 'non_roll':
            metaUtils.addToMeta(self.meta,'skinJoints',[skinjoint for skinjoint in self.upperArmTwistJoint.joints]
                                + [skinjoint for skinjoint in self.foreArmTwistJoint.joints])     
            self.upperArmTwistStart[0].setParent(SKL)
            self.upperArmTwistGrp.setParent(XTR)
            self.upperArmTwistInfoGrp.setParent(XTR)
            self.foreArmTwistStart[0].setParent(SKL)
            self.foreArmTwistGrp.setParent(XTR)        
        
def getUi(parent,mainUi):
    
    return LimbModuleUi(parent,mainUi)

class LimbModuleUi(object):
    
    def __init__(self,parent,mainUi):
        
        self.mainUi = mainUi
        self.__popuItems = []
        
        pm.setParent(parent)
        self.mainL = pm.columnLayout(adj = 1)
        pm.separator(h = 10)
        
        self.limb = pm.columnLayout(adj = 1,p = self.mainL) 
        self.name = pm.text(l = '**** Limb Module ****')       
        self.baseNameT = pm.textFieldGrp(l = 'baseName : ',ad2 = 1,cl2 = ['left','left'],text = 'arm')
        
        #size
        self.cntSize = pm.floatFieldGrp(l = 'ctrl Size : ',cl2 = ['left','left'],
                                        ad2 = 1,numberOfFields = 1,value1 = 1,p = self.limb)    
        
        #side
        pm.rowLayout(adj = 1,nc=100,p = self.limb)
        pm.button(l = 'side : ')
        self.sideR = pm.radioButtonGrp(nrb = 2,la2 = ['left','right'],sl = 1)        
        
        #mirror 
        pm.rowLayout(adj = 1,nc=100,p = self.limb)
        pm.button(l = 'mirror : ')
        self.mirrorNodeM = pm.optionMenu(l = 'mirrorMeta : ',p = self.limb)
        self.mirrorR = pm.radioButtonGrp(nrb = 2,la2 = ['yes','no'],sl = 2,onc = self.__metaReload)        
                
        #shoulder
        self.shoulderMenu = pm.optionMenu(l = 'shoulder : ',p = self.limb)
        pm.menuItem(l = 'yes',p = self.shoulderMenu)
        pm.menuItem(l = 'no',p = self.shoulderMenu)        
        
        #elbow
        self.elbowMenu = pm.optionMenu(l = 'elbow Method : ',p = self.limb)
        pm.menuItem(l = 'split',p = self.elbowMenu)
        pm.menuItem(l = 'partial',p = self.elbowMenu)
        pm.menuItem(l = 'nope',p = self.elbowMenu)
        
        #slover 
        self.solverMenu = pm.optionMenu(l = 'solver : ',p = self.limb)
        pm.menuItem(l = 'ikRPsolver',p = self.solverMenu)
        pm.menuItem(l = 'ikSCsolver',p = self.solverMenu) 
        
        #twist
        self.twistModule = pm.optionMenu(l = 'twist module : ',p = self.limb)
        pm.menuItem(l = 'non_roll',p = self.twistModule)
        pm.menuItem(l = 'ribon45hp',p = self.twistModule)
        pm.menuItem(l = 'nope',p = self.twistModule)
        
        #twist num
        pm.rowLayout(adj = 1,nc=100,p = self.limb)
        pm.button(l = 'upper Twist num : ')
        self.upperNum = pm.intSliderGrp(f=1,max=10,s=1,min = 2,v = 5)
         
        pm.rowLayout(adj = 1,nc=100,p = self.limb)
        pm.button(l = 'lower  Twist num : ')
        self.lowerNum = pm.intSliderGrp(f=1,max=10,s=1,min = 2,v = 5) 
        
        #meta
        self.metaSpineNodeM = pm.optionMenu(l = 'spineMeta : ',p = self.limb)
        metaUtils.metaSel()
        self.metaMainNodeM = pm.optionMenu(l = 'mainMeta : ',p = self.limb)
        metaUtils.metaSel()
        
        self.ver2Loc = pm.button(l = 'ver2Loc',c = self.__clusLoc,p = self.limb)
        pm.separator(h = 10,p = self.limb)
        self.removeB = pm.button(l = 'remove',c = self.__removeInstance,p = self.limb)
         
        self.__pointerClass = None
        
    def __removeInstance(self,*arg):
        
        pm.deleteUI(self.mainL)
        self.mainUi.modulesUi.remove(self)
        
    def __metaReload(self,*arg):
        
        oriItem = pm.optionMenu(self.mirrorNodeM,q = 1,ils = 1)        
        if oriItem != None:
            for Item in oriItem:
                pm.deleteUI(Item)
                
        selStr = pm.ls('*META*',type = 'lightInfo')     
        for sel in selStr:
            pm.menuItem(l = sel,p = self.mirrorNodeM)     
        
    def getModuleInstance(self):
        
        baseNameT = pm.textFieldGrp(self.baseNameT,q = 1,text = 1)
        sideR = pm.radioButtonGrp(self.sideR,q = True,sl = True)
        mirrorR = pm.radioButtonGrp(self.mirrorR,q = True,sl = True)
        
        if sideR == 1:
            sideT = 'l'
        elif sideR == 2:
            sideT = 'r'     
        
        if mirrorR == 1:
            mirrorT = 'yes'
        elif mirrorR == 2:
            mirrorT = 'no'        
            
        cntSizeV = pm.floatFieldGrp(self.cntSize,q = 1,value1 = 1)
        solverV = pm.optionMenu(self.solverMenu, q = 1,v = 1)
        elbowT = pm.optionMenu(self.elbowMenu, q = 1,v = 1)
        shoulderT = pm.optionMenu(self.shoulderMenu, q = 1,v = 1)
        twistT = pm.optionMenu(self.twistModule, q = 1,v = 1)
        upperTwistNumV = pm.intSliderGrp(self.upperNum , q = 1,v = 1)
        lowerTwistNumV = pm.intSliderGrp(self.lowerNum ,q = 1,v = 1)
        mainMetaNode = pm.optionMenu(self.metaMainNodeM,q = 1,v = 1)
        spineMetaNode = pm.optionMenu(self.metaSpineNodeM,q = 1,v = 1)
        mirrorMetaNode = pm.optionMenu(self.mirrorNodeM,q = 1,v = 1)
        
        self.__pointerClass = LimbModule(baseNameT,sideT,size = cntSizeV,solver = solverV,
                                         metaSpine = spineMetaNode,metaMain = mainMetaNode,
                                         shoulder = shoulderT,elbow = elbowT,twist = twistT,
                                         upperTwistNum = upperTwistNumV,lowerTwistNum = lowerTwistNumV,
                                         mirror = mirrorT,metaMirror = mirrorMetaNode)    
#         self.__pointerClass = LimbModule(baseNameT,sideT,size = cntSizeV,solver = solverV,
#                                          metaSpine = spineMetaNode,metaMain = mainMetaNode,mirror = mirrorC)                
        
        return self.__pointerClass
    
    def __clusLoc(self,*arg):
        
        '''create a clus base on edges'''
        sideR = pm.radioButtonGrp(self.sideR,q = True,sl = True)
        
        if sideR == 1:
            sideT = 'l'
        elif sideR == 2:
            sideT = 'r'    
            
        cntSizeV = pm.floatFieldGrp(self.cntSize,q = 1,value1 = 1)
        baseNameT = pm.textFieldGrp(self.baseNameT,q = 1,text = 1)

        #sl edges
        edges = pm.selected(flatten = True)
        #convert to edges
        verts = list(set(sum([list(e.connectedVertices()) for e in edges],[])))

        #create clus
        clusShp,clusTras = pm.cluster(verts)
          
        helpCtrl = control.Control(side = sideT,baseName = baseNameT + 'Pos',size = cntSizeV)
        helpCtrl.solidSphereCtrl()
        pcn = pm.pointConstraint(clusTras,helpCtrl.controlGrp, mo = False)
        pm.delete(pcn)
        pm.delete(clusTras)    
