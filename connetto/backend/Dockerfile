FROM python:3.11-slim

# 作業ディレクトリを指定
WORKDIR /app

# 必要なシステムパッケージをインストール
RUN apt-get update && apt-get install -y libpq-dev gcc

# requirements.txt をコピー
COPY requirements.txt .

# パッケージをインストール
RUN pip install --no-cache-dir -r requirements.txt

# 必要なツールのインストール
RUN pip install black isort flake8 pre-commit

# ソースコードをコピー
COPY . .

# ポート8000を公開
EXPOSE 8000

# コンテナ起動時に実行するコマンド
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
