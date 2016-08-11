import pymel.core as pm
from Modules.subModules import fkChain,ikChain,boneChain,ribbon
from Utils import nameUtils,metaUtils
from Modules import control,hierarchy,toolModule
from maya import OpenMaya

class LegModule(object):
    
    posHipArray = [[0.772,9.957,0],[0.772,9.008,0]]
    rotHipArray = [[0,0,0],[0,0,0]]
    posLegArray = [[0.772,9.008,0],[0.772,4.8,0.258],[0.772,1,-0.411],[0.772,0,-1.1],[0.772,0,1.8],[0.443,0,0.584],[1.665,0,0.584],[0.772,0,0.584]]
    rotLegArray = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    posSplitLegArray = [[0.772,5.1,0.258],[0.772,4.5,0.258]]
    rotSplitLegArray = [[0,0,0],[0,0,0]]
    
    def __init__(self,baseName = 'leg',side = 'l',size = 1.5,
                 controlOrient = [0,0,0],metaMain = None,metaSpine = None,
                 twist = None,split = None,upperTwistNum = None,
                 lowerTwistNum = None,mirror = None,metaMirror = None):
        
        self.baseName = baseName
        self.side = side
        self.size = size
        self.controlOrient = controlOrient
        self.twist = twist
        self.split = split
        self.upperTwistNum = upperTwistNum 
        self.lowerTwistNum = lowerTwistNum
        self.mirror = mirror
        
        '''
        self para
        '''
        
        #jj 
        self.ikRpPvChain = None
        self.ikRpChain = None
        self.ikBlendChain = None
        self.fkChain = None
        self.legBlendChain = None
        self.hipChain = None
        self.blendData = None   
        self.legGrp = None
        self.upperJointLentgh = None
        self.lowerJointLentgh = None        
        
        #cc
        self.footSettingCtrl = None
        self.hipCtrl = None
        self.ccDefGrp = None
        self.cntsGrp = None
        
        #guide
        self.hipGuides = None
        self.legGuides = None
        self.splitLegGuides = None
        self.guideGrp = None
        
        #ribon
        self.ribon = None
        self.ribon45hp = None 
        self.subMidCtrlThighKnee = None
        self.subMidCtrlKneeAnkle = None
        self.subMidCtrlKnee = None
        
        #Hook
        self.__tempSpaceSwitch = None
        self.locLocal = None
        self.locWorld = None
        self.hookData = {}
        
        #name list 
        self.ribbonData = ['ThighKnee','KneeAnkle','Knee']
        self.splitLegNameList = ['splitLegUp','splitLegDown']
        self.legNameList = ['Thigh','Knee','Ankle','Heel','Toe','Inside','Outside','Ball']
        self.footNameList = ['Thigh','Knee','Ankle','Ball','Toe','Heel']       
        
        #metanode
        self.meta = metaUtils.createMeta(self.side,self.baseName,0)
        self.metaMain = metaMain 
        self.metaSpine = metaSpine
        self.metaMirror = metaMirror
        
    def buildGuides(self):
        
        self.legGuides = []
        self.hipGuides = []       
        
        #hipGuides
        #set pos loc    
        for i,p in enumerate(self.posHipArray):
            name = nameUtils.getUniqueName(self.side,'hip','gud')
            loc = pm.spaceLocator(n = name)
            loc.t.set(p)
            loc.r.set(self.rotHipArray[i])
            loc.localScale.set(self.size,self.size,self.size)
            self.hipGuides.append(loc)
            
        tempHipGuides = list(self.hipGuides)
        tempHipGuides.reverse()        
      
        #legGuides
        #set pos loc    
        for i,p in enumerate(self.posLegArray):
            name = nameUtils.getUniqueName(self.side,self.legNameList[i],'gud')
            loc = pm.spaceLocator(n = name)
            loc.t.set(p)
            loc.r.set(self.rotLegArray[i])
            loc.localScale.set(self.size,self.size,self.size)
            self.legGuides.append(loc)
            
        tempLegGuides = list(self.legGuides)
        tempLegGuides.reverse()
        
        ###
        #split
        if self.split == 1:            
            self.splitLegGuides = []
            #splitLegGuides
            #set pos loc    
            for i,p in enumerate(self.posSplitLegArray):
                name = nameUtils.getUniqueName(self.side,self.splitLegNameList[i],'gud')
                loc = pm.spaceLocator(n = name)
                loc.t.set(p)
                loc.r.set(self.rotLegArray[i])
                self.splitLegGuides.append(loc)
        
        ###
        #mirror
        if self.mirror == 'yes':
            
            mirrorMetaNode = pm.ls(self.metaMirror)[0]            
            leftGuideLocMetaList = pm.connectionInfo(mirrorMetaNode.guideLocator, destinationFromSource=True)

            for guideLoc in leftGuideLocMetaList:
                destnation = guideLoc.split('_')
                #hip
                if str(destnation[1]) + str(destnation[2]) == 'hip0':
                    hipZeroLocStr = guideLoc.split('.')[0]
                    pm.select(hipZeroLocStr)
                    hipZeroLoc = pm.ls(sl = 1)[0]
                    
                elif str(destnation[1]) + str(destnation[2]) == 'hip1':
                    hipOneLocStr = guideLoc.split('.')[0]
                    pm.select(hipOneLocStr)
                    hipOneLoc = pm.ls(sl = 1)[0]               
                
                #leg
                elif str(destnation[1]) + str(destnation[2]) == 'legikNFStretchStart':
                    thighLocStr = guideLoc.split('.')[0]
                    pm.select(thighLocStr)
                    thighLoc = pm.ls(sl = 1)[0]
                     
                elif str(destnation[1]) == 'Knee':
                    kneeLocStr = guideLoc.split('.')[0]
                    pm.select(kneeLocStr)
                    kneeLoc = pm.ls(sl = 1)[0] 
                    
                elif str(destnation[1]) + str(destnation[2]) == 'legikNFStretchEnd':
                    clafLocStr = guideLoc.split('.')[0]
                    pm.select(clafLocStr)
                    clafLoc = pm.ls(sl = 1)[0] 
                    
                elif str(destnation[1]) == 'Heel':
                    heelLocStr = guideLoc.split('.')[0]
                    pm.select(heelLocStr)
                    heelLoc = pm.ls(sl = 1)[0]  
                    
                elif str(destnation[1]) == 'Toe':
                    toeLocStr = guideLoc.split('.')[0]
                    pm.select(toeLocStr)
                    toeLoc = pm.ls(sl = 1)[0]    
                    
                elif str(destnation[1]) == 'Inside':
                    insideLocStr = guideLoc.split('.')[0]
                    pm.select(insideLocStr)
                    insideLoc = pm.ls(sl = 1)[0]  
                    
                elif str(destnation[1]) == 'Outside':
                    outsideLocStr = guideLoc.split('.')[0]
                    pm.select(outsideLocStr)
                    outsideLoc = pm.ls(sl = 1)[0]    
                
                elif str(destnation[1]) == 'Ball':
                    ballLocStr = guideLoc.split('.')[0]
                    pm.select(ballLocStr)
                    ballLoc = pm.ls(sl = 1)[0]   
                            
                #split knee    
                elif str(destnation[1]) == 'splitLegUp':
                    splitLegUpLocStr = guideLoc.split('.')[0]
                    pm.select(splitLegUpLocStr)
                    splitLegUpLoc = pm.ls(sl = 1)[0]  
                    
                elif str(destnation[1]) == 'splitLegDown':
                    splitLegDownLocStr = guideLoc.split('.')[0]
                    pm.select(splitLegDownLocStr)
                    splitLegDownLoc = pm.ls(sl = 1)[0]    
                                    
            #hip
            hipZeroLocPos = hipZeroLoc.getTranslation(space = 'world')
            hipZeroLocRot = hipZeroLoc.getRotation(space = 'world')
            self.hipGuides[0].t.set(-hipZeroLocPos[0],hipZeroLocPos[1],hipZeroLocPos[2])         
            self.hipGuides[0].r.set(hipZeroLocRot[0],-hipZeroLocRot[1],-hipZeroLocRot[2])   
            
            hipOneLocPos = hipOneLoc.getTranslation(space = 'world')
            hipOneLocRot = hipOneLoc.getRotation(space = 'world')
            self.hipGuides[1].t.set(-hipOneLocPos[0],hipOneLocPos[1],hipOneLocPos[2])         
            self.hipGuides[1].r.set(hipOneLocRot[0],-hipOneLocRot[1],-hipOneLocRot[2])
            
            #leg
            thighLocPos = thighLoc.getTranslation(space = 'world')
            thighLocRot = thighLoc.getRotation(space = 'world')
            self.legGuides[0].t.set(-thighLocPos[0],thighLocPos[1],thighLocPos[2])         
            self.legGuides[0].r.set(thighLocRot[0],-thighLocRot[1],-thighLocRot[2])   
            
            kneeLocPos = kneeLoc.getTranslation(space = 'world')
            kneeLocRot = kneeLoc.getRotation(space = 'world')
            self.legGuides[1].t.set(-kneeLocPos[0],kneeLocPos[1],kneeLocPos[2])         
            self.legGuides[1].r.set(kneeLocRot[0],-kneeLocRot[1],-kneeLocRot[2])
            
            ankleLocPos = clafLoc.getTranslation(space = 'world')
            ankleLocRot = clafLoc.getRotation(space = 'world')
            self.legGuides[2].t.set(-ankleLocPos[0],ankleLocPos[1],ankleLocPos[2])
            self.legGuides[2].r.set(ankleLocRot[0],-ankleLocRot[1],-ankleLocRot[2])
            
            heelLocPos = heelLoc.getTranslation(space = 'world')
            heelLocRot = heelLoc.getRotation(space = 'world')
            self.legGuides[3].t.set(-heelLocPos[0],heelLocPos[1],heelLocPos[2])         
            self.legGuides[3].r.set(heelLocRot[0],-heelLocRot[1],-heelLocRot[2])
            
            toeLocPos = toeLoc.getTranslation(space = 'world')
            toeLocRot = toeLoc.getRotation(space = 'world')
            self.legGuides[4].t.set(-toeLocPos[0],toeLocPos[1],toeLocPos[2])         
            self.legGuides[4].r.set(toeLocRot[0],-toeLocRot[1],-toeLocRot[2])   
            
            insideLocPos = insideLoc.getTranslation(space = 'world')
            insideLocRot = insideLoc.getRotation(space = 'world')
            self.legGuides[5].t.set(-insideLocPos[0],insideLocPos[1],insideLocPos[2])         
            self.legGuides[5].r.set(insideLocRot[0],-insideLocRot[1],-insideLocRot[2])
            
            outsideLocPos = outsideLoc.getTranslation(space = 'world')
            outsideLocRot = outsideLoc.getRotation(space = 'world')
            self.legGuides[6].t.set(-outsideLocPos[0],outsideLocPos[1],outsideLocPos[2])         
            self.legGuides[6].r.set(outsideLocRot[0],-outsideLocRot[1],-outsideLocRot[2])
            
            ballLocPos = ballLoc.getTranslation(space = 'world')
            ballLocRot = ballLoc.getRotation(space = 'world')
            self.legGuides[7].t.set(-ballLocPos[0],ballLocPos[1],ballLocPos[2])         
            self.legGuides[7].r.set(ballLocRot[0],-ballLocRot[1],-ballLocRot[2])
            
            #split                 
            if self.split == 1:
                splitLegUpLocPos = splitLegUpLoc.getTranslation(space = 'world')
                splitLegUpLocRot = splitLegUpLoc.getRotation(space = 'world')
                self.splitLegGuides[0].t.set(-splitLegUpLocPos[0],splitLegUpLocPos[1],splitLegUpLocPos[2])         
                self.splitLegGuides[0].r.set(splitLegUpLocRot[0],-splitLegUpLocRot[1],-splitLegUpLocRot[2])
                
                splitLegDownLocPos = splitLegDownLoc.getTranslation(space = 'world')
                splitLegDownLocRot = splitLegDownLoc.getRotation(space = 'world')
                self.splitLegGuides[1].t.set(-splitLegDownLocPos[0],splitLegDownLocPos[1],splitLegDownLocPos[2])         
                self.splitLegGuides[1].r.set(splitLegDownLocRot[0],-splitLegDownLocRot[1],-splitLegDownLocRot[2])
        #regroup
        #set hip loc grp
        for i in range(len(tempHipGuides)):
            if i != (len(tempHipGuides) - 1):
                pm.parent(tempHipGuides[i],tempHipGuides[i + 1])
        
        #set leg loc grp
        for i in range(len(tempLegGuides)):
            if i != (len(tempLegGuides) - 1):
                pm.parent(tempLegGuides[i],tempLegGuides[i + 1])
        
        ###
        #split    
        if self.split == 1:
            #set loc grp
            pm.parent(self.splitLegGuides[1],self.splitLegGuides[0])
            self.splitLegGuides.reverse()
            
            self.splitLegGuides[1].setParent(self.legGuides[1])
            self.splitLegGuides.reverse()
        
        #mirror
        if self.mirror == 'no':
            
            for hipGuide in self.hipGuides:
                oriTx = hipGuide.tx.get()
                oriTy = hipGuide.ty.get()
                oriTz = hipGuide.tz.get()
                hipGuide.t.set(self.size * oriTx,self.size * oriTy,self.size * oriTz)
                
            for legGuide in self.legGuides:
                oriTx = legGuide.tx.get()
                oriTy = legGuide.ty.get()
                oriTz = legGuide.tz.get()
                legGuide.t.set(self.size * oriTx,self.size * oriTy,self.size * oriTz)                   
        
        #clean up
        guideGrpName = nameUtils.getUniqueName(self.side,self.baseName + '_Gud','grp')
        self.guideGrp = pm.group(em = 1,n = guideGrpName)
        
        self.hipGuides[0].setParent(self.guideGrp)  
        self.legGuides[0].setParent(self.guideGrp)
            
    def build(self):
                
        ###        
        #mirror        
        self.mirrorGuideGrp = pm.group(em = 1,n = nameUtils.getUniqueName(self.side,self.baseName + '_Gud','grp'))
        self.mirrorGuideList = []
        self.mirrorGuideGrp.v.set(0)
        
        for hipGuide in self.hipGuides:
            mirrorHipGuide = pm.duplicate(hipGuide)
            child = pm.listRelatives(mirrorHipGuide,c = 1,typ = 'transform')
            if child != None:
                pm.delete(child)
            newName = str(hipGuide) + 'Mirror' 
            renameGuide = pm.rename(mirrorHipGuide,newName)
            mirrorHipGuide[0].setParent(self.mirrorGuideGrp)
            self.mirrorGuideList.append(renameGuide)
        
        for legGuide in self.legGuides:
            mirrorLegGuide = pm.duplicate(legGuide)
            child = pm.listRelatives(mirrorLegGuide,c = 1,typ = 'transform')
            if child != None:
                pm.delete(child)
            newName = str(legGuide) + 'Mirror' 
            renameGuide = pm.rename(mirrorLegGuide,newName)
            mirrorLegGuide[0].setParent(self.mirrorGuideGrp)
            self.mirrorGuideList.append(renameGuide)

        ###split     
        if self.split == 1:                
            for splitLegGuide in self.splitLegGuides:
                mirrorSplitLegGuide = pm.duplicate(splitLegGuide)
                child = pm.listRelatives(mirrorSplitLegGuide,c = 1,typ = 'transform')
                if child != None:
                    pm.delete(child)
