import numpy as np
import os
import time
import tkinter as tk
import tkinter.filedialog as Fd
from math import cos, sin, pi
from pickle import dump
from pyglet import window, clock, app, options

from components.Car import Set_car, Set_car2
from components.buttons import button
from components.learning_rate import draw_graphe
from ddqn_Agent import DDQNAgent
from Track import track

# Constants
TOTAL_GAMETIME = 10000  # Maximum game time for one episode
N_EPISODES = 10001
REPLACE_TARGET = 100

# Global variables
Episodes_counter = 0
GameTime = 0
GameHistory = []
ddqn_scores = []
eps_history = []
observation = []
carPositionHistory = []
done = True
reward = 0
score = 0
counter = 0
gtime = 0
first_game = True
learnning_started = False
userControl = False
list_of_actions = []
show_real_car = False

# Initialize the DDQN agent
ddqn_agent = DDQNAgent(alpha=0.001, gamma=0.998, n_actions=3, epsilon=0.1, batch_size=128, input_dims=3)

# Create the game window
windows = window.Window(1000, 500)
windows.set_location(int(windows.screen.width / 2 - windows.width / 2), int(windows.screen.height / 2 - windows.height / 2))
windows.set_minimum_size(1000, 500)

# Set up tkinter root
root = tk.Tk()
root.withdraw()

# Set OpenGL debug options
options['debug_gl'] = False

# Keyboard handler
keyboard = window.key.KeyStateHandler()
windows.push_handlers(keyboard)

# Initialize the game environment
rotation_angle = 1
Track = track()
Track.setter()
Track_lines = Track.SetTrack
Track_goals = Track.SetGoals
for goal in Track_goals:
    goal[0].opacity = 0

# Initialize buttons and car components
buttons = button()
buttons.go()
Car = Set_car()
Car.gocar()
Car1 = Set_car2()
Car1.sprite.opacity = 1000
default_distance = Car.set_default_distance(Car.lines)

def on_mouse_press(x, y, button, modifier):
    global learnning_started, Track_lines, Track_goals, Track, userControl
    if Track.drawing_track:
        Track.add_track(x, y)
    elif Track.drawing_goal:
        Track.add_goal(x, y)
    handle_button_presses(x, y)

def handle_button_presses(x, y):
    """Handle button presses in the game window."""
    global learnning_started, Track_lines, Track_goals, Track
    if 0 < x < 150 :
        if 460 < y < 500:
            toggle_learning()
        elif 420 < y < 460:
            toggle_drawing('track')
        elif 380 < y < 420:
            toggle_drawing('goal')
        elif 340 < y < 380:
            save_track()
        elif 300 < y < 340:
            clear_track()
        elif 260 < y < 300:
            ddqn_agent.save_model()
        elif 220 < y < 260:
            load_model()
        elif 180 < y < 220:
            draw_ddqn_scores(True)
        elif 140 < y < 180:
            draw_ddqn_scores(False)
        elif 100 < y < 140:
            toggle_user_control()
        elif 60 < y < 100:
            reset_track()

def toggle_learning():
    """Toggle the learning state of the DDQN agent."""
    global learnning_started
    learnning_started = not learnning_started
    if learnning_started:
        buttons.button_text.text = 'Stop learning'
    else:
        buttons.button_text.text = 'Start learning'

def toggle_drawing(mode):
    """Toggle the drawing mode between track and goal."""
    global Track
    if mode == 'track':
        Track.drawing_track = not Track.drawing_track
        if Track.drawing_track:
            buttons.button_draw_track.text = 'Drawing'
            buttons.button_draw_goal.text = 'Draw Goal'
            Track.drawing_goal = False
            Track.new_added_goal = False
        else:
            buttons.button_draw_track.text = 'Draw Line'
            Track.new_added_track = False
    elif mode == 'goal':
        Track.drawing_goal = not Track.drawing_goal
        if Track.drawing_goal:
            buttons.button_draw_goal.text = 'Drawing'
            buttons.button_draw_track.text = 'Draw Line'
            Track.drawing_track = False
            Track.new_added_track = False
        else:
            buttons.button_draw_goal.text = 'Draw Goal'
            Track.new_added_goal = False

def save_track():
    """Save the current track to a file."""
    global Track_lines, Track_goals
    timestr = time.strftime("%d-%m-%Y-%H-%M")
    with open('Tracks/Track-' + timestr + '.dat', 'wb') as ch:
        dump([
            [[Track.SetTrack[i].x, Track.SetTrack[i].y, Track.SetTrack[i].x2, Track.SetTrack[i].y2] for i in range(len(Track.SetTrack))],
            [[Track.SetGoals[i][0].x, Track.SetGoals[i][0].y, Track.SetGoals[i][0].x2, Track.SetGoals[i][0].y2] for i in range(len(Track.SetGoals))]
        ], ch)
    Track_lines = Track.SetTrack
    Track_goals = Track.SetGoals

