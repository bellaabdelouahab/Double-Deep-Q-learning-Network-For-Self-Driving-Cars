from ast import For
from cgitb import reset
from pyglet import window,clock,app,options
from Track import track
from components.Car import Set_car,Set_car2
from pickle import dump
from components.buttons import button
from math import cos,sin,pi
from components.learning_rate import draw_graphe
import numpy as np
from ddqn_Agent import DDQNAgent
import tkinter.filedialog as Fd
import tkinter as tk
import os
import time
##################### set game env ##################

TOTAL_GAMETIME = 10000 # Max game time for one episode
N_EPISODES = 10001
Episodes_counter = 0
REPLACE_TARGET = 100 
GameTime = 0 
GameHistory = []
ddqn_agent = DDQNAgent(alpha=0.001, gamma=0.998, n_actions=3, epsilon=0.1, batch_size=128, input_dims=3)
# if you want to load the existing model uncomment this line.
# careful an existing model might be overwritten
 
ddqn_scores = []
eps_history = []
observation = []
carPositionHistory = []
#game state
done=True
reward=0
score = 0
counter = 0
gtime = 0 
first_game=True
learnning_started=False
userControl = False
list_of_actions=[]
#####################################################
show_real_car=False

windows = window.Window(1000,500)
windows.set_minimum_size(1000, 500)
root = tk.Tk()
root.withdraw()
options['debug_gl'] = False
keyboard = window.key.KeyStateHandler() 
windows.push_handlers(keyboard)
rotation_angel=1
Track=track()
Track.setter()
Track_lines=Track.SetTrack
Track_gols=Track.SetGoals
for goal in Track_gols:
    goal[0].opacity=0
buttons=button
Car=Set_car()
Car1=Set_car2()
Car1.sprite.opacity=1000
default_distance=Car.set_default_distance(Car.lines)

#################################
def on_mouse_press(x,y, button, modifier):
    global learnning_started,Track_lines,Track_gols,Track,userControl
    if track.drawing_track:
        Track.add_track(x,y)
    elif track.drawing_goal:
        Track.add_goal(x,y)
    if 0<x<150 and 460<y<500 :
        learnning_started=not learnning_started
        if learnning_started:
            buttons.button_text.text='Stop learning'
        else :
            buttons.button_text.text='Start learning'
    elif 0<x<150 and 420<y<460 :
        track.drawing_track=not track.drawing_track
        if track.drawing_track:
            buttons.button_draw_track.text='Drawing'
            buttons.button_draw_goal.text='Draw Goal'
            track.drawing_goal=False
            track.new_added_goal=False
        else :
            buttons.button_draw_track.text='Draw Line'
            track.new_added_track=False
    elif 0<x<150 and 380<y<420 :
        track.drawing_goal=not track.drawing_goal
        if track.drawing_goal:
            buttons.button_draw_goal.text='Drawing'
            buttons.button_draw_track.text='Draw Line'
            track.drawing_track=False
            track.new_added_track=False
        else :
            buttons.button_draw_goal.text='Draw Goal'
            track.new_added_goal=False
    elif 0<x<150 and 340<y<380 :
        track.drawing_goal=False
        track.drawing_track=False
        track.new_added_track=False
        track.new_added_goal=False
        timestr = time.strftime("%d-%m-%Y-%H-%M")
        with open('Trucks/Truck-'+timestr+'.dat','wb') as ch:
            dump([[[track.SetTrack[i].x,track.SetTrack[i].y,track.SetTrack[i].x2,track.SetTrack[i].y2] for i in range(len(track.SetTrack))],\
                    [[track.SetGoals[i][0].x,track.SetGoals[i][0].y,track.SetGoals[i][0].x2,track.SetGoals[i][0].y2] for i in range(len(track.SetGoals))]
                    ],ch )
        Track_lines=track.SetTrack
        Track_gols=track.SetGoals
    elif 0<x<150 and 300<y<340:
        track.drawing_goal=False
        track.drawing_track=False
        track.new_added_track=False
        track.new_added_goal=False
        track.SetTrack=[]
        track.SetGoals=[]
        Track_lines=[]
        Track_gols=[]
    elif 0<x<150 and 260<y<300:
        ddqn_agent.save_model()
    elif 0<x<150 and 220<y<260:
        filepath = Fd.askopenfile(filetypes=[("h5 files only", ".h5")])
        ddqn_agent.load_model(filepath.name)
        ddqn_agent.update_network_parameters()
    elif 0<x<150 and 180<y<220:
        draw_graphe([sum([ddqn_scores[j] for j in range(i)])/i for i in range(1,len(ddqn_scores))],True)
    elif 0<x<150 and 140<y<180:
        draw_graphe(ddqn_scores,True)
    elif 0<x<150 and 100<y<140:
        userControl = not userControl
        if userControl:
            buttons.manual_label.text='Manual : on'
            clock.schedule_interval(on_text_motion_in,1/60)
        else:
            buttons.manual_label.text='Manual : off'
            clock.unschedule(on_text_motion_in)
    elif 0<x<150 and 60<y<100:
        Track=track()
        Track.setter(True)
        Track_lines=Track.SetTrack
        Track_gols=Track.SetGoals
        for goal in Track_gols:
            goal[0].opacity=0
