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




def draw_bundles(gene, tree):
  for e in gene.getEdges():
    source = gene.source(e)
    target = gene.target(e)
    path = compute_path(tree, source, target)
    print path 



#  viewLayout_hierarchical = hierarchical_graph.getLayoutProperty("viewLayout")
#  viewLayout_interraction = gene_interraction.getLayoutProperty("viewLayout")
#  viewShape_hierarchical = hierarchical_graph.getIntegerProperty("viewShape")
#  viewShape = graph.getIntegerProperty("viewShape")
#  for e in gene_interraction.getEdges():
#    path = compute_path(hierarchical_graph, gene_interraction.source(e), gene_interraction.target(e))    
#    print path
#
#    	
#    	viewShape[e] = tlp.EdgeShape.BezierCurve
#    
#    
#def control_points(viewLayout_hierarchical, viewLayout_interraction, path, e):
#  position_vector = []
#  for n in path :
#    position_vector.append(viewLayout_hierarchical[n])
#  viewLayout_interraction.setEdgeValue(e, position_vector)
#  print position_vector





def main(graph): 
  #TODO scene color = white

  viewLayout = graph.getLayoutProperty("viewLayout")
  viewColor = graph.getColorProperty("viewColor")

  preprocessing(graph, viewColor)
  
  root_cluster = graph.getSubGraph("Genes interactions")
  hierarchical_tree = graph.addSubGraph("hierarchical_graph") # init new graph 
  
  root = hierarchical_tree.addNode({"name":"root"}) # first node as root 
  draw_hierarchical_tree(hierarchical_tree, root, root_cluster)
  
  apply_radial_algorithm(hierarchical_tree,viewLayout)
  
  updateVisualization(centerViews = True)

  draw_bundles( root_cluster, hierarchical_tree)
  
#  A = root_cluster.getRandomNode()
#  B = root_cluster.getRandomNode()
#  print A
#  print B  
#  print compute_path(hierarchical_tree, root, B)
  
#  print hierarchical_tree.existEdge(path[0],path[2]) # retourne <edge 4294967295> si l'edge existe pas

#  bundles = graph.getSubGraph("Bundles")
#  4294967295
  
  
  
  
  
  
