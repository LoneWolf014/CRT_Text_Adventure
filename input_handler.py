import pygame

class InputHandler:
    def __init__(self):
        self.input_text = ""
        self.input_active = True
        self.use_red = False
        self.cursor_timer = 0
        self.cursor_visible = True
        self.cursor_blink_rate = 30  # Frames between cursor blinks
        
        # Command history
        self.command_history = []
        self.history_index = -1
        
        # Input validation
        self.max_input_length = 50
        
        # Color cycling
        self.color_cycle = ['GREEN', 'RED', 'BLUE', 'YELLOW', 'PURPLE', 'WHITE']
        self.current_color_index = 0
    
    def handle_event(self, event, game_state):
        """Handle input events and return processed command"""
        if not self.input_active:
            return None
        
        if event.type == pygame.KEYDOWN:
            # Handle special keys
            if event.key == pygame.K_RETURN:
                return self._process_input()
            
            elif event.key == pygame.K_BACKSPACE:
                if self.input_text:
                    self.input_text = self.input_text[:-1]
            
            elif event.key == pygame.K_SPACE:
                # Toggle text color
                if not self.input_text:  # Only if no text is being typed
                    self.use_red = not self.use_red
                    return None
                else:
                    self.input_text += " "
            
            elif event.key == pygame.K_TAB:
                # Show inventory - we'll return a command instead
                if not self.input_text:  # Only if no text is being typed
                    return ('inventory', 'inventory')
                return None
            
            elif event.key == pygame.K_UP:
                # Navigate command history up
                self._navigate_history_up()
            
            elif event.key == pygame.K_DOWN:
                # Navigate command history down
                self._navigate_history_down()
            
            elif event.key == pygame.K_ESCAPE:
                # Clear current input
                self.input_text = ""
                self.history_index = -1
            
            elif event.key == pygame.K_F1:
                # Cycle through colors
                self._cycle_color()
            
            else:
                # Handle regular character input
                if len(self.input_text) < self.max_input_length:
                    char = event.unicode
                    if char.isprintable() and char != ' ':
                        self.input_text += char
                    elif event.key == pygame.K_SPACE:
                        self.input_text += " "
    
    def _process_input(self):
        """Process the current input and return command"""
        if not self.input_text.strip():
            return None
        
        command_text = self.input_text.strip().lower()
        original_text = self.input_text.strip()
        
        # Add to command history
        if original_text and (not self.command_history or self.command_history[-1] != original_text):
            self.command_history.append(original_text)
            if len(self.command_history) > 20:  # Keep last 20 commands
                self.command_history.pop(0)
        
        # Reset input
        self.input_text = ""
        self.history_index = -1
        
        # Process special commands
        if command_text in ['quit', 'exit', 'q']:
            return ('exit', original_text)
        
        elif command_text in ['help', 'h', '?']:
            return ('help', original_text)
        
        elif command_text in ['inventory', 'inv', 'i']:
            return ('inventory', original_text)
        
        elif command_text in ['look', 'l', 'examine']:
            return ('look', original_text)
        
        elif command_text.startswith('password '):
            return (command_text, original_text)
        
        elif command_text in ['start', 'start journey', 'begin']:
            return ('start', original_text)
        
        elif command_text in ['use terminal', 'terminal', 'computer']:
            return ('use terminal', original_text)
        
        elif command_text in ['open door', 'door', 'use door']:
            return ('open door', original_text)
        
        elif command_text in ['use keycard', 'keycard']:
            return ('use keycard', original_text)
        
        # Return the command as-is if no special processing needed
        return (command_text, original_text)
    
    def _navigate_history_up(self):
        """Navigate up in command history"""
        if not self.command_history:
            return
        
        if self.history_index == -1:
            self.history_index = len(self.command_history) - 1
        elif self.history_index > 0:
            self.history_index -= 1
        
        if 0 <= self.history_index < len(self.command_history):
            self.input_text = self.command_history[self.history_index]
    
    def _navigate_history_down(self):
        """Navigate down in command history"""
        if not self.command_history or self.history_index == -1:
            return
        
        if self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.input_text = self.command_history[self.history_index]
        else:
            self.history_index = -1
            self.input_text = ""
    
    def _cycle_color(self):
        """Cycle through available colors"""
        self.current_color_index = (self.current_color_index + 1) % len(self.color_cycle)
    
    def get_current_color(self):
        """Get the current display color"""
        if self.use_red:
            return 'RED'
        return self.color_cycle[self.current_color_index]
    
    def update(self):
        """Update input handler (called each frame)"""
        # Update cursor blink
        self.cursor_timer += 1
        if self.cursor_timer >= self.cursor_blink_rate:
            self.cursor_timer = 0
            self.cursor_visible = not self.cursor_visible
    
    def render(self, surface, crt_renderer, content_height):
        """Render the input area"""
        if not self.input_active:
            return
        
        # Update cursor animation
        self.update()
        
        # Calculate input area position
        input_y = content_height + 20
        input_x = 20
        
        # Render input prompt
        prompt_text = "> "
        crt_renderer.render_text_with_effects(surface, prompt_text, (input_x, input_y), self.get_current_color())
        
        # Calculate text position after prompt - FIXED THIS LINE
        prompt_width = crt_renderer.font.size(prompt_text)[0]  # Use size() method instead of get_rect()
        text_x = input_x + prompt_width
        
        # Render input text
        display_text = self.input_text
        if self.cursor_visible and self.input_active:
            display_text += "_"
        
        crt_renderer.render_text_with_effects(surface, display_text, (text_x, input_y), self.get_current_color())
        
        # Render help text
        help_y = input_y + 35
        help_texts = [
            "Commands: look, help, inventory/inv, start, exit",
            "Special: SPACE=color, TAB=inventory, ↑↓=history, F1=cycle colors, ESC=clear"
        ]
        
        for i, help_text in enumerate(help_texts):
            crt_renderer.render_ui_text(surface, help_text, (input_x, help_y + i * 20), 'GRAY')
    
    def set_input_active(self, active):
        """Enable/disable input handling"""
        self.input_active = active
        if not active:
            self.input_text = ""
    
    def clear_input(self):
        """Clear current input text"""
        self.input_text = ""
        self.history_index = -1
    
    def get_command_history(self):
        """Get the command history list"""
        return self.command_history.copy()
    
    def add_command_to_history(self, command):
        """Manually add a command to history"""
        if command and (not self.command_history or self.command_history[-1] != command):
            self.command_history.append(command)
            if len(self.command_history) > 20:
                self.command_history.pop(0)