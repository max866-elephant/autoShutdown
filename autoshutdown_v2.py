import tkinter as tk
from tkinter import ttk
import subprocess
from datetime import datetime, timedelta


# 獲取目前系統日期
current_date = datetime.now().strftime("%Y-%m-%d")

# 預設的關機時間
default_shutdown_hour = 22
default_shutdown_minute = 0
current_shutdown_text = ''

def set_shutdown_time():
    global shutdown_time, current_shutdown_text
    
    # 獲取目前系統時間
    current_time = datetime.now()

    # 取得使用者設定的關機時間
    shutdown_hour = int(hour_combo.get())
    shutdown_minute = int(minute_combo.get())

    # 設定關機時間
    shutdown_time = datetime.strptime(f"{current_date} {shutdown_hour:02d}:{shutdown_minute:02d}", "%Y-%m-%d %H:%M")
    
    # 更新目前的關機時間文字
    current_shutdown_text = f"已設定{current_date} {shutdown_hour:02d}:{shutdown_minute:02d} 自動關機"

    # 如果選擇的關機時間在當前時間之前，表示是隔一天的時間
    if shutdown_time <= current_time:
        shutdown_time += timedelta(days=1)

    # 計算關機時間和目前系統時間的差異秒數
    time_difference = round((shutdown_time - current_time).total_seconds())

    
    # Perform shutdown command (for demonstration)
    # subprocess.run(["shutdown", "/s", "/t", "60"])  # Uncomment this line to enable shutdown command
    subprocess.run(["shutdown", "/s", "/t", f"{time_difference}"])  
    
    # Disable start countdown button
    start_countdown_button.config(state="disabled")
      
    # Update current_shutdown_label
    update_shutdown_text = f"已設定{shutdown_time}自動關機"
    current_shutdown_label.config(text=update_shutdown_text, font=('微軟正黑體', 14, 'bold'), foreground='red')

def set_countdown_time():
    # 取得使用者設定的倒數關機時間
    countdown_minute = int(countdown_combo.get())

    # 計算倒數關機時間的秒數
    countdown_seconds = countdown_minute * 60

    # 執行倒數關機指令
    subprocess.run(["shutdown", "/s", "/t", str(countdown_seconds)])

    # 禁用設定關機時間按鈕
    shutdown_button.config(state="disabled")

    # 更新目前的關機時間文字
    countdown_shutdown_text = f"已設定倒數{countdown_minute:02d}分鐘後自動關機"
    
    # Update current_shutdown_label
    current_shutdown_label.config(text=countdown_shutdown_text, font=('微軟正黑體', 14, 'bold'), foreground='red')

def cancel_shutdown():
    # 執行取消關機指令
    subprocess.run(["shutdown", "/a"])

    # 啟用設定關機時間按鈕和設定倒數關機時間按鈕
    shutdown_button.config(state="normal")
    start_countdown_button.config(state="normal")

    # Update current_shutdown_label
    cancel_shutdown_text = f"已取消自動關機"
    current_shutdown_label.config(text=cancel_shutdown_text, font=('微軟正黑體', 14, 'bold'), foreground='red')


# 創建主視窗
root = tk.Tk()
root.title("減災監測組資訊管理科 預約關機程式 v1")
root.geometry("600x220")

# 獲取目前系統時間
current_time = datetime.now()

# 設定關機時間
default_shutdown_time = datetime.strptime(f"{current_date} {default_shutdown_hour:02d}:{default_shutdown_minute:02d}", "%Y-%m-%d %H:%M")

# 如果目前的時間在22:00時間之後，表示要隔一天的時間
if default_shutdown_time <= current_time:
    default_shutdown_time += timedelta(days=1)
print(f'current_time: {current_time}')
print(f'default_shutdown_time: {default_shutdown_time}')
# 計算關機時間和目前系統時間的差異秒數
default_time_difference = round((default_shutdown_time - datetime.now()).total_seconds())
print(f'default_time_difference: {default_time_difference}')
# 執行關機指令
subprocess.run(["shutdown", "/s", "/t", f"{default_time_difference}"])
current_shutdown_text = f"已設定{default_shutdown_time}自動關機"

# 創建標籤顯示目前設定的關機時間
current_shutdown_label = ttk.Label(root, text=current_shutdown_text, font=('微軟正黑體', 14, 'bold'))
current_shutdown_label.grid(row=0, column=0, columnspan=4, padx=10, pady=5)


# 創建標籤顯示設定關機時間
shutdown_label = ttk.Label(root, text="設定關機時間 (HH:MM):", font=('微軟正黑體', 14))
shutdown_label.grid(row=1, column=0, columnspan=1, padx=10, pady=5)

# 創建下拉選單選擇小時
hour_options = [str(i).zfill(2) for i in range(24)]
hour_combo = ttk.Combobox(root, values=hour_options, state="readonly", width=5, font=('微軟正黑體', 14))
hour_combo.grid(row=1, column=1, padx=5, pady=5)
hour_combo.current(default_shutdown_hour)

# 創建標籤顯示冒號
colon_label = ttk.Label(root, text=":", font=('微軟正黑體', 14))
colon_label.grid(row=1, column=2, padx=5, pady=5)

# 創建下拉選單選擇分鐘
minute_options = [str(i).zfill(2) for i in range(60)]
minute_combo = ttk.Combobox(root, values=minute_options, state="readonly", width=5, font=('微軟正黑體', 14))
minute_combo.grid(row=1, column=3, padx=5, pady=5)
minute_combo.current(default_shutdown_minute)

# 創建標籤顯示設定倒數關機時間
countdown_label = ttk.Label(root, text="設定倒數關機時間 (minutes):", font=('微軟正黑體', 14))
countdown_label.grid(row=2, column=0, padx=10, pady=5)

# 創建下拉選單選擇倒數分鐘
countdown_options = ["5", "10", "15", "30", "60", "120"]
countdown_combo = ttk.Combobox(root, values=countdown_options, state="readonly", width=5, font=('微軟正黑體', 14))
countdown_combo.grid(row=2, column=1, padx=5, pady=5)
countdown_combo.current(0)

# 創建按鈕設定關機時間
shutdown_button = ttk.Button(root, text="設定關機時間", command=set_shutdown_time)
shutdown_button.grid(row=3, column=0, padx=10, pady=10)

# 創建按鈕設定倒數關機時間
start_countdown_button = ttk.Button(root, text="設定倒數關機時間", command=set_countdown_time)
start_countdown_button.grid(row=3, column=1, padx=10, pady=10)

# 創建按鈕立即關機
shutdown_now_button = ttk.Button(root, text="取消預備關機", command=cancel_shutdown)
shutdown_now_button.grid(row=3, column=3, padx=10, pady=10)

# 提醒
memo_label = ttk.Label(root, text="設定完成後直接關閉視窗即可!", font=('微軟正黑體', 14, 'bold'))
memo_label.grid(row=4, column=0, columnspan=1, padx=10, pady=5)


# 設定視窗大小不可調整
root.resizable(False, False)

root.mainloop()
