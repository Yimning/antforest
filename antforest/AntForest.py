import os
from PIL import Image
import time


class AntForest:
    # 几种屏幕类型
    ALIPAY_HOME = 1
    ANT_FOREST_HOME = 2
    FRIENDS_PAGE = 3
    WAITING_PAGE = 4

    def __init__(self, path, sec=2):
        self.path = path
        self.sec = sec
        self.im_rgb: Image.Image = None
        self.initialize()

    def initialize(self):
        # 唤醒屏幕
        os.system("adb shell input keyevent 224")
        # 下滑出现密码界面
        os.system("adb shell input swipe 300 1000 300 500")
        # 输入密码解锁
        os.system("adb shell input text 199685")
        # 打开支付宝
        os.system("adb shell am start com.eg.android.AlipayGphone/.AlipayLogin")
        time.sleep(self.sec + 1)

    # 获取手机截图并返回截图存储路径
    def get_screen_shot(self):
        # 截图之前先清理上一次的内容
        self.clean()
        # 睡眠一会儿
        time.sleep(1)
        # 截屏到手机上临时存储
        os.popen("adb shell screencap -p /data/local/tmp/tmp.png")
        time.sleep(self.sec)
        # 将其转移到电脑里
        temp_open = os.popen("adb pull /data/local/tmp/tmp.png " + self.path)
        # 睡眠等待一会儿再返回 截图时间花费比较长
        time.sleep(self.sec)
        # 储存图片到变量中
        self.im_rgb = Image.open(self.path).convert("RGB")
        # 返回电脑中图片位置
        return self.path

    def clean(self):
        # 关闭打开的图片
        if self.im_rgb != None:
            self.im_rgb.close()
        # 删除手机上的临时文件
        os.popen("adb shell rm /data/local/tmp/tmp.png")
        # 删除电脑上的临时文件
        if os.path.exists(self.path):
            os.remove(self.path)

    @staticmethod
    def sleep(self):
        # 熄屏
        os.system("adb shell input keyevent 223")

    # 判断当前页面种类
    def page_classify(self):
        r, b, g = self.im_rgb.getpixel((500, 300))
        if (r, g, b) == (255, 255, 255):
            # 是好友列表
            return self.FRIENDS_PAGE
        elif (r, g, b) == (27, 130, 210):
            # 是支付宝首页
            return self.ALIPAY_HOME
        elif (r, g, b) == (48, 191, 108):
            # 是等待页面
            return self.WAITING_PAGE
        else:
            # 是森林页面
            return self.ANT_FOREST_HOME

    # 是支付宝首页，点进蚂蚁森林页面
    def alipay_to_forest(self):
        os.system("adb shell input tap 130 710")
        time.sleep(2)

    # 从森林页面到好友列表
    def forest_to_friends(self):
        # 先滑到底
        os.system("adb shell input swipe 300 1000 300 50")
        os.system("adb shell input swipe 300 1000 300 50")
        os.system("adb shell input swipe 300 1000 300 50")
        # 点击查看更多好友
        os.system("adb shell input tap 500 777")

    # 从好友列表到森林页
    def friends_to_forest(self):
        # 两次返回
        os.system("adb shell input keyevent 4")
        os.system("adb shell input keyevent 4")
        time.sleep(0.4)
        self.alipay_to_forest()

    # 返回按钮
    def tap_back(self):
        os.system("adb shell input tap 55 155")

    # 搜寻当前屏幕可收取能量的好友并点击进去收能量
    def get_friends_power_in_current_screen(self):
        # 更新一下屏幕截图
        self.get_screen_shot()
        for i in range(230, 2180, 55):
            for y in range(i, i + 55):
                # 如果找到可收取
                if self.im_rgb.getpixel((1079, y)) == (29, 160, 109):
                    i += 130
                    # 点击进去
                    os.system("adb shell input tap " + str(500) + " " + str(y + 20))
                    time.sleep(2)
                    # 更新一下屏幕截图
                    self.get_screen_shot()
                    # 收取能量
                    self.get_power()
                    # 返回好友列表
                    self.tap_back()
                    break

    # 好友列表收取能量
    def get_all_friends_power(self):
        # 先滑到底
        for i in range(0, 6):
            os.system("adb shell input swipe 300 2000 300 50")
            time.sleep(0.4)
        # 然后一页一页收取能量
        for i in range(10):
            self.get_friends_power_in_current_screen()
            os.system("adb shell input swipe 300 500 300 1500")

    # 收取能量
    def get_power(self):
        for x in range(100, 1000):
            for y in range(450, 800, 5):
                if self.im_rgb.getpixel((x, y)) == (34, 134, 112):
                    # todo 进来太多次了 优化一下
                    print(x, y)
                    os.system("adb shell input tap " + str(x) + " " + str(y))
                    x += 100
                    break


if __name__ == "__main__":
    # 截图存放路径
    path = os.getcwd() + "/tmp.png"
    # 初始化
    ant_forest = AntForest(path, 2)
    # 先获得屏幕截图
    ant_forest.get_screen_shot()
    # 判断当前页面
    page = ant_forest.page_classify()
    # 如果是支付宝首页，进入蚂蚁森林
    if page == ant_forest.ANT_FOREST_HOME:
        ant_forest.alipay_to_forest()
        ant_forest.get_screen_shot()
    # 如果是好友列表 回到蚂蚁森林首页
    elif page == ant_forest.FRIENDS_PAGE:
        ant_forest.friends_to_forest()
        ant_forest.get_screen_shot()
    # 如果是森林首页 开始操作
    elif page == ant_forest.ANT_FOREST_HOME:
        pass
    elif page == ant_forest.WAITING_PAGE:
        time.sleep(1)

    # 首先收取自己的能力
    ant_forest.get_power()
    # 然后进入好友列表收取能量
    ant_forest.forest_to_friends()
    ant_forest.get_all_friends_power()
