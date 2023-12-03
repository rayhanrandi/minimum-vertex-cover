import os
import random


class TreeNode:
    '''
    Representation of node in tree
    '''
    def __init__(self, value):
        self.value = value
        self.parent = None
        self.children = []


class Generator:

    '''
    Functions to generate tree where each node 
    have a random amount of children
    '''

    def __init__(self, small=10 ** 4, medium=10 ** 5, large=10 ** 6):
        self.SMALL = small
        self.MEDIUM = medium
        self.LARGE = large

    def adjacency_list(self, node: TreeNode) -> dict:
        '''
        Creates adjacency list for a given tree root
        '''
        if node is None:
            return {}

        adj_list = {node.value: [node.parent.value if node.parent else None] + [child.value for child in node.children]}

        for child in node.children:
            adj_list.update(self.adjacency_list(child))

        return adj_list
    
    def export_adjacency_list(self, adj_list: dict, filename: str) -> None:
        '''
        exports adjacency list to txtfile
        '''
        n = len(adj_list)

        with open(os.path.join(os.getcwd(), 'analysis_datasets', filename), "w") as f:
            for i in range(1, n+1):
                f.write(' '.join(map(str, adj_list[i])))
                f.write('\n')

    def generate_random_tree(self, n: int, export_filename: str) -> set:
        if n == 0:
            return None

        root = TreeNode(1)
        nodes = [root]

        for i in range(2, n + 1):
            parent = random.choice(nodes)
            child = TreeNode(i)
            child.parent = parent
            parent.children.append(child)
            nodes.append(child)

        # generate adjacency list from generated tree's root
        adj_list = self.adjacency_list(root)

        # remove root node's parent
        adj_list[1].remove(None)

        # export generated adjacency list to txtfile
        self.export_adjacency_list(adj_list, export_filename)


        return root, adj_list
    
    
    def generate(self) -> dict:
        return {
            'small': self.generate_random_tree(self.SMALL, 'small.txt'),
            'medium': self.generate_random_tree(self.MEDIUM, 'medium.txt'),
            'large': self.generate_random_tree(self.LARGE, 'large.txt'),
        }