def clear_track():
    """Clear the current track and goals."""
    global Track_lines, Track_goals
    Track.SetTrack = []
    Track.SetGoals = []
    Track_lines = []
    Track_goals = []

def load_model():
    """Load a model file using a file dialog."""
    filepath = Fd.askopenfile(filetypes=[("h5 files only", ".h5")])
    if filepath:
        ddqn_agent.load_model(filepath.name)
        ddqn_agent.update_network_parameters()

def draw_ddqn_scores(smooth):
    """Draw the DDQN scores graph."""
    if smooth:
        scores = [sum(ddqn_scores[j] for j in range(i)) / i for i in range(1, len(ddqn_scores))]
        draw_graphe(scores, True)
    else:
        draw_graphe(ddqn_scores, True)

def toggle_user_control():
    """Toggle the user control mode."""
    global userControl
    userControl = not userControl
    if userControl:
        buttons.manual_label.text = 'Manual: on'
        clock.schedule_interval(on_text_motion_in, 1 / 60)
    else:
        buttons.manual_label.text = 'Manual: off'
        clock.unschedule(on_text_motion_in)

def reset_track():
    """Reset the track to the initial state."""
    global Track, Track_lines, Track_goals
    Track = track()
    Track.setter(True)
    Track_lines = Track.SetTrack
    Track_goals = Track.SetGoals
    for goal in Track_goals:
        goal[0].opacity = 0

# Event handlers for Pyglet window
windows.on_mouse_press = on_mouse_press

@windows.event
def on_close():
    if Episodes_counter > 50:
        ddqn_agent.save_model()
        print("Model saved")
    return True

@windows.event
def on_mouse_motion(x, y, dx, dy):
    Track.change_track_coords(x, y)
    Track.change_goal_coords(x, y)

def car_movement(carX, carY):
    """Handle car movement based on input."""
    global Car, carPositionHistory
    Car.sprite.rotation += carX / (rotation_angle * 7)
    Car.Carx += carY / 10 * cos((-Car.sprite.rotation + 90) * pi / 180)
    Car.Cary += carY / 10 * sin((-Car.sprite.rotation + 90) * pi / 180)
    if abs(-Car.sprite.rotation + 90) >= 360:
        Car.sprite.rotation = 90
    Car.update(Car.sprite.rotation, Car.sprite)
    carPositionHistory.append((Car.Carx, Car.Cary))
    return (Car.sprite.rotation, Car.Carx, Car.Cary)

def hover(line, x4, y4, x3, y3, x2, y2, x1, y1):
    """Detect if a hover event occurs between the car and track lines or goals."""
    if ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)) == 0:
        return False
    uA = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))
    uB = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))
    if uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1:
        if line:
            line[2] = False
            line[1].x = x1 + (uA * (x2 - x1))
            line[1].y = y1 + (uA * (y2 - y1))
            line[0].x2 = x1 + (uA * (x2 - x1))
            line[0].y2 = y1 + (uA * (y2 - y1))
            line[3].text = str(format(((uA * (x2 - x1)) ** 2 + (uA * (y2 - y1) ** 2)) ** 0.5, ".2f"))
            return ((uA * (x2 - x1)) ** 2 + (uA * (y2 - y1) ** 2)) ** 0.5
        else:
            return x1 + (uA * (x2 - x1)), y1 + (uA * (y2 - y1))
    else:
        return False

@windows.event
def on_draw():
    """Draw the game window."""
    windows.clear()
    Car.car.draw()
    Track.batch.draw()
    buttons.buttono.draw()

def move(dt):
    """Handle car movements based on keyboard input."""
    global Car, rotation_angle
    if keyboard[window.key.MOTION_DOWN]:
        car_movement(0, Car.velocity)
        if Car.velocity > -20:
            Car.velocity -= 1
    if keyboard[window.key.MOTION_UP]:
        car_movement(0, Car.velocity)
        if Car.velocity < 20:
            Car.velocity += 1
    if keyboard[window.key.MOTION_LEFT]:
        car_movement(-Car.velocity, 0)
        if rotation_angle > 1:
            rotation_angle -= 1
    if keyboard[window.key.MOTION_RIGHT]:
        car_movement(Car.velocity, 0)
        if rotation_angle > 1:
            rotation_angle -= 1

