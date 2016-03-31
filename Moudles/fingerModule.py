import pymel.core as pm
from Modules.subModules import fkChain,ikChain,boneChain,ribbon
from Utils import nameUtils
from Modules import control,hierarchy,limbModule
from maya import OpenMaya

class FingerModule(object):
    
    posThumbArray = [(6.4540,13.8587,0.0015),(6.6541,13.8587,0.0015),(6.8466,13.8587,0.0015),(7.0855,13.8587,0.0015)]
    posIndexArray = [[6.58,14.03,-0.04],[6.94,14.03,-0.04],[7.3,14.03,-0.04],[7.515,14.03,-0.04],[7.74,14.03,-0.04]]
    posMiddleArray = [[6.539,14.05,-0.22],[6.9,14.05,-0.22],[7.361,14.05,-0.22],[7.58,14.05,-0.22],[7.88,14.05,-0.22]]
    posRingArray = [[6.58,14.055,-0.413],[6.94,14.055,-0.413],[7.3,14.055,-0.413],[7.515,14.055,-0.413],[7.74,14.055,-0.413]]
    posPinkyArray = [[6.746,14.03,-0.585],[6.94,14.03,-0.585],[7.134,14.03,-0.585],[7.276,14.03,-0.585],[7.5,14.03,-0.585]]
    
    rotThumbArrary = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    rotIndexArray = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    rotMiddleArray = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    rotRingArray = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    rotPinkyArray = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    
    def __init__(self,baseName = 'finger',side = 'l',size = 0.5,
                 metaArm = None,metaMain = None,metaSpine = None,
                 fingerNum = 'ni'):
        
        self.baseName = baseName
        self.side = side
        self.size = size

        #num
        if fingerNum == 'ni':
            self.fingerNum = 2            
        elif fingerNum == 'sann':
            self.fingerNum = 3            
        elif fingerNum == 'shi':
            self.fingerNum = 4            
        elif fingerNum == 'go':
            self.fingerNum = 5
        
        #guides 
        self.guides = None
        self.guideGrp = None     
        
        #sdk
        self.thumbSdks = None
        self.indexSdks = None
        self.midSdks = None
        self.ringSdks = None
        self.pinkySdks = None
        
        #cc  
        self.thumbCc = None
        self.indexCc = None
        self.midCc = None
        self.ringCc = None
        self.pinkyCc = None
        
        #Partial
        self.thumbPartial = None
        self.indexPartial = None
        self.midPartial = None
        self.ringPartial = None
        self.pinkyPartial = None
        
        #jj
        self.thumbGrp = None
        self.indexGrp = None
        self.midGrp = None
        self.ringGrp = None
        self.pinkyGrp = None       
        self.handGrp = None
        
        #meta
        self.metaArm = metaArm
        self.metaMain = metaMain
        self.metaSpine = metaSpine
        
        #info from arm
        self.armControls = None
        self.armChains = None
        
        #attrs
        self.attrs = ['fist_a','firs_b','relax_a','relax_b','relax_c',
                      'relax_d','relax_e','grab_a','grab_b','spread_a',
                      'spread_b','hand','palm_a','palm_b','thumb_a',
                      'thumb_b','thumb_c','thumb_d','index_curl',
                      'middle_curl','ring_curl','pinky_curl','point']
            
        #nameList
        self.fingerName = ['thumb','index','middle','ring','pinky']
        self.fingerJointName = ['Base','Root','Mid','Tip','End','Partial']
        self.thumbJointName = ['Base','Root','Mid','Tip','End','Partial']
        
    def buildGuides(self):
        
        #build guides        
        self.guides = []
        self.guideGrp = []        
        
        self.thumbGuides = []
        self.indexGuides = []
        self.middleGuides = []
        self.ringGuides = []
        self.pinkyGuides = []        
        
        #guide grp       
        guideName = nameUtils.getUniqueName(self.side,self.baseName + '_Gud','grp')
        self.guideGrp = pm.group(em = 1,n = guideName)
        print self.fingerNum
        #num
        if self.fingerNum == 2:
            self.posMiddleArray = []
            self.rotMiddleArray = []
            self.posRingArray = []
            self.rotRingArray = []
            self.posPinkyArray = []
            self.rotPinkyArray = []
            
        elif self.fingerNum == 3:
            self.posRingArray = []
            self.rotRingArray = []
            self.posPinkyArray = []
            self.rotPinkyArray = []
            
        elif self.fingerNum == 4:
            self.posPinkyArray = []
            self.rotPinkyArray = []        
        
        #thumb
        for num,obj in enumerate(self.posThumbArray):
            name = nameUtils.getUniqueName(self.side,self.fingerName[0] + self.thumbJointName[num],'gud')
            loc = pm.spaceLocator(n = name)
            loc.t.set(obj)
            loc.r.set(self.rotThumbArrary[num])
            loc.localScale.set(0.2,0.2,0.2)
            self.thumbGuides.append(loc)
            
        self.tempThumbGuides = list(self.thumbGuides)
        self.tempThumbGuides.reverse()
        for i in range(len(self.tempThumbGuides)):
            if i != (len(self.tempThumbGuides) - 1):
                pm.parent(self.tempThumbGuides[i],self.tempThumbGuides[i + 1])
        self.tempThumbGuides.reverse()
        self.guides.append(self.tempThumbGuides[0])
        self.tempThumbGuides[0].setParent(self.guideGrp)
        
        #index    
        for num,obj in enumerate(self.posIndexArray):
            name = nameUtils.getUniqueName(self.side,self.fingerName[1] + self.fingerJointName[num],'gud')
            loc = pm.spaceLocator(n = name)
            loc.t.set(obj)
            loc.r.set(self.rotIndexArray[num])
            loc.localScale.set(0.2,0.2,0.2)
            self.indexGuides.append(loc)
            
        self.tempIndexGuides = list(self.indexGuides)
        self.tempIndexGuides.reverse()
        for i in range(len(self.tempIndexGuides)):
            if i != (len(self.tempIndexGuides) - 1):
                pm.parent(self.tempIndexGuides[i],self.tempIndexGuides[i + 1])
        self.tempIndexGuides.reverse()
        self.guides.append(self.tempIndexGuides[0])
        self.tempIndexGuides[0].setParent(self.guideGrp)
        
        #middle
        for num,obj in enumerate(self.posMiddleArray):
            name = nameUtils.getUniqueName(self.side,self.fingerName[2] + self.fingerJointName[num],'gud')
            loc = pm.spaceLocator(n = name)
            loc.t.set(obj)
            loc.r.set(self.rotMiddleArray[num])
            loc.localScale.set(0.2,0.2,0.2)
            self.middleGuides.append(loc)

        if len(self.middleGuides) != 0:             
            self.tempMiddleGuides = list(self.middleGuides)
            self.tempMiddleGuides.reverse()
            for i in range(len(self.tempMiddleGuides)):
                if i != (len(self.tempMiddleGuides) - 1):
                    pm.parent(self.tempMiddleGuides[i],self.tempMiddleGuides[i + 1])
            self.tempMiddleGuides.reverse()
            self.guides.append(self.tempMiddleGuides[0])
            self.tempMiddleGuides[0].setParent(self.guideGrp)   
         
        #ring 
        for num,obj in enumerate(self.posRingArray):
            name = nameUtils.getUniqueName(self.side,self.fingerName[3] + self.fingerJointName[num],'gud')
            loc = pm.spaceLocator(n = name)
            loc.t.set(obj)
            loc.r.set(self.rotRingArray[num])
            loc.localScale.set(0.2,0.2,0.2)
            self.ringGuides.append(loc)
             
        if len(self.ringGuides) != 0:
            self.tempRingGuides = list(self.ringGuides)
            self.tempRingGuides.reverse()
            for i in range(len(self.tempRingGuides)):
                if i != (len(self.tempRingGuides) - 1):
                    pm.parent(self.tempRingGuides[i],self.tempRingGuides[i + 1])
            self.tempRingGuides.reverse()   
            self.guides.append(self.tempRingGuides[0])
            self.tempRingGuides[0].setParent(self.guideGrp)
         
        #pinky 
        for num,obj in enumerate(self.posPinkyArray):
            name = nameUtils.getUniqueName(self.side,self.fingerName[4] + self.fingerJointName[num],'gud')
            loc = pm.spaceLocator(n = name)
            loc.t.set(obj)
            loc.r.set(self.rotPinkyArray[num])
            loc.localScale.set(0.2,0.2,0.2)
            self.pinkyGuides.append(loc)
             
        if len(self.pinkyGuides) != 0:     
            self.tempPinkyGuides = list(self.pinkyGuides)
            self.tempPinkyGuides.reverse()
            for i in range(len(self.tempPinkyGuides)):
                if i != (len(self.tempPinkyGuides) - 1):
                    pm.parent(self.tempPinkyGuides[i],self.tempPinkyGuides[i + 1])
            self.tempPinkyGuides.reverse()   
            self.guides.append(self.tempPinkyGuides[0])
            self.tempPinkyGuides[0].setParent(self.guideGrp)    
        
    def build(self):
        
        self.guideGrp.v.set(0)
        
        #build index
        #thumb info
        self.guideThumbPos = [x.getTranslation(space = 'world') for x in self.thumbGuides]
        self.guideThumbRot = [x.getRotation(space = 'world') for x in self.thumbGuides]
                
        #thumb jj
        self.thumbChain = boneChain.BoneChain(self.fingerName[0],self.side,type = 'jj')
        self.thumbChain.fromList(self.guideThumbPos,self.guideThumbRot,autoOrient = 0)
        
        self.thumbGrp = pm.group(self.thumbChain.chain[0],n = nameUtils.getUniqueName(self.side,self.fingerName[0],'grp'))
        thumbInitial =  self.thumbChain.chain[0].getTranslation(space = 'world')
        pm.move(thumbInitial[0],thumbInitial[1],thumbInitial[2],self.thumbGrp + '.rotatePivot')
        pm.move(thumbInitial[0],thumbInitial[1],thumbInitial[2],self.thumbGrp + '.scalePivot')       
        
        #index info
        self.guideIndexPos = [x.getTranslation(space = 'world') for x in self.indexGuides]
        self.guideIndexRot = [x.getRotation(space = 'world') for x in self.indexGuides]

        #index jj
        self.indexChain = boneChain.BoneChain(self.fingerName[1],self.side,type = 'jj')
        self.indexChain.fromList(self.guideIndexPos,self.guideIndexRot)
        
        self.indexGrp = pm.group(self.indexChain.chain[0],n = nameUtils.getUniqueName(self.side,self.fingerName[1],'grp'))
        indexInitial =  self.indexChain.chain[0].getTranslation(space = 'world')
        pm.move(indexInitial[0],indexInitial[1],indexInitial[2],self.indexGrp + '.rotatePivot')
        pm.move(indexInitial[0],indexInitial[1],indexInitial[2],self.indexGrp + '.scalePivot')
        
        if self.fingerNum > 2:
            #mid info
            self.guideMidPos = [x.getTranslation(space = 'world') for x in self.middleGuides]
            self.guideMidRot = [x.getRotation(space = 'world') for x in self.middleGuides]
            
            #mid jj
            self.midChain = boneChain.BoneChain(self.fingerName[2],self.side,type = 'jj')
            self.midChain.fromList(self.guideMidPos,self.guideMidRot)    
            
            self.midGrp = pm.group(self.midChain.chain[0],n = nameUtils.getUniqueName(self.side,self.fingerName[2],'grp'))
            midInitial =  self.midChain.chain[0].getTranslation(space = 'world')
            pm.move(midInitial[0],midInitial[1],midInitial[2],self.midGrp + '.rotatePivot')
            pm.move(midInitial[0],midInitial[1],midInitial[2],self.midGrp + '.scalePivot')  
        
        if self.fingerNum > 3: 
            #ring info
            self.guideRingPos = [x.getTranslation(space = 'world') for x in self.ringGuides]
            self.guideRingRot = [x.getRotation(space = 'world') for x in self.ringGuides]
            
            #ring jj
            self.ringChain = boneChain.BoneChain(self.fingerName[3],self.side,type = 'jj')
            self.ringChain.fromList(self.guideRingPos,self.guideRingRot)     
            
            self.ringGrp = pm.group(self.ringChain.chain[0],n = nameUtils.getUniqueName(self.side,self.fingerName[3],'grp'))
            ringInitial =  self.ringChain.chain[0].getTranslation(space = 'world')
            pm.move(ringInitial[0],ringInitial[1],ringInitial[2],self.ringGrp + '.rotatePivot')
            pm.move(ringInitial[0],ringInitial[1],ringInitial[2],self.ringGrp + '.scalePivot')
        
        if self.fingerNum > 4:
            #pinky info
            self.guidePinkyPos = [x.getTranslation(space = 'world') for x in self.pinkyGuides]
            self.guidePinkyRot = [x.getRotation(space = 'world') for x in self.pinkyGuides] 
            
            #pinky jj
            self.pinkyChain = boneChain.BoneChain(self.fingerName[4],self.side,type = 'jj')
            self.pinkyChain.fromList(self.guidePinkyPos,self.guidePinkyRot)   
            
            self.pinkyGrp = pm.group(self.pinkyChain.chain[0],n = nameUtils.getUniqueName(self.side,self.fingerName[4],'grp'))
            pinkyInitial =  self.pinkyChain.chain[0].getTranslation(space = 'world')
            pm.move(pinkyInitial[0],pinkyInitial[1],pinkyInitial[2],self.pinkyGrp + '.rotatePivot')
            pm.move(pinkyInitial[0],pinkyInitial[1],pinkyInitial[2],self.pinkyGrp + '.scalePivot')               
 
        self.__fingerCC()
        self.__partialJoint()
        self.__setSDK()
    
    def __fingerCC(self):
        
        #init
        self.armControls = []
        self.armChains = []        
        
        #receive info from incoming package
        #receive info from arm meta
        if pm.objExists(self.metaArm) == 1 and 'META' in self.metaArm:
            
            print ''
            print 'package from (' + self.metaArm + ') has been received'
            print ''
            
            pm.select(self.metaArm) 
            armMeta = pm.selected()[0]

            armControlsMeta = pm.connectionInfo(armMeta.controls, destinationFromSource=True)
            armChainsMeta = pm.connectionInfo(armMeta.chain, destinationFromSource=True)
            
            #get element
            #arm ctrl
            for armControlMeta in armControlsMeta:
                armControlUnicode = armControlMeta.split('.')
                pm.select(armControlUnicode[0])
                armControl = pm.selected()
                self.armControls.append(armControl[0])
                
            #arm chain
            for armChainMeta in armChainsMeta:
                armChain = armChainMeta.split('.')
                self.armChains.append(armChain[0])            
            
            #self.Chain.chain[-1],self.ikChain.ikCtrl.control,self.fkChain.chain[-1]]
            
            #set cc
            pm.addAttr(self.armControls[0],ln = '___',at = 'enum',en = 'HandDrives:')
            pm.setAttr(self.armControls[0] + '.___',e = 1,channelBox = 1)
        
            #add attr
            control.addFloatAttr(self.armControls[0],self.attrs,-3,10) 
                        
            print 'package (' + self.metaArm + ') analyzed'
                
        else:
            OpenMaya.MGlobal.displayError('Package :' + self.metaArm + ' is NOT exist')
            