#                 self.mirrorGuideList.append(mirrorSplitLegGuide)
                newName = str(splitLegGuide) + 'Mirror' 
                renameGuide = pm.rename(mirrorSplitLegGuide,newName)
                renameGuide.setParent(self.mirrorGuideGrp)
                self.mirrorGuideList.append(renameGuide)
                
        #really ro roll            
        self.guideGrp.v.set(0)
        ###pos
        #create hip pos
        self.hipGuidesPos = [x.getTranslation(space = 'world') for x in self.hipGuides]
        self.hipGuidesRot = [x.getRotation(space = 'world') for x in self.hipGuides]
        
        self.hipChain = boneChain.BoneChain('hip',self.side,type = 'jj')
        self.hipChain.fromList(self.hipGuidesPos,self.hipGuidesRot) 
        pm.rename(self.hipChain.chain[-1],nameUtils.getUniqueName(self.side,'hip','je')) 
        
        #create leg pos
        self.legGuidesPos = [x.getTranslation(space = 'world') for x in self.legGuides]
        self.legGuidesRot = [x.getRotation(space = 'world') for x in self.legGuides]
        
        footPos = []
        footPos.append(self.legGuidesPos[-1])        
        footPos.append(self.legGuidesPos[4])
        footPos.append(self.legGuidesPos[3])
        
        #split
        if self.split == 1:
            #split pos
            self.splitKneePos = []
            self.splitKneePos.append(self.legGuidesPos[1])
            for splitLegGuide in self.splitLegGuides:
                splitLegGuidePos = splitLegGuide.getTranslation(space = 'world')
                self.splitKneePos.append(splitLegGuidePos)                
            
            #split rot
            self.splitKneeRot = []
            self.splitKneeRot.append(self.legGuidesPos[1])
            for splitLegGuide in self.splitLegGuides:
                splitLegGuideRot = splitLegGuide.getRotation(space = 'world')
                self.splitKneeRot.append(splitLegGuidePos)  
            
            #real pos
            #up
            self.splitLegUpPos = []
            self.splitLegUpPos.append(self.legGuidesPos[0])
            self.splitLegUpPos.append(self.splitKneePos[1])

            self.splitLegUpRot = []
            self.splitLegUpRot.append(self.legGuidesRot[0])
            self.splitLegUpRot.append(self.splitKneeRot[1])
            
            #down
            self.splitLegDownPos = []
            self.splitLegDownPos.append(self.splitKneePos[2])
            self.splitLegDownPos.append(self.legGuidesPos[2])
            
            self.splitLegDownRot = []
            self.splitLegDownRot.append(self.splitKneeRot[2])
            self.splitLegDownRot.append(self.legGuidesRot[2])
                        
        ###create joint
        #addBlendCtrl 
        self.footSettingCtrl = control.Control(self.side,self.baseName + 'Settings',self.size) 
        self.footSettingCtrl.ikfkBlender()
        
        #ikRpPvChain
        self.ikRpPvChain = ikChain.IkChain(self.baseName,self.side,self.size,solver = 'ikRPsolver')
        self.ikRpPvChain.fromList(self.legGuidesPos[0:3],self.legGuidesRot)
        for num,joint in enumerate(self.ikRpPvChain.chain):
            name = nameUtils.getUniqueName(self.side,self.footNameList[num],'ikRP')
            pm.rename(joint,name)
   
        #ikRpChain
        self.ikRpChain = ikChain.IkChain(self.baseName,self.side,self.size,solver = 'ikRPsolver',noFlip = 1)
        self.ikRpChain.fromList(self.legGuidesPos[0:3],self.legGuidesRot)
        for num,joint in enumerate(self.ikRpChain.chain):
            name = nameUtils.getUniqueName(self.side,self.footNameList[num],'ikNF')
            pm.rename(joint,name)
           
        #ik blend 
        self.ikBlendChain = boneChain.BoneChain(self.baseName,self.side,type = 'ik')
        self.ikBlendChain.fromList(self.legGuidesPos[0:3] + footPos,self.legGuidesRot)
        self.ikBlendChainData = boneChain.BoneChain.blendTwoChains(self.ikRpChain.chain,self.ikRpPvChain.chain,self.ikBlendChain.chain[0:3],
                                                                   self.ikRpPvChain.ikCtrl.control,'enable_PV',self.baseName,self.side)
        for num,joint in enumerate(self.ikBlendChain.chain):
            name = nameUtils.getUniqueName(self.side,self.footNameList[num],'ik')
            pm.rename(joint,name)
             
        #fk 
        self.fkChain = fkChain.FkChain(self.baseName,self.side,self.size)
        self.fkChain.fromList(self.legGuidesPos[0:3] + footPos,self.legGuidesRot)
        for num,joint in enumerate(self.fkChain.chain):
            name = nameUtils.getUniqueName(self.side,self.footNameList[num],'fk')
            pm.rename(joint,name)
        pm.delete(self.fkChain.chain[4].getShape())
         
        #ori chain
        self.legBlendChain = boneChain.BoneChain(self.baseName,self.side,type = 'jc')
        self.legBlendChain.fromList(self.legGuidesPos[0:3] + footPos,self.legGuidesRot)
        self.ikBlendChainData = boneChain.BoneChain.blendTwoChains(self.fkChain.chain,self.ikBlendChain.chain,self.legBlendChain.chain,
                                                                   self.footSettingCtrl.control,'IKFK',self.baseName,self.side)
        for num,joint in enumerate(self.legBlendChain.chain):
            name = nameUtils.getUniqueName(self.side,self.footNameList[num],'jc')
            pm.rename(joint,name)    
             
        #self.footNameList = ['Thigh','Knee','Ankle','Ball','Toe','Heel']       
        pm.rename(self.legBlendChain.chain[-4],nameUtils.getUniqueName(self.side,self.footNameList[-4],'jj'))
        pm.rename(self.legBlendChain.chain[-3],nameUtils.getUniqueName(self.side,self.footNameList[-3],'jj'))
        pm.rename(self.legBlendChain.chain[-2],nameUtils.getUniqueName(self.side,self.footNameList[-2],'je'))
        pm.rename(self.legBlendChain.chain[-1],nameUtils.getUniqueName(self.side,self.footNameList[-1],'je'))
          
        self.ikBlendChain.chain[-1].setParent(self.ikBlendChain.chain[-4])
        self.fkChain.chain[-1].setParent(self.fkChain.chain[-4])
        self.legBlendChain.chain[-1].setParent(self.legBlendChain.chain[-4])
         
        if self.split == 1:
             
            self.splitKneeChain = boneChain.BoneChain('splitKnee',self.side,type = 'jc')
            self.splitKneeChain.fromList(self.splitKneePos,self.splitKneeRot)
             
            self.splitLegUpChain = boneChain.BoneChain(self.splitLegNameList[0],self.side,type = 'jc')
            self.splitLegUpChain.fromList(self.splitLegUpPos,self.splitLegUpRot)
             
            self.splitLegDownChain = boneChain.BoneChain(self.splitLegNameList[1],self.side,type = 'jc')
            self.splitLegDownChain.fromList(self.splitLegDownPos,self.splitLegDownRot)
             
            self.__splitJointSet()
         
        #hip set
        self.__hipSet()
         
        #leg ikfk switcher set
        self.__ikSet()
        self.__ikfkBlendSet()
         
        #leg set        
        if self.twist == 'ribon45hp': 
            self.__ribonSetUp()
         
        if self.twist == 'non_roll':
            self.__nonRollSetUp()            
         
        #foot set
        self.__editCtrl()
        self.__ikFootSet() 
        self.__cleanUp()
         
        #final hook
        self.__buildHooks()
        
    def __hipSet(self):
        
        #create hip cc
        self.hipCtrl = control.Control(self.side,'hipSettings',self.size)
        self.hipCtrl.plusCtrl()
        
        #align cc
        #getpos
        hipPos = self.hipChain.chain[0].getTranslation(space = 'world')
        pm.xform(self.hipCtrl.controlGrp,ws = 1,matrix = self.hipChain.chain[0].worldMatrix.get())
        
        if self.side == 'l':
            pm.move(hipPos[0] + self.hipChain.chain[1].tx.get(),hipPos[1],hipPos[2],self.hipCtrl.controlGrp)
            
        elif self.side == 'r':
            pm.move(hipPos[0] - self.hipChain.chain[1].tx.get(),hipPos[1],hipPos[2],self.hipCtrl.controlGrp)
            
        pm.move(hipPos[0],hipPos[1],hipPos[2],self.hipCtrl.control + '.rotatePivot')      
        pm.move(hipPos[0],hipPos[1],hipPos[2],self.hipCtrl.control + '.scalePivot')      
        self.hipChain.chain[0].setParent(self.hipCtrl.control)
        
    def __ikSet(self):
        
        #stretch loc reset
        self.ikRpChain.stretchEndLoc.setParent(self.ikRpPvChain.ikCtrl.control)
        
        #reset ik cc
        pm.delete(self.ikRpChain.ikCtrl.controlGrp)
        
        #connect joint stretch
        self.ikRpPvChain.ikCtrl.control.stretch.connect(self.ikRpChain.stretchBlendcolorNode.blender)
        
        #connect ik handle point cnst
