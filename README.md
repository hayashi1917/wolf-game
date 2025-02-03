# wolf-game  
**人狼ゲーム支援システム**

議論スクリプトを解析して各発言者間の相互作用（質問・指摘、賛同、否定的な質問）を JSON 形式で出力し、さらにその情報からグラフを生成して可視化します。

---

## 環境構築の手順

### 1. 前提条件

- **Python 3.8 以上** をインストールしてください。  
- OpenAI の API キーを取得しておいてください。  
  ※ [OpenAI API キーの取得方法](https://platform.openai.com/account/api-keys)

### 2. プロジェクトディレクトリの作成

任意の場所にプロジェクト用のディレクトリ（例: `wolf-game`）を作成し、そこに移動します。

```bash
mkdir wolf-game
cd wolf-game
```

### 3. 仮想環境の作成と有効化

Python の仮想環境を作成し、有効化します。

- **Linux/macOS:**

  ```bash
  python -m venv venv
  source venv/bin/activate
  ```

- **Windows:**

  ```cmd
  python -m venv venv
  venv\Scripts\activate
  ```

### 4. 必要なパッケージのインストール

以下のコマンドで必要なライブラリをインストールします。

```bash
 pip install -r requirements.txt
```

### 5. プロジェクトファイルの配置

以下のファイルをプロジェクトディレクトリ内に用意してください。

- **.env**  
  OpenAI API キーを管理するためのファイル。例として、以下のように記述します。

  ```dotenv
  OPENAI_API_KEY=your-openai-api-key
  ```

  ※ ファイル名は `.env` とし、`analyze_discussion.py` 内で `python-dotenv` によって読み込むようにしてください。

- **discussion.txt**  
  議論スクリプトを保存するテキストファイル。  
  例:

  ```
  A: 最近の戦略についてどう思う？
  B: 確かに、その点は重要だね。
  C: いや、私は違う意見だ。
  A: Bさん、具体的にどういうところが？
  B: なるほど、説明すると…
  ```

---

## 使い方

### 1. 議論スクリプトの解析

1. **議論スクリプト（例: `discussion.txt`）** を用意します。  
   発言は各行が `Speaker: 発言内容` の形式になっている必要があります。

2. ターミナル上で以下のコマンドを実行して解析を行います。

   ```bash
   python analyze_discussion.py discussion.txt
   ```

3. 実行後、解析結果が標準出力に表示されるほか、JSON 形式の結果が `analysis_result.json` として保存されます。  
   ※ もし OpenAI API のレスポンスに Markdown のコードブロックが含まれている場合は、コード内でその部分を取り除く後処理が行われます。

### 2. グラフの生成と可視化

1. 解析結果として生成された JSON ファイル（例: `analysis_result.json`）をもとに、以下のコマンドを実行します。

   ```bash
   python visualize_graph.py analysis_result.json
   ```

2. 実行すると、NetworkX と matplotlib により、発言者間の相互作用（質問・指摘、賛同、否定的な質問）が色分けされたグラフが表示されます。  
   - 例:  
     - **赤**: 質問・指摘  
     - **緑**: 賛同  
     - **青**: 否定的な質問

---

## 注意事項

- **API キーの管理:**  
  .env ファイルに API キーを記述する際、セキュリティ上の理由から公開リポジトリなどに含めないように注意してください。

- **OpenAI API の利用:**  
  OpenAI API を使用するため、利用回数や料金に注意してください。また、モデル名の指定（例: `"gpt-3.5-turbo"` や `"gpt-4"`）については、アカウントの利用権限に応じて変更してください。

- **依存パッケージのバージョン:**  
  環境構築時に NumPy や matplotlib のバージョンの不整合に注意してください。エラーが発生した場合、必要に応じてパッケージのバージョンを調整してください（例: `pip install numpy==1.24.3` など）。

---

以上が、**wolf-game** プロジェクトの簡単な環境構築方法と使い方の手順です。これをベースに、実際の人狼ゲームの議論内容を解析・可視化するシステムの開発を進めてください。