#             print 'Do not receive META package, use ' + self.metaArm + ' instead.'
#             pm.select(self.metaArm)
#             objSelected = pm.selected()[0]
#             self.armControls.append(objSelected)
# 
#             #set cc
#             pm.addAttr(self.armControls[0],ln = '___',at = 'enum',en = 'HandDrives:')
#             pm.setAttr(self.armControls[0] + '.___',e = 1,channelBox = 1)
#         
#             #add attr
#             control.addFloatAttr(self.armControls[0],self.attrs,-3,10)         
        
        #sdk init
        self.thumbSdks = []
        self.indexSdks = []
        self.midSdks = []
        self.ringSdks = []
        self.pinkySdks = []
        
        #cc init
        self.thumbCc = []
        self.indexCc = []
        self.midCc = []
        self.ringCc = []
        self.pinkyCc = []
        
        #create thumb cc ctrl     
        for num,thumbJointName in enumerate(self.thumbChain.chain):
            #correct jj name
            pm.rename(thumbJointName,nameUtils.getUniqueName(self.side,self.fingerName[0] + self.thumbJointName[num],'jj'))
            
            if num < self.thumbChain.chainLength() - 1:    
                #create sdk and correct cc name
#                 cc = control.Control(self.side,self.baseName,size = thumbJointName.getRadius() / 5) 
                cc = control.Control(self.side,self.baseName,size = self.size) 
                cc.circleCtrl()
                self.thumbCc.append(cc.control)
                
                #create sdk grp
                sdkGrp = pm.group(em = 1,n = nameUtils.getUniqueName(self.side,self.fingerName[0] + self.thumbJointName[num],'SDK'))
                self.thumbSdks.append(sdkGrp)
                
                #align cc,sdk grp
                pm.xform(cc.controlGrp,ws = 1,matrix = thumbJointName.worldMatrix.get())
                pm.xform(sdkGrp,ws = 1,matrix = thumbJointName.worldMatrix.get())
                
                cc.control.setParent(sdkGrp)
                sdkGrp.setParent(cc.controlGrp)       
                
                #clean up and rename
                pm.rename(cc.control,nameUtils.getUniqueName(self.side,self.fingerName[0] + self.thumbJointName[num],'cc'))
                pm.rename(cc.controlGrp,nameUtils.getUniqueName(self.side,self.fingerName[0] + self.thumbJointName[num],'grp'))
                pm.delete(cc.control,ch=1)
        
        #jj clean up
        for num,ctrl in enumerate(self.thumbCc):
            self.thumbChain.chain[num].setParent(ctrl)
            if num > 0 :
                ctrl.getParent().getParent().setParent(self.thumbChain.chain[num - 1])
                
        #thumb clean up       
        self.thumbCc[0].getParent().getParent().setParent(self.thumbGrp )
        pm.rename(self.thumbChain.chain[-1],nameUtils.getUniqueName(self.side,self.fingerName[0]  + self.thumbJointName[4],'je')) 
        
        #create index cc ctrl
        for num,indexJoint in enumerate(self.indexChain.chain):
            #correct jj name
            pm.rename(indexJoint,nameUtils.getUniqueName(self.side,self.fingerName[1] + self.fingerJointName[num],'jj'))
            
            if num < self.indexChain.chainLength() - 1:
                #create sdk and correct cc name