def reset_game():
    """Reset the game environment to its initial state."""
    global default_distance, rotation_angle, carPositionHistory
    Car.Carx = Car.DefaultCarX
    Car.Cary = Car.DefaultCarY
    Car.update(-90, Car.sprite)
    Car.velocity = 0
    rotation_angle = 1
    default_distance = Car.set_default_distance(Car.lines)
    for i in range(len(Track_lines)):
        for j in range(len(Car.lines)):
            x = (hover(Car.lines[j], Track_lines[i].x2, Track_lines[i].y2, Track_lines[i].x, Track_lines[i].y,
                       Car.lines[j][0].x2, Car.lines[j][0].y2, Car.lines[j][0].x, Car.lines[j][0].y))
    for _ in range(len(Track_goals)):
        Track_goals[_][1] = False
    if len(Track_goals) > 0:
        Track_goals[0][1] = True
    print("Keyboard reset")
    for _ in keyboard.data.keys():
        keyboard.on_key_release(_, 0)
    for _ in range(len(Track_goals)):
        if Track_goals[_][1]:
            Track_goals[_][0].color = (20, 200, 20)
        else:
            Track_goals[_][0].color = (200, 20, 20)

def on_text_motion_in(dt, bytf=True):
    """Handle continuous text motion based on keyboard input."""
    global Car, rotation_angle
    reward = 0
    done = False
    move(dt)
    if not keyboard[window.key.MOTION_UP] and Car.velocity > 0:
        Car.velocity -= 0.5
        car_movement(0, Car.velocity)
    if not keyboard[window.key.MOTION_DOWN] and Car.velocity < 0:
        Car.velocity += 0.5
        car_movement(0, Car.velocity)
    if (not keyboard[window.key.MOTION_LEFT] and not keyboard[window.key.MOTION_RIGHT]) and rotation_angle < 11:
        rotation_angle += 5
    distance = [default_distance[i] / 1000 for i in range(len(default_distance))]
    for i in range(len(Track_lines)):
        for j in range(len(Car.lines)):
            x = (hover(Car.lines[j], Track_lines[i].x2, Track_lines[i].y2, Track_lines[i].x, Track_lines[i].y,
                       Car.lines[j][0].x2, Car.lines[j][0].y2, Car.lines[j][0].x, Car.lines[j][0].y))
            if x is not False and x < distance[j] * 1000:
                distance[j] = x / 1000
        for j in range(len(Car.car_shape)):
            if hover(False, Track_lines[i].x2, Track_lines[i].y2, Track_lines[i].x, Track_lines[i].y,
                     Car.car_shape[j].x2, Car.car_shape[j].y2, Car.car_shape[j].x, Car.car_shape[j].y):
                if not done:
                    reward -= 1
                    done = True
                    if bytf:
                        print('-1', end="")
    x = True
    for _ in range(len(Track_goals)):
        for i in range(len(Car.car_shape)):
            if hover(False, Track_goals[_][0].x2, Track_goals[_][0].y2, Track_goals[_][0].x, Track_goals[_][0].y,
                     Car.car_shape[i].x2, Car.car_shape[i].y2, Car.car_shape[i].x, Car.car_shape[i].y):
                if Track_goals[_][1]:
                    Track_goals[_][1] = False
                    if x:
                        if bytf:
                            print('+1', end="")
                        reward += 1
                        x = False
                    if _ + 1 == len(Track_goals):
                        Track_goals[0][1] = True
                    else:
                        Track_goals[_ + 1][1] = True
                    break
    for _ in range(len(Track_goals)):
        if Track_goals[_][1]:
            Track_goals[_][0].color = (20, 200, 20)
        else:
            Track_goals[_][0].color = (200, 20, 20)
    # Update distance
    for line in Car.lines:
        i = Car.lines.index(line)
        line[3].text = str(format(((line[0].x2 - (line[0].x)) ** 2 + (line[0].y2 - (line[0].y)) ** 2) ** 0.5, ".2f"))
        distance[i] = (((line[0].x2 - (line[0].x)) ** 2 + (line[0].y2 - (line[0].y)) ** 2) ** 0.5) / 1000
        if distance[i] == default_distance[i] / 1000:
            Car.lines[i][2] = True
    # Prevent from staying at the same spot
    if bytf:
        return distance, reward, done
    else:
        return done

