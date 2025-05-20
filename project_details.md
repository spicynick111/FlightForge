# FlightForge: Atmospheric Explorer - Project Documentation

## Overview
FlightForge is a sophisticated 2D game built with Pygame that expands on the classic "Flappy Bird" concept with numerous advanced features. The game uniquely incorporates real-world weather data to dynamically affect gameplay, making each session a distinct experience.

## Core Game Concept
Players control a drone that must navigate through procedurally generated obstacles by "flapping" (pressing the space bar). The game's environment and physics are influenced by real-time weather conditions, creating a dynamic and ever-changing gameplay experience.

## Key Technical Features

### Weather Integration
- Fetches real-time weather data from open-meteo.com API
- Adapts gameplay based on temperature, wind speed, and weather codes
- Changes visual elements (background color, obstacle color) based on weather conditions
- Modifies gameplay mechanics (wind force, gravity, flap strength) based on weather conditions
- Weather-specific particle effects (rain, snow, mist)

### Drone Selection System
- Three drone types: Standard, Heavy-Duty, and Agile
- Each drone has unique physics properties:
  - Standard: Balanced gravity (0.5) and flap strength (-8)
  - Heavy-Duty: Higher gravity (0.7) and stronger flap (-10)
  - Agile: Lower gravity (0.4) and gentler flap (-7)
- Visual differentiation through colors (red, blue, green)

### Power-up System
- Multiple power-up types:
  - Shield: Protects from one collision
  - Slow Time: Reduces game speed by 50%
  - Double Points: Doubles score for each obstacle passed
- Visual effects for active power-ups
- Timed duration system
- Collection and activation mechanics

### Particle System
- Weather-dependent particles (rain, snow, mist)
- Visual feedback for player actions
- Dynamic generation and movement

### Achievement System
- Tracks player accomplishments:
  - "First Flight": Fly for the first time
  - "High Flyer": Score 10 points
  - "Weather Navigator": Play in special weather conditions
  - "Master Pilot": Score 20 points
- Displays unlocked achievements on game over screen

### Score and High Score Tracking
- Persistent high score saved to file
- Score display during gameplay
- New high score recognition and celebration

### Audio System
- Sound effects for actions:
  - Flapping
  - Scoring points
  - Collecting power-ups
  - Game over
- File existence checking to prevent errors

### Menu System
- Main menu with drone selection
- Game over screen with achievements and score
- Instructions and controls display

### Obstacle Generation
- Procedurally generated obstacles with varying complexity
- Difficulty scaling based on score
- Multiple obstacle segments with varying gap positions

## Code Structure

### Main Class: FlightForge
- Game initialization and setup
- Game state management
- Physics and collision detection
- Rendering and drawing
- Input handling
- Weather data fetching and application
- Score tracking and achievement management

### Key Methods
- `__init__()`: Sets up game constants, display, and loads resources
- `reset_game()`: Resets all game state variables
- `get_weather_data()`: Fetches real-world weather data
- `apply_weather_effects()`: Applies weather effects to gameplay
- `spawn_obstacle()`: Creates new obstacles with varying complexity
- `spawn_power_up()`: Randomly generates power-ups
- `check_collisions()`: Detects collisions with obstacles and power-ups
- `update_score()`: Updates score when passing obstacles
- `draw_menu()`: Renders the main menu
- `draw_game_over()`: Renders the game over screen
- `run()`: Main game loop

## Technical Implementation Details

### Physics System
- Gravity and velocity calculations
- Wind effects from weather data
- Drone-specific physics properties
- Time factor for slow-motion effect

### Collision Detection
- Rectangle-based collision for obstacles
- Distance-based collision for power-ups
- Special handling for shield power-up

### Resource Management
- Checks for file existence before loading
- Error handling for missing resources
- High score persistence

### State Management
- Transitions between menu, gameplay, and game over states
- Persistent data between sessions

## Controls
- Space: Flap/Select in menus
- Left/Right Arrows: Select drone in menu
- Escape: Return to menu/Quit game

## Future Enhancement Opportunities
- Enhanced visual effects and animations
- Additional drone types with unique abilities
- More power-ups and obstacles
- Achievements and progression system
- Customization options for drones
- Leaderboards and social features
- Additional weather effects and interactions

## Technical Requirements
- Python 3.x
- Pygame library
- Internet connection for weather data (optional)
- Sound files (optional):
  - flap.wav
  - hit.wav
  - point.wav

## Project Structure
- main.py: Main game code
- highscore.txt: Persistent high score storage
- assets/: Directory for game assets (sounds, images)