#                 cc = control.Control(self.side,self.baseName,size = indexJoint.getRadius() / 5) 
                cc = control.Control(self.side,self.baseName,size = self.size)
                cc.circleCtrl()
                self.indexCc.append(cc.control)
                
                #create sdk grp
                sdkGrp = pm.group(em = 1,n = nameUtils.getUniqueName(self.side,self.fingerName[1] + self.fingerJointName[num],'SDK'))
                self.indexSdks.append(sdkGrp)

                #align cc,sdk grp
                pm.xform(cc.controlGrp,ws = 1,matrix = indexJoint.worldMatrix.get())
                pm.xform(sdkGrp,ws = 1,matrix = indexJoint.worldMatrix.get())
                
                cc.control.setParent(sdkGrp)
                sdkGrp.setParent(cc.controlGrp)                  
                
                #clean up and rename
                pm.rename(cc.control,nameUtils.getUniqueName(self.side,self.fingerName[1] + self.fingerJointName[num],'cc'))
                pm.rename(cc.controlGrp,nameUtils.getUniqueName(self.side,self.fingerName[1] + self.fingerJointName[num],'grp'))
                pm.delete(cc.control,ch=1)
                
        #jj clean up
        for num,ctrl in enumerate(self.indexCc):
            self.indexChain.chain[num].setParent(ctrl)
            if num > 0 :
                ctrl.getParent().getParent().setParent(self.indexChain.chain[num - 1])
                
        #index clean up       
        self.indexCc[0].getParent().getParent().setParent(self.indexGrp )
        pm.rename(self.indexChain.chain[-1],nameUtils.getUniqueName(self.side,self.fingerName[1]  + self.fingerJointName[4],'je')) 
        
        if self.fingerNum > 2:
            #create mid cc ctrl
            for num,midJoint in enumerate(self.midChain.chain):
                #correct jj name
                pm.rename(midJoint,nameUtils.getUniqueName(self.side,self.fingerName[2] + self.fingerJointName[num],'jj'))
                                        
                if num < self.midChain.chainLength() - 1:                
                    #create sdk and correct cc name
    #                 cc = control.Control(self.side,self.baseName,size = midJoint.getRadius() / 5) 
                    cc = control.Control(self.side,self.baseName,size = self.size) 
                    cc.circleCtrl()
                    self.midCc.append(cc.control)
                    
                    #create sdk grp
                    sdkGrp = pm.group(em = 1,n = nameUtils.getUniqueName(self.side,self.fingerName[2] + self.fingerJointName[num],'SDK'))
                    self.midSdks.append(sdkGrp)
                              
                    #align cc grp
                    pm.xform(cc.controlGrp,ws = 1,matrix = midJoint.worldMatrix.get())
                    pm.xform(sdkGrp,ws = 1,matrix = midJoint.worldMatrix.get())
    
                    cc.control.setParent(sdkGrp)
                    sdkGrp.setParent(cc.controlGrp) 
                    
                    #clean up and rename                
                    pm.rename(cc.control,nameUtils.getUniqueName(self.side,self.fingerName[2] + self.fingerJointName[num],'cc'))
                    pm.rename(cc.controlGrp,nameUtils.getUniqueName(self.side,self.fingerName[2] + self.fingerJointName[num],'grp'))    
                    pm.delete(cc.control,ch=1)
                    
            #jj clean up
            for num,ctrl in enumerate(self.midCc):
                self.midChain.chain[num].setParent(ctrl)
                if num > 0 :
                    ctrl.getParent().getParent().setParent(self.midChain.chain[num - 1])
                    
            #mid clean up       
            self.midCc[0].getParent().getParent().setParent(self.midGrp )
            pm.rename(self.midChain.chain[-1],nameUtils.getUniqueName(self.side,self.fingerName[2]  + self.fingerJointName[4],'je'))                 
        
        if self.fingerNum > 3:               
            #create ring cc ctrl
            for num,ringJoint in enumerate(self.ringChain.chain):
                #correct jj name
                pm.rename(ringJoint,nameUtils.getUniqueName(self.side,self.fingerName[3] + self.fingerJointName[num],'jj'))
                                        
                if num < self.ringChain.chainLength() - 1:                
                    #create sdk and correct cc name
    #                 cc = control.Control(self.side,self.baseName,size = ringJoint.getRadius() / 5) 
                    cc = control.Control(self.side,self.baseName,size = self.size) 
                    cc.circleCtrl()
                    self.ringCc.append(cc.control)                
                    
                    #create sdk grp
                    sdkGrp = pm.group(em = 1,n = nameUtils.getUniqueName(self.side,self.fingerName[3] + self.fingerJointName[num],'SDK'))                
                    self.ringSdks.append(sdkGrp)           
                         
                    #align cc grp
                    pm.xform(cc.controlGrp,ws = 1,matrix = ringJoint.worldMatrix.get())
                    pm.xform(sdkGrp,ws = 1,matrix = ringJoint.worldMatrix.get())     
                    
                    cc.control.setParent(sdkGrp)
                    sdkGrp.setParent(cc.controlGrp) 
                    
                    #clean up and rename
                    pm.rename(cc.control,nameUtils.getUniqueName(self.side,self.fingerName[3] + self.fingerJointName[num],'cc'))
                    pm.rename(cc.controlGrp,nameUtils.getUniqueName(self.side,self.fingerName[3] + self.fingerJointName[num],'grp'))
                    pm.delete(cc.control,ch=1)
            
            #jj clean up
            for num,ctrl in enumerate(self.ringCc):
                self.ringChain.chain[num].setParent(ctrl)
                if num > 0 :
                    ctrl.getParent().getParent().setParent(self.ringChain.chain[num - 1])
                    
            #ring clean up       
            self.ringCc[0].getParent().getParent().setParent(self.ringGrp )
            pm.rename(self.ringChain.chain[-1],nameUtils.getUniqueName(self.side,self.fingerName[3]  + self.fingerJointName[4],'je'))          
        
        if self.fingerNum > 4:
            #create pinky cc ctrl
            for num,pinkyJoint in enumerate(self.pinkyChain.chain):
                #correct jj name
                pm.rename(pinkyJoint,nameUtils.getUniqueName(self.side,self.fingerName[4] + self.fingerJointName[num],'jj'))
                                     
                if num < self.pinkyChain.chainLength() - 1:                
                    #create sdk and correct cc name
    #                 cc = control.Control(self.side,self.baseName,size = pinkyJoint.getRadius() / 5) 
                    cc = control.Control(self.side,self.baseName,size = self.size) 
                    cc.circleCtrl()
                    self.pinkyCc.append(cc.control)   
                    
                    #create sdk grp
                    sdkGrp = pm.group(em = 1,n = nameUtils.getUniqueName(self.side,self.fingerName[4] + self.fingerJointName[num],'SDK'))                
                    self.pinkySdks.append(sdkGrp)                     
                    
                    #align cc grp
                    pm.xform(cc.controlGrp,ws = 1,matrix = pinkyJoint.worldMatrix.get())
                    pm.xform(sdkGrp,ws = 1,matrix = pinkyJoint.worldMatrix.get())     
                    
                    cc.control.setParent(sdkGrp)
                    sdkGrp.setParent(cc.controlGrp) 
                    
                    #clean up and rename  
                    pm.rename(cc.control,nameUtils.getUniqueName(self.side,self.fingerName[4] + self.fingerJointName[num],'cc'))
                    pm.rename(cc.controlGrp,nameUtils.getUniqueName(self.side,self.fingerName[4] + self.fingerJointName[num],'grp'))
                    pm.delete(cc.control,ch=1)
                    
            #jj clean up
            for num,ctrl in enumerate(self.pinkyCc):
                self.pinkyChain.chain[num].setParent(ctrl)
                if num > 0 :
                    ctrl.getParent().getParent().setParent(self.pinkyChain.chain[num - 1])
                    
            #pinky clean up       
            self.pinkyCc[0].getParent().getParent().setParent(self.pinkyGrp )
            pm.rename(self.ringChain.chain[-1],nameUtils.getUniqueName(self.side,self.fingerName[4]  + self.fingerJointName[4],'je'))                       
           
    def __partialJoint(self):
        
        #Init
        self.thumbPartial = []
        self.indexPartial = []
        self.midPartial = []
        self.ringPartial = []
        self.pinkyPartial = []
        
        #thumb
        for num,joint in enumerate(self.thumbChain.chain):
            #create partial jj
            if num < (self.thumbChain.chainLength() - 1) and num != 0:
                partial = pm.joint(n = nameUtils.getUniqueName(self.side,self.fingerName[0]  + self.fingerJointName[num] + self.fingerJointName[5],'jj'),
                                   position = (0,0,0),orientation = (0,0,0))
                    
                pm.xform(partial,ws = 1,matrix = joint.worldMatrix.get())
                partial.setParent(self.thumbCc[num].getParent().getParent())
                
                #node name
                plusAverageName = nameUtils.getUniqueName(self.side,self.fingerName[0]  + self.fingerJointName[num] + self.fingerJointName[5],'PMA')
                multipleDivideName = nameUtils.getUniqueName(self.side,self.fingerName[0]  + self.fingerJointName[num] + self.fingerJointName[5],'MDN')
                 
                #create node 
                plusAverage = pm.createNode('plusMinusAverage',n = plusAverageName)
                multipleDivide = pm.createNode('multiplyDivide',n = multipleDivideName)
                 
                #connect node
                #PMA
                self.thumbSdks[num].rx.connect(plusAverage.input3D[0].input3Dx)
                self.thumbSdks[num].ry.connect(plusAverage.input3D[0].input3Dy)
                self.thumbSdks[num].rz.connect(plusAverage.input3D[0].input3Dz)
                self.thumbCc[num].rx.connect(plusAverage.input3D[1].input3Dx)
                self.thumbCc[num].ry.connect(plusAverage.input3D[1].input3Dy)
                self.thumbCc[num].rz.connect(plusAverage.input3D[1].input3Dz)
                 
                #MDN
                #input 
                plusAverage.output3Dx.connect(multipleDivide.input1X)
                plusAverage.output3Dy.connect(multipleDivide.input1Y)
                plusAverage.output3Dz.connect(multipleDivide.input1Z)
                multipleDivide.input2X.set(0.5)
                multipleDivide.input2Y.set(0.5)
                multipleDivide.input2Z.set(0.5)
                #output
                multipleDivide.output.outputX.connect(partial.rx)
                multipleDivide.output.outputY.connect(partial.ry)
                multipleDivide.output.outputZ.connect(partial.rz)
                
                #jointOrient
                for jointOrient in ['jointOrientX','jointOrientY','jointOrientZ']:
                    partial.attr(jointOrient).set(0)
                    
        #index
        for num,joint in enumerate(self.indexChain.chain):
            #create partial jj
            if num < (self.indexChain.chainLength() - 1) and num != 0:
                partial = pm.joint(n = nameUtils.getUniqueName(self.side,self.fingerName[1]  + self.fingerJointName[num] + self.fingerJointName[5],'jj'),
                                   position = (0,0,0))
                pm.xform(partial,ws = 1,matrix = joint.worldMatrix.get())
                partial.setParent(self.indexCc[num].getParent().getParent())
                
                #node name
                plusAverageName = nameUtils.getUniqueName(self.side,self.fingerName[1]  + self.fingerJointName[num] + self.fingerJointName[5],'PMA')
                multipleDivideName = nameUtils.getUniqueName(self.side,self.fingerName[1]  + self.fingerJointName[num] + self.fingerJointName[5],'MDN')
                
                #create node 
                plusAverage = pm.createNode('plusMinusAverage',n = plusAverageName)
                multipleDivide = pm.createNode('multiplyDivide',n = multipleDivideName)
                
                #connect node
                #PMA
                self.indexSdks[num].rx.connect(plusAverage.input3D[0].input3Dx)
                self.indexSdks[num].ry.connect(plusAverage.input3D[0].input3Dy)
                self.indexSdks[num].rz.connect(plusAverage.input3D[0].input3Dz)
                self.indexCc[num].rx.connect(plusAverage.input3D[1].input3Dx)
                self.indexCc[num].ry.connect(plusAverage.input3D[1].input3Dy)
                self.indexCc[num].rz.connect(plusAverage.input3D[1].input3Dz)
                
                #MDN
                #input 
                plusAverage.output3Dx.connect(multipleDivide.input1X)
                plusAverage.output3Dy.connect(multipleDivide.input1Y)
                plusAverage.output3Dz.connect(multipleDivide.input1Z)
                multipleDivide.input2X.set(0.5)
                multipleDivide.input2Y.set(0.5)
                multipleDivide.input2Z.set(0.5)
                #output
                multipleDivide.output.outputX.connect(partial.rx)
                multipleDivide.output.outputY.connect(partial.ry)
                multipleDivide.output.outputZ.connect(partial.rz)
                
                #jointOrient
                for jointOrient in ['jointOrientX','jointOrientY','jointOrientZ']:
                    partial.attr(jointOrient).set(0)
                    
        if self.fingerNum > 2:
            #middle
            for num,joint in enumerate(self.midChain.chain):
                #create partial jj
                if num < (self.midChain.chainLength() - 1) and num != 0:
                    partial = pm.joint(n = nameUtils.getUniqueName(self.side,self.fingerName[2]  + self.fingerJointName[num] + self.fingerJointName[5],'jj'),
                                       position = (0,0,0))
                    pm.xform(partial,ws = 1,matrix = joint.worldMatrix.get())
                    partial.setParent(self.midCc[num].getParent().getParent())
                    
                    #node name
                    plusAverageName = nameUtils.getUniqueName(self.side,self.fingerName[2]  + self.fingerJointName[num] + self.fingerJointName[5],'PMA')
                    multipleDivideName = nameUtils.getUniqueName(self.side,self.fingerName[2]  + self.fingerJointName[num] + self.fingerJointName[5],'MDN')
                    
                    #create node 
                    plusAverage = pm.createNode('plusMinusAverage',n = plusAverageName)
                    multipleDivide = pm.createNode('multiplyDivide',n = multipleDivideName)
                    
                    #connect node
                    #PMA
                    self.midSdks[num].rx.connect(plusAverage.input3D[0].input3Dx)
                    self.midSdks[num].ry.connect(plusAverage.input3D[0].input3Dy)
                    self.midSdks[num].rz.connect(plusAverage.input3D[0].input3Dz)
                    self.midCc[num].rx.connect(plusAverage.input3D[1].input3Dx)
                    self.midCc[num].ry.connect(plusAverage.input3D[1].input3Dy)
                    self.midCc[num].rz.connect(plusAverage.input3D[1].input3Dz)
                    
                    #MDN
                    #input 
                    plusAverage.output3Dx.connect(multipleDivide.input1X)
                    plusAverage.output3Dy.connect(multipleDivide.input1Y)
                    plusAverage.output3Dz.connect(multipleDivide.input1Z)
                    multipleDivide.input2X.set(0.5)
                    multipleDivide.input2Y.set(0.5)
                    multipleDivide.input2Z.set(0.5)
                    #output
                    multipleDivide.output.outputX.connect(partial.rx)
                    multipleDivide.output.outputY.connect(partial.ry)
                    multipleDivide.output.outputZ.connect(partial.rz)
                    
                    #jointOrient
                    for jointOrient in ['jointOrientX','jointOrientY','jointOrientZ']:
                        partial.attr(jointOrient).set(0)        
        
        if self.fingerNum > 3:
            #ring
            for num,joint in enumerate(self.ringChain.chain):
                #create partial jj
                if num < (self.ringChain.chainLength() - 1) and num != 0:
                    partial = pm.joint(n = nameUtils.getUniqueName(self.side,self.fingerName[3]  + self.fingerJointName[num] + self.fingerJointName[5],'jj'),
                                       position = (0,0,0))
                    pm.xform(partial,ws = 1,matrix = joint.worldMatrix.get())
                    partial.setParent(self.ringCc[num].getParent().getParent())
                    
                    #node name
                    plusAverageName = nameUtils.getUniqueName(self.side,self.fingerName[3]  + self.fingerJointName[num] + self.fingerJointName[5],'PMA')
                    multipleDivideName = nameUtils.getUniqueName(self.side,self.fingerName[3]  + self.fingerJointName[num] + self.fingerJointName[5],'MDN')
                    
                    #create node 
                    plusAverage = pm.createNode('plusMinusAverage',n = plusAverageName)
                    multipleDivide = pm.createNode('multiplyDivide',n = multipleDivideName)
                    
                    #connect node
                    #PMA
                    self.ringSdks[num].rx.connect(plusAverage.input3D[0].input3Dx)
                    self.ringSdks[num].ry.connect(plusAverage.input3D[0].input3Dy)
                    self.ringSdks[num].rz.connect(plusAverage.input3D[0].input3Dz)
                    self.ringCc[num].rx.connect(plusAverage.input3D[1].input3Dx)
                    self.ringCc[num].ry.connect(plusAverage.input3D[1].input3Dy)
                    self.ringCc[num].rz.connect(plusAverage.input3D[1].input3Dz)
                    
                    #MDN
                    #input 
                    plusAverage.output3Dx.connect(multipleDivide.input1X)
                    plusAverage.output3Dy.connect(multipleDivide.input1Y)
                    plusAverage.output3Dz.connect(multipleDivide.input1Z)
                    multipleDivide.input2X.set(0.5)
                    multipleDivide.input2Y.set(0.5)
                    multipleDivide.input2Z.set(0.5)
                    #output
                    multipleDivide.output.outputX.connect(partial.rx)
                    multipleDivide.output.outputY.connect(partial.ry)
                    multipleDivide.output.outputZ.connect(partial.rz)
                    
                    #jointOrient
                    for jointOrient in ['jointOrientX','jointOrientY','jointOrientZ']:
                        partial.attr(jointOrient).set(0)
                                
        if self.fingerNum > 4 :
            #pinky
            for num,joint in enumerate(self.pinkyChain.chain):
                #create partial jj
                if num < (self.pinkyChain.chainLength() - 1) and num != 0:
                    partial = pm.joint(n = nameUtils.getUniqueName(self.side,self.fingerName[4]  + self.fingerJointName[num] + self.fingerJointName[5],'jj'),
                                       position = (0,0,0))
                    pm.xform(partial,ws = 1,matrix = joint.worldMatrix.get())
                    partial.setParent(self.pinkyCc[num].getParent().getParent())
                    
                    #node name
                    plusAverageName = nameUtils.getUniqueName(self.side,self.fingerName[4]  + self.fingerJointName[num] + self.fingerJointName[5],'PMA')
                    multipleDivideName = nameUtils.getUniqueName(self.side,self.fingerName[4]  + self.fingerJointName[num] + self.fingerJointName[5],'MDN')
                    
                    #create node 
                    plusAverage = pm.createNode('plusMinusAverage',n = plusAverageName)
                    multipleDivide = pm.createNode('multiplyDivide',n = multipleDivideName)
                    
                    #connect node
                    #PMA
                    self.pinkySdks[num].rx.connect(plusAverage.input3D[0].input3Dx)
                    self.pinkySdks[num].ry.connect(plusAverage.input3D[0].input3Dy)
                    self.pinkySdks[num].rz.connect(plusAverage.input3D[0].input3Dz)
                    self.pinkyCc[num].rx.connect(plusAverage.input3D[1].input3Dx)
                    self.pinkyCc[num].ry.connect(plusAverage.input3D[1].input3Dy)
                    self.pinkyCc[num].rz.connect(plusAverage.input3D[1].input3Dz)
                    
                    #MDN
                    #input 
                    plusAverage.output3Dx.connect(multipleDivide.input1X)
                    plusAverage.output3Dy.connect(multipleDivide.input1Y)
                    plusAverage.output3Dz.connect(multipleDivide.input1Z)
                    multipleDivide.input2X.set(0.5)
                    multipleDivide.input2Y.set(0.5)
                    multipleDivide.input2Z.set(0.5)
                    #output
                    multipleDivide.output.outputX.connect(partial.rx)
                    multipleDivide.output.outputY.connect(partial.ry)
                    multipleDivide.output.outputZ.connect(partial.rz)
                    
                    #jointOrient
                    for jointOrient in ['jointOrientX','jointOrientY','jointOrientZ']:
                        partial.attr(jointOrient).set(0)             
           
    def __setSDK(self):

        #prepare chr:
        chr = ['x','y','z']
        
        #finger list:
   
        #set Append val List for index min ring pinky:
        #set Append val List fot thumb:
        thumbAppendMaxRotList = []
        thumbAppendMinRotList = []
        indexAppendMaxRotList = []
        indexAppendMinRotList = []
        midAppendMaxRotList = []
        midAppendMinRotList = []
        ringAppendMaxRotList = []
        ringAppendMinRotList = []                
        pinkyAppendMaxRotList = []
        pinkyAppendMinRotList = []                
        
        #set Main extreme list for index min ring pinky:
        thumbMainMaxRotList = []
        thumbMainMinRotList = []        
        indexMainMaxRotList = []
        indexMainMinRotList = []
        midMainMaxRotList = []
        midMainMinRotList = []
        ringMainMaxRotList = []
        ringMainMinRotList = []
        pinkyMainMaxRotList = []
        pinkyMainMinRotList = []
        
        #fist_a
        #fist_a max(10) val:
        thumbFistaMaxRotList = [[14.015346, 30.186936, -29.128069],[-30.812735, 11.812918, -1.1788441],[-3.72054, 100.88849, -27.580464]]
        indexFistaMaxRotList = [[0.0, 1.1667451, 0.0],[7.7256914, 98.47196, -6.9225698],[-5.0864835, 109.12878, -14.33877],[0.0, 121.35306, 0.0]]
        midFistaMaxRotList = [[0.0, 0.0, 0.0],[1.343452, 94.24476, -0.17447495],[-1.2531719, 111.28286, -3.2134328],[0.0, 111.31801, 0.0]]
        ringFistaMaxRotList = [[-2.2915976, 0.99224884, 0.3515861],[-1.654204, 94.229347, 8.2182298],[1.4022289, 107.094, 4.5496722],[0.0, 118.21848, 0.0]]
        pinkyFistaMaxRotList = [[-3.4711895, 4.0933869, 1.0393476],[-3.908681, 104.27619, 16.853265],[3.2222396, 102.18746, 14.587789],[0.0, 96.374496, 0.0]]
        
        thumbAppendMaxRotList.append(thumbFistaMaxRotList)
        indexAppendMaxRotList.append(indexFistaMaxRotList)
        midAppendMaxRotList.append(midFistaMaxRotList)
        ringAppendMaxRotList.append(ringFistaMaxRotList)
        pinkyAppendMaxRotList.append(pinkyFistaMaxRotList)
        
        #fist_a min(-3) val:    
        thumbFistaMinRotList = [[-4.2046040707, -9.05608119046, 8.73842055475],[9.243820566, -3.54387566227, 0.0],[1.11616195298, -30.2665488136, 8.27413964669]]    
        indexFistaMinRotList = [[0.0, 0.0, 0.0], [2.3656792422, -23.6599771482, 1.9016638177], [1.52594527386, -22.6379875224, 4.30163088994], [0.0, -26.3052739235, 0.0]]
        midFistaMinRotList = [[0.0, 0.0, 0.0], [0.0, -13.0502537762, 0.0], [0.0, -23.0761814451, 0.964029917432], [0.0, -23.0867256252, 0.0]]
        ringFistaMinRotList = [[0.0, 0.0, 0.0], [-8.0276, -10.3753295339, -0.732478856346], [0.0, -17.8428903421, -1.36490170652], [0.0, -21.1802374187, 0.0]]
        pinkyFistaMinRotList = [[1.04135682811, -1.22801612104, 0.0], [-8.96452963728, -10.9554773142, -2.95571135541], [-0.966671923269, -14.4907648544, -4.37633648762], [0.0, -12.7468772018, 0.0]]
        
        thumbAppendMinRotList.append(thumbFistaMinRotList)
        indexAppendMinRotList.append(indexFistaMinRotList)    
        midAppendMinRotList.append(midFistaMinRotList)        
        ringAppendMinRotList.append(ringFistaMinRotList)    
        pinkyAppendMinRotList.append(pinkyFistaMinRotList)    
        
        #fist_b
        #fist_b max(10) val:
        thumbFistbMaxRotList = [[-15.133029, 9.4707533, -13.099304],[-5.9042621, 26.54775, -8.1561952],[6.4844431, 80.168132, -6.1445437]]
        indexFistbMaxRotList = [[0.0, 0.0, 0.0],[4.4223436, 66.184789, 1.8546305],[0.0, 101.20612, 0.0],[0.0, 75.878746, 0.0]]
        midFistbMaxRotList = [[0.0, 0.0, 0.0],[0.0, 81.00373, 0.0],[0.0, 97.623089, 0.0],[0.0, 98.548929, 0.0]]
        ringFistbMaxRotList = [[0.0, 0.0, 0.0],[-4.8254718, 85.586453, 2.4808469],[0.0, 93.487201, 0.0],[0.0, 97.57188, 0.0]]
        pinkyFistbMaxRotList = [[0.0, 0.0, 0.0],[-11.238872, 91.357247, 3.8876141],[0.0, 90.796196, 0.0],[0.0, 94.880874, 0.0]]
        
        thumbAppendMaxRotList.append(thumbFistbMaxRotList)
        indexAppendMaxRotList.append(indexFistbMaxRotList)
        midAppendMaxRotList.append(midFistbMaxRotList)
        ringAppendMaxRotList.append(ringFistbMaxRotList)
        pinkyAppendMaxRotList.append(pinkyFistbMaxRotList)        

        #fist_b min(-3)val:
        thumbFistbMinRotList = [[4.5399086813, -2.84122596374, 3.92979114471],[1.77127871515, -7.96432593749, 2.44685860124],[-1.94533298514, -24.0504396995, 1.84336321642]]
        indexFistbMinRotList = [[0.0, 0.0, 0.0],[-1.32670302602, -19.8554351973, 0.0],[0.0, -30.3618382339, 0.0],[0.0, -22.7636215909, 0.0]]
        midFistbMinRotList = [[0.0, 0.0, 0.0],[0.0, -24.3011201928, 0.0],[0.0, -29.2869273013, 0.0],[0.0, -29.5646757999, 0.0]]
        ringFistbMinRotList = [[0.0, 0.0, 0.0],[1.44764159413, -25.6759372289, 0.0],[0.0, -28.0461595706, 0.0],[0.0, -29.2715641599, 0.0]]
        pinkyFistbMinRotList = [[0.0, 0.0, 0.0],[3.37166184668, -27.4071741155, -1.16628417085],[0.0, -27.2388580576, 0.0],[0.0, -28.4642617121, 0.0]]

        thumbAppendMinRotList.append(thumbFistbMinRotList)
        indexAppendMinRotList.append(indexFistbMinRotList)
        midAppendMinRotList.append(midFistbMinRotList)        
        ringAppendMinRotList.append(ringFistbMinRotList)    
        pinkyAppendMinRotList.append(pinkyFistbMinRotList)            
        
        #relax_a        
        #relax_a max(10) val:
        thumbRelaxaMaxRotList = [[21.260128, 2.1268255, 9.3753018],[0.59979165, -2.4811551, -25.320981],[0.0, 18.954413, 0.0]]
        indexRelaxaMaxRotList = [[0.0, 0.0, 0.0],[-0.89780606, -8.5116474, -9.925511],[0.0, 15.239331, 0.0],[0.0, 15.239331, 0.0]]
        midRelaxaMaxRotList = [[0.0, 0.0, 0.0],[-0.14373821, 4.6882137, -0.50410896],[0.0, 32.523238, 0.0],[0.0, 32.523238, 0.0]]
        ringRelaxaMaxRotList = [[-2.9928762, 0.0, 0.0],[4.1312803, 15.615173, 7.78713],[0.0, 30.371118, 0.0],[0.0, 30.371118, 0.0]]
        pinkyRelaxaMaxRotList = [[-1.8613005, 0.056215787, 1.7302502],[12.382909, 26.61312, 15.826518],[0.0, 45.728939, 0.0],[0.0, 45.728939, 0.0]]
                
        thumbAppendMaxRotList.append(thumbRelaxaMaxRotList)        
        indexAppendMaxRotList.append(indexRelaxaMaxRotList)
        midAppendMaxRotList.append(midRelaxaMaxRotList)
        ringAppendMaxRotList.append(ringRelaxaMaxRotList)
        pinkyAppendMaxRotList.append(pinkyRelaxaMaxRotList)        
        
        #relax_a  min(-3)val:          
        thumbRelaxaMinRotList = [[-6.37803851339, 0.0, -2.81259097677],[0.0, 0.0, 7.59629461146],[0.0, -5.68632420084, 0.0]]
        indexRelaxaMinRotList = [[0.0, 0.0, 0.0],[0.0, 2.55349438396, 2.97765346574],[0.0, -4.57179902403, 0.0],[0.0, -4.57179902403, 0.0]]
        midRelaxaMinRotList = [[0.0, 0.0, 0.0],[0.0, -1.40646424112, 0.0],[0.0, -9.75697114332, 0.0],[0.0, -9.75697114332, 0.0]]
        ringRelaxaMinRotList = [[0.897862892745, 0.0, 0.0],[-1.23938408908, -4.68455226138, -2.33613911906],[0.0, -9.11133613376, 0.0],[0.0, -9.11133613376, 0.0]]
        pinkyRelaxaMinRotList = [[0.0, 0.0, 0.0],[-3.7148726673, -7.98393590273, -4.74795583361],[0.0, -13.7186819746, 0.0],[0.0, -13.7186819746, 0.0]]
        
        thumbAppendMinRotList.append(thumbRelaxaMinRotList) 
        indexAppendMinRotList.append(indexRelaxaMinRotList) 
        midAppendMinRotList.append(midRelaxaMinRotList)        
        ringAppendMinRotList.append(ringRelaxaMinRotList)    
        pinkyAppendMinRotList.append(pinkyRelaxaMinRotList)            
        
        #relax_b        
        #relax_b max(10) val:        
        thumbRelaxbMaxRotList = [[-1.4470234, 7.0237145, 10.813747],[2.8576592, 24.041129, 4.7068679],[0.21696092, 16.943779, -0.16243521]]
        indexRelaxbMaxRotList = [[0.0, 0.0, 0.0],[4.6833866, 5.8816114, -0.1751071],[0.0, 10.100644, 0.0],[0.0, 10.100644, 0.0]]
        midRelaxbMaxRotList = [[0.0, 0.0, 0.0],[0.0, 15.223175, 0.0],[0.0, 10.308678, 0.0],[0.0, 10.308678, 0.0]]
        ringRelaxbMaxRotList = [[0.0, 0.0, 0.0],[-8.0276, 17.893472, 1.7329901],[0.0, 14.285307, 0.0],[0.0, 14.285307, 0.0]]
        pinkyRelaxbMaxRotList = [[0.0, 0.0, 0.0],[-10.137134, 20.327381, 2.100268],[0.0, 16.165473, 0.0],[0.0, 16.165473, 0.0]]
         
        thumbAppendMaxRotList.append(thumbRelaxbMaxRotList)     
        indexAppendMaxRotList.append(indexRelaxbMaxRotList)
        midAppendMaxRotList.append(midRelaxbMaxRotList)
        ringAppendMaxRotList.append(ringRelaxbMaxRotList)
        pinkyAppendMaxRotList.append(pinkyRelaxbMaxRotList)        
        
        #relax_b min(-3) val: 
        thumbRelaxbMinRotList = [[0.0, -2.10711457828, -3.24412391414],[0.0, -7.21233926037, -1.41206046319],[0.0, -5.08313310676, 0.0]]
        indexRelaxbMinRotList = [[0.0, 0.0, 0.0],[-1.40501603744, -1.76448329217, 0.0],[0.0, -3.0301932355, 0.0],[0.0, -3.0301932355, 0.0]]
        midRelaxbMinRotList = [[0.0, 0.0, 0.0],[0.0, -4.56695278412, 0.0],[0.0, -3.09260392401, 0.0],[0.0, -3.09260392401, 0.0]]
        ringRelaxbMinRotList = [[0.0, 0.0, 0.0],[2.40827997571, -5.36804128933, 0.0],[0.0, -4.28559214217, 0.0],[0.0, -4.28559214217, 0.0]]
        pinkyRelaxbMinRotList = [[0.0, 0.0, 0.0],[3.04113989245, -6.09821425613, 0.0],[0.0, -4.84964199343, 0.0],[0.0, -4.84964199343, 0.0]]
                 
        thumbAppendMinRotList.append(thumbRelaxbMinRotList)                 
        indexAppendMinRotList.append(indexRelaxbMinRotList)
        midAppendMinRotList.append(midRelaxbMinRotList)        
        ringAppendMinRotList.append(ringRelaxbMinRotList)    
        pinkyAppendMinRotList.append(pinkyRelaxbMinRotList)            
            
        #relax_c        
        #relax_c max(10) val:        
        thumbRelaxcMaxRotList = [[16.415574, 17.704726, -15.145172],[-0.19108961, 26.227951, 1.1962875],[0.0, 24.948623, 0.0]]
        indexRelaxcMaxRotList = [[0.0, 0.0, 0.0],[5.2831314, 31.345176, -3.2099818],[0.0, 22.91704, 0.0],[0.0, 22.91704, 0.0]]
        midRelaxcMaxRotList = [[0.0, 0.0, 0.0],[0.0, 46.799998, 0.0],[0.0, 38.519999, 0.0],[0.0, 38.519999, 0.0]]
        ringRelaxcMaxRotList = [[-2.8230663, 0.0, 0.0],[-4.8881484, 52.212118, 6.271701],[0.0, 43.664156, 0.0],[0.0, 43.664156, 0.0]]
        pinkyRelaxcMaxRotList = [[-2.8230663, 0.0, 0.0],[-3.8132578, 54.511244, 5.3288443],[0.0, 46.053723, 0.0],[0.0, 46.053723, 0.0]]
                                                
        thumbAppendMaxRotList.append(thumbRelaxcMaxRotList)                  
        indexAppendMaxRotList.append(indexRelaxcMaxRotList)      
        midAppendMaxRotList.append(midRelaxcMaxRotList)
        ringAppendMaxRotList.append(ringRelaxcMaxRotList)
        pinkyAppendMaxRotList.append(pinkyRelaxcMaxRotList)              
        
        #relax_c min(-3) val:
        thumbRelaxcMinRotList = [[-4.9246721435, -5.31141800316, 4.54355182057],[0.0, -7.86838517065, 0.0],[0.0, -7.48458766703, 0.0]]
        indexRelaxcMinRotList = [[0.0, 0.0, 0.0],[-1.58493940724, -9.40355275552, 0.962994550952],[0.0, -6.87511250747, 0.0],[0.0, -6.87511250747, 0.0]]
        midRelaxcMinRotList = [[0.0, 0.0, 0.0],[0.0, -14.0399988485, 0.0],[0.0, -11.5560003809, 0.0],[0.0, -11.5560003809, 0.0]]
        ringRelaxcMinRotList = [[0.0, 0.0, 0.0],[1.46644448156, -15.6636355533, -1.88151040577],[0.0, -13.099245447, 0.0],[0.0, -13.099245447, 0.0]]
        pinkyRelaxcMinRotList = [[0.0, 0.0, 0.0],[1.14397733976, -16.3533737924, -1.59865341533],[0.0, -13.8161171568, 0.0],[0.0, -13.8161171568, 0.0]]
                 
        thumbAppendMinRotList.append(thumbRelaxcMinRotList)         
        indexAppendMinRotList.append(indexRelaxcMinRotList)
        midAppendMinRotList.append(midRelaxcMinRotList)        
        ringAppendMinRotList.append(ringRelaxcMinRotList)    
        pinkyAppendMinRotList.append(pinkyRelaxcMinRotList)            
        
        #relax_d        
        #relax_d max(10) val:           
        thumbRelaxdMaxRotList = [[-1.4470234, 7.0237145, 10.813747],[4.8008923, 9.7098401, -6.9178941],[-2.4475809, 36.602661, -3.7445253]]   
        indexRelaxdMaxRotList = [[0.0, 0.0, 0.0],[5.4160948, 12.535184, 1.2137211],[0.0, 10.100644, -1.7270777e-08],[6.8093491e-09, 10.100644, -1.6329651e-08]]
        midRelaxdMaxRotList = [[0.0, 0.0, 0.0],[-1.7709299, 22.999166, -1.5032809],[6.9404626e-09, 10.308678, -1.6351366e-08],[9.7545475e-09, 10.308678, -1.4845411e-08]]
        ringRelaxdMaxRotList = [[0.0, 0.0, 0.0],[-9.0447572, 27.937911, -2.3253179],[8.2228049e-09, 14.285307, -1.5505428e-08],[1.1794547e-08, 14.285307, -1.2996997e-08]]
        pinkyRelaxdMaxRotList = [[0.0, 0.0, 0.0],[-15.723218, 33.076844, -1.6909839],[0.0, 16.165473, 0.0],[0.0, 16.165473, 0.0]]
        
        thumbAppendMaxRotList.append(thumbRelaxdMaxRotList)
        indexAppendMaxRotList.append(indexRelaxdMaxRotList)  
        midAppendMaxRotList.append(midRelaxdMaxRotList)
        ringAppendMaxRotList.append(ringRelaxdMaxRotList)
        pinkyAppendMaxRotList.append(pinkyRelaxdMaxRotList)            

        #relax_d min(-3) val:
        thumbRelaxdMinRotList = [[0.0, -2.10711457828, -3.24412391414],[-1.44026767113, -2.91295215522, 2.0753680697],[0.0, -10.9807975671, 1.1233574891]]
        indexRelaxdMinRotList = [[0.0, 0.0, 0.0],[-1.62482857459, -3.76055524696, 0.0],[0.0, -3.0301932355, 0.0],[0.0, -3.0301932355, 0.0]]
        midRelaxdMinRotList = [[0.0, 0.0, 0.0],[0.0, -6.89974964616, 0.0],[0.0, -3.09260392401, 0.0],[0.0, -3.09260392401, 0.0]]
        ringRelaxdMinRotList = [[0.0, 0.0, 0.0],[2.71342718955, -8.38137266181, 0.0],[0.0, -4.28559214217, 0.0],[0.0, -4.28559214217, 0.0]]
        pinkyRelaxdMinRotList = [[0.0, 0.0, 0.0],[4.71696534913, -9.92305375801, 0.0],[0.0, -4.84964199343, 0.0],[0.0, -4.84964199343, 0.0]]
                         
        thumbAppendMinRotList.append(thumbRelaxdMinRotList)                 
        indexAppendMinRotList.append(indexRelaxdMinRotList)
        midAppendMinRotList.append(midRelaxdMinRotList)        
        ringAppendMinRotList.append(ringRelaxdMinRotList)    
        pinkyAppendMinRotList.append(pinkyRelaxdMinRotList)         
        
        #relax_e         
        #relax_e max(10) val:       
        thumbRelaxeMaxRotList = [[16.415574, 17.704726, -15.145172],[-0.19108961, 26.227951, 1.1962875],[-1.715826, 40.044492, -3.6918888]]              
        indexRelaxeMaxRotList = [[0.0, 0.0, 0.0],[5.2831314, 31.345176, -3.2099818],[9.2055523e-09, 5.0979753, -1.5113549e-08],[1.0512118e-08, 12.199657, -1.4235765e-08]]
        midRelaxeMaxRotList = [[0.0, 0.0, 0.0],[0.0, 46.799998, 1.7771855e-08],[0.0, 38.519999, 2.5966873e-08],[0.0, 38.519999, 2.1833783e-07]]
        ringRelaxeMaxRotList = [[-2.8230663, 0.0, 0.0],[-4.8881484, 52.212118, 6.271701],[0.0, 47.306373, 0.0],[0.0, 47.306373, 0.0]]
        pinkyRelaxeMaxRotList = [[-2.8230663, 0.0, 0.0],[-11.348742, 55.622932, 9.5249724],[0.0, 46.053723, 0.0],[0.0, 46.053723, 0.0]]
                 
        thumbAppendMaxRotList.append(thumbRelaxeMaxRotList)                 
        indexAppendMaxRotList.append(indexRelaxeMaxRotList)         
        midAppendMaxRotList.append(midRelaxeMaxRotList)
        ringAppendMaxRotList.append(ringRelaxeMaxRotList)
        pinkyAppendMaxRotList.append(pinkyRelaxeMaxRotList)             
                
        #relax_e min(-3) val:
        thumbRelaxeMinRotList = [[-4.9246721435, -5.31141800316, 4.54355182057],[0.0, -7.86838517065, 0.0],[0.0, -12.0133485696, 1.10756668073]]
        indexRelaxeMinRotList = [[0.0, 0.0, 0.0],[-1.58493940724, -9.40355275552, 0.962994550952],[0.0, -1.52939260387, 0.0],[0.0, -3.65989711932, 0.0]]
        midRelaxeMinRotList = [[0.0, 0.0, 0.0],[0.0, -14.0399988485, 0.0],[0.0, -11.5560003809, 0.0],[0.0, -11.5560003809, 0.0]]
        ringRelaxeMinRotList = [[0.0, 0.0, 0.0],[1.46644448156, -15.6636355533, -1.88151040577],[0.0, -14.1919116307, 0.0],[0.0, -14.1919116307, 0.0]]
        pinkyRelaxeMinRotList = [[0.0, 0.0, 0.0],[3.4046228407, -16.6868815882, -2.85749193878],[0.0, -13.8161171568, 0.0],[0.0, -13.8161171568, 0.0]]
                 
        thumbAppendMinRotList.append(thumbRelaxeMinRotList)         
        indexAppendMinRotList.append(indexRelaxeMinRotList)   
        midAppendMinRotList.append(midRelaxeMinRotList)        
        ringAppendMinRotList.append(ringRelaxeMinRotList)    
        pinkyAppendMinRotList.append(pinkyRelaxeMinRotList)                 
         
        #grab_a 
        #grab_a max(10) val:        
        thumbGrabaMaxRotList = [[6.2972266, 7.3167996, -17.181614],[12.977213, -0.47780247, -17.957973],[0.0, 43.223566, 0.0]]
        indexGrabaMaxRotList = [[0.0, 0.0, 0.0],[-1.7635041, -8.5214628, -16.147383],[0.0, 41.94425, 0.0],[0.0, 44.280939, 0.0]]
        midGrabaMaxRotList = [[0.0, 0.0, 0.0],[-0.030713774, -5.1010537, -3.0009306],[0.0, 40.029996, 0.0],[0.0, 41.086042, 0.0]]
        ringGrabaMaxRotList = [[-2.9928762, 0.0, 0.0],[3.6224929, -2.4102271, 4.7080181],[0.0, 40.898433, 0.0],[0.0, 41.482517, 0.0]]
        pinkyGrabaMaxRotList = [[-1.8613005, 0.056215787, 1.7302502],[1.4394069, 0.14493989, 16.418532],[0.0, 43.58425, 0.0],[0.0, 52.072421, 0.0]]
        
        thumbAppendMaxRotList.append(thumbGrabaMaxRotList)  
        indexAppendMaxRotList.append(indexGrabaMaxRotList)
        midAppendMaxRotList.append(midGrabaMaxRotList)
        ringAppendMaxRotList.append(ringGrabaMaxRotList)
        pinkyAppendMaxRotList.append(pinkyGrabaMaxRotList)            
        
        #grab_a min(-3) val: 
        thumbGrabaMinRotList = [[-1.88916807572, -2.19504008654, 5.15448429452],[-3.89316354721, 0.0, 5.38739178149],[0.0, -12.9670684884, 0.0]]
        indexGrabaMinRotList = [[0.0, 0.0, 0.0],[0.0, 2.55643895266, 4.84421472464],[0.0, -12.5832744564, 0.0],[0.0, -13.284281742, 0.0]]
        midGrabaMinRotList = [[0.0, 0.0, 0.0],[0.0, 1.53031619331, 0.900279164949],[0.0, -12.0089988007, 0.0],[0.0, -12.3258143315, 0.0]]
        ringGrabaMinRotList = [[0.897862892745, 0.0, 0.0],[-1.08674781614, 0.0, -1.4124054644],[0.0, -12.2695308218, 0.0],[0.0, -12.4447552972, 0.0]]
        pinkyGrabaMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, -4.92555972899],[0.0, -13.0752754812, 0.0],[0.0, -15.6217261951, 0.0]]
                         
        thumbAppendMinRotList.append(thumbGrabaMinRotList)                         
        indexAppendMinRotList.append(indexGrabaMinRotList)   
        midAppendMinRotList.append(midGrabaMinRotList)        
        ringAppendMinRotList.append(ringGrabaMinRotList)    
        pinkyAppendMinRotList.append(pinkyGrabaMinRotList)                 
                
        #grab_b 
        #grab_b max(10) val:       
        thumbGrabbMaxRotList = [[6.2972266, 7.3167996, -17.181614],[12.977213, 11.173348, -17.957973],[0.0, 32.156193, 0.0]]
        indexGrabbMaxRotList = [[0.0, 0.0, 0.0],[-1.7635041, -8.5214628, -16.147383],[0.0, 20.931244, -1.7567324e-08],[0.0, 23.267933, -1.7348401e-08]]
        midGrabbMaxRotList = [[0.0, 0.0, 0.0],[-0.030713774, -2.9912371, -3.0009306],[0.0, 31.691439, -1.7747642e-08],[8.5345485e-09, 32.747485, -1.5588491e-08]]
        ringGrabbMaxRotList = [[-2.9928762, 0.0, 0.0],[-1.9605419, 10.418159, 11.084858],[0.0, 39.844309, 0.0],[0.0, 40.428393, 0.0]]
        pinkyGrabbMaxRotList = [[-1.8613005, 0.056215787, 1.7302502],[-1.9825828, 29.626945, 18.362295],[0.0, 35.245693, 0.0],[0.0, 34.28776, 0.0]]
                 
        thumbAppendMaxRotList.append(thumbGrabbMaxRotList)                         
        indexAppendMaxRotList.append(indexGrabbMaxRotList)
        midAppendMaxRotList.append(midGrabbMaxRotList)
        ringAppendMaxRotList.append(ringGrabbMaxRotList)
        pinkyAppendMaxRotList.append(pinkyGrabbMaxRotList)            
        
        #grab_b min(-3) val:           
        thumbGrabbMinRotList = [[-1.88916807572, -2.19504008654, 5.15448429452],[-3.89316354721, -3.35200451612, 5.38739178149],[0.0, -9.64685731798, 0.0]]      
        indexGrabbMinRotList = [[0.0, 0.0, 0.0],[0.0, 2.55643895266, 4.84421472464],[0.0, -6.27937348304, 0.0],[0.0, -6.98037935086, 0.0]]
        midGrabbMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.897371185757, 0.900279164949],[0.0, -9.5074318884, 0.0],[0.0, -9.82424536423, 0.0]]
        ringGrabbMinRotList = [[0.897862892745, 0.0, 0.0],[0.0, -3.12544759854, -3.32545729794],[0.0, -11.9532935107, 0.0],[0.0, -12.1285162186, 0.0]]
        pinkyGrabbMinRotList = [[0.0, 0.0, 0.0],[0.0, -8.8880835737, -5.50868833157],[0.0, -10.5737077603, 0.0],[0.0, -10.2863291471, 0.0]]
                            
        thumbAppendMinRotList.append(thumbGrabbMinRotList)                      
        indexAppendMinRotList.append(indexGrabbMinRotList)       
        midAppendMinRotList.append(midGrabbMinRotList)        
        ringAppendMinRotList.append(ringGrabbMinRotList)    
        pinkyAppendMinRotList.append(pinkyGrabbMinRotList)                        
                
        #Spreada 
        #Spreada max(10) val:       
        thumbSpreadaMaxRotList = [[0.0, -9.3049741, 0.0],[4.2133766, -7.0277477, -6.6997279],[4.2135112, -15.59141, -6.699995]]                  
        indexSpreadaMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, -25.582658],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        midSpreadaMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        ringSpreadaMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 8.8561972],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        pinkySpreadaMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 22.877102],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        
        thumbAppendMaxRotList.append(thumbSpreadaMaxRotList)
        indexAppendMaxRotList.append(indexSpreadaMaxRotList)
        midAppendMaxRotList.append(midSpreadaMaxRotList)
        ringAppendMaxRotList.append(ringSpreadaMaxRotList)
        pinkyAppendMaxRotList.append(pinkySpreadaMaxRotList)             
        
        #Spreada min(-3) val:  
        thumbSpreadaMinRotList = [[0.0, 2.79149289363, 0.0],[-1.26401297617, 2.10832434397, 2.00991835806],[-1.26405331915, 4.67742298399, 2.00999841029]]               
        indexSpreadaMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 7.67479746336],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        midSpreadaMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        ringSpreadaMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, -2.65685910148],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        pinkySpreadaMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, -6.86313075324],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
              
        thumbAppendMinRotList.append(thumbSpreadaMinRotList)              
        indexAppendMinRotList.append(indexSpreadaMinRotList)  
        midAppendMinRotList.append(midSpreadaMinRotList)        
        ringAppendMinRotList.append(ringSpreadaMinRotList)    
        pinkyAppendMinRotList.append(pinkySpreadaMinRotList)            


        #Spreadb 
        #Spreadb max(10) val:     
        thumbSpreadbMaxRotList = [[-14.745016, -9.5535818, 6.0563502],[4.2133766, -7.0277477, -6.6997279],[4.2135112, -16.811049, -6.699995]]            
        indexSpreadbMaxRotList = [[0.0, 0.0, 0.0],[8.7247019, -10.394853, -18.082124],[0.0, -8.2723094, -1.7277899e-08],[0.0, -8.2723094, -1.6642118e-08]]
        midSpreadbMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 3.5543708e-08],[0.0, -8.2723094, 3.5543707e-08],[0.0, -8.2723094, 1.7958196e-08]]
        ringSpreadbMaxRotList = [[0.0, 0.0, 0.0],[-10.955866, 7.5271701, 2.1637058],[0.0, -8.2723094, -1.7297596e-08],[0.0, -8.2723094, -1.7446468e-08]]
        pinkySpreadbMaxRotList = [[0.0, 0.0, 0.0],[-3.4375475, 29.857157, 26.640187],[0.0, -8.2723094, 0.0],[0.0, -8.2723094, 0.0]]
          
        thumbAppendMaxRotList.append(thumbSpreadbMaxRotList)                 
        indexAppendMaxRotList.append(indexSpreadbMaxRotList)
        midAppendMaxRotList.append(midSpreadbMaxRotList)
        ringAppendMaxRotList.append(ringSpreadbMaxRotList)
        pinkyAppendMaxRotList.append(pinkySpreadbMaxRotList)            
        
        #Spreadb min(-3) val:        
        thumbSpreadbMinRotList = [[4.42350464415, 2.86607474238, -1.81690513373],[-1.26401297617, 2.10832434397, 2.00991835806],[-1.26405331915, 5.04331486901, 2.00999841029]]         
        indexSpreadbMinRotList = [[0.0, 0.0, 0.0],[-2.61741043801, 3.11845608838, 5.42463689589],[0.0, 2.48169284085, 0.0],[0.0, 2.48169284085, 0.0]]
        midSpreadbMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 2.48169284085, 0.0],[0.0, 2.48169284085, 0.0]]
        ringSpreadbMinRotList = [[0.0, 0.0, 0.0],[3.28675999708, -2.25815105805, 0.0],[0.0, 2.48169284085, 0.0],[0.0, 2.48169284085, 0.0]]
        pinkySpreadbMinRotList = [[0.0, 0.0, 0.0],[1.03126421643, -8.95714757769, -7.99205549907],[0.0, 2.48169284085, 0.0],[0.0, 2.48169284085, 0.0]]
          
        thumbAppendMinRotList.append(thumbSpreadbMinRotList)                 
        indexAppendMinRotList.append(indexSpreadbMinRotList) 
        midAppendMinRotList.append(midSpreadbMinRotList)        
        ringAppendMinRotList.append(ringSpreadbMinRotList)    
        pinkyAppendMinRotList.append(pinkySpreadbMinRotList)             

        #hand 
        #hand max(10) val:    
        thumbHandMaxRotList = [[-2.8725175, -1.4837983, 14.140893],[16.690641, 35.772421, 1.9178732],[0.0, 0.0, 0.0]]                     
        indexHandMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 5.9506481],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        midHandMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.96022806],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        ringHandMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, -3.8924184],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        pinkyHandMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, -8.3619136],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        
        thumbAppendMaxRotList.append(thumbHandMaxRotList)      
        indexAppendMaxRotList.append(indexHandMaxRotList)
        midAppendMaxRotList.append(midHandMaxRotList)
        ringAppendMaxRotList.append(ringHandMaxRotList)
        pinkyAppendMaxRotList.append(pinkyHandMaxRotList)            
        
        #hand min(-3) val:      
        thumbHandMinRotList = [[0.861755245494, 0.0, -4.24226796854],[-5.00719244704, -10.7317273292, 0.0],[0.0, 0.0, 0.0]]           
        indexHandMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, -1.78519442026],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        midHandMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        ringHandMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 1.16772562065],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        pinkyHandMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 2.5085741245],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]       
            
        thumbAppendMinRotList.append(thumbHandMinRotList)     
        indexAppendMinRotList.append(indexHandMinRotList) 
        midAppendMinRotList.append(midHandMinRotList)        
        ringAppendMinRotList.append(ringHandMinRotList)    
        pinkyAppendMinRotList.append(pinkyHandMinRotList)             

        #palm_a 
        #palm_a max(10) val:             
        thumbPalmaMaxRotList = [[0.0, 26.925644, 0.0],[0.0, 7.5732221, 0.0],[0.0, 0.0, 0.0]]    
        indexPalmaMaxRotList = [[9.5015777, 0.0, 0.0],[12.129516, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        midPalmaMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        ringPalmaMaxRotList = [[-24.239371, -0.30426803, -0.74108914],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        pinkyPalmaMaxRotList = [[-17.534821, 1.0340395, -2.1197015],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]        
        
        thumbAppendMaxRotList.append(thumbPalmaMaxRotList)
        indexAppendMaxRotList.append(indexPalmaMaxRotList)
        midAppendMaxRotList.append(midPalmaMaxRotList)
        ringAppendMaxRotList.append(ringPalmaMaxRotList)
        pinkyAppendMaxRotList.append(pinkyPalmaMaxRotList)            
        
        #palm_a min(-3) val:        
        thumbPalmaMinRotList = [[0.0, -8.0776930081, 0.0],[0.0, -2.27196666052, 0.0],[0.0, 0.0, 0.0]]         
        indexPalmaMinRotList = [[-2.85047358591, 0.0, 0.0],[-3.6388550315, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        midPalmaMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        ringPalmaMinRotList = [[7.27181158401, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        pinkyPalmaMinRotList = [[5.2604463016, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]] 
        
        thumbAppendMinRotList.append(thumbPalmaMinRotList)      
        indexAppendMinRotList.append(indexPalmaMinRotList)  
        midAppendMinRotList.append(midPalmaMinRotList)        
        ringAppendMinRotList.append(ringPalmaMinRotList)    
        pinkyAppendMinRotList.append(pinkyPalmaMinRotList)            
        
        #palm_b 
        #palm_b max(10) val:
        thumbPalmbMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        indexPalmbMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        midPalmbMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        ringPalmbMaxRotList = [[-6.8414008, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        pinkyPalmbMaxRotList = [[-13.947657, 1.9094432, -0.4750786],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        
        thumbAppendMaxRotList.append(thumbPalmbMaxRotList)
        indexAppendMaxRotList.append(indexPalmbMaxRotList)
        midAppendMaxRotList.append(midPalmbMaxRotList)
        ringAppendMaxRotList.append(ringPalmbMaxRotList)
        pinkyAppendMaxRotList.append(pinkyPalmbMaxRotList)            
        
        #palm_b min(-3) val:            
        thumbPalmbMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        indexPalmbMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        midPalmbMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        ringPalmbMinRotList = [[2.05242044873, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        pinkyPalmbMinRotList = [[4.18429703895, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        
        thumbAppendMinRotList.append(thumbPalmbMinRotList)
        indexAppendMinRotList.append(indexPalmbMinRotList)
        midAppendMinRotList.append(midPalmbMinRotList)        
        ringAppendMinRotList.append(ringPalmbMinRotList)    
        pinkyAppendMinRotList.append(pinkyPalmbMinRotList)            
          
        
# thumbMaxData fa1 10:[dt.Vector([0.0, 32.298284, 0.0]), dt.Vector([0.0, 0.0, 0.0]), dt.Vector([0.0, 0.0, 0.0])]
# thumbMinData fa1 -3:[dt.Vector([0.0, -9.68948535195, 0.0]), dt.Vector([0.0, 0.0, 0.0]), dt.Vector([0.0, 0.0, 0.0])]      
          
        #thumba 
        #thumba max(10) val:               
        thumbThumbaMaxRotList = [[0.0, 32.298284, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]  
        indexThumbaMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        midThumbaMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        ringThumbaMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        pinkyThumbaMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        
        thumbAppendMaxRotList.append(thumbThumbaMaxRotList)
        indexAppendMaxRotList.append(indexThumbaMaxRotList)
        midAppendMaxRotList.append(midThumbaMaxRotList)
        ringAppendMaxRotList.append(ringThumbaMaxRotList)
        pinkyAppendMaxRotList.append(pinkyThumbaMaxRotList)            
        
        #thumba min(-3) val:        
        thumbThumbaMinRotList = [[0.0, -9.68948535195, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]         
        indexThumbaMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        midThumbaMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        ringThumbaMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        pinkyThumbaMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]                 
                
        thumbAppendMinRotList.append(thumbThumbaMinRotList)    
        indexAppendMinRotList.append(indexThumbaMinRotList)         
        midAppendMinRotList.append(midThumbaMinRotList)        
        ringAppendMinRotList.append(ringThumbaMinRotList)    
        pinkyAppendMinRotList.append(pinkyThumbaMinRotList)                     
        
# thumbMaxData fa2 10:[dt.Vector([0.0, 19.970794, 0.0]), dt.Vector([0.89798905, 40.121461, 3.5222933]), dt.Vector([0.0, 86.584018, 0.0])]
# thumbMinData fa2 -3:[dt.Vector([0.0, -5.99123853692, 0.0]), dt.Vector([0.0, -12.036438635, -1.05668802552]), dt.Vector([0.0, -25.9752055481, 0.0])]        
        
        #thumbb 
        #thumbb max(10) val:  
        thumbThumbbMaxRotList = [[0.0, 19.970794, 0.0],[0.89798905, 40.121461, 3.5222933],[0.0, 86.584018, 0.0]]               
        indexThumbbMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        midThumbbMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        ringThumbbMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        pinkyThumbbMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]                
        
        thumbAppendMaxRotList.append(thumbThumbbMaxRotList)
        indexAppendMaxRotList.append(indexThumbbMaxRotList)
        midAppendMaxRotList.append(midThumbbMaxRotList)
        ringAppendMaxRotList.append(ringThumbbMaxRotList)
        pinkyAppendMaxRotList.append(pinkyThumbbMaxRotList)            
        
        #thumbb min(-3) val:       
        thumbThumbbMinRotList = [[0.0, -5.99123853692, 0.0],[0.0, -12.036438635, -1.05668802552],[0.0, -25.9752055481, 0.0]]  
        indexThumbbMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        midThumbbMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        ringThumbbMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        pinkyThumbbMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]                
        
        thumbAppendMinRotList.append(thumbThumbbMinRotList)        
        indexAppendMinRotList.append(indexThumbbMinRotList)  
        midAppendMinRotList.append(midThumbbMinRotList)        
        ringAppendMinRotList.append(ringThumbbMinRotList)    
        pinkyAppendMinRotList.append(pinkyThumbbMinRotList)            

        #thumbc 
        #thumbc max(10) val:   
        thumbThumbcMaxRotList = [[1.3824678, 0.85791805, 24.089138],[0.0, 21.783755, 0.0],[0.0, 11.173675, 0.0]]
        indexThumbcMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 3.5543707e-08],[0.0, 0.0, 3.5543708e-08],[0.0, 0.0, 3.5543708e-08]]
        midThumbcMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 3.5543707e-08],[0.0, 0.0, 3.5543707e-08],[0.0, 0.0, 3.5543707e-08]]
        ringThumbcMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 3.5543708e-08],[0.0, 0.0, 3.5543708e-08],[0.0, 0.0, 3.5543708e-08]]
        pinkyThumbcMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
         
        thumbAppendMaxRotList.append(thumbThumbcMaxRotList) 
        indexAppendMaxRotList.append(indexThumbcMaxRotList)    
        midAppendMaxRotList.append(midThumbcMaxRotList)
        ringAppendMaxRotList.append(ringThumbcMaxRotList)
        pinkyAppendMaxRotList.append(pinkyThumbcMaxRotList)    
        
        #thumbc min(-3) val: 
        thumbThumbcMinRotList = [[0.0, 0.0, -7.22674131721],[0.0, -6.53512667879, 0.0],[0.0, -3.35210252391, 0.0]]
        indexThumbcMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        midThumbcMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        ringThumbcMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        pinkyThumbcMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        
        thumbAppendMinRotList.append(thumbThumbcMinRotList) 
        indexAppendMinRotList.append(indexThumbcMinRotList)
        midAppendMinRotList.append(midThumbcMinRotList)        
        ringAppendMinRotList.append(ringThumbcMinRotList)    
        pinkyAppendMinRotList.append(pinkyThumbcMinRotList)            
        
        #thumbd 
        #thumbd max(10) val:   
        thumbThumbdMaxRotList = [[-6.962866, 0.86260794, -15.827857],[-4.9098453, 24.682477, -13.450913],[0.0, 84.314659, 0.0]]
        indexThumbdMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 3.5543708e-08],[0.0, 0.0, 3.5543708e-08],[0.0, 0.0, 3.5543708e-08]]
        midThumbdMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 3.5543707e-08],[0.0, 0.0, 3.5543707e-08],[0.0, 0.0, 3.5543707e-08]]
        ringThumbdMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 3.5543708e-08],[0.0, 0.0, 3.5543708e-08],[0.0, 0.0, 3.5543708e-08]]
        pinkyThumbdMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
         
        thumbAppendMaxRotList.append(thumbThumbdMaxRotList) 
        indexAppendMaxRotList.append(indexThumbdMaxRotList)
        midAppendMaxRotList.append(midThumbdMaxRotList)
        ringAppendMaxRotList.append(ringThumbdMaxRotList)
        pinkyAppendMaxRotList.append(pinkyThumbdMaxRotList)            
        
        #thumbd min(-3) val: 
        thumbThumbdMinRotList = [[2.08885988614, 0.0, 4.74835730662],[1.47295359407, -7.40474266626, 4.03527363385],[0.0, -25.294399704, 0.0]]
        indexThumbdMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        midThumbdMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        ringThumbdMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        pinkyThumbdMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]

        thumbAppendMinRotList.append(thumbThumbdMinRotList)
        indexAppendMinRotList.append(indexThumbdMinRotList)
        midAppendMinRotList.append(midThumbdMinRotList)        
        ringAppendMinRotList.append(ringThumbdMinRotList)    
        pinkyAppendMinRotList.append(pinkyThumbdMinRotList)            
        
        #index_curl 
        #index_curl max(10) val:        
        thumbIndexCurlMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]            
        indexIndexCurlMaxRotList = [[0.0, 0.0, 0.0],[0.0, 90.0, 0.0],[0.0, 90.0, 0.0],[0.0, 90.0, 0.0]]
        midIndexCurlMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        ringIndexCurlMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        pinkyIndexCurlMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
                                 
        thumbAppendMaxRotList.append(thumbIndexCurlMaxRotList)                                 
        indexAppendMaxRotList.append(indexIndexCurlMaxRotList)
        midAppendMaxRotList.append(midIndexCurlMaxRotList)
        ringAppendMaxRotList.append(ringIndexCurlMaxRotList)
        pinkyAppendMaxRotList.append(pinkyIndexCurlMaxRotList)            
        
        #index_curl min(-3) val:            
        thumbIndexCurlMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]        
        indexIndexCurlMinRotList = [[0.0, 0.0, 0.0],[0.0, -27.0000020556, 0.0],[0.0, -27.0000020556, 0.0],[0.0, -27.0000020556, 0.0]]
        midIndexCurlMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        ringIndexCurlMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        pinkyIndexCurlMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
                        
        thumbAppendMinRotList.append(thumbIndexCurlMinRotList)                                 
        indexAppendMinRotList.append(indexIndexCurlMinRotList)  
        midAppendMinRotList.append(midIndexCurlMinRotList)        
        ringAppendMinRotList.append(ringIndexCurlMinRotList)    
        pinkyAppendMinRotList.append(pinkyIndexCurlMinRotList)            

        #middle_curl 
        #middle_curl max(10) val:                 
        thumbMiddleCurlMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]   
        indexMiddleCurlMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        midMiddleCurlMaxRotList = [[0.0, 0.0, 0.0],[0.0, 90.0, 0.0],[0.0, 90.0, 0.0],[0.0, 90.0, 0.0]]
        ringMiddleCurlMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        pinkyMiddleCurlMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        
        thumbAppendMaxRotList.append(thumbMiddleCurlMaxRotList)
        indexAppendMaxRotList.append(indexMiddleCurlMaxRotList)
        midAppendMaxRotList.append(midMiddleCurlMaxRotList)
        ringAppendMaxRotList.append(ringMiddleCurlMaxRotList)
        pinkyAppendMaxRotList.append(pinkyMiddleCurlMaxRotList)            
        
        #middle_curl min(-3) val:             
        thumbMiddleCurlMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]       
        indexMiddleCurlMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        midMiddleCurlMinRotList = [[0.0, 0.0, 0.0],[0.0, -27.0000020556, 0.0],[0.0, -27.0000020556, 0.0],[0.0, -27.0000020556, 0.0]]
        ringMiddleCurlMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        pinkyMiddleCurlMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]               
                
        thumbAppendMinRotList.append(thumbMiddleCurlMinRotList) 
        indexAppendMinRotList.append(indexMiddleCurlMinRotList)  
        midAppendMinRotList.append(midMiddleCurlMinRotList)        
        ringAppendMinRotList.append(ringMiddleCurlMinRotList)    
        pinkyAppendMinRotList.append(pinkyMiddleCurlMinRotList)            

        #ring_curl 
