import json
import os

OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")


def build_pi_cmd(model, tools, prompt):
    cmd = ["pi", "--provider", "ollama", "--model", model, "-p", prompt]
    if tools:
        cmd[1:1] = ["--tools", tools]
    return cmd, {"PI_OFFLINE": "1", "PI_SKIP_VERSION_CHECK": "1"}


def build_opencode_cmd(model, tools, prompt):
    cmd = ["opencode", "run", "--model", f"ollama/{model}", "--auto",
           "--format", "json", prompt]
    return cmd, {}


def extract_opencode_text(stdout):
    """從 opencode 的 JSONL 事件流抽出模型給使用者的文字(type=text)。"""
    texts = []
    for line in stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        if ev.get("type") == "text":
            texts.append(ev.get("part", {}).get("text", ""))
    return "\n".join(t for t in texts if t)


def build_copilot_cmd(model, tools, prompt):
    cmd = ["copilot", "-p", prompt, "--allow-all-tools", "-s", "--no-color",
           "--no-custom-instructions", "--no-ask-user", "--no-auto-update"]
    return cmd, {"COPILOT_PROVIDER_BASE_URL": f"{OLLAMA_BASE_URL}/v1",
                 "COPILOT_MODEL": model}


def build_codex_cmd(model, tools, prompt):
    cmd = ["codex", "exec", "--oss", "--local-provider", "ollama",
           "-m", model, "--dangerously-bypass-approvals-and-sandbox", prompt]
    return cmd, {}


HARNESSES = {
    "pi": dict(build=build_pi_cmd, tools_supported=True, extract=None),
    "opencode": dict(build=build_opencode_cmd, tools_supported=False,
                     extract=extract_opencode_text),
    "copilot": dict(build=build_copilot_cmd, tools_supported=False, extract=None),
    "codex": dict(build=build_codex_cmd, tools_supported=False, extract=None),
}
