import pygame
import random
import sys

# 初期設定
def run_game():
    pygame.init()

screen_width = 900
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("新妻先生おにごっこ")

# 色の定義
white = (100, 100, 100)
blue = (0, 0, 255)
red = (200, 10, 100)
yellow = (255, 255, 0)
black = (0, 200, 200)
aaa = (0,0,0)

# プレイヤーと敵の初期位置
enemies = [[random.randint(0, screen_width - 30), random.randint(0, screen_height - 30)]]
num_enemies = 1

# プレイヤーの画像ロード
player_image = pygame.image.load("player1.png")
player_size = 120
player_image = pygame.transform.scale(player_image, (player_size, player_size))
player_pos = [screen_width // 2, screen_height - player_size * 2]

# コインの初期位置
coins = [[random.randint(0, screen_width - 20), random.randint(0, screen_height - 20)] for _ in range(10)]

# スコア
score = 0

# フォントの設定
font = pygame.font.Font(None, 100)
countdown_font = pygame.font.Font(None, 800)

# ゲーム開始時間を追跡する変数
import pygame.time
start_time = pygame.time.get_ticks()  # ミリ秒単位の現在時刻

clock = pygame.time.Clock()

# カウントダウン用の変数
countdown_duration = 3  # カウントダウンの秒数
countdown_start_time = pygame.time.get_ticks()  # カウントダウンの開始時刻

# カウントダウンループ
while countdown_duration > 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(white)
    countdown_text = countdown_font.render(f"{countdown_duration}", True, black)
    screen.blit(countdown_text, (screen_width // 2 - 150, screen_height // 8))
    pygame.display.update()

    # 1秒ごとにカウントダウンを減らす
    if pygame.time.get_ticks() - countdown_start_time >= 1000:
        countdown_duration -= 1
        countdown_start_time = pygame.time.get_ticks()

    clock.tick(1)

running = True
game_over = False
# コインを生成する関数
def spawn_coin():
    coins.append([random.randint(0, screen_width - 100), random.randint(0, screen_height - 100)])


# ゲームループ
running = True
while running:
    current_time = pygame.time.get_ticks()  # ミリ秒単位の現在時刻
    elapsed_time = (current_time - start_time) / 1000  # 経過時間を秒に変換

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= 1
    if keys[pygame.K_RIGHT]:
        player_pos[0] += 1
    if keys[pygame.K_UP]:
        player_pos[1] -= 1
    if keys[pygame.K_DOWN]:
        player_pos[1] += 1

    # プレイヤーがウィンドウ外に出たら反対側からワープ
    if player_pos[0] > screen_width:
        player_pos[0] = -player_size
    if player_pos[0] < -player_size:
        player_pos[0] = screen_width
    if player_pos[1] > screen_height:
        player_pos[1] = -player_size
    if player_pos[1] < -player_size:
        player_pos[1] = screen_height

    # 敵を増やす
    while score >= 10 * num_enemies:
        num_enemies += 1
        enemies.append([random.randint(0, screen_width - 50), random.randint(0, screen_height - 50)])

    # 経過時間が10秒未満の場合、敵の動きを停止
    if elapsed_time < 10:
        for enemy in enemies:
            enemy[0] = enemy[0]  # X座標の位置を固定
            enemy[1] = enemy[1]  # Y座標の位置を固定
    else:
        # 経過時間が10秒以上の場合、通常の敵の動きを実行
        for enemy in enemies:
            enemy[0] += random.randint(-3, 3)
            enemy[1] += random.randint(-3, 3)

            # 敵がプレイヤーを追いかける
            if enemy[0] < player_pos[0]:
                enemy[0] += 0.3
            else:
                enemy[0] -= 0.3
            if enemy[1] < player_pos[1]:
                enemy[1] += 0.3
            else:
                enemy[1] -= 0.3

    # 当たり判定（プレイヤーと敵）
    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy[0], enemy[1], 30, 30)  # 敵の画像サイズを使う
        player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
        if player_rect.colliderect(enemy_rect):
            running = False

    # 当たり判定（プレイヤーとコイン）
    for coin in coins:
        coin_rect = pygame.Rect(coin[0], coin[1], 20, 20)  # コインの画像サイズを使う
        player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
        if player_rect.colliderect(coin_rect):
            coins.remove(coin)
            score += 1

    # コインがなくなったら新しいコインを生成
    if len(coins) == 0:
        spawn_coin()
        coins.append([random.randint(0, screen_width - 100), random.randint(0, screen_height - 100)])

    # 描画
    screen.fill(white)
    pygame.draw.rect(screen, blue, (player_pos[0], player_pos[1], player_size, player_size))
    for enemy in enemies:
        pygame.draw.rect(screen, red, (enemy[0], enemy[1], 30, 30))  # 敵の画像サイズを使う
    for coin in coins:
        pygame.draw.circle(screen, yellow, (coin[0], coin[1]), 10)

    screen.blit(player_image, player_pos)

    # スコアを描画
    score_text = font.render(f"Score: {score}", True, black)
    screen.blit(score_text, (10, 10))

    pygame.display.update()

# ゲームオーバー画面
game_over_text = font.render("Game Over", True, red)
screen.blit(game_over_text, (screen_width // 2 - 200, screen_height // 2 - 37))

# スコアを表示
score_text = font.render(f"Score: {score}", True, black)
screen.blit(score_text, (screen_width // 2 - 120, screen_height // 2 + 50))

pygame.display.update()

# 待機時間（例: 10秒）
pygame.time.wait(3000)

# ゲーム終了
pygame.quit()