#         pm.pointConstraint(self.ikRpPvChain.ikCtrl.control,self.ikRpChain.ikHandle,w = 1)
        
        #rename ikRPcc
        pm.rename(self.ikRpPvChain.ikCtrl.control,nameUtils.getUniqueName(self.side,self.baseName + 'ik','cc'))
        pm.rename(self.ikRpPvChain.ikCtrl.controlGrp,nameUtils.getUniqueName(self.side,self.baseName + 'ik','grp'))        
        
        #set ik flip
        self.ikRpChain.ikHandle.poleVectorX.set(-0.1)
        self.ikRpChain.ikHandle.poleVectorY.set(0)
        self.ikRpChain.ikHandle.poleVectorZ.set(0)
        
        
        PMAName = nameUtils.getUniqueName(self.side,self.baseName + '_noFlip','PMA')
        pm.addAttr(self.ikRpPvChain.ikCtrl.control, ln = 'knee_twist', at ="float",dv = 0,h = False,k = True )
#         control.addFloatAttr(self.ikRpPvChain.ikCtrl.control,['up_twist'],-90,90)
        pm.addAttr(self.ikRpPvChain.ikCtrl.control, ln = 'knee_offset', at ="float",dv = 0,h = False,k = True )
        plusMinusAverageNode = pm.createNode('plusMinusAverage',n = PMAName)
        
        flipTwistDefaultV = self.legGuides[0].ry.get() 
        self.ikRpPvChain.ikCtrl.control.knee_offset.connect(plusMinusAverageNode.input1D[0])
        self.ikRpPvChain.ikCtrl.control.knee_twist.connect(plusMinusAverageNode.input1D[1])                
        plusMinusAverageNode.output1D.connect(self.ikRpChain.ikHandle.twist)
        self.ikRpPvChain.ikCtrl.control.knee_offset.set(float(-90 - flipTwistDefaultV))
        self.ikRpPvChain.ikCtrl.control.knee_offset.lock(1)
        
        #add ik pv vis
        self.ikRpPvChain.ikCtrl.control.enable_PV.connect(self.ikRpPvChain.poleVectorCtrl.controlGrp.v)
        self.ikRpChain.ikHandle.v.set(0)
        self.ikRpChain.stretchStartLoc.v.set(0)
        self.ikRpPvChain.stretchStartLoc.v.set(0)  
        self.ikRpPvChain.ikCtrl.control.enable_PV.connect(self.ikRpPvChain.ikBeamCurve.v)
    
    def __ikfkBlendSet(self):
    
        #connect visable function
        #create node 
        reverseNodeName = nameUtils.getUniqueName(self.side,self.baseName + 'IKFK','REV')
        reverseNode = pm.createNode('reverse',n = reverseNodeName)
        
        #connecct node 
        self.footSettingCtrl.control.IKFK.connect(self.ikRpPvChain.ikCtrl.controlGrp.v)
        self.footSettingCtrl.control.IKFK.connect(self.footSettingCtrl.textObj[1].v)
        self.footSettingCtrl.control.IKFK.connect(reverseNode.inputX)
        reverseNode.outputX.connect(self.fkChain.chain[0].v)
        reverseNode.outputX.connect(self.footSettingCtrl.textObj[0].v)
        self.footSettingCtrl.controlGrp.sx.set(self.size / 2)
        self.footSettingCtrl.controlGrp.sy.set(self.size / 2)
        self.footSettingCtrl.controlGrp.sz.set(self.size / 2)
        pm.makeIdentity(self.footSettingCtrl.controlGrp,apply = True,t = 0,r = 0,s = 1,n = 0,pn = 1)
        
        #hide fk Chain vis
        for jointChain in self.fkChain.chain:
            control.lockAndHideAttr(jointChain,['v','radius'])
        
        #set pos
        pm.xform(self.footSettingCtrl.controlGrp,ws = 1,matrix = self.legBlendChain.chain[2].worldMatrix.get())
        self.footSettingCtrl.controlGrp.rx.set(0)
        self.footSettingCtrl.controlGrp.ry.set(0)
        self.footSettingCtrl.controlGrp.rz.set(0)
        pm.move(self.legGuidesPos[2][0],self.legGuidesPos[2][1],self.legGuidesPos[4][2],self.footSettingCtrl.controlGrp)
        ankle_pos = pm.xform(self.legBlendChain.chain[2],query=1,ws=1,rp=1)
        pm.move(ankle_pos[0],ankle_pos[1],ankle_pos[2],self.footSettingCtrl.controlGrp + '.rotatePivot')
        pm.move(ankle_pos[0],ankle_pos[1],ankle_pos[2],self.footSettingCtrl.controlGrp + '.scalePivot')
        pm.pointConstraint(self.legBlendChain.chain[2],self.footSettingCtrl.controlGrp,mo = 1)
#         pm.orientConstraint(self.legBlendChain.chain[2],self.footSettingCtrl.controlGrp,mo = 1)
        control.lockAndHideAttr(self.footSettingCtrl.control,['tx','ty','tz','rx','ry','rz','sx','sy','sz','v'])
        
        if self.twist == 'non_roll':
            control.addFloatAttr(self.footSettingCtrl.control,['proxy_vis'],0,1) 
      
    def __splitJointSet(self):
        
        self.splitKneeChain.chain[0].setParent(self.legBlendChain.chain[0])
        
        #create node
        #pos
        splitPosMDNodeName = nameUtils.getUniqueName(self.side,'splitKneePos','MDN')
        splitPosMDNode = pm.createNode('multiplyDivide',n = splitPosMDNodeName)
          
        #connect
        self.legBlendChain.chain[1].tx.connect(splitPosMDNode.input1X)
        self.legBlendChain.chain[1].ty.connect(splitPosMDNode.input1Y)
        self.legBlendChain.chain[1].tz.connect(splitPosMDNode.input1Z)
          
        splitPosMDNode.outputX.connect(self.splitKneeChain.chain[0].tx)
        splitPosMDNode.outputY.connect(self.splitKneeChain.chain[0].ty)
        splitPosMDNode.outputZ.connect(self.splitKneeChain.chain[0].tz)        
                
        #rot
        splitRotMDNodeName = nameUtils.getUniqueName(self.side,'splitKneeRot','MDN')
        splitRotMDNode = pm.createNode('multiplyDivide',n = splitRotMDNodeName)
         
        #connect
        self.legBlendChain.chain[1].rx.connect(splitRotMDNode.input1X)
        self.legBlendChain.chain[1].ry.connect(splitRotMDNode.input1Y)
        self.legBlendChain.chain[1].rz.connect(splitRotMDNode.input1Z)
        
        splitRotMDNode.input2X.set(-0.5)
        splitRotMDNode.input2Y.set(1)
        splitRotMDNode.input2Z.set(-0.5)
         
        splitRotMDNode.outputX.connect(self.splitKneeChain.chain[0].rx)
        splitRotMDNode.outputY.connect(self.splitKneeChain.chain[0].ry)
        splitRotMDNode.outputZ.connect(self.splitKneeChain.chain[0].rz)
        
        #ik handle
        upIkName = nameUtils.getUniqueName(self.side,'upSplit','iks')
        self.upSplitIkHandle,self.upSplitIkEffector = pm.ikHandle(sj = self.splitLegUpChain.chain[0],ee = self.splitLegUpChain.chain[1],solver = 'ikSCsolver',n = upIkName)
        
        downIkName = nameUtils.getUniqueName(self.side,'downSplit','iks')
        self.downSplitIkHandle,self.downSplitIkEffector = pm.ikHandle(sj = self.splitLegDownChain.chain[0],ee = self.splitLegDownChain.chain[1],solver = 'ikSCsolver',n = downIkName)
        
        #cleanUp
        #ik
        self.upSplitIkHandle.setParent(self.splitKneeChain.chain[1])
        self.downSplitIkHandle.setParent(self.legBlendChain.chain[2])
        self.upSplitIkHandle.v.set(0)
        self.downSplitIkHandle.v.set(0)
        
        #joint
        self.splitLegUpChain.chain[0].setParent(self.legBlendChain.chain[0])
        self.splitLegDownChain.chain[0].setParent(self.splitKneeChain.chain[2])        
        
    def __ribonSetUp(self):
        
        self.__setRibbonUpper()
        self.__setRibbonLower()
        self.__setRibbonSubMidCc()
  
    def __nonRollSetUp(self):
        
        if self.split == 0:
            
            #thigh:
            #create twist Leg 
            self.thighTwistStart = pm.duplicate(self.legBlendChain.chain[0],
                                                n = nameUtils.getUniqueName(self.side,'thighTwistS','jj')) 
            self.thighTwistEnd = pm.listRelatives(self.thighTwistStart,c = 1,typ = 'joint')
            
            tempJoint = pm.listRelatives(self.thighTwistEnd,c = 1,typ = 'joint')
            pm.delete(tempJoint)
            pm.rename(self.thighTwistEnd,nameUtils.getUniqueName(self.side,'thighTwistE','jj'))
             
            self.thighTwistJoint = toolModule.SplitJoint(self.thighTwistStart,self.upperTwistNum,box = 1,type = 'tool',size = self.size) 
            self.thighTwistJoint.splitJointTool()
            
            for cube in self.thighTwistJoint.cubeList:
                self.footSettingCtrl.control.proxy_vis.connect(cube[0].v)
             
            for twistJoints in self.thighTwistJoint.joints:
                pm.rename(twistJoints, nameUtils.getUniqueName(self.side,'thighTwist','jj'))  
                 
            #create iks
            thighTwistIkName = nameUtils.getUniqueName(self.side,'thighTwist','iks')  
            thighTwistIkCurveName = nameUtils.getUniqueName(self.side,'thighTwist','ikc')  
            self.thighTwistIk,self.thighTwistIkEffector,self.thighTwistIkCurve = pm.ikHandle(sj = self.thighTwistStart[0],
                                                                                             ee = self.thighTwistEnd[0],
                                                                                             solver = 'ikSplineSolver',
                                                                                             n = thighTwistIkName)
            upperSpIkC = pm.skinCluster(self.legBlendChain.chain[0],self.legBlendChain.chain[1],self.thighTwistIkCurve,
                                       n = nameUtils.getSkinName())
            self.thighTwistIkCurve.v.set(0)
            pm.rename(self.thighTwistIkCurve,thighTwistIkCurveName)
            self.thighTwistIk.poleVector.set(0,0,0)
            
            
            #set stretch
            #get last cv:
            pm.select(self.thighTwistIkCurve + '.cv[*]')
            upperIkCLastCv = pm.ls(sl = 1)[0][-1]
            pm.skinPercent(upperSpIkC,upperIkCLastCv,tv = [(self.legBlendChain.chain[1],1)])
             
            #get cv length
            thighTwistIkCurveInfoName = nameUtils.getUniqueName(self.side,'thighTwist','cvINFO')
            thighTwistIkCurveInfoNode = pm.createNode('curveInfo',n = thighTwistIkCurveInfoName)
            self.thighTwistIkCurve.getShape().worldSpace[0].connect(thighTwistIkCurveInfoNode.inputCurve)
             
            #create main Node
            thighTwistCurveMDNName = nameUtils.getUniqueName(self.side,'thighTwistCur','MDN')
            thighTwistCurveMDNNode = pm.createNode('multiplyDivide',n = thighTwistCurveMDNName)
             
            thighTwistIkCurveInfoNode.arcLength.connect(thighTwistCurveMDNNode.input1.input1X)
            thighTwistCurveMDNNode.input2.input2X.set(self.legBlendChain.chain[1].tx.get())
            thighTwistCurveMDNNode.operation.set(2)
             
            for num,twistJoints in enumerate(self.thighTwistJoint.joints):
                tempNodeName = nameUtils.getUniqueName(self.side,'thighTwistJnt','MDN')
                tempNode = pm.createNode('multiplyDivide',n = tempNodeName)
                if num > 0 :
                    tempNode.input1.input1X.set(twistJoints.tx.get())
                    thighTwistCurveMDNNode.outputX.connect(tempNode.input2.input2X)
                    tempNode.outputX.connect(twistJoints.tx)
             
            #create upperTwistGrp
            thighTwistGrpName = nameUtils.getUniqueName(self.side,'thighTwist','grp')
            self.thighTwistGrp = pm.group(em = 1,n = thighTwistGrpName) 
            self.thighTwistIk.setParent(self.thighTwistGrp) 
            self.thighTwistIkCurve.setParent(self.thighTwistGrp) 
             
            #create upperTwistInfoGrp 
            twistInfoGrpName = nameUtils.getUniqueName(self.side,'thighTwistInfo','grp')
            self.thighTwistInfoGrp = pm.group(em = 1,n = twistInfoGrpName)
             
            #nonFlip Jnt
            nonFlipStJnt = pm.duplicate(self.legBlendChain.chain[1],
                                        n = nameUtils.getUniqueName(self.side,'thighNonFlip','jc'))
            nonFlipEdJnt = pm.listRelatives(nonFlipStJnt,c = 1,typ = 'joint')
            tempTrashJnt = pm.listRelatives(nonFlipEdJnt,c = 1,typ = 'joint')
            pm.delete(tempTrashJnt)
            pm.rename(nonFlipEdJnt,nameUtils.getUniqueName(self.side,self.baseName + 'thighNonFlip','je'))
            nonFlipStJnt[0].setParent(self.thighTwistInfoGrp)
            nonFlipIks,nonFlipIksEffector = pm.ikHandle(sj = nonFlipStJnt[0],ee = nonFlipEdJnt[0],solver = 'ikRPsolver',
                                                        n = nameUtils.getUniqueName(self.side,'thighNonFlip','iks'))
            nonFlipIks.setParent(self.legBlendChain.chain[1])
            nonFlipIks.poleVector.set(0,0,0)
            nonFlipIks.r.set(0,0,0)
            nonFlipIks.v.set(0)
            pm.pointConstraint(self.legBlendChain.chain[1],nonFlipStJnt,mo = 1)
             
            #twist info jnt
            twistInfoJnt = pm.joint(n = nameUtils.getUniqueName(self.side,'thighTwistInfo','jc'))
            twistInfoJnt.setParent(nonFlipStJnt)
            twistInfoJnt.t.set(0,0,0)
            pm.aimConstraint(nonFlipEdJnt[0],twistInfoJnt,mo = 1,w = 1,aimVector = [1,0,0],upVector = [0,0,1],
                             worldUpType = 'objectrotation',worldUpVector = [0,0,1],
                             worldUpObject = self.legBlendChain.chain[1])
