from queue import PriorityQueue
from time import time
from search_problem import SearchProblem

# frontier: [(eval, (state, path_cost, parent_state))]
# expand_result: (to_state, edge_cost) 

class BestFirstSearch:

    def __init__(self, search_problem: SearchProblem):
        self.search_problem = search_problem
        self.search_history = {}
        self.frontier = PriorityQueue()
        self.max_frontier_size = 0
        self.reached_goal_state = None
        self.nodes_visited = 0
        self.time_taken = None
        self.search_complete = False

    def reset(self, randomize_input=False):
        if randomize_input:
            self.search_problem.initial_state = self.search_problem.get_random_state()
        self.search_history = {}
        self.frontier = PriorityQueue()
        self.max_frontier_size = 0
        self.reached_goal_state = None
        self.nodes_visited = 0
        self.time_taken = None
        self.search_complete = False

    def randomize_initial_state(self):
        raise Exception("Not Implemented")

    def evaluate(self, current_state, to_state, edge_cost):
        raise Exception("Not Implemented")

    def perform_search(self):
        start = time()
        if(self.search_problem.initial_state is None):
            raise Exception("Initial state not set")
        
        self.frontier.put((0, (self.search_problem.initial_state, 0, None)))
        while not self.frontier.empty():
            self.max_frontier_size = max(self.max_frontier_size, self.frontier.qsize())
            _, (current_state, path_cost, parent_state) = self.frontier.get()
            if(current_state in self.search_history):
                old_path_cost, _ = self.search_history[current_state]
                if(old_path_cost <= path_cost):
                    continue 
            
            self.search_history[current_state] = (path_cost, parent_state)
            if(self.search_problem.is_goal(current_state)):
                self.reached_goal_state = current_state
                break
            
            expand_result = self.search_problem.expand(current_state)
            for (to_state, edge_cost) in expand_result:
                self.nodes_visited += 1
                if(to_state in self.search_history):
                    old_path_cost, _ = self.search_history[to_state]
                    if(old_path_cost <= path_cost + edge_cost):
                        continue
                eval = self.evaluate(current_state, to_state, edge_cost)
                self.frontier.put((eval, (to_state, path_cost + edge_cost, current_state)))
        
        self.search_complete = True
        end = time()
        self.time_taken = end - start

    def get_solution(self):
        if not self.search_complete:
            raise Exception("Goal not yet found")
        
        if(self.reached_goal_state is None):
            return (-1,[])

        solution_path = [self.reached_goal_state]
        while True:
            _, parent_state = self.search_history[solution_path[0]]
            if(parent_state is None):
                break
            else:
                solution_path.insert(0, parent_state)
        
        path_cost, _ = self.search_history[self.reached_goal_state]

        return (path_cost, solution_path)

    def display_solution(self):
        path_cost, solution_path = self.get_solution()
        if(len(solution_path) == 0):
            print("Solution does not exist")
            return
        print("cost = " + str(path_cost))
        for state in solution_path:
            self.search_problem.display_state(state)
    
    def display_stats(self):
        path_cost, solution_path = self.get_solution()
        print("memory usage:")
        print("     max frontier size: " + str(self.max_frontier_size))
        print("     max state history size: " + str(len(self.search_history)))
        print("time:")
        print("     time taken: " + str(round(self.time_taken, 2)) + " seconds")
        print("     no. of nodes visited: " + str(self.nodes_visited))
        print("")
        print("solution cost: " + str(path_cost))
        print("solution depth: " + str(len(solution_path) - 1))
        print("no. of states visited: " + str(len(self.search_history)))
        if(self.reached_goal_state is None):
            print("goal found: None")
        else:
            print("goal found:\n")
            self.search_problem.display_state(self.reached_goal_state)
