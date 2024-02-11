from pyglet import shapes,graphics
from pickle import load
import tkinter.filedialog as Fd
class track():
    batch = graphics.Batch()
    SetTrack=[]
    SetGoals=[]
    new_added_track=False
    new_added_goal=False
    drawing_track=False
    drawing_goal=False
    def setter(self,path=False):
        try:
            if path:
                filepath = Fd.askopenfile(filetypes=[("binary files only", ".dat")])
                filename = filepath.name
            else:
                filename='Tracks/output.dat'
            with open(filename,'rb') as ch:
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
                        print('done')
                    except EOFError:
                        break
        except FileNotFoundError:
            print('file not found')
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
