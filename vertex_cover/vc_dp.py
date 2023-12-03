class DynamicProgramming:

    def solve(self, adj, N):
        dp = [[0 for j in range(2)] for i in range(N+1)]
        for i in range(1, N+1):
            # 0 denotes not included in vertex cover
            dp[i][0] = 0
    
            # 1 denotes included in vertex cover
            dp[i][1] = 1
    
        self.dfs(adj, dp, 1, -1)

        # return minimum size vertex cover
        return min(dp[1][0], dp[1][1])
    
    def dfs(self, adj, dp, src, par):
        for child in adj[src]:
            if child != par:
                self.dfs(adj, dp, child, src)
    
        for child in adj[src]:
            if child != par:
                # not including source in the vertex cover
                dp[src][0] = dp[child][1] + dp[src][0]
    
                # including source in the vertex cover
                dp[src][1] = dp[src][1] + min(dp[child][1], dp[child][0])