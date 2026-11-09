# 第3回 解答

## 演習

- 第1回（素のLLM）とエージェントの回答の違い：第1回では「基礎・応用・発展」であったが、今回は「基礎・実装・発展」となっており、しっかりエージェントが用語集を参照していることがわかる。

- `--trace` で見えたツール呼び出し（ツール名と引数）：
    --- trace ---
    [tool call]   search_glossary({'query': 'LoRA'})
    [tool call]   search_glossary({'query': 'QLoRA'})
    [tool return] search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…
    [tool return] search_glossary -> [{"term": "QLoRA", "lecture": 2, "definition": "ベースモデルの重みを4ビットなどに量子化してメモリを節約したうえで、LoRAで学習する手法。より大きなモデルを小さなGPUで扱える。本講座の第2…


- 1つの質問での LLM 呼び出し回数（`requests`）：
    [usage] RunUsage(cost=Decimal('0.0008113'), details={'text_prompt_tokens': 1196}, input_text_tokens=1196, input_tokens=1196, output_tokens=181, requests=2, tool_calls=2)


- 追加したツールと、docstring に書いた説明：
    モデルに見えているツール: 3 個

    [search_glossary]
      講座の用語集から用語を検索し、定義と、どの回で扱うかを返す。
  
      AIエンジニアリングの用語や、この講座（AIE2026）に固有の言葉について
      答える前に使うこと。query には調べたい用語を1つだけ入れる（例: "LoRA"）。
      引数: {"query": {"type": "string"}}

    [get_lecture_summary]
      指定した回（1始まりの整数）の講義の要点を返す。
  
      「第3回では何を学ぶ？」のように、回の内容や関係を聞かれたときに使う。
      引数: {"lecture": {"type": "integer"}}

    [make_quiz]
      指定した回の用語集から確認問題を1問作り、答えとともに返す。
  
      学習者から確認問題やクイズを求められたとき、指定された回の用語を復習するために使う。
      lecture には対象の回を1始まりの整数で指定する。
      引数: {"lecture": {"type": "integer"}}


## 宿題

- 取り組んだレベル：基礎 / 実装 / 発展
- やったこと：
- 結果：
- 気づき・疑問：
