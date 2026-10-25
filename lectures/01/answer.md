# 第1回 解答

## 演習

- 講座に固有の質問（宿題の3レベル）へのモデルの回答（要約でよい）：
    ```
    [model] gemini-3.5-flash-lite

    「3レベル」は基礎・応用・発展の3段階に分かれた宿題の難易度区分を指し、提出ルールが「選択制」か「全問必修」か事前に確認することが重要です。
    
    レベル1（基礎）: 授業の理解確認が目的。全員必修となる穴埋めや基本コードの実行が中心。
    レベル2（応用）: 知識の実践が目的。条件変更やエラー修正、簡単な実装に挑戦。
    レベル3（発展）: 実践的・高度な挑戦が目的。効率化や実務に近い発展課題を扱う。
    
    注意点: 1つ選んで提出する形式か、全レベルを順に解く形式かは講座の指定によるため、不明な場合はSlackやDiscord等で運営・講師へ確認を推奨。
    ```
- 用語集の正しい意味と比べて気づいたこと：
    - 正しい意味
    ```
    AIE2026の宿題の構成。「基礎（講義内容の確認）」「実装（自分でコードを書く）」「発展（調査や試行）」の3段階があり、どれか1つに取り組めばその回の宿題は完了。原則として採点はしない。
    ```
    - 気づき：LLMの回答は意訳されて文章が生成されている。かなり文章量が定義より多くなっている。
- 表示できたトークン数（入力 / 出力）：
    ```
    [API応答時間] 2.546秒
    [入力トークン数] 22
    [出力トークン数] 469
    [合計トークン数] 491
    ```

## 宿題

- 取り組んだレベル：発展
        - 「応答時間とトークン数を計測し、複数モデルや質問で比較する。無料枠レート制限と関係も考察する」

- やったこと：
    - モデルA（gemini-3.5-flash-lite）とモデルB（gemini-3.8-flash）でそれぞれ下記を実行する
        - 単純な質問：　「What is LoRA in machine learning?」
        - 複雑な質問：  「Explain the differences between LoRA and full fine-tuning in terms of computational cost, memory usage, and performance. Provide a practical use case.」
    - 応答時間のばらつきを評価するため、各モデルと質問の組み合わせについて最大3回の測定を実施した。繰り返し測定の回数は本実験で独自に設定したものであり、宿題の要件として指定されたものではない。

- 結果：

| Model | Question | Repetition | Response Time (s) | Input Tokens | Output Tokens | Total Tokens |
|---|---|---:|---:|---:|---:|---:|
| gemini-3.5-flash-lite | Q1: Simple | 1 | 3.288 | 9 | 822 | 831 |
| gemini-3.5-flash-lite | Q1: Simple | 2 | 9.676 | 9 | 883 | 892 |
| gemini-3.5-flash-lite | Q1: Simple | 3 | 3.044 | 9 | 746 | 755 |
| gemini-3.5-flash-lite | Q2: Complex | 1 | 4.340 | 30 | 1111 | 1141 |
| gemini-3.5-flash-lite | Q2: Complex | 2 | 4.439 | 30 | 1113 | 1143 |
| gemini-3.5-flash-lite | Q2: Complex | 3 | 4.480 | 30 | 1143 | 1173 |
| gemini-3.8-flash | Q1: Simple | 1 | 172.424 | 9 | 1027 | 2008 |
| gemini-3.8-flash | Q1: Simple | 2 | 242.872 | 9 | 920 | 1904 |
| gemini-3.8-flash | Q1: Simple | 3 | 189.394 | 9 | 919 | 1873 |
| gemini-3.8-flash | Q2: Complex | 1 | 204.453 | 30 | 1416 | 2519 |
| gemini-3.8-flash | Q2: Complex | 2 | — | — | — | — |
| gemini-3.8-flash | Q2: Complex | 3 | — | — | — | — |    


- 気づき・疑問：
Model B 503 6回
