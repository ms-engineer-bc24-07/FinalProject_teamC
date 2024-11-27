# Connetto

## 開発環境ガイド

### バックエンドの設定 (Black, isort, Flake8)

- **フォーマッター**:
    - `Black`: コードフォーマットを自動化し、PEP 8 に準拠したスタイルを維持します。
    - `isort`: インポートの順序を整理し、コードの可読性を向上させます。
- **リンター**:
    - `Flake8`: コードスタイルのチェックや潜在的なバグを検出します。
- **コード規約**: PEP 8 に準拠
- **設定ファイル**:
    - `pyproject.toml`: Black と isort の設定
    - `.flake8`: Flake8 の設定

---

### フロントエンドの設定 (Prettier, ESLint)

- **フォーマッター**:
    - `Prettier`: HTML/CSS/JavaScript/TypeScript などのコード整形を自動化します。
- **リンター**:
    - `ESLint`: JavaScript や TypeScript の静的解析を行い、コード品質を向上させます。
- **コード規約**: ESLint のルールを使用し、Prettier と統一
- **設定ファイル**:
    - `.prettierrc`: Prettier の設定
    - `.eslintrc.json`: ESLint の設定

---

### Git Hooks の設定 (Pre-commit Hooks)

このプロジェクトでは [pre-commit](https://pre-commit.com/) を使用して、フォーマットやチェックを自動化しています。Gitにコミットする前に、以下のツールが実行されます:

- Black
- isort
- Flake8

`pre-commit` をインストールし、設定を有効化してください。

```bash
pip install pre-commit
pre-commit install

```

Pre-commitの設定は `.pre-commit-config.yaml` に記載されています。

---

### 参考リンク

- [Black Documentation](https://black.readthedocs.io/)
- [isort Documentation](https://pycqa.github.io/isort/)
- [Flake8 Documentation](https://flake8.pycqa.org/)
- [Prettier Documentation](https://prettier.io/)
- [ESLint Documentation](https://eslint.org/)

---
