#!/usr/bin/env python
# -*- coding: utf-8 -*-

import openai
import json
import sys
import os
import re
from dotenv import load_dotenv

# .env ファイルを読み込む（デフォルトではカレントディレクトリの .env ファイルが対象）
load_dotenv()

# 環境変数から API キーを取得
openai.api_key = os.getenv("OPENAI_API_KEY")


openai.api_key = os.getenv("OPENAI_API_KEY") 

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_discussion.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    with open(input_file, "r", encoding="utf-8") as f:
        conversation = f.read()

    prompt = f"""
以下は発言者ラベル付きの議論スクリプトです（各行は "Speaker: 発言内容" の形式です）。
この議論から以下の情報を抽出してください。

1. **質問・指摘**: 誰が誰に対して質問や指摘を行ったか（疑問文や「～ですか」等の形を含む場合）。
2. **賛同**: 誰が誰に賛同したか（例：「確かに」「なるほど」などの表現を含む場合）。
3. **否定的な質問**: 誰が誰に否定的な質問を行ったか（例：「いや、」で始まる発言の場合）。

各ケースについて、発言回数をカウントしてください。

出力は以下の JSON 形式に従ってください。

{{
  "questions": {{
    "<発言者>": {{
      "<対象の発言者>": 回数,
      ...
    }},
    ...
  }},
  "agreements": {{
    "<発言者>": {{
      "<対象の発言者>": 回数,
      ...
    }},
    ...
  }},
  "negative_questions": {{
    "<発言者>": {{
      "<対象の発言者>": 回数,
      ...
    }},
    ...
  }}
}}

以下、議論スクリプトです。

{conversation}
"""
    #GPT4oで分析
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "あなたは議論分析に優れたアシスタントです。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0  
        )
    except Exception as e:
        print("OpenAI API呼び出しエラー:", e)
        sys.exit(1)

    result_text = response.choices[0].message["content"]
    
    #正規表現でJSON部分を抽出
    pattern = r"```(?:json)?\s*([\s\S]*?)\s*```"
    match = re.search(pattern, result_text)
    if match:
        json_code = match.group(1)
    else:
        json_code = result_text
    result_text = json_code
    
    lines = result_text.strip().splitlines()
    
    # 最初の行が ``` または ```json なら削除
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    
    result_text = "\n".join(lines)
    
    print("=== 抽出結果 ===")
    print(result_text)

    # 結果を JSON としてパースできればファイルに保存
    try:
        result_json = json.loads(result_text)
        with open("analysis_result.json", "w", encoding="utf-8") as outfile:
            json.dump(result_json, outfile, ensure_ascii=False, indent=2)
        print("\nanalysis_result.json として保存しました。")
    except Exception as e:
        print("JSONパースエラー:", e)
        # パースに失敗した場合は、結果テキストをそのまま保存
        with open("analysis_result.txt", "w", encoding="utf-8") as outfile:
            outfile.write(result_text)
        print("結果を analysis_result.txt として保存しました。")

if __name__ == "__main__":
    main()
