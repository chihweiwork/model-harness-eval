# model-harness-eval: bedrock/nvidia.nemotron-super-3-120b × pi × litellm
日期: 2026-07-14 16:35  harness=pi  provider=litellm  runs=1  tiers=smoke,complex,long,cli,real

| 任務 | tier | 通過率 | 靜默通過 | EMPTY | 平均秒數 |
|---|---|---|---|---|---|
| T1-程式理解 | smoke | 0/1 | 0 | 1 | 1.2 |
| T2-修bug | smoke | 0/1 | 0 | 1 | 1.0 |
| T3-寫檔案 | smoke | 0/1 | 0 | 1 | 0.7 |
| T4-bash查資料 | smoke | 0/1 | 0 | 1 | 0.8 |
| C1-跨檔bug | complex | 0/1 | 0 | 1 | 0.8 |
| C2-重構保綠 | complex | 0/1 | 0 | 1 | 0.8 |
| C3-誤導除錯 | complex | 0/1 | 0 | 1 | 0.9 |
| L1-spec建專案 | long | 0/1 | 0 | 1 | 0.8 |
| X1-陌生officecli | cli | 0/1 | 0 | 1 | 0.8 |
| X2-陌生opencli | cli | 0/1 | 0 | 1 | 0.8 |
| R1-agent-browser | real | 0/1 | 0 | 1 | 0.8 |

總計: **0/11**

## T1-程式理解

### run 1 — EMPTY-無痕 (1.2s) — 無輸出且完全沒動作; exit=1, stderr尾: 401): {"message":"Incorrect API key provided: sk-1234. You can find your API key at https://platform.openai.com/account/api-keys.","type":"invalid_request_error","code":"invalid_api_key","param":null}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/nvidia.nemotron-super-3-120b" not found for provider "openai". Using custom model id.
OpenAI API error (401): {"message":"Incorrect API key provided: sk-1234. You can find your API key at https://platform.openai.com/account/api-keys.","type":"invalid_request_error","code":"invalid_api_key","param":null}
```

## T2-修bug

### run 1 — EMPTY-無痕 (1.0s) — 無輸出且完全沒動作; exit=1, stderr尾: 401): {"message":"Incorrect API key provided: sk-1234. You can find your API key at https://platform.openai.com/account/api-keys.","type":"invalid_request_error","code":"invalid_api_key","param":null}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/nvidia.nemotron-super-3-120b" not found for provider "openai". Using custom model id.
OpenAI API error (401): {"message":"Incorrect API key provided: sk-1234. You can find your API key at https://platform.openai.com/account/api-keys.","type":"invalid_request_error","code":"invalid_api_key","param":null}
```

## T3-寫檔案

### run 1 — EMPTY-無痕 (0.7s) — 無輸出且完全沒動作; exit=1, stderr尾: 401): {"message":"Incorrect API key provided: sk-1234. You can find your API key at https://platform.openai.com/account/api-keys.","type":"invalid_request_error","code":"invalid_api_key","param":null}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/nvidia.nemotron-super-3-120b" not found for provider "openai". Using custom model id.
OpenAI API error (401): {"message":"Incorrect API key provided: sk-1234. You can find your API key at https://platform.openai.com/account/api-keys.","type":"invalid_request_error","code":"invalid_api_key","param":null}
```

## T4-bash查資料

### run 1 — EMPTY-無痕 (0.8s) — 無輸出且完全沒動作; exit=1, stderr尾: 401): {"message":"Incorrect API key provided: sk-1234. You can find your API key at https://platform.openai.com/account/api-keys.","type":"invalid_request_error","code":"invalid_api_key","param":null}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/nvidia.nemotron-super-3-120b" not found for provider "openai". Using custom model id.
OpenAI API error (401): {"message":"Incorrect API key provided: sk-1234. You can find your API key at https://platform.openai.com/account/api-keys.","type":"invalid_request_error","code":"invalid_api_key","param":null}
```

## C1-跨檔bug

