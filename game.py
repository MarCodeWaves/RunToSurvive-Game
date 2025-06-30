import pygame
from sys import exit
from random import randint, choice

# KLASA GRACZA
class Player(pygame.sprite.Sprite):  # dziedziczymy z innej klasy
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('Graphics/player/walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('Graphics/player/jump_1.png').convert_alpha()
        player_walk_3 = pygame.image.load('Graphics/player/walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2,player_walk_3]
        self.player_index = 0
        self.player_jump = pygame.image.load('Graphics/player/jump_1.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect()
        self.gravity = 0  # gracz jest na podłodze gdy zaczynamy grę

        self.jump_sound = pygame.mixer.Sound('Audio/jump.mp3') # dźwięk skakania
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()    #poieranie przycisków
        if keys[pygame.K_SPACE] and self.rect.bottom >= 200:    # kontrola upadku ze skoku (inaczej wylatuje poza ekran)
            self.gravity = -20      # upadanie
            self.jump_sound.play()   # dźwięk skoku

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:  # aby mieć pewność że gracz będzie widoczny
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1  # szybkość zmieniania się pozycji
            if self.player_index >= len(self.player_walk):
                self.player_index = 0  # po pętli pozycji gracza wracamy do początku

            self.image = self.player_walk[int(self.player_index)]  # zaokrąglanie

    def update(self):   # zmiany
        self.player_input()
        self.apply_gravity()
        self.animation_state()

# KLASA POTWORÓW
class Monster(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'bat':    # ładowanie zdjęć
            bat_1 = pygame.image.load('graphics/bat/bat_down.png').convert_alpha()
            bat_2 = pygame.image.load('graphics/bat/bat_up.png').convert_alpha()
            self.frames = [bat_1, bat_2]
            y_pos = 220
        else:
            ground_monster_1 = pygame.image.load('graphics/monster/monster_right.png').convert_alpha()
            ground_monster_2 = pygame.image.load('graphics/monster/monster_left.png').convert_alpha()
            self.frames = [ground_monster_1, ground_monster_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(850, 1100),y_pos))

    def animation_state(self):  # animacja potworów
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0

        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):   # niszczenie przy końcu ekranu
        if self.rect.x <= -50:
            self.kill()

# WYŚWIETLANIE WYNIKU
def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time    # 1 sekunda to jeden punkt ( pobiera czas w milisekundach)
    score_surf = game_font.render(f'Score: {current_time}', True, "white")
    score_rect = score_surf.get_rect(center=(350, 50))
    screen.blit(score_surf, score_rect)
    return current_time

# SPRAWDZANIE KOLIZJI
def collisions():
    if pygame.sprite.spritecollide(player.sprite, monster_group, False):
        die_sound.play()  # dźwięk przy przegranej
        monster_group.empty()
        return False
    else:
        return True

# POBIERANIE NAJWYŻSZEGO WYNIKU
def get_highest_score():
    with open("highest_score.txt","r") as f:
        return f.read()

pygame.init()  # inicjalizacja gry
screen = pygame.display.set_mode((700, 400)) # okno gry (rozmiar)
pygame.display.set_caption('Running turtle') # tytuł gry
clock = pygame.time.Clock() # potrzebne do określenia szybkości gry

# FONTY WYKORZYSTANE W GRZE
game_font = pygame.font.Font('Fonts/Emizen.ttf', 56)
font_mini = pygame.font.Font('Fonts/Emizen.ttf', 20)
button_font = pygame.font.Font('Fonts/Buttonfont.ttf', 45)

gaming_active = False      # rozpoczynamy grę od menu
start_time = 0    # czas to punkty, więc zaczynamy od 0
score = 0    # grę zaczynamy od wyniku 0

# AUDIO W GRZE
bg_music = pygame.mixer.Sound('Audio/music.wav') # muzyka w tle
bg_music.play(loops=-1)
die_sound = pygame.mixer.Sound('Audio/failure.wav') # dźwięk przy przegraniu
die_sound.set_volume(1)

# GRUPY POSTACI
player = pygame.sprite.GroupSingle()  # gracz ( grupa pojedyncza )
player.add(Player())

monster_group = pygame.sprite.Group() # grupa potworów

# TŁO I PODŁOGA
sky = pygame.image.load('graphics/123.jpg').convert()
ground = pygame.image.load('graphics/ground.png').convert()

# MENU (POCZĄTKOWY WIDOK)
menu_player = pygame.image.load('graphics/player/jump_1.png').convert_alpha()
menu_player = pygame.transform.rotozoom(menu_player, 0, 2)
menu_player_rect = menu_player.get_rect(center=(350, 200))

game_name = game_font.render('RUN TO SURVIVE', True, "#05F2DB")  # nazwa gry
game_name_rect = game_name.get_rect(center=(360, 60))

rules_place = pygame.image.load('graphics/ruless.png').convert_alpha()    # zasady gry
rules_place_rect = rules_place.get_rect(center=(130,240))

author_place = pygame.image.load('graphics/label.png').convert_alpha()     # informacje o autorze
author_place_rect = author_place.get_rect(center=(570,240))

start_button = button_font.render('START', True, "#05F2DB")  # przycisk start
start_button_rect = start_button.get_rect(center=(350, 300))

quit_button = button_font.render('QUIT', True, "#F54DDD")   #przycisk zakończ w menu
quit_button_rect = quit_button.get_rect(center=(350,370))

# MENU GAME OVER (NA KOŃCU GRY)
quit_button2 = button_font.render('QUIT', True, "#F54DDD")     # przycisk zakończ w menu Game Over
quit_button_rect2 = quit_button2.get_rect(center=(610,20))

back_button = button_font.render("REPLAY", True, "#05F2DB")     # przycisk uruchamiający grę ponownie
back_button_rect = back_button.get_rect(center=(350, 80))

# Częstotliwość pojawiania się potworów
monster_freq = pygame.USEREVENT + 1
pygame.time.set_timer(monster_freq, 1200) # raz na 1200 milisekund

try:
    highest_score = int(get_highest_score())
except:
    highest_score = 0

# Tu będą działy się wszystkie wydarzenia
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit() # dzięki temu możemy wyjść z gry

        if gaming_active:
            if event.type == monster_freq:
                monster_group.add(Monster(choice([ 'bat','monster', 'monster', 'monster']))) # losowe wybieranie potwora

        else:
            if event.type == pygame.MOUSEBUTTONDOWN :  # działanie przycisków START, QUIT, REPLAY
                if start_button_rect.collidepoint(pygame.mouse.get_pos()) or back_button_rect.collidepoint(pygame.mouse.get_pos()):
                    gaming_active = True
                    start_time = int(pygame.time.get_ticks() / 1000)
                if quit_button_rect.collidepoint(pygame.mouse.get_pos()) or quit_button_rect2.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    exit()

    # zapisywanie najwyższego wynik
    if (highest_score < score):
        highest_score = score
    with open("highest_score.txt", "w") as f:
        f.write(str(highest_score))

    if gaming_active:
        screen.blit(sky, (0, 0))
        screen.blit(ground, (0, 300))
        score = display_score()  # pokazywanie wyniku podczas gry

        player.draw(screen)
        player.update()

        monster_group.draw(screen)
        monster_group.update()

        gaming_active = collisions() # gra się wyłącza jeśli zaszła kolizja

    else:
        screen.fill("#260726") # kolor tła
        screen.blit(menu_player, menu_player_rect)

        score_info = game_font.render(f'Your score: {score}', True, "white")
        score_info_rect = score_info.get_rect(center=(350, 300))

        hscore_info = font_mini.render(f'Highest score: {highest_score}', True, "green")
        hscore_info_rect = hscore_info.get_rect(center=(570, 370))

        hscore2_info = game_font.render(f'Highest score: {highest_score}', True, "green")
        hscore2_info_rect = hscore_info.get_rect(center=(220, 330))


        if score == 0:
            screen.blit(game_name, game_name_rect)
            screen.blit(start_button, start_button_rect)
            screen.blit(quit_button,quit_button_rect)
            screen.blit(rules_place, rules_place_rect)
            screen.blit(author_place, author_place_rect)
            screen.blit(hscore_info, hscore_info_rect)
        else:
            screen.blit(back_button, back_button_rect)
            screen.blit(score_info, score_info_rect)
            screen.blit(quit_button2,quit_button_rect2)
            screen.blit(hscore2_info, hscore2_info_rect)


    pygame.display.update()
    clock.tick(58) # tu ustalona jest szybkość gry (optymalizacja względem różnych urządzeń)