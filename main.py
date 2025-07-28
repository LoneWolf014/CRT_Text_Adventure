import pygame
import sys
from game_state import GameState
from crt_effects import CRTRenderer
from ascii_art import ASCIIManager
from sound_manager import SoundManager
from input_handler import InputHandler
from text_manager import TextManager
from skull_3d import Skull3D

class CRTTextAdventure:
    def __init__(self):
        pygame.init()
        
        # Constants
        self.WIDTH, self.HEIGHT = 800, 600
        self.FPS = 30
        
        # Initialize pygame
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("CRT Text Adventure - Enhanced Edition")
        self.clock = pygame.time.Clock()
        
        # Initialize game components
        self.game_state = GameState()
        self.crt_renderer = CRTRenderer(self.WIDTH, self.HEIGHT)
        self.ascii_manager = ASCIIManager()
        self.sound_manager = SoundManager()
        self.input_handler = InputHandler()
        self.text_manager = TextManager(self.WIDTH, self.HEIGHT)
        self.skull_3d = Skull3D()
        
        # Game state
        self.running = True
        self.game_ending_countdown = -1
        
        # Initialize game
        self._initialize_game()
    
    def _initialize_game(self):
        """Initialize the game with welcome messages"""
        self.text_manager.add_game_message("WELCOME TO THE RETRO ADVENTURE", "YELLOW")
        self.text_manager.add_game_message("*******************************", "YELLOW")
        self.text_manager.add_game_message("You stand before the pixelated gate of destiny.", "GREEN")
        self.text_manager.add_game_message("Type 'start' or 'start journey' to begin.", "GREEN")
        self.text_manager.add_game_message("Type 'exit' to quit.", "GREEN")
        self.text_manager.add_game_message("Press SPACE to toggle text color.", "BLUE")
        self.text_manager.add_game_message("Press TAB for inventory.", "PURPLE")
    
    def handle_events(self):
        """Handle all pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            
            # Handle input events
            result = self.input_handler.handle_event(event, self.game_state)
            if result:
                command, input_text = result
                
                if command == 'exit':
                    self.text_manager.add_game_message("Closing...", "RED")
                    self.game_ending_countdown = self.FPS * 2
                    self.input_handler.input_active = False
                    self.sound_manager.play_sound('shutdown')
                else:
                    self._process_command(command, input_text)
    
    def _process_command(self, command, input_text):
        """Process game commands"""
        # Add player input to display
        self.text_manager.add_player_input(input_text, self.input_handler.use_red)
        
        # Get current state
        current_state = self.game_state.current_state
        
        # Process command based on current state
        if current_state == "main_menu":
            self._handle_main_menu_commands(command)
        elif current_state == "start":
            self._handle_start_commands(command)
        elif current_state == "terminal_prompt":
            self._handle_terminal_commands(command)
        elif current_state == "door_unlocked_state":
            self._handle_door_unlocked_commands(command)
        elif current_state == "end_game":
            pass  # No commands in end game
        
        # Play appropriate sound
        if command in ['look', 'use terminal', 'terminal']:
            self.sound_manager.play_sound('beep')
        elif command.startswith('password'):
            self.sound_manager.play_sound('type')
    
    def _handle_main_menu_commands(self, command):
        """Handle main menu commands"""
        if command in ['start', 'start journey']:
            self.text_manager.clear_messages()
            self.text_manager.add_game_message("The air is thick with static...", "GREEN")
            self.text_manager.add_game_message("A faint hum emanates from the archaic console before you.", "GREEN")
            self.text_manager.add_game_message("Type 'look' to observe your surroundings, or 'help' for assistance.", "GREEN")
            self.game_state.change_state("start")
            self.ascii_manager.change_sprite("door_closed")
            self.sound_manager.play_sound('startup')
        elif command == 'help':
            self.text_manager.add_game_message("Available commands: start, help, exit", "YELLOW")
        elif command == 'inventory' or command == 'inv':
            self.game_state.show_inventory(self.text_manager)
        else:
            self.text_manager.add_game_message(f"Command '{command}' not recognized.", "RED")
    
    def _handle_start_commands(self, command):
        """Handle start state commands"""
        if command == 'look':
            self.text_manager.add_game_message("You are in a dimly lit room. A rusty metal door is to your left.", "BLUE")
            self.text_manager.add_game_message("In front of you, a blinking TERMINAL sits on a dusty desk.", "BLUE")
        elif command in ['use terminal', 'terminal']:
            self.text_manager.add_game_message("The terminal screen flickers to life, asking for a PASSWORD.", "PURPLE")
            self.game_state.change_state("terminal_prompt")
            self.ascii_manager.change_sprite("monitor")
        elif command in ['open door', 'door']:
            self.text_manager.add_game_message("The door is bolted shut. It needs a key or a code.", "RED")
        elif command == 'help':
            self.text_manager.add_game_message("Try 'look' or 'use terminal'.", "YELLOW")
        elif command == 'inventory' or command == 'inv':
            self.game_state.show_inventory(self.text_manager)
        else:
            self.text_manager.add_game_message(f"Command '{command}' not recognized.", "RED")
    
    def _handle_terminal_commands(self, command):
        """Handle terminal state commands"""
        if command.startswith('password '):
            entered_password = command.split(' ', 1)[1]
            if entered_password == 'retr0':
                self.text_manager.add_game_message("Access granted. A soft click echoes from the door.", "BLUE")
                self.text_manager.add_game_message("You found a KEYCARD!", "YELLOW")
                self.game_state.terminal_solved = True
                self.game_state.door_unlocked = True
                self.game_state.add_to_inventory("keycard")
                self.game_state.change_state("door_unlocked_state")
                self.ascii_manager.change_sprite("door_open")
                self.sound_manager.play_sound('success')
            else:
                self.text_manager.add_game_message("Incorrect password. The terminal hums ominously.", "RED")
                self.game_state.health -= 5
                if self.game_state.health <= 0:
                    self.text_manager.add_game_message("The terminal overloads! Game Over.", "RED")
                    self.game_ending_countdown = self.FPS * 2
                else:
                    self.text_manager.add_game_message(f"Health: {self.game_state.health}/100", "YELLOW")
        elif command == 'look':
            self.text_manager.add_game_message("The terminal screen demands a password.", "BLUE")
        elif command == 'help':
            self.text_manager.add_game_message("Enter: 'password <your_guess>'", "YELLOW")
        elif command == 'inventory' or command == 'inv':
            self.game_state.show_inventory(self.text_manager)
        else:
            self.text_manager.add_game_message(f"Focus on the terminal. '{command}' won't help here.", "RED")
    
    def _handle_door_unlocked_commands(self, command):
        """Handle door unlocked state commands"""
        if command in ['open door', 'door', 'use keycard']:
            if 'keycard' in self.game_state.inventory:
                self.text_manager.add_game_message("The door creaks open, revealing blinding light...", "YELLOW")
                self.text_manager.add_game_message("You step through to victory!", "GREEN")
                self.game_state.change_state("end_game")
                self.ascii_manager.change_sprite("end_game_sprite")
                self.game_ending_countdown = self.FPS * 3
                self.input_handler.input_active = False
                self.sound_manager.play_sound('victory')
            else:
                self.text_manager.add_game_message("You need something to unlock the door.", "RED")
        elif command == 'look':
            self.text_manager.add_game_message("The door is now unlocked. Freedom awaits!", "BLUE")
        elif command == 'help':
            self.text_manager.add_game_message("Perhaps it's time to leave?", "YELLOW")
        elif command == 'inventory' or command == 'inv':
            self.game_state.show_inventory(self.text_manager)
        else:
            self.text_manager.add_game_message(f"You're almost free. What about '{command}'?", "PURPLE")
    
    def update(self):
        """Update game logic"""
        self.ascii_manager.update()
        self.crt_renderer.update()
        self.skull_3d.update()
        
        # Handle game ending countdown
        if self.game_ending_countdown > 0:
            self.game_ending_countdown -= 1
            if self.game_ending_countdown == 0:
                if self.game_state.current_state == "end_game":
                    self.text_manager.add_game_message("Thanks for playing the Enhanced CRT Adventure!", "YELLOW")
                    pygame.time.wait(2000)
                self.running = False
    
    def render(self):
        """Render everything to screen"""
        # Clear screen
        self.screen.fill((0, 0, 0))
        
        # Apply CRT base effects
        self.crt_renderer.apply_base_effects(self.screen)
        
        # Render text
        self.text_manager.render(self.screen, self.crt_renderer)
        
        # Render ASCII art
        current_sprite = self.ascii_manager.get_current_sprite()
        self.crt_renderer.render_ascii_sprite(self.screen, current_sprite, self.input_handler.get_current_color())
        
        # Render 3D skull on main menu
        if self.game_state.current_state == "main_menu":
            self.skull_3d.render(self.screen, self.WIDTH - 150, self.HEIGHT - 120)
        
        # Render input area
        self.input_handler.render(self.screen, self.crt_renderer, self.text_manager.get_content_height())
        
        # Render UI elements
        self._render_ui()
        
        # Apply final CRT effects
        self.crt_renderer.apply_final_effects(self.screen)
        
        # Update display
        pygame.display.flip()
    
    def _render_ui(self):
        """Render UI elements like health, inventory count, etc."""
        if self.game_state.current_state != "main_menu":
            # Health bar
            health_text = f"Health: {self.game_state.health}/100"
            self.crt_renderer.render_ui_text(self.screen, health_text, (10, 10), "GREEN")
            
            # Inventory count
            inv_count = len(self.game_state.inventory)
            inv_text = f"Items: {inv_count}"
            self.crt_renderer.render_ui_text(self.screen, inv_text, (10, 35), "BLUE")
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = CRTTextAdventure()
    game.run()