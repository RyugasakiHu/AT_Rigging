import pymel.core as pm
import maya.cmds as mc
from Modules import control

class Ribbon(object):

#     def __init__(self, RibbonName = 'Ribbon',Width = 1.0,Length = 5.0,UVal = 1,VVal = 5):
    def __init__(self, RibbonName,Width,Length,UVal,VVal):        
        '''
        initialize para
        '''
        
        self.RibbonName = RibbonName
        self.Width = Width
        self.Length = Length
        self.UVal = UVal
        self.VVal = VVal
        
        '''
        help para
        '''
        self.startloc = None
        self.midloc = None
        self.endloc = None
        
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
        
        #create burbs plane
        ribbonGeo = pm.nurbsPlane(p = (0,0,0),ax = (0,1,0),w = self.Width,lr = self.Length,d = 3,u = self.UVal,v = self.VVal,ch = 1,n = (self.RibbonName + '_Rbbn01_geo_01_'))

        #rebuild ribbon geo
        if self.VVal > self.UVal:
            pm.rebuildSurface(ribbonGeo[0],ch = 1,rpo = 1,rt = 0,end = 1,kr = 0,kcp = 0,kc = 0,su = self.UVal,du = 1,sv = self.VVal,dv = 3,tol = 0.000155,fr = 0,dir = 2)
            
        if self.UVal > self.VVal:
            pm.rebuildSurface(ribbonGeo[0],ch = 1,rpo = 1,rt = 0,end = 1,kr = 0,kcp = 0,kc = 0,su = self.UVal,du = 3,sv = self.VVal,dv = 1,tol = 0.000155,fr = 0,dir = 2)
        
        #clear history of ribbonGeometry
        pm.select(ribbonGeo[0],r = 1)
        pm.delete(ch = 1)
        
        #CREATE THE HAIR FOLLICLES
        pm.select(ribbonGeo[0],r = 1)
        mc.CreateHair(self.VVal,self.UVal,0,0,0,0,0,5,0,3,1,1)
        
        selFols = pm.select(self.RibbonName + '_Rbbn01_geo_01' + '*Follicle*',r = 1)
        folGrp = pm.group(n = self.RibbonName + '_Rbbn01_fol_grp')
        pm.parent(w = 1)
        pm.delete('hairSystem*')
        pm.delete('curve*')
        pm.delete('pfxHair1')
        pm.delete('nucleus1')
        
        selFols = pm.select(self.RibbonName + '_Rbbn01_geo_01' + '*Follicle*',r = 1)
        sel = pm.ls(sl = 1)        
        
        for i in range(len(sel)/2):
            j = i + 1
            newName = (self.RibbonName + '_Rbbn0' + str(i) + '_fol')
            pm.rename(sel[i],newName)
        
        #CREATE JOINTS SNAPPED AND PARENTED TO THE FOLLICLE---
        pm.select(cl = 1)    
        for a in range(len(sel)/2):
            b = a + 1
            #pm.joint(self.chain[0].name(),e = 1,oj = 'yzx',secondaryAxisOrient = 'zup',ch = 1)
            jJoint = pm.joint(n = self.RibbonName + '_Rbbn0' + str(a) + '_jj',p = (0,0,0),rad = min(self.Width,self.Length) * .25)
            pm.parent(self.RibbonName + '_Rbbn0' + str(a) + '_jj',self.RibbonName + '_Rbbn0' + str(a) + '_fol',r = True)
            self.jj.append(jJoint) 
            pm.select(cl = 1)
        #CREATE SOME TEMPORARY CLUSTERS TO PLACE THE POS LOCATORS---
        if self.UVal > self.VVal:
            vNo = self.UVal + 2
            pm.select(self.RibbonName + '_Rbbn01_geo_01_.cv[' + str(vNo) + '][0:1]',r = 1)
            pm.cluster(n = 'spCltr')
            pm.select(self.RibbonName + '_Rbbn01_geo_01_.cv[0][0:1]',r = 1)
            pm.cluster(n = 'epCltr')
            
        if self.VVal > self.UVal:
            vNo = self.VVal + 2
            pm.select(self.RibbonName + '_Rbbn01_geo_01_.cv[0:1][' + str(vNo) + ']',r = 1)
            pm.cluster(n = 'spCltr')
            pm.select(self.RibbonName + '_Rbbn01_geo_01_.cv[0:1][0]',r = 1)
            pm.cluster(n = 'epCltr')                
            
        #CREATE SOME LOCATORS---
        #CREATE START POINT LOCATORS AND PARENT THEM PROPERLY---
        spLocPos = pm.spaceLocator(p = (0,0,0), n = self.RibbonName + '_RbbnSp01_pos')
        spLocAim = pm.spaceLocator(p = (0,0,0), n = self.RibbonName + '_RbbnSp01_aim')
        spLocUp = pm.spaceLocator(p = (0,0,0), n = self.RibbonName + '_RbbnSp01_up')
        
        #hide shape
