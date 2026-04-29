import pygame
import sys
import time
import heapq
from collections import deque

# --- إعدادات الألوان ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (100, 150, 255)
VISITED_COLOR = (200, 230, 255) # لون الاستكشاف (أزرق فاتح جداً)
LIGHT_BLUE = (173, 216, 230)
BG_COLOR = (240, 240, 240)

# --- إعدادات النافذة والشبكة ---
WIDTH, HEIGHT = 800, 700
ROWS, COLS = 20, 20
CELL_SIZE = 25
GRID_WIDTH = COLS * CELL_SIZE
GRID_HEIGHT = ROWS * CELL_SIZE
GRID_X = (WIDTH - GRID_WIDTH) // 2
GRID_Y = 200

# --- الخرائط (المتاهات) ---
maps = [
    [
        "S.##################",
        "#.      #          #",
        "#.#.###.#.########.#",
        "#.#.#   #.#      #.#",
        "###.#.###.#.#### #.#",
        "#.  #.#   #.#    #.#",
        "#.###.#.###.#.####.#",
        "#.#   #.#   #.#  #.#",
        "#.#.###.#.###.#.##.#",
        "#.#.#   #.#   #.#  #",
        "#.#.#.###.#.###.#.##",
        "#.#.#.#   #.#   #.# ",
        "#.#.###.###.#.###.##",
        "#.#.#       #.#   .#",
        "###.#########.#.##.#",
        "#.  #         #.#  #",
        "#.###.#########.#.##",
        "#.#   #         #.# ",
        "#.#.###.#########.##",
        ".................. E"
    ],
    [
        "S..................#",
        "#.################.#",
        "#..................#",
        "#.################.#",
        "#..................#",
        "#.################.#",
        "#..................#",
        "#.################.#",
        "#..................#",
        "#.################.#",
        "#..................#",
        "#.################.#",
        "#..................#",
        "#.################.#",
        "#..................#",
        "#.################.#",
        "#..................#",
        "#.################.#",
        "#..................#",
        "##################.E"
    ]
]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smart Maze")
font = pygame.font.SysFont("arial", 16, bold=True)
stats_font = pygame.font.SysFont("arial", 14, bold=True)

class Button:
    def __init__(self, x, y, w, h, text, color, hover_color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, surface, selected=False):
        color = LIGHT_BLUE if selected else (self.hover_color if self.is_hovered else self.color)
        if self.text == "START": color = GREEN
        
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)

# --- خوارزميات البحث ترجع الآن ترتيب العقد التي تم استكشافها لرسمها ---
def get_neighbors(r, c, grid):
    neighbors = []
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] != '#':
            neighbors.append((nr, nc))
    return neighbors

def solve_bfs(grid, start, end):
    queue = deque([start])
    came_from = {start: None}
    visited_order = []
    visited_set = {start}
    
    while queue:
        current = queue.popleft()
        visited_order.append(current)
        
        if current == end:
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            return path[::-1], visited_order, len(visited_order)
            
        for neighbor in get_neighbors(current[0], current[1], grid):
            if neighbor not in visited_set:
                visited_set.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)
    return [], visited_order, len(visited_order)

def solve_dfs(grid, start, end):
    stack = [(start, [start])]
    visited_order = []
    visited_set = set()
    
    while stack:
        current, path = stack.pop()
        
        if current in visited_set:
            continue
            
        visited_set.add(current)
        visited_order.append(current)
        
        if current == end:
            return path, visited_order, len(visited_order)
            
        for neighbor in get_neighbors(current[0], current[1], grid):
            if neighbor not in visited_set:
                stack.append((neighbor, path + [neighbor]))
    return [], visited_order, len(visited_order)

def solve_astar(grid, start, end):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
        
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {start: None}
    g_score = {start: 0}
    visited_order = []
    visited_set = set()
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current in visited_set:
            continue
            
        visited_set.add(current)
        visited_order.append(current)
        
        if current == end:
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            return path[::-1], visited_order, len(visited_order)
            
        for neighbor in get_neighbors(current[0], current[1], grid):
            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic(neighbor, end)
                heapq.heappush(open_set, (f_score, neighbor))
    return [], visited_order, len(visited_order)

