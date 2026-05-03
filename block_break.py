  import pygame
import random
 
pygame.init()
W, H = 400, 500
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
 
# Paddle
PAD_W, PAD_H = 80, 12
pad_x = W // 2 - PAD_W // 2
pad_y = H - 40
 
# Ball
ball_x, ball_y = W // 2, H // 2 + 60
ball_vx, ball_vy = 3, -4
BALL_R = 6
 
# Bricks
BRICK_ROWS = 6
BRICK_COLS = 8
BRICK_W = (W - 20) // BRICK_COLS
BRICK_H = 18
BRICK_TOP = 50
BRICK_COLORS = [
    (231, 76, 60), (230, 126, 34), (241, 196, 15),
    (46, 204, 113), (52, 152, 219), (155, 89, 182),
]
 
def make_bricks():
    bricks = []
    for r in range(BRICK_ROWS):
        for c in range(BRICK_COLS):
            x = 10 + c * BRICK_W
            y = BRICK_TOP + r * (BRICK_H + 3)
            bricks.append(pygame.Rect(x, y, BRICK_W - 2, BRICK_H))
    return bricks
 
bricks = make_bricks()
score = 0
lives = 3
game_over = False
win = False
 
def reset_ball():
    global ball_x, ball_y, ball_vx, ball_vy
    ball_x, ball_y = W // 2, H // 2 + 60
    ball_vx = 3 if random.random() > 0.5 else -3
    ball_vy = -4
 
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            pad_x = max(0, min(W - PAD_W, event.pos[0] - PAD_W // 2))
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_over or win:
                bricks = make_bricks()
                score = 0
                lives = 3
                game_over = False
                win = False
                reset_ball()
            else:
                pad_x = max(0, min(W - PAD_W, event.pos[0] - PAD_W // 2))
 
    if not game_over and not win:
        ball_x += ball_vx
        ball_y += ball_vy
 
        # Wall bounce
        if ball_x - BALL_R <= 0 or ball_x + BALL_R >= W:
            ball_vx = -ball_vx
        if ball_y - BALL_R <= 0:
            ball_vy = abs(ball_vy)
 
        # Paddle bounce
        pad_rect = pygame.Rect(pad_x, pad_y, PAD_W, PAD_H)
        if ball_vy > 0 and pad_rect.collidepoint(ball_x, ball_y + BALL_R):
            ball_vy = -abs(ball_vy)
            offset = (ball_x - (pad_x + PAD_W / 2)) / (PAD_W / 2)
            ball_vx = int(offset * 5)
            if ball_vx == 0: ball_vx = 2 if ball_x > W//2 else -2
 
        # Brick collision
        ball_rect = pygame.Rect(ball_x - BALL_R, ball_y - BALL_R, BALL_R*2, BALL_R*2)
        for b in bricks[:]:
            if ball_rect.colliderect(b):
                bricks.remove(b)
                score += 10
                # Determine bounce direction
                if abs(ball_x - b.centerx) * b.height > abs(ball_y - b.centery) * b.width:
                    ball_vx = -ball_vx
                else:
                    ball_vy = -ball_vy
                break
 
        # Ball falls below
        if ball_y > H:
            lives -= 1
            if lives <= 0:
                game_over = True
            else:
                reset_ball()
 
        if not bricks:
            win = True
 
    # Draw
    screen.fill((20, 20, 35))
 
    # Bricks
    for i, b in enumerate(bricks):
        row = (b.y - BRICK_TOP) // (BRICK_H + 3)
        color = BRICK_COLORS[row % len(BRICK_COLORS)]
        pygame.draw.rect(screen, color, b, border_radius=3)
 
    # Paddle
    pygame.draw.rect(screen, (200, 220, 255), (int(pad_x), pad_y, PAD_W, PAD_H), border_radius=6)
 
    # Ball
    if not game_over:
        pygame.draw.circle(screen, (255, 255, 255), (int(ball_x), int(ball_y)), BALL_R)
 
    # HUD
    font = pygame.font.Font(None, 28)
    st = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(st, (10, 10))
    lt = font.render(f'Lives: {lives}', True, (255, 200, 200))
    screen.blit(lt, (W - 100, 10))
 
    if game_over:
        bf = pygame.font.Font(None, 48)
        gt = bf.render('Game Over!', True, (255, 80, 80))
        gr = gt.get_rect(center=(W//2, H//2))
        screen.blit(gt, gr)
        hf = pygame.font.Font(None, 24)
        ht = hf.render('Tap to restart', True, (200, 200, 200))
        hr = ht.get_rect(center=(W//2, H//2 + 35))
        screen.blit(ht, hr)
    elif win:
        bf = pygame.font.Font(None, 48)
        wt = bf.render('You Win!', True, (50, 255, 50))
        wr = wt.get_rect(center=(W//2, H//2))
        screen.blit(wt, wr)
        hf = pygame.font.Font(None, 24)
        ht = hf.render('Tap to play again', True, (200, 200, 200))
        hr = ht.get_rect(center=(W//2, H//2 + 35))
        screen.blit(ht, hr)
 
    pygame.display.flip()
    clock.tick(15)
 
pygame.quit()
 