#         spLocPos.getShape().v.set(0)
#         spLocAim.getShape().v.set(0)
#         spLocUp.getShape().v.set(0)
        
        self.startloc = spLocPos
        
        pm.parent(spLocAim,spLocPos)
        pm.parent(spLocUp,spLocPos)
        
        #CREATE MID POINT LOCATORS AND PARENT THEM PROPERLY---
        mpLocPos = pm.spaceLocator(p = (0,0,0), n = self.RibbonName + '_RbbnMp01_pos')
        self.mpLocAim = pm.spaceLocator(p = (0,0,0), n = self.RibbonName + '_RbbnMp01_aim')
        mpLocUp = pm.spaceLocator(p = (0,0,0), n = self.RibbonName + '_RbbnMp01_up')
        
        #hide shape
        mpLocPos.getShape().v.set(0)
        self.mpLocAim.getShape().v.set(0)
        mpLocUp.getShape().v.set(0)
        
        self.midloc = mpLocPos
        
        pm.parent(self.mpLocAim,mpLocPos)
        pm.parent(mpLocUp,mpLocPos)   
        
        #CREATE END POINT LOCATORS AND PARENT THEM PROPERLY---
        epLocPos = pm.spaceLocator(p = (0,0,0), n = self.RibbonName + '_RbbnEp01_pos')
        epLocAim = pm.spaceLocator(p = (0,0,0), n = self.RibbonName + '_RbbnEp01_aim')
        epLocUp = pm.spaceLocator(p = (0,0,0), n = self.RibbonName + '_RbbnEp01_up')
        
        #hide shape
        epLocPos.getShape().v.set(0)
        epLocAim.getShape().v.set(0)
        epLocUp.getShape().v.set(0)
        
        self.endloc = epLocPos
        
        pm.parent(epLocAim,epLocPos)
        pm.parent(epLocUp,epLocPos)     
        
        
        #CONSTRAINT EACH LOCATORS PROPERLY---                                                   
        pm.pointConstraint('spCltrHandle',spLocPos,o = (0,0,0),w = 1)                                    
        pm.delete(self.RibbonName + '_RbbnSp01_pos_pointConstraint1')
        
        pm.pointConstraint('epCltrHandle',epLocPos,o = (0,0,0),w = 1)                                    
        pm.delete(self.RibbonName + '_RbbnEp01_pos_pointConstraint1')
        
        pm.pointConstraint(spLocPos,epLocPos,mpLocPos,o = (0,0,0),w = 1)    
        pm.pointConstraint(spLocUp,epLocUp,mpLocUp,o = (0,0,0),w = 1)
    
        #OFFSET THE POSITION OF THE UP LOCATOR---
     
        pm.setAttr(spLocUp.ty,min(self.Width,self.Length) * .5)
        pm.setAttr(epLocUp.ty,min(self.Width,self.Length) * .5)       
        
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
        self.startJc = pm.joint(p = (0,0,0),rad = min(self.Width,self.Length) * .5,n = self.RibbonName + '_RbbnSp01_jc')
        pm.joint(p = (tx * .6,0,tz * .6),rad = min(self.Width,self.Length) * .5,n = self.RibbonName + '_RbbnSp02_jc')
        pm.joint(e = 1,zso = 1,oj = 'xyz',sao = 'yup',n = self.RibbonName + '_RbbnSp02_jc')
        
        #FOR MIDDLE POINT JOINT---
        pm.select(cl = 1)
        self.midJc = pm.joint(p = (0,0,0),rad = min(self.Width,self.Length) * .5,n = self.RibbonName + '_RbbnMp01_jc')
        pm.joint(e = 1,zso = 1,oj = 'xyz',sao = 'yup',n = self.RibbonName + '_RbbnMp01_jc')
        
        #FOR END POINT JOINT---
        pm.select(cl = 1)
        self.endJc = pm.joint(p = (0,0,0),rad = min(self.Width,self.Length) * .5,n = self.RibbonName + '_RbbnEp01_jc')
        pm.joint(p = (tx * -0.6,0,tz * -0.6),rad = min(self.Width,self.Length) * .5,n = self.RibbonName + '_RbbnEp02_jc')
        pm.joint(e = 1,zso = 1,oj = 'xyz',sao = 'yup',n = self.RibbonName + '_RbbnEp02_jc')  
    
        #PARENT THE CONTROL JOINTS APPROPRIATLY---     
        pm.parent(self.RibbonName + "_RbbnSp01_jc",spLocAim,r = 1)
        pm.parent(self.RibbonName + "_RbbnMp01_jc",self.mpLocAim,r = 1)
        pm.parent(self.RibbonName + "_RbbnEp01_jc",epLocAim,r = 1)
        

        
        #APPLY THE AIM CONSTRINTS---
        aTz = 0
        if self.VVal > self.UVal:
            aTz = 1
            
        aTx = 0
        if self.UVal > self.VVal:
            aTx = 1
        
        #FOR MIDDLE POINT---
        pm.aimConstraint(self.RibbonName + "_RbbnSp01_pos",self.RibbonName + "_RbbnMp01_aim",o = (0,0,0),w = 1,aim = (aTx * -1,0,aTz *  -1),u = (0,1,0),wut = 'object',wuo = self.RibbonName + '_RbbnMp01_up')
        #FOR START POINT---
        pm.aimConstraint(self.RibbonName + "_RbbnMp01_jc",self.RibbonName + "_RbbnSp01_aim",o = (0,0,0),w = 1,aim = (aTx,0,aTz),u = (0,1,0),wut = 'object',wuo = self.RibbonName + '_RbbnSp01_up')
        #FOR END POINT---
        pm.aimConstraint(self.RibbonName + "_RbbnMp01_jc",self.RibbonName + "_RbbnEp01_aim",o = (0,0,0),w = 1,aim = (aTx * -1,0,aTz *  -1),u = (0,1,0),wut = 'object',wuo = self.RibbonName + '_RbbnEp01_up')
            
        #APPLY SKINCLUSTER---
        pm.select(cl = 1)
        pm.skinCluster(self.RibbonName + "_RbbnSp01_jc",self.RibbonName + "_RbbnMp01_jc",self.RibbonName + "_RbbnEp01_jc",self.RibbonName + "_Rbbn01_geo_01_",tsb = 1,ih = 1,mi = 3,dr = 4,rui = 1)
        
        #CLEAN UP
        pm.delete('spCltrHandle')
        pm.delete('epCltrHandle')
        pm.rename(self.RibbonName + '_Rbbn01_geo_01_',self.RibbonName + '_Rbbn01_geo_01')  
        
        #GROUP THEM ALL
        self.main = pm.group(self.RibbonName + '_Rbbn01_fol_grp',self.RibbonName + '_Rbbn01_geo_01',self.RibbonName + '_RbbnSp01_pos',self.RibbonName + '_RbbnMp01_pos',self.RibbonName + '_RbbnEp01_pos',n = self.RibbonName + "_Rbbn01_grp")
        pm.xform(os = 1,piv = (0,0,0))
        
#         print self.startJc,self.midJc,self.endJc
    
# from Modules.subModules import ribbon
# ribon45hp = ribbon.Ribbon(RibbonName = 'Ribbon',Width = 1.0,Length = 5.0,UVal = 1,VVal = 5)
# ribon45hp.construction()
