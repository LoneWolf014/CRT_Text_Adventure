﻿# CRT_Text_Adventure

A retro terminal-style text adventure engine built using Python and Pygame.

This isn’t a full game — it’s a design prototype to explore how early interactive fiction (like Zork) parsed text commands and created immersive gameplay without any graphics. I wanted to see how minimal UI, typed input, and atmospheric sound could still feel engaging.

> **Note:**  
> This project was built as part of my personal **AI-collab portfolio**, where I explored creative coding ideas with the help of ChatGPT and Claude. It’s vibe-coded — not production-ready — but a great learning experiment.

---

## Features

- Command parser with input history and shortcut support  
- Scrollable message log with retro CRT-style rendering  
- Procedural sound effects (beep, startup, error, typing)  
- Real-time 3D skull renderer (math-driven, no models)  
- Clean modular codebase: `InputHandler`, `GameState`, `TextManager`, `SoundManager`, etc.

---

## Requirements

- Python 3.9+  
- Pygame (`pip install pygame`)

---
