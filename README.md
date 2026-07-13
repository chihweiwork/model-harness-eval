# model-harness-eval — 模型 × harness 能力評估框架

（原名 pi-bench；目前的 harness 以 pi coding agent 為主，架構上可換成其他 agent harness）

用可重複、可驗證的方式回答一個問題：**「某個地端模型（透過 Ollama）配上 pi coding agent，到底能撐到哪一級任務？」**

不聽模型自己說做完了——每個任務都由程式實際檢查結果（跑 pytest、執行產出的程式、比對檔案），並且每題跑多輪來量化穩定性。

## 檔案結構

```
model-harness-eval/
├── run_bench.py        # 主評測程式
├── selftest.py         # 評測本身的可信度自測
├── fixtures/           # 每個複雜任務的起始專案
│   ├── C1-crossfile-bug/
│   ├── C2-refactor-green/
│   ├── C3-misleading-trace/
│   ├── L1-todo-spec/
│   ├── X1-officecli/
│   └── X2-opencli/
├── results/            # 每次評測的 Markdown 報告
└── README.md
```

## 執行方式

```bash
# 完整評測：11 個任務 × 每題 5 輪
python3 run_bench.py gemma4:12b

# 多模型比較
python3 run_bench.py gemma4:12b qwen3.5:9b

# 只跑特定 tier、控制輪數
python3 run_bench.py gemma4:12b --runs 1 --tier complex,cli
```

前置需求：`pi` 已安裝且 `~/.pi/agent/models.json` 已註冊 Ollama 模型、`pytest` 可用、（R tier）`agent-browser` 已安裝。首次使用需先產生 X1 素材：`python3 fixtures/X1-officecli/.build.py`。

## 任務清單（5 個 tier、11 題）

### Tier: smoke — 基準線（4 題，timeout 300s）

確認模型具備最基本的 agent 能力，同時做為跨模型比較的底線。

| 題目 | 工具限制 | 內容 | 驗證 |
|---|---|---|---|
| T1-程式理解 | read,grep,find,ls（唯讀） | 解釋 inventory.py 的兩個函式 | 回答提到 take 和 restock |
| T2-修bug | 預設 4 工具 | calc.py 的 `a - b` 應為 `a + b` | 實際執行 calc.py 看 "all tests passed" |
| T3-寫檔案 | 預設 4 工具 | 從零寫 FizzBuzz 1-15 | 執行產出檔，逐行比對第 3/15 行 |
| T4-bash查資料 | read,bash | 數 CSV 資料列數 | 回答含正確數字 42 |

### Tier: complex — 多檔案 coding（3 題，timeout 600s）

**C1 跨檔 bug 追蹤**（`fixtures/C1-crossfile-bug/`）
三層架構 `store.py`（庫存）→ `orders.py`（下單）→ `report.py`（報表）。bug 埋在最底層 store.py 的 `reserve()`：`>` 應為 `>=`，導致「剛好把庫存買完」被拒絕。但 pytest 的失敗斷言出現在最上層的報表測試。
- **測什麼**：模型會不會被失敗訊息的位置誤導，能否沿呼叫鏈往下追根因。
- **驗證**：tempdir 內跑 `python3 -m pytest -q`，exit 0 才 PASS。
- **防作弊**：test_report.py 受 SHA-256 保護（見下方「保護檔案」）。

**C2 重構保綠**（`fixtures/C2-refactor-green/`）
a.py 與 b.py 有一段完全相同的名字正規化邏輯（`" ".join(name.strip().split()).title()`），要求抽成 utils.py 供兩邊共用。
- **測什麼**：「改結構不改行為」——同時動三個檔案且不能弄壞任何測試。
- **驗證**：三重檢查——pytest 通過 **且** utils.py 存在 **且** a.py/b.py 內容都引用 utils。缺一即 FAIL（防止模型假重構：測試過了但根本沒抽共用邏輯）。

**C3 誤導性除錯**（`fixtures/C3-misleading-trace/`）
`python3 main.py` 噴 TypeError，trace 指向 server.py 的 `self.port + 1`；真因在 config.py——settings.json 的 port 是字串 `"8080"`，config 層沒轉 int。
- **測什麼**：治本 vs 治標的判斷力。
- **驗證**：兩段式——(1) main.py 跑通且輸出含 "admin 8081"；(2) **根因檢查**：`load_config()["port"]` 必須是 int。若模型只在 server.py 貼 `int()` 繃帶，第 (1) 段會過但第 (2) 段 FAIL。修 config.py 或 settings.json 都算根因修法。

### Tier: long — 長程多步驟（1 題，timeout 900s）

**L1 從 spec 建專案**（`fixtures/L1-todo-spec/`）
給 SPEC.md（todo CLI 完整規格：add/list/done 三個子命令、todos.json 持久化、精確輸出格式、id 不回收、done 冪等、未知 id 要 exit 1）+ 現成的 9 個 pytest 案例（用 subprocess 黑箱測試），要求從零寫出 todo.py。
- **測什麼**：持續力。模型需要 讀規格 → 實作 → 跑測試 → 讀失敗訊息 → 修 → 再跑 的多輪迭代，小模型常中途「宣布完成」就停手。
- **驗證**：todo.py 存在且 `pytest test_todo.py -q` 全綠。

### Tier: cli — 陌生 CLI 操作（2 題，timeout 600s，工具限 read,bash）