#         ringMaxData fd 10:[dt.Vector([0.0, 0.0, 0.0]), dt.Vector([0.0, 90.0, 0.0]), dt.Vector([0.0, 90.0, 0.0]), dt.Vector([0.0, 90.0, 0.0])]
#         ringMinData fd -3:[dt.Vector([0.0, 0.0, 0.0]), dt.Vector([0.0, -27.0000020556, 0.0]), dt.Vector([0.0, -27.0000020556, 0.0]), dt.Vector([0.0, -27.0000020556, 0.0])]     
          
        #ring_curl max(10) val:     
        thumbRingCurlMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]               
        indexRingCurlMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        midRingCurlMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        ringRingCurlMaxRotList = [[0.0, 0.0, 0.0],[0.0, 90.0, 0.0],[0.0, 90.0, 0.0],[0.0, 90.0, 0.0]]
        pinkyRingCurlMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]                
        
        thumbAppendMaxRotList.append(thumbRingCurlMaxRotList)
        indexAppendMaxRotList.append(indexRingCurlMaxRotList)
        midAppendMaxRotList.append(midRingCurlMaxRotList)
        ringAppendMaxRotList.append(ringRingCurlMaxRotList)
        pinkyAppendMaxRotList.append(pinkyRingCurlMaxRotList)            
        
        #ring_curl min(-3) val:   
        thumbRingCurlMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]              
        indexRingCurlMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        midRingCurlMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        ringRingCurlMinRotList = [[0.0, 0.0, 0.0],[0.0, -27.0000020556, 0.0],[0.0, -27.0000020556, 0.0],[0.0, -27.0000020556, 0.0]]
        pinkyRingCurlMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
                 
        thumbAppendMinRotList.append(thumbRingCurlMinRotList)                    
        indexAppendMinRotList.append(indexRingCurlMinRotList)
        midAppendMinRotList.append(midRingCurlMinRotList)        
        ringAppendMinRotList.append(ringRingCurlMinRotList)    
        pinkyAppendMinRotList.append(pinkyRingCurlMinRotList)            
        
        #pinky_curl 
        #pinky_curl max(10) val:   
        thumbPinkyCurlMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]              
        indexPinkyCurlMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        midPinkyCurlMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        ringPinkyCurlMaxRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        pinkyPinkyCurlMaxRotList = [[0.0, 0.0, 0.0],[0.0, 90.0, 0.0],[0.0, 90.0, 0.0],[0.0, 90.0, 0.0]]
                         
        thumbAppendMaxRotList.append(thumbPinkyCurlMaxRotList)                         
        indexAppendMaxRotList.append(indexPinkyCurlMaxRotList)
        midAppendMaxRotList.append(midPinkyCurlMaxRotList)
        ringAppendMaxRotList.append(ringPinkyCurlMaxRotList)
        pinkyAppendMaxRotList.append(pinkyPinkyCurlMaxRotList)            
        
        #pinky_curl min(-3) val:  
        thumbPinkyCurlMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]               
        indexPinkyCurlMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        midPinkyCurlMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        ringPinkyCurlMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
        pinkPinkyCurlMinRotList = [[0.0, 0.0, 0.0],[0.0, -27.0000020556, 0.0],[0.0, -27.0000020556, 0.0],[0.0, -27.0000020556, 0.0]]
                           
        thumbAppendMinRotList.append(thumbPinkyCurlMinRotList)                           
        indexAppendMinRotList.append(indexPinkyCurlMinRotList)       
        midAppendMinRotList.append(midPinkyCurlMinRotList)        
        ringAppendMinRotList.append(ringPinkyCurlMinRotList)    
        pinkyAppendMinRotList.append(pinkPinkyCurlMinRotList)                                 

        #point 
        #point max(10) val: 
        thumbPointMaxRotList = [[-10.297729, 19.527241, -3.216298],[-2.6821504, 18.788421, -7.8319604],[6.7352422, 58.884666, -9.4826603]]                
        indexPointMaxRotList = [[0.0, 0.0, 0.0],[-0.48240779, 0.29722213, -0.10914528],[0.0, -7.8036046, 0.0],[0.0, -7.8036046, 0.0]]
        midPointMaxRotList = [[0.0, 0.0, 0.0],[1.6502186, 52.116256, -4.3852106],[0.0, 99.9835, 0.0],[0.0, 76.63128, 0.0]]
        ringPointMaxRotList = [[0.0, 0.0, 0.0],[-5.1919839, 62.997629, -1.741267],[0.0, 97.862165, 0.0],[0.0, 78.57743, 0.0]]
        pinkyPointMaxRotList = [[0.0, 0.0, 0.0],[-11.35146, 70.628056, 0.91715981],[0.0, 83.653515, 0.0],[0.0, 83.653515, 0.0]]
                                
        thumbAppendMaxRotList.append(thumbPointMaxRotList)                                
        indexAppendMaxRotList.append(indexPointMaxRotList)
        midAppendMaxRotList.append(midPointMaxRotList)
        ringAppendMaxRotList.append(ringPointMaxRotList)
        pinkyAppendMaxRotList.append(pinkyPointMaxRotList)    
        
        #point min(-3) val:            
        thumbPointMinRotList = [[3.08931860821, -5.85817240051, 0.964889427749],[0.0, -5.63652682313, 2.34958807188],[-2.02057267633, -17.6654010348, 2.84479838267]]     
        indexPointMinRotList = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 2.34108130208, 0.0],[0.0, 2.34108130208, 0.0]]
        midPointMinRotList = [[0.0, 0.0, 0.0],[0.0, -15.6348762585, 1.3155631832],[0.0, -29.9950512267, 0.0],[0.0, -22.9893817888, 0.0]]
        ringPointMinRotList = [[0.0, 0.0, 0.0],[1.55759534157, -18.8992888563, 0.0],[0.0, -29.358649066, 0.0],[0.0, -23.5732288764, 0.0]]
        pinkyPointMinRotList = [[0.0, 0.0, 0.0],[3.40543798067, -21.1884157715, 0.0],[0.0, -25.0960539922, 0.0],[0.0, -25.0960539922, 0.0]]
                             
        thumbAppendMinRotList.append(thumbPointMinRotList)                             
        indexAppendMinRotList.append(indexPointMinRotList)       
        midAppendMinRotList.append(midPointMinRotList)        
        ringAppendMinRotList.append(ringPointMinRotList)    
        pinkyAppendMinRotList.append(pinkyPointMinRotList)               
        
        
        #set attr list:
        thumbRotAttrs = []
        indexRotAttrs = []
        midRotAttrs = []
        ringRotAttrs = []
        pinkyRotAttrs = []                        
        
        #set attr for each rot attr
        for selfAttr in self.attrs:
            
