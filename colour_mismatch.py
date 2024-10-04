import pygame
import random

pygame.init()

width, height = 400, 600
box_size = 100
bg = (255, 255, 255)
text = (0, 0, 0)

FONT = pygame.font.SysFont("Arial", 32)
SCORE_FONT = pygame.font.SysFont("Arial", 24)
BUTTON_FONT = pygame.font.SysFont("Arial", 20)

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Colour Match")


def draw_game(window, boxes, score, high_score):
    window.fill(bg)

    title_text = FONT.render("Colour Mismatch", True, text)
    window.blit(title_text, (width // 2 - title_text.get_width() // 2, 10))

    high_score_text = SCORE_FONT.render(f"High score: {high_score}", True, text)
    score_text = SCORE_FONT.render(f"Current score: {score}", True, text)
    window.blit(high_score_text, (10, 60))
    window.blit(score_text, (10, 90))

    for i, color in enumerate(boxes):
        x = (i % 4) * box_size
        y = 150 + (i // 4) * box_size
        pygame.draw.rect(window, color, (x, y, box_size, box_size))

    pygame.display.update()


def check_selection(mouse_pos):
    x, y = mouse_pos
    if y < 150:
        return -1
    box_x = x // box_size
    box_y = (y - 150) // box_size
    if box_y < 0 or box_y >= 4:
        return -1
    return box_y * 4 + box_x


def draw_game_over(window, score, high_score, new_high_score):
    window.fill(bg)

    if new_high_score:
        msg_text = FONT.render(f"New high score!", True, text)
    else:
        msg_text = FONT.render(f"Better luck next time!", True, text)

    score_text = SCORE_FONT.render(f"Score: {score}", True, text)
    high_score_text = SCORE_FONT.render(f"High score: {high_score}", True, text)

    # Draw text
    window.blit(msg_text, (width // 2 - msg_text.get_width() // 2, 150))
    window.blit(score_text, (width // 2 - score_text.get_width() // 2, 200))
    if not new_high_score:
        window.blit(high_score_text, (width // 2 - high_score_text.get_width() // 2, 240))

    # Draw buttons
    restart_button = pygame.Rect(width // 4, 300, width // 2, 40)
    quit_button = pygame.Rect(width // 4, 360, width // 2, 40)

    pygame.draw.rect(window, (100, 200, 100), restart_button)
    pygame.draw.rect(window, (200, 100, 100), quit_button)

    restart_text = BUTTON_FONT.render("Restart game", True, text)
    quit_text = BUTTON_FONT.render("Quit", True, text)

    window.blit(restart_text, (width // 2 - restart_text.get_width() // 2, 310))
    window.blit(quit_text, (width // 2 - quit_text.get_width() // 2, 370))

    pygame.display.update()

    return restart_button, quit_button


score = 0
high_score = 0
running = True

while running:
    base_color = [random.randint(50, 200) for _ in range(3)]

    boxes = [base_color[:] for _ in range(16)]

    correct_box = random.randint(0, 15)
    different_color = [(c + 5) % 256 for c in base_color]
    boxes[correct_box] = different_color

    draw_game(window, boxes, score, high_score)

    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_over = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                clicked_box = check_selection(mouse_pos)
                if clicked_box == correct_box:
                    score += 1
                    if score > high_score:
                        high_score = score
                    game_over = True
                elif clicked_box != -1:
                    new_high_score = score > high_score
                    restart_button, quit_button = draw_game_over(window, score, high_score, new_high_score)
                    score = 0

                    game_over_screen = True
                    while game_over_screen:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False
                                game_over_screen = False
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                mouse_pos = pygame.mouse.get_pos()
                                if restart_button.collidepoint(mouse_pos):
                                    game_over_screen = False
                                if quit_button.collidepoint(mouse_pos):
                                    running = False
                                    game_over_screen = False

                    game_over = True

pygame.quit()
