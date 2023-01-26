###################################################################
#
#           MM     MM
#           MMM   MMM
#           MMMM MMMM
#           MM MMM MM
#           MM  M  MM
#           MM     MM
#          MMMM   MMMM     AaronMing 2020-2023
#
#       贪食蛇，蛇的定义
#
###################################################################

from UMSGround import MSGround

#定义蛇的方向常量
MSDirec_Up    = 0
MSDirec_Down  = 1
MSDirec_Left  = 2
MSDirec_Right = 3


#创建贪食蛇类
class MSnake:

    
    #构造函数
    def __init__(self, AGround, BodyLength = 5, Direc = MSDirec_Right):
        self.AGround = AGround               #蛇可以跑的场地
        self.BodyLength = BodyLength         #蛇的长度
        self.DefaultDirec = Direc
        self.Direc = Direc                   #蛇的方向   
        self._Prepare()
    

    #准备蛇
    def _Prepare(self):
        self.Body = list()
        #创建蛇的身体在地图上的坐标信息，起点默认在最上方从左往右横向开始
        #列表第一个元素就是头的位置
        for i in range(self.BodyLength):
            self.Body.append(
                [self.BodyLength - i - 1,0]
                )
        #设置为默认方向
        self.Direc = self.DefaultDirec
    
    #在地图上画蛇
    def Drawbody(self):
        self.AGround.DrawBlocks(self.Body)
    

    #判断一个节点是不是在蛇的身上
    def NodeInSnake(self, ANode):
        #定义返回值
        return ANode in self.Body         

    #判断蛇是否可以移动
    def CanMove(self, NextStepLoc):
        return (NextStepLoc[0] >= 0) and (NextStepLoc[0] < self.AGround.GetGroundWidth()) and (NextStepLoc[1] >= 0) and (NextStepLoc[1] < self.AGround.GetGroundHeight()) and (not self.NodeInSnake(NextStepLoc))
        

    #移动,返回值为是否成功移动了,参数Grow表示是不是长大了，如果长大了就不删除尾巴
    def Move(self, Grow = False):
        Result = False
        #根据头坐标计算前进到的新一节的坐标，并删除最后一节
        NewHead = self.Body[0].copy() #这个copy是个坑，一个坑里不能掉两次
        if self.Direc == MSDirec_Down:
            NewHead[1] += 1
        elif self.Direc == MSDirec_Up:
            NewHead[1] -= 1
        elif self.Direc == MSDirec_Left:
            NewHead[0] -= 1
        elif self.Direc == MSDirec_Right:
            NewHead[0] += 1
        #如果可以移动，则移动蛇
        if self.CanMove(NewHead):
            #取得并删除尾巴，插入新头
            #为减少系统资源消耗，只需要把蛇头的新位置画出来，并且清楚尾巴的位置就可以了
            self.Body.insert(0,NewHead)
            self.AGround.OccupyABlock(NewHead)         
            self.AGround.DrawABlock(NewHead[0],NewHead[1])
            if not Grow:   
                SLastBlock = self.Body.pop()
                self.AGround.ReleaseABlock(SLastBlock)
                self.AGround.ClearABlock(SLastBlock[0],SLastBlock[1])
            Result = True
        return Result     
    
    #取得当前蛇头部的在地图上的坐标
    def GetHeadLoc(self):
        return self.Body[0]

    #取得当前方向
    def GetDirect(self):
        return self.Direc
    
    #取得当前蛇的长度
    def GetLength(self):
        return len(self.Body)
    
    #修改当前方向，不允许变成和当前相反的方向
    def SetDirect(self, NewDirect):
        Result = False #定义执行结果
        if self.Direc != NewDirect:
            if ( 
            (self.Direc == MSDirec_Up) and (NewDirect != MSDirec_Down)
            or
            (self.Direc == MSDirec_Down) and (NewDirect != MSDirec_Up)
            or
            (self.Direc == MSDirec_Left) and (NewDirect != MSDirec_Right)
            or
            (self.Direc == MSDirec_Right) and (NewDirect != MSDirec_Left)
            ):
                self.Direc = NewDirect
                Result = True
        return Result #返回执行结果

    #取得蛇当前使用的场地
    def GetGround(self):
        return self.AGround

    #重置蛇
    def Reset(self):
        
        #释放蛇在地图上占用的空间
        for B in self.Body:
            self.AGround.ReleaseABlock(B)
        
        self.Body.clear()
        self._Prepare()





            



