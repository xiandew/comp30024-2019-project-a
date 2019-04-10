from .priorityQueue import PriorityQueue
from .node import Node
import functools

# ______________________________________________________________________________
# Uninformed Search algorithms
def best_first_graph_search(problem, f):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""

    """
    Conditions when appending nodes to the priority queue have been modified.
    Duplicate states are allowed in the heap to avoid deleting from heap.
    Referenced from <https://www.redblobgames.com/pathfinding/a-star/
    implementation.html#python-astar>
    """
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = {}

    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        explored[node.state] = node
        for child in node.expand(problem):
            if ( child.state not in explored or
                    child.path_cost < explored[child.state].path_cost ):
                frontier.append(child)
                explored[child.state] = child
    return None

def uniform_cost_search(problem):
    """[Figure 3.14]"""
    return best_first_graph_search(problem, lambda node: node.path_cost)

# ______________________________________________________________________________
# Informed (Heuristic) Search
def astar_search(problem, h=None):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))

# ______________________________________________________________________________

def memoize(fn, slot=None, maxsize=32):
    """Memoize fn: make it remember the computed value for any argument list.
    If slot is specified, store result in that slot of first argument.
    If slot is false, use lru_cache for caching the values."""
    if slot:
        def memoized_fn(obj, *args):
            if hasattr(obj, slot):
                return getattr(obj, slot)
            else:
                val = fn(obj, *args)
                setattr(obj, slot, val)
                return val
    else:
        @functools.lru_cache(maxsize=maxsize)
        def memoized_fn(*args):
            return fn(*args)

    return memoized_fn
