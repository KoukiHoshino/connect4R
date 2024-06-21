import numpy as np
from State import State_3_3_3 
from State import State_7_7_4 
from State import State_osero
from State import State_6_8_4 as State  
from Net import Net
from Node import Node
from Tree import Tree
from Net import Net
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import matplotlib.pyplot as plt
import csv
import pandas as pd

BLACK, WHITE = 1, -1
def random_agent(state):
    # ランダムな手を返すエージェント
    legal_actions = state.legal_actions()
    print(legal_actions )
    if len(legal_actions) == 0:
      print(legal_actions)
      return -1
    else:
        print(legal_actions)
        return np.random.choice(legal_actions)
        
def AI_agent(state):
    # ランダムな手を返すエージェント
    legal_actions = state.legal_actions()
    net1 = Net()
    net1.load_state_dict(torch.load(f"models/sim0_UCB_700_50.pth"))
    
    print(legal_actions )
    if len(legal_actions) == 0:
      print(legal_actions)
      return -1
    else:
        p, _ = net1.predict(state)
        action = sorted([(a, p[a]) for a in legal_actions], key=lambda x:-x[1])[0][0]
        print(legal_actions)
        return action

def human_agent(state):
    # ユーザーが手を指定するエージェント
    legal_actions = state.legal_actions()
    if legal_actions == None:
      return -1
    while True:
        print(f"your action is {legal_actions}\n")
        action_str = input("Your action? (e.g. A3): ")
        if len(action_str) != 2:
            print("Invalid input. Please input a letter and a number.")
            continue
        x, y = action_str[0], action_str[1]
        if x not in State.X or y not in State.Y:
            print("Invalid input. Please input a letter between A and F and a number between 1 and 6.")
            continue
        action = state.str2action(action_str)
        if action not in legal_actions:
            print("Invalid action. Please input a legal action.")
            continue
        return action

def play_game(player1, player2):
    state = State()
    count111 = 0
    print(state)
    while not state.terminal():
        if state.color == BLACK:
            action = player1(state)
            if action == -1:
              
              count111 = count111 + 1
              print(state.color)
              #state.color = - state.color

              print(f"count111=={count111}")
              if count111  > 2:
                print(f"count111=={count111}")

                break


            else:
              state.play(action)
              count111 = 0
        else:
            action = player2(state)
            if action == -1:
              #state.color == BLACK
              #state.color = - state.color
              count111 = count111 + 1
              print(f"count111=={count111}")
              if count111 >= 2:
                print(f"count111=={count111}")
                break

            else:
              state.play(action)
              count111 = 0
        print(state)
    #state.win_color = state.pass_drop()
    print(state.win_color)
    print(state)
    if state.win_color== 1:
        print("BLACK wins!")
    elif state.win_color == -1:
        print("WHITE wins!")
    else:
        print("Draw!")
        
# ランダムな手を打ち続けるAgentとユーザーが手を指定することができるAgentの対戦
play_game(human_agent, AI_agent)