#             twistInfoJnt.rx.connect(self.thighTwistIk.twist)
    #         pm.parentConstraint(self.hipChain.chain[0],twistInfoGrpName,mo = 1)
             
            ###
            #fore Leg
            self.clafTwistStart = pm.duplicate(self.legBlendChain.chain[1],
                                                  n = nameUtils.getUniqueName(self.side,'clafTwistS','jj')) 
            self.clafTwistEnd = pm.listRelatives(self.clafTwistStart,c = 1,typ = 'joint')
            pm.parent(self.clafTwistStart,w = 1)
            
            tempClafTrashJnt = pm.listRelatives(self.clafTwistEnd,c = 1,typ = 'joint')
            pm.delete(tempClafTrashJnt)
            
            tempClafTrashNode = pm.listRelatives(self.clafTwistStart,c = 1,typ = 'ikHandle')
            pm.delete(tempClafTrashNode)
            
            self.clafTwistJoint = toolModule.SplitJoint(self.clafTwistStart,self.lowerTwistNum,box = 1,type = 'tool',size = self.size) 
            self.clafTwistJoint.splitJointTool()
            
            for cube in self.clafTwistJoint.cubeList:
                self.footSettingCtrl.control.proxy_vis.connect(cube[0].v)
               
            for twistJoints in self.clafTwistJoint.joints:
                pm.rename(twistJoints, nameUtils.getUniqueName(self.side,'clafTwist','jj'))  
                   
            #create iks      
            clafTwistIkName = nameUtils.getUniqueName(self.side,'clafTwist','iks')  
            clafTwistIkCurveName = nameUtils.getUniqueName(self.side,'clafTwist','ikc')  
            self.clafTwistIk,self.clafTwistIkEffector,self.clafTwistIkCurve = pm.ikHandle(sj = self.clafTwistStart[0],
                                                                                          ee = self.clafTwistEnd[0],
                                                                                          solver = 'ikSplineSolver',
                                                                                          n = clafTwistIkName)
            thighSpIkCluster = pm.skinCluster(self.legBlendChain.chain[1],self.legBlendChain.chain[2],self.clafTwistIkCurve,n = nameUtils.getSkinName())
            pm.rename(self.clafTwistIkCurve,clafTwistIkCurveName)
            self.clafTwistIkCurve.v.set(0)
            self.clafTwistIk.poleVector.set(0,0,0)

              
            #set stretch
            #get last cv:
            pm.select(self.clafTwistIkCurve + '.cv[*]')
            foreIkCLastCv = pm.ls(sl = 1)[0][-1]
            pm.skinPercent(thighSpIkCluster,foreIkCLastCv,tv = [(self.legBlendChain.chain[2],1)])
              
            #get cv length
            clafTwistIkCurveInfoName = nameUtils.getUniqueName(self.side,'clafTwist','cvINFO')
            clafTwistIkCurveInfoNode = pm.createNode('curveInfo',n = clafTwistIkCurveInfoName)
            self.clafTwistIkCurve.getShape().worldSpace[0].connect(clafTwistIkCurveInfoNode.inputCurve)
              
            #create main Node
            clafTwistCurveMDNName = nameUtils.getUniqueName(self.side,'clafTwistCur','MDN')
            clafTwistCurveMDNNode = pm.createNode('multiplyDivide',n = clafTwistCurveMDNName)
              
            clafTwistIkCurveInfoNode.arcLength.connect(clafTwistCurveMDNNode.input1.input1X)
            clafTwistCurveMDNNode.input2.input2X.set(self.legBlendChain.chain[2].tx.get())
            clafTwistCurveMDNNode.operation.set(2)
              
            for num,twistJoints in enumerate(self.clafTwistJoint.joints):
                tempNodeName = nameUtils.getUniqueName(self.side,'clafTwistJnt','MDN')
                tempNode = pm.createNode('multiplyDivide',n = tempNodeName)
                if num > 0 :
                    tempNode.input1.input1X.set(twistJoints.tx.get())
                    clafTwistCurveMDNNode.outputX.connect(tempNode.input2.input2X)
                    tempNode.outputX.connect(twistJoints.tx)
              
            #create foreTwistGrp
            clafTwistGrpName = nameUtils.getUniqueName(self.side,'clafTwist','grp')
            self.clafTwistGrp = pm.group(em = 1,n = clafTwistGrpName) 
            self.clafTwistIk.setParent(self.clafTwistGrp) 
            self.clafTwistIkCurve.setParent(self.clafTwistGrp) 
              
            #lowerTwist
            clafTwistLocStr = pm.spaceLocator(n = nameUtils.getUniqueName(self.side,'clafTwistStart','loc'))
            clafTwistLocEd = pm.spaceLocator(n = nameUtils.getUniqueName(self.side,'clafTwistEnd','loc'))
              
            clafTwistLocStr.setParent(self.legBlendChain.chain[1])
            clafTwistLocEd.setParent(self.legBlendChain.chain[2])
            clafTwistLocStr.t.set(0,0,0)
            clafTwistLocStr.r.set(0,0,0)
            clafTwistLocEd.t.set(0,0,0)
            clafTwistLocEd.r.set(0,0,0)
            clafTwistLocStr.v.set(0)
            clafTwistLocEd.v.set(0)
              
            self.clafTwistIk.dTwistControlEnable.set(1)
            self.clafTwistIk.dWorldUpType.set(4)
            self.clafTwistIk.dWorldUpAxis.set(3)
            self.clafTwistIk.dWorldUpVector.set(0,0,1)
            self.clafTwistIk.dWorldUpVectorEnd.set(0,0,1)
            clafTwistLocStr.worldMatrix.connect(self.clafTwistIk.dWorldUpMatrix)
            clafTwistLocEd.worldMatrix.connect(self.clafTwistIk.dWorldUpMatrixEnd)
             
        elif self.split == 1:
            
            #thigh:
            #non roll up            
            #create twist Leg
            self.thighTwistStart = pm.duplicate(self.splitLegUpChain.chain[0],
                                                n = nameUtils.getUniqueName(self.side,'thighTwistS','jj'))
            tempThighTrashEffNode = pm.listRelatives(self.thighTwistStart,c = 1,typ = 'ikEffector')
            pm.delete(tempThighTrashEffNode)
            self.thighTwistEnd = pm.listRelatives(self.thighTwistStart,c = 1,typ = 'joint')
            
            tempJoint = pm.listRelatives(self.thighTwistEnd,c = 1,typ = 'joint')
            pm.delete(tempJoint)
            pm.rename(self.thighTwistEnd,nameUtils.getUniqueName(self.side,'thighTwistE','jj'))
             
            self.thighTwistJoint = toolModule.SplitJoint(self.thighTwistStart,self.upperTwistNum,box = 1,type = 'tool',size = self.size) 
            self.thighTwistJoint.splitJointTool()
            
            for cube in self.thighTwistJoint.cubeList:
                self.footSettingCtrl.control.proxy_vis.connect(cube[0].v)
             
            for twistJoints in self.thighTwistJoint.joints:
                pm.rename(twistJoints, nameUtils.getUniqueName(self.side,'thighTwist','jj'))  
                 
            #create iks
            thighTwistIkName = nameUtils.getUniqueName(self.side,'thighTwist','iks')  
            thighTwistIkCurveName = nameUtils.getUniqueName(self.side,'thighTwist','ikc')  
            self.thighTwistIk,self.thighTwistIkEffector,self.thighTwistIkCurve = pm.ikHandle(sj = self.thighTwistStart[0],
                                                                                             ee = self.thighTwistEnd[0],
                                                                                             solver = 'ikSplineSolver',
                                                                                             n = thighTwistIkName)
            self.thighTwistIk.setParent(self.splitLegUpChain.chain[0])
            pm.parent(self.thighTwistIkCurve,w = 1)
            pm.parent(self.thighTwistStart,w = 1)
            thighSpIkCurveSkinCluster = pm.skinCluster(self.splitLegUpChain.chain[0],self.splitLegUpChain.chain[1],self.thighTwistIkCurve,n = nameUtils.getSkinName())
            pm.rename(self.thighTwistIkCurve,thighTwistIkCurveName)
            self.thighTwistIk.poleVector.set(0,0,0)            
             
            #set stretch
            #get last cv:
            pm.select(self.thighTwistIkCurve + '.cv[*]')
            upperIkCLastCv = pm.ls(sl = 1)[0][-1]
            pm.skinPercent(thighSpIkCurveSkinCluster,upperIkCLastCv,tv = [(self.splitKneeChain.chain[1],1)])
              
            #get cv length
            thighTwistIkCurveInfoName = nameUtils.getUniqueName(self.side,'thighTwist','cvINFO')
            thighTwistIkCurveInfoNode = pm.createNode('curveInfo',n = thighTwistIkCurveInfoName)
            self.thighTwistIkCurve.getShape().worldSpace[0].connect(thighTwistIkCurveInfoNode.inputCurve)
               
            #create main Node
            thighTwistCurveMDNName = nameUtils.getUniqueName(self.side,'thighTwistCur','MDN')
            thighTwistCurveMDNNode = pm.createNode('multiplyDivide',n = thighTwistCurveMDNName)
               
            thighTwistIkCurveInfoNode.arcLength.connect(thighTwistCurveMDNNode.input1.input1X)
            thighTwistCurveMDNNode.input2.input2X.set(self.splitLegUpChain.chain[1].tx.get())
            thighTwistCurveMDNNode.operation.set(2)
               
            for num,twistJoints in enumerate(self.thighTwistJoint.joints):
                tempNodeName = nameUtils.getUniqueName(self.side,'thighTwistJnt','MDN')
                tempNode = pm.createNode('multiplyDivide',n = tempNodeName)
                if num > 0 :
                    tempNode.input1.input1X.set(twistJoints.tx.get())
                    thighTwistCurveMDNNode.outputX.connect(tempNode.input2.input2X)
                    tempNode.outputX.connect(twistJoints.tx)
                      
            #create upperTwistGrp
            thighTwistGrpName = nameUtils.getUniqueName(self.side,'thighTwist','grp')
            self.thighTwistGrp = pm.group(em = 1,n = thighTwistGrpName) 
            self.thighTwistIk.setParent(self.thighTwistGrp) 
            self.thighTwistIkCurve.setParent(self.thighTwistGrp) 
             
            #create upperTwistInfoGrp 
            twistInfoGrpName = nameUtils.getUniqueName(self.side,'thighTwistInfo','grp')
            self.thighTwistInfoGrp = pm.group(em = 1,n = twistInfoGrpName)
             
            #nonFlip Jnt
            nonFlipStJnt = pm.duplicate(self.legBlendChain.chain[1],
                                        n = nameUtils.getUniqueName(self.side,'thighNonFlip','jc'))
            nonFlipEdJnt = pm.listRelatives(nonFlipStJnt,c = 1,typ = 'joint')
            tempTrashJnt = pm.listRelatives(nonFlipEdJnt,c = 1,typ = 'joint')
            pm.delete(tempTrashJnt)
            pm.rename(nonFlipEdJnt,nameUtils.getUniqueName(self.side,self.baseName + 'thighNonFlip','je'))
            nonFlipStJnt[0].setParent(self.thighTwistInfoGrp)
            nonFlipIks,nonFlipIksEffector = pm.ikHandle(sj = nonFlipStJnt[0],ee = nonFlipEdJnt[0],solver = 'ikRPsolver',
                                                        n = nameUtils.getUniqueName(self.side,'thighNonFlip','iks'))
            nonFlipIks.setParent(self.legBlendChain.chain[1])
            nonFlipIks.poleVector.set(0,0,0)
            nonFlipIks.r.set(0,0,0)
            nonFlipIks.v.set(0)
            pm.pointConstraint(self.legBlendChain.chain[1],nonFlipStJnt,mo = 1)
               
            #twist info jnt
            twistInfoJnt = pm.joint(n = nameUtils.getUniqueName(self.side,'thighTwistInfo','jc'))
            twistInfoJnt.setParent(nonFlipStJnt)
            twistInfoJnt.t.set(0,0,0)
            pm.aimConstraint(nonFlipEdJnt[0],twistInfoJnt,mo = 1,w = 1,aimVector = [1,0,0],upVector = [0,0,1],
                             worldUpType = 'objectrotation',worldUpVector = [0,0,1],
                             worldUpObject = self.legBlendChain.chain[1])
