import os
import time

import networkx as nx
import matplotlib.pyplot as plt

from utils.dataset import Generator
from utils.visualizer import Visualizer 

from vertex_cover.vc_bnb import BranchAndBound
from vertex_cover.vc_dp import DynamicProgramming


def vertex_cover_dp(adj_list: dict, N: int) -> set:
    '''
    Run dynamic programming solution for vertex cover
    '''

    # convert adj_list to valid format
    temp = [[] for i in range(N + 1)]
    for i in range(1, N + 1):
        temp[i] = adj_list[i]
    adj_list = temp
    
    dp = DynamicProgramming()
    
    start = time.perf_counter()
    vc = dp.solve_n_ary_tree(adj_list, N)
    end = time.perf_counter()

    elapsed = (end - start) * 1000  # to ms

    return vc, elapsed


# def vertex_cover_bnb(adj_list: dict) -> set:
#     '''
#     Run branch and bound solution for vertex cover,
#     only calculating either 100, 300, or 900 tree nodes.
#     '''
#     G = nx.from_dict_of_lists(adj_list)

#     bnb = BranchAndBound()

#     start = time.perf_counter()
#     # vc = bnb.solve(tree)
#     end = time.perf_counter()

#     for element in vc:
#         if element[1]==0:
#             vc.remove(element)

#     elapsed = (end - start) * 1000  # to ms

#     return len(vc), elapsed
    

def main():

    # initialize size of tree
    N = {
        'small': 10 ** 4,
        'medium': 10 ** 5,
        'large': 10 ** 6
    }

    # leave parameter empty for default generator values (10^4, 10^5, 10^5)
    generator = Generator(N['small'], N['medium'], N['large'])
    
    dataset = generator.generate()


    for size in dataset:

        filename = f'{size}_output.txt'

        with open(os.path.join(os.getcwd(), 'output', filename), "w") as f:
        
            tree_root, adj_list = dataset[size]

            header = f'''
                [DP] Solving for size {size} ({N[size]})...
                '''

            print()

            dp_result, dp_time = vertex_cover_dp(adj_list, len(adj_list))

            print(f'''[DP] Total minimum vertex cover: {dp_result}''')
            print(f'''[DP] Elapsed time: {dp_time:.2f} ms.''')

            # print(f'''
            #     [BnB] Solving for size {size} ({N[size]})...
            #     ''')

            # bnb_result, bnb_time = vertex_cover_bnb(adj_list)

            # print(f'''[BnB] Total minimum vertex cover: {bnb_result}''')
            # print(f'''[BnB] Elapsed time: {bnb_time:.2f} ms.''')
        

            '''Uncomment to visualize tree'''
            # print("Adjacency List:")
            # print(adj_list)

            # viz = Visualizer()
            # pos = viz.hierarchy_pos(G, 1)
            # nx.draw(G, pos, with_labels=True)
            # plt.show()
        


if __name__ == '__main__':

    main()




