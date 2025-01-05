import openai
import os
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()

def test_openai_connection():
    """
    OpenAI APIが正常に接続されているかを確認するためのテスト。
    """
    try:
        # APIキーを設定
        openai.api_key = os.getenv("OPENAI_API_KEY")

        # サンプルプロンプト
        prompt = "こんにちは、OpenAI。接続が正常に行われているか確認するためのテストです。"

        # 新しいインターフェースでリクエストを送信
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "あなたは親切なアシスタントです。"},
                {"role": "user", "content": prompt},
            ]
        )

        # 応答を表示
        print("OpenAIからの応答:")
        print(response["choices"][0]["message"]["content"].strip())

    except Exception as e:
        print(f"OpenAI接続エラー: {e}")

# 実行
if __name__ == "__main__":
    test_openai_connection()


