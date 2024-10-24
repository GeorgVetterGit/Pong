import pygame

HEIGHT = 400
WIDTH = 600
BAR_SPEED = 10
BAR_LENGTH = 100
BAR_WIDTH = 15
BALL_SPEED = 12
RATIO = 1.1
COOL_DOWN = 3000

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.font.init()

COLORS = {'WHITE': (255, 255, 255),
          'BLACK': (0, 0, 0)}

pygame.display.set_caption("Pong")

class bar():

    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = pygame.Rect(self.x_pos, self.y_pos, BAR_WIDTH, BAR_LENGTH)
        pass

    def move(self, key: str):
        if key == 'up':
            self.y_pos = max(self.y_pos - BAR_SPEED, 0)
        if key == 'down':
            self.y_pos = min(self.y_pos + BAR_SPEED, 
                             HEIGHT - BAR_LENGTH)
        self.rect = pygame.Rect(self.x_pos, self.y_pos, BAR_WIDTH, BAR_LENGTH)
    
    def draw(self):
        return self.rect

class ball():

    def __init__(self):
        self.x_pos = (WIDTH / 2) - 10
        self.y_pos = (HEIGHT / 2) - 10
        self.rect = pygame.Rect(self.x_pos, self.y_pos, 20, 20)
        pass

    def move(self, ratio: float, BALL_SPEED: int, player, opponent):
        hit_right_border = self.rect.right > WIDTH
        hit_left_border = self.rect.left < 0

        player_collide = self.rect.colliderect(player.rect)
        opponent_collide = self.rect.colliderect(opponent.rect)

        if player_collide:
            BALL_SPEED *= -1
            ratio = 1 - (1 - ratio)
            ratio2 = 1 + (((self.y_pos - player.y_pos) / BAR_LENGTH) - 0.5)
            ratio = ratio2
            self.x_pos -= 5
        if opponent_collide:
            BALL_SPEED *= -1
            ratio = 1 - (1 - ratio)
            ratio2 = 1 + (((self.y_pos - opponent.y_pos) / BAR_LENGTH) - 0.5)
            ratio = ratio2
            self.x_pos += 5
        if hit_right_border or hit_left_border:
            self.x_pos = (WIDTH / 2) - 10
            self.y_pos = (HEIGHT / 2) - 10
            BALL_SPEED *= -1
            ratio = 1
        if self.rect.top < 0: #upper border
            ratio = 1 + (1 - ratio)
            self.y_pos += 5
        if self.rect.bottom > HEIGHT: #lower border
            ratio = 1 + (1 - ratio)
            self.y_pos -= 5
        if not hit_right_border or hit_left_border:
            self.x_pos += BALL_SPEED
            if BALL_SPEED < 0:
                self.y_pos += BALL_SPEED * (1 - ratio)
            else:
                self.y_pos += BALL_SPEED * (ratio - 1)

        self.rect = pygame.Rect(self.x_pos, self.y_pos, 20, 20)

        return ratio, BALL_SPEED, hit_right_border, hit_left_border
        
    def draw(self):
        rect = pygame.Rect(self.x_pos, self.y_pos, 20, 20)
        return rect

player = bar(WIDTH - 30, int(HEIGHT / 2))
opponent = bar(30, int(HEIGHT / 2))
playball = ball()

score_opp = 0
score_player = 0

my_font = pygame.font.SysFont('Consolas', 45)
my_font_small = pygame.font.SysFont('Consolas', 15)

last_time = 0
hit_right = False
hit_left = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player.move('up')
    if keys[pygame.K_DOWN]:
        player.move('down')
    if keys[pygame.K_w]:
        opponent.move('up')
    if keys[pygame.K_s]:
        opponent.move('down')
    
    now = pygame.time.get_ticks()
    if now - last_time >= COOL_DOWN:
        RATIO, BALL_SPEED, hit_right, hit_left = playball.move(RATIO, BALL_SPEED, player, opponent)
    
    remain_time = COOL_DOWN - (now - last_time)

    if hit_right:
        score_opp += 1
        last_time = now
        hit_right = False
    if hit_left:
        score_player += 1
        last_time = now
        hit_left = False

    screen.fill(COLORS['BLACK'])

    #Middle line
    pygame.draw.rect(screen, COLORS['WHITE'], (WIDTH / 2, 30, 5, HEIGHT - 60))

    player_bar = player.draw()
    pygame.draw.rect(screen, COLORS['WHITE'], player_bar)
    opponent_bar = opponent.draw()
    pygame.draw.rect(screen, COLORS['WHITE'], opponent_bar)
    ball_pic = playball.draw()
    pygame.draw.rect(screen, COLORS['WHITE'], ball_pic)

    opp_score_text = my_font.render(str(score_opp), False, COLORS['WHITE'])
    length_score_opp = len(str(score_opp))
    screen.blit(opp_score_text, (60 - (length_score_opp * 20),15))

    player_score_text = my_font.render(str(score_player), False, COLORS['WHITE'])
    length_score_player = len(str(score_player))
    screen.blit(player_score_text, (WIDTH - 20 - (20 * length_score_player),15))

    if remain_time > 0:
        time_text = my_font_small.render('Start in ' + str(round(remain_time / 1000, 1)), False, COLORS['WHITE'])
        screen.blit(time_text, (WIDTH / 2 - 50, HEIGHT - 20))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
