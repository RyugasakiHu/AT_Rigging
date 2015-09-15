import control,limbModule,hierarchy,legModule

def reloadIt():
    reload(control)
    reload(limbModule)
    reload(hierarchy)
    reload(legModule)
    
    print '----->Modules Reload : OK'
