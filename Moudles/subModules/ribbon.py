import pymel.core as pm
from Modules import control
from maya import OpenMaya,cmds

class Ribbon(object):

#     def __init__(self, RibbonName = 'Ribbon',Width = 1.0,Length = 5.0,UVal = 1,VVal = 5):
    def __init__(self, RibbonName,Width,Length,UVal,VVal,segment = 5,subMid = 0,side = 'm',baseName = 'Mid_CC'):        
        '''
        initialize para
        '''
        
        self.RibbonName = RibbonName
        self.Width = Width
        self.Length = Length
        self.UVal = UVal
        self.VVal = VVal
        self.subMid = subMid
        self.side = side
        self.baseName = baseName
        self.segment = segment
        
        self.folList = None
        self.folGrp = None
                
        self.startLoc = None
        self.midLoc = None
        self.endLoc = None
        self.epUploc = None
#         self.spLocAim = None
        self.mpLocAim = None
#         self.epLocAim = None
        
        self.startJc = None
        self.midJc = None
        self.endJc = None
        self.main = None
        
        self.subMidCtrl = None 
        
        self.jj = []


    def construction(self):
        
        self.folList = []
        
        #create burbs plane
        ribbonGeo = pm.nurbsPlane(p = (0,0,0),ax = (0,1,0),w = self.Width,lr = self.Length,
                                  d = 3,u = self.UVal,v = self.VVal,ch = 1,n = (self.side + '_' + self.RibbonName + '_Rbbn01_geo_01_'))

        #rebuild ribbon geo
        if self.VVal > self.UVal:
            pm.rebuildSurface(ribbonGeo[0],ch = 1,rpo = 1,rt = 0,end = 1,kr = 0,kcp = 0,kc = 0,su = self.UVal,du = 1,sv = self.VVal,dv = 3,tol = 0.000155,fr = 0,dir = 2)
            
        if self.UVal > self.VVal:
            pm.rebuildSurface(ribbonGeo[0],ch = 1,rpo = 1,rt = 0,end = 1,kr = 0,kcp = 0,kc = 0,su = self.UVal,du = 3,sv = self.VVal,dv = 1,tol = 0.000155,fr = 0,dir = 2)
        
        #clear history of ribbonGeometry
        pm.select(ribbonGeo[0],r = 1)
        pm.delete(ch = 1)
        
        #CREATE THE HAIR FOLLICLES
        self.folGrp = pm.group(em = 1,n = getUniqueName(self.side,self.RibbonName + 'Fol','grp')) 
        
        for fol in range(self.segment):
            
            #createNodeName
            follicleTransName = getUniqueName(self.side,self.RibbonName,'fol')
            follicleShapeName = getUniqueName(self.side,self.RibbonName,'folShape')
            
            #createNode
            follicleShape = pm.createNode('follicle',n = follicleShapeName)
            follicleTrans = pm.listRelatives(follicleShape, parent=True)[0]
            follicleTrans = pm.rename(follicleTrans, follicleTransName)
            
            # connect the surface to the follicle
            
            if ribbonGeo[0].getShape().nodeType() == 'nurbsSurface':
                pm.connectAttr((ribbonGeo[0] + '.local'), (follicleShape + '.inputSurface'))
                
            #Connect the worldMatrix of the surface into the follicleShape
            pm.connectAttr((ribbonGeo[0] + '.worldMatrix[0]'), (follicleShape + '.inputWorldMatrix'))
            
            #Connect the follicleShape to it's transform
            pm.connectAttr((follicleShape + '.outRotate'), (follicleTrans + '.rotate'))
            pm.connectAttr((follicleShape + '.outTranslate'), (follicleTrans + '.translate'))
            
            #Set the uValue and vValue for the current follicle
            pm.setAttr((follicleShape + '.parameterU'), 0.5)
            pm.setAttr((follicleShape + '.parameterV'), float(1.0 / self.segment) * fol + (1.0 / (self.segment * 2)))
            
            #Lock the translate/rotate of the follicle
            pm.setAttr((follicleTrans + '.translate'), lock=True)
            pm.setAttr((follicleTrans + '.rotate'), lock=True)
            
            #parent
            self.folList.append(follicleTrans)
            follicleTrans.setParent(self.folGrp)

        #CREATE JOINTS SNAPPED AND PARENTED TO THE FOLLICLE---

        for num,fol in enumerate(self.folList):
            jJoint = pm.joint(n = self.side + '_' + self.RibbonName + '_Rbbn0' + str(num) + '_jj',p = (0,0,0),rad = min(self.Width,self.Length) * .25)
            pm.parent(jJoint,fol)
            jJoint.translate.set(0,0,0)
            self.jj.append(jJoint)
             
        #CREATE SOME TEMPORARY CLUSTERS TO PLACE THE POS LOCATORS---
        if self.UVal > self.VVal:
            vNo = self.UVal + 2
            pm.select(self.side + '_' + self.RibbonName + '_Rbbn01_geo_01_.cv[' + str(vNo) + '][0:1]',r = 1)
            startCls =  pm.cluster(n = 'spCltr')
            pm.select(self.side + '_' + self.RibbonName + '_Rbbn01_geo_01_.cv[0][0:1]',r = 1)
            endCls = pm.cluster(n = 'epCltr')
             
        if self.VVal > self.UVal:
            vNo = self.VVal + 2
            pm.select(self.side + '_' + self.RibbonName + '_Rbbn01_geo_01_.cv[0:1][' + str(vNo) + ']',r = 1)
            startCls = pm.cluster(n = 'spCltr')
            pm.select(self.side + '_' + self.RibbonName + '_Rbbn01_geo_01_.cv[0:1][0]',r = 1)
            endCls = pm.cluster(n = 'epCltr')                
             
        #CREATE SOME LOCATORS---
        #CREATE START POINT LOCATORS AND PARENT THEM PROPERLY---
        spLocPos = pm.spaceLocator(p = (0,0,0), n = self.side + '_' + self.RibbonName + '_RbbnSp01_pos')
        spLocAim = pm.spaceLocator(p = (0,0,0), n = self.side + '_' + self.RibbonName + '_RbbnSp01_aim')
        spLocUp = pm.spaceLocator(p = (0,0,0), n = self.side + '_' + self.RibbonName + '_RbbnSp01_up')
         
        #hide shape