#             #thumb
#             for thumbSdk in self.thumbSdks:
#                 for ch in chr:
#                     attr = thumbSdk + '.r' + ch
#                     thumbRotAttrs.append(attr)            
            
            #index
            for indexSdk in self.indexSdks:
                for ch in chr:
                    attr = indexSdk + '.r' + ch
                    indexRotAttrs.append(attr)

            #mid
            for midSdk in self.midSdks:
                for ch in chr:
                    attr = midSdk + '.r' + ch
                    midRotAttrs.append(attr)                    

            #ring
            for ringSdk in self.ringSdks:
                for ch in chr:
                    attr = ringSdk + '.r' + ch
                    ringRotAttrs.append(attr)                    
                    
            #pinky
            for pinkySdk in self.pinkySdks:
                for ch in chr:
                    attr = pinkySdk + '.r' + ch
                    pinkyRotAttrs.append(attr)                    

            #set default(0) sdk
            
#             #set thumb default:
#             for thumbSdk in self.thumbSdks:
#                 for ch in chr:            
#                     pm.setDrivenKeyframe(thumbSdk + '.r' + ch,v = 0, 
#                                          cd = self.armControls[0] + '.' + selfAttr,dv = 0)            
            
            #set index default:
            for indexSdk in self.indexSdks:
                for ch in chr:            
                    pm.setDrivenKeyframe(indexSdk + '.r' + ch,v = 0, 
                                         cd = self.armControls[0] + '.' + selfAttr,dv = 0)
                    
            #set mid default:
            for midSdk in self.midSdks:
                for ch in chr:            
                    pm.setDrivenKeyframe(midSdk + '.r' + ch,v = 0, 
                                         cd = self.armControls[0] + '.' + selfAttr,dv = 0)   
                    
            #set ring default:
            for ringSdk in self.ringSdks:
                for ch in chr:            
                    pm.setDrivenKeyframe(ringSdk + '.r' + ch,v = 0, 
                                         cd = self.armControls[0] + '.' + selfAttr,dv = 0)   
                    
            #set index default:
            for pinkySdk in self.pinkySdks:
                for ch in chr:            
                    pm.setDrivenKeyframe(pinkySdk + '.r' + ch,v = 0, 
                                         cd = self.armControls[0] + '.' + selfAttr,dv = 0)                                                                           
                      
        #get/set rotate Max val to main rot list:
        #get thumb list
