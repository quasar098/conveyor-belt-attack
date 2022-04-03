import pygame
from button import Button
from utils import *
from conveyer import ConveyerBelt
from gain_time_effect import GainTimeEffect
from crafting_tooltip import CraftingTooltip

pygame.init()

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Conveyor Belt Attack")
# todo: make an icon for the game
font = pygame.font.Font(get_path("assets", "font.ttf"), 36)
bigger_font = pygame.font.Font(get_path("assets", "font.ttf"), 48)
timer_font = pygame.font.Font(get_path("assets", "timer.ttf"), 48)
clock = pygame.time.Clock()


def change_screen(new: str):
    global viewing_screen
    reset_game()
    viewing_screen = new


def reset_game():
    global blocks, belt, time_left, opening_smooth, survival_time, stage, highest_tier, time_multiplier
    stage = 1
    blocks = []
    belt.passengers = []
    time_left = starting_time
    opening_smooth = 1
    survival_time = 0
    highest_tier = 0
    time_multiplier = 1.6-difficulty*0.5


def toggle_music():
    global music_paused
    music_paused = not music_paused
    if music_paused:
        channels[0].pause()
    else:
        channels[0].unpause()


def toggle_difficulty():
    global difficulty
    difficulty += 1
    if difficulty > 2:
        difficulty = 0


# main menu stuff
_ = pygame.Rect(0, 0, 270, 60)
_.midtop = screen.get_rect().move(0, 300).midtop
play_button = Button(_.inflate(-10, 0), font, "Play Game", callback=change_screen, callback_args=(GAME,),
                     sound_path=get_path("assets", "sounds", "start_game.wav"))
how_to_play_button = Button(_.copy().move(0, 90), font, "How To Play", callback=change_screen,
                            callback_args=(HOW_TO_PLAY,), sound_path=get_path("assets", "sounds", "start_game.wav"))
toggle_music_button = Button(_.copy().move(0, 180).inflate(14, 0), font, "Toggle Music", toggle_music,
                             sound_path=get_path("assets", "sounds", "start_game.wav"))
toggle_hardcore_button = Button(_.copy().move(0, 270).inflate(68, 0), font, "Change Difficulty", toggle_difficulty,
                                sound_path=get_path("assets", "sounds", "start_game.wav"))

# game stuff
belt = ConveyerBelt(top=80, speed=1)
blocks = []
starting_time = 30
time_left = starting_time
opening_smooth = 1
time_multiplier = 0.6
survival_time = 0
stage = 1
gain_time_effect = GainTimeEffect(font)
play_sound(get_path("assets", "sounds", "bg_music.mp3"), looping=-1)
music_paused = False
toggle_music()
warning_delay = 0
highest_tier = 0
crafting_tooltip = CraftingTooltip(pygame.Rect(WIDTH-298, 10, 288, 80), font)
warning_arrow_surface = fetch_texture(get_path("assets", "images", "warning_arrow.png"))
difficulty = 0

# how to play stuff
back_to_menu = Button(pygame.Rect(10, 10, 150, 60), font, "Back", callback=change_screen, callback_args=(MAIN_MENU,),
                      sound_path=get_path("assets", "sounds", "start_game.wav"))
tutorial_image = fetch_texture(get_path("assets", "images", "tutorial.png"))

# preload timer texts
for _ in range(time_left*10):
    fetch_text(f"time left: {_/10}", timer_font)

