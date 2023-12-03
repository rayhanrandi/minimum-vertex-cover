"""
The algorithm is summarized as follows:

Every vertex is considered as having one of two states: 1 or 0
State 1---> Vertex is a part of Vertex Cover (VC) 
State 0---> Vertex is not a part of Vertex Cover (VC) whihc means all its neighbors HAVE to be in VC

Frontier Set: contains the set of candiadate vertices for a subproblem. Each entry is a tuple list comprising of (vertex ID, state, parent in searching tree) 

CurG: subproblem of current graph after removing explored nodes 
CurVC: Current VC found in particular instance of search
OptVC: Best (i.e. minimum) value of |CurVC| at any given point from start

Bounds to Solutions:
Upper Bound: Initially set to number of nodes and updated to size of current solution (i.e. size of minimum vertex cover found in search)

Lower bound: |Current VC| + LB(CurG)
LB(CurG)=sum of edges in CurG / maximum node degree in CurG

Stages of Implementation:
1) Choose candidate node (vi)
	Each search is started from the node with highest degree in CurG, as it represents the most promising node to be included in the VC. This node is stored in the last index of Frontier set, and accessed using Frontier.pop().

	Appened (vi,1) and (vi,0) to CurVC as a tuple= (vertex,state)


2)  If State==1: Remove from CurG 
	This removes the node and its edges from CurG
	
	If state==0, Add all neighbors of vi to CurVC and remove vi from CurG

3) Consider CurG
	If No more edges in CurG-->Candidate solution is found (CurVC accounts for all edges). 
		Check to see if |CurVC| lesser than |OptVC| (and update OptVC if true, otherwise backtrack to find new path) 
	Else Update Lower bound and prune as necessary.
		If Lowerbound<Upperbound, solution is possible
			Append next highest degree node in CurG to Frontier set 
		Else, there is no better solution in this search sapce, so can be pruned from CurG. Backtrack to find new path.

4) Backtracking
	After reaching the end of a path, we need to backtrack to consider a new path. To do this, we have to undo the changes made to CurG and CurVC, which is where the parent item of each tuple in Frontier is handy.
	
	If the parent node is in the VC, then 
		we remove the last few elements from CurVC that were added after teh parent node was discovered and add the corresponing nodes+edges back to CurG. This basically 'undoes the mistakes' to CurG...
	Else then the parent must be (-1,-1) i.e. start of the graph or root node
		Reset CurG to G and CurVC to empty 

When Frontier Set==empty, the whole graph and all possible solutions have been examined.G

End
"""

import time
import operator