#         for number,valueList in enumerate(thumbAppendMaxRotList):
#             for value in valueList:
#                 for num in [0,1,2]:
#                     val = value[num]
#                     thumbMainMaxRotList.append(val)
        
        #get index list
        for number,valueList in enumerate(indexAppendMaxRotList):
            for value in valueList:
                for num in [0,1,2]:
                    val = value[num]
                    indexMainMaxRotList.append(val)
        
        #get mid list
        for number,valueList in enumerate(midAppendMaxRotList):
            for value in valueList:
                for num in [0,1,2]:
                    val = value[num]
                    midMainMaxRotList.append(val)
                    
        #get ring list
        for number,valueList in enumerate(ringAppendMaxRotList):
            for value in valueList:
                for num in [0,1,2]:
                    val = value[num]
                    ringMainMaxRotList.append(val)                            

        #get pinky list
        for number,valueList in enumerate(pinkyAppendMaxRotList):
            for value in valueList:
                for num in [0,1,2]:
                    val = value[num]
                    pinkyMainMaxRotList.append(val)        
        
        #set dic max(10) val
        #set thumb
#         for number,attrList in enumerate(thumbRotAttrs):
#             pm.setDrivenKeyframe(attrList,v = thumbMainMaxRotList[number],
#                                  cd = self.armControls[0] + '.' + self.attrs[number/12],dv = 10)        
        
        #set index
        for number,attrList in enumerate(indexRotAttrs):
            pm.setDrivenKeyframe(attrList,v = indexMainMaxRotList[number],
                                 cd = self.armControls[0] + '.' + self.attrs[number/12],dv = 10)
            
        #set dic max(10) val
        #set mid
        for number,attrList in enumerate(midRotAttrs):
            pm.setDrivenKeyframe(attrList,v = midMainMaxRotList[number],
                                 cd = self.armControls[0] + '.' + self.attrs[number/12],dv = 10)  
            
        #set dic max(10) val
        #set ring
        for number,attrList in enumerate(ringRotAttrs):
            pm.setDrivenKeyframe(attrList,v = ringMainMaxRotList[number],
                                 cd = self.armControls[0] + '.' + self.attrs[number/12],dv = 10)  
            
        #set dic max(10) val
        #set pinky
        for number,attrList in enumerate(pinkyRotAttrs):
            pm.setDrivenKeyframe(attrList,v = pinkyMainMaxRotList[number],
                                 cd = self.armControls[0] + '.' + self.attrs[number/12],dv = 10)                                          
            
        #get/set rotate Min val to main rot list:
        #get thumb list
