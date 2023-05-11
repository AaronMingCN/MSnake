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
#       贪食蛇，蛇的食物单元
#       GitHub Commit pull test
#
###################################################################


from UMSGround import MSGround
from UMSnake import *
import random


class MSFood:
    # 构造函数
    def __init__(self, ASnake, MaxFoodCount=5):
        self.ASnake = ASnake  # 蛇
        self.MaxFoodCount = MaxFoodCount  # 食物最多的个数
        self._Prepare()

    def _Prepare(self):
        # 创建食物的列表
        self.Food = list()

    # 吃掉一个食物
    def EatAFood(self, SHead):
        Result = False
        for i in range(len(self.Food)):
            if (SHead[0] == self.Food[i][0]) and (SHead[1] == self.Food[i][1]):
                self.ASnake.GetGround().ReleaseABlock(self.Food[i])
                self.Food.remove(self.Food[i])
                Result = True
                break
        return Result

    # 判断一个节点是不是在食物列表里
    def NodeInFood(self, AFood):
        return AFood in self.Food

    # 判断一个食物是否可添加：条件1、是否已经在食物列表里了。2、是否在蛇的身上
    def AFoodCanAdd(self, AFood):
        Result = True
        if self.NodeInFood(AFood):
            Result = False
        elif self.ASnake.NodeInSnake(AFood):
            Result = False
        return Result

    # 创造一个食物
    def CreateAFood(self):
        Result = None  # 定义结果，默认为None
        ABlankBlockList = self.ASnake.AGround.GetBlankBlockList()
        RIndex = random.randint(0, len(ABlankBlockList) - 1)
        Result = ABlankBlockList[RIndex].copy()
        return Result

    # 画一个食物
    def _DrawAFood(self, AFood):
        AGround = self.ASnake.GetGround()
        AGround.DrawACircle(AFood[0], AFood[1], Afill=False)

    # 添加一个食物
    def AddFood(self):
        if len(self.Food) < self.MaxFoodCount:
            # 取随机位置
            AFood = self.CreateAFood()
            # 将食物添加到列表
            self.Food.append(AFood)
            self.ASnake.GetGround().OccupyABlock(AFood)
            self._DrawAFood(AFood)

    # 画所有的food
    def DrawAllFood(self):
        for F in self.Food:
            self._DrawAFood(F)
