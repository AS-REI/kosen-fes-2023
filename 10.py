import pygame
import random
import sys
#import code1
#import code2
#import code3

pygame.init()

# 画面の設定
screen_width, screen_height = 1000, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("ゲーム選択")

# 日本語フォントの設定
font = pygame.font.Font(r"C:\Users\ryzen\OneDrive\デスクトップ\新妻ゲーム\BIZ-UDGOTHICB.TTC", 60)

# 色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 画像の読み込み
image = pygame.image.load("player1.png")  # 画像を読み込む

# 画像の表示位置設定
image_x = screen_width // 1.5 - image.get_width() //3   # 画像のx座標
image_y = screen_height // 1.7 - image.get_height() // 2  # 画像のy座標

# メインループ
show_title_screen = True
while show_title_screen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                # 新妻落下ゲームの起動
                show_title_screen = False
                import code1  # 新妻落下ゲームのコードをインポート
                code1.run_game()  # 新妻落下ゲームを実行
            elif event.key == pygame.K_2:
                # 新妻シューティングゲームの起動
                show_title_screen = False
                import code2  # 新妻シューティングゲームのコードをインポート
                code2.run_game()  # 新妻シューティングゲームを実行
            elif event.key == pygame.K_3:
                # 新妻おにごっこの起動
                show_title_screen = False
                import code3  # 新妻おにごっこのコードをインポート
                code3.run_game()  # 新妻おにごっを実行

    # タイトル画面表示
    screen.fill(WHITE)
    title_text = font.render("新妻先生 げーむ", True, BLACK)
    code1_text = font.render("1. 避けげー", True, BLACK)
    code2_text = font.render("2. 撃つげー", True, BLACK)
    code3_text = font.render("3. 逃げげー", True, BLACK)

    # 画像を描画
    screen.blit(image, (image_x, image_y))

    screen.blit(title_text, (screen_width // 2 - 250, screen_height // 4))
    screen.blit(code1_text, (screen_width // 3.4 - 100, screen_height // 2 - 37))
    screen.blit(code2_text, (screen_width // 3.4 - 100, screen_height // 2 + 50))
    screen.blit(code3_text, (screen_width // 3.4 - 100, screen_height // 2 + 137))
    pygame.display.update()
