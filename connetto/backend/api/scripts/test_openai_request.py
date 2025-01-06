import openai
import os
from dotenv import load_dotenv
import logging

# ログの設定
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# .envファイルを読み込む
load_dotenv()

# APIキーを設定
openai.api_key = os.getenv("OPENAI_API_KEY")

def test_openai_request():
    """
    OpenAI APIが正常に接続されているかを確認するためのテスト関数。
    """
    try:
        logging.info("OpenAIリクエストを送信します...")

        prompt = (
        f"横浜駅、品川駅二つの駅の中間駅を教えてください。"
        f"答えるのは駅名だけで大丈夫です。"
    )
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ]
        )

        message_content = response.choices[0].message.content

        logging.info(message_content)

    except Exception as e:  # すべてのエラーをキャッチ
        logging.error(f"エラーが発生しました: {e}")

# 実行部分
if __name__ == "__main__":
    test_openai_request()


