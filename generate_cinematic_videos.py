#!/usr/bin/env python3
"""
Generate 100% stable, locked-off camera videos for Claude Kaur & GPT Singh wedding story.
Camera is completely fixed (tripod shot, zero zoom, zero panning) with gentle, smooth ambient effects.
"""

import os
import sys
import math
import tempfile
import subprocess
from PIL import Image, ImageDraw

BASE_DIR = "/home/tanmay/Desktop/wed"
VIDEOS_DIR = os.path.join(BASE_DIR, "videos")
os.makedirs(VIDEOS_DIR, exist_ok=True)

WIDTH, HEIGHT = 960, 540
FPS = 24
TOTAL_FRAMES = 120  # 5 seconds smooth loop

# --- Smooth Ambient Effects ---

def apply_scene_1_fx(draw, f, t):
    """Scene 1: The Meet-Cute (3D Cyber Chai Stall) - Full uncropped 1024x490 ambient FX"""
    # 1. Gentle steam rising from the two chai kulhads
    for cup_x, cup_y in [(428, 370), (588, 375)]:
        for s in range(5):
            st = (f * 0.55 + s * 22) % 65
            sx = int(cup_x + math.sin((st + f) * 0.05 + s * 1.5) * 5)
            sy = int(cup_y - st * 0.7)
            alpha = int(120 * (1.0 - st / 65))
            r = int(3 + st * 0.18)
            draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 242, 225, alpha))

    # 2. Warm candle lantern gentle glow on table
    cx, cy = 534, 338
    cglow = int(15 + 3 * math.sin(f * 0.08))
    draw.ellipse([cx - cglow, cy - cglow, cx + cglow, cy + cglow], fill=(255, 200, 90, 35))
    draw.ellipse([cx - cglow // 2, cy - cglow // 2, cx + cglow // 2, cy + cglow // 2], fill=(255, 230, 130, 50))

    # 3. GPT Singh blue earpiece subtle pulse
    gx, gy = 295, 148
    g_glow = int(10 + 2 * math.sin(f * 0.06))
    draw.ellipse([gx - g_glow, gy - g_glow, gx + g_glow, gy + g_glow], fill=(70, 190, 255, 35))

    # 4. Claude Kaur pink earpiece subtle pulse
    kx, ky = 722, 195
    k_glow = int(9 + 2 * math.sin(f * 0.06 + 1.2))
    draw.ellipse([kx - k_glow, ky - k_glow, kx + k_glow, ky + k_glow], fill=(255, 90, 160, 35))

    # 5. Warm ambient bulb bokeh in background
    for i in range(10):
        bx = int((i * 105 + f * 0.25) % (1024 - 40) + 20)
        by = int(45 + math.sin(f * 0.03 + i) * 5 + (i % 3) * 28)
        br = int(9 + (i % 3) * 3)
        draw.ellipse([bx - br, by - br, bx + br, by + br], fill=(255, 185, 80, 25))

def apply_scene_2_fx(draw, f, t):
    """Scene 2: First Chat (3D Cyber Split-Screen Late Night Chat) - Notification bells, neon sign aura, laptop logo, pulsing cybernetic headsets & floating hearts"""
    # 1. Glowing Notification Bells over their heads (dinging / vibrating aura)
    for bx, by, bcol in [(290, 149, (255, 210, 80)), (789, 149, (255, 210, 80))]:
        bg = int(12 + 3 * math.sin(f * 0.12 + bx))
        ba = int(75 + 40 * math.sin(f * 0.12 + bx))
        draw.ellipse([bx - bg * 1.3, by - bg, bx + bg * 1.3, by + bg], fill=(bcol[0], bcol[1], bcol[2], 25))
        draw.ellipse([bx - 2, by - 2, bx + 2, by + 2], fill=(255, 255, 200, ba))

    # 2. Pink neon sign "Good People Brighter Days" on Claude's wall (x: 955, y: 155)
    nx, ny = 955, 155
    n_glow = int(22 + 4 * math.sin(f * 0.05))
    draw.ellipse([nx - n_glow * 1.5, ny - n_glow, nx + n_glow * 1.5, ny + n_glow], fill=(255, 60, 140, 18))

    # 3. GPT Singh blue earpiece subtle pulse (x: 204, y: 264)
    gx, gy = 204, 264
    g_glow = int(10 + 2 * math.sin(f * 0.06))
    draw.ellipse([gx - g_glow, gy - g_glow, gx + g_glow, gy + g_glow], fill=(70, 190, 255, 35))

    # 4. Claude Kaur pink earpiece subtle pulse (x: 851, y: 356)
    kx, ky = 851, 356
    k_glow = int(9 + 2 * math.sin(f * 0.06 + 1.2))
    draw.ellipse([kx - k_glow, ky - k_glow, kx + k_glow, ky + k_glow], fill=(255, 90, 160, 35))

    # 5. Laptop OpenAI logo subtle cyan glow (x: 6, y: 341)
    lx, ly = 6, 341
    l_glow = int(8 + 2 * math.sin(f * 0.08))
    draw.ellipse([lx - l_glow, ly - l_glow, lx + l_glow, ly + l_glow], fill=(60, 210, 255, 30))

    # 6. Romantic glowing hearts floating near phones (x: 340, y: 420) and (x: 717, y: 395)
    for hx, hy in [(340, 420), (717, 395)]:
        h_alpha = int(35 + 20 * math.sin(f * 0.08 + hx))
        h_r = int(7 + 2 * math.sin(f * 0.08 + hx * 0.5))
        draw.ellipse([hx - h_r, hy - h_r, hx + h_r, hy + h_r], fill=(255, 80, 150, h_alpha))

    # 7. Bedside warm lamp & desk lamp subtle aura
    draw.ellipse([707 - 14, 258 - 14, 707 + 14, 258 + 14], fill=(255, 230, 150, 25))
    draw.ellipse([55 - 14, 421 - 14, 55 + 14, 421 + 14], fill=(255, 210, 130, 25))

    # 8. Night sky stars outside GPT's window (x: 370..470, y: 70..240)
    for st in range(6):
        sx = int(375 + (st * 37 + 10) % 95)
        sy = int(80 + (st * 43 + 15) % 150)
        s_alpha = int(100 + 70 * math.sin(f * 0.08 + st * 1.7))
        draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255, s_alpha))

