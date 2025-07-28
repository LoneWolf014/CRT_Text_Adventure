import pygame
from collections import deque

class TextManager:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("Courier", 20, bold=True)
        self.small_font = pygame.font.SysFont("Courier", 16, bold=True)
        
        # Text display settings
        self.text_area_width = width // 2  # Left half for text
        self.text_area_height = height - 120  # Reserve space for input
        self.line_height = 25
        self.max_lines = self.text_area_height // self.line_height
        
        # Message storage
        self.messages = deque(maxlen=self.max_lines)
        self.scroll_offset = 0
        
        # Text formatting
        self.margin_left = 20
        self.margin_top = 20
        
        # Text effects
        self.typewriter_mode = False
        self.typewriter_speed = 2  # Characters per frame
        self.current_message_chars = 0
        
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
    
    def add_game_message(self, text, color='GREEN'):
        """Add a game message with specified color"""
        self._add_message(text, color, 'GAME')
    
    def add_player_input(self, text, use_red=False):
        """Add player input to the message history"""
        color = 'RED' if use_red else 'YELLOW'
        self._add_message(f"> {text}", color, 'INPUT')
    
    def add_system_message(self, text):
        """Add a system message"""
        self._add_message(text, 'GRAY', 'SYSTEM')
    
    def _add_message(self, text, color, message_type):
        """Add a message to the display queue"""
        # Word wrap long messages
        wrapped_lines = self._wrap_text(text, self.text_area_width - 40)
        
        for line in wrapped_lines:
            message = {
                'text': line,
                'color': color,
                'type': message_type,
                'timestamp': pygame.time.get_ticks()
            }
            self.messages.append(message)
        
        # Auto-scroll to bottom when new message is added
        self.scroll_to_bottom()
    
    def _wrap_text(self, text, max_width):
        """Wrap text to fit within specified width"""
        words = text.split(' ')
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            test_surface = self.font.render(test_line, True, (255, 255, 255))
            
            if test_surface.get_width() <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                    current_line = word
                else:
                    # Word is too long, break it
                    lines.append(word)
                    current_line = ""
        
        if current_line:
            lines.append(current_line)
        
        return lines if lines else [text]
    
    def scroll_up(self):
        """Scroll text up"""
        if self.scroll_offset > 0:
            self.scroll_offset -= 1
    
    def scroll_down(self):
        """Scroll text down"""
        max_scroll = max(0, len(self.messages) - self.max_lines)
        if self.scroll_offset < max_scroll:
            self.scroll_offset += 1
    
    def scroll_to_bottom(self):
        """Scroll to the bottom of the text"""
        max_scroll = max(0, len(self.messages) - self.max_lines)
        self.scroll_offset = max_scroll
    
    def scroll_to_top(self):
        """Scroll to the top of the text"""
        self.scroll_offset = 0
    
    def clear_messages(self):
        """Clear all messages"""
        self.messages.clear()
        self.scroll_offset = 0
    
    def get_content_height(self):
        """Get the height of the content area"""
        return self.text_area_height
    
    def render(self, surface, crt_renderer):
        """Render all text messages"""
        if not self.messages:
            return
        
        # Calculate which messages to display
        start_index = self.scroll_offset
        end_index = min(start_index + self.max_lines, len(self.messages))
        
        # Render each visible message
        for i in range(start_index, end_index):
            message = self.messages[i]
            y_pos = self.margin_top + (i - start_index) * self.line_height
            
            # Apply text effects based on message type
            if message['type'] == 'INPUT':
                # Player input with slight indent
                x_pos = self.margin_left + 10
            else:
                x_pos = self.margin_left
            
            # Use CRT renderer for enhanced text effects
            crt_renderer.render_text_with_effects(
                surface, 
                message['text'], 
                (x_pos, y_pos), 
                message['color']
            )
        
        # Render scroll indicators
        self._render_scroll_indicators(surface, crt_renderer)
    
    def _render_scroll_indicators(self, surface, crt_renderer):
        """Render scroll indicators if needed"""
        if len(self.messages) > self.max_lines:
            # Show scroll position indicator
            total_messages = len(self.messages)
            visible_messages = min(self.max_lines, total_messages)
            
            # Calculate scroll bar position
            scroll_bar_height = max(20, (visible_messages / total_messages) * 100)
            scroll_bar_y = self.margin_top + (self.scroll_offset / total_messages) * 100
            
            # Draw scroll bar
            scroll_bar_x = self.text_area_width - 10
            pygame.draw.rect(surface, (50, 50, 50), 
                           (scroll_bar_x, self.margin_top, 5, 100))
            pygame.draw.rect(surface, (100, 100, 100), 
                           (scroll_bar_x, scroll_bar_y, 5, scroll_bar_height))
            
            # Show scroll indicators
            if self.scroll_offset > 0:
                crt_renderer.render_ui_text(surface, "↑ More", 
                                          (self.margin_left, self.margin_top - 15), 'GRAY')
            
            if self.scroll_offset < len(self.messages) - self.max_lines:
                bottom_y = self.margin_top + self.max_lines * self.line_height
                crt_renderer.render_ui_text(surface, "↓ More", 
                                          (self.margin_left, bottom_y), 'GRAY')
    
    def handle_scroll_input(self, event):
        """Handle scroll input events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                for _ in range(5):  # Scroll 5 lines at a time
                    self.scroll_up()
                return True
            elif event.key == pygame.K_PAGEDOWN:
                for _ in range(5):  # Scroll 5 lines at a time
                    self.scroll_down()
                return True
            elif event.key == pygame.K_HOME:
                self.scroll_to_top()
                return True
            elif event.key == pygame.K_END:
                self.scroll_to_bottom()
                return True
        
        return False
    
    def get_message_count(self):
        """Get the total number of messages"""
        return len(self.messages)
    
    def get_latest_message(self):
        """Get the most recent message"""
        return self.messages[-1] if self.messages else None
    
    def search_messages(self, search_term):
        """Search for messages containing the search term"""
        results = []
        for i, message in enumerate(self.messages):
            if search_term.lower() in message['text'].lower():
                results.append((i, message))
        return results
    
    def export_messages(self):
        """Export all messages as a list of strings"""
        return [msg['text'] for msg in self.messages]
    
    def set_typewriter_mode(self, enabled):
        """Enable or disable typewriter effect"""
        self.typewriter_mode = enabled
        self.current_message_chars = 0
    
    def update_typewriter(self):
        """Update typewriter effect"""
        if self.typewriter_mode and self.messages:
            self.current_message_chars += self.typewriter_speed