viewing_screen = MAIN_MENU
running = True
while running:
    screen.fill(BG_COLOR)
    # events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            if viewing_screen != GAME:
                running = False
            else:
                change_screen(MAIN_MENU)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if viewing_screen != MAIN_MENU:
                    change_screen(MAIN_MENU)
    # main menu
    if viewing_screen == MAIN_MENU:
        # handle
        play_button.handle_events(events)
        how_to_play_button.handle_events(events)
        toggle_music_button.handle_events(events)
        toggle_hardcore_button.handle_events(events)
        # draw
        _ = fetch_text("Conveyor Belt Attack", font)
        screen.blit(_, _.get_rect(midtop=screen.get_rect().move(0, 30).midtop))
        play_button.draw(screen)
        how_to_play_button.draw(screen)
        toggle_music_button.draw(screen)
        toggle_hardcore_button.draw(screen)
        _ = fetch_text(["Easy Mode", "Normal Mode", "Hardcore Mode"][difficulty], font)
        screen.blit(_, _.get_rect(midtop=toggle_hardcore_button.rect.move(0, 16).midbottom))
        belt.draw(screen, 75/FRAMERATE, 0.5)
    # how to play
    if viewing_screen == HOW_TO_PLAY:
        # handle
        back_to_menu.handle_events(events)
        # draw
        back_to_menu.draw(screen)
        screen.blit(tutorial_image, (0, 0))
    # game
    if viewing_screen == GAME:
        # game functionality
        time_left -= 1/FRAMERATE
        if time_left > starting_time:
            time_left -= 1/FRAMERATE  # double drain if above starting time
        if time_left < 0:
            viewing_screen = HIGH_SCORE
        opening_smooth -= 1/FRAMERATE
        if opening_smooth < 0:
            opening_smooth = 0
        survival_time += 1/FRAMERATE
        warning_delay -= 1/FRAMERATE
        if time_left < 10:
            if warning_delay <= 0:
                warning_delay = 1
                play_sound(get_path("assets", "sounds", "warning.wav"))
        # draw
        speed_mod = clamp(2-opening_smooth*1.5+survival_time/15, 0, 10)
        belt.draw(screen, 75/FRAMERATE, speed_mod)
        belt.add_occasionally(75/FRAMERATE+survival_time/15, survival_time/30)
        offload_area_rect = pygame.Rect(10, belt.rect.bottom+10, belt.rect.w-20, HEIGHT-(belt.rect.bottom+20))
        offload_area_rect.inflate_ip(-offload_area_rect.w*opening_smooth, 0)
        pygame.draw.rect(screen, (0, 0, 0), offload_area_rect)
        pygame.draw.rect(screen, (220, 220, 227), offload_area_rect.inflate(-2, -2))
        tl_text = fetch_text(f"time left: {int(time_left*10)/10}", timer_font)
        screen.blit(tl_text, (10, 10))
        crafting_tooltip.draw(screen, blocks)
        if time_left < 10:
            screen.blit(warning_arrow_surface,
                        warning_arrow_surface.get_rect(midleft=(305+cserp(time_left)*10, 36)))
        # draw all blocks
        for block in belt.passengers.__reversed__():
            block.x += 75/FRAMERATE*speed_mod
            block.draw(screen, font)
            if block.x > WIDTH+75:
                if block.tier > 1 and block.do_points:
                    time_left += ((block.tier/2)*block.tier)*time_multiplier
                    play_sound(get_path("assets", "sounds", "gain_time.wav"))
                    gain_time_effect.show_gain(((block.tier/2)*block.tier)*time_multiplier, [WIDTH-100, 150])
                belt.passengers.remove(block)
        for block in blocks:
            block.draw(screen, font)
        # handle conveyor blocks
        for block in belt.passengers.__reversed__():
            if block.do_start_grab(events):
                block.grabbed = True
                belt.passengers.remove(block)
                blocks.append(block)
                play_sound(get_path("assets", "sounds", "grab_block.wav"))
                break
        else:
            belt.handle_events(events)
        # handle other blocks
        for block in blocks.__reversed__():
            if block.do_start_grab(events):
                block.grabbed = True
                blocks.remove(block)
                blocks.append(block)
                play_sound(get_path("assets", "sounds", "grab_block.wav"))
                break
            if block.do_let_go(events):
                block.grabbed = False
                play_sound(get_path("assets", "sounds", "let_go_of_block.wav"))
                if block.y < 300:
                    block.y = 150
                    blocks.remove(block)
                    belt.passengers.append(block)
                    break
                for other in [other for other in blocks if other != block]:
                    if other.rect.colliderect(block.rect):
                        for recipe in RECIPIES:
                            if (block.tier, other.tier) == recipe or (other.tier, block.tier) == recipe:
                                block.tier = RECIPIES[recipe]
                                if highest_tier < block.tier:
                                    highest_tier = block.tier
                                block.x = (block.x+other.x)/2
                                block.y = (block.y+other.y)/2
                                block.do_points = True
                                blocks.remove(other)
                                break
                break
        gain_time_effect.draw(screen, 75/FRAMERATE)
    # high score
    if viewing_screen == HIGH_SCORE:
        # handle
        back_to_menu.handle_events(events)
        # draw
        _ = fetch_text(f"You survived for {int(survival_time*10)/10}s", font)
        screen.blit(_, _.get_rect(center=screen.get_rect().move(0, -30).center))
        _ = fetch_text(
            f"The highest quality box you crafted had quality {highest_tier}.", font
        )
        screen.blit(_, _.get_rect(center=screen.get_rect().move(0, 30).center))
        back_to_menu.draw(screen)
    pygame.display.flip()
    clock.tick(FRAMERATE)
pygame.quit()
