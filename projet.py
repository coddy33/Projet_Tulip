# Powered by Python 2.7
# -*- coding: utf-8 -*-

"""


@author: BLAIS Benjamin
@author: JUNG Frédéric 

@organization: Universite de Bordeaux

  
@requires: tlp, time, python2


@date: 02/03/2019


@license: MIT License

Copyright (c) 2019 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from tulip import tlp
import time

start = time.time()


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
  
  @type tree: tlp.Graph
  @param tree: graph holding root
  @type current_cluster: tlp.Graph
  @param current_cluster : a Tulip graph of the hierarchical ########TODO Ben - decrire la recursivite 
  @type root: tlp.node
  @param root: root node of the current_cluster
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


def BFS_search(gr, u, v):
  """
  find the shortest path between two nodes (source and target) unsing
  the Breadth-First Search (BFS) algorithme.
  
  @type  gr: tlp.Graph
  @param gr: Tulip graph
  @type   u: tlp.node
  @param  u: First node of interest
  @type   v: tlp.node
  @param  v: Second node of interest
  """
  explored = []
  queue = []
  queue.append([u])
  while queue :
    path = queue.pop(0)
    node = path[-1]
    if node not in explored: 
      for n in gr.getInOutNodes(node):
        new_path = list(path)
        new_path.append(n)
        queue.append(new_path)
        if n == v:
          new_path.pop()
          del new_path[0]
          return new_path 
      explored.append(node)

def find_clusters(gr):
  """
  find nodes (that are not corresponding to a gene) in a hierarchical tree.
  
  @type  gr: tlp.Graph
  @param gr: hierarchical tree
  @rtype   : list
  @return  : list of nodes
  @todo    : use it with BFS_search()
  """
  viewLabel = gr.getStringProperty("viewLabel")
  clusters = []
  for n in gr.getNodes():
    if viewLabel[n] == "" :
      clusters.append(n)
  return clusters


def compute_path(L1, L2):   
  """
  Find the shortest path between two nodes using two lists. The lists are the path between the node of interest and the root node.
  The first common node between this two path is the closest node which links the source and the target. 
  
  This function allow to find the first common node between two lists and remove the others nodes.
  Then return the path between the source and the target.
  
  @type  L1: list
  @param L1: first path between the source node and root.
  @type  L2: list
  @param L2: second path between the target node and root.
  @return:   node list ordered as the shortest path.
  """ 
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
   
    
      
def set_control_points(tree, gene, path, e):
  position_vector = []
  for n in path :
    position_vector.append(tree[n])
  # position_vector sous cette forme : [(-2683.61,3082.42,0), (-1554.76,2237.48,0), (-1155.87,721.011,0)]  
  gene.setEdgeValue(e, position_vector)

def find_parents(gr, node, parents):
  """
  Find the shortest path between the node and its parent.
  
  @type       gr: tlp.Graph
  @param      gr: the current graph
  @type     node: tlp.node
  @param    node: the node of intereset
  @type  parents: list
  @param parents: empty list of node'parents
  @rtype        : list
  @return       : list of parents
  """
  if gr.getInNodes(node) > 0 :
    parents.append(node)
    for n in gr.getInNodes(node):
      find_parents(gr, n, parents)
  return parents


def find_path(gr, source, target):
  L1 = []
  L2 = []
  L1 = find_parents(gr, source, L1)
  L2 = find_parents(gr, target, L2)
  path = compute_path(L1,L2)
  path.pop()
  del path[0]
  return path


def draw_bundles(gene, tree):
  """
  @type  gene: tlp.Graph
  @param gene: Gene interactions graph
  @type  tree: tlp.Graph
  @param tree: hierarchical tree graph
  """
  viewLayout_interraction = gene.getLayoutProperty("viewLayout")
  viewLayout_hierarchical = tree.getLayoutProperty("viewLayout")
  viewShape = gene.getIntegerProperty("viewShape")
  for e in gene.getEdges():
    source = gene.source(e)
    target = gene.target(e)
    path = find_path(tree, source, target)
#    path = BFS_search(tree,source,target)
    set_control_points(viewLayout_hierarchical, viewLayout_interraction, path, e)
  viewShape.setAllEdgeValue(tlp.EdgeShape.CubicBSplineCurve)

def color_gradient(nb_gradient):
  """
  Compute and return the color gradient form red to green for
  a color mapping algorithme.
  
  @type  nb_gradient: int
  @param nb_gradient: the number of gradients 
  @rtype            : list
  @return           : the list of gradients colors
  """
  colors = []
  r = 255
  g = 0
  b = 0
  gradient = 255/(nb_gradient/2)
  for i in range(nb_gradient/2) :
    colors.append(tlp.Color(r,g,b))
    colors.append(tlp.Color(r,g,b))
    r = r - gradient
  r = 0
  colors.append(tlp.Color.Black)
  colors.append(tlp.Color.Black)
  for i in range (nb_gradient/2):
    colors.append(tlp.Color(r,g,b))
    colors.append(tlp.Color(r,g,b))
    g = g + gradient
  return colors
  
  
  
def color_graph(gr,param,color):
  """
  
  """
  params = tlp.getDefaultPluginParameters("Color Mapping",gr)
  colorScale = tlp.ColorScale([])
  params["input property"] = param
  colors = color_gradient(20)
  #  colors = [tlp.Color.Red, tlp.Color.Black, tlp.Color.Green] # can be use intead of previous line
  colorScale.setColorScale(colors)
  params["color scale"] = colorScale
  gr.applyColorAlgorithm("Color Mapping", color, params)



def timePoint_hierarchy(nb_TP):
  """
  Convert the number of time points in a list with all the time points. This list is used by 
  the others functions.
  
  The time points columns in the input dataset should be write like : "tp* s"
  * is the time point number (the first time point is 1).
  
  @type  nb_TP: integer
  @param nb_TP: the number of time points
  @rtype      : list
  @return     : all the Time points name.
  """
  TPs = []
  for i in range(nb_TP):
    TP_name = "tp" + str(i+1) + " s"
    TPs.append(TP_name)
  return TPs
  
  
def draw_timePoint_hierarchy(TPs, SM, gene):
  """
  Add a Small Multiples subgraph for each time points with the gene interractions properties.
  
  Time points data are set in the viewMetric columns and defined the graph colors.
  
  @type   TPs: list 
  @param  TPs: the Time points name 
  @type    SM: Tulip graph
  @param   SM: Small Multiples subgraph
  @type  gene: Tulip graph
  @param gene: Genes interactions subgraph
  """
  viewColor = graph.getColorProperty("viewColor")
  for tp in TPs :
    tmp = SM.addSubGraph(tp)
    tlp.copyToGraph(tmp, gene)
    Metric = tmp.getDoubleProperty("viewMetric")
    pr = tmp.getDoubleProperty(tp)
    for n in tmp.getNodes():
      properties = tmp.getNodePropertiesValues(n)
      Metric[n] = properties[tp]
    color_graph(tmp, pr, viewColor)
    
def draw_small_multiples(nb_col,TPs,SM,lay):
  """
  """
  bb_tp = tlp.computeBoundingBox(SM)
  x = 0
  y=0
  count = 0
  for gr in TPs :
    x = x + bb_tp.width() + 2000
    tp = SM.getSubGraph(gr)
    if count >= nb_col :
      x = bb_tp.width() + 2000
      y = y - bb_tp.height() - 2000
      count =0
    for n in tp.getNodes() :
      lay[n] = lay[n] + tlp.Vec3f( x,y,0)  
    for e in tp.getEdges():
      Ltmp = []
      for el in lay[e]:
        h = el + tlp.Vec3f(x ,y,0)  
        Ltmp.append(h)
      lay[e] = Ltmp
    count +=1


def draw_small_multiples_v2(nb_col,TPs,SM,lay):
  #TODO dire qu'on a gagné du temps par rapport à l'autre v1
  bb_tp = tlp.computeBoundingBox(SM)
  x = 0
  y=0
  count = 0
  for gr in TPs :
    x = x + bb_tp.width() + 2000
    tp = SM.getSubGraph(gr)
    #lay = tp.getLayoutProperty("viewlayout")
    if count >= nb_col :
      x = bb_tp.width() + 2000
      y = y - bb_tp.height() - 2000
      count =0
    count=count+1
    lay.translate(tlp.Vec3f(x,y,0),tp)
    
  

  

def main(graph):
  viewLayout = graph.getLayoutProperty("viewLayout")
  viewColor = graph.getColorProperty("viewColor")
  
  # Part I : Pre-processing
  preprocessing(graph, viewColor)
  
  #Part II : Drawing of interaction network
  root_cluster = graph.getSubGraph("Genes interactions")
  hierarchical_tree = graph.addSubGraph("hierarchical_graph") # init new graph 
  root = hierarchical_tree.addNode({"name":"root"}) # first node as root 
  
  draw_hierarchical_tree(hierarchical_tree, root, root_cluster)
  apply_radial_algorithm(hierarchical_tree,viewLayout)
  draw_bundles( root_cluster, hierarchical_tree)
  
  #Part III : Thumbnails construction
  TPs = timePoint_hierarchy(17)
  SM = graph.addSubGraph("Small multiples")
  lay = SM.getLayoutProperty("viewLayout")
  draw_timePoint_hierarchy(TPs, SM, root_cluster)
  #draw_small_multiples(5,TPs,SM,lay)
  draw_small_multiples_v2(5,TPs,SM,lay)



  #Time counter
  print "Time elapsed :", time.time() - start, " secondes"
    
#  Time elapsed :10.0036051273 secondes -> find_path()
#  Time elapsed :103.376773834 secondes -> compute_pathway()
  
  
