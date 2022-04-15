# Self Driving Cars Using Double Deep Q-learning Network 

## Introduction
This is a Tensorflow implementation of Double-DQN Agent [[paper](https://arxiv.org/abs/1509.06461)]


In this work, I represent a simple self-driving car using the DDQN algorithm.

The algorithm consists of two main parts. The model and the agent

- Model

The model is an artificial neural network that consists of five layers. <br>
 -> The input layer : represents the distance of the car from the walls on the front side, left side, and right side. <br>
 -> hidden layers : There are 3 hidden layers, each layer containing 32 neurons. <br>
 -> out-put layer : The output layer represents the action that the agent takes based on the calculation of the NN, <br>
    There are three possible actions: left, right, and break (decrease speed).<br>
    
 Model Structure
 
 <p align="center"><img src="https://github.com/bellaabdelouahab/Double-Deep-Q-learning-Network-For-Self-Driving-Cars/blob/main/Media/IMG_20220415_101040.jpg" width="100%" alt=""/></p>
 
 - Agent
  The Q-learning agent uses a Q-table, which is a multi-dimotional table. <br>
  containsin the different stateofom thenvironmentnt beside the score for that state <br>
  The q-table for each state is normally updated by the corresponding scroe for that state. <br>
  But with using the DDQN algorithm, we actually use two models known as Q-eval and Q-target. <br>
  The Q-eval is the model responsible for the training and taking action. <br>
  On the other hand, we do not train the Q-target; instead, we only update its weights every specified number of episodes. <br>
  The role of the Q-target is to update the Q-table so that the agent does not get stuck in one area and get used to low scores. <br>
  Further explanation can be found in the original paper. <br>

<p align="center"><img src="https://miro.medium.com/max/1400/1*o8PMTWmT1XK1jdSK59QrYQ.png" width="100%" alt=""/></p>

We minimize the mean squared error between Q and Q* , 
but we have Q' slowly copy the parameters of Q .
We can do so by periodically hard-copying over the parameters


<br><br>

## Overview
- `Model/`: includes different trained models saved in an H5 format.
- `Track/`: contains the structure of the track to easley train model on various tracks.
- `Learning rate graphs/`: includes the graphical representation of the training (score & average score).


## Requirements
The code is developed using python 3.9.0 on Windows 10. NVIDIA GPU (GT 340M or above) ared needed to train and test. 
See [`requirements.txt`](requirements.txt ) for other dependencies.
