class ASCIIManager:
    def __init__(self):
        self.current_sprite_key = "player_walk"
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_speed = 8  # Frames between animation updates
        
        # Enhanced ASCII art collection
        self.sprites = {
            "player_walk": [
                [
                    "    (o_o)    ",
                    "   <)   (>   ",
                    "    /|_|\\    ",
                    "     | |     ",
                    "    /   \\    "
                ],
                [
                    "    (O_O)    ",
                    "   <)   (>   ",
                    "    /| |\\    ",
                    "     |_|     ",
                    "    /   \\    "
                ],
                [
                    "    (°_°)    ",
                    "   <)   (>   ",
                    "    /|^|\\    ",
                    "     |_|     ",
                    "    /   \\    "
                ]
            ],
            
            "monitor": [
                [
                    "  .========================.",
                    "  |  [■]                  |",
                    "  |  |> _ SYSTEM READY    |",
                    "  |                       |",
                    "  |  ENTER PASSWORD:      |",
                    "  |  [________________]   |",
                    "  |                       |",
                    "  |  > RETR0 TERMINAL     |",
                    "  '======================='"
                ]
            ],
            
            "monitor_active": [
                [
                    "  .========================.",
                    "  |  [●]                  |",
                    "  |  |> █ SYSTEM ACTIVE   |",
                    "  |                       |",
                    "  |  PASSWORD ACCEPTED    |",
                    "  |  [████████████████]   |",
                    "  |                       |",
                    "  |  > ACCESS GRANTED     |",
                    "  '======================='"
                ]
            ],
            
            "door_closed": [
                [
                    "  +========================+",
                    "  |                        |",
                    "  |         [ # ]          |",
                    "  |                        |",
                    "  |          _|_           |",
                    "  |         / | \\          |",
                    "  |           |            |",
                    "  |      [LOCKED]          |",
                    "  |                        |",
                    "  +========================+"
                ]
            ],
            
            "door_open": [
                [
                    "         +========================+",
                    "        /|                        |",
                    "       / |                        |",
                    "      /  |                        |",
                    "     /   |       FREEDOM          |",
                    "    /    |                        |",
                    "   /     |        AWAITS          |",
                    "  /      |                        |",
                    " /       |                        |",
                    "+--------+========================+"
                ]
            ],
            
            "end_game_sprite": [
                [
                    "     (^_^)     ",
                    "    <)   (>    ",
                    "     /|★|\\     ",
                    "      |_|      ",
                    "     /   \\     ",
                    "               ",
                    "   VICTORY!    "
                ]
            ],
            
            "computer_terminal": [
                [
                    "    ┌─────────────────┐",
                    "    │ ████████████████ │",
                    "    │ █ MAINFRAME █ █  │",
                    "    │ ████████████████ │",
                    "    │                  │",
                    "    │ > LOGIN REQUIRED │",
                    "    │                  │",
                    "    └─────────────────┘"
                ]
            ],
            
            "robot_guard": [
                [
                    "     [●] [●]     ",
                    "       ╱─╲       ",
                    "      ╱   ╲      ",
                    "     ┌─────┐     ",
                    "     │█████│     ",
                    "     │█████│     ",
                    "     └─┬─┬─┘     ",
                    "       │ │       ",
                    "      ╱─ ─╲      "
                ]
            ],
            
            "keycard": [
                [
                    "  ┌──────────────┐",
                    "  │ ████         │",
                    "  │ ████ ACCESS  │",
                    "  │ ████ GRANTED │",
                    "  │ ████         │",
                    "  └──────────────┘"
                ]
            ],
            
            "warning_sign": [
                [
                    "     ▲▲▲▲▲▲▲     ",
                    "    ▲ DANGER ▲    ",
                    "   ▲ HIGH VOLT ▲   ",
                    "    ▲ DANGER ▲    ",
                    "     ▼▼▼▼▼▼▼     "
                ]
            ],
            
            "power_core": [
                [
                    "    ╔═══════════╗",
                    "    ║ ◆ POWER ◆ ║",
                    "    ║ ◆ CORE  ◆ ║",
                    "    ║ ◆◆◆◆◆◆◆ ║",
                    "    ║ ◆ ACTIVE ◆║",
                    "    ║ ◆◆◆◆◆◆◆ ║",
                    "    ╚═══════════╝"
                ]
            ],
            
            "glitch_sprite": [
                [
                    "    ▓▓░░▓▓░░    ",
                    "   ░▓▓░░▓▓░░▓   ",
                    "    ░▓▓▓▓▓▓░    ",
                    "     ░▓▓▓▓░     ",
                    "    ░▓░▓▓░▓░    "
                ],
                [
                    "    ░░▓▓░░▓▓    ",
                    "   ▓░░▓▓░░▓▓░   ",
                    "    ▓░░░░░░▓    ",
                    "     ▓░░░░▓     ",
                    "    ▓░▓░░▓░▓    "
                ]
            ]
        }
    
    def change_sprite(self, sprite_key):
        """Change the current sprite"""
        if sprite_key in self.sprites:
            self.current_sprite_key = sprite_key
            self.frame_index = 0
            self.frame_timer = 0
    
    def update(self):
        """Update animation frame"""
        self.frame_timer += 1
        
        if self.frame_timer >= self.frame_speed:
            self.frame_timer = 0
            
            # Only animate sprites that have multiple frames
            current_sprite_frames = self.sprites[self.current_sprite_key]
            if len(current_sprite_frames) > 1:
                self.frame_index = (self.frame_index + 1) % len(current_sprite_frames)
    
    def get_current_sprite(self):
        """Get the current sprite frame"""
        current_sprite_frames = self.sprites[self.current_sprite_key]
        return current_sprite_frames[self.frame_index]
    
    def get_sprite_by_name(self, sprite_name):
        """Get a specific sprite by name"""
        if sprite_name in self.sprites:
            return self.sprites[sprite_name][0]  # Return first frame
        return []
    
    def add_custom_sprite(self, name, frames):
        """Add a custom sprite to the collection"""
        self.sprites[name] = frames
    
    def list_available_sprites(self):
        """Get list of available sprite names"""
        return list(self.sprites.keys())
    
    def is_animated(self, sprite_name=None):
        """Check if a sprite is animated"""
        sprite_name = sprite_name or self.current_sprite_key
        if sprite_name in self.sprites:
            return len(self.sprites[sprite_name]) > 1
        return False
    
    def get_frame_count(self, sprite_name=None):
        """Get the number of frames in a sprite"""
        sprite_name = sprite_name or self.current_sprite_key
        if sprite_name in self.sprites:
            return len(self.sprites[sprite_name])
        return 0