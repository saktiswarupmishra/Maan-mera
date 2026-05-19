import os
import sys
import time
import math
import random
import colorsys

if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')
    sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

try:
    import pygame
except ImportError:
    print("Installing Pygame...")
    os.system("pip install pygame")
    import pygame

SONG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "maan mera.mpeg")

def rgb_fg(r, g, b):
    return f"\033[38;2;{int(r)};{int(g)};{int(b)}m"

def hsv_to_rgb(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return (int(r * 255), int(g * 255), int(b * 255))

RESET = "\033[0m"
BOLD = "\033[1m"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"
CLEAR_SCREEN = "\033[2J\033[H"

CYBERPUNK_PINK = (255, 0, 128)
CYBERPUNK_CYAN = (0, 255, 255)
NEON_PURPLE = (178, 102, 255)
NEON_YELLOW = (255, 255, 0)
DIM_GRAY = (70, 70, 70)

LYRICS = [
    (0.0,   "Thode thode hosh madhoshi si hai", "vocal"),
    (5.0,   "Neend behoshi si hai", "vocal"),
    (9.0,   "Jaane kuchh bhi na mann mera", "vocal"),
    (15.0,  "Kabhi mera tha par ab begaana hai ye", "vocal"),
    (19.5,  "Deewana deewana samjhe na", "vocal"),
    (23.5,  "Ho... kabhi chup chup rahe kabhi gaaya ye kare", "highlight"),
    (27.5,  "Bin poochhe teri taareefein sunaya ye kare", "highlight"),
    (31.0,  "Hai koi haqeeqat tu ya koi fasana hai", "vocal"),
    (35.0,  "Kuchh jaane agar to itna ki ye tera deewana hai re...", "vocal"),
]

def format_time(seconds):
    m, s = divmod(int(seconds), 60)
    return f"{m}:{s:02d}"

def gradient_text(text, start_rgb, end_rgb):
    if not text: return ""
    length = len(text)
    res = ""
    for i, char in enumerate(text):
        if char == ' ':
            res += char
            continue
        ratio = i / max(length - 1, 1)
        r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio)
        g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio)
        b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio)
        res += f"\033[38;2;{r};{g};{b}m{char}"
    return res + RESET