#################################
windows.on_mouse_press=on_mouse_press
@windows.event       
def on_close():
    if Episodes_counter>50:
        ddqn_agent.save_model()
        print("save model")
    return
@windows.event
def on_mouse_motion(x, y, dx, dy):
    Track.change_track_coords(x,y)
    Track.change_goal_coords(x,y)
def car(carX,carY):
    global Car , carPositionHistory
    Car.sprite.rotation+=carX/(rotation_angel*7)
    Car.Carx+=carY/10*cos((-Car.sprite.rotation+90)*pi/180)
    Car.Cary+=carY/10*sin((-Car.sprite.rotation+90)*pi/180)
    if abs(-Car.sprite.rotation+90)>=360:
        Car.sprite.rotation=90
    Car.update(Car.sprite.rotation,Car.sprite)
    carPositionHistory.append((Car.Carx,Car.Cary))
    return (Car.sprite.rotation,Car.Carx,Car.Cary)
def hover(line,x4,y4,x3,y3,x2,y2,x1,y1):
    if ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))==0:
        return False
    uA = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
    uB = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
    if uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1:
        if line:
            line[2]=False
            line[1].x = x1 + (uA * (x2-x1))
            line[1].y = y1 + (uA * (y2-y1))
            line[0].x2 = x1 + (uA * (x2-x1))
            line[0].y2 = y1 + (uA * (y2-y1))
            line[3].text=str(format(((uA * (x2-x1))**2+(uA * (y2-y1)**2))**0.5, ".2f"))
            return ((uA * (x2-x1))**2+(uA * (y2-y1)**2))**0.5
        else:
            
            return x1 + (uA * (x2-x1)),y1 + (uA * (y2-y1))
    else:
        return False   
def on_draw():
    windows.clear()
    Car.car.draw()
    # Car1.car1.draw()
    track.batch.draw()
    button.button.draw()
windows.on_draw=on_draw
def move(dt):
    global Car,rotation_angel
    if keyboard[window.key.MOTION_DOWN]:
        car(0,Car.velocity)
        if Car.velocity>-20 :
            Car.velocity-=1
    if keyboard[window.key.MOTION_UP]:
        car(0,Car.velocity)
        if Car.velocity<20:
            Car.velocity+=1
    if keyboard[window.key.MOTION_LEFT]:
        car(-Car.velocity,0)
        if rotation_angel>1:
            rotation_angel-=1
    if keyboard[window.key.MOTION_RIGHT]:
        car(Car.velocity,0)
        if rotation_angel>1:
            rotation_angel-=1
def resetgame():
    global default_distance,rotation_angel,carPositionHistory
    Car.Carx=Car.DefaultCarX
    Car.Cary=Car.DefaultCarY
    Car.update(-90,Car.sprite)
    Car.velocity=0
    rotation_angel=1
    default_distance=Car.set_default_distance(Car.lines)
    for i in range(0,len(Track_lines)):
        for j in range(0,len(Car.lines)):
            x=(hover(Car.lines[j],Track_lines[i].x2,Track_lines[i].y2,Track_lines[i].x,Track_lines[i].y,\
                Car.lines[j][0].x2,Car.lines[j][0].y2,Car.lines[j][0].x,Car.lines[j][0].y))
    for _ in range(len(Track_gols)):
        Track_gols[_][1]=False
    if len(Track_gols)>0: 
        Track_gols[0][1]=True
    for _ in keyboard:
        keyboard[_]=False
    for _ in range(len(Track_gols)):
        if Track_gols[_][1]:
            Track_gols[_][0].color=(20,200,20)
        else:
            Track_gols[_][0].color=(200,20,20)
