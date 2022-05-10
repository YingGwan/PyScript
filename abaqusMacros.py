# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__

def save():
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    
    session.linkedViewportCommands.setValues(_highlightLinkedViewports=True)
    leaf = dgo.LeafFromPartInstance(partInstanceName=("CHEST-LEFT-1", 
        "CHEST-RIGHT-1", "WAIST-DOWN-1", "WAIST-MIDDLE-1", "WAIST-UP-1", ))
    session.viewports['Viewport: 1'].odbDisplay.displayGroup.remove(leaf=leaf)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=0.820754, 
        farPlane=1.45846, width=0.745767, height=0.384294, 
        viewOffsetX=0.00509369, viewOffsetY=0.0109739)
    session.writeOBJFile(
        fileName='H:/DropBoxNewFolder/2022-ML-based-Soft-Mannequin-Control/AbaqusScript-ML/client-original/model.obj', 
        canvasObjects= (session.viewports['Viewport: 1'], ))


def save2():
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    session.linkedViewportCommands.setValues(_highlightLinkedViewports=True)
    leaf = dgo.LeafFromPartInstance(partInstanceName=("CHEST-LEFT-1", 
        "CHEST-RIGHT-1", "WAIST-DOWN-1", "WAIST-MIDDLE-1", "WAIST-UP-1", ))
    session.viewports['Viewport: 1'].odbDisplay.displayGroup.remove(leaf=leaf)


def Macro4():
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
        DEFORMED, ))
    session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=0 )
    session.viewports['Viewport: 1'].odbDisplay.setFrame(step=4, frame=21 )


