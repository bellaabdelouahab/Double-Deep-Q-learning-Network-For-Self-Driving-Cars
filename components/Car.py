from pyglet import shapes,resource,sprite,graphics,text
from math import cos,sin,pi
class Set_car:
    car = graphics.Batch()
    def gocar(self):
        self.image=resource.image('Car.png')
        self.DefaultCarX=750
        self.DefaultCarY=110
        self.Carx=750
        self.Cary=110
        self.image.width=20
        self.image.height=40
        self.image.anchor_x = 10
        self.image.anchor_y = 20
        self.sprite = sprite.Sprite(resource.image('Car.png'), x = self.Carx, y = self.Cary,batch=self.car)
        self.sprite.rotation=-90
        self.sprite.opacity=1000
        self.lines=[
        # [shapes.Line(self.Carx , self.Cary,self.Carx+500*cos( 18*pi/180) , self.Cary+500*sin( 18*pi/180),width=1, color=(255,255,255), batch=self.car),shapes.Circle(self.Carx+60 , self.Cary-60, 3, color=(50, 225, 30), batch=self.car),True,text.Label('',font_name='Times New Roman',font_size=15,x=930, y=245,batch=self.car)],
        # [shapes.Line(self.Carx , self.Cary,self.Carx+500*cos( 36*pi/180) , self.Cary+500*sin( 36*pi/180),width=1, color=(255,255,255), batch=self.car),shapes.Circle(self.Carx+ 5 , self.Cary+60, 3, color=(50, 225, 30), batch=self.car),True,text.Label('',font_name='Times New Roman',font_size=15,x=930, y=230,batch=self.car)],
        # [shapes.Line(self.Carx , self.Cary,self.Carx+500*cos( 54*pi/180) , self.Cary+500*sin( 54*pi/180),width=1, color=(255,255,255), batch=self.car),shapes.Circle(self.Carx+ 5 , self.Cary-60, 3, color=(50, 225, 30), batch=self.car),True,text.Label('',font_name='Times New Roman',font_size=15,x=930, y=215,batch=self.car)],
        # [shapes.Line(self.Carx , self.Cary,self.Carx+500*cos( 72*pi/180) , self.Cary+500*sin( 72*pi/180),width=1, color=(255,255,255), batch=self.car),shapes.Circle(self.Carx+ 5 , self.Cary-60, 3, color=(50, 225, 30), batch=self.car),True,text.Label('',font_name='Times New Roman',font_size=15,x=930, y=200,batch=self.car)],
        # [shapes.Line(self.Carx                 , self.Cary+self.image.height/4,self.Carx+500*cos( 90*pi/180) , self.Cary+500*sin( 90*pi/180),width=1, color=(255,255,255), batch=self.car),shapes.Circle(self.Carx-90 , self.Cary+10, 3, color=(255,255,255), batch=self.car),True,text.Label('',font_name='Times New Roman',font_size=15,x=930, y=485,batch=self.car)],
        # [shapes.Line(self.Carx-1/4*self.image.width , self.Cary+self.image.height/4,self.Carx+500*cos(108*pi/180) , self.Cary+500*sin(108*pi/180),width=1, color=(255,255,255), batch=self.car),shapes.Circle(self.Carx-90 , self.Cary-10, 3, color=(255,255,255), batch=self.car),True,text.Label('',font_name='Times New Roman',font_size=15,x=930, y=470,batch=self.car)],
        # [shapes.Line(self.Carx-2/4*self.image.width , self.Cary+self.image.height/4,self.Carx+500*cos(126*pi/180) , self.Cary+500*sin(126*pi/180),width=1, color=(255,255,255), batch=self.car),shapes.Circle(self.Carx-60 , self.Cary+60, 3, color=(255,255,255), batch=self.car),True,text.Label('',font_name='Times New Roman',font_size=15,x=930, y=455,batch=self.car)],
        # [shapes.Line(self.Carx-3/4*self.image.width , self.Cary+self.image.height/4,self.Carx+500*cos(144*pi/180) , self.Cary+500*sin(144*pi/180),width=1, color=(255,255,255), batch=self.car),shapes.Circle(self.Carx-60 , self.Cary-60, 3, color=(255,255,255), batch=self.car),True,text.Label('',font_name='Times New Roman',font_size=15,x=930, y=440,batch=self.car)],
        [shapes.Line(self.Carx-self.image.width     , self.Cary+self.image.height/4,self.Carx+500*cos(162*pi/180) , self.Cary+500*sin(162*pi/180),width=1, color=(255,255,255), batch=self.car),shapes.Circle(self.Carx+90 , self.Cary+10, 3, color=(255,255,255), batch=self.car),True,text.Label('',font_name='Times New Roman',font_size=15,x=930, y=485,batch=self.car)],
        [shapes.Line(self.Carx-self.image.width     , self.Cary               ,self.Carx+500*cos(180*pi/180) , self.Cary+500*sin(180*pi/180),width=1, color=(255,255,255), batch=self.car),shapes.Circle(self.Carx+90 , self.Cary-10, 3, color=(255,255,255), batch=self.car),True,text.Label('',font_name='Times New Roman',font_size=15,x=930, y=470,batch=self.car)],
        [shapes.Line(self.Carx-self.image.width     , self.Cary-self.image.height/4,self.Carx+500*cos(198*pi/180) , self.Cary+500*sin(198*pi/180),width=1, color=(255,255,255), batch=self.car),shapes.Circle(self.Carx+60 , self.Cary+60, 3, color=(255,255,255), batch=self.car),True,text.Label('',font_name='Times New Roman',font_size=15,x=930, y=455,batch=self.car)],
        # [shapes.Line(self.Carx-3/4*self.image.width , self.Cary-self.image.height/4,self.Carx+500*cos(216*pi/180) , self.Cary+500*sin(216*pi/180),width=1, color=(255,255,255), batch=self.car),shapes.Circle(self.Carx+60 , self.Cary-60, 3, color=(255,255,255), batch=self.car),True,text.Label('',font_name='Times New Roman',font_size=15,x=930, y=380,batch=self.car)],
        # [shapes.Line(self.Carx-2/4*self.image.width , self.Cary-self.image.height/4,self.Carx+500*cos(234*pi/180) , self.Cary+500*sin(234*pi/180),width=1, color=(255,255,255), batch=self.car),shapes.Circle(self.Carx+ 5 , self.Cary+60, 3, color=(255,255,255), batch=self.car),True,text.Label('',font_name='Times New Roman',font_size=15,x=930, y=365,batch=self.car)],
        # [shapes.Line(self.Carx-1/4*self.image.width , self.Cary-self.image.height/4,self.Carx+500*cos(252*pi/180) , self.Cary+500*sin(252*pi/180),width=1, color=(255,255,255), batch=self.car),shapes.Circle(self.Carx+ 5 , self.Cary-60, 3, color=(255,255,255), batch=self.car),True,text.Label('',font_name='Times New Roman',font_size=15,x=930, y=350,batch=self.car)],
        # [shapes.Line(self.Carx                 , self.Cary-self.image.height/4,self.Carx+500*cos(270*pi/180) , self.Cary+500*sin(270*pi/180),width=1, color=(255,255,255), batch=self.car),shapes.Circle(self.Carx+ 5 , self.Cary-60, 3, color=(255,255,255), batch=self.car),True,text.Label('',font_name='Times New Roman',font_size=15,x=930, y=335,batch=self.car)]
        # [shapes.Line(self.Carx , self.Cary,self.Carx+500*cos(288*pi/180) , self.Cary+500*sin(288*pi/180),width=1, color=(255,255,255), batch=self.car),shapes.Circle(self.Carx-60 , self.Cary+60, 3, color=(50, 225, 30), batch=self.car),True,text.Label('',font_name='Times New Roman',font_size=15,x=930, y=320,batch=self.car)],
        # [shapes.Line(self.Carx , self.Cary,self.Carx+500*cos(306*pi/180) , self.Cary+500*sin(306*pi/180),width=1, color=(255,255,255), batch=self.car),shapes.Circle(self.Carx-60 , self.Cary-60, 3, color=(50, 225, 30), batch=self.car),True,text.Label('',font_name='Times New Roman',font_size=15,x=930, y=305,batch=self.car)],
        # [shapes.Line(self.Carx , self.Cary,self.Carx+500*cos(324*pi/180) , self.Cary+500*sin(324*pi/180),width=1, color=(255,255,255), batch=self.car),shapes.Circle(self.Carx+90 , self.Cary+10, 3, color=(50, 225, 30), batch=self.car),True,text.Label('',font_name='Times New Roman',font_size=15,x=930, y=290,batch=self.car)],
        # [shapes.Line(self.Carx , self.Cary,self.Carx+500*cos(342*pi/180) , self.Cary+500*sin(342*pi/180),width=1, color=(255,255,255), batch=self.car),shapes.Circle(self.Carx+90 , self.Cary-10, 3, color=(50, 225, 30), batch=self.car),True,text.Label('',font_name='Times New Roman',font_size=15,x=930, y=275,batch=self.car)],
        # [shapes.Line(self.Carx , self.Cary,self.Carx+500*cos(360*pi/180) , self.Cary+500*sin(360*pi/180),width=1, color=(255,255,255), batch=self.car),shapes.Circle(self.Carx+60 , self.Cary+60, 3, color=(50, 225, 30), batch=self.car),True,text.Label('',font_name='Times New Roman',font_size=15,x=930, y=260,batch=self.car)]
        ]
        self.car_shape=[
            shapes.Line( self.Carx-self.image.width,self.Cary+self.image.height/4,self.Carx+self.image.width,self.Cary+self.image.height/4,width=1, color=(0, 0, 200), batch=self.car),
            shapes.Line( self.Carx-self.image.width,self.Cary-self.image.height/4,self.Carx+self.image.width,self.Cary-self.image.height/4,width=1, color=(20, 20, 250), batch=self.car),
            shapes.Line( self.Carx-self.image.width,self.Cary+self.image.height/4,self.Carx-self.image.width,self.Cary-self.image.height/4,width=1, color=(20, 200, 20), batch=self.car),
            shapes.Line( self.Carx+self.image.width,self.Cary+self.image.height/4,self.Carx+self.image.width,self.Cary-self.image.height/4,width=1, color=(20, 200, 20), batch=self.car)
        ]
        for line in self.lines:
            line[1].opacity=0
            line[0].opacity=0
            line[3].color = (100, 255, 100, 255)
            line[3].text=str(format(((line[0].x2-(line[0].x))**2 + (line[0].y2-(line[0].y))**2)**0.5, ".2f"))
        for line in self.car_shape:
            line.opacity=0
        self.lines_coord=[[line[0].x-750,line[0].y-110,line[0].x2-750,line[0].y2-110] for line in self.lines]

