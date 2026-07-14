import json
import os

OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
LITELLM_BASE_URL = os.environ.get("LITELLM_BASE_URL", "http://localhost:4000")

PROVIDERS = ("ollama", "litellm")


def build_pi_cmd(model, provider, tools, prompt, workdir):
    if provider == "litellm":
        cmd = ["pi", "--provider", "litellm", "--model", model, "-p", prompt]
        env = {"PI_OFFLINE": "1", "PI_SKIP_VERSION_CHECK": "1"}
    else:
        cmd = ["pi", "--provider", "ollama", "--model", model, "-p", prompt]
        env = {"PI_OFFLINE": "1", "PI_SKIP_VERSION_CHECK": "1"}
    if tools:
        cmd[1:1] = ["--tools", tools]
    cmd[1:1] = ["--no-session"]
    return cmd, env


def build_opencode_cmd(model, provider, tools, prompt, workdir):
    prefix = "litellm" if provider == "litellm" else "ollama"
    cmd = ["opencode", "run", "--dir", str(workdir),
           "--model", f"{prefix}/{model}", "--auto", "--format", "json",
           prompt]
    return cmd, {}


def extract_opencode_text(stdout):
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


def build_copilot_cmd(model, provider, tools, prompt, workdir):
    env = {"COPILOT_PROVIDER_TYPE": "openai", "COPILOT_MODEL": model}
    if provider == "litellm":
        base = f"{LITELLM_BASE_URL}/v1"
        env["COPILOT_PROVIDER_API_KEY"] = "sk-1234"
    else:
        base = f"{OLLAMA_BASE_URL}/v1"
    env["COPILOT_PROVIDER_BASE_URL"] = base
    cmd = ["copilot", "-C", str(workdir), "-p", prompt,
           "--allow-all-tools", "-s", "--no-color",
           "--no-custom-instructions", "--no-ask-user", "--no-auto-update"]
    return cmd, env


def build_codex_cmd(model, provider, tools, prompt, workdir):
    if provider == "litellm":
        cmd = ["codex", "exec", "-C", str(workdir), "--ephemeral", "-m", model,
               "--dangerously-bypass-approvals-and-sandbox", prompt]
        env = {"OPENAI_BASE_URL": LITELLM_BASE_URL,
               "OPENAI_API_KEY": "sk-1234"}
    else:
        cmd = ["codex", "exec", "-C", str(workdir), "--ephemeral",
               "--oss", "--local-provider", "ollama",
               "-m", model, "--dangerously-bypass-approvals-and-sandbox", prompt]
        env = {}
    return cmd, env


HARNESSES = {
    "pi": dict(build=build_pi_cmd, tools_supported=True, extract=None),
    "opencode": dict(build=build_opencode_cmd, tools_supported=False,
                     extract=extract_opencode_text),
    "copilot": dict(build=build_copilot_cmd, tools_supported=False, extract=None),
    "codex": dict(build=build_codex_cmd, tools_supported=False, extract=None),
}
