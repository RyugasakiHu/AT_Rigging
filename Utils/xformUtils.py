from maya import OpenMaya
import pymel.core as pm
import nameUtils

def zero(obj):
    #get parent object 
    par = obj.getParent()
    
    #create group name
    name = obj.name()
    temp = name.split('_')
    #name = 'character_name' + side + '_' + basename + str(0) +  '_' + suffix
    #charactername_r_wrist_0_loc
    groupName = nameUtils.getUniqueName(temp[1], temp[2], 'grp')
    if not groupName:
        OpenMaya.MGlobal.displayError('Error generating name')
        return
    
    #create group
    
    grp = pm.createNode('transform', n =groupName)
    
    #set martix
    matrix = obj.wm.get()
    
    grp.setMatrix(matrix)
    
    #rebuild hierachy
    
    obj.setParent(grp)
    if par:
        grp.setParent(par)
    
    return grp
# 
#     print grp,par,groupName,matrix
#     
