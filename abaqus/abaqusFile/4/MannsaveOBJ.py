from abaqus import *
from abaqusConstants import *
import __main__


import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior
import numpy as np
#os.getcwd()

#print(fileNAME)
#np.savetxt("D:/Software/abaqus2020/temp/script/AbaqusScript/name.txt", fileNAME, fmt="%s")
#D:\Software\abaqus2020\temp\script\AbaqusScript




# session.mdbData.summary()
# session.viewports['Viewport: 1'].setValues(
    # displayedObject=session.odbs[odbFile])
# o3 = session.openOdb(name=odbFile)
# session.viewports['Viewport: 1'].setValues(displayedObject=o3)
# session.viewports['Viewport: 1'].makeCurrent()
# session.viewports['Viewport: 1'].view.setValues(nearPlane=1.13824, 
    # farPlane=1.73435, width=0.476951, height=0.270356, cameraPosition=(
    # 1.52335, 0.643999, -0.337639), cameraUpVector=(-0.489093, 0.872081, 
    # -0.0161989), cameraTarget=(0.368814, 0.458902, -0.080335), 
    # viewOffsetX=-0.0183398, viewOffsetY=-0.165387)
# session.viewports['Viewport: 1'].odbDisplay.setFrame(step=1, frame=83 )
# session.viewports['Viewport: 1'].odbDisplay.setFrame(step=1, frame=83 )
# session.viewports['Viewport: 1'].odbDisplay.setFrame(step=1, frame=83 )
# session.linkedViewportCommands.setValues(_highlightLinkedViewports=True)
# leaf = dgo.LeafFromPartInstance(partInstanceName=("ELLIPSE-1", "ELLIPSE-2", 
    # "ELLIPSE-3", "PART-6-COPY-1", "RESTRICTSHARPROD-1", 
    # "RESTRICTSHARPROD-COPY-1", ))
# session.viewports['Viewport: 1'].odbDisplay.displayGroup.remove(leaf=leaf)
# session.viewports['Viewport: 1'].view.setValues(nearPlane=1.16374, 
    # farPlane=1.72984, width=0.487636, height=0.276413, cameraPosition=(
    # 1.44816, 0.212351, -0.693242), cameraUpVector=(-0.242406, 0.969041, 
    # -0.0468864), cameraTarget=(0.391536, 0.385789, -0.157628), 
    # viewOffsetX=-0.0187507, viewOffsetY=-0.169092)
# session.writeOBJFile(
    # fileName=fileNAME, 
    # canvasObjects= (session.viewports['Viewport: 1'], ))
    
    
    
import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior
# odbFile = os.path.join(os.getcwd(),"Job-Man.odb")
# fileNAME = sys.argv[-1]
# session.mdbData.summary()
# o1 = session.openOdb(
    # name=odbFile)
# session.viewports['Viewport: 1'].setValues(displayedObject=o1)
# session.viewports['Viewport: 1'].view.setValues(nearPlane=0.830023, 
    # farPlane=1.57415, width=0.469713, height=0.382807, cameraPosition=(
    # 1.29499, 0.618026, 0.240981), cameraUpVector=(-0.594761, 0.791407, 
    # -0.141192))
# session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    # DEFORMED, ))
# session.viewports['Viewport: 1'].view.setValues(nearPlane=0.904202, 
    # farPlane=1.51041, width=0.511691, height=0.417018, cameraPosition=(
    # 1.37114, 0.253341, -0.184461), cameraUpVector=(-0.339189, 0.939948, 
    # 0.0380681), cameraTarget=(0.186337, 0.243411, -0.0126731))
# #session.viewports['Viewport: 1'].odbDisplay.setFrame(step=1, frame=29 )
# session.linkedViewportCommands.setValues(_highlightLinkedViewports=True)
# leaf = dgo.LeafFromPartInstance(partInstanceName=("ELLIPSE-1", "ELLIPSE-2", 
    # "ELLIPSE-3", "PART-6-COPY-1", "RESTRICTSHARPROD-1", 
    # "RESTRICTSHARPROD-COPY-1", ))
# session.viewports['Viewport: 1'].odbDisplay.displayGroup.remove(leaf=leaf)
# session.viewports['Viewport: 1'].view.setValues(nearPlane=0.889819, 
    # farPlane=1.51455, width=0.503551, height=0.410384, cameraPosition=(
    # 1.38165, 0.229227, 0.0572015), cameraUpVector=(-0.320033, 0.946127, 
    # -0.049228), cameraTarget=(0.186426, 0.243207, -0.0106294))
# session.writeOBJFile(
    # fileName=fileNAME, 
    # canvasObjects= (session.viewports['Viewport: 1'], ))
    
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
odbFile = os.path.join(os.getcwd(),"Job-Man.odb")
fileNAME = sys.argv[-1]
session.mdbData.summary()
o1 = session.openOdb(
    name=odbFile)
    
    
session.viewports['Viewport: 1'].setValues(displayedObject=o1)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    DEFORMED, ))
session.linkedViewportCommands.setValues(_highlightLinkedViewports=True)
leaf = dgo.LeafFromPartInstance(partInstanceName=("MODEL1-VER2-CHEST-RIGHT-1", 
    "MODEL1-VER2-DOWNWAIST-1", "MODEL1-VER2-LEFTCHEST-1", 
    "MODEL1-VER2-UPWAIST-1", "MODEL1-VER2-WAISTBETWEEN-TRY2-1", ))
session.viewports['Viewport: 1'].odbDisplay.displayGroup.remove(leaf=leaf)

session.writeOBJFile(
fileName=fileNAME, 
canvasObjects= (session.viewports['Viewport: 1'], ))