#         for number,valueList in enumerate(thumbAppendMinRotList):
#             for value in valueList:
#                 for num in [0,1,2]:
#                     val = value[num]
#                     thumbMainMinRotList.append(val)        
        
        #get index list
        for number,valueList in enumerate(indexAppendMinRotList):
            for value in valueList:
                for num in [0,1,2]:
                    val = value[num]
                    indexMainMinRotList.append(val)
                    
        #get mid list
        for number,valueList in enumerate(midAppendMinRotList):
            for value in valueList:
                for num in [0,1,2]:
                    val = value[num]
                    midMainMinRotList.append(val)
                    
        #get ring list
        for number,valueList in enumerate(ringAppendMinRotList):
            for value in valueList:
                for num in [0,1,2]:
                    val = value[num]
                    ringMainMinRotList.append(val)
                    
        #get pinky list
        for number,valueList in enumerate(pinkyAppendMinRotList):
            for value in valueList:
                for num in [0,1,2]:
                    val = value[num]
                    pinkyMainMinRotList.append(val)                                                            
        
        #set dic min(-3) val
#         #thumb min(-3) val
#         for number,attrList in enumerate(thumbRotAttrs):
#             pm.setDrivenKeyframe(attrList,v = thumbMainMinRotList[number],
#                                  cd = self.armControls[0] + '.' + self.attrs[number/12],dv = -3)        
        
        #index min(-3) val
        for number,attrList in enumerate(indexRotAttrs):
            pm.setDrivenKeyframe(attrList,v = indexMainMinRotList[number],
                                 cd = self.armControls[0] + '.' + self.attrs[number/12],dv = -3)

        #mid min(-3) val
        for number,attrList in enumerate(midRotAttrs):
            pm.setDrivenKeyframe(attrList,v = midMainMinRotList[number],
                                 cd = self.armControls[0] + '.' + self.attrs[number/12],dv = -3)      
            
        #ring min(-3) val
        for number,attrList in enumerate(ringRotAttrs):
            pm.setDrivenKeyframe(attrList,v = ringMainMinRotList[number],
                                 cd = self.armControls[0] + '.' + self.attrs[number/12],dv = -3)      
            
        #pinky min(-3) val
        for number,attrList in enumerate(pinkyRotAttrs):
            pm.setDrivenKeyframe(attrList,v = pinkyMainMinRotList[number],
                                 cd = self.armControls[0] + '.' + self.attrs[number/12],dv = -3)                                                       
                 
    def buildConnections(self):
        
        #set whole grp
        self.handGrp = pm.group(self.thumbGrp,self.indexGrp,self.midGrp,self.ringGrp,self.pinkyGrp,n = nameUtils.getUniqueName(self.side,'hand','grp'))
        pm.select(self.armChains[5])
        armChains5 = pm.selected()
        pm.select(self.armChains[2])
        armChains2 = pm.selected()
        
        handGrpPiv = armChains5[0].getTranslation(space = 'world')
        pm.move(handGrpPiv[0],handGrpPiv[1],handGrpPiv[2],self.handGrp + '.rotatePivot')
        pm.move(handGrpPiv[0],handGrpPiv[1],handGrpPiv[2],self.handGrp + '.scalePivot')
        pm.pointConstraint(armChains5[0],self.handGrp,mo = 0)
         
        #create bridge loc and grp
        #create bri loc
        ikBri = pm.spaceLocator(n = nameUtils.getUniqueName(self.side,'armIK_bri','loc'))
        fkBri = pm.spaceLocator(n = nameUtils.getUniqueName(self.side,'armFK_bri','loc'))
        pm.move(handGrpPiv[0],handGrpPiv[1],handGrpPiv[2],ikBri)
        pm.move(handGrpPiv[0],handGrpPiv[1],handGrpPiv[2],fkBri)
         
        #create bri grp
        ikBriGrp = pm.group(ikBri,n = nameUtils.getUniqueName(self.side,'armIK_bri','grp'))
        fkBriGrp = pm.group(fkBri,n = nameUtils.getUniqueName(self.side,'armFK_bri','grp'))
        pm.move(handGrpPiv[0],handGrpPiv[1],handGrpPiv[2],ikBriGrp + '.rotatePivot')
        pm.move(handGrpPiv[0],handGrpPiv[1],handGrpPiv[2],fkBriGrp + '.scalePivot')
        ikBriGrp.v.set(0)
        fkBriGrp.v.set(0)
         
        #parent bridge
        ikBriGrp.setParent(self.armControls[1])
        fkBriGrp.setParent(armChains5[0])
         
        #create Oristraint
        ori = pm.orientConstraint(ikBri,fkBri,self.handGrp,mo = 0)
        self.armControls[0].IKFK.connect(ori.attr(ikBri.name() + 'W0'))
         
        #createNode
        reverseNode = pm.createNode('reverse',n = nameUtils.getUniqueName(self.side,'hand','REV'))
        self.armControls[0].IKFK.connect(reverseNode.inputX)
        reverseNode.outputX.connect(ori.attr(fkBri.name() + 'W1'))

        #receive info from incoming package
        #connect to the main meta
        if pm.objExists(self.metaMain) and pm.objExists(self.metaArm) == 1:
            
            print ''
            print 'Package from (' + self.metaMain + ') has been received'
            print 'Package from (' + self.metaSpine + ') has been received'
            
            
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
        else:
            OpenMaya.MGlobal.displayError('Package :' + self.metaMain + ' is NOT exist')
            
        self.handGrp.setParent(spineDestinations[0])
        
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
        
        self.guideGrp.setParent(CC)
        
