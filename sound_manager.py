import pygame
import math

class SoundManager:
    def __init__(self):
        # Initialize pygame mixer
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self.sound_enabled = True
        except pygame.error:
            print("Warning: Could not initialize sound system")
            self.sound_enabled = False
            return
        
        # Sound settings
        self.master_volume = 0.7
        self.sfx_volume = 0.8
        self.ambient_volume = 0.3
        
        # Simple sound storage
        self.sounds = {}
        self._create_simple_sounds()
        
        # Ambient sound control
        self.ambient_playing = False
        self.ambient_channel = None
    
    def _create_simple_sounds(self):
        """Create simple synthetic sounds without numpy"""
        if not self.sound_enabled:
            return
        
        sample_rate = 22050
        duration = 0.2  # 200ms sounds
        
        # Create simple beep sounds using pure Python
        try:
            # Startup sound - ascending beeps
            self.sounds['startup'] = self._create_beep_sequence([440, 880, 1320], sample_rate, 0.1)
            
            # Shutdown sound - descending beeps
            self.sounds['shutdown'] = self._create_beep_sequence([1320, 880, 440], sample_rate, 0.1)
            
            # Success sound - happy chord
            self.sounds['success'] = self._create_beep_sequence([523, 659, 784], sample_rate, 0.15)
            
            # Victory sound - triumph
            self.sounds['victory'] = self._create_beep_sequence([523, 659, 784, 1047], sample_rate, 0.2)
            
            # Simple beep
            self.sounds['beep'] = self._create_single_beep(800, sample_rate, 0.1)
            
            # Typing sound
            self.sounds['type'] = self._create_single_beep(1200, sample_rate, 0.05)
            
            # Error sound
            self.sounds['error'] = self._create_single_beep(200, sample_rate, 0.3)
            
        except Exception as e:
            print(f"Warning: Could not create sounds: {e}")
            self.sound_enabled = False
    
    def _create_single_beep(self, frequency, sample_rate, duration):
        """Create a single beep tone"""
        if not self.sound_enabled:
            return None
        
        try:
            frames = int(duration * sample_rate)
            arr = []
            
            for i in range(frames):
                # Generate sine wave
                time_point = float(i) / sample_rate
                wave = math.sin(2 * math.pi * frequency * time_point)
                
                # Apply envelope (fade in/out to avoid clicks)
                envelope = 1.0
                fade_frames = frames // 10  # 10% fade
                if i < fade_frames:
                    envelope = float(i) / fade_frames
                elif i > frames - fade_frames:
                    envelope = float(frames - i) / fade_frames
                
                # Convert to 16-bit signed integer
                sample = int(wave * envelope * 32767 * 0.3)  # Reduce volume
                arr.append([sample, sample])  # Stereo
            
            # Convert to bytes
            sound_bytes = b''
            for sample_pair in arr:
                for sample in sample_pair:
                    # Convert to 16-bit little-endian
                    sound_bytes += sample.to_bytes(2, 'little', signed=True)
            
            # Create sound from raw bytes
            sound = pygame.mixer.Sound(buffer=sound_bytes)
            return sound
            
        except Exception as e:
            print(f"Error creating beep: {e}")
            return None
    
    def _create_beep_sequence(self, frequencies, sample_rate, note_duration):
        """Create a sequence of beeps"""
        if not self.sound_enabled:
            return None
        
        try:
            total_frames = int(len(frequencies) * note_duration * sample_rate)
            frames_per_note = int(note_duration * sample_rate)
            arr = []
            
            for freq_index, frequency in enumerate(frequencies):
                start_frame = freq_index * frames_per_note
                
                for i in range(frames_per_note):
                    time_point = float(i) / sample_rate
                    wave = math.sin(2 * math.pi * frequency * time_point)
                    
                    # Apply envelope
                    envelope = 1.0
                    fade_frames = frames_per_note // 10
                    if i < fade_frames:
                        envelope = float(i) / fade_frames
                    elif i > frames_per_note - fade_frames:
                        envelope = float(frames_per_note - i) / fade_frames
                    
                    sample = int(wave * envelope * 32767 * 0.2)
                    arr.append([sample, sample])
            
            # Convert to bytes
            sound_bytes = b''
            for sample_pair in arr:
                for sample in sample_pair:
                    sound_bytes += sample.to_bytes(2, 'little', signed=True)
            
            sound = pygame.mixer.Sound(buffer=sound_bytes)
            return sound
            
        except Exception as e:
            print(f"Error creating beep sequence: {e}")
            return None
    
    def play_sound(self, sound_name):
        """Play a named sound effect"""
        if not self.sound_enabled:
            return
        
        if sound_name in self.sounds and self.sounds[sound_name]:
            try:
                channel = self.sounds[sound_name].play()
                if channel:
                    channel.set_volume(self.sfx_volume * self.master_volume)
            except pygame.error as e:
                print(f"Error playing sound {sound_name}: {e}")
    
    def stop_all_sounds(self):
        """Stop all currently playing sounds"""
        if self.sound_enabled:
            pygame.mixer.stop()
    
    def set_master_volume(self, volume):
        """Set master volume (0.0 to 1.0)"""
        self.master_volume = max(0.0, min(1.0, volume))
    
    def set_sfx_volume(self, volume):
        """Set sound effects volume (0.0 to 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
    
    def toggle_sound(self):
        """Toggle sound on/off"""
        self.sound_enabled = not self.sound_enabled
        if not self.sound_enabled:
            self.stop_all_sounds()
    
    def is_sound_enabled(self):
        """Check if sound is enabled"""
        return self.sound_enabled
    
    def play_ambient_sound(self, sound_name):
        """Play ambient sound on loop"""
        if not self.sound_enabled or sound_name not in self.sounds:
            return
        
        try:
            if self.ambient_channel:
                self.ambient_channel.stop()
            
            self.ambient_channel = self.sounds[sound_name].play(-1)  # Loop indefinitely
            if self.ambient_channel:
                self.ambient_channel.set_volume(self.ambient_volume * self.master_volume)
                self.ambient_playing = True
        except pygame.error as e:
            print(f"Error playing ambient sound: {e}")
    
    def stop_ambient_sound(self):
        """Stop ambient sound"""
        if self.ambient_channel:
            self.ambient_channel.stop()
            self.ambient_playing = False
    
    def cleanup(self):
        """Clean up sound resources"""
        if self.sound_enabled:
            self.stop_all_sounds()
            pygame.mixer.quit()