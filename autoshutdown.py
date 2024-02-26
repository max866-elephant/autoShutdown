import os
import subprocess
import threading
import time
import tkinter as tk
import sys

def shutdown():
    log("關機")
    subprocess.run(["shutdown", "/f", "/s", "/t", "0"], check=True)

def log(message):
    """寫入日誌

    Args:
        message: 日誌訊息
    """

    with open("log.txt", "a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}: {message}\n")



def ask_shutdown():
    """詢問是否關機

    Returns:
        True 表示繼續使用，False 表示關機
    """

    root = tk.Tk()
    root.withdraw()

    # 建立視窗
    window = tk.Toplevel(root)
    window.title("關機確認")
    window.geometry("500x150")

    # 設定視窗置中
    window.update_idletasks()
    x = (root.winfo_screenwidth() - window.winfo_width()) // 2
    y = (root.winfo_screenheight() - window.winfo_height()) // 2
    window.geometry(f"+{x}+{y}")

    # 建立標籤
    label = tk.Label(window, text="已偵測到您的電腦未關機，請問是否繼續使用？ \n60秒後未操作將自動關機", font=("微軟正黑體", 14))
    label.pack()
    
    # 建立倒數計時器
    countdown_label = tk.Label(window, text="60", font=("微軟正黑體", 14), fg="red")
    countdown_label.pack()

    # 建立按鈕
    frame = tk.Frame(window)
    frame.pack()

    yes_button = tk.Button(frame, text="繼續使用", command=lambda: sys.exit(), fg="white", bg="green", width=10, height=2, font=("consolas", 12))
    yes_button.pack(side="left")
    
    # 在兩個按鈕之間放入一個空格
    label = tk.Label(frame, text=" ")
    label.pack(side="left")
    
    no_button = tk.Button(frame, text="關機", command=lambda: shutdown(), fg="white", bg="red", width=10, height=2, font=("consolas", 12))
    no_button.pack(side="right")

    # 設定計時器
    def countdown():
        for i in range(60):
            time.sleep(1)
            countdown_label.config(text=str(60 - i))
        shutdown()


    thread = threading.Thread(target=countdown)
    thread.start()
    
    # 設定視窗大小不可調整
    window.resizable(False, False)
    
    # 顯示視窗
    window.mainloop()

    # 記錄使用者選擇
    log(f"使用者選擇 {'繼續使用' if window.winfo_exists() else '關機'}")

    return window.winfo_exists()

def main():
    # 記錄程式開始執行
    log("程式開始執行")

    # 建立一個計時器，每隔1秒檢查一次時間
    while True:
        # 檢查時間
        now = time.localtime()
        if now.tm_hour == 22 and now.tm_min == 00:
            # 詢問是否關機
            if not ask_shutdown():
                # 執行關機命令
                subprocess.run(["shutdown", "/f", "/s", "/t", "0"], check=True)

        # 睡眠1秒
        time.sleep(1)

if __name__ == "__main__":
    # 記錄程式開始執行
    log("程式開始執行")

    # 執行主程式
    main()
    

    # 記錄程式結束執行
    log("程式結束執行")
