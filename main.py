import pgzrun
import pygame
import random

WIDTH = 960
HEIGHT = 600
TITLE = "Windows 7 Clicker Remastered v0.vibe.109 (dev build)"
FPS = 60
DEFAULT_FONT = "win7font.ttf"

intro_played = False

# --- Objetos ---
background = Actor("background.png", (WIDTH//2, HEIGHT//2))

animal = Actor("windows.png", (200, 330))
animal.scale = 0.60
animal_base_y = animal.y

bonus_1 = Actor("bonus.png", (700, 180))
bonus_2 = Actor("bonus.png", (700, 320))
bonus_3 = Actor("bonus.png", (700, 460))

bonus_1.scale = 1.3
bonus_2.scale = 1.3
bonus_3.scale = 1.3

# --- Variables ---
count = 0
click_value = 1

bonus_1_active = False
bonus_1_per_sec = 1
bonus_1_price = 15
bonus_1_owned = 0

bonus_2_active = False
bonus_2_per_sec = 15
bonus_2_price = 200
bonus_2_owned = 0

bonus_3_price = 100
bonus_3_owned = 0

hover_bonus_1 = False
hover_bonus_2 = False
hover_bonus_3 = False

particles = []

# --- CRÍTICOS ---
def aplicar_click():
    global count

    crit = random.random() < 0.1  # 10%

    if crit:
        gain = click_value * 5
    else:
        gain = click_value

    count += gain
    return gain, crit

# --- Bonus automático ---
def bonus_1_tick():
    global count
    count += bonus_1_per_sec

def bonus_2_tick():
    global count
    count += bonus_2_per_sec

# --- Update ---
def start_music():
    music.play("bgwin7")
    music.set_volume(0.5)
def update():
    global hover_bonus_1, hover_bonus_2, hover_bonus_3, intro_played

    if not intro_played:
        sounds.win7intro.play()
        intro_played = True

        # iniciar música después
        clock.schedule(start_music, 3.0)

    mouse_pos = pygame.mouse.get_pos()

    hover_bonus_1 = bonus_1.collidepoint(mouse_pos)
    hover_bonus_2 = bonus_2.collidepoint(mouse_pos)
    hover_bonus_3 = bonus_3.collidepoint(mouse_pos)

    bonus_1.scale = 1.4 if hover_bonus_1 else 1.3
    bonus_2.scale = 1.4 if hover_bonus_2 else 1.3
    bonus_3.scale = 1.4 if hover_bonus_3 else 1.3

    # partículas
    for p in particles:
        p["y"] -= 1
        p["life"] -= 1

    particles[:] = [p for p in particles if p["life"] > 0]

# --- Dibujar ---
def draw():
    screen.clear()
    background.draw()

    animal.draw()
    bonus_1.draw()
    bonus_2.draw()
    bonus_3.draw()

    # 💰 contador
    screen.draw.text(
        f"${int(count):,}",
        center=(animal.x, animal_base_y - 180),
        fontsize=90,
        color="white",
        fontname=DEFAULT_FONT
    )

    draw_bonus(bonus_1, "AUTO CLICKER", bonus_1_price, bonus_1_owned)
    draw_bonus(bonus_2, "SUPER CLICKER", bonus_2_price, bonus_2_owned)
    draw_bonus(bonus_3, "MULTI CLICK", bonus_3_price, bonus_3_owned)

    # ✨ partículas
    for p in particles:
        screen.draw.text(
            str(p["value"]),
            center=(p["x"], p["y"]),
            fontsize=30,
            color="yellow" if p["value"] == "CRIT!" else "white",
            fontname=DEFAULT_FONT
        )

    # watermark dev
    screen.draw.text(
        "PRIVATE DEV BUILD v0.vibe.109\nDO NOT DISTRIBUTE\nbuttons not final\nbuild date: 30/04/2026 3:09:48 AM UTC-6\n©️ 2026 https://github.com/AlexOrtega301",
        topright=(WIDTH - 10, 10),
        fontsize=10,
        color=(255, 255, 255, 120),
        fontname=DEFAULT_FONT
    )

# --- UI ---
def draw_bonus(actor, title, price, owned):
    spacing = 14
    base_x = actor.x
    base_y = actor.y - 20

    price_color = "red" if count < price else "black"

    screen.draw.text(title, center=(base_x, base_y), fontsize=15, color="black", fontname=DEFAULT_FONT)
    screen.draw.text(f"PRECIO: ${price:,}", center=(base_x, base_y + spacing), fontsize=10, color=price_color, fontname=DEFAULT_FONT)
    screen.draw.text(f"POSEÍDO: {owned}", center=(base_x, base_y + spacing*2), fontsize=8, color="darkgreen", fontname=DEFAULT_FONT)

# --- Clicks ---
def on_mouse_down(pos, button):
    global count, click_value
    global bonus_1_active, bonus_1_owned
    global bonus_2_active, bonus_2_owned
    global bonus_3_owned

    if button != mouse.LEFT:
        return

    # CLICK
    if animal.collidepoint(pos):
        gain, crit = aplicar_click()
        sounds.win7.play()

        particles.append({
            "x": animal.x,
            "y": animal.y - 100,
            "life": 40,
            "value": "CRIT!" if crit else f"+{gain}"
        })

        target_y = animal_base_y - 180

        def bajar():
            animate(animal, duration=0.35, tween="bounce_end", y=animal_base_y)

        animate(animal, duration=0.12, tween="accelerate", y=target_y, on_finished=bajar)

    # BONUS 1
    elif bonus_1.collidepoint(pos):
        if count >= bonus_1_price:
            count -= bonus_1_price
            bonus_1_owned += 1
            sounds.win7battery.play()

            if not bonus_1_active:
                clock.schedule_interval(bonus_1_tick, 2.0)
                bonus_1_active = True

    # BONUS 2
    elif bonus_2.collidepoint(pos):
        if count >= bonus_2_price:
            count -= bonus_2_price
            bonus_2_owned += 1
            sounds.win7battery.play()

            if not bonus_2_active:
                clock.schedule_interval(bonus_2_tick, 2.0)
                bonus_2_active = True

    # BONUS 3
    elif bonus_3.collidepoint(pos):
        if count >= bonus_3_price:
            count -= bonus_3_price
            bonus_3_owned += 1
            click_value += 1
            sounds.win7battery.play()

pgzrun.go()