# --- الحلقة الرئيسية للبرنامج ---
def main():
    clock = pygame.time.Clock()
    
    buttons = {
        "BFS": Button(200, 30, 60, 30, "BFS", WHITE, GRAY),
        "DFS": Button(270, 30, 60, 30, "DFS", WHITE, GRAY),
        "A*": Button(340, 30, 60, 30, "A*", WHITE, GRAY),
        "START": Button(410, 30, 70, 30, "START", GREEN, GREEN),
        "RESET": Button(490, 30, 70, 30, "RESET", WHITE, GRAY),
        "SWITCH": Button(570, 30, 80, 30, "SWITCH", WHITE, GRAY)
    }
    
    current_algo = "A*"
    map_index = 0
    path = []
    visited_nodes = []
    
    stats = {
        "BFS": {"time": 0.0, "nodes": 0},
        "DFS": {"time": 0.0, "nodes": 0},
        "A*": {"time": 0.0, "nodes": 0}
    }

    # دالة داخلية لرسم الشاشة أثناء حركة الـ Animation
    def draw_current_state(current_grid, start_pos, end_pos, current_visited, current_path):
        screen.fill(BG_COLOR)
        
        for name, btn in buttons.items():
            btn.draw(screen, selected=(name == current_algo))

        stats_text = [
            f"BFS: {stats['BFS']['time']:.5f}s | {stats['BFS']['nodes']}",
            f"DFS: {stats['DFS']['time']:.5f}s | {stats['DFS']['nodes']}",
            f"A*: {stats['A*']['time']:.5f}s | {stats['A*']['nodes']}"
        ]
        
        for i, text in enumerate(stats_text):
            surf = stats_font.render(text, True, BLACK)
            screen.blit(surf, (150 + i * 180, 80))
            
        map_text = stats_font.render(f"Map: {map_index + 1}", True, BLACK)
        screen.blit(map_text, (WIDTH // 2 - 30, 110))

        for r in range(ROWS):
            for c in range(COLS):
                rect = pygame.Rect(GRID_X + c * CELL_SIZE, GRID_Y + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                
                if current_grid[r][c] == '#':
                    pygame.draw.rect(screen, BLACK, rect)
                else:
                    pygame.draw.rect(screen, WHITE, rect)
                    
                if (r, c) in current_path and current_grid[r][c] not in ['S', 'E']:
                    pygame.draw.rect(screen, BLUE, rect)
                elif (r, c) in current_visited and current_grid[r][c] not in ['S', 'E']:
                    pygame.draw.rect(screen, VISITED_COLOR, rect)
                    
                if current_grid[r][c] == 'S':
                    pygame.draw.rect(screen, GREEN, rect)
                elif current_grid[r][c] == 'E':
                    pygame.draw.rect(screen, RED, rect)
                    
                pygame.draw.rect(screen, GRAY, rect, 1)

        pygame.display.flip()

    running = True
    while running:
        current_grid = maps[map_index]
        start_pos = None
        end_pos = None
        
        for r in range(ROWS):
            for c in range(COLS):
                if current_grid[r][c] == 'S': start_pos = (r, c)
                elif current_grid[r][c] == 'E': end_pos = (r, c)

        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for name, btn in buttons.items():
                        if btn.rect.collidepoint(mouse_pos):
                            if name in ["BFS", "DFS", "A*"]:
                                current_algo = name
                            elif name == "SWITCH":
                                map_index = (map_index + 1) % len(maps)
                                path = []
                                visited_nodes = []
                            elif name == "RESET":
                                path = []
                                visited_nodes = []
                            elif name == "START":
                                path = []
                                visited_nodes = []
                                
                                # 1. حساب المسار والوقت أولاً (في الخلفية بسرعة)
                                start_time = time.time()
                                if current_algo == "BFS":
                                    final_path, visited_order, nodes = solve_bfs(current_grid, start_pos, end_pos)
                                elif current_algo == "DFS":
                                    final_path, visited_order, nodes = solve_dfs(current_grid, start_pos, end_pos)
                                elif current_algo == "A*":
                                    final_path, visited_order, nodes = solve_astar(current_grid, start_pos, end_pos)
                                end_time = time.time()
                                
                                stats[current_algo]["time"] = end_time - start_time
                                stats[current_algo]["nodes"] = nodes
                                
                                # 2. تشغيل الـ Animation لحركة البحث (اللون الفاتح)
                                temp_visited = []
                                for node in visited_order:
                                    for ev in pygame.event.get():
                                        if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
                                    temp_visited.append(node)
                                    draw_current_state(current_grid, start_pos, end_pos, temp_visited, [])
                                    pygame.time.delay(5) # سرعة حركة البحث
                                
                                visited_nodes = temp_visited
                                
                                # 3. تشغيل الـ Animation لرسم المسار (اللون الغامق)
                                temp_path = []
                                for node in final_path:
                                    for ev in pygame.event.get():
                                        if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
                                    temp_path.append(node)
                                    draw_current_state(current_grid, start_pos, end_pos, visited_nodes, temp_path)
                                    pygame.time.delay(20) # سرعة رسم المسار
                                    
                                path = temp_path

        for name, btn in buttons.items():
            btn.check_hover(mouse_pos)

        # رسم الشاشة في الحالة العادية (عند عدم وجود Animation)
        draw_current_state(current_grid, start_pos, end_pos, visited_nodes, path)
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()