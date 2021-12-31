###################################################################
#
#           MM     MM
#           MMM   MMM
#           MMMM MMMM
#           MM MMM MM
#           MM  M  MM
#           MM     MM
#          MMMM   MMMM     AaronMing 2020
#
#       贪食蛇，游戏控制单元
#
###################################################################


from pybricks.hubs import EV3Brick
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.media.ev3dev import Font  # 引入字体类

from UMSGround import MSGround
from UMSnake import *
import time


# 调用主机
ev3 = EV3Brick()


class MSControler:
    # 构造函数
    def __init__(self, ASnake, AFood):
        self.ASnake = ASnake  # 蛇
        self.AFood = AFood
        self.ALevel = 1  # 当前等级
        self.TopScore = 0  # 最高分
        self.LoadTopScore()
        ev3.speaker.set_speech_options(language=None, voice="f2", speed=180, pitch=None)
        ev3.speaker.set_volume(5, which="Beep")
        chinese_font = Font(size=12, lang="zh-cn")
        big_font = Font(size=12, bold=True)
        ev3.screen.set_font(chinese_font)

    # 读取最高分数
    def LoadTopScore(self):
        # 打开保存最高分的文件
        FTopScore = open("score.txt", "r")
        score = FTopScore.readline()  # 读取第一行
        self.TopScore = int(score)  # 把自己当前的最高分设置为从文件读取的最高分

    # 将最高分数写入文件
    def WriteTopScore(self):
        FTopScore = open("score.txt", "w")
        FTopScore.write(str(self.TopScore))  # 把自己当前的最高分设置为从文件读取的最高分

    # 根据当前数据设置最高分，如果超过最高分，则刷新最高分
    def _RefreshTopScore(self):
        score = self.ASnake.GetLength()
        if score > self.TopScore:
            self.TopScore = score
            self.WriteTopScore()
            ev3.speaker.say("New high score! Congratulations!")

    # 显示最高分
    def ShowBest(self):
        self.LoadTopScore()
        ev3.screen.draw_line(
            4, 5, 4 + self.TopScore // 2, 5, width=3, color=Color.BLACK
        )

    # 显示积分
    def ShowScore(self):
        ev3.screen.draw_line(
            4, 9, 4 + self.ASnake.GetLength() // 2, 9, width=3, color=Color.BLACK
        )

    # 显示游戏信息
    def ShowGameInfo(self):
        ev3.screen.print(
            "=============================\n"
            + "   MM     MM\n"
            + "   MMM   MMM\n"
            + "   MMMM MMMM\n"
            + "   MM MMM MM  AaronMing 2020\n"
            + "   MM  M  MM   MSnake  V0.0 \n"
            + "   MM     MM     《贪食蛇》\n"
            + "  MMMM   MMMM\n"
            + "============================="
        )

    # 显示启动页面并等待开始
    def ShowWelcomAndWait(self):
        ev3.screen.print(
            "\n"
            + "   上方第一条线：最高分数\n\n"
            + "   上方第二条线：当前分数\n\n\n"
            + "   当前最高分数："
            + str(self.TopScore)
            + "\n"
            + "\n"
            + "        按右键继续..."
        )
        while not Button.RIGHT in ev3.buttons.pressed():
            time.sleep(0.01)

    # 计算蛇的等级
    def _CalLevel(self):
        SLen = self.ASnake.GetLength()
        # 如果长度大于200，则长度为200
        if SLen > 90:
            SLen = 90
        self.ALevel = (SLen // 10) + 1

    # 计算等待的计数次数
    def _CalWaitTag(self):
        if self.ALevel == 1:
            Result = 160
        elif self.ALevel == 2:
            Result = 150
        elif self.ALevel == 3:
            Result = 140
        elif self.ALevel == 4:
            Result = 130
        elif self.ALevel == 5:
            Result = 120
        elif self.ALevel == 6:
            Result = 110
        elif self.ALevel == 7:
            Result = 100
        elif self.ALevel == 8:
            Result = 90
        elif self.ALevel == 9:
            Result = 80
        elif self.ALevel == 10:
            Result = 70
        return Result

    # 开始游戏
    def StartGame(self):
        ev3.screen.clear()
        self.ASnake.GetGround().RedrawGround()
        self.ASnake.Reset()
        self.ASnake.Drawbody()
        self.ShowBest()
        self.ShowScore()

        # 播放开始游戏的声音
        ev3.speaker.say("Go Go Go!")
        # 避免程序在sleep时实去响应，定义此参数，等待计数
        waitTag = 0
        AWaitCnt = self._CalWaitTag()

        # 取得蛇的方向，
        ADir = self.ASnake.GetDirect()
        while True:
            # 根据按键确认方向
            if Button.RIGHT in ev3.buttons.pressed():
                ADir = MSDirec_Right
            elif Button.DOWN in ev3.buttons.pressed():
                ADir = MSDirec_Down
            elif Button.LEFT in ev3.buttons.pressed():
                ADir = MSDirec_Left
            elif Button.UP in ev3.buttons.pressed():
                ADir = MSDirec_Up

            if waitTag == AWaitCnt:
                # if waitTag == 70:
                # 根据最后的输入确定改变蛇的方向
                self.ASnake.SetDirect(ADir)
                # 如果蛇头吃掉了一个食物
                if self.AFood.EatAFood(self.ASnake.GetHeadLoc()):
                    AGrow = True
                    self.ShowScore()
                else:
                    AGrow = False

                self._CalLevel()
                AWaitCnt = self._CalWaitTag()

                # 如果移动失败了，说明游戏结束了
                if not self.ASnake.Move(AGrow):
                    ev3.speaker.say("Game over! ")
                    break
                    # 重置等待计数
                self.AFood.AddFood()
                self.AFood.DrawAllFood()
                waitTag = 0
            else:
                waitTag += 1

            time.sleep(0.001)

    # 显示游戏结果并等待
    def ShowResult(self):
        ev3.screen.print(
            "\n\n"
            + "   最高分："
            + str(self.TopScore)
            + "\n\n"
            + "   您的得分："
            + str(self.ASnake.GetLength())
            + "\n\n\n"
            + "\n"
            + "        按右键继续..."
        )

    # 开始运行
    def Run(self):
        RunGame = True  # 定义游戏是否继续运行
        ev3.screen.clear()  # 清理屏幕
        self.ShowGameInfo()  # 显示游戏信息
        time.sleep(1)
        ev3.screen.clear()  # 清理屏幕
        self.ShowWelcomAndWait()
        while RunGame:
            self.StartGame()
            ev3.screen.clear()  # 清理屏幕
            self.ShowResult()
            self._RefreshTopScore()
            while not Button.RIGHT in ev3.buttons.pressed():
                time.sleep(0.01)
