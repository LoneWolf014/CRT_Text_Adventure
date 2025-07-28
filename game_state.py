class GameState:
    def __init__(self):
        self.current_state = "main_menu"
        self.terminal_solved = False
        self.door_unlocked = False
        self.health = 100
        self.inventory = []
        self.game_flags = {}
        
        # Story progression tracking
        self.visited_locations = set()
        self.completed_puzzles = set()
        
    def change_state(self, new_state):
        """Change the current game state"""
        self.current_state = new_state
        self.visited_locations.add(new_state)
    
    def add_to_inventory(self, item):
        """Add an item to the inventory"""
        if item not in self.inventory:
            self.inventory.append(item)
    
    def remove_from_inventory(self, item):
        """Remove an item from the inventory"""
        if item in self.inventory:
            self.inventory.remove(item)
    
    def has_item(self, item):
        """Check if player has an item"""
        return item in self.inventory
    
    def set_flag(self, flag_name, value=True):
        """Set a game flag"""
        self.game_flags[flag_name] = value
    
    def get_flag(self, flag_name, default=False):
        """Get a game flag value"""
        return self.game_flags.get(flag_name, default)
    
    def show_inventory(self, text_manager):
        """Display inventory contents"""
        if not self.inventory:
            text_manager.add_game_message("Your inventory is empty.", "YELLOW")
        else:
            text_manager.add_game_message("INVENTORY:", "YELLOW")
            for item in self.inventory:
                text_manager.add_game_message(f"- {item.upper()}", "GREEN")
    
    def take_damage(self, amount):
        """Reduce health by amount"""
        self.health -= amount
        if self.health < 0:
            self.health = 0
    
    def heal(self, amount):
        """Increase health by amount"""
        self.health += amount
        if self.health > 100:
            self.health = 100
    
    def is_alive(self):
        """Check if player is still alive"""
        return self.health > 0
    
    def complete_puzzle(self, puzzle_name):
        """Mark a puzzle as completed"""
        self.completed_puzzles.add(puzzle_name)
    
    def is_puzzle_completed(self, puzzle_name):
        """Check if a puzzle has been completed"""
        return puzzle_name in self.completed_puzzles
    
    def get_state_info(self):
        """Get a dictionary of current state information"""
        return {
            'current_state': self.current_state,
            'health': self.health,
            'inventory_count': len(self.inventory),
            'terminal_solved': self.terminal_solved,
            'door_unlocked': self.door_unlocked,
            'visited_locations': len(self.visited_locations),
            'completed_puzzles': len(self.completed_puzzles)
        }