import pygame
import random
import sys
import math
import time
import json
import urllib.request
from datetime import datetime

class FlightForge:
    def __init__(self):
        pygame.init()
        
        # Game Constants
        self.WIDTH, self.HEIGHT = 800, 600
        self.GRAVITY = 0.5
        self.FLAP_STRENGTH = -8
        self.SCROLL_SPEED = 3
        self.OBSTACLE_GAP = 200
        self.OBSTACLE_FREQUENCY = 1500  # milliseconds between obstacles
        
        # Display setup
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("FlightForge: Atmospheric Explorer")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 25)
        self.large_font = pygame.font.SysFont('Arial', 40)
        
        # Game state variables
        self.reset_game()
        
        # Load weather data
        self.weather_conditions = self.get_weather_data()
        self.apply_weather_effects()
        
        # Audio setup
        pygame.mixer.init()
        self.sound_flap = pygame.mixer.Sound("flap.wav") if self.file_exists("flap.wav") else None
        self.sound_hit = pygame.mixer.Sound("hit.wav") if self.file_exists("hit.wav") else None
        self.sound_point = pygame.mixer.Sound("point.wav") if self.file_exists("point.wav") else None
        
        # Menu state
        self.show_menu = True
        self.drone_selection = 0
        self.drones = ["Standard", "Heavy-Duty", "Agile"]
        self.drone_stats = {
            "Standard": {"gravity": 0.5, "flap": -8, "color": (255, 0, 0)},
            "Heavy-Duty": {"gravity": 0.7, "flap": -10, "color": (0, 0, 255)},
            "Agile": {"gravity": 0.4, "flap": -7, "color": (0, 255, 0)}
        }
        
        # Achievement system
        self.achievements = {
            "First Flight": {"description": "Fly for the first time", "unlocked": False},
            "High Flyer": {"description": "Score 10 points", "unlocked": False},
            "Weather Navigator": {"description": "Play in special weather conditions", "unlocked": False},
            "Master Pilot": {"description": "Score 20 points", "unlocked": False}
        }
        
        # Load high score
        self.high_score = self.load_high_score()
    
    def file_exists(self, filename):
        """Check if file exists to prevent errors when loading sounds"""
        try:
            with open(filename):
                return True
        except FileNotFoundError:
            return False
    
    def reset_game(self):
        """Reset all game state variables"""
        self.drone_x = 100
        self.drone_y = self.HEIGHT // 2
        self.drone_vel_y = 0
        self.obstacles = []
        self.last_obstacle_time = pygame.time.get_ticks()
        self.score = 0
        self.game_over = False
        self.particles = []
        self.obstacle_passed = set()  # Track which obstacles we've passed for scoring
        
        # Power-up system
        self.power_ups = []
        self.active_power_ups = {}
        self.power_up_types = {
            "shield": {"duration": 5000, "color": (255, 215, 0)},
            "slow_time": {"duration": 3000, "color": (0, 191, 255)},
            "double_points": {"duration": 7000, "color": (138, 43, 226)}
        }
    
    def get_weather_data(self):
        """Attempt to fetch real-world weather data for dynamic gameplay"""
        try:
            # Using a free weather API - in production, use a more reliable service
            # and your own API key
            url = "https://api.open-meteo.com/v1/forecast?latitude=40.71&longitude=-74.01&current_weather=true"
            response = urllib.request.urlopen(url)
            data = json.loads(response.read().decode())
            return {
                "temperature": data["current_weather"]["temperature"],
                "wind_speed": data["current_weather"]["windspeed"],
                "weather_code": data["current_weather"]["weathercode"]
            }
        except Exception as e:
            print(f"Error fetching weather data: {e}")
            # Default weather conditions if API fails
            return {
                "temperature": 20,
                "wind_speed": 5,
                "weather_code": 0  # 0 is clear sky
            }
    
    def apply_weather_effects(self):
        """Apply weather effects to gameplay based on real-world data"""
        if self.weather_conditions:
            # Wind effects based on real wind speed
            self.wind_force = (self.weather_conditions["wind_speed"] - 5) * 0.05
            
            # Visual effects based on weather code
            code = self.weather_conditions["weather_code"]
            
            # Clear sky (0-1)
            if code <= 1:
                self.bg_color = (135, 206, 235)  # Sky blue
                self.obstacle_color = (34, 139, 34)  # Forest green
                self.has_particles = False
            
            # Cloudy (2-3)
            elif code <= 3:
                self.bg_color = (200, 200, 200)  # Gray
                self.obstacle_color = (105, 105, 105)  # Dim gray
                self.has_particles = False
            
            # Foggy/Misty (45-48)
            elif code in [45, 48]:
                self.bg_color = (220, 220, 220)  # Light gray
                self.obstacle_color = (169, 169, 169)  # Dark gray
                self.has_particles = True
                self.particle_color = (255, 255, 255)  # White mist
                # Reduce visibility by increasing obstacle frequency
                self.OBSTACLE_FREQUENCY = 1200
            
            # Rainy (51-67)
            elif 51 <= code <= 67:
                self.bg_color = (105, 105, 105)  # Dim gray
                self.obstacle_color = (47, 79, 79)  # Dark slate gray
                self.has_particles = True
                self.particle_color = (184, 184, 184)  # Light gray rain
                # Make gameplay harder with reduced flap strength
                self.FLAP_STRENGTH = -7.5
            
            # Snowy (71-77)
            elif 71 <= code <= 77:
                self.bg_color = (240, 248, 255)  # Alice blue
                self.obstacle_color = (176, 196, 222)  # Light steel blue
                self.has_particles = True
                self.particle_color = (255, 250, 250)  # Snow
                # Make control more slippery
                self.GRAVITY = 0.45
            
            # Thunderstorm (80-99)
            elif code >= 80:
                self.bg_color = (47, 79, 79)  # Dark slate gray
                self.obstacle_color = (25, 25, 112)  # Midnight blue
                self.has_particles = True
                self.particle_color = (255, 255, 0)  # Yellow lightning
                # Make gameplay unpredictable with wind gusts
                self.FLAP_STRENGTH = -8.5
                
            # Mark weather navigation achievement
            if code != 0:
                self.achievements["Weather Navigator"]["unlocked"] = True
        else:
            # Default settings if no weather data
            self.wind_force = 0
            self.bg_color = (135, 206, 235)  # Sky blue
            self.obstacle_color = (34, 139, 34)  # Forest green
            self.has_particles = False
    
    def spawn_obstacle(self):
        """Create a new obstacle with varying height and gap position"""
        gap_y = random.randint(100, self.HEIGHT - 100 - self.OBSTACLE_GAP)
        
        # Create more complex obstacles as score increases
        complexity = min(self.score // 5, 3)
        segments = 1 + complexity
        
        obstacle_parts = []
        
        for i in range(segments):
            segment_gap_y = gap_y + random.randint(-30, 30)
            segment_gap_y = max(50, min(self.HEIGHT - 50 - self.OBSTACLE_GAP, segment_gap_y))
            
            obstacle_parts.append({
                "x": self.WIDTH,
                "gap_y": segment_gap_y,
                "width": 50,
                "passed": False
            })
        
        self.obstacles.append(obstacle_parts)
    
    def spawn_power_up(self):
        """Spawn a random power-up"""
        if random.random() < 0.2:  # 20% chance to spawn a power-up
            power_up_type = random.choice(list(self.power_up_types.keys()))
            self.power_ups.append({
                "type": power_up_type,
                "x": self.WIDTH,
                "y": random.randint(50, self.HEIGHT - 50),
                "radius": 15,
                "collected": False
            })
    
    def draw_drone(self):
        """Draw the player's drone with animations based on velocity"""
        drone_color = self.drone_stats[self.drones[self.drone_selection]]["color"]
        
        # Base drone shape
        pygame.draw.circle(self.screen, drone_color, (self.drone_x, self.drone_y), 20)
        
        # Propellers animation based on flapping
        propeller_speed = abs(self.drone_vel_y) * 2
        propeller_offset = 5 + propeller_speed
        
        # Draw propellers
        pygame.draw.line(self.screen, (50, 50, 50), 
                         (self.drone_x - 15, self.drone_y - propeller_offset),
                         (self.drone_x - 25, self.drone_y - propeller_offset), 5)
        pygame.draw.line(self.screen, (50, 50, 50), 
                         (self.drone_x + 15, self.drone_y - propeller_offset),
                         (self.drone_x + 25, self.drone_y - propeller_offset), 5)
        
        # Draw body details
        pygame.draw.rect(self.screen, (80, 80, 80), 
                         (self.drone_x - 10, self.drone_y - 5, 20, 10))
        
        # Draw active power-ups visual effects
        if "shield" in self.active_power_ups:
            pygame.draw.circle(self.screen, (255, 215, 0, 128), 
                              (self.drone_x, self.drone_y), 25, 2)
        
        if "slow_time" in self.active_power_ups:
            pygame.draw.circle(self.screen, (0, 191, 255, 128), 
                              (self.drone_x, self.drone_y), 30, 1)
    
    def draw_obstacles(self):
        """Draw the obstacles"""
        for obstacle_set in self.obstacles:
            for obstacle in obstacle_set:
                # Top obstacle
                pygame.draw.rect(self.screen, self.obstacle_color, 
                                (obstacle["x"], 0, obstacle["width"], obstacle["gap_y"]))
                
                # Bottom obstacle
                pygame.draw.rect(self.screen, self.obstacle_color, 
                                (obstacle["x"], 
                                 obstacle["gap_y"] + self.OBSTACLE_GAP, 
                                 obstacle["width"], 
                                 self.HEIGHT - (obstacle["gap_y"] + self.OBSTACLE_GAP)))
    
    def draw_power_ups(self):
        """Draw power-ups"""
        for power_up in self.power_ups:
            if not power_up["collected"]:
                color = self.power_up_types[power_up["type"]]["color"]
                pygame.draw.circle(self.screen, color, 
                                  (power_up["x"], power_up["y"]), 
                                  power_up["radius"])
                
                # Draw icon inside based on type
                if power_up["type"] == "shield":
                    pygame.draw.circle(self.screen, (255, 255, 255), 
                                      (power_up["x"], power_up["y"]), 
                                      power_up["radius"] - 5, 2)
                elif power_up["type"] == "slow_time":
                    # Draw clock symbol
                    pygame.draw.circle(self.screen, (255, 255, 255), 
                                      (power_up["x"], power_up["y"]), 
                                      power_up["radius"] - 5, 1)
                    pygame.draw.line(self.screen, (255, 255, 255),
                                    (power_up["x"], power_up["y"]),
                                    (power_up["x"] + 5, power_up["y"] - 3), 2)
                elif power_up["type"] == "double_points":
                    # Draw x2 symbol
                    text = self.font.render("x2", True, (255, 255, 255))
                    text_rect = text.get_rect(center=(power_up["x"], power_up["y"]))
                    self.screen.blit(text, text_rect)
    
    def update_particles(self):
        """Update particle effects for weather visualization"""
        if self.has_particles:
            # Add new particles
            if random.random() < 0.3:
                self.particles.append({
                    "x": random.randint(0, self.WIDTH),
                    "y": 0,
                    "size": random.randint(1, 3),
                    "speed": random.uniform(2, 5)
                })
            
            # Update existing particles
            for particle in self.particles[:]:
                particle["y"] += particle["speed"]
                if particle["y"] > self.HEIGHT:
                    self.particles.remove(particle)
    
    def draw_particles(self):
        """Draw weather particles"""
        for particle in self.particles:
            pygame.draw.circle(self.screen, self.particle_color, 
                              (int(particle["x"]), int(particle["y"])), 
                              particle["size"])
    
    def draw_hud(self):
        """Draw heads-up display with score and active power-ups"""
        # Score display
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (20, 20))
        
        # High score
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, (255, 255, 255))
        self.screen.blit(high_score_text, (20, 50))
        
        # Display active power-ups
        power_up_y = 80
        for power_up, end_time in self.active_power_ups.items():
            remaining = (end_time - pygame.time.get_ticks()) / 1000
            if remaining > 0:
                power_text = self.font.render(f"{power_up.title()}: {remaining:.1f}s", True, 
                                           self.power_up_types[power_up]["color"])
                self.screen.blit(power_text, (20, power_up_y))
                power_up_y += 30
        
        # Weather info
        if self.weather_conditions:
            weather_text = self.font.render(
                f"Temp: {self.weather_conditions['temperature']}°C | Wind: {self.weather_conditions['wind_speed']} km/h", 
                True, (255, 255, 255))
            self.screen.blit(weather_text, (self.WIDTH - 350, 20))
    
    def check_collisions(self):
        """Check if the drone has collided with obstacles or collected power-ups"""
        # Skip collision detection if shield is active
        if "shield" in self.active_power_ups:
            has_shield = True
        else:
            has_shield = False
        
        # Check if drone hit the ceiling or floor
        if self.drone_y <= 0 or self.drone_y >= self.HEIGHT:
            if not has_shield:
                self.game_over = True
                if self.sound_hit:
                    self.sound_hit.play()
        
        # Check obstacle collisions
        drone_rect = pygame.Rect(self.drone_x - 20, self.drone_y - 20, 40, 40)
        
        for obstacle_set in self.obstacles:
            for obstacle in obstacle_set:
                # Top obstacle rect
                top_rect = pygame.Rect(obstacle["x"], 0, 
                                      obstacle["width"], obstacle["gap_y"])
                
                # Bottom obstacle rect
                bottom_rect = pygame.Rect(obstacle["x"], 
                                         obstacle["gap_y"] + self.OBSTACLE_GAP,
                                         obstacle["width"], 
                                         self.HEIGHT - (obstacle["gap_y"] + self.OBSTACLE_GAP))
                
                # Check for collisions
                if drone_rect.colliderect(top_rect) or drone_rect.colliderect(bottom_rect):
                    if not has_shield:
                        self.game_over = True
                        if self.sound_hit:
                            self.sound_hit.play()
                    else:
                        # Remove shield after blocking one hit
                        del self.active_power_ups["shield"]
        
        # Check power-up collisions
        for power_up in self.power_ups:
            if not power_up["collected"]:
                # Simple distance-based collision detection
                distance = math.sqrt((self.drone_x - power_up["x"])**2 + 
                                    (self.drone_y - power_up["y"])**2)
                
                if distance < power_up["radius"] + 20:  # 20 is drone radius
                    power_up["collected"] = True
                    
                    # Activate power-up
                    power_up_type = power_up["type"]
                    duration = self.power_up_types[power_up_type]["duration"]
                    self.active_power_ups[power_up_type] = pygame.time.get_ticks() + duration
    
    def update_score(self):
        """Update score when passing obstacles"""
        for obstacle_set in self.obstacles:
            for i, obstacle in enumerate(obstacle_set):
                if not obstacle["passed"] and self.drone_x > obstacle["x"] + obstacle["width"]:
                    obstacle["passed"] = True
                    self.score += 1 * (2 if "double_points" in self.active_power_ups else 1)
                    
                    if self.sound_point:
                        self.sound_point.play()
                    
                    # Unlock achievements
                    if self.score >= 10:
                        self.achievements["High Flyer"]["unlocked"] = True
                    if self.score >= 20:
                        self.achievements["Master Pilot"]["unlocked"] = True
    
    def check_power_up_expiry(self):
        """Check and remove expired power-ups"""
        current_time = pygame.time.get_ticks()
        for power_up in list(self.active_power_ups.keys()):
            if self.active_power_ups[power_up] < current_time:
                del self.active_power_ups[power_up]
    
    def load_high_score(self):
        """Load high score from file"""
        try:
            with open("highscore.txt", "r") as file:
                return int(file.read())
        except:
            return 0
    
    def save_high_score(self):
        """Save high score to file"""
        if self.score > self.high_score:
            self.high_score = self.score
            try:
                with open("highscore.txt", "w") as file:
                    file.write(str(self.high_score))
            except:
                pass
    
    def draw_menu(self):
        """Draw main menu"""
        # Background
        self.screen.fill((50, 50, 50))
        
        # Title
        title_text = self.large_font.render("FlightForge: Atmospheric Explorer", True, (255, 255, 255))
        self.screen.blit(title_text, (self.WIDTH//2 - title_text.get_width()//2, 100))
        
        # Instructions
        instructions = [
            "Navigate your drone through obstacles",
            "Space to flap, avoid obstacles",
            "Collect power-ups for special abilities",
            "Real weather affects gameplay dynamics!",
            "",
            "Press SPACE to start flying",
            "Left/Right arrows to select drone"
        ]
        
        y_pos = 200
        for line in instructions:
            text = self.font.render(line, True, (200, 200, 200))
            self.screen.blit(text, (self.WIDTH//2 - text.get_width()//2, y_pos))
            y_pos += 30
        
        # Drone selection
        y_pos = 400
        for i, drone in enumerate(self.drones):
            color = (255, 255, 255) if i == self.drone_selection else (100, 100, 100)
            drone_text = self.font.render(drone, True, color)
            
            # Highlight selected drone
            if i == self.drone_selection:
                pygame.draw.rect(self.screen, (70, 70, 70), 
                               (self.WIDTH//2 - 100, y_pos - 5, 200, 30))
            
            self.screen.blit(drone_text, (self.WIDTH//2 - drone_text.get_width()//2, y_pos))
            y_pos += 40
        
        # Display drone stats
        selected_drone = self.drones[self.drone_selection]
        stats_text = self.font.render(
            f"Weight: {self.drone_stats[selected_drone]['gravity']:.1f} | Power: {abs(self.drone_stats[selected_drone]['flap']):.1f}", 
            True, (200, 200, 200))
        self.screen.blit(stats_text, (self.WIDTH//2 - stats_text.get_width()//2, y_pos))
        
        # Display high score
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, (255, 215, 0))
        self.screen.blit(high_score_text, (self.WIDTH//2 - high_score_text.get_width()//2, 550))
    
    def draw_game_over(self):
        """Draw game over screen with score and achievements"""
        overlay = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Game Over text
        game_over_text = self.large_font.render("Game Over", True, (255, 0, 0))
        self.screen.blit(game_over_text, (self.WIDTH//2 - game_over_text.get_width()//2, 150))
        
        # Score display
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (self.WIDTH//2 - score_text.get_width()//2, 220))
        
        # Check if high score was beaten
        if self.score > self.high_score:
            new_high_text = self.font.render("New High Score!", True, (255, 215, 0))
            self.screen.blit(new_high_text, (self.WIDTH//2 - new_high_text.get_width()//2, 260))
        
        # Show unlocked achievements
        y_pos = 300
        achievement_title = self.font.render("Achievements:", True, (200, 200, 200))
        self.screen.blit(achievement_title, (self.WIDTH//2 - achievement_title.get_width()//2, y_pos))
        y_pos += 30
        
        for name, data in self.achievements.items():
            color = (0, 255, 0) if data["unlocked"] else (100, 100, 100)
            achievement_text = self.font.render(f"{name}: {data['description']}", True, color)
            self.screen.blit(achievement_text, (self.WIDTH//2 - achievement_text.get_width()//2, y_pos))
            y_pos += 30
        
        # Restart instructions
        restart_text = self.font.render("Press SPACE to restart or ESC for menu", True, (255, 255, 255))
        self.screen.blit(restart_text, (self.WIDTH//2 - restart_text.get_width()//2, 500))
    
    def run(self):
        """Main game loop"""
        running = True
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    if self.show_menu:
                        if event.key == pygame.K_SPACE:
                            self.show_menu = False
                            self.reset_game()
                            self.achievements["First Flight"]["unlocked"] = True
                        elif event.key == pygame.K_LEFT:
                            self.drone_selection = (self.drone_selection - 1) % len(self.drones)
                        elif event.key == pygame.K_RIGHT:
                            self.drone_selection = (self.drone_selection + 1) % len(self.drones)
                        elif event.key == pygame.K_ESCAPE:
                            running = False
                    
                    elif self.game_over:
                        if event.key == pygame.K_SPACE:
                            self.reset_game()
                        elif event.key == pygame.K_ESCAPE:
                            self.show_menu = True
                    
                    else:  # Active gameplay
                        if event.key == pygame.K_SPACE:
                            # Apply drone-specific flap strength
                            selected_drone = self.drones[self.drone_selection]
                            self.drone_vel_y = self.drone_stats[selected_drone]["flap"]
                            if self.sound_flap:
                                self.sound_flap.play()
                        elif event.key == pygame.K_ESCAPE:
                            self.show_menu = True
            
            # Show menu if needed
            if self.show_menu:
                self.draw_menu()
                pygame.display.flip()
                self.clock.tick(60)
                continue
            
            # Game over state
            if self.game_over:
                self.save_high_score()
                self.draw_game_over()
                pygame.display.flip()
                self.clock.tick(60)
                continue
            
            # Game physics updates
            selected_drone = self.drones[self.drone_selection]
            self.GRAVITY = self.drone_stats[selected_drone]["gravity"]
            
            # Apply physics
            self.drone_vel_y += self.GRAVITY
            
            # Apply wind from weather conditions
            self.drone_x += self.wind_force
            
            # Apply slow time effect
            time_factor = 0.5 if "slow_time" in self.active_power_ups else 1.0
            
            # Update drone position
            self.drone_y += self.drone_vel_y * time_factor
            
            # Update obstacles
            current_time = pygame.time.get_ticks()
            if current_time - self.last_obstacle_time > self.OBSTACLE_FREQUENCY * time_factor:
                self.spawn_obstacle()
                self.spawn_power_up()
                self.last_obstacle_time = current_time
            
            # Move obstacles
            for obstacle_set in self.obstacles[:]:
                # Move each obstacle in the set
                remove_set = True
                for obstacle in obstacle_set:
                    obstacle["x"] -= self.SCROLL_SPEED * time_factor
                    if obstacle["x"] > -50:  # Still on screen
                        remove_set = False
                
                # Remove obstacle set if all segments are off screen
                if remove_set:
                    self.obstacles.remove(obstacle_set)
            
            # Move power-ups
            for power_up in self.power_ups[:]:
                power_up["x"] -= self.SCROLL_SPEED * time_factor
                if power_up["x"] < -20:
                    self.power_ups.remove(power_up)
            
            # Check collisions
            self.check_collisions()
            
            # Update score
            self.update_score()
            
            # Update power-ups
            self.check_power_up_expiry()
            
            # Update particles
            self.update_particles()
            
            # Keep drone within bounds
            if self.drone_x < 0:
                self.drone_x = 0
            elif self.drone_x > self.WIDTH:
                self.drone_x = self.WIDTH
            
            # Drawing
            self.screen.fill(self.bg_color)
            
            # Draw particles
            self.draw_particles()
            
            # Draw game elements
            self.draw_obstacles()
            self.draw_power_ups()
            self.draw_drone()
            self.draw_hud()
            
            # Update display
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = FlightForge()
    game.run()