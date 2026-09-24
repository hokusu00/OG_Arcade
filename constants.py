import pygame

# Screen Dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors (RGB)
COLOR_BG = (20, 20, 35)
COLOR_WHITE = (255, 255, 255)
COLOR_YELLOW = (255, 215, 0)
COLOR_RED = (230, 50, 50)
COLOR_GREEN = (50, 220, 100)
COLOR_CYAN = (0, 230, 230)
COLOR_GRAY = (100, 100, 120)

# Gameplay Constants
MAX_LIVES = 3
GAME_DURATION = 60  # seconds

# Item Types & Point Values
TYPE_TOKEN = "token"
TYPE_DIAMOND = "diamond"
TYPE_BOMB = "bomb"
TYPE_HEART = "heart"

ITEM_CONFIG = {
    TYPE_TOKEN: {"points": 10, "is_hazard": False, "is_heal": False, "penalize_miss": True, "color": COLOR_YELLOW},
    TYPE_DIAMOND: {"points": 25, "is_hazard": False, "is_heal": False, "penalize_miss": False, "color": COLOR_CYAN},
    TYPE_BOMB: {"points": 0, "is_hazard": True, "is_heal": False, "penalize_miss": False, "color": COLOR_RED},
    TYPE_HEART: {"points": 0, "is_hazard": False, "is_heal": True, "penalize_miss": False, "color": COLOR_GREEN},
}

# Bilingual Text Dictionary
TEXT = {
    "en": {
        "title": "OG ARCADE",
        "start": "Press [ENTER] to Start",
        "instructions": "Press [I] for Instructions",
        "lang_toggle": "Press [L] for Bahasa Melayu",
        "back": "Press [ESC] to Return to Menu",
        "paused": "GAME PAUSED - Press [P] to Resume",
        "game_over": "GAME OVER!",
        "victory": "STAGE CLEARED!",
        "score": "Score",
        "lives": "Lives",
        "time": "Time",
        "level": "Level",
        "restart": "Press [R] to Restart | [M] for Menu",
        "how_to_play": "HOW TO PLAY",
        "rule_1": "- Catch Tokens (+10 pts) and Diamonds (+25 pts)",
        "rule_2": "- Avoid Glitch Bombs (-1 Life)",
        "rule_3": "- Catch 1-UP Hearts to restore lives",
        "rule_4": "- Missing Tokens costs 1 Life!",
        "controls": "Controls: Left/Right Arrows to Move | P to Pause | R to Restart"
    },
    "ms": {
        "title": "ARKED OG",
        "start": "Tekan [ENTER] untuk Mula",
        "instructions": "Tekan [I] untuk Panduan",
        "lang_toggle": "Tekan [L] to switch to English",
        "back": "Tekan [ESC] untuk Kembali ke Menu",
        "paused": "PERMAINAN DIHENTIKAN - Tekan [P] untuk Sambung",
        "game_over": "PERMAINAN TAMAT!",
        "victory": "TAHAP SELESAI!",
        "score": "Skor",
        "lives": "Nyawa",
        "time": "Masa",
        "level": "Tahap",
        "restart": "Tekan [R] untuk Mula Semula | [M] untuk Menu",
        "how_to_play": "CARA BERMAIN",
        "rule_1": "- Tangkap Token (+10 mata) dan Berlian (+25 mata)",
        "rule_2": "- Elakkan Bom Glitch (-1 Nyawa)",
        "rule_3": "- Tangkap Hati 1-UP untuk pulihkan nyawa",
        "rule_4": "- Terlepas Token menolak 1 Nyawa!",
        "controls": "Kawalan: Kekunci Anak Panah Kiri/Kanan | P untuk Jeda | R untuk Mula Semula"
    }
}