def on_text_motion_in(dt,bytf=True):
    global Car,rotation_angel
    reward=0
    done=False
    move(dt)
    if not keyboard[window.key.MOTION_UP] and Car.velocity>0 :
        Car.velocity-=0.5
        car(0,Car.velocity)
    if not keyboard[window.key.MOTION_DOWN] and Car.velocity<0:
        Car.velocity+=0.5
        car(0,Car.velocity)
    if (not keyboard[window.key.MOTION_LEFT] and not keyboard[window.key.MOTION_RIGHT]) and rotation_angel<11:
        rotation_angel+=5
    distence=[default_distance[i]/1000 for i in range(len(default_distance))]
    # print(distence)
    for i in range(0,len(Track_lines)):
        for j in range(0,len(Car.lines)):
            x=(hover(Car.lines[j],Track_lines[i].x2,Track_lines[i].y2,Track_lines[i].x,Track_lines[i].y,\
                Car.lines[j][0].x2,Car.lines[j][0].y2,Car.lines[j][0].x,Car.lines[j][0].y))
            if x!=False:
                # print(x,"<",distence[j]*100,x<distence[j]*100,end="\n")
                if x<distence[j]*1000:
                    distence[j]=x/1000
        for j in range(len(Car.car_shape)):
            if(hover(False,Track_lines[i].x2,Track_lines[i].y2,Track_lines[i].x,Track_lines[i].y,\
                Car.car_shape[j].x2,Car.car_shape[j].y2,Car.car_shape[j].x,Car.car_shape[j].y)):
                if not done:
                    reward-=1
                    done = True
                    if bytf:
                        print('-1',end="")
    x=True
    for _ in range(len(Track_gols)):
        for i in range(len(Car.car_shape)):
            if (hover(False,Track_gols[_][0].x2,Track_gols[_][0].y2,Track_gols[_][0].x,Track_gols[_][0].y,\
                Car.car_shape[i].x2,Car.car_shape[i].y2,Car.car_shape[i].x,Car.car_shape[i].y)):
                #check if the goal is valid
                if Track_gols[_][1]:
                    Track_gols[_][1]=False
                    if x:
                        if bytf:
                            print('+1',end="")
                        reward+=1
                        x=False
                    if _+1==len(Track_gols):
                        Track_gols[0][1]=True
                    else:
                        Track_gols[_+1][1]=True
                    break;
    for _ in range(len(Track_gols)):
        if Track_gols[_][1]:
            Track_gols[_][0].color=(20,200,20)
        else:
            Track_gols[_][0].color=(200,20,20)
    # update distance
    for line in Car.lines:
        i=Car.lines.index(line)
        line[3].text=str(format(((line[0].x2-(line[0].x))**2 + (line[0].y2-(line[0].y))**2)**0.5, ".2f"))
        distence[i]=(((line[0].x2-(line[0].x))**2 + (line[0].y2-(line[0].y))**2)**0.5)/1000
        if distence[i]==default_distance[i]/1000:
            Car.lines[i][2]=True
    #prevent from stying at the same spot
    if(bytf):
        return distence,reward,done
    else:
        return done

def step(dt,action,bytf=False):
    keyboard[window.key.MOTION_UP]=True
    buttons.move_up.color=(200,20,20)
    if not 0<=action<6 or action==6:
        print(action)
        exit()
    # if action==0:
    #     keyboard[window.key.MOTION_UP]=True
    #     keyboard[window.key.MOTION_DOWN]=False
    #     buttons.move_up.color=(200,20,20)
    #     buttons.move_down.color=(156,134,199)
    # elif action==4:
    #     keyboard[window.key.MOTION_DOWN]=False
    #     keyboard[window.key.MOTION_UP]=False
    #     buttons.move_down.color=(156,134,199)
    #     buttons.move_up.color=(156,34,199)
    elif action==1:
        keyboard[window.key.MOTION_LEFT]=True
        keyboard[window.key.MOTION_RIGHT]=False
        buttons.move_left.color=(200,20,20)
        buttons.move_right.color=(156,34,199)
    elif action==2:
        keyboard[window.key.MOTION_RIGHT]=True
        keyboard[window.key.MOTION_LEFT]=False
        buttons.move_right.color=(200,20,20)
        buttons.move_left.color=(156,34,199)
    # elif action==4:
    #     keyboard[window.key.MOTION_RIGHT]=True
    #     keyboard[window.key.MOTION_LEFT]=False
    #     buttons.move_right.color=(200,20,20)
    #     buttons.move_left.color=(156,34,199)
    elif action==3:
        keyboard[window.key.MOTION_RIGHT]=False
        keyboard[window.key.MOTION_LEFT]=False
        buttons.move_right.color=(156,34,199)
        buttons.move_left.color=(156,34,199)
    return on_text_motion_in(dt,bytf)