#             twistInfoJnt.rx.connect(self.thighTwistIk.twist)
       
            ###
            #fore Leg
            self.clafTwistStart = pm.duplicate(self.splitLegDownChain.chain[0],
                                               n = nameUtils.getUniqueName(self.side,'clafTwistS','jj'))
            tempClafTrashEffNode = pm.listRelatives(self.clafTwistStart,c = 1,typ = 'ikEffector')
            pm.delete(tempClafTrashEffNode) 
            self.clafTwistEnd = pm.listRelatives(self.clafTwistStart,c = 1,typ = 'joint')
            pm.parent(self.clafTwistStart,w = 1)
             
            self.clafTwistJoint = toolModule.SplitJoint(self.clafTwistStart,self.lowerTwistNum,box = 1,type = 'tool',size = self.size) 
            self.clafTwistJoint.splitJointTool()
            
            for cube in self.clafTwistJoint.cubeList:
                self.footSettingCtrl.control.proxy_vis.connect(cube[0].v)
              
            for twistJoints in self.clafTwistJoint.joints:
                pm.rename(twistJoints, nameUtils.getUniqueName(self.side,'clafTwist','jj'))  
                  
            #create iks      
            clafTwistIkName = nameUtils.getUniqueName(self.side,'clafTwist','iks')  
            clafTwistIkCurveName = nameUtils.getUniqueName(self.side,'clafTwist','ikc')  
            self.clafTwistIk,self.clafTwistIkEffector,self.clafTwistIkCurve = pm.ikHandle(sj = self.clafTwistStart[0],
                                                                                          ee = self.clafTwistEnd[0],
                                                                                          solver = 'ikSplineSolver',
                                                                                          n = clafTwistIkName)
            
            self.clafTwistIk.setParent(self.splitLegDownChain.chain[0])
            pm.parent(self.clafTwistIkCurve,w = 1)
            pm.parent(self.clafTwistStart,w = 1)
            clafSpIkCurveSkinCluster = pm.skinCluster(self.splitLegDownChain.chain[0],self.legBlendChain.chain[2],self.clafTwistIkCurve,n = nameUtils.getSkinName())
            pm.rename(self.clafTwistIkCurve,clafTwistIkCurveName)
            self.clafTwistIk.poleVector.set(0,0,0)
            
            #set stretch
            #get last cv:
            pm.select(self.clafTwistIkCurve + '.cv[*]')
            clafIkCLastCv = pm.ls(sl = 1)[0][-1]
            pm.skinPercent(clafSpIkCurveSkinCluster,clafIkCLastCv,tv = [(self.legBlendChain.chain[2],1)])
              
            #get cv length
            clafTwistIkCurveInfoName = nameUtils.getUniqueName(self.side,'clafTwist','cvINFO')
            clafTwistIkCurveInfoNode = pm.createNode('curveInfo',n = clafTwistIkCurveInfoName)
            self.clafTwistIkCurve.getShape().worldSpace[0].connect(clafTwistIkCurveInfoNode.inputCurve)
              
            #create main Node
            clafTwistCurveMDNName = nameUtils.getUniqueName(self.side,'clafTwistCur','MDN')
            clafTwistCurveMDNNode = pm.createNode('multiplyDivide',n = clafTwistCurveMDNName)
              
            clafTwistIkCurveInfoNode.arcLength.connect(clafTwistCurveMDNNode.input1.input1X)
            clafTwistCurveMDNNode.input2.input2X.set(self.splitLegDownChain.chain[1].tx.get())
            clafTwistCurveMDNNode.operation.set(2)
              
            for num,twistJoints in enumerate(self.clafTwistJoint.joints):
                tempNodeName = nameUtils.getUniqueName(self.side,'clafTwistJnt','MDN')
                tempNode = pm.createNode('multiplyDivide',n = tempNodeName)
                if num > 0 :
                    tempNode.input1.input1X.set(twistJoints.tx.get())
                    clafTwistCurveMDNNode.outputX.connect(tempNode.input2.input2X)
                    tempNode.outputX.connect(twistJoints.tx)
              
            #create foreTwistGrp
            clafTwistGrpName = nameUtils.getUniqueName(self.side,'clafTwist','grp')
            self.clafTwistGrp = pm.group(em = 1,n = clafTwistGrpName) 
            self.clafTwistIk.setParent(self.clafTwistGrp) 
            self.clafTwistIkCurve.setParent(self.clafTwistGrp) 
              
            #lowerTwist
            clafTwistLocStr = pm.spaceLocator(n = nameUtils.getUniqueName(self.side,'clafTwistStart','loc'))
            clafTwistLocEd = pm.spaceLocator(n = nameUtils.getUniqueName(self.side,'clafTwistEnd','loc'))
              
            clafTwistLocStr.setParent(self.legBlendChain.chain[1])
            clafTwistLocEd.setParent(self.legBlendChain.chain[2])
            clafTwistLocStr.t.set(0,0,0)
            clafTwistLocStr.r.set(0,0,0)
            clafTwistLocEd.t.set(0,0,0)
            clafTwistLocEd.r.set(0,0,0)
            clafTwistLocStr.v.set(0)
            clafTwistLocEd.v.set(0)
              
            self.clafTwistIk.dTwistControlEnable.set(1)
            self.clafTwistIk.dWorldUpType.set(4)
            self.clafTwistIk.dWorldUpAxis.set(3)
            self.clafTwistIk.dWorldUpVector.set(0,0,1)
            self.clafTwistIk.dWorldUpVectorEnd.set(0,0,1)
            clafTwistLocStr.worldMatrix.connect(self.clafTwistIk.dWorldUpMatrix)
            clafTwistLocEd.worldMatrix.connect(self.clafTwistIk.dWorldUpMatrixEnd)               
        
        self.clafTwistIkCurve.v.set(0)
        self.thighTwistIkCurve.v.set(0)
        self.thighTwistIk.v.set(0)
        self.clafTwistIk.v.set(0)
        #twist custom attr
        #thigh
        control.addFloatAttr(self.footSettingCtrl.control,['thigh_twist'],-180,180)
        
        #node perpare
        thighTwistPMANodeName = nameUtils.getUniqueName(self.side,'thighTwistFix','PMA')
        thighTwistPMANode = pm.createNode('plusMinusAverage',n = thighTwistPMANodeName)
        
        #connect
        twistInfoJnt.rx.connect(thighTwistPMANode.input1D[0])
        self.footSettingCtrl.control.thigh_twist.connect(thighTwistPMANode.input1D[1])
        thighTwistPMANode.output1D.connect(self.thighTwistIk.twist)  
        
        #claf
        control.addFloatAttr(self.footSettingCtrl.control,['claf_roll'],-180,180) 
        self.footSettingCtrl.control.claf_roll.connect(self.clafTwistIk.roll)
        control.addFloatAttr(self.footSettingCtrl.control,['claf_twist'],-180,180) 
        self.footSettingCtrl.control.claf_twist.connect(self.clafTwistIk.twist)
                                
    def __setRibbonUpper(self):
                
        control.addFloatAttr(self.footSettingCtrl.control,['CC'],0,1) 
        '''
        this function set ribbon for the Upper 
        '''
        self.upperJointLentgh = self.legBlendChain.chain[1].tx.get()
        self.ribon = ribbon.Ribbon(RibbonName = self.baseName + self.ribbonData[0],Length = self.upperJointLentgh,
                                   size = self.size * 0.75,subMid = 1,side = self.side,
                                   midCcName = self.baseName + self.ribbonData[0])   
             
        self.ribon.construction()
        
        pm.xform(self.ribon.startLoc,ws = 1,matrix = self.legBlendChain.chain[0].worldMatrix.get())
        pm.xform(self.ribon.endLoc,ws = 1,matrix = self.legBlendChain.chain[1].worldMatrix.get())
        
#         pm.parentConstraint(self.ikChain.chain[0],self.ribon.startLoc,mo = 1)
        