def getUi(parent,mainUi):
    
    return FingerModuleUi(parent,mainUi)

class FingerModuleUi(object):
    
    def __init__(self,parent,mainUi):
        
        self.mainUi = mainUi
        self.__popuItems = []
        
        pm.setParent(parent)
        self.mainL = pm.columnLayout(adj = 1)
        pm.separator(h = 10)
        
        #(self,baseName = 'arm',side = 'l',size = 1.5,
        self.name = pm.text(l = '**** Finger Module ****')       
        self.baseNameT = pm.textFieldGrp(l = 'baseName : ',ad2 = 1,text = 'finger',cl2 = ['left','left'],)
        self.sideT = pm.textFieldGrp(l = 'side :',ad2 = 1,text = 'l',cl2 = ['left','left'],)
        self.cntSize = pm.floatFieldGrp(l = 'ctrl Size : ',cl2 = ['left','left'],ad2 = 1,nf = 1,value1 = 0.5)
        
        #finger num 
        self.fingerNumMenu = pm.optionMenu(l = 'finger Num : ')
        pm.menuItem(l = 'ni',p = self.fingerNumMenu)
        pm.menuItem(l = 'sann',p = self.fingerNumMenu)
        pm.menuItem(l = 'shi',p = self.fingerNumMenu)
        pm.menuItem(l = 'go',p = self.fingerNumMenu)
        
        self.armMetaNodeN = pm.textFieldGrp(l = 'armMeta :',ad2 = 1,cl2 = ['left','left'],text = 'l_arm_0_META')
        self.spineMetaNodeN = pm.textFieldGrp(l = 'spineMeta :',ad2 = 1,cl2 = ['left','left'],text = 'm_spine_0_META')
        self.mainMetaNodeN = pm.textFieldGrp(l = 'mainMeta :',ad2 = 1,cl2 = ['left','left'],text = 'm_test_0_META')
        pm.separator(h = 10)
        
        #ver2Loc
        self.ver2LocTool = pm.text(l = '**** Lid Tool ****')
        self.ver2Loc = pm.button(l = 'ver2Loc',c = self.__clusLoc)
        pm.separator(h = 10)
        
        #remove
        self.removeButtonIntr = pm.text(l = '**** Remove This Panel ****')
        self.removeB = pm.button(l = 'remove',c = self.__removeInstance)
        pm.separator(h = 10)
        
        self.__pointerClass = None
        
    def __removeInstance(self,*arg):
        
        pm.deleteUI(self.mainL)
        self.mainUi.modulesUi.remove(self)
        
    def getModuleInstance(self):
        
        baseNameT = pm.textFieldGrp(self.baseNameT,q = 1,text = 1)
        sideT = pm.textFieldGrp(self.sideT,q = 1,text = 1)
        cntSizeV = pm.floatFieldGrp(self.cntSize,q = 1,value1 = 1)
        fingerNumT = pm.optionMenu(self.fingerNumMenu, q = 1,v = 1)
        armMetaNode = pm.textFieldGrp(self.armMetaNodeN,q = 1,text = 1)
        spineMetaNode = pm.textFieldGrp(self.spineMetaNodeN,q = 1,text = 1)
        mainMetaNode = pm.textFieldGrp(self.mainMetaNodeN,q = 1,text = 1)
        
        self.__pointerClass = FingerModule(baseNameT,sideT,size = cntSizeV,metaArm = armMetaNode,
                                           metaMain = mainMetaNode,metaSpine = spineMetaNode,fingerNum = fingerNumT)
        return self.__pointerClass        
    
    def __clusLoc(self,*arg):
        
        '''create a clus base on edges'''
        sideT = pm.textFieldGrp(self.sideT,q = 1,text = 1)
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