def run_agent(dt):
    global learnning_started,Episodes_counter,done,observation,score,counter,reward,gtime,first_game,show_real_car,list_of_actions,render_actions
    if learnning_started and Episodes_counter<N_EPISODES and done and not show_real_car:
        if Episodes_counter==200:    
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        #     ddqn_agent.Plotit()
        if not first_game:
            eps_history.append(ddqn_agent.epsilon)
            ddqn_scores.append(score)
            avg_score = np.mean(ddqn_scores[max(0, Episodes_counter-100):(Episodes_counter+1)])
            if Episodes_counter% REPLACE_TARGET == 0 and Episodes_counter>= REPLACE_TARGET:
                ddqn_agent.update_network_parameters()
                print('<------Netwrok parameters updated------>')
            if Episodes_counter% 100 == 0 and Episodes_counter>= 100:
                ddqn_agent.save_model()
                print("save model")
            print('Episode: ', Episodes_counter,'Score: %.2f' % score,' Sverage score %.2f' % avg_score,' Epsolon: %.4f ' % ddqn_agent.epsilon,' Memory size', ddqn_agent.memory.mem_cntr % ddqn_agent.memory.mem_size)
            render_actions=list_of_actions
            show_real_car=True
        list_of_actions=[]
        Episodes_counter+=1
        resetgame() #reset env 
        done = False
        score = 0
        counter = 0
        observation= [i/1000 for i in default_distance]
        gtime = 0   # set game time back to 0
        if not first_game:
            print('-------------------------------Render game--------------------------------------')
def run_an_episode(dt):
    global learnning_started,done,observation,counter,score,gtime,first_game,list_of_actions
    if learnning_started and not done and not show_real_car:    
        if not show_real_car:
            Car.sprite.opacity=1000
            Car1.sprite.opacity=0
        action = ddqn_agent.choose_action(observation)
        # print(action)
        observation_, reward, done = step(dt,action,True)
        list_of_actions.append(action)
        # This is a countdown if no reward is collected the car will be done within 100 ticks
        if reward == 0:
            counter += 1
            if counter > 100:
                done = True
                print("No Rewards")
        else:
            counter = 0
        print(end="")
        score += reward
        
        ddqn_agent.remember(observation, action, reward, observation_, int(done))
        observation = observation_
        ddqn_agent.learn()
        
        gtime += 1

        if gtime >= TOTAL_GAMETIME:
            done = True
            print('timeout ')
        first_game=False
        if done :
            print("\nnumber of action taken : ",len(list_of_actions))#,"\n", list_of_actions)
def run_a_round(dt):
    global render_actions,show_real_car,first_game
    if show_real_car:
        Car.sprite.opacity=1000
        Car1.sprite.opacity=0
        done=False
        done=step(dt,render_actions[0],False)
        if done:
            render_actions=[]
            first_game=True
            resetgame()
            done=False
            show_real_car=False
            print('\n-------------------------------Render END---------------------------------------')
            return False
        render_actions.pop(0)
        if render_actions==[]:
            resetgame()
            first_game=True
            print('\n-------------------------------Render END---------------------------------------')
            show_real_car=False

clock.schedule_interval(run_agent, 1/60)
clock.schedule_interval(run_an_episode, 1/60)
clock.schedule_interval(run_a_round, 1/60)

# uncomment the following line if you want to controlle the car PS: don't train your model while controlling the car

# clock.schedule_interval(on_text_motion_in,1/60)


def run_game():
    resetgame()
    app.run()

if __name__ == '__main__':
    run_game()