#         pm.parentConstraint(self.legBlendChain.chain[0],self.ribon.startLoc,mo = 1)
#         pm.parentConstraint(self.legBlendChain.chain[0],self.legBlendChain.chain[1],self.ribon.epUploc,mo = 1)
        
        #connect scale for thighKnee jj2
        self.subMidCtrlThighKnee = self.ribon.subMidCtrl
        self.subMidCtrlThighKnee.control.scaleX.connect(self.ribon.jj[2].scaleX)
        self.subMidCtrlThighKnee.control.scaleY.connect(self.ribon.jj[2].scaleY)
        self.subMidCtrlThighKnee.control.scaleZ.connect(self.ribon.jj[2].scaleZ)
            
    def __setRibbonLower(self):

        '''
        this function set ribbon for the thighKnee 
        '''
        self.lowerJointLentgh = self.legBlendChain.chain[2].tx.get()
        self.ribon45hp = ribbon.Ribbon(RibbonName = self.baseName + self.ribbonData[1],Length = self.lowerJointLentgh,
                                   size = self.size * 0.75,subMid = 1,side = self.side,
                                   midCcName = self.baseName + self.ribbonData[1])   
                
        self.ribon45hp.construction()
        
        #align
        pm.xform(self.ribon45hp.startLoc,ws = 1,matrix = self.legBlendChain.chain[1].worldMatrix.get())
        pm.xform(self.ribon45hp.endLoc,ws = 1,matrix = self.legBlendChain.chain[2].worldMatrix.get())
        
        #parentCnst for the ankle
        self.ribon45hp.endLoc.ry.set(self.ribon45hp.endLoc.ry.get() + 90)
        pm.parentConstraint(self.legBlendChain.chain[2],self.ribon45hp.endLoc,mo = 1)
        
        #connect scale for mid jj
        self.subMidCtrlKneeAnkle = self.ribon45hp.subMidCtrl
        self.subMidCtrlKneeAnkle.control.scaleX.connect(self.ribon45hp.jj[2].scaleX)
        self.subMidCtrlKneeAnkle.control.scaleY.connect(self.ribon45hp.jj[2].scaleY)
        self.subMidCtrlKneeAnkle.control.scaleZ.connect(self.ribon45hp.jj[2].scaleZ)

    def __setRibbonSubMidCc(self):
                
                
        self.subMidCtrlKnee = control.Control(size = self.size * 0.75,baseName = self.ribbonData[2] + '_CC',side = self.side,aimAxis = 'y') 
        self.subMidCtrlKnee.circleCtrl()
        kneePos = pm.xform(self.legBlendChain.chain[1],query=1,ws=1,rp=1)
        pm.move(self.subMidCtrlKnee.controlGrp,kneePos[0],kneePos[1],kneePos[2],a=True)
        
        pm.parentConstraint(self.subMidCtrlKnee.control,self.ribon45hp.startLoc,mo = 1)
        pm.parentConstraint(self.subMidCtrlKnee.control,self.ribon.endLoc,mo = 1)
        pm.parentConstraint(self.legBlendChain.chain[1],self.subMidCtrlKnee.controlGrp,mo = 1)
        
        #name setting for the scale node for thighKnee Jj1
        thighKneeScaleNodeNameJj1 = nameUtils.getUniqueName(self.side,self.baseName + 'thighKneeScaleJj1','PMA')
        
        #create Node for  thighKnee Jj1
        #ribbon name for robin
        thighKneeScalePlusMinusAverageNodeJj1 = pm.createNode('plusMinusAverage',n = thighKneeScaleNodeNameJj1)
        
        #connect thighKnee scale for  thighKnee Jj1
        self.subMidCtrlThighKnee.control.scaleX.connect(thighKneeScalePlusMinusAverageNodeJj1.input3D[0].input3Dx)
        self.subMidCtrlKnee.control.scaleX.connect(thighKneeScalePlusMinusAverageNodeJj1.input3D[1].input3Dx)
        self.subMidCtrlThighKnee.control.scaleY.connect(thighKneeScalePlusMinusAverageNodeJj1.input3D[0].input3Dy)
        self.subMidCtrlKnee.control.scaleY.connect(thighKneeScalePlusMinusAverageNodeJj1.input3D[1].input3Dy)  
        self.subMidCtrlThighKnee.control.scaleZ.connect(thighKneeScalePlusMinusAverageNodeJj1.input3D[0].input3Dz)
        self.subMidCtrlKnee.control.scaleZ.connect(thighKneeScalePlusMinusAverageNodeJj1.input3D[1].input3Dz)     
        thighKneeScalePlusMinusAverageNodeJj1.operation.set(3)
        
        #output scale to thighKnee Jj1
        thighKneeScalePlusMinusAverageNodeJj1.output3D.output3Dx.connect(self.ribon.jj[1].scaleX)
        thighKneeScalePlusMinusAverageNodeJj1.output3D.output3Dy.connect(self.ribon.jj[1].scaleY)
        thighKneeScalePlusMinusAverageNodeJj1.output3D.output3Dz.connect(self.ribon.jj[1].scaleZ)
        
        #name setting for the scale node for thighKnee Jj3
        thighKneeScaleNodeNameJj3 = nameUtils.getUniqueName(self.side,self.baseName + 'thighKneeScaleJj3','PMA')
        
        #create Node for  thighKnee Jj3
        thighKneeScalePlusMinusAverageNodeJj3 = pm.createNode('plusMinusAverage',n = thighKneeScaleNodeNameJj3)
           
        #connect thighKnee scale for  thighKnee Jj3
        
        self.subMidCtrlThighKnee.control.scaleX.connect(thighKneeScalePlusMinusAverageNodeJj3.input3D[0].input3Dx)
        self.legBlendChain.chain[1].scaleX.connect(thighKneeScalePlusMinusAverageNodeJj3.input3D[1].input3Dx)
        self.subMidCtrlThighKnee.control.scaleY.connect(thighKneeScalePlusMinusAverageNodeJj3.input3D[0].input3Dy)
        self.legBlendChain.chain[1].scaleY.connect(thighKneeScalePlusMinusAverageNodeJj3.input3D[1].input3Dy)  
        self.subMidCtrlThighKnee.control.scaleZ.connect(thighKneeScalePlusMinusAverageNodeJj3.input3D[0].input3Dz)
        self.legBlendChain.chain[1].scaleZ.connect(thighKneeScalePlusMinusAverageNodeJj3.input3D[1].input3Dz)     
        thighKneeScalePlusMinusAverageNodeJj3.operation.set(3)
        
        #output scale to thighKnee Jj3
        thighKneeScalePlusMinusAverageNodeJj3.output3D.output3Dx.connect(self.ribon.jj[3].scaleX)
        thighKneeScalePlusMinusAverageNodeJj3.output3D.output3Dy.connect(self.ribon.jj[3].scaleY)
        thighKneeScalePlusMinusAverageNodeJj3.output3D.output3Dz.connect(self.ribon.jj[3].scaleZ)
        
        #connect scale to thighKnee jj0
        self.subMidCtrlKnee.control.scaleX.connect(self.ribon.jj[0].scaleX)
        self.subMidCtrlKnee.control.scaleY.connect(self.ribon.jj[0].scaleY)
        self.subMidCtrlKnee.control.scaleZ.connect(self.ribon.jj[0].scaleZ)
        
        #connect scale to thighKnee jj4
        self.legBlendChain.chain[0].scaleX.connect(self.ribon.jj[4].scaleX)
        self.legBlendChain.chain[0].scaleY.connect(self.ribon.jj[4].scaleY)
        self.legBlendChain.chain[0].scaleZ.connect(self.ribon.jj[4].scaleZ)
 
        #name setting for the scale node for kneeAnkle Jj1
        kneeAnkleScaleNodeNameJj1 = nameUtils.getUniqueName(self.side,self.baseName + 'kneeAnkleScaleJj1','PMA')
        
        #create Node for  kneeAnkle jj1
        kneeAnkleScalePlusMinusAverageNodeJj1 = pm.createNode('plusMinusAverage',n = kneeAnkleScaleNodeNameJj1)
               
        #connect kneeAnkle scale for kneeAnkle jj1
        self.subMidCtrlKneeAnkle.control.scaleX.connect(kneeAnkleScalePlusMinusAverageNodeJj1.input3D[0].input3Dx)
        self.subMidCtrlKnee.control.scaleX.connect(kneeAnkleScalePlusMinusAverageNodeJj1.input3D[1].input3Dx)
        self.subMidCtrlKneeAnkle.control.scaleY.connect(kneeAnkleScalePlusMinusAverageNodeJj1.input3D[0].input3Dy)
        self.subMidCtrlKnee.control.scaleY.connect(kneeAnkleScalePlusMinusAverageNodeJj1.input3D[1].input3Dy)  
        self.subMidCtrlKneeAnkle.control.scaleZ.connect(kneeAnkleScalePlusMinusAverageNodeJj1.input3D[0].input3Dz)
        self.subMidCtrlKnee.control.scaleZ.connect(kneeAnkleScalePlusMinusAverageNodeJj1.input3D[1].input3Dz)     
        kneeAnkleScalePlusMinusAverageNodeJj1.operation.set(3)
        
        #output scale to kneeAnkle jj1
        kneeAnkleScalePlusMinusAverageNodeJj1.output3D.output3Dx.connect(self.ribon45hp.jj[1].scaleX)
        kneeAnkleScalePlusMinusAverageNodeJj1.output3D.output3Dy.connect(self.ribon45hp.jj[1].scaleY)
        kneeAnkleScalePlusMinusAverageNodeJj1.output3D.output3Dz.connect(self.ribon45hp.jj[1].scaleZ)
        
        #name setting for the scale node for kneeAnkle Jj3
        kneeAnkleScaleNodeNameJj3 = nameUtils.getUniqueName(self.side,self.baseName + 'kneeAnkleScaleJj3','PMA')
        
        #create Node for  kneeAnkle jj3
        kneeAnkleScalePlusMinusAverageNodeJj3 = pm.createNode('plusMinusAverage',n = kneeAnkleScaleNodeNameJj3)
               
        #connect kneeAnkle scale for kneeAnkle jj3
        self.subMidCtrlKneeAnkle.control.scaleX.connect(kneeAnkleScalePlusMinusAverageNodeJj3.input3D[0].input3Dx)
        self.subMidCtrlKnee.control.scaleX.connect(kneeAnkleScalePlusMinusAverageNodeJj3.input3D[1].input3Dx)
        self.subMidCtrlKneeAnkle.control.scaleY.connect(kneeAnkleScalePlusMinusAverageNodeJj3.input3D[0].input3Dy)
        self.subMidCtrlKnee.control.scaleY.connect(kneeAnkleScalePlusMinusAverageNodeJj3.input3D[1].input3Dy)  
        self.subMidCtrlKneeAnkle.control.scaleZ.connect(kneeAnkleScalePlusMinusAverageNodeJj3.input3D[0].input3Dz)
        self.subMidCtrlKnee.control.scaleZ.connect(kneeAnkleScalePlusMinusAverageNodeJj3.input3D[1].input3Dz)     
        kneeAnkleScalePlusMinusAverageNodeJj3.operation.set(3)
        
        #output scale to kneeAnkle jj3
        kneeAnkleScalePlusMinusAverageNodeJj3.output3D.output3Dx.connect(self.ribon45hp.jj[3].scaleX)
        kneeAnkleScalePlusMinusAverageNodeJj3.output3D.output3Dy.connect(self.ribon45hp.jj[3].scaleY)
        kneeAnkleScalePlusMinusAverageNodeJj3.output3D.output3Dz.connect(self.ribon45hp.jj[3].scaleZ)
        
        #connect scale to kneeAnkle jj4
        self.subMidCtrlKnee.control.scaleX.connect(self.ribon45hp.jj[4].scaleX)
        self.subMidCtrlKnee.control.scaleY.connect(self.ribon45hp.jj[4].scaleY)
        self.subMidCtrlKnee.control.scaleZ.connect(self.ribon45hp.jj[4].scaleZ)
        
        #connect scale to kneeAnkle jj0
        self.legBlendChain.chain[2].scaleX.connect(self.ribon45hp.jj[0].scaleX)
        self.legBlendChain.chain[2].scaleY.connect(self.ribon45hp.jj[0].scaleY)
        self.legBlendChain.chain[2].scaleZ.connect(self.ribon45hp.jj[0].scaleZ)
    
    def __editCtrl(self):
                
        self.ikRpPvChain.ikCtrl.control.addAttr('foot_roll',at = 'double',min = 0,max = 0,dv = 0)
        pm.setAttr(self.ikRpPvChain.ikCtrl.control + '.foot_roll',e = 0,channelBox = 1)
        self.ikRpPvChain.ikCtrl.control.foot_roll.lock(1)

        self.ikRpPvChain.ikCtrl.control.addAttr('ball',at = 'double',dv = 0,k = 1)
        self.ikRpPvChain.ikCtrl.control.addAttr('toe_lift',at = 'double',dv = 0,k = 1)
        self.ikRpPvChain.ikCtrl.control.addAttr('toe_straight',at = 'double',dv = 0,k = 1)
        self.ikRpPvChain.ikCtrl.control.addAttr('toe_wiggle',at = 'double',dv = 0,k = 1)
        self.ikRpPvChain.ikCtrl.control.addAttr('toe_spin',at = 'double',dv = 0,k = 1)
        self.ikRpPvChain.ikCtrl.control.addAttr('side',at = 'double',dv = 0,k = 1)
        
        self.ikRpPvChain.ikCtrl.control.addAttr('single_roll',at = 'double',min = 0,max = 0,dv = 0)
        pm.setAttr(self.ikRpPvChain.ikCtrl.control + '.single_roll',e = 0,channelBox = 1)
        self.ikRpPvChain.ikCtrl.control.single_roll.lock(1)
        control.addFloatAttr(self.ikRpPvChain.ikCtrl.control,['ball_roll'],0,90) 
        control.addFloatAttr(self.ikRpPvChain.ikCtrl.control,['toe_roll'],0,90) 
        control.addFloatAttr(self.ikRpPvChain.ikCtrl.control,['heel_roll'],-90,90) 

    def __ikFootSet(self):
        
        #add toe wiggle loc
        toeWiggleLoc = pm.spaceLocator(n = nameUtils.getUniqueName(self.side,'toeWiggle','gud'))
        pm.xform(toeWiggleLoc,ws = 1,matrix = self.legGuides[-1].worldMatrix.get())
        pm.parent(toeWiggleLoc,self.legGuides[-2])
        
        #ik
        ballIkName = nameUtils.getUniqueName(self.side,'ballSc','iks')
        toeWiggleIKName = nameUtils.getUniqueName(self.side,'toeWiggleSc','iks')
        ballIkHandle,ballIkEffector = pm.ikHandle(sj = self.ikBlendChain.chain[-4],ee = self.ikBlendChain.chain[-3],solver = 'ikSCsolver',n = ballIkName)
        toeIkHandle,toeIkEffector = pm.ikHandle(sj = self.ikBlendChain.chain[-3],ee = self.ikBlendChain.chain[-2],solver = 'ikSCsolver',n = toeWiggleIKName)
        pm.parent(ballIkHandle,self.legGuides[-1])
        self.ikRpChain.ikHandle.setParent(self.legGuides[-1])
        self.ikRpPvChain.ikHandle.setParent(self.legGuides[-1])
        pm.delete(self.ikRpPvChain.ikHandle + '_pointConstraint1')
        
