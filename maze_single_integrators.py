import pygame

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Robot settings
robot_radius = 5
robot_color = WHITE

# Initiate multiple robots
robots = [
    {"x": 75, "y": 75, "dx": 5, "dy": 5},
    {"x": 90, "y": 75, "dx": 4, "dy": 4},
    {"x": 105, "y": 75, "dx": 3, "dy": 3},
    {"x": 60, "y": 75, "dx": 5, "dy": 5},
    {"x": 45, "y": 75, "dx": 3, "dy": 3},
    {"x": 30, "y": 75, "dx": 5, "dy": 5},
    {"x": 75, "y": 90, "dx": 3, "dy": 3},
    {"x": 75, "y": 105, "dx": 4, "dy": 4},
    {"x": 75, "y": 60, "dx": 5, "dy": 5},
    {"x": 75, "y": 45, "dx": 4, "dy": 4},
]

# Obstacles (example: lines and optional circles)
obstacles = [
    # Frame
    {"type": "line", "start_pos": (0, 0), "end_pos": (0, 600), "width": 5},
    {"type": "line", "start_pos": (0, 0), "end_pos": (800, 0), "width": 5},
    {"type": "line", "start_pos": (800, 0), "end_pos": (800, 600), "width": 5},
    {"type": "line", "start_pos": (0, 600), "end_pos": (800, 600), "width": 5},
    # Walls
    {"type": "line", "start_pos": (0, 150), "end_pos": (650, 150), "width": 5},
    {"type": "line", "start_pos": (150, 300), "end_pos": (800, 300), "width": 5},
    {"type": "line", "start_pos": (0, 450), "end_pos": (650, 450), "width": 5},
]

def draw_obstacles():
    for obstacle in obstacles:
        if obstacle["type"] == "line":
            pygame.draw.line(screen, RED, obstacle["start_pos"], obstacle["end_pos"], obstacle["width"])
        elif obstacle["type"] == "circle":
            pygame.draw.circle(screen, RED, obstacle["center"], obstacle["radius"])

def move_robots(direction_x, direction_y):
    for i, robot in enumerate(robots):
        new_x = robot["x"] + direction_x * robot["dx"]
        new_y = robot["y"] + direction_y * robot["dy"]
        can_move = True

        # Check collision with obstacles
        for obstacle in obstacles:
            if obstacle["type"] == "circle":
                distance = ((new_x - obstacle["center"][0]) ** 2 + (new_y - obstacle["center"][1]) ** 2) ** 0.5
                if distance < robot_radius + obstacle["radius"]:
                    can_move = False
                    break
            elif obstacle["type"] == "line":
                start_x, start_y = obstacle["start_pos"]
                end_x, end_y = obstacle["end_pos"]
                line_width = obstacle["width"]
                
                if start_y == end_y:  # Horizontal line
                    if start_x > end_x:
                        start_x, end_x = end_x, start_x
                    if start_y - line_width <= new_y <= start_y + line_width and start_x <= new_x <= end_x:
                        can_move = False
                        break
                elif start_x == end_x:  # Vertical line
                    if start_y > end_y:
                        start_y, end_y = end_y, start_y
                    if start_x - line_width <= new_x <= start_x + line_width and start_y <= new_y <= end_y:
                        can_move = False
                        break
        
        # Check collision with other robots
        for j, other_robot in enumerate(robots):
            if i != j:  # Don't check against itself
                distance = ((new_x - other_robot["x"]) ** 2 + (new_y - other_robot["y"]) ** 2) ** 0.5
                if distance < robot_radius * 2:  # Assuming all robots have the same radius
                    can_move = False
                    break
        
        if can_move:
            robot["x"], robot["y"] = new_x, new_y


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    direction_x = 0
    direction_y = 0
    if keys[pygame.K_LEFT]:
        direction_x = -1
    if keys[pygame.K_RIGHT]:
        direction_x = 1
    if keys[pygame.K_UP]:
        direction_y = -1
    if keys[pygame.K_DOWN]:
        direction_y = 1
    
    move_robots(direction_x, direction_y)

    # Clear the screen
    screen.fill(BLACK)
    # Draw the obstacles
    draw_obstacles()
    # Draw each robot
    for robot in robots:
        pygame.draw.circle(screen, robot_color, (robot["x"], robot["y"]), robot_radius)
    
    # Update the display
    pygame.display.flip()
    # Cap the frame rate
    pygame.time.Clock().tick(60)

pygame.quit()