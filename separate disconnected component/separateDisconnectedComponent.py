'''
This is used to separate several disconnected components from one mesh file

Required lib: 
@numpy, open3d, trimesh, itertools, networkx
'''

import numpy as np
import open3d as o3d
import trimesh as tm
import itertools
import networkx as nx


if __name__ == "__main__":

    '''
    Input: fileName
           outputName
    '''
    filename = "1500.obj"
    outputName = "1500.ply"
    
    #####################################################################
    #bunnyMesh = o3d.io.read_triangle_mesh(filename)
    mesh = tm.load_mesh(filename)
    #bunnyMesh = _readTriMesh(filename)
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
    
    #for component in components:
    VertexNumberArray = np.zeros([len(components)],dtype = int)
    
    index = 0
    for component in components:
        VertexNumberArray[index] = len(component)
        index = index + 1
    #print(VertexNumberArray)
    maxValue = np.amax(VertexNumberArray)
    #print(maxValue)
    
    maxIdx = VertexNumberArray.argmax(axis=0)
    #print(maxIdx)
    
    index = 0
    membraneVertexIndexArray = []
    membraneVArray = np.zeros([maxValue,3],dtype=float)
    for component in components:
        #print(component)
        #part = np.asarray(component)
        #component
        #print(component)
        # if index == maxIdx:
            # vIdx = 0
            # for j in component:
            
                # colors[j,0] = rgb[index,0]
                # colors[j,1] = rgb[index,1]
                # colors[j,2] = rgb[index,2]
                
                # membraneVArray[vIdx, 0] = vArray[j,0]
                # membraneVArray[vIdx, 1] = vArray[j,1]
                # membraneVArray[vIdx, 2] = vArray[j,2]
                
                # vIdx = vIdx + 1
            # membraneVertexIndexArray = component
            
        vIdx = 0
        for j in component:
        
            colors[j,0] = rgb[index,0]
            colors[j,1] = rgb[index,1]
            colors[j,2] = rgb[index,2]
            
            membraneVArray[vIdx, 0] = vArray[j,0]
            membraneVArray[vIdx, 1] = vArray[j,1]
            membraneVArray[vIdx, 2] = vArray[j,2]
            
            vIdx = vIdx + 1
        #membraneVertexIndexArray = component    

                
        #print(len(component))
        index = index + 1
    
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(vArray)
    pcd.paint_uniform_color([0.81,0.81,0.81])
    pcd.colors = o3d.utility.Vector3dVector(colors)
    
    pcd_selected = o3d.geometry.PointCloud()
    pcd_selected.points = o3d.utility.Vector3dVector(membraneVArray)
     
    #####################################################################
    #o3d.io.write_point_cloud(outputName, pcd_selected)
    o3d.visualization.draw_geometries([pcd])    
    #print("shape:\n",np.asarray(components).shape)
    
    
    