def step(dt, action, bytf=False):
    """Take a step in the game based on the action."""
    keyboard.on_key_press(window.key.MOTION_UP, 0)
    buttons.move_up.color = (200, 20, 20)
    if not 0 <= action < 6 or action == 6:
        print(action)
        exit()
    elif action == 1:
        keyboard.on_key_press(window.key.MOTION_LEFT, 0)
        keyboard.on_key_release(window.key.MOTION_RIGHT, 0)
        buttons.move_left.color = (200, 20, 20)
        buttons.move_right.color = (156, 34, 199)
    elif action == 2:
        keyboard.on_key_press(window.key.MOTION_RIGHT, 0)
        keyboard.on_key_release(window.key.MOTION_LEFT, 0)
        buttons.move_right.color = (200, 20, 20)
        buttons.move_left.color = (156, 34, 199)
    elif action == 3:
        keyboard.on_key_release(window.key.MOTION_RIGHT, 0)
        keyboard.on_key_release(window.key.MOTION_LEFT, 0)
        buttons.move_right.color = (156, 34, 199)
        buttons.move_left.color = (156, 34, 199)
    return on_text_motion_in(dt, bytf)

def run_agent(dt):
    """Run the DDQN agent to make decisions based on the game state."""
    global learnning_started, Episodes_counter, done, observation, score, counter, reward, gtime, first_game, show_real_car, list_of_actions, render_actions
    if learnning_started and Episodes_counter < N_EPISODES and done and not show_real_car:
        if Episodes_counter == 200:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        if not first_game:
            eps_history.append(ddqn_agent.epsilon)
            ddqn_scores.append(score)
            avg_score = np.mean(ddqn_scores[max(0, Episodes_counter - 100):(Episodes_counter + 1)])
            if Episodes_counter % REPLACE_TARGET == 0 and Episodes_counter >= REPLACE_TARGET:
                ddqn_agent.update_network_parameters()
                print('<------Network parameters updated------>')
            if Episodes_counter % 100 == 0 and Episodes_counter >= 100:
                ddqn_agent.save_model()
                print("Model saved")
            print('Episode: ', Episodes_counter, 'Score: %.2f' % score, 'Average score %.2f' % avg_score, 'Epsilon: %.4f ' % ddqn_agent.epsilon, 'Memory size', ddqn_agent.memory.mem_cntr % ddqn_agent.memory.mem_size)
            render_actions = list_of_actions
            show_real_car = True
        list_of_actions = []
        Episodes_counter += 1
        reset_game()  # reset environment
        done = False
        score = 0
        counter = 0
        observation = [i / 1000 for i in default_distance]
        gtime = 0  # set game time back to 0
        if not first_game:
            print('-------------------------------Render game--------------------------------------')

def run_an_episode(dt):
    """Run a single episode of the game."""
    global learnning_started, done, observation, counter, score, gtime, first_game, list_of_actions
    if learnning_started and not done and not show_real_car:
        if not show_real_car:
            Car.sprite.opacity = 1000
            Car1.sprite.opacity = 0
        action = ddqn_agent.choose_action(observation)
        observation_, reward, done = step(dt, action, True)
        list_of_actions.append(action)
        # This is a countdown if no reward is collected the car will be done within 100 ticks
        if reward == 0:
            counter += 1
            if counter > 100:
                done = True
                print("No Rewards")
        else:
            counter = 0
        score += reward

        ddqn_agent.remember(observation, action, reward, observation_, int(done))
        observation = observation_
        ddqn_agent.learn()

        gtime += 1

        if gtime >= TOTAL_GAMETIME:
            done = True
            print('Timeout')
        first_game = False
        if done:
            print("\nNumber of actions taken: ", len(list_of_actions))

def run_a_round(dt):
    """Run a round of the game using precomputed actions."""
    global render_actions, show_real_car, first_game
    if show_real_car:
        Car.sprite.opacity = 1000
        Car1.sprite.opacity = 0
        done = False
        done = step(dt, render_actions[0], False)
        if done:
            render_actions = []
            first_game = True
            reset_game()
            done = False
            show_real_car = False
            print('\n-------------------------------Render END---------------------------------------')
            return False
        render_actions.pop(0)
        if render_actions == []:
            reset_game()
            first_game = True
            print('\n-------------------------------Render END---------------------------------------')
            show_real_car = False

# Schedule game loops
clock.schedule_interval(run_agent, 1 / 60)
clock.schedule_interval(run_an_episode, 1 / 60)
clock.schedule_interval(run_a_round, 1 / 60)

# Uncomment the following line if you want to control the car manually. Note: do not train your model while controlling the car manually.
# clock.schedule_interval(on_text_motion_in, 1 / 60)

def run_game():
    """Start and run the game."""
    print("Game is starting")
    reset_game()
    print("Game is running")
    app.run()

if __name__ == '__main__':
    run_game()
