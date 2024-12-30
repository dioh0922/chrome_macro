#import win32gui
#import win32con
import time
import pyautogui
import pygetwindow as gw
from PIL import ImageGrab

'''
# 特定のウィンドウを取得する
def find_chrome_window():
    def enum_windows_callback(hwnd, windows_list):
        title = win32gui.GetWindowText(hwnd)
        if "Google Chrome" in title:
            windows_list.append(hwnd)
    windows = []
    win32gui.EnumWindows(enum_windows_callback, windows)
    return windows
'''

windows = gw.getAllWindows()

# 取得したウィンドウの情報を表示
for index, window in enumerate(windows):
  print(f"index:{index}, Window Title: {window.title}, ID: {window._hWnd}, Position: {window.left}, {window.top}, Size: {window.width}x{window.height}")

user_input = input("操作したいウィンドウのIDを入力してください: ")


try:
  target_window = windows[int(user_input)]

  # 入力されたIDに該当するウィンドウがあればアクティブにする
  if target_window:
    print(f"ウィンドウ '{target_window.title}' をアクティブにします。")
    target_window.activate()
    target_window.restore() 
    time.sleep(1)

    pyautogui.press('left')  # Tabキーを押す
    time.sleep(1)

    # スクリーンショットをキャプチャ（画面全体のスクリーンショット）
    screenshot = ImageGrab.grab()  # 画面全体のスクリーンショット

    # スクリーンショットを保存
    screenshot.save("screenshot.png")

    # スクリーンショットを表示（オプション）
    screenshot.show()

  else:
    print("指定したIDのウィンドウが見つかりませんでした。")
except ValueError:
  print("無効なIDが入力されました。IDは整数で入力してください。")

exit(0)

#windows = gw.getWindowsWithTitle("Chrome")  # Chromeウィンドウを探す
windows = None
# Chromeウィンドウが見つかった場合
if windows:
  chrome_window = windows[0]  # 最初に見つかったウィンドウを選択
  chrome_window.activate()  # ウィンドウをアクティブにする
  chrome_window.restore()  # 最小化されている場合は復元する

  # 少し待機して、ブラウザがアクティブになるのを待つ
  time.sleep(1)

  # キーストロークを送信（例：Tabキーを押す）
  pyautogui.press('left')  # Tabキーを押す
  time.sleep(1)

  # スクリーンショットをキャプチャ（画面全体のスクリーンショット）
  screenshot = ImageGrab.grab()  # 画面全体のスクリーンショット

  # スクリーンショットを保存
  screenshot.save("screenshot.png")

  # スクリーンショットを表示（オプション）
  screenshot.show()

else:
  print("Chromeウィンドウが見つかりませんでした")