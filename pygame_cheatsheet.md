# Pygame Quick Reference for Interviews

## Core Pygame Concepts Used in FlightForge

### Initialization and Setup
```python
import pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("FlightForge")
clock = pygame.time.Clock()
```

### Game Loop Structure
```python
running = True
while running:
    # 1. Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # 2. Update game state
    update_game_logic()
    
    # 3. Render graphics
    screen.fill(background_color)
    draw_game_elements()
    
    # 4. Update display and maintain frame rate
    pygame.display.flip()
    clock.tick(60)  # 60 FPS
```

### Drawing Elements
```python
# Drawing shapes
pygame.draw.rect(screen, color, (x, y, width, height))
pygame.draw.circle(screen, color, (center_x, center_y), radius)

# Drawing text
font = pygame.font.SysFont('Arial', 24)
text_surface = font.render("Hello World", True, (255, 255, 255))
screen.blit(text_surface, (x, y))

# Drawing images
image = pygame.image.load("image.png")
screen.blit(image, (x, y))
```

### Collision Detection
```python
# Rectangle collision
rect1 = pygame.Rect(x1, y1, width1, height1)
rect2 = pygame.Rect(x2, y2, width2, height2)
if rect1.colliderect(rect2):
    # Collision occurred

# Circle collision (distance-based)
distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
if distance < radius1 + radius2:
    # Collision occurred
```

### Input Handling
```python
# Keyboard events
if event.type == pygame.KEYDOWN:
    if event.key == pygame.K_SPACE:
        # Space key pressed
    elif event.key == pygame.K_ESCAPE:
        # Escape key pressed

# Mouse events
if event.type == pygame.MOUSEBUTTONDOWN:
    mouse_pos = pygame.mouse.get_pos()
    # Mouse clicked at mouse_pos
```

### Sound Effects
```python
pygame.mixer.init()
sound = pygame.mixer.Sound("sound.wav")
sound.play()

# Background music
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)  # -1 means loop indefinitely
```

### Time Management
```python
current_time = pygame.time.get_ticks()  # Time in milliseconds since pygame.init()

# For timing events
if current_time - last_event_time > event_interval:
    trigger_event()
    last_event_time = current_time
```

## Key Python Concepts Used in FlightForge

### Object-Oriented Programming
```python
class GameObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
    
    def update(self):
        self.y += self.velocity
    
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, 50, 50))
```

### Dictionary Data Structures
```python
# Storing game object properties
drone_stats = {
    "Standard": {"gravity": 0.5, "flap": -8, "color": (255, 0, 0)},
    "Heavy-Duty": {"gravity": 0.7, "flap": -10, "color": (0, 0, 255)},
    "Agile": {"gravity": 0.4, "flap": -7, "color": (0, 255, 0)}
}

# Accessing properties
selected_drone = "Standard"
gravity = drone_stats[selected_drone]["gravity"]
```

### API Integration
```python
import json
import urllib.request

def get_weather_data():
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=40.71&longitude=-74.01&current_weather=true"
        response = urllib.request.urlopen(url)
        data = json.loads(response.read().decode())
        return data["current_weather"]
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return {"temperature": 20, "windspeed": 5, "weathercode": 0}
```

### File I/O
```python
# Reading from file
def load_high_score():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except:
        return 0

# Writing to file
def save_high_score(score):
    try:
        with open("highscore.txt", "w") as file:
            file.write(str(score))
    except:
        pass
```

### Error Handling
```python
def file_exists(filename):
    try:
        with open(filename):
            return True
    except FileNotFoundError:
        return False

# Using the function
sound = pygame.mixer.Sound("sound.wav") if file_exists("sound.wav") else None

# Safely playing sounds
if sound:
    sound.play()
```

## Game Development Concepts

### Game States
- Menu state
- Playing state
- Game over state
- State transitions based on events

### Game Loop
- Input processing
- Game logic update
- Rendering
- Frame rate control

### Physics
- Gravity simulation
- Velocity and acceleration
- Collision response

### Procedural Generation
- Randomly generated obstacles
- Varying difficulty based on score
- Random power-up spawning

### Game Balance
- Difficulty progression
- Risk vs. reward (power-ups)
- Different player options (drone types)

Remember: You don't need to memorize code syntax perfectly for interviews. Understanding the concepts and being able to explain your approach is more important!