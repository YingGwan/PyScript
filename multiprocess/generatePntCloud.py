'''
This is used to handle a huge amounts of mesh files,
converting them to disconnected point cloud
'''

import numpy as np
import open3d as o3d
import trimesh as tm
import itertools
import networkx as nx
from os import listdir
from os.path import isfile, join
import multiprocess
from multiprocess import Process, Queue
from multiprocess import Condition
import time

'''
'''
npactiveProcessNum = 0

activeProcessNum = multiprocess.Value('i', npactiveProcessNum)
maximumProcessNum = 10

lock_of_data = multiprocess.RLock()               #in order to access same data structure
lock_of_outstream = multiprocess.RLock()  
'''
    Different process will call the same template function
'''
def _generateSinglePCD(inputFileName, outputFileName,activeProcessNum):

    mesh = tm.load_mesh(inputFileName)
    vArray = np.asarray(mesh.vertices)
    fArray = np.asarray(mesh.faces)
    eArray = np.asarray(mesh.edges)
    edges = []
    faces = fArray
    for face in faces:
        edges.extend(list(itertools.combinations(face, 2)))
    g = nx.from_edgelist(edges)
    # compute connected components and print results
    components = list(nx.algorithms.components.connected_components(g))
    colors = np.zeros([vArray.shape[0],3],dtype = float)
    rgb = [[1,0,0],[0,1,0],[0,0,1],[1,1,0],[1,0,1],[0,1,1]]
    rgb = np.asarray(rgb)
    VertexNumberArray = np.zeros([len(components)],dtype = int)
    index = 0
    for component in components:
        VertexNumberArray[index] = len(component)
        index = index + 1
    maxValue = np.amax(VertexNumberArray)
    maxIdx = VertexNumberArray.argmax(axis=0)
    index = 0
    membraneVertexIndexArray = []
    membraneVArray = np.zeros([maxValue,3],dtype=float)
    for component in components:
        if index == maxIdx:
            vIdx = 0
            for j in component:
            
                colors[j,0] = rgb[index,0]
                colors[j,1] = rgb[index,1]
                colors[j,2] = rgb[index,2]
                
                membraneVArray[vIdx, 0] = vArray[j,0]
                membraneVArray[vIdx, 1] = vArray[j,1]
                membraneVArray[vIdx, 2] = vArray[j,2]
                
                vIdx = vIdx + 1
            membraneVertexIndexArray = component
        index = index + 1
   
    pcd_selected = o3d.geometry.PointCloud()
    pcd_selected.points = o3d.utility.Vector3dVector(membraneVArray)
    o3d.io.write_point_cloud(outputFileName, pcd_selected)

    #in order to access same data in different processes,
    #we need to lock the RLock before accessing it
    lock_of_data.acquire()
    activeProcessNum.value = activeProcessNum.value - 1
    #print(f"active will be: {activeProcessNum.value}")
    lock_of_data.release()
    
    lock_of_outstream.acquire()
    print(f"finished: {inputFileName}")
    lock_of_outstream.release()

####thread to handle listening
def process_manager():

    #multi-process
    mypath = "../fullData/"
    process_file_outputFolder = "../fullData_processed/"
    
    
    process_file_postfix = "_post.ply"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    # onlyfiles[0][::-1][0:4]
    # print(onlyfiles[1])
    # print(onlyfiles[1][::-1][4:][::-1])
    fileSize = len(onlyfiles)
    print(f"file size is {fileSize}")
    outputShowDataIdx = 0
    fileIdx = 0
    while True:
        lock_of_data.acquire()
        number = activeProcessNum.value
        lock_of_data.release()
        if number < maximumProcessNum:
            #if the number of process is smaller than maximum,]
            #assign new tasks here
            
            if fileIdx >= fileSize:
                break;
            
            
            inFile = mypath + onlyfiles[fileIdx]
                                                                  #crop number only
            outFile = process_file_outputFolder+ onlyfiles[fileIdx][::-1][4:][::-1] + process_file_postfix
            
            lock_of_data.acquire()
            activeProcessNum.value = activeProcessNum.value +1
            lock_of_data.release()
            
            processWorker = Process(target=_generateSinglePCD, args=(inFile, outFile,activeProcessNum))
            processWorker.start() 
            
            fileIdx = fileIdx+1
        
        else:
            time.sleep(0.5)
            outputShowDataIdx = outputShowDataIdx + 1
            if outputShowDataIdx%20 == 0:
                lock_of_outstream.acquire()
                print(f"[MAIN THREAD] Waiting for free process...\n[MAIN THREAD] Next file Index: {fileIdx}")
                lock_of_outstream.release()
            
    #print(len(onlyfiles))
    print(f"[MAIN THREAD] will exit")
    
    
            

if __name__ == "__main__":
    process_manager()
    
    