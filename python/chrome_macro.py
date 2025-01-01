import time
import pyautogui
import os
import pygetwindow as gw
from PIL import ImageGrab

import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
from PIL import Image


parent_dir = "tmp"
dir_name = "result"
image = None
cropped_image = None
start_x, start_y, end_x, end_y = -1, -1, -1, -1  # マウスイベントで使う変数
drawing = False  # マウスドラッグの状態

def makedir():
  full_path = os.path.join(parent_dir, dir_name)

  # tmpディレクトリが存在しない場合は作成する
  if not os.path.exists(parent_dir):
      os.makedirs(parent_dir)

  # 新しいディレクトリが存在しない場合に作成する
  if not os.path.exists(full_path):
      os.makedirs(full_path)

def screenShot(i):
  # スクリーンショットをキャプチャ（画面全体のスクリーンショット）
  screenshot = ImageGrab.grab()  # 画面全体のスクリーンショット

  # スクリーンショットを保存
  screenshot.save(f"{os.path.join(parent_dir, dir_name)}/{i + 1:04d}.png")

  pyautogui.press('left')  # Tabキーを押す
  time.sleep(1)

def load_image(image_path):
  global image
  image = Image.open(image_path)  # 画像を読み込んでグローバル変数に保存

def onselect(eclick, erelease):
  global cropped_image
  global image
  global start_x, start_y, end_x, end_y
  # 矩形の座標を取得
  start_x, start_y = int(eclick.xdata), int(eclick.ydata)
  end_x, end_y = int(erelease.xdata), int(erelease.ydata)
  
  # 画像を切り出す
  cropped_image = image.crop((start_x, start_y, end_x, end_y))
  plt.close()


def cropAllImage():
  #TODO: result/tmpのみにしたい
  for dirpath, dirnames, filenames in os.walk(os.path.join(parent_dir, dir_name)):
    for filename in filenames:
      # 各ファイルのフルパスを作成
      file_path = os.path.join(parent_dir, dir_name, filename)
      cropTarget(file_path)

def cropTarget(image_path):
  global start_x, start_y, end_x, end_y
  print(image_path)
  target_image = Image.open(image_path) 
  image_array = target_image.convert("RGB")
  edit_image = target_image.crop((start_x, start_y, end_x, end_y))
  edit_image.save(image_path.replace('.png', '.jpg'), format="JPEG", quality=60)
  os.remove(image_path)

def main():
  windows = gw.getAllWindows()

  # 取得したウィンドウの情報を表示
  for index, window in enumerate(windows):
    print(f"ID:{index}, Window Title: {window.title}, ID: {window._hWnd}, Position: {window.left}, {window.top}, Size: {window.width}x{window.height}")

  user_input = input("操作したいウィンドウのIDを入力してください: ")

  try:
    target_window = windows[int(user_input)]

    # 入力されたIDに該当するウィンドウがあればアクティブにする
    if target_window:
      print(f"ウィンドウ '{target_window.title}' をアクティブにします。")

      #title = input("タイトルを入力：")
      page = int(input("ページ数を入力(の半分を繰り返す)："))
      page = int(page / 2) + 1
      makedir()

      target_window.activate()
      target_window.restore() 
      time.sleep(1)

      for i in range(page): 
        screenShot(i)

      # 画像の読み込み
      image_path = f"{parent_dir}/{dir_name}/{1:04d}.png"  # 画像ファイルのパス
      load_image(image_path)
      image_array = image.convert("RGB")
      # 切り抜きのための範囲選択

      # 画像を表示し、ユーザーに矩形選択を促す
      fig, ax = plt.subplots(figsize=(10, 8), dpi=180)
      ax.imshow(image_array)

      # RectangleSelectorを設定
      selector = RectangleSelector(ax, onselect, useblit=True, button=[1], spancoords='pixels', interactive=True)
      plt.show()

      # 切り抜いた画像があれば表示（選択後に実行される）
      if cropped_image:
        cropAllImage()
    else:
      print("指定したIDのウィンドウが見つかりませんでした。")
  except ValueError:
    print("無効なIDが入力されました。IDは整数で入力してください。")


if __name__ == "__main__":
    main()