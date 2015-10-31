import autorig_settings
import nameUtils
import pymel.core as pm
    
def createHook(baseName = 'hook',side = 'm',snapTo = None,inOut = 'in'):
    
    hookName = nameUtils.getUniqueName(side, baseName, 'HOOK')
    hookNode = pm.createNode('locator',n = hookName)
    
    hookNode = hookNode.getParent()
    hookNode.rename(hookName)
    
    digitType = 0
    
    if inOut == 'out':
        digitType = 1
    
    hookNode.addAttr('hookType',at = 'float',dv = digitType)
    hookNode.attr('hookType').lock(1)
    
    if snapTo:
        pm.xform(hookNode,ws = 1,matrix = snapTo.wm.get())
        
    return hookNode
