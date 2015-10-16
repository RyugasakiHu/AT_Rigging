import pymel.core as pm
from subModules import fkChain,ikChain,boneChain,ribbon
from Utils import nameUtils
from Modules import control,hierarchy

class SpineModule(object):

    posSpineArray = [[],[],[]]

    def __init__(self,baseName = 'spine',size = 0.5,segment = 9):
        
        #self para
        self.side = 'c'
        self.baseName = baseName 
        self.size = size
        self.segment = segment
        self.length  = None
        
        #guide para
        self.guideCc = None
        self.guideTrv = None
        self.guides = None
        self.guideGrp = None
        
        
    def buildGuides(self):
        
        #set hi
        self.hi = hierarchy.Hierarchy(characterName = 'test')
        self.hi.build()        
        
        #group
        self.guides = []
        
        #build curve
        self.guideCc = pm.curve(d = 3,p = [[0,9.040668,0.0623416],[0,10.507795,0.181759],[0,11.991982,0.164699],
                                         [0,13.322632,-0.108255],[0,14.397388,-0.0570757]],k = [0,0,0,1,2,2,2],
                              n = nameUtils.getUniqueName(self.side,self.baseName + '_cc','gud'))      
        curveInfo = pm.createNode('curveInfo',n = nameUtils.getUniqueName(self.side,self.baseName + '_cc','cvINFO'))
        self.guideCc.getShape().worldSpace.connect(curveInfo.inputCurve)
        self.length = curveInfo.arcLength.get()
        
    def build(self):
        
        #build Trv
        self.guideTrv = pm.joint(p = [0,0,0],n = nameUtils.getUniqueName(self.side,self.baseName,'trv'))
        moPathName = nameUtils.getUniqueName(self.side,self.baseName,'MOP')
        moPathNode = pm.pathAnimation(self.guideCc,self.guideTrv,fractionMode = 1,follow = 1,followAxis = 'x',upAxis = 'y',worldUpType = 'vector',
                                      worldUpVector = [0,1,0],inverseUp = 0,inverseFront = 0,bank = 0,startTimeU = 1,endTimeU = 24,n = moPathName)        
        pm.disconnectAttr(moPathNode + '_uValue.output',moPathNode + '.uValue')
        
        #set Trv Loc:
        trvPosList = []

        for num in range(0,self.segment):
            trvDis = num * (1 / float(self.segment-1))
            pm.setAttr(moPathNode + '.uValue',trvDis)
            trvPos = self.guideTrv.getTranslation(space = 'world')
            trvPosList.append(trvPos)

        #set loc
        #set loc grp
        for i,p in enumerate(trvPosList):
            trvName = nameUtils.getUniqueName(self.side,self.baseName,'gud')
            loc = pm.spaceLocator(n = trvName)
            loc.t.set(p)
            self.guides.append(loc)
            loc.setParent(self.guideGrp)
            
        tempGuides = list(self.guides)
        tempGuides.reverse()
        
        #set loc grp
        for i in range(len(tempGuides)):
            if i != (len(tempGuides) - 1):
                pm.parent(tempGuides[i],tempGuides[i + 1])            
        
        name = nameUtils.getUniqueName(self.side,self.baseName + '_Gud','grp')        
        self.guideGrp = pm.group(self.guideCc,self.guides[0],self.guideTrv,n = name)   
        
        #create jj
        self.guideSpinePos = [x.getTranslation(space = 'world') for x in self.guides]
        self.guideSpineRot = [x.getRotation(space = 'world') for x in self.guides]
        
        self.spineBlendChain = boneChain.BoneChain(self.baseName,self.side,type = 'jj')
        self.spineBlendChain.fromList(self.guideSpinePos,self.guideSpineRot)
        
        #create IKRibbonSpine
        #ribbon spine info:
        curveInfo = [0,(self.segment - 1) / 4,(self.segment - 1) / 2,
                     ((self.segment - 1) / 2 + (self.segment - 1)) / 2,
                     (self.segment - 1)]
        ribbonCurve = []
        
        #create curve
        for jjInfo in curveInfo:
            ribonJjPos = self.spineBlendChain.chain[jjInfo].getTranslation(space = 'world') 
            ribbonCurve.append(ribonJjPos)
        
        #set ribbon offset
        offset = 0.0
        if self.length / self.segment <= 1:
            offset = 0.5
        else :
            offset = self.length / ((self.segment - 1) / 2)
        
        #set ribbon cur
        ribbonCurveL = pm.curve(d = 3,p = [ribbonCurve[0],ribbonCurve[1],ribbonCurve[2],ribbonCurve[3],ribbonCurve[4]],
                                k = [0,0,0,1,2,2,2],n = nameUtils.getUniqueName(self.side,self.baseName + '_ribbonL','gud'))

        pm.move(offset,0,0,ribbonCurveL)         

        ribbonCurveR = pm.curve(d = 3,p = [ribbonCurve[0],ribbonCurve[1],ribbonCurve[2],ribbonCurve[3],ribbonCurve[4]],
                                k = [0,0,0,1,2,2,2],n = nameUtils.getUniqueName(self.side,self.baseName + '_ribbonR','gud')) 
         
        pm.move(-offset,0,0,ribbonCurveR)     
        
        ribbonCurveR.setParent(self.guideGrp)
        ribbonCurveL.setParent(self.guideGrp)
        
        #create ribbon surf
        ribbonSurf = pm.loft(ribbonCurveR,ribbonCurveL,ch = 0,u = 1,c = 0,ar = 1,d = 3,ss = 1, rn = 0,po = 0,rsn = 1,
                             n = nameUtils.getUniqueName(self.side,self.baseName + '_ribbon','surf'))
        
        ribbonClusList = []
        ribbonJc = []
        
        for num in [0,2,4]:
            pos = pm.select(ribbonSurf[0] + '.cv[' + str(num) + '][0:3]',r = 1)
            clus = pm.cluster()
            pm.rename(clus[1],nameUtils.getUniqueName(self.side,self.baseName + '_ribbon','cls'))
            ribbonClusList.append(clus)
            pm.select(cl = 1)
            
        for num,x in enumerate(ribbonClusList):
            jc = pm.joint(p = x[1].getRotatePivot(),n = nameUtils.getUniqueName(self.side,self.baseName + '_ribbon','jc'))
            ribbonJc.append(jc)
            pm.select(cl = 1)
            pm.delete(ribbonClusList[num])
        
        
                
            
# import maya.cmds as mc
# from see import see
# pathOfFiles = 'C:\Users\UV\Desktop\Rigging workshop/'
# fileType = 'obj'
# files = mc.getFileList(folder = pathOfFiles,fs = '*.%s' % fileType)
# mc.file(new = 1,f = 1)
#  
# if len(files) == 0:
#     mc.warning('no files found')
# else:
#     for fi in files:
#         print pathOfFiles + fi
#         mc.file(pathOfFiles + fi,i = True)
#          
# import sys
# myPath = 'C:/eclipse/test/OOP/AutoRig'
#  
# if not myPath in sys.path:
#     sys.path.append(myPath)    
#      
# import reloadMain
# reload(reloadMain)   
#  
# from Modules import spineModule
# rp = spineModule.SpineModule()
# rp.buildGuides()
# rp.build()         