### run 1 — EMPTY-無痕 (0.8s) — 無輸出且完全沒動作; exit=1, stderr尾: 401): {"message":"Incorrect API key provided: sk-1234. You can find your API key at https://platform.openai.com/account/api-keys.","type":"invalid_request_error","code":"invalid_api_key","param":null}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/nvidia.nemotron-super-3-120b" not found for provider "openai". Using custom model id.
OpenAI API error (401): {"message":"Incorrect API key provided: sk-1234. You can find your API key at https://platform.openai.com/account/api-keys.","type":"invalid_request_error","code":"invalid_api_key","param":null}
```

## C2-重構保綠

### run 1 — EMPTY-無痕 (0.8s) — 無輸出且完全沒動作; exit=1, stderr尾: 401): {"message":"Incorrect API key provided: sk-1234. You can find your API key at https://platform.openai.com/account/api-keys.","type":"invalid_request_error","code":"invalid_api_key","param":null}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/nvidia.nemotron-super-3-120b" not found for provider "openai". Using custom model id.
OpenAI API error (401): {"message":"Incorrect API key provided: sk-1234. You can find your API key at https://platform.openai.com/account/api-keys.","type":"invalid_request_error","code":"invalid_api_key","param":null}
```

## C3-誤導除錯

### run 1 — EMPTY-無痕 (0.9s) — 無輸出且完全沒動作; exit=1, stderr尾: 401): {"message":"Incorrect API key provided: sk-1234. You can find your API key at https://platform.openai.com/account/api-keys.","type":"invalid_request_error","code":"invalid_api_key","param":null}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/nvidia.nemotron-super-3-120b" not found for provider "openai". Using custom model id.
OpenAI API error (401): {"message":"Incorrect API key provided: sk-1234. You can find your API key at https://platform.openai.com/account/api-keys.","type":"invalid_request_error","code":"invalid_api_key","param":null}
```

## L1-spec建專案

### run 1 — EMPTY-無痕 (0.8s) — 無輸出且完全沒動作; exit=1, stderr尾: 401): {"message":"Incorrect API key provided: sk-1234. You can find your API key at https://platform.openai.com/account/api-keys.","type":"invalid_request_error","code":"invalid_api_key","param":null}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/nvidia.nemotron-super-3-120b" not found for provider "openai". Using custom model id.
OpenAI API error (401): {"message":"Incorrect API key provided: sk-1234. You can find your API key at https://platform.openai.com/account/api-keys.","type":"invalid_request_error","code":"invalid_api_key","param":null}
```

## X1-陌生officecli

### run 1 — EMPTY-無痕 (0.8s) — 無輸出且完全沒動作; exit=1, stderr尾: 401): {"message":"Incorrect API key provided: sk-1234. You can find your API key at https://platform.openai.com/account/api-keys.","type":"invalid_request_error","code":"invalid_api_key","param":null}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/nvidia.nemotron-super-3-120b" not found for provider "openai". Using custom model id.
OpenAI API error (401): {"message":"Incorrect API key provided: sk-1234. You can find your API key at https://platform.openai.com/account/api-keys.","type":"invalid_request_error","code":"invalid_api_key","param":null}
```

## X2-陌生opencli

### run 1 — EMPTY-無痕 (0.8s) — 無輸出且完全沒動作; exit=1, stderr尾: 401): {"message":"Incorrect API key provided: sk-1234. You can find your API key at https://platform.openai.com/account/api-keys.","type":"invalid_request_error","code":"invalid_api_key","param":null}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/nvidia.nemotron-super-3-120b" not found for provider "openai". Using custom model id.
OpenAI API error (401): {"message":"Incorrect API key provided: sk-1234. You can find your API key at https://platform.openai.com/account/api-keys.","type":"invalid_request_error","code":"invalid_api_key","param":null}
```

## R1-agent-browser

### run 1 — EMPTY-無痕 (0.8s) — 無輸出且完全沒動作; exit=1, stderr尾: 401): {"message":"Incorrect API key provided: sk-1234. You can find your API key at https://platform.openai.com/account/api-keys.","type":"invalid_request_error","code":"invalid_api_key","param":null}

```
(無輸出)
```

stderr:
```
Warning: Model "bedrock/nvidia.nemotron-super-3-120b" not found for provider "openai". Using custom model id.
OpenAI API error (401): {"message":"Incorrect API key provided: sk-1234. You can find your API key at https://platform.openai.com/account/api-keys.","type":"invalid_request_error","code":"invalid_api_key","param":null}
```
