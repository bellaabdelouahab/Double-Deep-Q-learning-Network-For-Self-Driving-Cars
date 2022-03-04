from numpy.lib.function_base import select
from pyglet import shapes,resource,sprite,graphics,text
from pyglet.shapes import Line
from pickle import load
from math import cos,sin,pi
M=graphics.Batch()
# ttt4=[
    
#     Line(100 , 350,470 , 452 ,width=1, color=(20, 200, 20),batch=M),
#     Line(175 , 291,489 , 372 ,width=1, color=(20, 200, 20),batch=M),
#     Line(100 , 350, 98 , 196 ,width=1, color=(20, 200, 20),batch=M),
#     Line(175 , 291,175 , 192 ,width=1, color=(20, 200, 20),batch=M),
#     Line( 98 , 196,  4 , 119 ,width=1, color=(20, 200, 20),batch=M),
#     Line(175 , 192, 97 , 119 ,width=1, color=(20, 200, 20),batch=M),
#     Line(  4 , 119, 83 ,   2 ,width=1, color=(20, 200, 20),batch=M),
#     Line( 97 , 119,137 ,  70 ,width=1, color=(20, 200, 20),batch=M),
#     Line( 83 ,   2,830 ,   2 ,width=1, color=(20, 20, 200),batch=M),
#     Line(137 ,  70,780 ,  70 ,width=1, color=(20, 200, 20),batch=M),
#     Line(830 ,   2,855 ,  30 ,width=1, color=(20, 200, 20),batch=M),
#     Line(855 ,  30,855 , 110 ,width=1, color=(20, 200, 20),batch=M),
#     Line(855 , 110,830 , 140 ,width=1, color=(20, 200, 20),batch=M),
#     Line(830 , 140,200 , 140 ,width=1, color=(20, 200, 20),batch=M),
#     Line(470 , 452,558 , 452 ,width=1, color=(20, 200, 20),batch=M),
#     Line(558 , 452,825 , 220 ,width=1, color=(20, 200, 20),batch=M),
#     Line(489 , 372,717 , 218 ,width=1, color=(20, 200, 20),batch=M),
#     Line(826 , 222,829 , 141 ,width=1, color=(20, 200, 20),batch=M),
#     Line(175 , 191,716 , 218 ,width=1, color=(20, 200, 20),batch=M)]
# ttt5=[
#     [Line( 310  ,  139 , 310  ,  72  ,width=1, color=(200,20, 20),batch=M),True],
#     [Line( 250  ,  139 , 250  ,  72  ,width=1, color=(200,20, 20),batch=M),False],
#     [Line( 208  ,  139 , 205  ,  72  ,width=1, color=(200,20, 20),batch=M),False],
#     [Line( 198  ,  143 , 176  , 192  ,width=1, color=(200,20, 20),batch=M),False],
#     [Line( 377  ,  143 , 372  , 201  ,width=1, color=(200,20, 20),batch=M),False],
#     [Line( 547  ,  142 , 537  , 210  ,width=1, color=(200,20, 20),batch=M),False],
#     [Line( 672  ,  142 , 656  , 216  ,width=1, color=(200,20, 20),batch=M),False],
#     [Line( 716  ,  219 , 828  , 187  ,width=1, color=(200,20, 20),batch=M),False],
#     [Line( 633  ,  276 , 692  , 335  ,width=1, color=(200,20, 20),batch=M),False],
#     [Line( 512  ,  356 , 560  , 449  ,width=1, color=(200,20, 20),batch=M),False],
#     [Line( 438  ,  360 , 428  , 439  ,width=1, color=(200,20, 20),batch=M),False],
#     [Line( 256  ,  314 , 231  , 387  ,width=1, color=(200,20, 20),batch=M),False],
#     [Line( 174  ,  291 , 100  , 353  ,width=1, color=(200,20, 20),batch=M),False],
#     [Line( 173  ,  193 ,  98  , 196  ,width=1, color=(200,20, 20),batch=M),False],
#     [Line(  96  ,  120 ,   6  , 119  ,width=1, color=(200,20, 20),batch=M),False],
#     [Line( 136  ,   70 ,  85  ,   4  ,width=1, color=(200,20, 20),batch=M),False],
#     [Line( 284  ,   69 , 284  ,   7  ,width=1, color=(200,20, 20),batch=M),False],
#     [Line( 443  ,   70 , 441  ,   5  ,width=1, color=(200,20, 20),batch=M),False],
#     [Line( 571  ,   71 , 571  ,   5  ,width=1, color=(200,20, 20),batch=M),False],
#     [Line( 715  ,   69 , 715  ,   2  ,width=1, color=(200,20, 20),batch=M),False],
#     [Line( 782  ,   71 , 854  ,  72  ,width=1, color=(200,20, 20),batch=M),False],
#     [Line( 709  ,  141 , 709  ,  74  ,width=1, color=(200,20, 20),batch=M),False],
#     [Line( 607  ,  139 , 607  ,  73  ,width=1, color=(200,20, 20),batch=M),False],
#     [Line( 473  ,  141 , 473  ,  70  ,width=1, color=(200,20, 20),batch=M),False],
#     [Line( 376  ,  139 , 375  ,  72  ,width=1, color=(200,20, 20),batch=M),False],
# ]
class track():
    batch = M
    SetTrack=[]
    SetGoals=[]
    new_added_track=False
    new_added_goal=False
    drawing_track=False
    drawing_goal=False
    def setter(self):
        try:
            with open('output.dat','rb') as ch:
                while True:
                    try:
                        lis=load(ch)
                        self.SetTrack=[shapes.Line(lis[0][i][0] , lis[0][i][1],lis[0][i][2] , lis[0][i][3] ,\
                                        width=1, color=(20, 200, 20), batch=self.batch) for i in range(len(lis[0]))]
                        self.SetGoals=[[shapes.Line(lis[1][i][0] , lis[1][i][1],lis[1][i][2] , lis[1][i][3] ,\
                                        width=1, color=(200, 20, 20), batch=self.batch),False] for i in range(len(lis[1]))]
                        if len(self.SetGoals)>0:
                            self.SetGoals[0][1]=True
                        self.batch.invalidate()
                    except EOFError:
                        break
        except FileNotFoundError:
            SetTrack=[]
            SetGoals=[]
    def add_track(self,x,y):
        if self.drawing_track:
            if not self.new_added_track:
                self.new_added_track=shapes.Line( x , y, x , y ,width=1, color=(20, 200, 20), batch=self.batch)
            else:
                self.new_added_track.x2=x
                self.new_added_track.y2=y
                self.SetTrack.append(self.new_added_track)
                self.new_added_track=False
    def change_track_coords(self,x,y):
        if self.drawing_track and self.new_added_track:
            self.new_added_track.x2=x
            self.new_added_track.y2=y
    def add_goal(self,x,y):
        if self.drawing_goal:
            if not self.new_added_goal:
                self.new_added_goal=[shapes.Line( x , y , x , y ,width=1, color=(200,20, 20), batch=self.batch),False]
            else:
                self.new_added_goal[0].x2=x
                self.new_added_goal[0].y2=y
                self.SetGoals.append(self.new_added_goal)
                self.new_added_goal=False
    def change_goal_coords(self,x,y):
        if self.drawing_goal and self.new_added_goal:
            self.new_added_goal[0].x2=x
            self.new_added_goal[0].y2=y
