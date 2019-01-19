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

def hierarchique(tree, root, cluster_courant):
  return 0
  
  

def main(graph): 
  
  viewLabel = graph.getStringProperty("viewLabel")
  viewColor = graph.getColorProperty("viewColor")
  viewSize = graph.getIntegerProperty("size of nodes")
  green = tlp.Color(0,255,0)
  red = tlp.Color(255,0,0)
  size=100
  #TODO scene color

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
      

  
  root_cluster = graph.getSubGraph("Genes interactions")
  new = graph.addSubGraph("new")
  hierarchique(new, root_cluster, cluster)
  
    

  
  
