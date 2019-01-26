# Powered by Python 2.7
# -*- coding: utf-8 -*-

"""
BLAIS Benjamin
JUNG Frédéric 

Visual analysis of gene expression data

01/26/2016
"""

# To cancel the modifications performed by the script
# on the current graph, click on the undo button.

# Some useful keyboards shortcuts : 
#   * Ctrl + D : comment selected lines.
#   * Ctrl + Shift + D  : uncomment selected lines.
#   * Ctrl + I : indent selected lines.
#   * Ctrl + Shift + I  : unindent selected lines.
#   * Ctrl + Return  : run script.
#   * Ctrl + F  : find selected text.
#   * Ctrl + R  : replace selected text.
#   * Ctrl + Space  : show auto-completion dialog.

# -*- coding: utf-8 -*-
from tulip import tlp

# The updateVisualization(centerViews = True) function can be called
# during script execution to update the opened views

# The pauseScript() function can be called to pause the script execution.
# To resume the script execution, you will have to click on the "Run script " button.

# The runGraphScript(scriptFile, graph) function can be called to launch
# another edited script on a tlp.Graph object.
# The scriptFile parameter defines the script name to call (in the form [a-zA-Z0-9_]+.py)

# The main(graph) function must be defined 
# to run the script on the current graph


def preprocessing(gr, viewColor):
  viewLabel = gr.getStringProperty("viewLabel")
  LabelPosition = gr.getIntegerProperty("viewLabelPosition")
  viewSize = gr.getIntegerProperty("size of nodes")
  green = tlp.Color(0,255,0)
  red = tlp.Color(255,0,0)
  size=100
  for n in graph.getNodes():
    properties = gr.getNodePropertiesValues(n)
    locus_name = properties["locus"]
    viewLabel[n] = locus_name
    viewSize[n] = size
    LabelPosition[n] = tlp.LabelPosition.Center
  for e in gr.getEdges():
    properties = gr.getEdgePropertiesValues(e)
    if (properties["Positive"] == True ) :
      viewColor[e] = green
    else :
      viewColor[e] = red


def draw_hierarchical_tree(tree, root, current_cluster):
  """
  Draw the hierarchical tree. Each clusters are represented by a subgraphs. For each clusters add a node 
  in the tree then fit the edges between the cluster and its parent recursively.
  
  Then, for each current clusters that doesn't have childs draw each genes as nodes and fit it to its cluster.
  
  @param tree: graph holding root
  @param current_cluster : a Tulip graph of the hierarchical ########TODO Ben - decrire la recursivite 
  @param root: ro
  ot node of the current_cluster

  """
  for cluster in current_cluster.getSubGraphs():
    current_node = tree.addNode()
    tree.addEdge(root,current_node) 
    draw_hierarchical_tree(tree, current_node, cluster)
  if len(list(current_cluster.getSubGraphs())) == 0 :
    for n in current_cluster.getNodes():
      tree.addNode(n)
      tree.addEdge(root, n)
  
  

def apply_radial_algorithm(gr,viewLayout):
  """
  Apply the "Tree Radial" algorithme on gr
  
  @param gr: Tulip graph 
  @param viewLayout: layout property
  """
  params = tlp.getDefaultPluginParameters("Tree Radial", gr)
  params["layer spacing"] = 64
  params["node spacing"] = 18
  gr.applyLayoutAlgorithm("Tree Radial", viewLayout, params)


#Recuperer le chemin entre deux noeuds (sommets)
def compute_path(gr, u, v):
#   source : https://stackoverflow.com/questions/8922060/how-to-trace-the-path-in-a-breadth-first-search
  """
 This function allows to recover the path (nodes) which separate two nodes 

 @param gr : Tulip graph
 @ u : First node of interest
 @ v : Second node of interest
  """
  print "coucou"
  queue = []
  queue.append([u])
  while queue :
    path = queue.pop(0)
    node = path[-1]
    if node == v:
      return path
    for adjacent in gr.getInOutNodes(node):
      new_path = list(path)
      new_path.append(adjacent)
      queue.append(new_path)