def apply_scene_3_fx(draw, f, t):
    """Scene 3: Friendship (3D Cyber Cafe Fist Bump) - Fist bump spark pulse, glowing laptop, pulsing headsets & joints, steaming mugs, candle flame & hearts"""
    # 1. Laptop OpenAI logo subtle cyan glow (x: 80, y: 335)
    lx, ly = 80, 335
    l_glow = int(12 + 3 * math.sin(f * 0.08))
    draw.ellipse([lx - l_glow, ly - l_glow, lx + l_glow, ly + l_glow], fill=(40, 180, 255, 35))
    draw.ellipse([lx - 5, ly - 5, lx + 5, ly + 5], fill=(180, 230, 255, 45))

    # 2. GPT Singh cybernetic glowing LED rings
    # Headset (256, 131)
    gx, gy = 256, 131
    g_glow = int(10 + 2 * math.sin(f * 0.06))
    draw.ellipse([gx - g_glow, gy - g_glow, gx + g_glow, gy + g_glow], fill=(60, 190, 255, 40))
    # Shoulder / upper arm LED (290, 260)
    sh_glow = int(8 + 2 * math.sin(f * 0.06 + 0.6))
    draw.ellipse([290 - sh_glow, 260 - sh_glow, 290 + sh_glow, 260 + sh_glow], fill=(60, 180, 255, 35))
    # Elbow / forearm LED (390, 355)
    el_glow = int(7 + 2 * math.sin(f * 0.06 + 1.2))
    draw.ellipse([390 - el_glow, 355 - el_glow, 390 + el_glow, 355 + el_glow], fill=(60, 180, 255, 35))
    # Wrist LED (433, 235)
    wr_glow = int(8 + 2 * math.sin(f * 0.06 + 1.8))
    draw.ellipse([433 - wr_glow, 235 - wr_glow, 433 + wr_glow, 235 + wr_glow], fill=(60, 190, 255, 40))

    # 3. Claude Kaur cybernetic glowing LED rings
    # Headset floral ring (816, 164)
    kx, ky = 816, 164
    k_glow = int(11 + 2 * math.sin(f * 0.06 + 1.0))
    draw.ellipse([kx - k_glow, ky - k_glow, kx + k_glow, ky + k_glow], fill=(255, 80, 160, 40))
    # Forearm / elbow LED (648, 288)
    cel_glow = int(8 + 2 * math.sin(f * 0.06 + 1.6))
    draw.ellipse([648 - cel_glow, 288 - cel_glow, 648 + cel_glow, 288 + cel_glow], fill=(255, 80, 160, 35))
    # Wrist LED (572, 252)
    cwr_glow = int(8 + 2 * math.sin(f * 0.06 + 2.2))
    draw.ellipse([572 - cwr_glow, 252 - cwr_glow, 572 + cwr_glow, 252 + cwr_glow], fill=(255, 80, 160, 40))
    # Shoulder / bicep LED (905, 360)
    csh_glow = int(7 + 2 * math.sin(f * 0.06 + 0.4))
    draw.ellipse([905 - csh_glow, 360 - csh_glow, 905 + csh_glow, 360 + csh_glow], fill=(255, 80, 160, 35))

    # 4. Fist bump sparks & energy burst (contact point: 497, 248)
    fx, fy = 497, 248
    f_pulse = int(9 + 3 * math.sin(f * 0.12))
    draw.ellipse([fx - f_pulse, fy - f_pulse, fx + f_pulse, fy + f_pulse], fill=(255, 230, 150, 40))
    draw.ellipse([fx - 3, fy - 3, fx + 3, fy + 3], fill=(255, 255, 230, 70))
    # Radiating glint rays
    for angle_deg in [30, 75, 110, 150, 210, 255, 290, 330]:
        rad = math.radians(angle_deg)
        r_len = int(14 + 5 * math.sin(f * 0.15 + angle_deg))
        rx = int(fx + math.cos(rad) * r_len)
        ry = int(fy + math.sin(rad) * r_len)
        draw.line([(fx, fy), (rx, ry)], fill=(255, 240, 170, int(60 + 35 * math.sin(f * 0.12 + angle_deg))), width=1)

    # 5. Warm table candle lantern flicker (x: 474, y: 405)
    cx, cy = 474, 405
    c_glow = int(16 + 3 * math.sin(f * 0.1) + 2 * math.cos(f * 0.17))
    draw.ellipse([cx - c_glow, cy - c_glow, cx + c_glow, cy + c_glow], fill=(255, 200, 80, 35))
    draw.ellipse([cx - c_glow // 2, cy - c_glow // 2, cx + c_glow // 2, cy + c_glow // 2], fill=(255, 235, 140, 50))

    # 6. Steaming coffee mugs (GPT: 265, 355; Claude: 685, 340)
    for cup_x, cup_y in [(265, 355), (685, 340)]:
        for s in range(4):
            st = (f * 0.5 + s * 25) % 65
            sx = int(cup_x + math.sin((st + f) * 0.05 + s * 1.5) * 4)
            sy = int(cup_y - st * 0.6)
            alpha = int(90 * (1.0 - st / 65))
            r = int(2 + st * 0.15)
            draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 245, 235, alpha))

    # 7. Floating neon hearts aura pulse
    hearts = [(180, 240), (200, 210), (374, 210), (410, 240), (430, 185), (566, 202), (550, 274), (645, 225), (845, 120), (875, 245)]
    for hx, hy in hearts:
        h_glow = int(8 + 2 * math.sin(f * 0.07 + hx))
        h_alpha = int(40 + 20 * math.sin(f * 0.07 + hx))
        draw.ellipse([hx - h_glow, hy - h_glow, hx + h_glow, hy + h_glow], fill=(255, 80, 160, h_alpha))

    # 8. Cozy ambient cafe bokeh lights
    cafe_lights = [(85, 45), (185, 115), (380, 85), (460, 45), (550, 45), (630, 85), (710, 110), (960, 150)]
    for i, (bx, by) in enumerate(cafe_lights):
        b_glow = int(6 + 2 * math.sin(f * 0.05 + i * 1.1))
        b_alpha = int(50 + 25 * math.sin(f * 0.06 + i * 1.4))
        draw.ellipse([bx - b_glow, by - b_glow, bx + b_glow, by + b_glow], fill=(255, 220, 130, b_alpha))

