import openai
import os
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()

# APIキーを設定
openai.api_key = os.getenv("OPENAI_API_KEY")

def test_openai_request():
    try:
        print("OpenAIリクエストを送信します...")

        # リクエスト送信
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "こんにちは、接続が正常か確認しています。"},
            ]
        )

        print("ChatGPTからの応答:")
        print(response['choices'][0]['message']['content'])

    except openai.error.OpenAIError as e:
        print(f"OpenAI APIエラー: {e}")
    except Exception as e:
        print(f"その他のエラー: {e}")

if __name__ == "__main__":
    test_openai_request()