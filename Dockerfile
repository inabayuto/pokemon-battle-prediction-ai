FROM python:3.12-slim

WORKDIR /workspace

# システムの依存関係をインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# requirements.txtをコピーしてパッケージをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Jupyterのカーネルを明示的にインストール
RUN python -m ipykernel install --user --name python3 --display-name "Python 3"

EXPOSE 8888
