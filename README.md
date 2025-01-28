# Connetto
社内のコミュニケーションの場を自動で設定してくれるアプリ<br>
法人が福利厚生ツールとして契約。<br>
利用者は、飲み会など参加希望の日時や希望条件を登録するだけで、飲み会の場所や日時を自動で提案・決定します。<br>
これにより、幹事の負担を大幅に軽減し、飲み会を迅速にセットアップできます。
<br />

## 画面イメージ
| トップ画面 |　ログイン画面 |　ホーム画面 |
| ---- | ---- | ---- |
| <img src="https://github.com/user-attachments/assets/4d9c142f-e676-454d-8713-583af39e5b5b" width="290">| <img src="https://github.com/user-attachments/assets/3ea7200c-f1dc-4b66-823f-bb47f5afd93c" width="290"> | <img src="https://github.com/user-attachments/assets/f2b74edc-e165-430a-806e-704bf0e1210c" width="290"> |
| ログイン前のトップ画面 | アドレスとパスワードでの認証 | ホーム画面で日時/希望条件を登録できます |

| 通知BOX画面 |　登録内容確認画面 |　一覧画面 |
| ---- | ---- | ---- |
| <img src="https://github.com/user-attachments/assets/dce9fde9-5345-4294-85e2-128e787f5059" width="290">| <img src="https://github.com/user-attachments/assets/07579c29-e126-4414-a7b0-1346148a2670" width="290"> | <img src="https://github.com/user-attachments/assets/7b84c65a-a1fc-4e11-81b9-5523dc7c8e70" width="290"> |
| 通知が届く画面で通知のバッチも表示 | 希望登録した日時の変更や削除が可能 | 開催が決定した会の一覧を表示 |

<br />

## 使用技術
| Category          | Technology Stack                                     |
| ----------------- | --------------------------------------------------   |
| Frontend          | TypeScript, Next.js                                  |
| Backend           | Python, Django                                       |
| Database          | PostgreSQL                                           |
| Environment setup | Docker                                               |
| Design            | Figma                                                |
| API               | OpenAIAPI, GooglemapAPI, HotpepperAPI                |
| Authentication    | Firebase                                             |
| etc.              | ESLint, Prettier, GitHub                             |

<br />

## 機能一覧
- **新規登録・ログイン**
    - 企業コード＋パスワードで新規登録
    - 二段階認証（個人メールアドレスとパスワード）
- **個人基本情報登録**
    - 個人プロフィール（名前、部署、年齢　等）
    - パスワード再設定
    - 通知設定
- **TOP（行きたい登録）ページ**
    - 参加希望日時、希望条件登録
    - 複数日付登録可能
- **開催決定一覧・参加履歴一覧確認**
    - 日時、場所、ステータス表示
    - タブ切替にて予定、過去一覧の確認可能
- **登録内容確認**
    - 登録した希望条件の変更、削除
- **お店提案**
    - 参加者中間地点の算出（OpenAI、GooglemapAPI）
    - お店三店舗選出（OpenAI、HotppepperAPI）

<br />

---
