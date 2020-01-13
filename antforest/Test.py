import os
from PIL import Image
import time

# 唤醒屏幕
os.system("adb shell input keyevent 224")
# 下滑出现密码界面
os.system("adb shell input swipe 300 1000 300 500")
# 打开支付宝
os.system("adb shell am start com.eg.android.AlipayGphone/.AlipayLogin")