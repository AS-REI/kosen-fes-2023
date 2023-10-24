import pygame
import random
import sys

# 初期化
def run_game():
    pygame.init()

# 画面の設定
screen_width, screen_height = 1000, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("新妻シューティング")

# 色
#　ちなみに色と数値は一致してないよ
WHITE = (0, 0, 0)
RED = (200,200, 0)
BLACK = (255,255,255)
BLUE = (255,0,0)

# プレイヤーの画像ロード
player_image = pygame.image.load("player.png")
player_size = 80
player_image = pygame.transform.scale(player_image, (player_size, player_size))
player_pos = [screen_width // 2, screen_height - player_size * 2]

# 敵
enemy_size = 40
enemy_pos = [random.randint(0, screen_width - enemy_size), 0]
enemy_list = [enemy_pos]

class Enemy:
    def __init__(self) -> None:
        self.size = 40;
        self.pos = [random.randint(0, screen_width - enemy_size), 0];
    def move (self, dir) -> None:
        self.pos += dir;

# 速度
player_speed = 1
enemy_speed = 0.1

# 弾
bullet_size = 5
bullet_pos = []
bullet_speed = 1

class Bullet: 
    def __init__(self) -> None:
        self.size = 5;
        self.pos = [];
        self.speed = 1;
    def move(self, dir) -> None:
        self.pos += dir;

# ゲームオーバー
game_over = False

# スコア
score = 0

# スコアアップ敵
score_enemy_size = 30
score_enemy_pos = [random.randint(0, screen_width - score_enemy_size), 0]
score_enemy_list = [score_enemy_pos]
score_enemy_speed = 0.3

# フォント
font = pygame.font.Font(None, 36)
countdown_font = pygame.font.Font(None, 800)

# 時間経過ではやくするか否か
time_increase_speed = True;

clock = pygame.time.Clock()

# カウントダウン用の変数
countdown_duration = 3  # カウントダウンの秒数
countdown_start_time = pygame.time.get_ticks()  # カウントダウンの開始時刻


# カウントダウンループ
while countdown_duration > 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(WHITE)
    countdown_text = countdown_font.render(f"{countdown_duration}", True, BLACK)
    screen.blit(countdown_text, (screen_width // 2 - 150, screen_height // 8))
    pygame.display.update()

    # 1秒ごとにカウントダウンを減らす
    if pygame.time.get_ticks() - countdown_start_time >= 1000:
        countdown_duration -= 1
        countdown_start_time = pygame.time.get_ticks()

    clock.tick(1)

running = True
game_over = False

# メインループ
while not game_over:
    # イベント処理 
    #ちなみにbulletは銃弾って意味よ
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_pos.append([player_pos[0] + player_size // 2, player_pos[1]])

    # プレイヤーの移動
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT]:
        player_pos[0] += player_speed

    # 敵の移動
    for enemy_pos in enemy_list:
        enemy_pos[1] += enemy_speed

    # 弾の移動
    for bullet in bullet_pos:
        bullet[1] -= bullet_speed
        
    
    # スコアアップ敵の移動
    for score_enemy_pos in score_enemy_list:
        score_enemy_pos[1] += score_enemy_speed    

    # 敵の生成
    #randintの数をおっきくすればするほど敵少なくなるよ
    if random.randint(0, 500) < 2:
        enemy_list.append([random.randint(0, screen_width - enemy_size), 0])

    # スコアアップ敵の生成
    if random.randint(0, 100) < 1:
        score_enemy_list.append([random.randint(0, screen_width - score_enemy_size), 0])

    # 当たり判定
    for enemy_pos in enemy_list:
        if enemy_pos[1] > screen_height:
            enemy_list.remove(enemy_pos)
            score += 1
            if time_increase_speed:
                enemy_speed += score * 0.000001

        if (player_pos[0] <= enemy_pos[0] and player_pos[0] + player_size >= enemy_pos[0]) or \
                (player_pos[0] >= enemy_pos[0] and player_pos[0] <= enemy_pos[0] + enemy_size):
            if player_pos[1] <= enemy_pos[1] + enemy_size:
                game_over = True

        for bullet in bullet_pos:
            if (bullet[0] >= enemy_pos[0] and bullet[0] <= enemy_pos[0] + enemy_size) and \
                    (enemy_pos[1] >= bullet[1] and enemy_pos[1] <= bullet[1] + bullet_size):
                enemy_list.remove(enemy_pos)
                bullet_pos.remove(bullet)
                score += 10
                enemy_speed += score * 0.0001
                
    # スコアアップ敵との当たり判定
    for score_enemy_pos in score_enemy_list:
        if score_enemy_pos[1] > screen_height:
            score_enemy_list.remove(score_enemy_pos)

        if (player_pos[0] <= score_enemy_pos[0] and player_pos[0] + player_size >= score_enemy_pos[0]) or \
                (player_pos[0] >= score_enemy_pos[0] and player_pos[0] <= score_enemy_pos[0] + score_enemy_size):
            if player_pos[1] <= score_enemy_pos[1] + score_enemy_size:
                score_enemy_list.remove(score_enemy_pos)
                score += 1
                enemy_speed += score * 0.00001

    # 画面の描画
    screen.fill(WHITE)

    # プレイヤーの画像描画
    screen.blit(player_image, player_pos)

    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, RED, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

    for bullet in bullet_pos:
        pygame.draw.circle(screen, BLUE, (bullet[0], bullet[1]), bullet_size, 0)

    for score_enemy_pos in score_enemy_list:
        pygame.draw.rect(screen, (0, 255, 0), (score_enemy_pos[0], score_enemy_pos[1], score_enemy_size, score_enemy_size))

    # スコアの描画
    score_text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(score_text, (50, 50))
    pygame.display.update()
"""
# ゲームオーバー表示
font = pygame.font.Font(None, 90)
game_over_text = font.render("Game Over", True, BLACK)
screen.blit(game_over_text, (screen_width // 2 - 200, screen_height // 2 - 37))
pygame.display.update()

#game_over_text = font.render("Game Over", True, RED)
#screen.blit(game_over_text, (screen_width // 2 - 100, screen_height // 2 - 18))
#pygame.display.update()

# 3秒待機
pygame.time.wait(3000)

# 終了
pygame.quit()
"""

# ゲームオーバー表示
font = pygame.font.Font(None, 130)
game_over_text = font.render("Game Over", True, BLACK)
screen.blit(game_over_text, (screen_width // 2 - 250, screen_height // 2 - 120))
pygame.display.update()

# スコアを描画
font = pygame.font.Font(None, 100)
score_text = font.render("Your Score: " + str(score), True, BLACK)
score_text_rect = score_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
screen.blit(score_text, score_text_rect)
pygame.display.update()

# 10秒待機
pygame.time.wait(3000)

# 終了
pygame.quit()
