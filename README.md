# aiwolf-nlp-human-agent

人狼知能コンテスト(自然言語部門)の人間参加用サンプルエージェントです。\
このプログラムは[aiwolf-nlp-agent](https://github.com/kano-lab/aiwolf-nlp-agent)をベースにしているため、実行方法などの詳細はこちらをご覧ください。

## 環境構築
```
source setup.sh
```

## 実行方法
```x
python3 src/main.py 
```

> [!NOTE]
> ゲームの実行にはゲームサーバの立ち上げ、残り4プレイヤーの立ち上げが必要です。\
> 詳細については下記をご覧ください。\
> プレイヤーの立ち上げ: [aiwolf-nlp-agent](https://github.com/kano-lab/aiwolf-nlp-agent)\
> ゲームサーバの立ち上げ: [aiwolf-nlp-server](https://github.com/kano-lab/aiwolf-nlp-server)

## ゲーム画面

### スタート画面
名前を入力して"Start"ボタンを押すことでゲームを開始することができます。
ボタンをクリックすることで押すことができるほか、Tabで選択の切り替え、Enterで決定することができます。

![スクリーンショット 2025-02-08 17 43 17](https://github.com/user-attachments/assets/606c04b4-d179-415b-8c6e-8eba6fe673f4)

### 会話画面
画面左側が会話履歴で、右側は自身の設定です。
会話履歴右上の数字は入力の制限時間です。

![スクリーンショット 2025-02-08 17 48 49](https://github.com/user-attachments/assets/732eb5ae-abe8-4b0c-b6b9-ae99e25b9b41)

### 投票画面
投票、占い、襲撃の際の画面です。
クリックのほか、Enterでも決定できます。

![スクリーンショット 2025-02-08 17 48 21](https://github.com/user-attachments/assets/9c0ec888-ed73-4428-b09d-b484510e85cc)
