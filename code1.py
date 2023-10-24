import pygame
import sys
import random


pygame.init()

# 画面のサイズ
screen_width, screen_height = 1000, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("新妻")

# 色
white = (250, 200, 200)
BLACK = (200, 150, 0)

# フォント
font = pygame.font.Font(None, 36)
countdown_font = pygame.font.Font(None, 800)

# プレイヤー
player_width, player_height = 30, 30
player = pygame.Rect(screen_width // 2, screen_height - player_height, player_width, player_height)


# 敵の画像ロード
enemy_imgs = [
    pygame.image.load('enemy.png'),
    pygame.image.load('enemy2.png'),
    pygame.image.load('enemy3.png')
]

enemy_width, enemy_height = 70, 70

# 敵クラス
class Enemy:
    def __init__(self):
        self.x = random.randint(0, screen_width - enemy_width)
        self.y = 0
        self.id = random.randint(0, 2);

    def move(self, speed):
        self.y += speed

# ゲームループ
clock = pygame.time.Clock()
score = 0
start_time = pygame.time.get_ticks()  # ゲーム開始時刻を取得
enemy_speed = 5
speed_increment_interval = 30000  # スピードを増加させる間隔（ミリ秒）

# カウントダウン用の変数
countdown_duration = 3  # カウントダウンの秒数
countdown_start_time = pygame.time.get_ticks()  # カウントダウンの開始時刻

# カウントダウンループ
while countdown_duration > 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(white)
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

# ゲームループ（カウントダウン後）

# 敵リスト
enemy_list = []

running = True
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.move_ip(-5, 0)
    if keys[pygame.K_RIGHT] and player.right < screen_width:
        player.move_ip(5, 0)

    # 敵を追加
    if random.randint(1, 100) < 15:
        enemy_list.append(Enemy())

    # 敵の落下
    for enemy in enemy_list:
        enemy.move(enemy_speed)
        if enemy.y > screen_height:
            enemy_list.remove(enemy)
            score += 1

        # 衝突判定
        enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy_width, enemy_height)
        if player.colliderect(enemy_rect):
            game_over = True

    # 画面描画
    screen.fill(white)
    pygame.draw.rect(screen, (255, 0, 0), player)

    # 敵の画像描画
    for enemy in enemy_list:
        screen.blit(enemy_imgs[enemy.id], (enemy.x, enemy.y))

    # 経過時間を表示
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # ミリ秒から秒に変換
    time_text = font.render(f"Run NITSUMA: {elapsed_time} km", True, BLACK)
    screen.blit(time_text, (10, 10))

    # 一定の間隔で敵のスピードを増加させる
    if elapsed_time > 20 and elapsed_time % (speed_increment_interval // 1000) == 0:
        enemy_speed += 10

    pygame.display.update()
    clock.tick(50)

    if game_over:
        # Clear the screen
        screen.fill(white)

        # Display "Game Over" text
        game_over_font = pygame.font.Font(None, 90)
        game_over_text = game_over_font.render("Game Over", True, BLACK)
        screen.blit(game_over_text, (screen_width // 2 - 200, screen_height // 2 - 37))

        # Display the final score
        final_score_text = font.render(f"Final Score: {score}", True, BLACK)
        screen.blit(final_score_text, (screen_width // 2 - 120, screen_height // 2 + 50))

        pygame.display.update()

        pygame.time.delay(10000)  # Wait for 10 seconds
        running = False

# Close the pygame window
pygame.quit()