#         spLocPos.getShape().v.set(0)
#         spLocAim.getShape().v.set(0)
#         spLocUp.getShape().v.set(0)
         
        self.startLoc = spLocPos
         
        pm.parent(spLocAim,spLocPos)
        pm.parent(spLocUp,spLocPos)
         
        #CREATE MID POINT LOCATORS AND PARENT THEM PROPERLY---
        mpLocPos = pm.spaceLocator(p = (0,0,0), n = self.side + '_' + self.RibbonName + '_RbbnMp01_pos')
        self.mpLocAim = pm.spaceLocator(p = (0,0,0), n = self.side + '_' + self.RibbonName + '_RbbnMp01_aim')
        mpLocUp = pm.spaceLocator(p = (0,0,0), n = self.side + '_' + self.RibbonName + '_RbbnMp01_up')
         
        #hide shape
        mpLocPos.getShape().v.set(0)
        self.mpLocAim.getShape().v.set(0)
        mpLocUp.getShape().v.set(0)
         
        self.midloc = mpLocPos
         
        pm.parent(self.mpLocAim,mpLocPos)
        pm.parent(mpLocUp,mpLocPos)   
         
        #CREATE END POINT LOCATORS AND PARENT THEM PROPERLY---
        epLocPos = pm.spaceLocator(p = (0,0,0), n = self.side + '_' + self.RibbonName + '_RbbnEp01_pos')
        epLocAim = pm.spaceLocator(p = (0,0,0), n = self.side + '_' + self.RibbonName + '_RbbnEp01_aim')
        self.epUploc = pm.spaceLocator(p = (0,0,0), n = self.side + '_' + self.RibbonName + '_RbbnEp01_up')
         
        #hide shape
        epLocPos.getShape().v.set(0)
        epLocAim.getShape().v.set(0)
        self.epUploc.getShape().v.set(0)
         
        self.endLoc = epLocPos
         
        pm.parent(epLocAim,epLocPos)
        pm.parent(self.epUploc,epLocPos)     
         
        #CONSTRAINT EACH LOCATORS PROPERLY---                                                   
        pm.pointConstraint('spCltrHandle',spLocPos,o = (0,0,0),w = 1)                                    
        pm.delete(self.side + '_' + self.RibbonName + '_RbbnSp01_pos_pointConstraint1')
         
        pm.pointConstraint('epCltrHandle',epLocPos,o = (0,0,0),w = 1)                                    
        pm.delete(self.side + '_' + self.RibbonName + '_RbbnEp01_pos_pointConstraint1')
         
        pm.pointConstraint(spLocPos,epLocPos,mpLocPos,o = (0,0,0),w = 1)    
        pm.pointConstraint(spLocUp,self.epUploc,mpLocUp,o = (0,0,0),w = 1)
     
        #OFFSET THE POSITION OF THE UP LOCATOR---
      
        pm.setAttr(spLocUp.ty,min(self.Width,self.Length) * .5)
        pm.setAttr(self.epUploc.ty,min(self.Width,self.Length) * .5)       
         
        #CREATE CTRL JOINTS
        pm.select(cl = 1)
        tx = tz = 0.0
        if self.VVal > self.UVal:
            tz = self.Length * .2
             
        if self.UVal > self.VVal:
            tx = self.Width * .2    
             
        #############   
         
        #transmit Jc joint info---
        #FOR START POINT JOINT---
        self.startJc = pm.joint(p = (0,0,0),rad = min(self.Width,self.Length) * .5,n = self.side + '_' + self.RibbonName + '_RbbnSp01_jc')
        pm.joint(p = (tx * .6,0,tz * .6),rad = min(self.Width,self.Length) * .5,n = self.side + '_' + self.RibbonName + '_RbbnSp02_jc')
        pm.joint(e = 1,zso = 1,oj = 'xyz',sao = 'yup',n = self.side + '_' + self.RibbonName + '_RbbnSp02_jc')
         
        #FOR MIDDLE POINT JOINT---
        pm.select(cl = 1)
        self.midJc = pm.joint(p = (0,0,0),rad = min(self.Width,self.Length) * .5,n = self.side + '_' + self.RibbonName + '_RbbnMp01_jc')
        pm.joint(e = 1,zso = 1,oj = 'xyz',sao = 'yup',n = self.side + '_' + self.RibbonName + '_RbbnMp01_jc')
         
        #FOR END POINT JOINT---
        pm.select(cl = 1)
        self.endJc = pm.joint(p = (0,0,0),rad = min(self.Width,self.Length) * .5,n = self.side + '_' + self.RibbonName + '_RbbnEp01_jc')
        pm.joint(p = (tx * -0.6,0,tz * -0.6),rad = min(self.Width,self.Length) * .5,n = self.side + '_' + self.RibbonName + '_RbbnEp02_jc')
        pm.joint(e = 1,zso = 1,oj = 'xyz',sao = 'yup',n = self.side + '_' + self.RibbonName + '_RbbnEp02_jc')  
     
        #PARENT THE CONTROL JOINTS APPROPRIATLY---     
        pm.parent(self.side + '_' + self.RibbonName + "_RbbnSp01_jc",spLocAim,r = 1)
        pm.parent(self.side + '_' + self.RibbonName + "_RbbnMp01_jc",self.mpLocAim,r = 1)
        pm.parent(self.side + '_' + self.RibbonName + "_RbbnEp01_jc",epLocAim,r = 1)
         
        #APPLY THE AIM CONSTRINTS---
        aTz = 0
        if self.VVal > self.UVal:
            aTz = 1
             
        aTx = 0
        if self.UVal > self.VVal:
            aTx = 1
         
        #FOR MIDDLE POINT---
        pm.aimConstraint(self.side + '_' + self.RibbonName + "_RbbnSp01_pos",self.side + '_' + self.RibbonName + "_RbbnMp01_aim",o = (0,0,0),w = 1,aim = (aTx * -1,0,aTz *  -1),u = (0,1,0),wut = 'object',wuo = self.side + '_' + self.RibbonName + '_RbbnMp01_up')
        #FOR START POINT---
        pm.aimConstraint(self.side + '_' + self.RibbonName + "_RbbnMp01_jc",self.side + '_' + self.RibbonName + "_RbbnSp01_aim",o = (0,0,0),w = 1,aim = (aTx,0,aTz),u = (0,1,0),wut = 'object',wuo = self.side + '_' + self.RibbonName + '_RbbnSp01_up')
        #FOR END POINT---
        pm.aimConstraint(self.side + '_' + self.RibbonName + "_RbbnMp01_jc",self.side + '_' + self.RibbonName + "_RbbnEp01_aim",o = (0,0,0),w = 1,aim = (aTx * -1,0,aTz *  -1),u = (0,1,0),wut = 'object',wuo = self.side + '_' + self.RibbonName + '_RbbnEp01_up')
             
        #APPLY SKINCLUSTER---
        pm.select(cl = 1)
        pm.skinCluster(self.side + '_' + self.RibbonName + "_RbbnSp01_jc",self.side + '_' + self.RibbonName + "_RbbnMp01_jc",self.side + '_' + self.RibbonName + "_RbbnEp01_jc",self.side + '_' + self.RibbonName + "_Rbbn01_geo_01_",tsb = 1,ih = 1,mi = 3,dr = 4,rui = 1)
         
        #CLEAN UP
        pm.delete(startCls)
        pm.delete(endCls)
        pm.rename(self.side + '_' + self.RibbonName + '_Rbbn01_geo_01_',self.side + '_' + self.RibbonName + '_Rbbn01_geo_01')  
         
        #GROUP THEM ALL
        self.main = pm.group(self.folGrp,self.side + '_' + self.RibbonName + '_Rbbn01_geo_01',self.side + '_' + self.RibbonName + '_RbbnSp01_pos',self.side + '_' + self.RibbonName + '_RbbnMp01_pos',self.side + '_' + self.RibbonName + '_RbbnEp01_pos',n = self.side + '_' + self.RibbonName + "_Rbbn01_grp")
        pm.xform(os = 1,piv = (0,0,0))
         
        if self.subMid == 1:
            self.__midCC()
    
