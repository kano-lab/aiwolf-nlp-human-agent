#!/bin/sh

# 仮想環境の作成
python -m venv .venv

# OS に応じて仮想環境を有効化
if [ "$OS" = "Windows_NT" ]; then
    . .venv/Scripts/activate
else
    . .venv/bin/activate
fi

# 設定ファイルのコピー（存在する場合はスキップ）
if [ ! -f src/res/config.ini ]; then
    cp src/res/config.ini.example src/res/config.ini
fi

if [ ! -f src/res/log.ini ]; then
    cp src/res/log.ini.example src/res/log.ini
fi

# パッケージのインストール
pip install .