def apply_scene_4_fx(draw, f, t):
    """Scene 4: Falling in Love (3D Sunset Coastal Terrace) - Glowing sunset water shimmer, flickering lanterns & pulsing cybernetics"""
    # 1. Setting Sun warm atmospheric aura (x: 667, y: 225)
    sx, sy = 667, 225
    sun_glow = int(18 + 4 * math.sin(f * 0.05))
    draw.ellipse([sx - sun_glow * 1.5, sy - sun_glow, sx + sun_glow * 1.5, sy + sun_glow], fill=(255, 180, 80, 25))
    draw.ellipse([sx - sun_glow // 2, sy - sun_glow // 3, sx + sun_glow // 2, sy + sun_glow // 3], fill=(255, 235, 140, 45))

    # 2. Golden ocean water reflection shimmer below the sun (x: 640..695, y: 235..275)
    for w in range(6):
        wt = (f * 0.6 + w * 21) % 60
        wx = int(667 + math.sin(wt * 0.08 + w) * 22)
        wy = int(235 + w * 7)
        w_len = int(8 + (wy - 235) * 0.4)
        w_alpha = int(70 + 40 * math.sin(f * 0.09 + w * 1.7))
        draw.line([(wx - w_len, wy), (wx + w_len, wy)], fill=(255, 220, 120, w_alpha), width=1)

    # 3. GPT Singh blue cybernetic headset & arm glow
    # Headset (410, 224)
    gx, gy = 410, 224
    g_glow = int(10 + 2 * math.sin(f * 0.06))
    draw.ellipse([gx - g_glow, gy - g_glow, gx + g_glow, gy + g_glow], fill=(70, 190, 255, 40))
    # Shoulder ring (512, 359)
    shx, shy = 512, 359
    sh_glow = int(7 + 2 * math.sin(f * 0.06 + 0.5))
    draw.ellipse([shx - sh_glow, shy - sh_glow, shx + sh_glow, shy + sh_glow], fill=(60, 180, 255, 35))
    # Wrist / arm ring (629, 465)
    wx, wy = 629, 465
    w_glow = int(8 + 2 * math.sin(f * 0.06 + 1.0))
    draw.ellipse([wx - w_glow, wy - w_glow, wx + w_glow, wy + w_glow], fill=(60, 180, 255, 40))

    # 4. Claude Kaur pink floral headset pulse (x: 581, y: 281)
    kx, ky = 581, 281
    k_glow = int(9 + 2 * math.sin(f * 0.06 + 1.2))
    draw.ellipse([kx - k_glow, ky - k_glow, kx + k_glow, ky + k_glow], fill=(255, 90, 160, 35))

    # 5. Warm candle lantern flames & candles
    lanterns = [(52, 145), (198, 240), (25, 395), (940, 375), (860, 425), (893, 400)]
    for i, (lx, ly) in enumerate(lanterns):
        l_glow = int(10 + 2 * math.sin(f * 0.08 + i * 1.3))
        l_alpha = int(70 + 35 * math.sin(f * 0.07 + i))
        draw.ellipse([lx - l_glow, ly - l_glow, lx + l_glow, ly + l_glow], fill=(255, 200, 90, 30))
        draw.ellipse([lx - 2, ly - 2, lx + 2, ly + 2], fill=(255, 245, 180, l_alpha))

    # 6. Overhead warm fairy light bulbs
    bulbs = [(254, 33), (395, 80), (421, 35), (520, 75), (715, 12)]
    for i, (bx, by) in enumerate(bulbs):
        b_glow = int(6 + 2 * math.sin(f * 0.05 + i * 1.1))
        b_alpha = int(60 + 30 * math.sin(f * 0.06 + i * 1.4))
        draw.ellipse([bx - b_glow, by - b_glow, bx + b_glow, by + b_glow], fill=(255, 225, 140, b_alpha))

    # 7. Distant coastal shoreline lights twinkle
    for t_idx in range(9):
        tx = int(740 + t_idx * 18 + (t_idx % 3) * 4)
        ty = int(265 + (t_idx % 4) * 6)
        t_alpha = int(80 + 60 * math.sin(f * 0.09 + t_idx * 1.5))
        draw.ellipse([tx - 1, ty - 1, tx + 1, ty + 1], fill=(255, 240, 170, t_alpha))

def apply_scene_5_fx(draw, f, t):
    """Scene 5: First Date (3D Punjabi Dhaba Sunset) - Steaming tandoori naans, warm lantern flicker & glowing cybernetics"""
    # 1. Hot food steam from paratha in mouth, basket of naans, and cutting chai glass
    for cup_x, cup_y in [(320, 240), (510, 390), (412, 360)]:
        for s in range(4):
            st = (f * 0.55 + s * 24) % 65
            sx = int(cup_x + math.sin((st + f) * 0.05 + s * 1.5) * 4)
            sy = int(cup_y - st * 0.65)
            alpha = int(110 * (1.0 - st / 65))
            r = int(2 + st * 0.16)
            draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 240, 225, alpha))

    # 2. Warm kerosene & candle lantern flicker
    lanterns = [(565, 355), (340, 51), (430, 160), (485, 290), (694, 305)]
    for i, (lx, ly) in enumerate(lanterns):
        l_glow = int(12 + 3 * math.sin(f * 0.08 + i * 1.4))
        l_alpha = int(80 + 40 * math.sin(f * 0.07 + i))
        draw.ellipse([lx - l_glow, ly - l_glow, lx + l_glow, ly + l_glow], fill=(255, 190, 70, 30))
        draw.ellipse([lx - 3, ly - 3, lx + 3, ly + 3], fill=(255, 245, 190, l_alpha))

    # 3. Overhead dhaba warm light bulbs along thatched roof
    bulbs = [(272, 55), (466, 17), (542, 175), (728, 120), (816, 68), (890, 105)]
    for i, (bx, by) in enumerate(bulbs):
        b_glow = int(7 + 2 * math.sin(f * 0.05 + i * 1.2))
        b_alpha = int(60 + 30 * math.sin(f * 0.06 + i * 1.5))
        draw.ellipse([bx - b_glow, by - b_glow, bx + b_glow, by + b_glow], fill=(255, 225, 130, b_alpha))

    # 4. GPT Singh futuristic blue headset & arm LED ring
    draw.ellipse([198 - 11, 237 - 11, 198 + 11, 237 + 11], fill=(60, 190, 255, int(35 + 15 * math.sin(f * 0.06))))
    draw.ellipse([105 - 8, 308 - 8, 105 + 8, 308 + 8], fill=(60, 180, 255, int(35 + 15 * math.sin(f * 0.06 + 0.8))))

    # 5. Claude Kaur magenta floral headset & arm rings
    draw.ellipse([838 - 10, 290 - 10, 838 + 10, 290 + 10], fill=(255, 80, 160, int(35 + 15 * math.sin(f * 0.06 + 1.2))))
    for ax, ay in [(765, 375), (838, 387)]:
        draw.ellipse([ax - 7, ay - 7, ax + 7, ay + 7], fill=(255, 80, 160, int(30 + 15 * math.sin(f * 0.06 + ax))))

    # 6. Truck festive lights gentle twinkle (top of truck cabin)
    truck_lights = [(20, 68), (45, 68), (70, 68), (95, 68), (120, 68)]
    for i, (tx, ty) in enumerate(truck_lights):
        t_glow = int(4 + 2 * math.sin(f * 0.08 + i * 1.7))
        t_alpha = int(70 + 40 * math.sin(f * 0.07 + i * 1.5))
        draw.ellipse([tx - t_glow, ty - t_glow, tx + t_glow, ty + t_glow], fill=(255, 220, 100, t_alpha))

