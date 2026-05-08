import tkinter as tk
from tkinter import messagebox
import time
from collections import deque
import heapq

BG_COLOR = "#1E1E2E"       
CANVAS_BG = "#313244"      
PATH_COLOR = "#CDD6F4"     
START_COLOR = "#A6E3A1"    
END_COLOR = "#F38BA8"      
VISITED_COLOR = "#89B4FA"  
ROUTE_COLOR = "#F9E2AF"    
BTN_BG = "#45475A"         
BTN_FG = "#CDD6F4"         
ACCENT = "#CBA6F7"

MAZES = [
    ["S00001000000000", "111011101111101", "000000000000101", "011111111110101", "000000100000101", "011110101111101", "010000101000001", "010111101011101", "010100001010001", "010101111011101", "010100000000101", "010111111110101", "000000000010001", "111111111011101", "00000000000000E"],
    ["S00000000000000", "011111111111110", "010000000000010", "010111111111010", "010100000001010", "010101111101010", "010101000101010", "0101010E0101010", "010101011101010", "010101000001010", "010101111111010", "010100000000010", "010111111111110", "010000000000000", "011111111111111"],
    ["S00010001000100", "011010101010101", "000000000000001", "101110111011101", "000100010001001", "010101010101011", "010001000100001", "011101110111011", "000100010001000", "110101010101010", "000100010001000", "011101110111011", "010000000000001", "010111111111101", "00000000000000E"],
    ["S01000001010000", "001011100010110", "100010001110100", "011010100000101", "000010111110101", "111010000010001", "000011110111101", "011000010000101", "001110111110101", "100010100010000", "011010101011110", "001000101000010", "011110101111010", "000010000001000", "11101111111110E"],
    ["S00000000000000", "010111111111111", "010000000000000", "111111111111110", "000000000000010", "011111111111110", "010000000000000", "010111111111111", "010000000000000", "111111111111110", "000000000000010", "011111111111110", "010000000000000", "010111111111111", "00000000000000E"]
]

def get_maze_info(maze_grid):
    start_node = end_node = None
    for row in range(15):
        for col in range(15):
            if maze_grid[row][col] == 'S': start_node = (row, col)
            if maze_grid[row][col] == 'E': end_node = (row, col)
    return start_node, end_node

def get_neighbors(current_node, maze_grid):
    row, col = current_node
    valid_neighbors = []
    for delta_row, delta_col in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        new_row, new_col = row + delta_row, col + delta_col
        if 0 <= new_row < 15 and 0 <= new_col < 15 and maze_grid[new_row][new_col] != '1':
            valid_neighbors.append((new_row, new_col))
    return valid_neighbors

def heuristic(node_a, node_b): 
    return abs(node_a[0] - node_b[0]) + abs(node_a[1] - node_b[1])

def bfs(maze_grid):
    start_node, end_node = get_maze_info(maze_grid)
    queue = deque([start_node])
    parent_map = {start_node: None}
    explored_nodes = []
    
    while queue:
        current_node = queue.popleft()
        if current_node != start_node and current_node != end_node: 
            explored_nodes.append(current_node)
        if current_node == end_node: 
            break
            
        for neighbor in get_neighbors(current_node, maze_grid):
            if neighbor not in parent_map: 
                parent_map[neighbor] = current_node
                queue.append(neighbor)
                
    shortest_path = []
    backtrack_node = end_node
    while backtrack_node in parent_map and parent_map[backtrack_node] is not None: 
        shortest_path.append(backtrack_node)
        backtrack_node = parent_map[backtrack_node]
        
    return explored_nodes, shortest_path[::-1]

def dfs(maze_grid):
    start_node, end_node = get_maze_info(maze_grid)
    stack = [start_node]
    parent_map = {start_node: None}
    explored_nodes = []
    
    while stack:
        current_node = stack.pop()
        if current_node != start_node and current_node != end_node: 
            explored_nodes.append(current_node)
        if current_node == end_node: 
            break
            
        for neighbor in reversed(get_neighbors(current_node, maze_grid)):
            if neighbor not in parent_map: 
                parent_map[neighbor] = current_node
                stack.append(neighbor)
                
    shortest_path = []
    backtrack_node = end_node
    while backtrack_node in parent_map and parent_map[backtrack_node] is not None: 
        shortest_path.append(backtrack_node)
        backtrack_node = parent_map[backtrack_node]
        
    return explored_nodes, shortest_path[::-1]

