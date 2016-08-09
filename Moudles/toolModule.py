import pymel.core as pm
import maya.mel as mel
import maya.cmds as mc
import math
from Modules import control
from Modules.subModules import fkChain,ikChain,boneChain
from Utils import nameUtils,metaUtils

def getUi(parent,mainUi):
    
    return ToolModuleUi(parent,mainUi)

class ToolModuleUi(object):
    
    '''
    this module include three part:
    1.sel skin joint for each meta
    2.fk chain
    3.dynamic ik 
    '''
    
    def __init__(self,parent,mainUi):
        
        #mirror para
        ###
        self.axis = [1,1,1]
        ###
        
        self.mainUi = mainUi
        self.__popuItems = []
 
        pm.setParent(parent)
        self.mainL = pm.columnLayout(adj = 1) 
        self.name = pm.text(l = '**** Tool Module ****')          
        pm.separator(h = 10)
                
        #metaSel
        #all
        self.jointSel = pm.frameLayout('joint Select Tool : ',cll=1,p = self.mainL,cl = 1)
        #skin Joint
        self.skinJointSel = pm.frameLayout('skinJoint Select Tool : ',cll=1,p = self.jointSel,cl = 1)
        self.skinJointMenu = pm.optionMenu(l = 'meta : ')
        metaUtils.metaSel()  
        pm.button(l = 'select Skin Joint',c = self.__selSkinJoint)
        
        #partial Joint
        self.partialSkinJointSel = pm.frameLayout('skinPartialJoint Select Tool : ',cll=1,p = self.jointSel,cl = 1)
        self.partialSkinJointMenu = pm.optionMenu(l = 'meta : ')
        metaUtils.metaSel()  
        pm.button(l = 'select PartialSkin Joint',c = self.__selPartialSkinJoint)
        
        #skinTool
        self.skinAreaTool = pm.frameLayout('skin Area Tool : ',cll=1,p = self.mainL)        
        pm.button('skin Area Weight',c = self.__areaSkin) 
        
        #splitJoint
        self.splitJoint = pm.frameLayout('split Joint Tool : ',cll=1,p = self.mainL,cl = 1)
        self.splitNum = pm.intSliderGrp('intSliderGrp2',min = 1,max = 10,f = 1,s = 1,v = 1)
        pm.button('split Joint',c = self.__splitJointButton) 
        
        #shapeSize
        self.shape = pm.frameLayout('curve Shape Tool : ',cll=1,p = self.mainL,cl = 1)
        self.shapeLayout = pm.columnLayout('shapeLayout',adj=1)  
        
        #mirrorSize
        pm.text('mirror Axis : ')
        self.xAxis = pm.button('X axis ',c = self.__setXAxis)
        self.zAxis = pm.button('Z axis ',c = self.__setZAxis)

        #scaleCurve
        self.sizeLayout = pm.rowLayout(p = self.shapeLayout,adj = 1,nc = 10)
        pm.button('scale curve',c = self.__scaleCv) 
        self.sizeFloatSlider = pm.floatSliderGrp('cvSize',f=1,max=1.0,v=0.0,min=-1.0)
        
        #remove this panel
        pm.separator(h = 10,p = self.mainL)
        self.removeB = pm.button(l = 'remove',c = self.__removeInstance,p = self.mainL)
        pm.separator(h = 10)
        
        self.__pointerClass = None
 
    def __removeInstance(self,*arg):
        
        pm.deleteUI(self.mainL)
        self.mainUi.modulesUi.remove(self) 
        
    def __selSkinJoint(self,*args):
        
        jointList = []
        
        metaT = pm.optionMenu(self.skinJointMenu, q = 1,v = 1)  
        meta = pm.ls(metaT)[0]
        jointStrs = pm.connectionInfo(meta.skinJoints, destinationFromSource=True) 
        pm.select(cl = 1) 
         
        for jointStr in jointStrs : 
            joint = jointStr.split('.') 
            pm.select(joint[0],add = 1)
            jointList.append(joint[0])
                
        print 'Skin joint from ' + metaT + ' are :'
        print 
        print  jointList
        print 
        print 'Number of ' + metaT + ' is ' + str(len(jointList))
        
    def __selPartialSkinJoint(self,*args):
        
        partialJointList = []
        
        metaT = pm.optionMenu(self.partialSkinJointMenu, q = 1,v = 1)  
        meta = pm.ls(metaT)[0]
        jointStrs = pm.connectionInfo(meta.partialSkinJoints, destinationFromSource=True) 
        pm.select(cl = 1) 
         
        for jointStr in jointStrs : 
            joint = jointStr.split('.') 
            pm.select(joint[0],add = 1)
            partialJointList.append(joint[0])
                
        print 'Partial Skin joint from ' + metaT + ' are :'
        print  
        print partialJointList
        print 
        print 'Number of ' + metaT + ' is ' + str(len(partialJointList))               
            
    def __splitJointButton(self,*args):
        
        sel = pm.ls(sl = 1)
        splitJoint = sel[0] 
        num = pm.intSliderGrp(self.splitNum,q = 1,v = 1)
        splitJoint =  SplitJoint(splitJoint,num,box = 1,type = 'tool')   
        splitJoint.splitJointTool()
        
    def __scaleCv(self,*args):
        
        scaleValue = pm.floatSliderGrp(self.sizeFloatSlider,q=1,v=1)
         
        if(scaleValue > 0):
            scaleValue = scaleValue+1
            
        if(scaleValue<0):
            scaleValue = 1-abs(scaleValue)/2
            
        sel = pm.ls(sl = 1)
        pm.select(cl = 1)
        
        for cv in sel:
            pm.select(cv + '.cv[*]',add = 1) 
        
        pm.scale(scaleValue,scaleValue,scaleValue,r=1)
        pm.select(cl = 1) 
        
        for obj in sel:
            pm.select(obj,add = 1)
 
    def __setXAxis(self,*args):
        
        self.axis = [-1,1,1]
        self.__mirrorShape()
        
    def __setZAxis(self,*args):     
    
        self.axis = [1,1,-1]
        self.__mirrorShape()
    
    def __mirrorShape(self,*args):
        
        ###init
        sel = pm.ls(sl = 1) 
        oriCvList = []
        tarCvList = []
        oriCvPosList = []
        tempPosList = []
        
        if len(sel) < 2:
            mel.eval('warning "Please cmds.select two Curve!"')
            return
        
        oriCur = sel[0] 
        tarCur = sel[1] 
        pm.select(cl = 1)
        
        #ori info get 
        pm.select(oriCur + '.cv[*]',add = 1) 
        oriCvs = pm.ls(sl = 1,fl = 1)
        for oriCv in oriCvs:
            oriCvList.append(oriCv) 
        pm.select(cl = 1)
        
        #tar info get    
        pm.select(tarCur + '.cv[*]',add = 1) 
        tarCvs = pm.ls(sl = 1,fl = 1)
        for tarCv in tarCvs:
            tarCvList.append(tarCv)
        pm.select(cl = 1)
            
        #mirror    
        if len(oriCvList) == len(tarCvList):
            
            for oriCv in oriCvList:
                oriCvPos = pm.xform(oriCv,q = 1,ws = 1,t = 1)
                oriCvPosList.append(oriCvPos)
             
            for oriCvPos in oriCvPosList: 
                tempPos = [self.axis[0] * oriCvPos[0],self.axis[1] * oriCvPos[1],self.axis[2] * oriCvPos[2]]
                tempPosList.append(tempPos)
            
            pm.select(tarCur + '.cv[*]',add = 1) 
            tarCvs = pm.ls(sl = 1,fl = 1)
            
            for num,tarCv in enumerate(tarCvs):
                pm.xform(tarCv,ws = 1,t = tempPosList[num])
                
            pm.select(cl = 1)    

    def __areaSkin(self,*args):

        geo = pm.ls(sl = 1)[0]
        skinCluster = mel.eval('findRelatedSkinCluster ' + geo)
        vertex = pm.polyEvaluate(geo,v = 1)
        joints = pm.skinCluster(skinCluster,q = 1,inf = 1)
        skinList = {}

        for num in range(0,vertex):
            vertex = geo + '.vtx[' + str(num) + ']'
            vertPos = pm.xform(vertex,q = 1,t = 1,ws = 1)
            tempDict = {}
          
            for joint in joints:
                jntPos = pm.xform(joint,q = 1,t = 1,ws = 1)
                dist = math.sqrt(pow(vertPos[0] - jntPos[0],2) + pow(vertPos[1] - jntPos[1],2) + pow(vertPos[2] - jntPos[2],2))
                tempDict.setdefault(joint,dist)
                  
            minDistVal = min(distVal for distVal in tempDict.values())
          
            for joint in tempDict.keys(): 
                if minDistVal == tempDict[joint]:
                    if joint not in skinList:
                        skinList[joint] = []
                    skinList[joint].append(vertex)
                      
        for item in skinList.items():
            joint =  item[0]
            vertex = item[1]
            for vert in vertex:
                pm.skinPercent(skinCluster,vert,transformValue = (joint,1))        

