# Powered by Python 2.7

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

#2.1 et 2.2 
def draw_hierarchical_tree(tree, root, current_cluster):
  test=0
  for cluster in current_cluster.getSubGraphs():
    current_node = tree.addNode()
    tree.addEdge(root,current_node) 
    draw_hierarchical_tree(tree, current_node, cluster)
  if len(list(current_cluster.getSubGraphs())) == 0 :
    for n in current_cluster.getNodes():
      tree.addNode(n)#Modifie
      tree.addEdge(root,n)#Modifie
def apply_radial_algorithm(gr, root_cluster,viewLayout):
  params = tlp.getDefaultPluginParameters("Tree Radial", gr)
  params["layer spacing"] = 64
  params["node spacing"] = 18
  gr.applyLayoutAlgorithm("Tree Radial", viewLayout, params)
#  root_cluster.applyLayoutAlgorithm("Tree Radial", viewLayout, params)


def compute_path(gr, u, v):
#   source : https://stackoverflow.com/questions/8922060/how-to-trace-the-path-in-a-breadth-first-search
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

def draw_bundles(gr):
  viewShape = graph.getIntegerProperty("viewShape")
  for e in gr.getEdges():
    viewShape[e] = tlp.EdgeShape.BezierCurve

#colorier les sommets (couleur à regler)
def color_graph(gr,param,color):
  params = tlp.getDefaultPluginParameters("Color Mapping",gr)
  params["input property"] = param
  print params #Voir a quoi ressemble la liste des couleurs
  params["minimum value"]=0
  params["maximum value"]=15
  #params["color scale"]=
  gr.applyColorAlgorithm("Color Mapping", color, params)
  return # stub	
#Couleur maison
#def color_graph(gr,param,color):
#  green = tlp.Color(0,255,0)
#  red = tlp.Color(255,0,0)
#  for n in graph.getNodes():
#    if param[n] <= 7:
#      color[n]=green
#    else:
#      color[n]=red
#  for n in graph.getEdges():
#    if param[n]<=1:
#      color[n]=green
#    else:
#      color[n]=red

def main(graph): 
  #TODO scene color = white
  tlp.LabelPosition.Center

  viewLayout = graph.getLayoutProperty("viewLayout")
  viewColor = graph.getColorProperty("viewColor")
  param = graph.getDoubleProperty("tp1 s")
  preprocessing(graph, viewColor)
  
  root_cluster = graph.getSubGraph("Genes interactions")
  hierarchical_tree = graph.addSubGraph("hierarchical_graph")
  
  root = hierarchical_tree.addNode()
  draw_hierarchical_tree(hierarchical_tree,root,root_cluster)
  apply_radial_algorithm(hierarchical_tree, root_cluster,viewLayout)
  
  color_graph(graph,param,viewColor)
  #color_graph(hierarchical_tree,param,viewColor)
  A = hierarchical_tree.getRandomNode()
  path = compute_path(hierarchical_tree, root, A )
  print path
  #new = graph.addSubGraph("new")
 
  
  updateVisualization(centerViews = True)
  
  
#  print hierarchical_tree.existEdge(path[0],path[2]) # retourne <edge 4294967295> si l'edge existe pas

#  bundles = graph.getSubGraph("Bundles")
#  4294967295
  
  