def find_clusters(gr):
  viewLabel = gr.getStringProperty("viewLabel")
  clusters = []
  for n in gr.getNodes():
    if viewLabel[n] == "" :
      clusters.append(n)
  return clusters


def find_path(L1, L2):    
  doublons = []
  for i in range(len(L1)) : 
    for j in range(len(L2)):
      if L1[i] == L2[j]:
        doublons.append(L1[i])
        L2.pop(j)
        break
  del doublons[0]
  for j in range(len(doublons)):
    L1.remove(doublons[j])
      
  L2.reverse()
  return L1 + L2    
  
def find_path2(gr, node, position):
  #TODO enlever position en argument -> Fredo
  if gr.getInNodes(node) > 0 :
    position.append(node)
    for n in gr.getInNodes(node):
      find_path2(gr, n, position)
  



def compute_path2(tree, source, target):
  path = []
  clusters = find_clusters(tree)
  count =  0
  for n in tree.getInOutNodes(source):
    parent_source = n
  for n in tree.getInOutNodes(target):
    parent_target= n
  path.append(parent_source)
  find_path(tree, parent_source, parent_target, path, clusters)
  path.append(parent_target)
  return path
    
    
      
def set_control_points(tree, gene, path, e):
  position_vector = []
  for n in path :
    position_vector.append(tree[n])
  # position_vector sous cette forme : [(-2683.61,3082.42,0), (-1554.76,2237.48,0), (-1155.87,721.011,0)]  
  gene.setEdgeValue(e, position_vector)
  


def draw_bundles(gene, tree):
  viewLayout_interraction = gene.getLayoutProperty("viewLayout")
  viewLayout_hierarchical = tree.getLayoutProperty("viewLayout")
  viewShape = gene.getIntegerProperty("viewShape")
  for e in gene.getEdges():
    source = gene.source(e)
    target = gene.target(e)
    L1 = []
    find_path2(tree, source, L1)
    L2 = []
    find_path2(tree, target, L2)
    path = find_path(L1,L2)
    path.pop()
    del path[0]
    set_control_points(viewLayout_hierarchical, viewLayout_interraction, path, e)
  viewShape.setAllEdgeValue(tlp.EdgeShape.CubicBSplineCurve)


#colorier les sommets (couleur à regler)
def color_graph(gr,param,color):
  params = tlp.getDefaultPluginParameters("Color Mapping",gr)
  params["input property"] = param
  params["minimum value"]=0
  params["maximum value"]=15
  #params["color scale"]=
  gr.applyColorAlgorithm("Color Mapping", color, params)


def timePoint_hierarchy(nb_TP):
  TPs = []
  for i in range(nb_TP):
    TP_name = "tp" + str(i+1) + " s"
    TPs.append(TP_name)
  return TPs
  
  
def draw_timePoint_hierarchy(TPs, SM, gene):
  for tp in TPs :
    tmp = SM.addSubGraph(tp)
    tlp.copyToGraph(tmp, gene)

def main(graph): 
  viewLayout = graph.getLayoutProperty("viewLayout")
  viewColor = graph.getColorProperty("viewColor")
  param = graph.getDoubleProperty("tp1 s")


  preprocessing(graph, viewColor)
  
  root_cluster = graph.getSubGraph("Genes interactions")
  hierarchical_tree = graph.addSubGraph("hierarchical_graph") # init new graph 
  
  root = hierarchical_tree.addNode({"name":"root"}) # first node as root 
  draw_hierarchical_tree(hierarchical_tree, root, root_cluster)
  
  apply_radial_algorithm(hierarchical_tree,viewLayout)
  

  draw_bundles( root_cluster, hierarchical_tree)
  color_graph(root_cluster,param,viewColor)
  
  TPs = timePoint_hierarchy(17)
  SM = graph.addSubGraph("Small multiples")
  draw_timePoint_hierarchy(TPs, SM, root_cluster)


  updateVisualization(centerViews = True)

 
  
  
  
