# model-harness-eval: bedrock/us.meta.llama4-maverick-17b-instruct-v1:0 × pi × litellm
日期: 2026-07-14 17:56  harness=pi  provider=litellm  runs=5  tiers=smoke,complex,long,cli,real

| 任務 | tier | 通過率 | 靜默通過 | EMPTY | 平均秒數 |
|---|---|---|---|---|---|
| T1-程式理解 | smoke | 0/5 | 0 | 5 | 0.7 |
| T2-修bug | smoke | 0/5 | 0 | 5 | 0.7 |
| T3-寫檔案 | smoke | 0/5 | 0 | 5 | 0.7 |
| T4-bash查資料 | smoke | 0/5 | 0 | 5 | 0.7 |
| C1-跨檔bug | complex | 0/5 | 0 | 5 | 0.7 |
| C2-重構保綠 | complex | 0/5 | 0 | 5 | 0.7 |
| C3-誤導除錯 | complex | 0/5 | 0 | 5 | 0.7 |
| L1-spec建專案 | long | 0/5 | 0 | 5 | 0.7 |
| X1-陌生officecli | cli | 0/5 | 0 | 5 | 0.7 |
| X2-陌生opencli | cli | 0/5 | 0 | 5 | 0.7 |
| R1-agent-browser | real | 0/5 | 0 | 5 | 0.7 |

總計: **0/55**

## T1-程式理解

### run 1 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 2 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 3 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 4 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 5 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

## T2-修bug

### run 1 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 2 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 3 — EMPTY-無痕 (0.8s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 4 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 5 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

## T3-寫檔案

### run 1 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 2 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 3 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 4 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 5 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

## T4-bash查資料

### run 1 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 2 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 3 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 4 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 5 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

## C1-跨檔bug

### run 1 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 2 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 3 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 4 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 5 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

## C2-重構保綠

### run 1 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 2 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 3 — EMPTY-無痕 (0.8s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 4 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 5 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

## C3-誤導除錯

### run 1 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 2 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 3 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 4 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 5 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

## L1-spec建專案

### run 1 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 2 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 3 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 4 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 5 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

## X1-陌生officecli

### run 1 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 2 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 3 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 4 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 5 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

## X2-陌生opencli

### run 1 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 2 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 3 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 4 — EMPTY-無痕 (0.8s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 5 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

## R1-agent-browser

### run 1 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 2 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 3 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 4 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```

### run 5 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: del doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/us.meta.llama4-maverick-17b-instruct-v1:0" not found for provider "litellm". Using custom model id.
400: {"message":"litellm.BadRequestError: BedrockException - {\"message\":\"This model doesn't support tool use in streaming mode.\"}. Received Model Group=bedrock/us.meta.llama4-maverick-17b-instruct-v1:0\nAvailable Model Group Fallbacks=None","type":null,"param":null,"code":"400"}
```
