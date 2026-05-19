# 🚀 Cyberpunk Terminal Lyrics Player — "Maan Mera" Edition

Welcome to the **Cyberpunk Terminal Lyrics Player**! This is a highly visual, fully animated, true-color terminal-based music player. This edition is configured to play **"Maan Mera"** by *Gajendra Verma*, featuring a synchronized, cinematic lyric experience directly in your command line.

## ✨ Features & Visual Aesthetics

- **Cyberpunk Gradient Engine:** Custom-built per-character gradient engine that smoothly blends cyberpunk pinks, cyans, and neon purples across text in real-time.
- **Dynamic Equalizer:** A massive, reactive audio visualizer at the bottom of the screen that dynamically bounces based on calculated frequencies, simulating heavy bass and snares.
- **Synchronized Lyrics:** Lyrics are synced flawlessly to the audio. As the song plays, the current line is highlighted using an animated gradient fill while dimming sung parts, keeping you perfectly on beat.
- **Floating Particles:** Ambient neon particles (stars, pluses, dots) gently float upwards in the background, adding depth and a magical atmosphere to the terminal window.
- **Smooth Playback UI:** Includes a dynamic progress bar, playback timers, a pulsing "REC" indicator, and a beautifully structured boxed layout.
- **Flicker-Free Rendering:** Optimized terminal buffer updates ensure buttery smooth animations without screen tearing or flickering.

## 🛠️ Prerequisites

To run this project, you will need:
- **Python 3.6+** installed on your system.
- The **pygame** library for audio playback.

You can install the required library using pip:
```bash
pip install pygame
```

*Note: For Windows users, the script automatically reconfigures the console to support UTF-8 and ANSI escape sequences.*

## 🚀 How to Run

Ensure that the audio file `maan mera.mpeg` is located in the same directory as the script. Then, run the Python script directly from your terminal:

```bash
python lyrics_player.py
```

## 📂 Project Structure

- `lyrics_player.py`: The main script containing the rendering engine, UI layout, lyric timestamps, visualizers, and animation loops.
- `maan mera.mpeg`: The audio track used by the application.
- `README.md`: This documentation file.

## 🎨 Customization

You can personalize the player by editing `lyrics_player.py`:
- **Change the Song:** Update the `SONG_FILE` variable at the top of the file to point to your own `.mpeg` or `.mp3` file.
- **Update Lyrics:** Modify the `LYRICS` array with your new lyrics and timestamps to sync a different song.
- **Tweak Colors:** Explore and modify the `CYBERPUNK_PINK`, `CYBERPUNK_CYAN`, and `NEON_PURPLE` RGB tuples to create your own aesthetic themes.
- **Adjust Particles:** Change the particle characters, speed, and density in the `notes` list generation loop.

## 🐛 Troubleshooting

- **Terminal displays weird codes (e.g., `[38;2;...`):** Your terminal does not support true colors. Please use a modern terminal emulator like **Windows Terminal**, **iTerm2**, or **VS Code's integrated terminal**.
- **No Sound:** Ensure your volume is up and that the audio file `maan mera.mpeg` is located in the exact same folder as the script.

## 🎬 Credits

- **Song:** Maan Mera
- **Artist:** Gajendra Verma
- **Album:** Table No. 21

---
*Keep Creating... Keep Coding...*
