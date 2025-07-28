import pygame
import random
import math

class CRTRenderer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("Courier", 24, bold=True)
        self.small_font = pygame.font.SysFont("Courier", 16, bold=True)
        
        # CRT effect parameters
        self.scanline_y_pos = 0
        self.scanline_speed = 3
        self.scanline_thickness = 2
        self.wiggle_amplitude = 1
        self.wiggle_timer = 0
        self.wiggle_update_interval = 8
        self.current_wiggle_offset_x = 0
        
        # Phosphor glow effect
        self.glow_intensity = 0.3
        self.glow_radius = 2
        
        # Screen curvature simulation
        self.curvature_strength = 0.02
        
        # Barrel distortion
        self.barrel_strength = 0.1
        
        # Color bleeding
        self.color_bleed_strength = 0.8
        
        # Surfaces for effects
        self.scanline_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.glow_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Static noise
        self.noise_intensity = 0.1
        self.noise_timer = 0
        
        # Screen flicker
        self.flicker_timer = 0
        self.flicker_intensity = 0.95
        
        # Color definitions
        self.colors = {
            'GREEN': (0, 255, 0),
            'RED': (255, 50, 50),
            'BLUE': (50, 150, 255),
            'YELLOW': (255, 255, 50),
            'PURPLE': (200, 50, 255),
            'WHITE': (255, 255, 255),
            'GRAY': (128, 128, 128)
        }
    
    def get_color(self, color_name):
        """Get color tuple from name"""
        return self.colors.get(color_name, self.colors['GREEN'])
    
    def apply_base_effects(self, surface):
        """Apply base CRT effects"""
        # Update wiggle offset
        self.wiggle_timer += 1
        if self.wiggle_timer >= self.wiggle_update_interval:
            self.wiggle_timer = 0
            self.current_wiggle_offset_x = random.randint(-self.wiggle_amplitude, self.wiggle_amplitude)
        
        # Update scanline position
        self.scanline_y_pos = (self.scanline_y_pos + self.scanline_speed) % (self.height + 20)
        
        # Update noise and flicker
        self.noise_timer += 1
        self.flicker_timer += 1
    
    def render_text_with_effects(self, surface, text, pos, color_name):
        """Render text with CRT effects"""
        x, y = pos
        color = self.get_color(color_name)
        
        # Apply wiggle offset
        x += self.current_wiggle_offset_x
        
        # Render multiple ghost layers for phosphor glow
        self._render_ghost_text(surface, text, (x, y), color)
    
    def _render_ghost_text(self, surface, text, pos, color):
        """Render text with phosphor glow effect"""
        x, y = pos
        
        # Primary ghost (medium intensity)
        ghost_color_1 = (color[0] // 3, color[1] // 3, color[2] // 3)
        ghost_1 = self.font.render(text, True, ghost_color_1)
        surface.blit(ghost_1, (x + 2, y + 2))
        
        # Secondary ghost (low intensity, wider)
        ghost_color_2 = (color[0] // 5, color[1] // 5, color[2] // 5)
        ghost_2 = self.font.render(text, True, ghost_color_2)
        surface.blit(ghost_2, (x + 4, y + 4))
        
        # Color bleeding effect
        if self.color_bleed_strength > 0:
            bleed_color = (min(255, int(color[0] * self.color_bleed_strength)), 
                          min(255, int(color[1] * self.color_bleed_strength)), 
                          min(255, int(color[2] * self.color_bleed_strength)))
            bleed_text = self.font.render(text, True, bleed_color)
            surface.blit(bleed_text, (x + 1, y))
            surface.blit(bleed_text, (x - 1, y))
        
        # Main text
        main_text = self.font.render(text, True, color)
        surface.blit(main_text, (x, y))
    
    def render_ascii_sprite(self, surface, sprite_lines, color_name):
        """Render ASCII sprite with effects"""
        if not sprite_lines:
            return
        
        color = self.get_color(color_name)
        
        # Calculate position (right side of screen)
        text_panel_width = self.width // 2
        sprite_panel_width = self.width - text_panel_width
        
        # Center the sprite - FIX: Use font.size() instead of font.get_rect()
        first_line_width = self.font.size(sprite_lines[0])[0]  # Returns (width, height)
        sprite_x = text_panel_width + (sprite_panel_width - first_line_width) // 2
        sprite_y = 80
        
        # Apply wiggle to sprite
        sprite_x += self.current_wiggle_offset_x
        
        # Render each line of the sprite
        for i, line in enumerate(sprite_lines):
            y_pos = sprite_y + i * 28
            self._render_ghost_text(surface, line, (sprite_x, y_pos), color)
    
    def render_ui_text(self, surface, text, pos, color_name):
        """Render UI text with smaller font"""
        x, y = pos
        color = self.get_color(color_name)
        
        # Simple render for UI elements
        ui_text = self.small_font.render(text, True, color)
        surface.blit(ui_text, (x, y))
    
    def apply_final_effects(self, surface):
        """Apply final CRT effects over everything"""
        # Apply scanlines
        self._apply_scanlines(surface)
        
        # Apply screen flicker
        self._apply_screen_flicker(surface)
        
        # Apply subtle noise
        self._apply_noise(surface)
        
        # Draw screen border/bezel
        self._draw_screen_border(surface)
    
    def _apply_scanlines(self, surface):
        """Apply moving scanline effect"""
        # Clear scanline surface
        self.scanline_surface.fill((0, 0, 0, 0))
        
        # Draw multiple horizontal scanlines
        for i in range(0, self.height, 4):
            alpha = 30 if i % 8 == 0 else 15
            scanline_color = (20, 20, 20, alpha)
            pygame.draw.line(self.scanline_surface, scanline_color, 
                           (0, i), (self.width, i), 1)
        
        # Draw the moving bright scanline
        moving_scanline_color = (40, 40, 40, 80)
        for thickness in range(self.scanline_thickness):
            y_pos = (self.scanline_y_pos + thickness) % self.height
            pygame.draw.line(self.scanline_surface, moving_scanline_color,
                           (0, y_pos), (self.width, y_pos), 1)
        
        # Blit scanlines to main surface
        surface.blit(self.scanline_surface, (0, 0))
    
    def _apply_screen_flicker(self, surface):
        """Apply subtle screen flicker"""
        if self.flicker_timer % 120 == 0:  # Flicker every 4 seconds at 30 FPS
            # Create a dark overlay
            flicker_surface = pygame.Surface((self.width, self.height))
            flicker_surface.fill((0, 0, 0))
            flicker_surface.set_alpha(int(255 * (1 - self.flicker_intensity)))
            surface.blit(flicker_surface, (0, 0))
    
    def _apply_noise(self, surface):
        """Apply subtle static noise"""
        if self.noise_timer % 3 == 0:  # Update noise every 3 frames
            noise_surface = pygame.Surface((self.width, self.height))
            noise_surface.set_alpha(int(255 * self.noise_intensity))
            
            # Generate random noise pixels
            for _ in range(50):  # 50 random noise pixels
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                brightness = random.randint(0, 255)
                noise_color = (brightness, brightness, brightness)
                noise_surface.set_at((x, y), noise_color)
            
            surface.blit(noise_surface, (0, 0))
    
    def _draw_screen_border(self, surface):
        """Draw a subtle screen border/bezel"""
        border_color = (30, 30, 30)
        pygame.draw.rect(surface, border_color, (0, 0, self.width, self.height), 2)
        
        # Draw panel separator
        panel_separator_x = self.width // 2
        pygame.draw.line(surface, border_color, 
                        (panel_separator_x, 0), (panel_separator_x, self.height - 100), 1)
    
    def update(self):
        """Update CRT effect timers"""
        # This method is called each frame to update effect timers
        pass