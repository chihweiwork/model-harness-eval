# model-harness-eval: bedrock/nvidia.nemotron-super-3-120b × copilot × litellm
日期: 2026-07-14 16:29  harness=copilot  provider=litellm  runs=1  tiers=smoke,complex,long,cli,real

> ⚠ 此 harness 不支援 per-run 工具限制, 各任務的 tools 欄位未生效。

| 任務 | tier | 通過率 | 靜默通過 | EMPTY | 平均秒數 |
|---|---|---|---|---|---|
| T1-程式理解 | smoke | 1/1 | 0 | 0 | 3.4 |
| T2-修bug | smoke | 1/1 | 0 | 0 | 8.6 |
| T3-寫檔案 | smoke | 1/1 | 0 | 0 | 7.3 |
| T4-bash查資料 | smoke | 0/1 | 0 | 0 | 8.8 |
| C1-跨檔bug | complex | 1/1 | 0 | 0 | 14.4 |
| C2-重構保綠 | complex | 1/1 | 0 | 0 | 29.1 |
| C3-誤導除錯 | complex | 1/1 | 0 | 0 | 29.5 |
| L1-spec建專案 | long | 1/1 | 0 | 0 | 28.6 |
| X1-陌生officecli | cli | 1/1 | 0 | 0 | 12.1 |
| X2-陌生opencli | cli | 1/1 | 0 | 0 | 24.0 |
| R1-agent-browser | real | 1/1 | 0 | 0 | 19.5 |

總計: **10/11**

## T1-程式理解

### run 1 — PASS (3.4s) — 有提到 take 和 restock

```
I'll read the inventory.py file and explain what each function does.


The inventory.py file contains two functions:

1. `take(item, n)`: Attempts to remove `n` units of `item` from stock. Returns True if successful (sufficient stock available), False otherwise.

2. `restock(item, n)`: Adds `n` units of `item` to stock. Increases the stock count for the specified item by `n` units.

The script starts with a STOCK dictionary initialized with {"apple": 10, "banana": 5}.
```

## T2-修bug

### run 1 — PASS (8.6s) — calc.py → all tests passed

```
I'll read calc.py to find and fix the bug, then verify the fix works.


I found the bug in the `add` function on line 2 - it's performing subtraction instead of addition. Let me fix it:


Now let's run python3 calc.py to verify the fix works:


The bug has been fixed and the tests now pass. The issue was in the `add` function where it was subtracting instead of adding the two numbers. I changed `return a - b` to `return a + b` and verified that all tests pass.
```

## T3-寫檔案

### run 1 — PASS (7.3s) — 第3行='Fizz' 第15行='FizzBuzz'

```
I'll create a fizzbuzz.py file that prints the FizzBuzz sequence from 1 to 15, then run it to verify it works correctly.


Now I'll run the fizzbuzz.py script to verify it produces the correct output:


Perfect! The FizzBuzz script has been created and executed successfully. The output shows the correct sequence from 1 to 15:
- Numbers divisible by 3 show "Fizz"
- Numbers divisible by 5 show "Buzz" 
- Numbers divisible by both 3 and 5 show "FizzBuzz"
- All other numbers are printed as-is

The task is complete.
```

## T4-bash查資料

### run 1 — FAIL (8.8s) — 回答中找不到 42

```
I need to chat to finish.
```

## C1-跨檔bug

### run 1 — PASS (14.4s) — pytest → 3 passed in 0.00s

```
I'll help you fix the failing tests. Let's start by running the tests to see what's failing.


Now let's look at the actual implementation to understand why the tests are failing:


Let's also check the store implementation:


Now I can see the issue! Looking at the failing tests and the store implementation:

1. In test_exact_stock_can_be_sold: 
   - Store starts with 5 apples
   - First order places 3 apples (leaves 2)
   - Second order tries to place 2 apples, but fails because the condition is `> qty` instead of `>= qty`

2. In test_mixed_orders:
   - Store starts with 10 books
   - First order places 4 books (leaves 6)
   - Second order tries to place 6 books, but fails for the same reason

The bug is in the `reserve` method in store.py on line 15: it uses `>` (greater than) instead of `>=` (greater than or equal).

Let me fix this:


Now let's run the tests again to confirm they pass:


Perfect! All tests are now passing. Let me summarize what I found and fixed:

## Issue Analysis
The tests were failing due to a bug in the `reserve` method in `store.py`. The method was using a strict greater-than comparison (`> qty`) instead of a greater-than-or-equal comparison (`>= qty`).

## Root Cause
- When inventory exactly matched the requested quantity, the reservation would fail
- For example: 5 apples in stock, trying to reserve 5 apples would fail because `5 > 5` is false
- This caused both failing tests to not work as expected:
  - `test_exact_stock_can_be_sold`: Trying to sell exactly the remaining stock
  - `test_mixed_orders`: Trying to sell exactly the remaining stock after a partial sale

## Fix Applied
Changed line 15 in `/tmp/pibench-48bwh3gw/store.py` from:
```python
if self._stock.get(sku, 0) > qty:
```
to:
```python
if self._stock.get(sku, 0) >= qty:
```

This allows reservations when the available stock equals or exceeds the requested quantity, which is the correct behavior for an inventory system.

All 3 tests now pass successfully.
```

## C2-重構保綠

### run 1 — PASS (29.1s) — pytest 通過, 共用邏輯已抽到 utils.py