def greedy(maze_grid):
    start_node, end_node = get_maze_info(maze_grid)
    priority_queue = [(heuristic(start_node, end_node), start_node)]
    parent_map = {start_node: None}
    explored_nodes = []
    
    while priority_queue:
        _, current_node = heapq.heappop(priority_queue)
        if current_node != start_node and current_node != end_node: 
            explored_nodes.append(current_node)
        if current_node == end_node: 
            break
            
        for neighbor in get_neighbors(current_node, maze_grid):
            if neighbor not in parent_map: 
                parent_map[neighbor] = current_node
                heapq.heappush(priority_queue, (heuristic(neighbor, end_node), neighbor))
                
    shortest_path = []
    backtrack_node = end_node
    while backtrack_node in parent_map and parent_map[backtrack_node] is not None: 
        shortest_path.append(backtrack_node)
        backtrack_node = parent_map[backtrack_node]
        
    return explored_nodes, shortest_path[::-1]

def astar(maze_grid):
    start_node, end_node = get_maze_info(maze_grid)
    # Priority Queue stores: (f_score, g_score, node)
    priority_queue = [(heuristic(start_node, end_node), 0, start_node)]
    parent_map = {start_node: None}
    explored_nodes = []
    g_scores = {start_node: 0}
    visited_set = set()
    
    while priority_queue:
        _, current_g_score, current_node = heapq.heappop(priority_queue)
        
        if current_node in visited_set: 
            continue
        visited_set.add(current_node)
        
        if current_node != start_node and current_node != end_node: 
            explored_nodes.append(current_node)
        if current_node == end_node: 
            break
            
        for neighbor in get_neighbors(current_node, maze_grid):
            new_g_score = current_g_score + 1
            if neighbor not in g_scores or new_g_score < g_scores[neighbor]: 
                g_scores[neighbor] = new_g_score
                parent_map[neighbor] = current_node
                f_score = new_g_score + heuristic(neighbor, end_node)
                heapq.heappush(priority_queue, (f_score, new_g_score, neighbor))
                
    shortest_path = []
    backtrack_node = end_node
    while backtrack_node in parent_map and parent_map[backtrack_node] is not None: 
        shortest_path.append(backtrack_node)
        backtrack_node = parent_map[backtrack_node]
        
    return explored_nodes, shortest_path[::-1]


