import os

import psutil


class DynamicProgramming:
    '''
    Dynamic programming class with solver to find minimum vertex cover of tree graph
    '''

    def solve(self, adj: list[list[int]], N: int) -> tuple[int, int]:
        mem_start = self.process_memory()

        dp = [[0 for j in range(2)] for i in range(N+1)]
        for i in range(1, N+1):
            # 0 denotes not included in vertex cover
            dp[i][0] = 0
    
            # 1 denotes included in vertex cover
            dp[i][1] = 1
    
        self.dfs(adj, dp, 1, -1)

        mem_end = self.process_memory()
        mem_usage = mem_end - mem_start

        # return minimum size vertex cover
        return min(dp[1][0], dp[1][1]), mem_usage
    
    def dfs(self, adj: list[list[int]], dp: list[list[int]], src: int, par: int) -> None:
        for child in adj[src]:
            if child != par:
                self.dfs(adj, dp, child, src)
    
        for child in adj[src]:
            if child != par:
                # not including source in the vertex cover
                dp[src][0] = dp[child][1] + dp[src][0]
    
                # including source in the vertex cover
                dp[src][1] = dp[src][1] + min(dp[child][1], dp[child][0])
    
    def process_memory(self) -> int:
        '''
        evaluates memory usage in MB
        '''

        process = psutil.Process(os.getpid())
        mem_info = process.memory_info()
        return mem_info.rss / (1024 ** 2)   # bytes to MB