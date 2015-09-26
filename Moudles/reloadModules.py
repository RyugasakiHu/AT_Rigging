import control,limbModule,hierarchy,legModule,footModule,fingerModule

def reloadIt():
    reload(control)
    reload(limbModule)
    reload(hierarchy)
    reload(legModule)
    reload(footModule)
    reload(fingerModule)
    
    print '----->Modules Reload : OK'
