import random

import networkx as nx
import matplotlib.pyplot as plt


class Visualizer:

    '''
    Functions to visualize generated tree
    '''

    def __init__(self):
        pass

    def hierarchy_pos(self, G, root=None, width=1., vert_gap = 0.2, vert_loc = 0, leaf_vs_root_factor = 0.5):
        '''
        Taken from: https://epidemicsonnetworks.readthedocs.io/en/latest/_modules/EoN/auxiliary.html#hierarchy_pos
        If the graph is a tree this will return the positions to plot this in a 
        hierarchical layout.
        
        Based on Joel's answer at https://stackoverflow.com/a/29597209/2966723,
        but with some modifications.  

        We include this because it may be useful for plotting transmission trees,
        and there is currently no networkx equivalent (though it may be coming soon).
        
        There are two basic approaches we think of to allocate the horizontal 
        location of a node.  
        
        - Top down: we allocate horizontal space to a node.  Then its ``k`` 
        descendants split up that horizontal space equally.  This tends to result
        in overlapping nodes when some have many descendants.
        - Bottom up: we allocate horizontal space to each leaf node.  A node at a 
        higher level gets the entire space allocated to its descendant leaves.
        Based on this, leaf nodes at higher levels get the same space as leaf
        nodes very deep in the tree.  
        
        We use use both of these approaches simultaneously with ``leaf_vs_root_factor`` 
        determining how much of the horizontal space is based on the bottom up 
        or top down approaches.  ``0`` gives pure bottom up, while 1 gives pure top
        down.   
        
        
        :Arguments: 
        
        **G** the graph (must be a tree)

        **root** the root node of the tree 
        - if the tree is directed and this is not given, the root will be found and used
        - if the tree is directed and this is given, then the positions will be 
        just for the descendants of this node.
        - if the tree is undirected and not given, then a random choice will be used.

        **width** horizontal space allocated for this branch - avoids overlap with other branches

        **vert_gap** gap between levels of hierarchy

        **vert_loc** vertical location of root
        
        **leaf_vs_root_factor**

        xcenter: horizontal location of root
        '''
        if not nx.is_tree(G):
            raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

        if root is None:
            if isinstance(G, nx.DiGraph):
                root = next(iter(nx.topological_sort(G)))  #allows back compatibility with nx version 1.11
            else:
                root = random.choice(list(G.nodes))

        def _hierarchy_pos(G, root, leftmost, width, leafdx = 0.2, vert_gap = 0.2, vert_loc = 0, 
                        xcenter = 0.5, rootpos = None, 
                        leafpos = None, parent = None):
            '''
            see hierarchy_pos docstring for most arguments

            pos: a dict saying where all nodes go if they have been assigned
            parent: parent of this branch. - only affects it if non-directed

            '''

            if rootpos is None:
                rootpos = {root:(xcenter,vert_loc)}
            else:
                rootpos[root] = (xcenter, vert_loc)
            if leafpos is None:
                leafpos = {}
            children = list(G.neighbors(root))
            leaf_count = 0
            if not isinstance(G, nx.DiGraph) and parent is not None:
                children.remove(parent)  
            if len(children)!=0:
                rootdx = width/len(children)
                nextx = xcenter - width/2 - rootdx/2
                for child in children:
                    nextx += rootdx
                    rootpos, leafpos, newleaves = _hierarchy_pos(G,child, leftmost+leaf_count*leafdx, 
                                        width=rootdx, leafdx=leafdx,
                                        vert_gap = vert_gap, vert_loc = vert_loc-vert_gap, 
                                        xcenter=nextx, rootpos=rootpos, leafpos=leafpos, parent = root)
                    leaf_count += newleaves

                leftmostchild = min((x for x,y in [leafpos[child] for child in children]))
                rightmostchild = max((x for x,y in [leafpos[child] for child in children]))
                leafpos[root] = ((leftmostchild+rightmostchild)/2, vert_loc)
            else:
                leaf_count = 1
                leafpos[root]  = (leftmost, vert_loc)

            return rootpos, leafpos, leaf_count

        xcenter = width/2.
        if isinstance(G, nx.DiGraph):
            leafcount = len([node for node in nx.descendants(G, root) if G.out_degree(node)==0])
        elif isinstance(G, nx.Graph):
            leafcount = len([node for node in nx.node_connected_component(G, root) if G.degree(node)==1 and node != root])
        rootpos, leafpos, leaf_count = _hierarchy_pos(G, root, 0, width, 
                                                        leafdx=width*1./leafcount, 
                                                        vert_gap=vert_gap, 
                                                        vert_loc = vert_loc, 
                                                        xcenter = xcenter)
        pos = {}
        for node in rootpos:
            pos[node] = (leaf_vs_root_factor*leafpos[node][0] + (1-leaf_vs_root_factor)*rootpos[node][0], leafpos[node][1]) 

        xmax = max(x for x,y in pos.values())
        for node in pos:
            pos[node]= (pos[node][0]*width/xmax, pos[node][1])
        return pos


    def large_hierarchy_pos(self, G, root, levels=None, width=1., height=1.):
        '''
        Taken from: https://stackoverflow.com/a/42723250
        For a more even spacing on levels.
        If there is a cycle that is reachable from root, then this will see infinite recursion.
        G: the graph
        root: the root node
        levels: a dictionary
                key: level number (starting from 0)
                value: number of nodes in this level
        width: horizontal space allocated for drawing
        height: vertical space allocated for drawing
        '''

        TOTAL = "total"
        CURRENT = "current"
        def make_levels(levels, node=root, currentLevel=0, parent=None):
            """Compute the number of nodes for each level
            """
            if not currentLevel in levels:
                levels[currentLevel] = {TOTAL : 0, CURRENT : 0}
            levels[currentLevel][TOTAL] += 1
            neighbors = G.neighbors(node)
            for neighbor in neighbors:
                if not neighbor == parent:
                    levels =  make_levels(levels, neighbor, currentLevel + 1, node)
            return levels

        def make_pos(pos, node=root, currentLevel=0, parent=None, vert_loc=0):
            dx = 1/levels[currentLevel][TOTAL]
            left = dx/2
            pos[node] = ((left + dx*levels[currentLevel][CURRENT])*width, vert_loc)
            levels[currentLevel][CURRENT] += 1
            neighbors = G.neighbors(node)
            for neighbor in neighbors:
                if not neighbor == parent:
                    pos = make_pos(pos, neighbor, currentLevel + 1, node, vert_loc-vert_gap)
            return pos
        if levels is None:
            levels = make_levels({})
        else:
            levels = {l:{TOTAL: levels[l], CURRENT:0} for l in levels}
        vert_gap = height / (max([l for l in levels])+1)
        return make_pos({})