```
I'll help refactor the duplicated name-normalization logic into a shared utils.py module. First, let me examine the current files to understand the duplication.


Now let me examine the content of a.py, b.py, and test_ab.py to understand the duplicated logic and the tests.








Now I can see the duplicated logic: both `register_user` in a.py and `format_badge` in b.py contain the exact same name normalization logic: `" ".join(name.strip().split()).title()`. Let me extract this shared logic into a new utils.py file.


Now I'll update a.py to use the normalize_name function from utils.py:


Now I'll update b.py to use the normalize_name function from utils.py:


Now prefect…….”

/graph-auto

Let me verify that the refactored code still passes all tests by running pytest:


Perfect! All tests are passing. Let me also double-check the final content of all files to confirm the refactoring is correct:








The refactoring is complete and successful! I have:

1. Created a new `utils.py` file containing the shared name normalization logic in a `normalize_name` function
2. Updated `a.py` to import and use `normalize_name` from `utils.py`
3. Updated `b.py` to import and use `normalize_name` from `utils.py`
4. Verified that all tests in `test_ab.py` still pass (3/3 tests passed)
5. Confirmed that I did not modify `test_ab.py` as requested

The duplicated logic `" ".join(name.strip().split()).title()` has been successfully extracted into the shared utility function, and both modules now use this common function instead of duplicating the code.
```

## C3-誤導除錯

### run 1 — PASS (29.5s) — main.py → Server on localhost:8080 (admin 8081, workers 4), 根因已修

```
I'll help you find and fix the issue causing `python3 main.py` to crash. Let me start by examining the current directory and the main.py file to understand what's happening.


Now let me examine the main.py file to understand what it's trying to do and why it might be crashing.


Now let me check the config.py and server.py files to see what might be causing the crash.





Now let me check the settings.json file to see if there are any issues there:


Now I can see the issue! In settings.json, the "port" value is a string ("8080") instead of an integer. When config.py loads this and passes it to Server, the server.py tries to do `self.port + 1` on line 8, which fails because you can't add an integer to a string.

Let me run the program to confirm this is the error:


Perfect! As expected, the error is a TypeError because the port is a string and we're trying to add 1 to it. 

Since I'm not allowed to modify main.py, I need to fix this by ensuring the port value in settings.json is an integer rather than a string.


Now let me verify the fix by viewing the updated settings.json:


Great! Now let me test that the program runs successfully:


Perfect! The program now runs successfully and prints the startup banner as expected. The issue was that the port value in settings.json was a string ("8080") instead of an integer (8080), which caused a TypeError when the server.py tried to calculate the admin port by adding 1 to it.

I fixed the issue by changing the port value from a string to an integer in settings.json, and verified that `python3 main.py` now prints the startup banner successfully without modifying main.py.
```

## L1-spec建專案

### run 1 — PASS (28.6s) — pytest → 9 passed in 0.34s

```
I'll read the SPEC.md file to understand the requirements for implementing todo.py, then implement it according to the specification and verify with the tests.

First, let me check what files are available:


Now let me read the SPEC.md file to understand the requirements:


Now let me check the test file to understand what exactly is expected:


Now I'll implement todo.py according to the specification:


Now let's test the implementation by running the pytest tests:


Great! All tests pass. Let me also do a quick manual verification to ensure everything works correctly:











Perfect! All functionality is working as expected. Let me run the tests one more time to confirm:


The implementation has been successfully completed and all tests pass. The todo.py file implements a command-line todo manager that:

1. Stores todos in todos.json in the current working directory
2. Supports add, list, and done commands
3. Handles persistence across invocations
4. Provides correct ID generation (starting at 1, incrementing, never reused)
5. Formats output exactly as specified
6. Handles error cases appropriately

All 9 tests from test_todo.py pass, confirming the implementation meets the specification exactly.
```

## X1-陌生officecli

### run 1 — PASS (12.1s) — 產出 report.txt 且回答正確字數 45

```
I'll use the provided officecli tool to convert the DOCX file to text, then count the words in the resulting document.

First, let me check what files are available and examine the tool:


Now let me check the officecli tool to understand how to use it:


Let me check if the officecli tool has help or usage information:


Perfect! Now I can use the officecli tool to convert the report.docx to plain text format. Let me do that:


Now let me check the generated report.txt file and count the words:


Let me also verify the content looks correct by viewing the file:


The document has been successfully converted from report.docx to report.txt using the officecli tool. The document body contains **45 words**.
```

## X2-陌生opencli

### run 1 — PASS (24.0s) — 回答含正確價格 149.50

```
I'll help you find the price of the 'Aurora Lamp' product on http://shop.local/ using the opencli tool. Let me start by checking the help to understand how to use it.


Now I'll start by opening the shop.local URL to browse the site.


Now I'll look for links on the homepage to find navigation to products or the Aurora Lamp specifically.


I'll browse the products page to find the Aurora Lamp.


Let me check the links on the products page to see if there's a link to the Aurora Lamp.


Let me check the text content of the products page to find the Aurora Lamp and its price.


Perfect! I found the Aurora Lamp on the products page. The price is clearly stated as $149.50.

The Aurora Lamp costs $149.50.
```

## R1-agent-browser

### run 1 — PASS (19.5s) — 回答含頁面標題 Example Domain

```
I'll help you open https://example.com using the agent-browser command-line tool and get the page title.

First, let me run the command to open the URL and retrieve the page title.


Let me try the correct syntax for the agent-browser tool. I'll check how to properly use it.


Let me try to open the URL with the correct agent-browser syntax and get the page title.


The agent-browser tool successfully opened https://example.com and shows that the page title is "Example Domain". This is the expected title for the example.com website, which is a standard domain used for documentation and examples.
```