# ================= الواجهة المدمجة =================
class CompactMazeApp:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("AI Maze Solver")
        self.root.geometry("650x780") 
        self.root.configure(bg=BG_COLOR)
        
        self.current_maze_idx = 0
        self.cell_size = 22 
        self.is_animating = False
        self.algorithms = {"DFS": dfs, "BFS": bfs, "Greedy": greedy, "A*": astar}
        self.grid_cells = {}
        
        self.build_ui()
        self.reset_maze()

    def build_ui(self):
        tk.Label(self.root, text="Maze AI", font=("Segoe UI", 16, "bold"), bg=BG_COLOR, fg=ACCENT).pack(pady=5)

        buttons_frame = tk.Frame(self.root, bg=BG_COLOR)
        buttons_frame.pack(pady=2)
        for alg_name, alg_func in self.algorithms.items():
            tk.Button(buttons_frame, text=alg_name, bg=BTN_BG, fg=BTN_FG, width=8, font=("Segoe UI", 9, "bold"),
                      relief="flat", cursor="hand2", command=lambda func=alg_func: self.start_solving(func)).pack(side="left", padx=3)

        self.canvas = tk.Canvas(self.root, width=334, height=334, bg=CANVAS_BG, highlightthickness=1, highlightbackground="#585B70")
        self.canvas.pack(pady=8)

        controls_frame = tk.Frame(self.root, bg=BG_COLOR)
        controls_frame.pack(pady=2)
        self.level_var = tk.IntVar(value=1)
        for level in range(1, 6):
            tk.Radiobutton(controls_frame, text=f"L{level}", variable=self.level_var, value=level, bg=BG_COLOR, fg=PATH_COLOR,
                           selectcolor=BTN_BG, font=("Segoe UI", 10), command=self.reset_maze).pack(side="left", padx=5)

        tk.Button(self.root, text="BEST ALGORITHM ANALYSIS 🏆", bg=ACCENT, fg="#11111B", 
                  font=("Segoe UI", 11, "bold"), relief="flat", padx=20, pady=3, command=self.show_best_algorithms).pack(pady=10)

        self.results_frame = tk.Frame(self.root, bg="#24273A", padx=10, pady=10, relief="ridge", borderwidth=1)
        self.results_frame.pack(fill="x", padx=30)
        
        headers = ["Algorithm", "Nodes", "Path", "Score"]
        for col_idx, header_text in enumerate(headers):
            tk.Label(self.results_frame, text=header_text, bg="#24273A", fg=ACCENT, font=("Segoe UI", 9, "bold")).grid(row=0, column=col_idx, sticky="nsew", padx=10)
        
        for col_idx in range(4): 
            self.results_frame.columnconfigure(col_idx, weight=1)
            
        self.table_rows = []

    def reset_maze(self):
        self.is_animating = False
        self.current_maze_idx = self.level_var.get() - 1
        self.canvas.delete("all")
        self.grid_cells = {}
        
        current_maze = MAZES[self.current_maze_idx]
        for row in range(15):
            for col in range(15):
                x1, y1 = col * self.cell_size + 2, row * self.cell_size + 2
                cell_color = PATH_COLOR
                
                if current_maze[row][col] == '1': cell_color = CANVAS_BG
                elif current_maze[row][col] == 'S': cell_color = START_COLOR
                elif current_maze[row][col] == 'E': cell_color = END_COLOR
                
                self.grid_cells[(row, col)] = self.canvas.create_rectangle(x1, y1, x1 + self.cell_size, y1 + self.cell_size, fill=cell_color, outline="#1E1E2E")
                
        for row_labels in self.table_rows: 
            for label in row_labels: label.destroy()
        self.table_rows = []

    def start_solving(self, algorithm_func):
        if self.is_animating: return
        self.reset_maze()
        self.is_animating = True
        
        explored_nodes, shortest_path = algorithm_func(MAZES[self.current_maze_idx])
        self.animate_exploration(explored_nodes, shortest_path, 0)

    def animate_exploration(self, explored_nodes, shortest_path, step_index):
        if not self.is_animating: return
        
        if step_index < len(explored_nodes):
            self.canvas.itemconfig(self.grid_cells[explored_nodes[step_index]], fill=VISITED_COLOR)
            self.root.after(8, lambda: self.animate_exploration(explored_nodes, shortest_path, step_index + 1))
        else: 
            self.animate_path(shortest_path, 0)

    def animate_path(self, shortest_path, step_index):
        if not self.is_animating: return
        
        if step_index < len(shortest_path):
            node = shortest_path[step_index]
            if MAZES[self.current_maze_idx][node[0]][node[1]] != 'E':
                self.canvas.itemconfig(self.grid_cells[node], fill=ROUTE_COLOR)
            self.root.after(15, lambda: self.animate_path(shortest_path, step_index + 1))
        else: 
            self.is_animating = False

    def show_best_algorithms(self):
        current_maze = MAZES[self.current_maze_idx]
        analysis_data = []
        
        for alg_name, alg_func in self.algorithms.items():
            explored_nodes, shortest_path = alg_func(current_maze)
            score = len(explored_nodes) + len(shortest_path) if shortest_path else 999
            analysis_data.append({
                "name": alg_name, 
                "visited": len(explored_nodes), 
                "path_len": len(shortest_path) if shortest_path else "N/A", 
                "score": score
            })
        
        analysis_data.sort(key=lambda item: item["score"])
        
        for row_labels in self.table_rows: 
            for label in row_labels: label.destroy()
        self.table_rows = []

        for row_idx, data in enumerate(analysis_data):
            text_color = START_COLOR if row_idx == 0 else BTN_FG
            font_style = ("Segoe UI", 9, "bold") if row_idx == 0 else ("Segoe UI", 9)
            
            display_values = [data["name"] + (" 🏆" if row_idx == 0 else ""), data["visited"], data["path_len"], data["score"]]
            current_row_labels = []
            
            for col_idx, value in enumerate(display_values):
                label = tk.Label(self.results_frame, text=value, bg="#24273A", fg=text_color, font=font_style)
                label.grid(row=row_idx + 1, column=col_idx, pady=1)
                current_row_labels.append(label)
                
            self.table_rows.append(current_row_labels)

if __name__ == "__main__":
    main_window = tk.Tk()
    CompactMazeApp(main_window)
    main_window.mainloop()