class BranchAndBound:
	
    # BRANCH AND BOUND FUNCTION to find minimum VC of a graph
    def solve(self, G):

        # INITIALIZE SOLUTION VC SETS AND FRONTIER SET TO EMPTY SET
        OptVC = []
        CurVC = []
        Frontier = []
        neighbor = []

        # ESTABLISH INITIAL UPPER BOUND
        UpperBound = G.number_of_nodes()
        print('Initial UpperBound:', UpperBound)

        CurG = G.copy()  # make a copy of G
        # sort dictionary of degree of nodes to find node with highest degree
        v = self.find_maxdeg(CurG)
        #v=(1,0)

        # APPEND (V,1,(parent,state)) and (V,0,(parent,state)) TO FRONTIER
        Frontier.append((v[0], 0, (-1, -1)))  # tuples of node,state,(parent vertex,parent vertex state)
        Frontier.append((v[0], 1, (-1, -1)))
        # print(Frontier)

        while Frontier!=[]:
            (vi,state,parent)=Frontier.pop() #set current node to last element in Frontier
            
            #print('New Iteration(vi,state,parent):', vi, state, parent)
            backtrack = False

            #print(parent[0])
            # print('Neigh',vi,neighbor)
            # print('Remaining no of edges',CurG.number_of_edges())

            
            if state == 0:  # if vi is not selected, state of all neighbors=1
                neighbor = CurG.neighbors(vi)  # store all neighbors of vi
                for node in list(neighbor):
                    CurVC.append((node, 1))
                    CurG.remove_node(node)  # node is in VC, remove neighbors from CurG
            elif state == 1:  # if vi is selected, state of all neighbors=0
                # print('curg',CurG.nodes())
                CurG.remove_node(vi)  # vi is in VC,remove node from G
                #print('new curG',CurG.edges())
            else:
                pass

            CurVC.append((vi, state))
            CurVC_size = self.vc_size(CurVC)
            #print('CurVC Size', CurVC_size)
            # print(CurG.number_of_edges())
            # print(CurG.edges())

            # print('no of edges',CurG.number_of_edges())
            if CurG.number_of_edges() == 0:  # end of exploring, solution found
                #print('In FIRST IF STATEMENT')
                if CurVC_size < UpperBound:
                    OptVC = CurVC.copy()
                    #print('OPTIMUM:', OptVC)
                    print('Current Opt VC size', CurVC_size)
                    UpperBound = CurVC_size
                    #print('New VC:',OptVC)
                backtrack = True
                #print('First backtrack-vertex-',vi)
                    
            else:   #partial solution
                #maxnode, maxdegree = find_maxdeg(CurG)
                CurLB = self.lowerbound(CurG) + CurVC_size
                #print(CurLB)
                #CurLB=297

                if CurLB < UpperBound:  # worth exploring
                    # print('upper',UpperBound)
                    vj = self.find_maxdeg(CurG)
                    Frontier.append((vj[0], 0, (vi, state)))#(vi,state) is parent of vj
                    Frontier.append((vj[0], 1, (vi, state)))
                    # print('Frontier',Frontier)
                else:
                    # end of path, will result in worse solution,backtrack to parent
                    backtrack=True
                    #print('Second backtrack-vertex-',vi)


            if backtrack==True:
                #print('Hello. CurNode:',vi,state)
                if Frontier != []:	#otherwise no more candidates to process
                    nextnode_parent = Frontier[-1][2]	#parent of last element in Frontier (tuple of (vertex,state))
                    #print(nextnode_parent)

                    # backtrack to the level of nextnode_parent
                    if nextnode_parent in CurVC:
                        
                        id = CurVC.index(nextnode_parent) + 1
                        while id < len(CurVC):	#undo changes from end of CurVC back up to parent node
                            mynode, mystate = CurVC.pop()	#undo the addition to CurVC
                            CurG.add_node(mynode)	#undo the deletion from CurG
                            
                            # find all the edges connected to vi in Graph G
                            # or the edges that connected to the nodes that not in current VC set.
                            
                            curVC_nodes = list(map(lambda t:t[0], CurVC))
                            for nd in G.neighbors(mynode):
                                if (nd in CurG.nodes()) and (nd not in curVC_nodes):
                                    CurG.add_edge(nd, mynode)	#this adds edges of vi back to CurG that were possibly deleted

                    elif nextnode_parent == (-1, -1):
                        # backtrack to the root node
                        CurVC.clear()
                        CurG = G.copy()
                    else:
                        print('error in backtracking step')

        return OptVC
    
    #TO FIND THE VERTEX WITH MAXIMUM DEGREE IN REMAINING GRAPH
    def find_maxdeg(self, g):
        deglist = g.degree()
        deglist_sorted = sorted(deglist, reverse=True, key=operator.itemgetter(1))  # sort in descending order of node degree
        v = deglist_sorted[0]  # tuple - (node,degree)
        return v

    #EXTIMATE LOWERBOUND
    def lowerbound(self, graph):
        lb = graph.number_of_edges() / self.find_maxdeg(graph)[1]
        lb = self.ceil(lb)
        return lb


    def ceil(self, d):
        """
        return the minimum integer that is bigger than d
        """ 
        if d > int(d):
            return int(d) + 1
        else:
            return int(d)
        

    #CALCULATE SIZE OF VERTEX COVER (NUMBER OF NODES WITH STATE=1)
    def vc_size(self, VC):
        # VC is a tuple list, where each tuple = (node_ID, state, (node_ID, state)) vc_size is the number of nodes which has state == 1
        vc_size = 0
        for element in VC:
            vc_size = vc_size + element[1]
        return vc_size