#         parentCnst = pm.parentConstraint(self.ikRpPvChain.ikCtrl.control,self.legGuides[2],mo = 1)
         
        pointCnst = pm.pointConstraint(self.ikRpPvChain.ikCtrl.control,self.legGuides[2],mo = 1)
        orientCnst = pm.orientConstraint(self.ikRpPvChain.ikCtrl.control,self.legGuides[2],mo = 1)
         
        #node Name
        heelConditionNodeName = nameUtils.getUniqueName(self.side,'Heel','COND')
        ballConditionNodeName = nameUtils.getUniqueName(self.side,'Ball','COND')
        ballRangeNodeName = nameUtils.getUniqueName(self.side,'Ball','RANG')
        ballRangeMultipleNodeName = nameUtils.getUniqueName(self.side,'Ball','MDN')
        ballPlusMinusAverageNodeName = nameUtils.getUniqueName(self.side,'Ball','PMA')
        tipRangeNodeName = nameUtils.getUniqueName(self.side,'Tip','RANG')
        tipRangeMultipleNodeName = nameUtils.getUniqueName(self.side,'tipRange','MDN')
        insideConditionNodeName = nameUtils.getUniqueName(self.side,'Inside','COND')
        outsideConditionNodeName = nameUtils.getUniqueName(self.side,'Outside','COND')
        singleBallPlusMinusAverageNodeName = nameUtils.getUniqueName(self.side,'singleBall','PMA')
        singleToePlusMinusAverageNodeName = nameUtils.getUniqueName(self.side,'singleToe','PMA')
        singleHeelPlusMinusAverageNodeName = nameUtils.getUniqueName(self.side,'singleHeel','PMA')        
          
        #create Node
        heelConditionNode = pm.createNode('condition',n = heelConditionNodeName)
        ballConditionNode = pm.createNode('condition',n = ballConditionNodeName)
        ballMultipleNode = pm.createNode('multiplyDivide',n = ballRangeMultipleNodeName)
        ballRangeNode = pm.createNode('setRange',n = ballRangeNodeName)
        ballPlusMinusAverageNode = pm.createNode('plusMinusAverage',n = ballPlusMinusAverageNodeName)
        tipRangeNode = pm.createNode('setRange',n = tipRangeNodeName)
        tipRangeMultipleNode = pm.createNode('multiplyDivide',n = tipRangeMultipleNodeName)
        insideConditionNode = pm.createNode('condition',n = insideConditionNodeName)
        outsideConditionNode = pm.createNode('condition',n = outsideConditionNodeName)
        singleBallPlusMinusAverageNode = pm.createNode('plusMinusAverage',n = singleBallPlusMinusAverageNodeName)        
        singleToePlusMinusAverageNode = pm.createNode('plusMinusAverage',n = singleToePlusMinusAverageNodeName)        
        singleHeelPlusMinusAverageNode = pm.createNode('plusMinusAverage',n = singleHeelPlusMinusAverageNodeName)                
          
        #connecting
        #ball negetive
        self.ikRpPvChain.ikCtrl.control.ball.connect(heelConditionNode.firstTerm)
        self.ikRpPvChain.ikCtrl.control.ball.connect(heelConditionNode.colorIfTrueR)
        self.ikRpPvChain.ikCtrl.control.heel_roll.connect(singleHeelPlusMinusAverageNode.input1D[0])
        heelConditionNode.outColorR.connect(singleHeelPlusMinusAverageNode.input1D[1])
        heelConditionNode.secondTerm.set(0)
        heelConditionNode.operation.set(5)
        heelConditionNode.colorIfFalseR.set(0)
        singleHeelPlusMinusAverageNode.output1D.connect(self.legGuides[3].rx)
         
        #ball value
        self.ikRpPvChain.ikCtrl.control.ball.connect(ballConditionNode.firstTerm)
        self.ikRpPvChain.ikCtrl.control.ball.connect(ballConditionNode.colorIfTrueR)
        ballConditionNode.secondTerm.set(0)
        ballConditionNode.operation.set(3)
        ballConditionNode.colorIfFalseR.set(0)
         
        #ball lift/straight
        tipRangeNode.minX.set(0)
        tipRangeNode.maxX.set(1)
        ballRangeNode.minX.set(0)
        ballRangeNode.maxX.set(1)
        self.ikRpPvChain.ikCtrl.control.ball.connect(ballRangeNode.valueX)
        self.ikRpPvChain.ikCtrl.control.ball_roll.connect(singleBallPlusMinusAverageNode.input1D[0])
        self.ikRpPvChain.ikCtrl.control.toe_lift.connect(ballRangeNode.oldMinX)
        self.ikRpPvChain.ikCtrl.control.toe_straight.connect(ballRangeNode.oldMaxX)        
        ballRangeNode.outValueX.connect(ballPlusMinusAverageNode.input1D[1])
        ballConditionNode.outColorR.connect(ballMultipleNode.input1X)
        ballMultipleNode.operation.set(1)
        ballPlusMinusAverageNode.operation.set(2)
        ballPlusMinusAverageNode.input1D[0].set(1)
        ballPlusMinusAverageNode.output1D.connect(ballMultipleNode.input2X)
        ballMultipleNode.outputX.connect(singleBallPlusMinusAverageNode.input1D[1])
        singleBallPlusMinusAverageNode.output1D.connect(self.legGuides[-1].rx)
         
        #toe lift/ straight
        tipRangeNode.minX.set(0)
        tipRangeNode.maxX.set(1)
        self.ikRpPvChain.ikCtrl.control.ball.connect(tipRangeNode.valueX)
        self.ikRpPvChain.ikCtrl.control.toe_lift.connect(tipRangeNode.oldMinX)
        self.ikRpPvChain.ikCtrl.control.toe_straight.connect(tipRangeNode.oldMaxX)
        self.ikRpPvChain.ikCtrl.control.toe_roll.connect(singleToePlusMinusAverageNode.input1D[0])        
        ballConditionNode.outColorR.connect(tipRangeMultipleNode.input1X)
        tipRangeNode.outValueX.connect(tipRangeMultipleNode.input2X)
        tipRangeMultipleNode.outputX.connect(singleToePlusMinusAverageNode.input1D[1])
        singleToePlusMinusAverageNode.output1D.connect(self.legGuides[-4].rx)
        self.ikRpPvChain.ikCtrl.control.toe_spin.connect(self.legGuides[-4].ry)
        self.legGuides.append(toeWiggleLoc)
        pm.parent(toeIkHandle,self.legGuides[-1])
        self.ikRpPvChain.ikCtrl.control.toe_wiggle.connect(self.legGuides[-1].rx)
        
        ###side
        if self.side == 'l': 
            #inside
            self.ikRpPvChain.ikCtrl.control.side.connect(insideConditionNode.firstTerm)
            self.ikRpPvChain.ikCtrl.control.side.connect(insideConditionNode.colorIfTrueR)
            insideConditionNode.operation.set(3)
            insideConditionNode.outColorR.connect(self.legGuides[-4].rz)
             
            #outside
            self.ikRpPvChain.ikCtrl.control.side.connect(outsideConditionNode.firstTerm)
            self.ikRpPvChain.ikCtrl.control.side.connect(outsideConditionNode.colorIfTrueR)
            outsideConditionNode.operation.set(5)
            outsideConditionNode.outColorR.connect(self.legGuides[-3].rz)
        elif self.side == 'r':     
            #inside
            self.ikRpPvChain.ikCtrl.control.side.connect(insideConditionNode.firstTerm)
            self.ikRpPvChain.ikCtrl.control.side.connect(insideConditionNode.colorIfTrueR)
            insideConditionNode.operation.set(5)
            insideConditionNode.outColorR.connect(self.legGuides[-4].rz)
             
            #outside
            self.ikRpPvChain.ikCtrl.control.side.connect(outsideConditionNode.firstTerm)
            self.ikRpPvChain.ikCtrl.control.side.connect(outsideConditionNode.colorIfTrueR)
            outsideConditionNode.operation.set(3)
            outsideConditionNode.outColorR.connect(self.legGuides[-3].rz)
        #default set
        self.ikRpPvChain.ikCtrl.control.toe_lift.set(35)
        self.ikRpPvChain.ikCtrl.control.toe_straight.set(70)
            
    def __cleanUp(self):
        
        #cc grp and v 
        self.cntsGrp = pm.group(empty = 1,n = nameUtils.getUniqueName(self.side,self.baseName + 'CC','grp')) 
        self.footSettingCtrl.controlGrp.setParent(self.cntsGrp)
        self.ikRpPvChain.ikCtrl.controlGrp.setParent(self.cntsGrp)
        self.ikRpPvChain.poleVectorCtrl.controlGrp.setParent(self.cntsGrp)
        
        #ccDef grp and v
        if self.twist == 'ribon45hp':
            self.ccDefGrp = pm.group(empty = 1,n = nameUtils.getUniqueName(self.side,self.baseName + 'Def','grp'))
            self.subMidCtrlKneeAnkle.controlGrp.setParent(self.ccDefGrp)
            self.subMidCtrlThighKnee.controlGrp.setParent(self.ccDefGrp)
            self.subMidCtrlKnee.controlGrp.setParent(self.ccDefGrp)
            self.footSettingCtrl.control.CC.connect(self.ccDefGrp.v)
            self.ribon.main.v.set(0)
            self.ribon45hp.main.v.set(0)
            self.ccDefGrp.setParent(self.cntsGrp)
            
        self.footSettingCtrl.control.IKFK.set(1)
        #jj grp
        self.legGrp = pm.group(em = 1,n = nameUtils.getUniqueName(self.side,self.baseName,'grp'))
        self.ikRpChain.stretchStartLoc.setParent(self.legGrp)
        self.ikRpPvChain.stretchStartLoc.setParent(self.legGrp)
        self.ikRpPvChain.lockUpStartLoc.setParent(self.legGrp)
        
        for b in (self.ikRpChain,self.ikRpPvChain,self.ikBlendChain,self.fkChain,self.legBlendChain):
            b.chain[0].setParent(self.legGrp)
        
        self.legGrp.setParent(self.hipCtrl.control)
        
        #guide grp
        self.ikRpChain.stretchEndLoc.v.set(0)
        self.guideGrp.v.set(0)

        self.legGuides[2].v.set(0)       
        
    def __buildHooks(self):
        
        #create and align
        worldName = nameUtils.getUniqueName(self.side,self.baseName + 'World','loc')
        self.locWorld = pm.spaceLocator(n = worldName)
        self.locWorld.v.set(0)
          
        localName = nameUtils.getUniqueName(self.side,self.baseName + 'Local','loc')
        self.locLocal = pm.spaceLocator(n = localName)
        self.locLocal.v.set(0)
          
        pm.xform(self.locWorld,ws = 1,matrix = self.legBlendChain.chain[0].wm.get())
        pm.xform(self.locLocal,ws = 1,matrix = self.legBlendChain.chain[0].wm.get())
        
        self.locWorld.r.set(0,0,0)
        self.locLocal.r.set(0,0,0)
         
        self.locLocal.setParent(self.hipChain.chain[-1])
        pm.parentConstraint(self.hipCtrl.control,self.locWorld,skipRotate = ['x','y','z'],mo = 1)
           
        self.fkChain.chain[0].addAttr('space',at = 'enum',en = 'world:local:',k = 1)
           
        #add target tester
        targetName = nameUtils.getUniqueName(self.side,self.baseName + 'Tar','loc')
        self.__tempSpaceSwitch = pm.spaceLocator(n = targetName)
        pm.xform(self.__tempSpaceSwitch,ws = 1,matrix = self.legBlendChain.chain[0].wm.get())
