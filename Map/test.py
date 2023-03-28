import win32api

# 获取显示器分辨率
width = win32api.GetSystemMetrics(0)
height = win32api.GetSystemMetrics(1)

# 打印分辨率信息
print("Display width: ", width)
print("Display height: ", height)
