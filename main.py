#!/usr/bin/env pybricks-micropython

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
#       MSnake  V0.0
#       还原经典黑白屏手机小游戏《贪食蛇》
#       
#       2021-12-19 提交到GitHub
#       Remote Open Test
#       PSPi VSC Test
###################################################################


import time
from UMSGround import MSGround
from UMSnake import *
from UMSFood import *
from UMSControler import *


G = MSGround(ABrick = ev3, GridVisible = True)
K = MSGround(ABrick = ev3,LeftTopX = 0, LeftTopY = 0 ,BlockSize = 12, XBlockCount = 13 , YBlockCount = 8, UseBorder = True, UseGrid = False , GridVisible = True)
#L = MSGround(ABrick = ev3, LeftTopX = 2, LeftTopY = 30 ,BlockSize = 5, XBlockCount = 29 , YBlockCount = 16, GridVisible = False)
L = MSGround(ABrick = ev3, LeftTopX = 4, LeftTopY = 13 ,BlockSize = 7, XBlockCount = 21 , YBlockCount = 14, GridVisible = False)

#选择地图G或者K或者L
#MG = K
#MG = G
MG = L


#创建我的蛇
ASnake = MSnake(MG, BodyLength = 5)

#创建蛇的食物
AMSFood = MSFood(ASnake,MaxFoodCount = 3)

AControler = MSControler(ASnake,AMSFood)
AControler.Run()
