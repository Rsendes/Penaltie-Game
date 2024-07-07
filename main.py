import pygame
import random
import time

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BALL_INI_X = SCREEN_WIDTH // 2
BALL_INI_Y = 620
GK_INI_X = SCREEN_WIDTH // 2
GK_INI_Y = 290
BANNER_X = SCREEN_WIDTH // 2
BANNER_Y = 50
gk_positions = [
    ["assets/GK/TL.png", 450, 250], ["assets/GK/T.png", GK_INI_X, GK_INI_Y],
    ["assets/GK/TR.png", 825, 250], ["assets/GK/BL.png", 450, 350],
    ["assets/GK/B.png", GK_INI_X, GK_INI_Y + 20], ["assets/GK/BR.png", 800, 350]
]
goal_positions = [
    [300, 120, 527, 250], [527, 120, 753, 250], [743, 120, 980, 250],
    [300, 250, 527, 380], [527, 250, 753, 380], [753, 250, 980, 380]
]
cpu_positions = [
    [370, 175], [SCREEN_WIDTH // 2, 175], [915, 175],
    [370, 320], [SCREEN_WIDTH // 2, 320], [915, 320]
]

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Penalty Shootout")
font = pygame.font.SysFont(None, 36)

# Load Images
background_image = pygame.image.load("assets/background.png")
ball_image = pygame.image.load("assets/small_ball.png").convert_alpha()
banner_image = pygame.image.load("assets/Banners/turn_score.png").convert_alpha()
gk_image = pygame.image.load("assets/GK/C.png").convert_alpha()

ball_rect = ball_image.get_rect(center=(BALL_INI_X, BALL_INI_Y))
banner_rect = banner_image.get_rect(center=(BANNER_X, BANNER_Y))
gk_rect = gk_image.get_rect(center=(GK_INI_X, GK_INI_Y))

def displays_score():
    player_text = font.render(f"Player: {player_score}", True, (0, 0, 0))
    cpu_text = font.render(f"CPU: {cpu_score}", True, (0, 0, 0))
    screen.blit(player_text, (10, 10))
    screen.blit(cpu_text, (10, 50))

def update_screen():
    screen.blit(background_image, (0, 0))
    screen.blit(gk_image, gk_rect)
    screen.blit(ball_image, ball_rect)
    screen.blit(banner_image, banner_rect)
    displays_score()
    pygame.display.update()

def check_goal(click_x, click_y, gk_decision):
    if click_x > goal_positions[gk_decision][0] and click_y > goal_positions[gk_decision][1] and click_x < goal_positions[gk_decision][2] and click_y < goal_positions[gk_decision][3]:
        return "Save"
    elif click_x < 300 or click_x > 980 or click_y < 120 or click_y > 380:
        return "Miss"
    else:
        return "Goal"

run = True
player_score = 0
cpu_score = 0
is_player = True

# Main Loop
while run:
    events = pygame.event.get()
    if any(event.type == pygame.QUIT for event in events):
        run = False
    
    if is_player:
        banner_image = pygame.image.load("assets/Banners/turn_score.png").convert_alpha()
        event = next((event for event in events if event.type == pygame.MOUSEBUTTONDOWN), None)
        if event:
            click_x, click_y = event.pos
            ball_rect.center = (click_x, click_y)

            gk_decision = random.randint(0, 5)
            gk_image = pygame.image.load(gk_positions[gk_decision][0]).convert_alpha()
            gk_rect.center = (gk_positions[gk_decision][1], gk_positions[gk_decision][2])

            result = check_goal(click_x, click_y, gk_decision)
            if result == "Save":
                banner_image = pygame.image.load("assets/Banners/Save.png").convert_alpha()
            elif result == "Miss":
                banner_image = pygame.image.load("assets/Banners/Miss.png").convert_alpha()
            else:
                banner_image = pygame.image.load("assets/Banners/GOAL!.png").convert_alpha()
                player_score += 1
            is_player = False

            update_screen()
            time.sleep(1.5)

    else:
        banner_image = pygame.image.load("assets/Banners/turn_save.png").convert_alpha()
        event = next((event for event in events if event.type == pygame.MOUSEBUTTONDOWN), None)
        if event:
            click_x, click_y = event.pos
            player_decision = next((i for i, pos in enumerate(goal_positions) if pos[0] < click_x < pos[2] and pos[1] < click_y < pos[3]), 6)
            if player_decision < 6:
                gk_image = pygame.image.load(gk_positions[player_decision][0]).convert_alpha()
                gk_rect.center = (gk_positions[player_decision][1], gk_positions[player_decision][2])

            cpu_decision = random.randint(0, 5)
            ball_rect.center = (cpu_positions[cpu_decision][0], cpu_positions[cpu_decision][1])

            if player_decision == cpu_decision:
                banner_image = pygame.image.load("assets/Banners/SAVE!.png").convert_alpha()
            else:
                banner_image = pygame.image.load("assets/Banners/Goal.png").convert_alpha()
                cpu_score += 1
            is_player = True

            if (player_score > 4 and cpu_score <= 4) or (player_score > 5 and player_score > cpu_score) or (player_score == cpu_score + 3):
                banner_image = pygame.image.load("assets/Banners/WIN.png").convert_alpha()
                run = False
            elif (cpu_score > 4 and player_score <= 4) or (cpu_score > 5 and cpu_score > player_score) or (cpu_score == player_score + 3):
                banner_image = pygame.image.load("assets/Banners/LOST.png").convert_alpha()
                run = False

            update_screen()
            time.sleep(1.5)

    gk_rect.center = (GK_INI_X, GK_INI_Y)
    gk_image = pygame.image.load("assets/GK/C.png").convert_alpha()
    ball_rect.center = (BALL_INI_X, BALL_INI_Y)
    update_screen()

pygame.quit()