def play_song():
    if not os.path.isfile(SONG_FILE):
        print(f"\n  ✘ Song file not found: {SONG_FILE}")
        sys.exit(1)
    
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=1024)
    pygame.mixer.init()
    pygame.mixer.music.load(SONG_FILE)

    sys.stdout.write(CLEAR_SCREEN + HIDE_CURSOR)
    
    lyric_index = 0
    song_duration = 37.0
    
    current_lyric = ""
    next_lyric = LYRICS[0][1] if len(LYRICS) > 0 else ""
    prev_lyric = ""
    future_lyric = LYRICS[1][1] if len(LYRICS) > 1 else ""
    lyric_start_time = 0.0
    lyric_end_time = 5.0

    eq_bands = []
    eq_peaks = []
    notes = []
    
    for _ in range(30):
        notes.append({
            "x": random.uniform(2, 70),
            "y": random.uniform(3, 15),
            "char": random.choice(["+", "✧", "⋆", "°", "·"]),
            "speed": random.uniform(0.02, 0.06),
            "color": hsv_to_rgb(random.uniform(0.5, 0.8), 0.5, 0.6)
        })
    
    pygame.mixer.music.play()

    try:
        while pygame.mixer.music.get_busy():
            pos_ms = pygame.mixer.music.get_pos()
            if pos_ms < 0:
                time.sleep(0.01)
                continue
            
            try:
                cols, rows = os.get_terminal_size()
            except:
                cols, rows = 80, 24
            
            UI_WIDTH = max(60, min(100, cols - 2))
            UI_HEIGHT = max(22, min(35, rows - 2))
            
            x_off = max(1, (cols - UI_WIDTH) // 2)
            y_off = max(1, (rows - UI_HEIGHT) // 2)
            
            output_buffer = []
            def print_at(lx, ly, text):
                if 0 <= ly < UI_HEIGHT and 0 <= lx < UI_WIDTH:
                    output_buffer.append(f"\033[{y_off + ly};{x_off + lx}H{text}")

            current_time = pos_ms / 1000.0
            
            # --- Lyric Advance Logic ---
            if lyric_index < len(LYRICS) and current_time >= LYRICS[lyric_index][0]:
                lyric_index += 1
                idx_curr = lyric_index - 1
                
                current_lyric = LYRICS[idx_curr][1]
                lyric_start_time = LYRICS[idx_curr][0]
                
                if lyric_index < len(LYRICS):
                    next_lyric = LYRICS[lyric_index][1]
                    lyric_end_time = LYRICS[lyric_index][0]
                else:
                    next_lyric = ""
                    lyric_end_time = lyric_start_time + 4.0
                    
                prev_lyric = LYRICS[idx_curr - 1][1] if idx_curr >= 1 else ""
                future_lyric = LYRICS[lyric_index + 1][1] if lyric_index + 1 < len(LYRICS) else ""

            # --- 1. Draw Border and Background ---
            pulse = (math.sin(current_time * 3) + 1) / 2
            b_col = rgb_fg(int(0 + pulse * 100), int(200 - pulse * 50), 255)
            
            top_border = "╭" + "━" * (UI_WIDTH - 2) + "╮"
            bottom_border = "╰" + "━" * (UI_WIDTH - 2) + "╯"
            print_at(0, 0, b_col + top_border)
            for y in range(1, UI_HEIGHT - 1):
                print_at(0, y, b_col + "┃")
                print_at(1, y, " " * (UI_WIDTH - 2)) # Clear inside
                print_at(UI_WIDTH - 1, y, b_col + "┃")
            print_at(0, UI_HEIGHT - 1, b_col + bottom_border)

            # --- 2. Header ---
            print_at(2, 1, rgb_fg(150, 150, 255) + BOLD + "♫ NOW PLAYING")
            rec_text = "● REC" if int(current_time * 2) % 2 == 0 else "○ REC"
            print_at(UI_WIDTH - 9, 1, rgb_fg(255, 50, 50) + rec_text)
            print_at(0, 2, b_col + "┠" + "─" * (UI_WIDTH - 2) + "┨" + RESET)

            # --- 3. Floating Particles ---
            for p in notes:
                p["y"] += p["speed"]
                if p["y"] > 12:
                    p["y"] = 3.0
                    p["x"] = random.uniform(2, UI_WIDTH - 3)
                
                px, py = int(p["x"]), int(p["y"])
                if not (4 <= py <= 8): # Keep lyrics clear
                    print_at(px, py, rgb_fg(*p["color"]) + p["char"])

            # --- 4. Lyrics Display ---
            duration_to_sing = min((lyric_end_time - lyric_start_time) * 0.75, len(current_lyric) * 0.12)
            duration_to_sing = max(duration_to_sing, 0.5)
            progress = max(0.0, min(1.0, (current_time - lyric_start_time) / duration_to_sing))

            if prev_lyric:
                lx = max(1, (UI_WIDTH - len(prev_lyric)) // 2)
                print_at(lx, 4, rgb_fg(80, 80, 80) + prev_lyric)
                
            if current_lyric:
                box_width = len(current_lyric) + 4
                bx = max(1, (UI_WIDTH - box_width) // 2)
                
                print_at(bx, 5, rgb_fg(100, 0, 200) + "╭" + "─" * (box_width - 2) + "╮")
                
                h_len = int(progress * len(current_lyric))
                highlighted = gradient_text(current_lyric[:h_len], CYBERPUNK_PINK, CYBERPUNK_CYAN)
                dim = rgb_fg(120, 120, 120) + current_lyric[h_len:]
                
                print_at(bx, 6, rgb_fg(100, 0, 200) + "│ " + BOLD + highlighted + dim + rgb_fg(100, 0, 200) + " │")
                print_at(bx, 7, rgb_fg(100, 0, 200) + "╰" + "─" * (box_width - 2) + "╯")

            if next_lyric:
                lx = max(1, (UI_WIDTH - len(next_lyric)) // 2)
                print_at(lx, 9, rgb_fg(80, 80, 80) + next_lyric)

            # --- 5. Title ---
            title_str = "✦   M A N N   M E R A   -   G A J E N D R A   V E R M A   ✦"
            tx = max(1, (UI_WIDTH - len(title_str)) // 2)
            print_at(tx, 11, BOLD + gradient_text(title_str, NEON_PURPLE, CYBERPUNK_CYAN))

            # --- 6. Massive Equalizer ---
            eq_start_y = 13
            eq_height = max(4, (UI_HEIGHT - 3) - eq_start_y)
            num_bands = UI_WIDTH - 4
            
            if len(eq_bands) != num_bands:
                eq_bands = [0.0] * num_bands
                eq_peaks = [0.0] * num_bands
                for p in notes: p["x"] = random.uniform(2, num_bands)

            bass = (math.sin(current_time * 12) + 1) / 2
            snare = (math.cos(current_time * 8) + 1) / 2
            
            for i in range(num_bands):
                pos = (i / num_bands) * 2 - 1.0
                energy = 0.0
                energy += bass * math.exp(-(pos * 4)**2) * 1.2
                energy += snare * math.exp(-(abs(pos) - 0.5)**2 * 10) * 0.8
                energy += random.uniform(0, 1.0) * math.exp(-(abs(pos) - 0.8)**2 * 20) * 0.6
                energy += (math.sin(current_time * 4 + pos * 5) + 1) * 0.2
                
                target = energy * 0.85
                
                if target > eq_bands[i]:
                    eq_bands[i] += (target - eq_bands[i]) * 0.7
                else:
                    eq_bands[i] -= 0.04
                    
                eq_bands[i] = max(0.0, min(1.0, eq_bands[i]))
                
                if eq_bands[i] > eq_peaks[i]:
                    eq_peaks[i] = eq_bands[i]
                else:
                    eq_peaks[i] -= 0.015

            chars = [" ", "▂", "▃", "▄", "▅", "▆", "▇", "█"]
            for l in range(eq_height):
                ratio = l / max(1, eq_height - 1)
                row_color = hsv_to_rgb(0.8 - ratio*0.3, 1.0, 1.0)
                c_str = rgb_fg(*row_color)
                
                row_str = ""
                for i in range(num_bands):
                    val = eq_bands[i]
                    scaled = int(val * eq_height * 8)
                    block_val = max(0, min(7, scaled - (eq_height - 1 - l) * 8))
                    
                    peak_scaled = int(eq_peaks[i] * eq_height * 8)
                    if block_val == 0 and (eq_height - 1 - l) * 8 <= peak_scaled < (eq_height - l) * 8:
                        row_str += rgb_fg(255, 255, 255) + "-" + c_str
                    else:
                        row_str += chars[block_val]
                
                print_at(2, eq_start_y + l, c_str + row_str)

            # --- 7. Progress Bar ---
            p_width = UI_WIDTH - 18
            p_prog = min(1.0, current_time / song_duration)
            filled = int(p_width * p_prog)
            empty = p_width - filled
            
            bar_fill = gradient_text("━" * filled, CYBERPUNK_PINK, CYBERPUNK_CYAN)
            bar_head = rgb_fg(255, 255, 255) + "⬤"
            bar_empty = rgb_fg(50, 50, 50) + "─" * empty
            
            t_curr = rgb_fg(200, 200, 200) + format_time(current_time)
            t_tot = rgb_fg(100, 100, 100) + format_time(song_duration)
            
            px = max(1, (UI_WIDTH - (p_width + 12)) // 2)
            print_at(px, UI_HEIGHT - 2, f"{t_curr} {bar_fill}{bar_head}{bar_empty} {t_tot}")

            sys.stdout.write("".join(output_buffer) + RESET)
            sys.stdout.flush()
            time.sleep(0.04)

    except KeyboardInterrupt:
        pygame.mixer.music.stop()
    
    finally:
        pygame.mixer.quit()
        sys.stdout.write(SHOW_CURSOR)
        sys.stdout.write(CLEAR_SCREEN)
        
        try:
            cols, rows = os.get_terminal_size()
        except:
            cols, rows = 80, 24
            
        msg = "Playback complete. Thank you for watching!"
        
        border_len = len(msg) + 8
        box_width = border_len
        box_height = 5
        
        start_x = max(1, (cols - box_width) // 2)
        start_y = max(1, (rows - box_height) // 2)
        
        output_buffer = []
        def end_print_at(lx, ly, text):
            output_buffer.append(f"\033[{ly};{lx}H{text}")
            
        b_color = rgb_fg(0, 255, 255)
        
        top_b = b_color + "╔" + "═" * (box_width - 2) + "╗" + RESET
        mid_empty = b_color + "║" + " " * (box_width - 2) + "║" + RESET
        mid_text = b_color + "║   " + gradient_text(msg, CYBERPUNK_PINK, CYBERPUNK_CYAN) + b_color + "   ║" + RESET
        bot_b = b_color + "╚" + "═" * (box_width - 2) + "╝" + RESET
        
        end_print_at(start_x, start_y, top_b)
        end_print_at(start_x, start_y + 1, mid_empty)
        end_print_at(start_x, start_y + 2, mid_text)
        end_print_at(start_x, start_y + 3, mid_empty)
        end_print_at(start_x, start_y + 4, bot_b)
        
        end_print_at(1, rows, "\n")
        sys.stdout.write("".join(output_buffer))
        sys.stdout.flush()

if __name__ == "__main__":
    play_song()