###########
        self.car_body=[[line.x-750,line.y-110,line.x2-750,line.y2-110] for line in self.car_shape]
        self.velocity=0
    def update(self,rotation,sprite):
        sprite.update(x=self.Carx,y=self.Cary,rotation=rotation)
        for i in range(0,len(self.lines_coord)):
            self.move_lines(self.lines[i],self.lines_coord[i][0],self.lines_coord[i][1],self.lines_coord[i][2],self.lines_coord[i][3],rotation)
        for i in range(len(self.car_body)):
            self.move_lines([self.car_shape[i],0,False],self.car_body[i][0],self.car_body[i][1],self.car_body[i][2],self.car_body[i][3],rotation)
    def move_lines(self,line,a,b,c,d,rotation):
        line[0].x=self.Carx+(a)*cos(-(rotation-270)*pi/180)-(b)*sin(-(rotation-270)*pi/180)
        line[0].y=self.Cary+(a)*sin(-(rotation-270)*pi/180)+(b)*cos(-(rotation-270)*pi/180)
        line[0].x2=self.Carx+(c)*cos(-(rotation-270)*pi/180)-(d)*sin(-(rotation-270)*pi/180)
        line[0].y2=self.Cary+(c)*sin(-(rotation-270)*pi/180)+(d)*cos(-(rotation-270)*pi/180)
        if line[2]:
            line[1].x=line[0].x2 
            line[1].y=line[0].y2
    def set_default_distance(self,x):
        x[0][3].text=str(format(((x[0][0].x2-(x[0][0].x))**2 + (x[0][0].y2-(x[0][0].y))**2)**0.5, ".2f"))
        x[1][3].text=str(format(((x[1][0].x2-(x[1][0].x))**2 + (x[1][0].y2-(x[1][0].y))**2)**0.5, ".2f"))
        x[2][3].text=str(format(((x[2][0].x2-(x[2][0].x))**2 + (x[2][0].y2-(x[2][0].y))**2)**0.5, ".2f"))
        # x[3][3].text=str(format(((x[3][0].x2-(x[3][0].x))**2 + (x[3][0].y2-(x[3][0].y))**2)**0.5, ".2f"))
        # x[4][3].text=str(format(((x[4][0].x2-(x[4][0].x))**2 + (x[4][0].y2-(x[4][0].y))**2)**0.5, ".2f"))
        # x[5][3].text=str(format(((x[5][0].x2-(x[5][0].x))**2 + (x[5][0].y2-(x[5][0].y))**2)**0.5, ".2f"))
        # x[6][3].text=str(format(((x[6][0].x2-(x[6][0].x))**2 + (x[6][0].y2-(x[6][0].y))**2)**0.5, ".2f"))
        # x[7][3].text=str(format(((x[7][0].x2-(x[7][0].x))**2 + (x[7][0].y2-(x[7][0].y))**2)**0.5, ".2f"))
        # x[8][3].text=str(format(((x[8][0].x2-(x[8][0].x))**2 + (x[8][0].y2-(x[8][0].y))**2)**0.5, ".2f"))
        # x[9][3].text=str(format(((x[9][0].x2-(x[9][0].x))**2 + (x[9][0].y2-(x[9][0].y))**2)**0.5, ".2f"))
        return [eval(x[i][3].text) for i in range(len(x))]
    car.invalidate()
    
class Set_car2:
    car1 = graphics.Batch()
    image=resource.image('Car.png')
    Carx=750
    Cary=110
    image.width=20
    image.height=40
    image.anchor_x = 10
    image.anchor_y = 20
    sprite = sprite.Sprite(image, x = Carx, y = Cary,batch=car1)
    sprite.rotation=-90
    sprite.opacity=100