# from Modules.subModules import ribbon
# ribon45hp = ribbon.Ribbon(RibbonName = 'Ribbon',Width = 1.0,Length = 5.0,UVal = 0.5,VVal = 5)
# ribon45hp.construction()

    def __midCC(self):
        
        self.subMidCtrl = control.Control(size = 1,baseName = self.baseName,side = self.side) 
        self.subMidCtrl.circleCtrl()
        pm.setAttr(self.subMidCtrl.controlGrp +'.ry',90)
        #add parent cnst for the mid jc
        pm.parentConstraint(self.subMidCtrl.control,self.midJc,mo = 1)
        #add parent cnst for sub grp 
        pm.parentConstraint(self.mpLocAim,self.subMidCtrl.controlGrp,mo = 1)
        
def getUniqueName(side,basename,suf):
    
    security = 1000
    
    sides = ['l','m','r']
    suffix = ['grp','fol','folShape']
    
    if not side in sides:
        OpenMaya.MGlobal.displayError('Side is not valid')
        return
    
    if not suf in suffix:
        OpenMaya.MGlobal.displayError('Suffix is not valid')
        return
    
    name = side + '_' + basename + '_' + str(0) +  '_' + suf
       
    i = 0
    while (cmds.objExists(name) == 1):
        if(i < security):
            i += 1
            name = side + '_' + basename + '_' + str(i) +  '_' + suf
            
    return name    
        