class SplitJoint(object):
    
    def __init__(self,splitJoint,num,type,box):
        
        self.splitJoint = splitJoint
        self.num = num 
        self.box = box
        self.joints = []
        self.cubeList = None
        self.type = type
                     
    def splitJointTool(self): 
         
        insertJointList = [] 
        pm.select(self.splitJoint) 
        parent = pm.ls(sl = 1)
        child = pm.listRelatives(parent,c = 1,typ = 'joint')
        
        parentPos = pm.xform(parent,q = 1,ws = 1,t = 1)
        childPos = pm.xform(child,q = 1,ws = 1,t = 1)
         
        self.joints.append(parent[0]) 
         
        #unparent
        pm.parent(child,w = 1)
         
        for i in range(0,self.num):
             
            pm.select(parent,r = 1) 
            tempPos = [(parentPos[0] - childPos[0])*(i + 1)/(self.num + 1) + childPos[0],
                       (parentPos[1] - childPos[1])*(i + 1)/(self.num + 1) + childPos[1],
                       (parentPos[2] - childPos[2])*(i + 1)/(self.num + 1) + childPos[2]]
            radius = pm.getAttr(parent[0] + '.radius')
            insertJoint = pm.joint(rad = radius,p = (tempPos[0],tempPos[1],tempPos[2]),
                                   n = (parent[0].name() + '_insert'))  
            insertJointList.append(insertJoint) 
        
        for num,joint in enumerate(insertJointList):
            if num != len(insertJointList) - 1:
                pm.parent(insertJointList[num],insertJointList[num + 1])
        
        insertJointList.reverse()
        for insertJoint in insertJointList:
            self.joints.append(insertJoint)        
         
        pm.parent(insertJointList[0],parent)
        pm.parent(child,insertJointList[-1])
        
        self.joints.append(child[0]) 
        
        if self.box == 1:
            self.boxCreate()
        
    def boxCreate(self):     
        
        self.cubeList = []
        #bos create
        #local variable
        a = 1
        count = 0
        pm.select(cl = 1)
        
        for joint in self.joints:
            pm.select(joint,add = 1) 
         
        joints = pm.ls(sl=1,type='joint')       
        child = pm.listRelatives(c=1) 
         
        #shader check:
        if not pm.objExists('green'):
            green = pm.shadingNode('lambert', asShader=True,n='green')
            pm.setAttr(green + '.color',0,1,0,type = "double3")
            pm.sets(r=True,nss=True,em=True,n='greenSG') 
            pm.connectAttr('green.outColor','greenSG.surfaceShader',f=True)
             
            red = pm.shadingNode('lambert', asShader=True,n='red')
            pm.setAttr(red + '.color',1,0,0,type = "double3") 
            pm.sets(r=True,nss=True,em=True,n='redSG') 
            pm.connectAttr('red.outColor','redSG.surfaceShader',f=True)
             
            blue = pm.shadingNode('lambert', asShader=True,n='blue')
            pm.setAttr(blue + '.color',0,0,1,type = "double3") 
            pm.sets(r=True,nss=True,em=True,n='blueSG') 
            pm.connectAttr('blue.outColor','blueSG.surfaceShader',f=True)
             
        #rolling:
        for joint in joints:       
            cube = pm.polyCube(n=joint.name() + '_geo_' + str(a),sx=1,sy=1,sz=1)
            self.cubeList.append(cube)
            pm.parent(cube,joint)
            if count < (len(joints)-1):
                tx = pm.getAttr(child[count] + '.tx')
                ty = pm.getAttr(child[count] + '.ty')
                tz = pm.getAttr(child[count] + '.tz')
                         
                abtx = abs(tx)
                abty = abs(ty)
                abtz = abs(tz)
                 
                pm.setAttr(cube[0] + '.tx',tx * 0.5)
                pm.setAttr(cube[0] + '.ty',ty * 0.5)
                pm.setAttr(cube[0] + '.tz',tz * 0.5)
                pm.setAttr(cube[0] + '.r',0,0,0)
             
                radius = pm.getAttr(joint + '.radius')
             
                if abtx > 0.001:
                    sx = abtx
                else :    
                    sx = radius
                 
                if abty > 0.001:
                    sy = abty
                else :    
                    sy = radius
            
                if abtz > 0.001:
                    sz = abtz
                else :    
                    sz = radius            
             
                pm.setAttr(cube[0] + '.sx',sx)
                pm.setAttr(cube[0] + '.sy',sy)
                pm.setAttr(cube[0] + '.sz',sz)
                 
                #set material
                greenFace = pm.select(cube[0] + '.f[0]',cube[0] + '.f[2]')  
                mc.sets(fe = 'greenSG',e=True) 
                 
                redFace = pm.select(cube[0] + '.f[1]',cube[0] + '.f[3]') 
                mc.sets(fe = 'redSG',e=True)
                 
                blueFace = pm.select(cube[0] + '.f[4]',cube[0] + '.f[5]') 
                mc.sets(fe = 'blueSG',e=True)
     
                #clear history
                pm.select(cube[0])
                pm.makeIdentity(cube[0],t=1,s=1,r=1,a=1)
                 
                #go head TAC-com
                a += 1
                count += 1
                control.lockAndHideAttr(cube[0],['tx','ty','tz','rx','ry','rz','sx','sy','sz'])     
        #break the cycle delete the tail       
        pm.delete(self.cubeList[-1])
        self.cubeList.pop()          
                