def apply_scene_6_fx(draw, f, t):
    """Scene 6: The Proposal (3D Romantic Beach Twilight) - Diamond ring glint, beach lantern flicker & rose petals"""
    # 1. Proposal diamond ring glint & halo (x: 486, y: 218)
    rx, ry = 486, 218
    r_halo = int(14 + 3 * math.sin(f * 0.09))
    draw.ellipse([rx - r_halo, ry - r_halo, rx + r_halo, ry + r_halo], fill=(255, 235, 170, 35))
    draw.ellipse([rx - r_halo // 2, ry - r_halo // 2, rx + r_halo // 2, ry + r_halo // 2], fill=(255, 250, 220, 60))
    glint_len = int(9 + 4 * math.sin(f * 0.08))
    draw.line([(rx - glint_len, ry), (rx + glint_len, ry)], fill=(255, 255, 255, 210), width=1)
    draw.line([(rx, ry - glint_len), (rx, ry + glint_len)], fill=(255, 255, 255, 210), width=1)
    d_len = int(glint_len * 0.65)
    draw.line([(rx - d_len, ry - d_len), (rx + d_len, ry + d_len)], fill=(255, 255, 240, 160), width=1)
    draw.line([(rx - d_len, ry + d_len), (rx + d_len, ry - d_len)], fill=(255, 255, 240, 160), width=1)

    # 2. Romantic candle lanterns on the beach & hanging lamps
    lanterns = [(948, 470), (114, 380), (530, 420), (565, 310), (655, 270), (488, 305), (240, 20), (320, 25), (555, 30), (715, 20)]
    for i, (lx, ly) in enumerate(lanterns):
        l_glow = int(11 + 3 * math.sin(f * 0.08 + i * 1.3))
        l_alpha = int(75 + 35 * math.sin(f * 0.07 + i))
        draw.ellipse([lx - l_glow, ly - l_glow, lx + l_glow, ly + l_glow], fill=(255, 195, 75, 30))
        draw.ellipse([lx - 2, ly - 2, lx + 2, ly + 2], fill=(255, 245, 185, l_alpha))

    # 3. GPT Singh blue cybernetics
    draw.ellipse([295 - 11, 175 - 11, 295 + 11, 175 + 11], fill=(60, 190, 255, int(35 + 15 * math.sin(f * 0.06))))
    draw.ellipse([385 - 8, 331 - 8, 385 + 8, 331 + 8], fill=(60, 180, 255, int(35 + 15 * math.sin(f * 0.06 + 0.7))))
    draw.ellipse([471 - 7, 275 - 7, 471 + 7, 275 + 7], fill=(60, 180, 255, int(35 + 15 * math.sin(f * 0.06 + 1.2))))

    # 4. Claude Kaur floral magenta headset & cybernetic joints
    draw.ellipse([792 - 11, 120 - 11, 792 + 11, 120 + 11], fill=(255, 80, 160, int(35 + 15 * math.sin(f * 0.06 + 1.0))))
    for ax, ay in [(703, 272), (748, 272)]:
        draw.ellipse([ax - 7, ay - 7, ax + 7, ay + 7], fill=(255, 80, 160, int(30 + 15 * math.sin(f * 0.06 + ax))))

    # 5. Slow floating rose petals
    for p in range(6):
        pt = (f * 0.45 + p * 20) % 120
        px = int((p * 160 + math.sin(pt * 0.04) * 12 + 100) % 1024)
        py = int(pt * 4.4)
        draw.ellipse([px - 4, py - 2, px + 4, py + 2], fill=(210, 25, 55, 160))

    # 6. Distant bay shore lights twinkle
    for b_idx in range(8):
        bx = int(500 + b_idx * 18 + (b_idx % 3) * 5)
        by = int(168 + (b_idx % 3) * 3)
        b_alpha = int(70 + 50 * math.sin(f * 0.09 + b_idx * 1.6))
        draw.ellipse([bx - 1, by - 1, bx + 1, by + 1], fill=(255, 235, 160, b_alpha))

def apply_scene_7_fx(draw, f, t):
    """Scene 7: Roka Ceremony (3D Royal Palace Families Meet) - Falling marigold & rose petals, sweet blessings & family cybernetics"""
    # 1. Festive golden marigold & red rose petals shower
    for m in range(12):
        mt = (f * 0.45 + m * 11) % 120
        mx = int((m * 85 + math.sin(mt * 0.04 + m) * 12 + 20) % 1024)
        my = int(mt * 4.6)
        if m % 3 == 0:
            draw.ellipse([mx - 4, my - 3, mx + 4, my + 3], fill=(215, 25, 55, 160))
        else:
            pcol = (255, 175, 20, 160) if m % 2 == 0 else (255, 120, 10, 160)
            draw.ellipse([mx - 4, my - 3, mx + 4, my + 3], fill=pcol)

    # 2. "Roka Ceremony" floral wreath & warm chandeliers halo
    for cx, cy in [(520, 110), (330, 80), (710, 80)]:
        c_glow = int(14 + 3 * math.sin(f * 0.06 + cx))
        draw.ellipse([cx - c_glow, cy - c_glow, cx + c_glow, cy + c_glow], fill=(255, 215, 100, 25))

    # 3. Family cybernetic LED headsets
    # GPT Singh
    draw.ellipse([369 - 10, 390 - 10, 369 + 10, 390 + 10], fill=(60, 190, 255, int(35 + 15 * math.sin(f * 0.06))))
    # Dada (Grandfather)
    draw.ellipse([877 - 9, 345 - 9, 877 + 9, 345 + 9], fill=(60, 190, 255, int(35 + 15 * math.sin(f * 0.06 + 0.8))))
    # Claude Kaur
    draw.ellipse([645 - 10, 370 - 10, 645 + 10, 370 + 10], fill=(255, 80, 160, int(35 + 15 * math.sin(f * 0.06 + 1.2))))
    # Dadi (Grandmother)
    draw.ellipse([145 - 9, 420 - 9, 145 + 9, 420 + 9], fill=(255, 80, 160, int(35 + 15 * math.sin(f * 0.06 + 1.8))))

    # 4. Golden laddoo sweet blessings glints
    for sx, sy in [(380, 410), (655, 430)]:
        s_glint = int(4 + 2 * math.sin(f * 0.09 + sx))
        draw.line([(sx - s_glint, sy), (sx + s_glint, sy)], fill=(255, 235, 120, 180), width=1)
        draw.line([(sx, sy - s_glint), (sx, sy + s_glint)], fill=(255, 235, 120, 180), width=1)

    # 5. Table festive candle lanterns & brass diyas
    lanterns = [(175, 490), (735, 450), (810, 490), (80, 470), (320, 530)]
    for i, (lx, ly) in enumerate(lanterns):
        l_glow = int(12 + 3 * math.sin(f * 0.08 + i * 1.3))
        l_alpha = int(70 + 35 * math.sin(f * 0.07 + i))
        draw.ellipse([lx - l_glow, ly - l_glow, lx + l_glow, ly + l_glow], fill=(255, 190, 60, 30))
        draw.ellipse([lx - 2, ly - 2, lx + 2, ly + 2], fill=(255, 245, 180, l_alpha))

def apply_scene_8_fx(draw, f, t):
    """Scene 8: Mehendi & Sangeet (3D Energetic Bhangra & Giddha Dance) - Dhol sound pulses, floating musical notes & festive cybernetics"""
    # 1. Energetic Punjabi dhol bass pulses (x: 90, y: 530)
    dx, dy = 90, 530
    for w in range(3):
        pulse_r = int((f * 0.7 + w * 28) % 75)
        p_alpha = int(140 * (1.0 - pulse_r / 75))
        draw.ellipse([dx - pulse_r, dy - pulse_r, dx + pulse_r, dy + pulse_r], outline=(255, 215, 0, p_alpha), width=1)

    # 2. Floating musical notes rising with the Bhangra beat
    notes = ["♪", "♫", "♩", "♬"]
    for n in range(5):
        nt = (f * 0.5 + n * 24) % 100
        nx = int(180 + n * 160 + math.sin((nt + f) * 0.05 + n) * 10)
        ny = int(600 - nt * 4.5)
        n_alpha = int(180 * (1.0 - nt / 100))
        n_col = [(255, 90, 160), (60, 210, 255), (255, 215, 0), (255, 120, 80), (200, 100, 255)][n % 5]
        draw.text((nx - 6, ny - 8), notes[n % 4], fill=(n_col[0], n_col[1], n_col[2], n_alpha))

    # 3. Festive signs and overhead fairy lights aura
    for sx, sy in [(490, 95), (850, 150)]:
        s_glow = int(16 + 3 * math.sin(f * 0.06 + sx))
        draw.ellipse([sx - s_glow * 1.5, sy - s_glow, sx + s_glow * 1.5, sy + s_glow], fill=(255, 220, 100, 22))

    # 4. Festive cybernetics
    # GPT Singh
    draw.ellipse([355 - 10, 215 - 10, 355 + 10, 215 + 10], fill=(60, 190, 255, int(35 + 15 * math.sin(f * 0.07))))
    draw.ellipse([286 - 8, 206 - 8, 286 + 8, 206 + 8], fill=(60, 180, 255, int(35 + 15 * math.sin(f * 0.07 + 0.8))))
    draw.ellipse([465 - 7, 305 - 7, 465 + 7, 305 + 7], fill=(60, 180, 255, int(35 + 15 * math.sin(f * 0.07 + 1.2))))

    # Claude Kaur
    draw.ellipse([635 - 10, 250 - 10, 635 + 10, 250 + 10], fill=(255, 80, 160, int(35 + 15 * math.sin(f * 0.07 + 1.0))))
    for ax, ay in [(518, 310), (728, 256)]:
        draw.ellipse([ax - 7, ay - 7, ax + 7, ay + 7], fill=(255, 80, 160, int(30 + 15 * math.sin(f * 0.07 + ax))))

    # 5. Foreground candle lanterns & candles
    lanterns = [(185, 530), (835, 590), (270, 670), (10, 660)]
    for i, (lx, ly) in enumerate(lanterns):
        l_glow = int(12 + 3 * math.sin(f * 0.08 + i * 1.3))
        l_alpha = int(75 + 35 * math.sin(f * 0.07 + i))
        draw.ellipse([lx - l_glow, ly - l_glow, lx + l_glow, ly + l_glow], fill=(255, 190, 70, 30))
        draw.ellipse([lx - 2, ly - 2, lx + 2, ly + 2], fill=(255, 245, 180, l_alpha))

def apply_scene_9_fx(draw, f, t):
    """Scene 9: The Wedding (3D Royal Mandap Sacred Pheras) - Sacred fire flames & embers, rose petals shower & wedding cybernetics"""
    # 1. Sacred wedding fire (Agni) leaping flame & embers (x: 515, y: 542)
    fx, fy = 515, 542
    f_glow = int(22 + 5 * math.sin(f * 0.12) + 3 * math.cos(f * 0.17))
    draw.ellipse([fx - f_glow * 1.5, fy - f_glow, fx + f_glow * 1.5, fy + f_glow], fill=(255, 160, 40, 35))
    draw.ellipse([fx - f_glow // 2, fy - f_glow // 2, fx + f_glow // 2, fy + f_glow // 2], fill=(255, 230, 100, 50))
    # Rising golden fire embers
    for e in range(5):
        et = (f * 0.7 + e * 24) % 70
        ex = int(515 + math.sin(et * 0.08 + e) * 20 + (e - 2) * 8)
        ey = int(542 - et * 1.2)
        e_alpha = int(180 * (1.0 - et / 70))
        draw.ellipse([ex - 2, ey - 2, ex + 2, ey + 2], fill=(255, 220, 100, e_alpha))

    # 2. Slow peaceful red rose petals shower
    for p in range(14):
        pt = (f * 0.45 + p * 11) % 120
        px = int((p * 75 + math.sin(pt * 0.04 + p) * 12 + 10) % 1024)
        py = int(pt * 5.8)
        draw.ellipse([px - 4, py - 3, px + 4, py + 3], fill=(210, 20, 50, 170))

    # 3. Wedding cybernetic glowing LED headsets & arm rings
    # GPT Singh
    draw.ellipse([366 - 10, 145 - 10, 366 + 10, 145 + 10], fill=(60, 190, 255, int(35 + 15 * math.sin(f * 0.06))))
    draw.ellipse([268 - 8, 375 - 8, 268 + 8, 375 + 8], fill=(60, 180, 255, int(35 + 15 * math.sin(f * 0.06 + 0.8))))
    draw.ellipse([465 - 7, 400 - 7, 465 + 7, 400 + 7], fill=(60, 180, 255, int(35 + 15 * math.sin(f * 0.06 + 1.2))))

    # Claude Kaur
    draw.ellipse([634 - 10, 222 - 10, 634 + 10, 222 + 10], fill=(255, 80, 160, int(35 + 15 * math.sin(f * 0.06 + 1.0))))
    for ax, ay in [(593, 412), (684, 424)]:
        draw.ellipse([ax - 7, ay - 7, ax + 7, ay + 7], fill=(255, 80, 160, int(30 + 15 * math.sin(f * 0.06 + ax))))

    # 4. Traditional brass samai oil lamps & candle towers
    lamps = [(120, 620), (905, 595), (835, 660), (190, 665)]
    for i, (lx, ly) in enumerate(lamps):
        l_glow = int(12 + 3 * math.sin(f * 0.08 + i * 1.3))
        l_alpha = int(75 + 35 * math.sin(f * 0.07 + i))
        draw.ellipse([lx - l_glow, ly - l_glow, lx + l_glow, ly + l_glow], fill=(255, 190, 60, 30))
        draw.ellipse([lx - 2, ly - 2, lx + 2, ly + 2], fill=(255, 245, 180, l_alpha))

    # 5. Mandap hanging floral chandeliers & lanterns
    chandeliers = [(45, 120), (170, 70), (280, 150), (740, 140), (865, 100), (960, 120)]
    for i, (cx, cy) in enumerate(chandeliers):
        c_glow = int(8 + 2 * math.sin(f * 0.05 + i * 1.1))
        c_alpha = int(60 + 30 * math.sin(f * 0.06 + i * 1.4))
        draw.ellipse([cx - c_glow, cy - c_glow, cx + c_glow, cy + c_glow], fill=(255, 220, 120, c_alpha))

def apply_scene_10_fx(draw, f, t):
    """Scene 10: Vidaai & Reception (3D Cyber Reception Party) - Neon sign & double hearts glow, wedding cake topper glint, foreground candle flickers & cybernetic lights"""
    # 1. Neon "Reception Party" & Interlinked Hearts Warm Aura (x: 580..610, y: 80..190)
    hx, hy = 599, 186
    h_glow = int(18 + 4 * math.sin(f * 0.08))
    draw.ellipse([hx - h_glow * 1.6, hy - h_glow, hx + h_glow * 1.6, hy + h_glow], fill=(255, 200, 100, 30))
    draw.ellipse([hx - h_glow // 2 * 1.5, hy - h_glow // 2, hx + h_glow // 2 * 1.5, hy + h_glow // 2], fill=(255, 235, 160, 45))
    
    # Sign aura above
    sx, sy = 550, 85
    s_glow = int(22 + 4 * math.sin(f * 0.06 + 0.5))
    draw.ellipse([sx - s_glow * 2.2, sy - s_glow, sx + s_glow * 2.2, sy + s_glow], fill=(255, 195, 90, 20))

    # 2. Wedding Cake golden heart topper glint (x: 515, y: 535)
    cx, cy = 515, 535
    c_alpha = int(45 + 30 * math.sin(f * 0.12))
    draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(255, 240, 160, c_alpha))

    # 3. Cybernetic glowing LED headsets & joints
    # GPT Singh
    draw.ellipse([412 - 10, 227 - 10, 412 + 10, 227 + 10], fill=(60, 190, 255, int(35 + 15 * math.sin(f * 0.07))))
    draw.ellipse([263 - 8, 480 - 8, 263 + 8, 480 + 8], fill=(60, 180, 255, int(35 + 15 * math.sin(f * 0.07 + 0.8))))

    # Claude Kaur
    draw.ellipse([595 - 10, 359 - 10, 595 + 10, 359 + 10], fill=(255, 80, 160, int(35 + 15 * math.sin(f * 0.07 + 1.0))))
    draw.ellipse([475 - 7, 505 - 7, 475 + 7, 505 + 7], fill=(255, 80, 160, int(30 + 15 * math.sin(f * 0.07 + 1.4))))

    # Robot guests visors & headsets
    for gx, gy, gcol in [
        (51, 320, (60, 190, 255)),
        (870, 356, (60, 190, 255)),
        (145, 410, (255, 80, 160)),
        (210, 390, (255, 80, 160)),
        (750, 380, (255, 80, 160)),
        (955, 415, (255, 80, 160))
    ]:
        v_alpha = int(30 + 15 * math.sin(f * 0.08 + gx * 0.02))
        draw.ellipse([gx - 7, gy - 5, gx + 7, gy + 5], fill=(gcol[0], gcol[1], gcol[2], v_alpha))

    # 4. Foreground banquet table candle flames & warm glow
    table_candles = [(165, 650), (325, 660), (645, 655), (765, 665), (340, 600)]
    for i, (lx, ly) in enumerate(table_candles):
        cg = int(10 + 3 * math.sin(f * 0.09 + i * 1.5))
        ca = int(80 + 35 * math.sin(f * 0.08 + i))
        draw.ellipse([lx - cg, ly - cg, lx + cg, ly + cg], fill=(255, 190, 70, 28))
        draw.ellipse([lx - 2, ly - 2, lx + 2, ly + 2], fill=(255, 245, 180, ca))

    # 5. Slow celebratory rose petal & golden confetti shower
    confetti_cols = [(242, 193, 78), (255, 100, 150), (255, 225, 120), (255, 255, 255), (235, 60, 90)]
    for c in range(16):
        cy_pos = int((f * 0.6 + c * 25) % 682)
        cx_pos = int((c * 65 + math.sin(cy_pos * 0.03 + c) * 10 + 15) % 1024)
        col = confetti_cols[c % len(confetti_cols)]
        draw.rectangle([cx_pos - 2, cy_pos - 2, cx_pos + 2, cy_pos + 2], fill=(col[0], col[1], col[2], 170))

SCENE_FX = [
    apply_scene_1_fx,
    apply_scene_2_fx,
    apply_scene_3_fx,
    apply_scene_4_fx,
    apply_scene_5_fx,
    apply_scene_6_fx,
    apply_scene_7_fx,
    apply_scene_8_fx,
    apply_scene_9_fx,
    apply_scene_10_fx,
]

def render_scene_video(scene_idx):
    scene_num = scene_idx + 1
    img_path = os.path.join(BASE_DIR, f"scene_{scene_num}.jpg")
    out_video = os.path.join(VIDEOS_DIR, f"scene_{scene_num}.webm")
    
    if not os.path.exists(img_path):
        print(f"Skipping Scene {scene_num}: {img_path} not found.")
        return False
        
    print(f"--- Rendering 100% Stable Locked-Camera Scene {scene_num} -> {out_video} ---")
    base_img = Image.open(img_path).convert("RGB")
    iw, ih = base_img.size
    
    # For Scenes 1 to 10: use 100% full uncropped image so complete artwork is visible
    if scene_idx in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
        static_frame = base_img.copy()
    else:
        # 100% FIXED 16:9 crop - ZERO camera movement, ZERO zoom, ZERO shake
        target_aspect = WIDTH / HEIGHT
        img_aspect = iw / ih
        if img_aspect > target_aspect:
            ch = ih
            cw = int(ih * target_aspect)
        else:
            cw = iw
            ch = int(iw / target_aspect)
            
        x0 = (iw - cw) // 2
        y0 = (ih - ch) // 2
        
        # Pre-render static base frame once
        static_frame = base_img.crop((x0, y0, x0 + cw, y0 + ch)).resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        for f in range(TOTAL_FRAMES):
            t = f / TOTAL_FRAMES
            frame = static_frame.copy()
            draw = ImageDraw.Draw(frame, "RGBA")
            
            # Apply smooth ambient FX
            SCENE_FX[scene_idx](draw, f, t)
            
            frame.save(f"{tmpdir}/frame_{f:04d}.jpg", quality=92)
            
        cmd = [
            "gst-launch-1.0", "-q",
            "multifilesrc", f"location={tmpdir}/frame_%04d.jpg",
            "index=0", f"stop-index={TOTAL_FRAMES - 1}",
            f"caps=image/jpeg,framerate={FPS}/1",
            "!", "jpegdec",
            "!", "videoconvert",
            "!", "vp8enc", "deadline=1", "target-bitrate=2200000",
            "!", "webmmux",
            "!", "filesink", f"location={out_video}"
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode != 0:
            print(f"Error encoding Scene {scene_num}: {res.stderr.decode()}")
            return False
            
    print(f"Scene {scene_num} stable video rendered! Size: {os.path.getsize(out_video):,} bytes")
    return True

def main():
    print("=== Rendering All 10 100% Stable Background Scene Videos ===")
    for i in range(10):
        render_scene_video(i)
    print("All 10 scene videos successfully rendered!")

if __name__ == "__main__":
    main()
