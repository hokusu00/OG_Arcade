import pygame
import random
import os
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, MAX_LIVES, GAME_DURATION,
    TYPE_TOKEN, TYPE_DIAMOND, TYPE_BOMB, TYPE_HEART, TEXT
)
from player import Player
from item import Item


class GameManager:
    def __init__(self):
        self.STATE_MENU = "menu"
        self.STATE_INSTRUCTIONS = "instructions"
        self.STATE_PLAYING = "playing"
        self.STATE_GAMEOVER = "game_over"
        self.current_state = self.STATE_MENU
        self.lang = "en"

        self.score = 0
        self.lives = MAX_LIVES
        self.level = 1
        self.multiplier = 1
        self.streak_count = 0
        self.start_ticks = 0
        self.time_left = GAME_DURATION

        # Setup Audio
        pygame.mixer.init()
        self.catch_sound = self.load_sound("assets/sounds/catch.wav")
        self.miss_sound = self.load_sound("assets/sounds/miss.wav")
        self.game_over_sound = self.load_sound("assets/sounds/game_over.wav")

        # Setup Background
        self.background = None
        if os.path.exists("assets/images/background.png"):
            bg = pygame.image.load("assets/images/background.png")
            self.background = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.all_sprites = pygame.sprite.Group()
        self.item_group = pygame.sprite.Group()

        # Setup Player Image
        player_img = None
        if os.path.exists("assets/images/player.png"):
            player_img = pygame.image.load("assets/images/player.png")
        self.player = Player(image=player_img)
        self.all_sprites.add(self.player)

        self.spawn_timer = 0
        self.spawn_interval = 45

        self.font_title = pygame.font.SysFont("Arial", 42, bold=True)
        self.font_large = pygame.font.SysFont("Arial", 28, bold=True)
        self.font_medium = pygame.font.SysFont("Arial", 20, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 16)

    def load_sound(self, path):
        if os.path.exists(path):
            return pygame.mixer.Sound(path)
        return None

    def play_sound(self, sound_obj):
        if sound_obj:
            sound_obj.play()

    def start_game(self):
        self.score = 0
        self.lives = MAX_LIVES
        self.level = 1
        self.multiplier = 1
        self.streak_count = 0
        self.time_left = GAME_DURATION
        for item in self.item_group:
            item.kill()
        self.player.reset_position()
        self.start_ticks = pygame.time.get_ticks()
        self.current_state = self.STATE_PLAYING

    def toggle_language(self):
        self.lang = "ms" if self.lang == "en" else "en"

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_l:
                self.toggle_language()
            if self.current_state == self.STATE_MENU:
                if event.key == pygame.K_RETURN:
                    self.start_game()
                elif event.key == pygame.K_i:
                    self.current_state = self.STATE_INSTRUCTIONS
                elif event.key == pygame.K_ESCAPE:
                    return False
            elif self.current_state == self.STATE_INSTRUCTIONS:
                if event.key == pygame.K_ESCAPE:
                    self.current_state = self.STATE_MENU
            elif self.current_state == self.STATE_PLAYING:
                if event.key == pygame.K_p:
                    self.current_state = "paused"
                elif event.key == pygame.K_r:
                    self.start_game()
                elif event.key == pygame.K_m:
                    self.current_state = self.STATE_MENU
            elif self.current_state == "paused":
                if event.key == pygame.K_p:
                    self.current_state = self.STATE_PLAYING
                elif event.key == pygame.K_m:
                    self.current_state = self.STATE_MENU
            elif self.current_state == self.STATE_GAMEOVER:
                if event.key == pygame.K_r:
                    self.start_game()
                elif event.key == pygame.K_m:
                    self.current_state = self.STATE_MENU
        return True

    def update(self):
        if self.current_state != self.STATE_PLAYING:
            return

        seconds_passed = (pygame.time.get_ticks() - self.start_ticks) // 1000
        self.time_left = max(0, GAME_DURATION - seconds_passed)

        if self.time_left <= 0:
            self.current_state = self.STATE_GAMEOVER
            self.play_sound(self.game_over_sound)
            return

        if self.time_left > 40:
            self.level = 1
            base_speed = 4
            self.spawn_interval = 45
        elif self.time_left > 20:
            self.level = 2
            base_speed = 6
            self.spawn_interval = 35
        else:
            self.level = 3
            base_speed = 8
            self.spawn_interval = 25

        keys = pygame.key.get_pressed()
        self.player.update(keys)

        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            rand_val = random.random()
            if rand_val < 0.55:
                item_type = TYPE_TOKEN
            elif rand_val < 0.75:
                item_type = TYPE_DIAMOND
            elif rand_val < 0.90:
                item_type = TYPE_BOMB
            else:
                item_type = TYPE_HEART

            item_speed = random.randint(base_speed, base_speed + 3)

            # Setup Item Image
            item_img = None
            img_path = f"assets/images/{item_type}.png"
            if os.path.exists(img_path):
                item_img = pygame.image.load(img_path)

            new_item = Item(item_type, item_speed, image=item_img)
            self.item_group.add(new_item)
            self.all_sprites.add(new_item)

        for item in self.item_group:
            item.update()
            if item.is_off_screen():
                if item.penalize_miss:
                    self.lives -= 1
                    self.play_sound(self.miss_sound)
                    self.streak_count = 0
                    self.multiplier = 1
                    if self.lives <= 0:
                        self.current_state = self.STATE_GAMEOVER
                        self.play_sound(self.game_over_sound)
                item.kill()

        caught_items = pygame.sprite.spritecollide(self.player, self.item_group, True)
        for item in caught_items:
            if item.is_hazard:
                self.lives -= 1
                self.play_sound(self.miss_sound)
                self.streak_count = 0
                self.multiplier = 1
                if self.lives <= 0:
                    self.current_state = self.STATE_GAMEOVER
                    self.play_sound(self.game_over_sound)
            elif item.is_heal:
                self.lives = min(MAX_LIVES, self.lives + 1)
                self.play_sound(self.catch_sound)
            else:
                self.streak_count += 1
                if self.streak_count >= 5:
                    self.multiplier = 3
                elif self.streak_count >= 3:
                    self.multiplier = 2
                else:
                    self.multiplier = 1
                self.score += item.points * self.multiplier
                self.play_sound(self.catch_sound)

    def render(self, screen):
        t = TEXT[self.lang]

        if self.current_state == self.STATE_MENU:
            screen.fill((20, 20, 35))
            title_surf = self.font_title.render(t["title"], True, (0, 230, 230))
            start_surf = self.font_large.render(t["start"], True, (255, 255, 255))
            inst_surf = self.font_medium.render(t["instructions"], True, (255, 215, 0))
            lang_surf = self.font_medium.render(t["lang_toggle"], True, (50, 220, 100))
            screen.blit(title_surf, (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 160))
            screen.blit(start_surf, (SCREEN_WIDTH // 2 - start_surf.get_width() // 2, 280))
            screen.blit(inst_surf, (SCREEN_WIDTH // 2 - inst_surf.get_width() // 2, 350))
            screen.blit(lang_surf, (SCREEN_WIDTH // 2 - lang_surf.get_width() // 2, 410))

        elif self.current_state == self.STATE_INSTRUCTIONS:
            screen.fill((20, 20, 35))
            head_surf = self.font_title.render(t["how_to_play"], True, (255, 215, 0))
            screen.blit(head_surf, (SCREEN_WIDTH // 2 - head_surf.get_width() // 2, 100))
            rules = [t["rule_1"], t["rule_2"], t["rule_3"], t["rule_4"], t["controls"]]
            for i, rule in enumerate(rules):
                r_surf = self.font_medium.render(rule, True, (255, 255, 255))
                screen.blit(r_surf, (80, 200 + (i * 45)))
            back_surf = self.font_small.render(t["back"], True, (150, 150, 180))
            screen.blit(back_surf, (SCREEN_WIDTH // 2 - back_surf.get_width() // 2, 500))

        elif self.current_state in [self.STATE_PLAYING, "paused"]:
            if self.background:
                screen.blit(self.background, (0, 0))
            else:
                screen.fill((25, 25, 45))

            self.all_sprites.draw(screen)

            score_txt = f"{t['score']}: {self.score} (x{self.multiplier})"
            lives_txt = f"{t['lives']}: {'❤️ ' * self.lives}"
            time_txt = f"{t['time']}: {self.time_left}s"
            level_txt = f"{t['level']}: {self.level}"
            s_surf = self.font_medium.render(score_txt, True, (255, 255, 255))
            l_surf = self.font_medium.render(lives_txt, True, (230, 50, 50))
            t_surf = self.font_medium.render(time_txt, True, (255, 215, 0))
            lv_surf = self.font_medium.render(level_txt, True, (0, 230, 230))
            screen.blit(s_surf, (20, 20))
            screen.blit(l_surf, (20, 55))
            screen.blit(t_surf, (SCREEN_WIDTH - 160, 20))
            screen.blit(lv_surf, (SCREEN_WIDTH - 160, 55))

            if self.current_state == "paused":
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150))
                screen.blit(overlay, (0, 0))
                p_surf = self.font_large.render(t["paused"], True, (255, 255, 255))
                screen.blit(p_surf, (SCREEN_WIDTH // 2 - p_surf.get_width() // 2, SCREEN_HEIGHT // 2 - 20))

        elif self.current_state == self.STATE_GAMEOVER:
            screen.fill((20, 20, 35))
            msg = t["victory"] if self.time_left == 0 else t["game_over"]
            col = (50, 220, 100) if self.time_left == 0 else (230, 50, 50)
            msg_surf = self.font_title.render(msg, True, col)
            final_score = self.font_large.render(f"{t['score']}: {self.score}", True, (255, 255, 255))
            res_surf = self.font_medium.render(t["restart"], True, (200, 200, 200))
            screen.blit(msg_surf, (SCREEN_WIDTH // 2 - msg_surf.get_width() // 2, 180))
            screen.blit(final_score, (SCREEN_WIDTH // 2 - final_score.get_width() // 2, 270))
            screen.blit(res_surf, (SCREEN_WIDTH // 2 - res_surf.get_width() // 2, 350))