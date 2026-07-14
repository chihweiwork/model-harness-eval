# model-harness-eval: bedrock/us.meta.llama4-maverick-17b-instruct-v1:0 × codex × litellm
日期: 2026-07-14 18:48  harness=codex  provider=litellm  runs=5  tiers=smoke,complex,long,cli,real

> ⚠ 此 harness 不支援 per-run 工具限制, 各任務的 tools 欄位未生效。

| 任務 | tier | 通過率 | 靜默通過 | EMPTY | 平均秒數 |
|---|---|---|---|---|---|
| T1-程式理解 | smoke | 0/5 | 0 | 5 | 2.3 |
| T2-修bug | smoke | 0/5 | 0 | 5 | 3.6 |
| T3-寫檔案 | smoke | 0/5 | 0 | 5 | 2.7 |
| T4-bash查資料 | smoke | 0/5 | 0 | 5 | 2.6 |
| C1-跨檔bug | complex | 0/5 | 0 | 5 | 3.0 |
| C2-重構保綠 | complex | 0/5 | 0 | 5 | 3.0 |
| C3-誤導除錯 | complex | 0/5 | 0 | 5 | 2.8 |
| L1-spec建專案 | long | 0/5 | 0 | 5 | 2.6 |
| X1-陌生officecli | cli | 0/5 | 0 | 5 | 3.0 |
| X2-陌生opencli | cli | 0/5 | 0 | 5 | 4.3 |
| R1-agent-browser | real | 0/5 | 0 | 5 | 2.6 |

總計: **0/55**

## T1-程式理解

### run 1 — EMPTY-無痕 (1.6s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 2 — EMPTY-無痕 (2.2s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 3 — EMPTY-無痕 (1.8s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 4 — EMPTY-無痕 (2.1s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 5 — EMPTY-無痕 (3.7s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

## T2-修bug

### run 1 — EMPTY-無痕 (5.0s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 2 — EMPTY-無痕 (2.2s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 3 — EMPTY-無痕 (2.4s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 4 — EMPTY-無痕 (1.7s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 5 — EMPTY-無痕 (6.5s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

## T3-寫檔案

### run 1 — EMPTY-無痕 (2.6s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 2 — EMPTY-無痕 (2.2s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 3 — EMPTY-無痕 (2.9s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 4 — EMPTY-無痕 (3.6s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 5 — EMPTY-無痕 (2.1s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

## T4-bash查資料

### run 1 — EMPTY-無痕 (1.7s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 2 — EMPTY-無痕 (2.3s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 3 — EMPTY-無痕 (3.7s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 4 — EMPTY-無痕 (3.4s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 5 — EMPTY-無痕 (1.7s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

## C1-跨檔bug

### run 1 — EMPTY-無痕 (4.0s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 2 — EMPTY-無痕 (1.3s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 3 — EMPTY-無痕 (2.9s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 4 — EMPTY-無痕 (4.3s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 5 — EMPTY-無痕 (2.4s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

## C2-重構保綠

### run 1 — EMPTY-無痕 (3.1s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 2 — EMPTY-無痕 (2.0s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 3 — EMPTY-無痕 (1.8s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 4 — EMPTY-無痕 (1.7s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 5 — EMPTY-無痕 (6.3s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

## C3-誤導除錯

### run 1 — EMPTY-無痕 (3.1s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 2 — EMPTY-無痕 (2.1s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 3 — EMPTY-無痕 (1.9s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 4 — EMPTY-無痕 (1.7s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 5 — EMPTY-無痕 (5.4s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

## L1-spec建專案

### run 1 — EMPTY-無痕 (3.1s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 2 — EMPTY-無痕 (2.4s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 3 — EMPTY-無痕 (3.0s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 4 — EMPTY-無痕 (2.1s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 5 — EMPTY-無痕 (2.4s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

## X1-陌生officecli

### run 1 — EMPTY-無痕 (1.8s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 2 — EMPTY-無痕 (3.1s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 3 — EMPTY-無痕 (4.8s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 4 — EMPTY-無痕 (3.4s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 5 — EMPTY-無痕 (2.0s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

## X2-陌生opencli

### run 1 — EMPTY-無痕 (5.7s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 2 — EMPTY-無痕 (6.3s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 3 — EMPTY-無痕 (1.7s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 4 — EMPTY-無痕 (3.8s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 5 — EMPTY-無痕 (3.9s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

## R1-agent-browser

### run 1 — EMPTY-無痕 (1.8s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 2 — EMPTY-無痕 (3.4s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 3 — EMPTY-無痕 (3.8s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 4 — EMPTY-無痕 (1.9s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```

### run 5 — EMPTY-無痕 (2.3s) — 無輸出且完全沒動作; exit=1, stderr尾: el doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}

```
(無輸出)
```

stderr:
```
 model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
ERROR: {"error":{"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}}
```
