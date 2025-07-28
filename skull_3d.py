import math
import pygame

class Skull3D:
    def __init__(self):
        self.rotation_x = 0
        self.rotation_y = 0
        self.rotation_z = 0
        self.rotation_speed_x = 0.00
        self.rotation_speed_y = 0.03
        self.rotation_speed_z = 0.00
        
        # 3D skull vertices (simplified skull shape)
        self.original_vertices = [
            # Top of skull
            (0, -20, 0),     # 0 - top center
            (-10, -15, 5),   # 1 - top left front
            (10, -15, 5),    # 2 - top right front
            (-10, -15, -5),  # 3 - top left back
            (10, -15, -5),   # 4 - top right back
            
            # Upper skull
            (-15, -5, 8),    # 5 - left temple
            (15, -5, 8),     # 6 - right temple
            (-15, -5, -8),   # 7 - left back
            (15, -5, -8),    # 8 - right back
            
            # Eye sockets
            (-8, -2, 12),    # 9 - left eye outer
            (-4, -2, 12),    # 10 - left eye inner
            (4, -2, 12),     # 11 - right eye inner
            (8, -2, 12),     # 12 - right eye outer
            
            # Nose area
            (0, 2, 15),      # 13 - nose tip
            (-2, 0, 12),     # 14 - nose left
            (2, 0, 12),      # 15 - nose right
            
            # Jaw
            (-12, 8, 8),     # 16 - left jaw
            (12, 8, 8),      # 17 - right jaw
            (-8, 12, 10),    # 18 - left jaw lower
            (8, 12, 10),     # 19 - right jaw lower
            (0, 10, 12),     # 20 - jaw center
            
            # Teeth (simplified)
            (-6, 12, 12),    # 21 - left teeth
            (-2, 12, 12),    # 22 - center left teeth
            (2, 12, 12),     # 23 - center right teeth
            (6, 12, 12),     # 24 - right teeth
        ]
        
        # Define edges connecting vertices
        self.edges = [
            # Skull outline
            (0, 1), (0, 2), (0, 3), (0, 4),     # top connections
            (1, 2), (3, 4), (1, 3), (2, 4),     # top cross connections
            (1, 5), (2, 6), (3, 7), (4, 8),     # top to temple
            (5, 6), (7, 8), (5, 7), (6, 8),     # temple connections
            
            # Eye sockets
            (9, 10), (11, 12),                   # eye socket lines
            (5, 9), (10, 14), (11, 15), (6, 12), # eye to skull
            
            # Nose
            (13, 14), (13, 15), (14, 15),        # nose triangle
            
            # Jaw structure
            (5, 16), (6, 17),                    # temple to jaw
            (16, 17), (16, 18), (17, 19),        # jaw outline
            (18, 19), (18, 20), (19, 20),        # lower jaw
            
            # Teeth
            (20, 21), (21, 22), (22, 23), (23, 24), (24, 20),  # teeth line
            (18, 21), (19, 24),                  # teeth to jaw
        ]
        
        self.transformed_vertices = []
        self.font = pygame.font.SysFont("Courier", 12, bold=True)
        
        # Colors for different parts
        self.skull_color = (0, 255, 0)      # Green CRT color
        self.eye_color = (255, 50, 50)      # Red for eye sockets
        self.teeth_color = (255, 255, 50)   # Yellow for teeth
    
    def rotate_point_3d(self, point, rx, ry, rz):
        """Rotate a 3D point around all three axes"""
        x, y, z = point
        
        # Rotate around X axis
        cos_rx, sin_rx = math.cos(rx), math.sin(rx)
        y, z = y * cos_rx - z * sin_rx, y * sin_rx + z * cos_rx
        
        # Rotate around Y axis
        cos_ry, sin_ry = math.cos(ry), math.sin(ry)
        x, z = x * cos_ry + z * sin_ry, -x * sin_ry + z * cos_ry
        
        # Rotate around Z axis
        cos_rz, sin_rz = math.cos(rz), math.sin(rz)
        x, y = x * cos_rz - y * sin_rz, x * sin_rz + y * cos_rz
        
        return (x, y, z)
    
    def project_to_2d(self, point_3d, center_x, center_y, scale=3):
        """Project 3D point to 2D screen coordinates"""
        x, y, z = point_3d
        
        # Simple perspective projection
        distance = 50  # Distance from viewer
        factor = distance / (distance + z)
        
        screen_x = center_x + int(x * scale * factor)
        screen_y = center_y + int(y * scale * factor)
        
        return (screen_x, screen_y, z)  # Return z for depth sorting
    
    def update(self):
        """Update rotation angles"""
        self.rotation_x += self.rotation_speed_x
        self.rotation_y += self.rotation_speed_y
        self.rotation_z += self.rotation_speed_z
        
        # Keep rotations within 2π
        if self.rotation_x >= 2 * math.pi:
            self.rotation_x -= 2 * math.pi
        if self.rotation_y >= 2 * math.pi:
            self.rotation_y -= 2 * math.pi
        if self.rotation_z >= 2 * math.pi:
            self.rotation_z -= 2 * math.pi
        
        # Transform all vertices
        self.transformed_vertices = []
        for vertex in self.original_vertices:
            rotated = self.rotate_point_3d(vertex, self.rotation_x, self.rotation_y, self.rotation_z)
            self.transformed_vertices.append(rotated)
    
    def render(self, surface, center_x, center_y):
        """Render the 3D skull to the surface"""
        if not self.transformed_vertices:
            return
        
        # Project all vertices to 2D
        projected_vertices = []
        for vertex in self.transformed_vertices:
            projected = self.project_to_2d(vertex, center_x, center_y)
            projected_vertices.append(projected)
        
        # Sort edges by average depth for proper rendering order
        edge_depths = []
        for edge in self.edges:
            v1_idx, v2_idx = edge
            if v1_idx < len(projected_vertices) and v2_idx < len(projected_vertices):
                z1 = projected_vertices[v1_idx][2]
                z2 = projected_vertices[v2_idx][2]
                avg_depth = (z1 + z2) / 2
                edge_depths.append((edge, avg_depth))
        
        # Sort by depth (back to front)
        edge_depths.sort(key=lambda x: x[1])
        
        # Draw edges
        for edge, depth in edge_depths:
            v1_idx, v2_idx = edge
            if v1_idx < len(projected_vertices) and v2_idx < len(projected_vertices):
                x1, y1, z1 = projected_vertices[v1_idx]
                x2, y2, z2 = projected_vertices[v2_idx]
                
                # Choose color based on edge type
                color = self.skull_color
                
                # Eye socket edges
                if edge in [(9, 10), (11, 12)]:
                    color = self.eye_color
                
                # Teeth edges
                elif edge in [(20, 21), (21, 22), (22, 23), (23, 24), (24, 20)]:
                    color = self.teeth_color
                
                # Vary brightness based on depth
                depth_factor = max(0.3, 1.0 - abs(depth) / 30.0)
                adjusted_color = (
                    int(color[0] * depth_factor),
                    int(color[1] * depth_factor),
                    int(color[2] * depth_factor)
                )
                
                # Draw the line with anti-aliasing if possible
                try:
                    if abs(x2 - x1) > 1 or abs(y2 - y1) > 1:  # Only draw if points are different
                        pygame.draw.line(surface, adjusted_color, (x1, y1), (x2, y2), 2)
                except:
                    pass  # Skip invalid coordinates
        
        # Draw special features
        self._draw_eye_sockets(surface, projected_vertices)
        self._draw_skull_title(surface, center_x, center_y)
    
    def _draw_eye_sockets(self, surface, projected_vertices):
        """Draw filled eye sockets"""
        # Left eye socket
        if len(projected_vertices) > 10:
            left_eye_center = projected_vertices[9]  # Left eye outer
            x, y = int(left_eye_center[0]), int(left_eye_center[1])
            
            # Draw a small filled circle for the eye socket
            try:
                pygame.draw.circle(surface, (100, 0, 0), (x, y), 3)
            except:
                pass
        
        # Right eye socket
        if len(projected_vertices) > 12:
            right_eye_center = projected_vertices[12]  # Right eye outer
            x, y = int(right_eye_center[0]), int(right_eye_center[1])
            
            try:
                pygame.draw.circle(surface, (100, 0, 0), (x, y), 3)
            except:
                pass
    
    def _draw_skull_title(self, surface, center_x, center_y):
        """Draw a title below the skull"""
        title_text = "RETR0 SKULL"
        text_surface = self.font.render(title_text, True, (0, 150, 0))
        text_rect = text_surface.get_rect()
        text_rect.centerx = center_x
        text_rect.y = center_y + 60
        
        # Add some glow effect to the title
        glow_surface = self.font.render(title_text, True, (0, 50, 0))
        glow_rect = glow_surface.get_rect()
        glow_rect.centerx = center_x + 1
        glow_rect.y = center_y + 61
        
        surface.blit(glow_surface, glow_rect)
        surface.blit(text_surface, text_rect)
    
    def set_rotation_speed(self, speed_x, speed_y, speed_z):
        """Set custom rotation speeds"""
        self.rotation_speed_x = speed_x
        self.rotation_speed_y = speed_y
        self.rotation_speed_z = speed_z