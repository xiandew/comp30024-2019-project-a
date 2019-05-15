# Chexers

## PROBLEM FORMULATION:
Part A of this project requires us to design a single-player agent program, which moves the chess pieces from their initial locations to their destinations, where they can exit the board. Our aim is to find the least number of moves to achieve this goal. In order to find a solution, we need to abstract and formulate the problem based on the following components:
- **State**: a state should contain the current locations of all the chess pieces.
- **Actions**: the available actions or the available moves for a chess piece are: 1) move to its surrounding cell; 2) jump over a block or another chess piece; 3) exit the board from a certain edge of the board.
- **Goal test**: all the chess pieces need to exit from the board and the state should be empty.
- **Path cost**: the number of actions taken for the chess pieces to reach their current state.
By formulating our problem in this way, we can represent each state as a node in a graph, and each action is the edge that connects the node. Then, it is a graph search problem. Since we are informed of the configuration of the board and the colour of our pieces and only A* algorithm can find a guaranteed optimal solution among the informed algorithms we learnt in class, we chose A* algorithm to tackle the problem.


## ALGORITHM ANLYSIS:
A* algorithm can be analysed from the following four perspectives:
- Completeness: since we are using a graph structure that avoids the repeated state, it should be complete.
- Time: for A* algorithm, the time complexity is exponential to the relative error in our heuristic function times the depth of the tree.
- Space: keep all the nodes in memory
- Optimal: our approach should be optimal since our heuristic function is admissible.

When we first start with the heuristic function, we chose the Euclidean distance to approach to this problem. However, since we are working on a board where each cell is in the shape of a hexagon, Euclidean distance can’t accurately model this situation. Therefore, we chose the sum of the Hex Manhattan distance from each piece to the closest exit cell to be our heuristic function. This hex distance works well for most of the test cases, but when the chess piece needs to detour in order to get around many blocks, the time taken to compute the result will exceed 30 seconds. The inaccuracy of the hex distance is mainly caused by the ignorance of the blocks. Therefore, when a large number of blocks that will block the way of the pieces, there will be a large error between the hex distance and the actual cost. The following board configuration gives one example where our pieces might fall into the trap of blocks:



```
#           .-'-._.-'-._.-'-._.-'-.
#          | red | red | red |BLOCK|
#        .-'-._.-'-._.-'-._.-'-._.-'-.
#       |     |     |     |     |BLOCK|
#     .-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
#    |     |     |     |     |BLOCK|BLOCK|
#  .-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
# | red |     |     |     |BLOCK|BLOCK|     |
# '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#    |     |     |     |BLOCK|BLOCK|     |
#    '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#       |     |     |BLOCK|BLOCK|     |
#       '-._.-'-._.-'-._.-'-._.-'-._.-'
#          |     |     |     |     |
#          '-._.-'-._.-'-._.-'-._.-'
```
In order to further improve our heuristic function, so that it considers the blocks, we decided to pre-generate the approximate path cost for each hex without a block to the exit cells. Each of the path cost is generated by running a Dijkstra algorithm from the exit cells (the internal implementation of the Dijkstra algorithm is actually a uniform cost search without a goal state). In generating the path cost for each cell, in order to guarantee the admissibility of this heuristic, we allow a jump action to be performed even without an occupied hex as a pivot. With all of these considerations, our heuristic will have a good estimate of the true cost.


## PROBLEM FEATURES ANLYSIS:
In general, by testing our program through some input, we found that an empty board is more likely to have a longer running time. We believe that the branching factor will be negatively proportional to the number of blocks, and positive proportional to the number of pieces onboard.

```
#
#           .-'-._.-'-._.-'-._.-'-.
#          | red |     |     |     |
#        .-'-._.-'-._.-'-._.-'-._.-'-.
#       |     |     |     |     |     |
#     .-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
#    |     |     |     |     |     |     |
#  .-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
# | red |     |     |     |     |     |     |
# '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#    |     |     |     |     |     |     |
#    '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#       |     |     |     |     |     |
#       '-._.-'-._.-'-._.-'-._.-'-._.-'
#          | red |     |     | red |
#          '-._.-'-._.-'-._.-'-._.-'
# number of expanded nodes: 15543


#
#           .-'-._.-'-._.-'-._.-'-.
#          |     |BLOCK|     |BLOCK|
#        .-'-._.-'-._.-'-._.-'-._.-'-.
#       |BLOCK|BLOCK|     |BLOCK|     |
#     .-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
#    |BLOCK|     |BLOCK|     |BLOCK|BLOCK|
#  .-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
# |BLOCK|     |BLOCK|     |BLOCK|BLOCK|     |
# '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#    |     |BLOCK|BLOCK|BLOCK|BLOCK|     |
#    '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#       |BLOCK|BLOCK| red |BLOCK|BLOCK|
#       '-._.-'-._.-'-._.-'-._.-'-._.-'
#          |     |     |     |BLOCK|
#          '-._.-'-._.-'-._.-'-._.-'
# number of expanded nodes: 12
```

Since the braching factor is mainly determined by the available actions at each state, the more blocks we have, or the fewer players we have, the fewer available actions can be performed. Therefore, an increase in the number of blocks or decrease in the number of players will reduce the branching factors for our search tree, which then reduced the search space and time.
