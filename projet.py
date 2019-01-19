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


def preprocessing(graph):
  viewLabel = graph.getStringProperty("viewLabel")
  viewColor = graph.getColorProperty("viewColor")
  viewSize = graph.getIntegerProperty("size of nodes")
  green = tlp.Color(0,255,0)
  red = tlp.Color(255,0,0)
  size=100
  for n in graph.getNodes():
    properties = graph.getNodePropertiesValues(n)
    locus_name = properties["locus"]
    viewLabel[n] = locus_name
    viewSize[n] = size
    
  for e in graph.getEdges():
    properties = graph.getEdgePropertiesValues(e)
    if (properties["Positive"] == True ) :
      viewColor[e] = green
    else :
      viewColor[e] = red
      

  

def draw_hierarchical_tree(tree, root, current_cluster):
  current_node = tree.addNode()
  tree.addEdge(root,current_node) 
  for cluster in current_cluster.getSubGraphs():
    draw_hierarchical_tree(tree, current_node, cluster)
  if len(list(current_cluster.getSubGraphs())) == 0 :
    print "coucou"
    for n in current_cluster.getNodes():
      node = tree.addNode()
      tree.addEdge(root, node)
  

def main(graph): 
  
  #TODO scene color

  preprocessing(graph)
  
  root_cluster = graph.getSubGraph("Genes interactions")
  hierarchical_tree = graph.addSubGraph("hierarchical_graph")
  
  root = hierarchical_tree.addNode({"name":"root"})
  for cluster in root_cluster.getSubGraphs():
    draw_hierarchical_tree(hierarchical_tree, root, cluster)


  
  
