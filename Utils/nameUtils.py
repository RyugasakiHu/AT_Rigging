from maya import OpenMaya,cmds
import autorig_settings

def getUniqueName(side,basename,suffix):
    
    security = 1000
    
    if not side in autorig_settings.sides:
        OpenMaya.MGlobal.displayError('Side is not valid')
        return
    
    if not suffix in autorig_settings.suffix:
        OpenMaya.MGlobal.displayError('Suffix is not valid')
        return
    
    name = 'CN' + '_' + side + '_' + basename + '_' + str(0) +  '_' + suffix
       
    i = 0
    while (cmds.objExists(name) == 1):
        if(i < security):
            i += 1
            name = 'CN' + '_' + side + '_' + basename + '_' + str(i) +  '_' + suffix
            
    return name           

def getHierachyName(characterName,suffix):
    
    if not suffix in autorig_settings.suffix:
        OpenMaya.MGlobal.displayError('Suffix is not valid')
        return
    
    name = characterName + '_' + suffix
    
    if cmds.objExists(name) == 1:
        OpenMaya.MGlobal.displayError('Name repeated')

    return name    