模擬使用者的實際目標（OfficeCLI、opencli/agent-browser）：模型面對一個**訓練資料裡不存在**的工具，能否從 `--help` 自學用法並完成任務。

**X1 陌生 officecli**（`fixtures/X1-officecli/`）
目錄裡有 `report.docx` 與 `./bin/officecli`（自製 Python CLI，argparse 完整 help，子命令 `info`/`convert`）。report.docx 是自訂 OFFX 容器格式：magic header + metadata + **base64 封裝的內文**——所以模型無法直接 `cat` 數字數，唯一路徑是學會 `officecli convert report.docx --format txt -o report.txt`。
- **驗證**：.txt 輸出檔存在 + 回答含正確字數 45。
- 素材由 `.build.py` 產生（runner 複製 fixture 時排除點開頭檔案，模型看不到產生邏輯與原文）。

**X2 陌生 opencli**（`fixtures/X2-opencli/`）
`./bin/opencli` 是迷你瀏覽器 CLI（`open <url>` / `links` / `text <selector>` / `dump`），頁面存在 fixture 的 pages/ 裡（假網站 shop.local，三頁）。任務：從首頁出發找 Aurora Lamp 的價格。**故意設計成兩跳**：首頁沒有價格，必須 open 首頁 → 從連結發現 /products → open 商品頁 → 用 selector 取價。工具用 `.opencli_session.json` 記住當前頁面，測模型的多步驟狀態管理。
- **驗證**：回答含正確價格 149.50。

### Tier: real — 真實工具整合（1 題，timeout 600s）

**R1 agent-browser**：用真實安裝的 agent-browser 開 https://example.com 回報標題。X2 是它的離線替身；R1 驗證真實環境（真瀏覽器、真網路、真工具的複雜輸出）。
- **驗證**：回答含 "Example Domain"。

## Runner 機制細節（run_bench.py）

**每輪的執行流程**：
1. `prepare_dir()` 建全新 tempdir：fixture 整包複製（排除 `.` 開頭檔案與 `__pycache__`），`bin/` 下的檔案自動 chmod +x；無 fixture 的任務跑 inline setup 函式。
2. 記下所有「保護檔案」的 SHA-256。
3. 以 tempdir 為 cwd 執行 `pi --provider ollama --model <M> [--tools ...] -p "<prompt>"`，環境帶 `PI_OFFLINE=1` 與 `PI_SKIP_VERSION_CHECK=1`（避免啟動時的網路請求干擾計時）。
4. 依序判定，取第一個命中的結果：
   - **逾時**：超過任務 timeout，pi 被強制終止。
   - **EMPTY**：pi 正常退出但 stdout 為空——模型從頭到尾沒產出給使用者的文字。注意：目前只讀 stdout，模型中間做了什麼、pi 有沒有在 stderr 報錯都看不到（已知盲點，見下）。
   - **違規修改保護檔案**：任何保護檔案的 SHA-256 變了或檔案消失 → 直接 FAIL。防止模型「把測試改到會過」這種作弊路徑。
   - **verify 函式**：該任務專屬的程式化驗證（跑 pytest、執行產出、比對輸出）。
5. tempdir 銷毀，輪與輪之間零污染。

**統計與報告**：
- 終端即時印每輪結果（✅ / ❌ / ⬜EMPTY + 秒數 + 細節）。
- 每模型彙總表：任務 × (通過數/輪數, EMPTY 數, 平均秒數) + 總通過率。
- `results/<model>_<timestamp>.md`：彙總表 + **每一輪的完整模型輸出**，供人工檢查回答品質與失敗模式。

**多輪的意義**：地端小模型有偶發性失敗（同一任務有時過有時空轉）。單輪只能回答「會不會」，5 輪能回答「多可靠」——`3/5` 和 `0/5` 是完全不同的診斷：前者是不穩，後者是系統性問題。

## selftest.py — 評測自身的可信度

評測結果要可信，驗證邏輯本身得先被驗證。selftest 對 6 個複雜任務各做兩個方向的檢查：

1. **原始碼直接跑 verify → 必須 FAIL**：確認 bug 真的存在、驗證不會放水（假陰性檢查的反面）。
2. **套用人工正解再跑 verify → 必須 PASS**：確認驗證不會誤殺正確解法，同時實測 mock CLI 真的能用（X1 正解就是真的去執行 officecli convert）。

任何一項不符 exit 1，擋住後續評測，避免拿壞掉的尺去量模型。

## 已知限制與待辦

- **stderr 盲點**：runner 只讀 stdout。EMPTY 的真正死因（pi 的錯誤訊息、tool call 解析失敗等）可能在 stderr 但目前被丟棄。診斷計畫：補記 stderr/exit code + 用 `pi --mode json` 抓事件流。
- **C1 系統性 EMPTY**：gemma4:12b 在 C1 連續 5/5 空輸出（17-24 秒即結束，未達 token 上限），原因調查中；嫌疑包括 `~/.pi/agent/models.json` 中重複的 gemma4:12b 條目（pi /model 選單自動寫入的 `reasoning: true` 版本）。
- **X1 字數驗證**只認阿拉伯數字 45，模型答 "forty-five" 會被誤判 FAIL（目前接受此限制）。
- **EMPTY ≠ 一定沒做事**：判定僅基於最終 stdout，模型可能有動工但最後一輪沒輸出文字。