#         self.__tempSpaceSwitch.setParent(self.hi.XTR)
        self.__tempSpaceSwitch.v.set(0)
    
        #final cnst
        finalCnst = pm.parentConstraint(self.locLocal,self.locWorld,self.__tempSpaceSwitch,mo = 0)
        reverseNodeName = nameUtils.getUniqueName(self.side,self.baseName + 'Hook','REV')
        reverseNode = pm.createNode('reverse',n = reverseNodeName)
            
        #fk cnst
        pm.parentConstraint(self.__tempSpaceSwitch,self.legGrp,mo = 1)
 
        self.fkChain.chain[0].attr('space').connect(finalCnst.attr(self.locLocal.name() + 'W0'))
        self.fkChain.chain[0].attr('space').connect(reverseNode.inputX)
        reverseNode.outputX.connect(finalCnst.attr(self.locWorld.name() + 'W1'))        
              
    def buildConnections(self):
        
        #reveice info from incoming package
        if pm.objExists(self.metaMain) == 1:
            
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
            spineControls = pm.connectionInfo(spine.controls, destinationFromSource=True)
            
            #get linked
            for tempMainDestination in moduleGrp:
                splitTempMainDestination = tempMainDestination.split('.')
                mainDestinations.append(splitTempMainDestination[0])
                
            for tempSpineDestination in spineControls:
                splitTempSpineDestination = tempSpineDestination.split('.')
                spineDestinations.append(splitTempSpineDestination[0])


            #to the hip
#             self.shoulderBladeGrp.setParent(spineDestinations[0])
#             self.shoulderAtChain.chain[0].setParent(spineDestinations[0])
#             self.shoulderCtrl.controlGrp.setParent(spineDestinations[0])
#             self.poseReadorGrp.setParent(spineDestinations[0])
            
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
            
            #to the main hierachy
            self.legGrp.setParent(self.hipCtrl.control)
            self.cntsGrp.setParent(CC) 
            self.legGuides[2].setParent(IK)
            self.guideGrp.setParent(GUD)
            self.mirrorGuideGrp.setParent(GUD)
            self.locWorld.setParent(IK)
            self.__tempSpaceSwitch.setParent(XTR)
            self.ikRpPvChain.ikBeamCurve.setParent(XTR)
            self.ikRpPvChain.distTransNode.setParent(XTR)
            self.ikRpPvChain.upDistTransNode.setParent(XTR)
            self.ikRpPvChain.downDistTransNode.setParent(XTR)
            self.ikRpChain.distTransNode.setParent(XTR)
            self.hipCtrl.controlGrp.setParent(spineDestinations[0])

            if self.twist == 'ribon45hp':
                self.ribon.main.setParent(XTR)
                self.ribon45hp.main.setParent(XTR)
            
            if self.twist == 'non_roll':
                metaUtils.addToMeta(self.meta,'skinJoints',[skinjoint for skinjoint in self.thighTwistJoint.joints]
                                    + [skinjoint for skinjoint in self.clafTwistJoint.joints])     
                self.thighTwistStart[0].setParent(SKL)
                self.thighTwistGrp.setParent(XTR)
                self.thighTwistInfoGrp.setParent(XTR)
                self.clafTwistStart[0].setParent(SKL)
                self.clafTwistGrp.setParent(XTR)
#                 self.ikRpPvChain.ikCtrl.control.up_twist.connect(self.ikRpPvChain.ikHandle.twist)                
            
            print ''
            print 'Info from (' + self.meta + ') has been integrate, ready for next Module'
            print ''
            
        else:
            OpenMaya.MGlobal.displayError('Target :' + self.metaMain + ' is NOT exist')
            
        #create package send for next part
        #template:
        #metaUtils.addToMeta(self.meta,'attr', objs)
        metaUtils.addToMeta(self.meta,'controls',[self.footSettingCtrl.control]
                            + [self.ikRpPvChain.ikCtrl.control,self.ikRpPvChain.poleVectorCtrl.control]
                            + [fk for fk in self.fkChain.chain])
        metaUtils.addToMeta(self.meta,'skinJoints',[self.hipChain.chain[0],self.legBlendChain.chain[-3],self.legBlendChain.chain[-4]])
        metaUtils.addToMeta(self.meta,'guideLocator',[mirrorGuide for mirrorGuide in self.mirrorGuideList])
#         metaUtils.addToMeta(self.meta,'moduleGrp',[self.legGrp])
#         metaUtils.addToMeta(self.meta,'chain', [ik for ik in self.ikChain.chain] + [ori for ori in self.legBlendChain.chain])
        
def getUi(parent,mainUi):
    
    return LegModuleUi(parent,mainUi)

class LegModuleUi(object):
#     baseName = 'leg',side = 'l',size = 1.5,
    def __init__(self,parent,mainUi):
        
        self.mainUi = mainUi
        self.__popuItems = []
        
        pm.setParent(parent)
        self.mainL = pm.columnLayout(adj = 1)
        pm.separator(h = 10)
        
        self.leg = pm.columnLayout(adj = 1,p = self.mainL) 
        self.name = pm.text(l = '**** Leg Module ****')       
        self.baseNameT = pm.textFieldGrp(l = 'baseName : ',ad2 = 1,text = 'leg',cl2 = ['left','left'])        
        pm.rowLayout(adj = 1,nc=100,p = self.leg)
        
        #size
        self.cntSizeV = pm.floatFieldGrp(l = 'ctrl Size : ',cl2 = ['left','left'],
                                         ad2 = 1,numberOfFields = 1,value1 = 1,p = self.leg)
        
        #side
        pm.rowLayout(adj = 1,nc=100,p = self.leg)
        pm.button(l = 'side : ')
        self.sideR = pm.radioButtonGrp(nrb = 2,la2 = ['left','right'],sl = 1)
        
        #mirror 
        pm.rowLayout(adj = 1,nc=100,p = self.leg)
        pm.button(l = 'mirror : ')
        self.mirrorNodeM = pm.optionMenu(l = 'mirrorMeta : ',p = self.leg)
        self.mirrorR = pm.radioButtonGrp(nrb = 2,la2 = ['yes','no'],sl = 2,onc = self.__metaReload)        
        
        #split
        pm.rowLayout(adj = 1,nc=100,p = self.leg)
        pm.button(l = 'split knee: ')
        self.splitR = pm.radioButtonGrp(nrb = 2,la2 = ['yes','no'],sl = 2)   
                
        #twist
        self.twistModule = pm.optionMenu(l = 'twist module : ',p = self.leg)
        pm.menuItem(l = 'non_roll',p = self.twistModule)
        pm.menuItem(l = 'ribon45hp',p = self.twistModule)
        pm.menuItem(l = 'nope',p = self.twistModule)
        
        #twist num
        pm.rowLayout(adj = 1,nc=100,p = self.leg)
        pm.button(l = 'upper Twist num : ')
        self.upperNum = pm.intSliderGrp(f=1,max=10,s=1,min = 2,v = 5)
         
        pm.rowLayout(adj = 1,nc=100,p = self.leg)
        pm.button(l = 'lower  Twist num : ')
        self.lowerNum = pm.intSliderGrp(f=1,max=10,s=1,min = 2,v = 5) 
        
        #meta
        self.metaSpineNodeM = pm.optionMenu(l = 'spineMeta : ',p = self.leg)
        metaUtils.metaSel()
        self.metaMainNodeM = pm.optionMenu(l = 'mainMeta : ',p = self.leg)
        metaUtils.metaSel()
        
        pm.separator(h = 10,p = self.leg)
        self.removeB = pm.button(l = 'remove',c = self.__removeInstance,p = self.leg)   
        
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
        splitR = pm.radioButtonGrp(self.splitR,q = True,sl = True)
        mirrorR = pm.radioButtonGrp(self.mirrorR,q = True,sl = True)
        
        if sideR == 1:
            sideT = 'l'
        elif sideR == 2:
            sideT = 'r'     
        
        if splitR == 1:
            splitT = 1
        elif splitR == 2:
            splitT = 0
            
        if mirrorR == 1:
            mirrorT = 'yes'
        elif mirrorR == 2:
            mirrorT = 'no'    
                
        cntSizeV = pm.floatFieldGrp(self.cntSizeV,q = 1,value1 = 1)
        mainMetaNode = pm.optionMenu(self.metaMainNodeM,q = 1,v = 1)
        spineMetaNode = pm.optionMenu(self.metaSpineNodeM,q = 1,v = 1)
        mirrorMetaNode = pm.optionMenu(self.mirrorNodeM,q = 1,v = 1)
        twistT = pm.optionMenu(self.twistModule, q = 1,v = 1)
        upperTwistNumV = pm.intSliderGrp(self.upperNum , q = 1,v = 1)
        lowerTwistNumV = pm.intSliderGrp(self.lowerNum ,q = 1,v = 1)
        
        self.__pointerClass = LegModule(baseName = baseNameT,side = sideT,size = cntSizeV,
                                        metaMain = mainMetaNode,metaSpine = spineMetaNode,
                                        twist = twistT,upperTwistNum = upperTwistNumV,split = splitT,
                                        lowerTwistNum = lowerTwistNumV,mirror = mirrorT,metaMirror = mirrorMetaNode)
        return self.__pointerClass             

# import sys
# myPath = 'C:/eclipse/test/OOP/AutoRig'
# 
# if not myPath in sys.path:
#     sys.path.append(myPath)
#     
# import reloadMain
# reload(reloadMain)
# 
# from Modules import legModule
# lg = legModule.LegModule()
# lg.buildGuides()
# lg.build()        
        
                        
