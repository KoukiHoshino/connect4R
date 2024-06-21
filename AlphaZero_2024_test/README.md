# 概要
- 情報システム総合演習2024でAlphaZeroを扱う人向けのリポジトリです
- Dockerでいいリポジトリが見つからなかったのでanacondaなどでの環境構築を想定

## AlphaZeroとは
- 囲碁、将棋、チェスなどのボードゲームにおいて人間超えの性能を出したもの
    - 今回はその縮小版を扱うことで、その強さを体験する

## 今回できること
- 別のゲームでAlphaZeroの強さを体験する
    - 他のゲームを実装できるのであれば可能
    - 去年はこちらをやった
- 別のアルゴリズムを追加して元のAlphaZeroと対戦などで比較
    - 去年はこちらもやった
        - 特に高橋研での研究対象であるAlphaZeroのUCTをRSに交換して性能比較
- あえて負けさせるめちゃめちゃ弱いやつを作る
    - オセロとかかな
- 段階的な強さの実装

- 
## 環境
-  必要な物のインストール
    - 基本的にPyTorchとNumpyがあればコードは動くのでインストールをお願いします
        -  `pip3 install torch torchvision torchaudio `
        -  `pip3 install numpy`
    - pandasもファイルの保存時に使っているので余裕があればインストール
        - `pip3 install numpy`

## 三目並べを AlphaZero で学習したプログラム(このコードの原型)
AlphaZero の解説
https://qiita.com/KazuyaTomita/items/bd53bc2c7a2bf016f7cb  
完全な Self-play(自己対戦)のみで学習する強力な強化学習 AI

強化学習アーキテクチャでハンズオンとして公開されたコード
URL: https://rlarch.connpass.com/event/138893/
製作者：大渡勝己 (フリーランス)

# チュートリアル
1. Pytorch関係のインストール
    - 基本的にPyTorchとNumpyが動けばこのコードは動くのでAnacondaなどで仮想環境を作っておくと良いです
2. _UCB_save.pyと_RS_save.pyを実行し, modelsの中にモデル名.pthが作成されていることを確認
    - モデル名は必要に応じて書き換えるとよい
3. UCBvsRS1.pyの読み込むモデル名を適宜変更して実行することで、対戦結果がcsvファイルで出力されます
4. 出力されたファイルを任意のコードで可視化してください
    - いずれ誰かがplot.pyなどで実装

# 各ファイルの説明
## 定義など
### state.py
- 環境を用意ゲームの盤面. 遷移などのルールを決める. 
- 違うゲームで試したければここをいじる
    - オセロ(6×6)、3目ならべ、7×7の4目並べがデフォであります
- 平たくいうとゲームを実装する場所

### Net.py
- ニューラルネットワークの定義
- サイズなんかは引数で取ってなかった気もするので、ゲームなどに合わせて編集が必要かも？
    - 基本的にはいじらなくても動作しますが、パラメータチューニングをするときにいじる必要があるかも

### node.py
- ある1状態の探索結果を保存
- 基本いじらなくてOK

### tree.py
- モンテカルロ木探索を定義
    - RSのものとUCBのものがあります
- RSの設定(パラメータ変更)などのためにいじる必要あり？

### common.py
- いろんなファイルで使われるものをまとめて定義してあるファイル
- 基本いじらなくてOK

## 実行ファイル（実際に自分たちが動かすときに使うファイル）

### RS_save.py
- treeファイルで設定した目的水準に従って学習したRSのニューラルネットワークをmodel_save_name で保存するファイル
   - State,Net,Tree,Tree_UCB
    -  基本的に下記を変更すればok
```
sims = 10
num_games = 1001
num_train_steps = 1
num_simulations = 50
```
```
    if g % 100 == 0:
        model_save_name = f'sim{i}_RS0.6_{g}_{num_simulations}_1000tr.pth'
        torch.save(net_ucb.state_dict(), f"{model_save_name}")
```
※  pthファイル名が同じだと上書きされてしまうので注意
### UCB_save.py
- 学習したUCBのニューラルネットワークをmodel_save_name で保存するファイル
- 学習したUCBのニューラルネットワークをmodel_save_name.pthに従って保存する
- State,Net,Tree,Tree_UCB
- 基本はRS_save.pyと同じ
### UCBvsRS1ファイル
- RS_saveファイル、UCB_saveファイルによって保存したpthファイルをフォルダーから呼び出し対戦させkekkaフォルダへ出力するファイル
```
sims = 10
num_games = 101
num_train_steps = 1
num_simulations = 50
```
```
       if g % 100 == 0 :
            net3.load_state_dict(torch.load(f"sim{i}_RS{R}_{g}_{num_simulations}_1000tr.pth"))
            net_ucb.load_state_dict(torch.load(f"sim{i}_UCB_100_50.pth"))
            print("sim=",i)
            print("game=",g)
            n=vs_ucb_result(net3,net_ucb)
            result[g,i] = n
            df = pd.DataFrame(result)
            df.to_csv(f'sim10_RS{R}_numsim{num_simulations}_1000vsUCB__result.csv')
```
※ pthファイルが存在しないとエラーが出るので注意

