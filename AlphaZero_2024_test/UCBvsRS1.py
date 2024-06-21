import numpy as np
from Net import Net
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import matplotlib.pyplot as plt
import pandas as pd
from common import show_net
from common import gen_target
from common import train
from common import vs_random
from common import vs_player
from common import vs_random_result
from common import vs_ucb_result

# 初期ネットワークで探索を行う

"""# 学習コード"""

# ニューラルネットの学習
batch_size = 32
num_epochs = 30

"""# Main 文
実際に学習と対戦の実行を行うところ

"""
#対戦 
#ここに対戦させたい2つのモデルの相対パスを書く.
PATH1 = "models/sim0_RS0.6_0_50_1000tr.pth" 
PATH2 = "models/sim0_UCB_100_50.pth"
# 学習のための Self-play の試合数
num_games = 1
sims = 1000
# 何回の試合ごとに学習するか
num_train_steps = 1
# 何回先読みするか
num_simulations = 50
check1 = 0
net3 = Net()
net_ucb = Net()
R = 0.6
result = np.zeros((num_games,sims)) #結果を保存
for i in range(sims): 
    for g in range(num_games):
        if g % 1 == 0 : #横軸学習回数のためこのような表記. 後ほど変更
            net3.load_state_dict(torch.load(PATH1)) #ここでパスを指定
            net_ucb.load_state_dict(torch.load(PATH2))
            print("sim=",i)
            print("game=",g)
            n=vs_ucb_result(net3,net_ucb)
            result[g,i] = n
            df = pd.DataFrame(result)
            df.to_csv(f'kekka/sim10_RS{R}_numsim{num_simulations}_1000vsUCB__result.csv')

print(np.mean(result))
print("finish")
