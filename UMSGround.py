####################################################################################################
#
#           MM     MM
#           MMM   MMM
#           MMMM MMMM
#           MM MMM MM
#           MM  M  MM
#           MM     MM
#          MMMM   MMMM     AaronMing 2020
#
#       地图模块 V0.2
#
#    更新日志：
#    2020-10-14 V0.1 
#               增加是否需要使用边框和网格属性
#               增加可以根据地图坐标位置选择对应地图块的坐标值的方法，以便调用者自主绘图用
#    2020-10-19 V0.2
#               增加空白块列表的操作方法，标记占用和空白
#
###################################################################################################

from pybricks.hubs import EV3Brick
from pybricks.parameters import Color


#创建场地类
class MSGround:
    """
        蛇可以运动的场地,边框和网格的宽度都是1个像素 
        想了想，这个已经不仅仅是蛇的地方了,这是重新定义了一下这块小屏幕

    """
    #定义构造函数
    def __init__(self, ABrick , LeftTopX = 1, LeftTopY = 10 ,BlockSize = 6, XBlockCount = 25 , YBlockCount = 15, UseBorder = True, UseGrid = True, BorderVisible = True , GridVisible = False):
        self.ABrick = ABrick                #传递进来的ev3Brick
        self.LeftTopX = LeftTopX            #场地左上角的X坐标
        self.LeftTopY = LeftTopY            #场地左上角的Y坐标
        self.BlockSize = BlockSize          #每一个块的边长
        self.XBlockCount = XBlockCount      #横向块的数量
        self.YBlockCount = YBlockCount      #纵向块的数量
        self.UseBorder = UseBorder          #是否使用边框
        self.UseGrid = UseGrid              #是否使用网格
        self.BorderVisible = BorderVisible  #是否显示边框
        self.GridVisible = GridVisible      #是否显示网格
        self._Calculate()                   #根据输入的值进行计算场地的数据
        self._CreateBlankBlocks()
    

    """
        场地块列表里的数据格式
        [左上X,左上Y,右下X,右下Y],[左上X,左上Y,右下X,右下Y],[左上X,左上Y,右下X,右下Y]....
        [左上X,左上Y,右下X,右下Y],[左上X,左上Y,右下X,右下Y],[左上X,左上Y,右下X,右下Y]
        [左上X,左上Y,右下X,右下Y],[左上X,左上Y,右下X,右下Y],[左上X,左上Y,右下X,右下Y]
        .
        .
        .
        #网格列表里的数据格式
        [起点X,起点Y,终点X,重点Y],[起点X,起点Y,终点X,重点Y],[起点X,起点Y,终点X,重点Y]...

    """
    def _Calculate(self):   #根据当前的属性值进行计算
        
        if self.UseBorder:
            self.BorderSize = 1
        else:
            self.BorderSize = 0
        
        
        #如果使用网格，则设置网格宽度
        if self.UseGrid:
            self.GridSize = 1
        else:
            self.GridSize = 0

        self.Width = self.BorderSize * 2 + self.BlockSize * self.XBlockCount + (self.XBlockCount - 1) * self.GridSize #计算整个场地宽度，包括边框和网格
        self.Height = self.BorderSize * 2 + self.BlockSize * self.YBlockCount + (self.YBlockCount - 1) * self.GridSize #计算整个场地的高度，包括边框和网格

        self.RightBottomX = self.LeftTopX + self.Width - 1           #计算右下角的X坐标
        self.RightBottomY = self.LeftTopY + self.Height - 1          #计算右下角的Y坐标
        #计算网格
        #定义网格列表
        self.Grids = list()    #创建地图块的列表
        if self.UseGrid:
            #计算纵向格栅
            TempY = self.LeftTopY + self.Height - 1  #所有纵向网格两端的Y值都是一样的，所以预先计算
            for i in range(self.XBlockCount - 1):
                TempX = self.LeftTopX + (i + 1) * self.BlockSize + self.GridSize * i + self.BorderSize #逐个计算X坐标
                self.Grids.append([TempX ,self.LeftTopY, TempX , TempY])
            #计算横向格栅
            TempX = self.LeftTopX + self.Width - 1 #所有横向格栅两端的X值都是一样的
            for i in range(self.YBlockCount - 1):
                TempY = self.LeftTopY + (i + 1) * self.BlockSize + self.GridSize * i + self.BorderSize #逐个计算Y坐标
                self.Grids.append([self.LeftTopX , TempY , TempX , TempY])
        
        #计算地图快坐标信息
        #定义地图块列表
        self.Blocks = list()

        #计算每一个场地块的坐标信息
        for i in range(self.XBlockCount):
            TempRow = list()
            for j in range(self.YBlockCount):
                TempRow.append(
                    [
                        self.LeftTopX + self.BorderSize + self.GridSize * i + (i * self.BlockSize),
                        self.LeftTopY + self.BorderSize + self.GridSize * j + (j * self.BlockSize),
                        self.LeftTopX + self.BorderSize + self.GridSize * i + (i + 1) * self.BlockSize - 1,
                        self.LeftTopY + self.BorderSize + self.GridSize * j + (j + 1) * self.BlockSize - 1 
                    ]
                )
            self.Blocks.append(TempRow)



    #创建空白地图块列表
    def _CreateBlankBlocks(self):
        self.BlankBlockList = list()
        for i in range(self.XBlockCount):
            for j in range(self.YBlockCount):
                ABlock = [i,j]
                self.BlankBlockList.append(ABlock)

    #占用一个块
    def OccupyABlock(self, ABlock):
        if ABlock in self.BlankBlockList:
            self.BlankBlockList.remove(ABlock)


    #释放一个块
    def ReleaseABlock(self,ABlock):
        if not (ABlock in self.BlankBlockList):
            self.BlankBlockList.append(ABlock.copy())
        #print(len(self.BlankBlockList))

    #取得空白块的列表
    def GetBlankBlockList(self):
        return self.BlankBlockList

    #画边框
    def _DrawBorder(self, AColor = Color.BLACK):
        if self.UseBorder: 
            self.ABrick.screen.draw_box(self.LeftTopX, self.LeftTopY, self.RightBottomX, self.RightBottomY, r=0, fill=False, color=AColor)

    #显示边框
    def ShowBorder(self):     
        self._DrawBorder(Color.BLACK)

    #隐藏边框
    def HideBorder(self):       
        self._DrawBorder(Color.WHITE)

    #画网格
    def _DrawGrid(self, AColor = Color.BLACK):  
        for G in self.Grids:
           self.ABrick.screen.draw_line(G[0], G[1], G[2], G[3], width=1, color=AColor)

    #显示网格
    def ShowGrid(self):
        self._DrawGrid(Color.BLACK)

    #隐藏网格
    def HideGrid(self):
        self._DrawGrid(Color.WHITE)

    #画地图块
    def DrawABlock(self, BlockX, BlockY, Afill=True, AColor = Color.BLACK):
        self.ABrick.screen.draw_box(
            self.Blocks[BlockX][BlockY][0], 
            self.Blocks[BlockX][BlockY][1],
            self.Blocks[BlockX][BlockY][2],
            self.Blocks[BlockX][BlockY][3],
            r=0, fill = Afill, color=AColor)

    #在地图块指定位置画圆
    def DrawACircle(self,BlockX,BlockY, Afill=True ,AColor = Color.BLACK):
        self.ABrick.screen.draw_circle(
            (self.Blocks[BlockX][BlockY][0] + self.Blocks[BlockX][BlockY][2]) / 2, 
            (self.Blocks[BlockX][BlockY][1] +  self.Blocks[BlockX][BlockY][3]) / 2,
            self.BlockSize / 2,
            fill=Afill, color=AColor)


    #清除地图块
    def ClearABlock(self,BlockX,BlockY):
        self.DrawABlock(BlockX,BlockY,Afill = True, AColor = Color.WHITE)

    #画出列表里的所有地图块
    def DrawBlocks(self,Blocks = [],AColor = Color.BLACK):
        for B in Blocks:
            self.DrawABlock(B[0],B[1],AColor)

    #清楚列表里所有的地图快
    def ClearBlocks(self,Blocks = []):
        self.DrawBlocks(Blocks,Color.WHITE)

    #清除场地
    def ClearGround(self):              
        self.ABrick.screen.draw_box(self.LeftTopX, self.LeftTopY, self.RightBottomX, self.RightBottomY, r=0, fill=True, color=Color.WHITE)

    #画场地
    def DrawGround(self):                    
        if self.BorderVisible:
            self._DrawBorder()
        if self.GridVisible:
            self._DrawGrid()

    #重画场地
    def RedrawGround(self):
        self.ClearGround()
        self.DrawGround()

    #取得场地的宽度
    def GetGroundWidth(self):
        return self.XBlockCount
    
    #取得场地的高度
    def GetGroundHeight(self):
        return self.YBlockCount

    #取得地图块的坐标坐标信息
    def GetABlockLoc(self, BlockX, BlockY):
        return self.Blocks[BlockX][BlockY]

    