#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$SCRIPT_DIR/.litellm.pid"
LOG_FILE="$SCRIPT_DIR/.litellm.log"
CONFIG_FILE="$SCRIPT_DIR/litellm_config.yaml"
PORT="${LITELLM_PORT:-4000}"
HOST="${LITELLM_HOST:-127.0.0.1}"
BASE_URL="http://$HOST:$PORT"
API_KEY="sk-1234"

# PostgreSQL connection
DB_HOST="${LITELLM_DB_HOST:-localhost}"
DB_PORT="${LITELLM_DB_PORT:-5432}"
DB_NAME="${LITELLM_DB_NAME:-litellm}"
DB_USER="${LITELLM_DB_USER:-litellm}"
DB_PASSWORD="${LITELLM_DB_PASSWORD:-litellm_password}"
DATABASE_URL="postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

error() { echo -e "${RED}✗${NC} $*" >&2; }
success() { echo -e "${GREEN}✓${NC} $*"; }
info() { echo -e "${YELLOW}→${NC} $*"; }

check_config() {
    if [[ ! -f "$CONFIG_FILE" ]]; then
        error "Config not found: $CONFIG_FILE"
        exit 1
    fi
}

check_aws_env() {
    if [[ -z "${AWS_ACCESS_KEY_ID:-}" ]] || [[ -z "${AWS_SECRET_ACCESS_KEY:-}" ]]; then
        error "AWS credentials not set"
        info "Export: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION"
        exit 1
    fi
    if [[ -z "${AWS_DEFAULT_REGION:-}" ]] && [[ -z "${AWS_REGION_NAME:-}" ]]; then
        info "AWS_DEFAULT_REGION not set, using us-west-2"
        export AWS_DEFAULT_REGION=us-west-2
    fi
}

check_postgres() {
    if ! command -v psql &>/dev/null; then
        error "PostgreSQL not found"
        info "Install: sudo apt install postgresql"
        exit 1
    fi

    if ! pg_isready -h "$DB_HOST" -p "$DB_PORT" >/dev/null 2>&1; then
        error "PostgreSQL not running at $DB_HOST:$DB_PORT"
        info "Start: sudo systemctl start postgresql"
        exit 1
    fi

    # Test connection to database
    if ! PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c '\q' 2>/dev/null; then
        error "Cannot connect to database '$DB_NAME'"
        info "Setup database: sudo bash setup_litellm_db.sh"
        exit 1
    fi
}

is_running() {
    [[ -f "$PID_FILE" ]] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null
}

get_pid() {
    [[ -f "$PID_FILE" ]] && cat "$PID_FILE"
}

cmd_start() {
    check_config
    check_aws_env
    check_postgres

    if is_running; then
        local pid
        pid=$(get_pid)
        success "LiteLLM already running (PID: $pid)"
        info "Use './litellm.sh restart' to reload config"
        return 0
    fi

    info "Starting LiteLLM with PostgreSQL..."

    # Use PostgreSQL database
    export DATABASE_URL="$DATABASE_URL"

    litellm --config "$CONFIG_FILE" --port "$PORT" --host "$HOST" \
        </dev/null >>"$LOG_FILE" 2>&1 &
    local pid=$!
    echo "$pid" > "$PID_FILE"

    # Wait for ready
    info "Waiting for LiteLLM to start..."
    for i in {1..30}; do
        sleep 1
        if curl -sf "$BASE_URL/health" -H "Authorization: Bearer $API_KEY" >/dev/null 2>&1; then
            success "LiteLLM started (PID: $pid)"
            success "Listening on $BASE_URL"
            success "Database: postgresql://$DB_USER@$DB_HOST:$DB_PORT/$DB_NAME"
            info "Logs: $LOG_FILE"
            return 0
        fi
        echo -n "."
    done

    echo ""
    error "Failed to start (timeout)"
    info "Check logs: tail $LOG_FILE"

    # Cleanup on failure
    if [[ -f "$PID_FILE" ]]; then
        rm "$PID_FILE"
    fi
    exit 1
}

cmd_stop() {
    if ! is_running; then
        info "LiteLLM not running"
        [[ -f "$PID_FILE" ]] && rm "$PID_FILE"
        return 0
    fi

    local pid
    pid=$(get_pid)
    info "Stopping LiteLLM (PID: $pid)..."
    kill "$pid" 2>/dev/null || true

    # Wait for process to exit
    for i in {1..10}; do
        if ! kill -0 "$pid" 2>/dev/null; then
            success "LiteLLM stopped"
            rm "$PID_FILE"
            return 0
        fi
        sleep 0.5
    done

    # Force kill if still alive
    if kill -0 "$pid" 2>/dev/null; then
        info "Force killing..."
        kill -9 "$pid" 2>/dev/null || true
    fi

    rm "$PID_FILE"
    success "LiteLLM stopped"
}

cmd_restart() {
    cmd_stop
    sleep 1
    cmd_start
}

cmd_status() {
    if is_running; then
        local pid
        pid=$(get_pid)
        success "LiteLLM is running"
        echo "  PID:      $pid"
        echo "  URL:      $BASE_URL"
        echo "  Config:   $CONFIG_FILE"
        echo "  Database: postgresql://$DB_USER@$DB_HOST:$DB_PORT/$DB_NAME"
        echo "  Log:      $LOG_FILE"
        echo ""
        echo "Models:"
        curl -sf "$BASE_URL/v1/models" -H "Authorization: Bearer $API_KEY" 2>/dev/null \
            | jq -r '.data[].id' 2>/dev/null \
            | sed 's/^/  - /' || echo "  (failed to fetch)"
    else
        info "LiteLLM not running"
        [[ -f "$PID_FILE" ]] && rm "$PID_FILE"
        return 1
    fi
}

cmd_logs() {
    local tail_lines=""
    if [[ "${1:-}" == "--tail" ]] && [[ -n "${2:-}" ]]; then
        tail_lines="-n $2"
    elif [[ "${1:-}" == "-f" ]] || [[ "${1:-}" == "--follow" ]]; then
        tail_lines="-f"
    fi

    if [[ ! -f "$LOG_FILE" ]]; then
        error "Log file not found: $LOG_FILE"
        exit 1
    fi

    if [[ -n "$tail_lines" ]]; then
        tail $tail_lines "$LOG_FILE"
    else
        cat "$LOG_FILE"
    fi
}

cmd_test() {
    if ! is_running; then
        error "LiteLLM not running"
        info "Start with: ./litellm.sh start"
        exit 1
    fi

    info "Testing health endpoint..."
    if ! curl -sf "$BASE_URL/health" -H "Authorization: Bearer $API_KEY" >/dev/null; then
        error "Health check failed"
        exit 1
    fi
    success "Health OK"

    info "Testing model (bedrock/nvidia.nemotron-super-3-120b)..."
    local response
    response=$(curl -sf "$BASE_URL/v1/chat/completions" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $API_KEY" \
        -d '{"model":"bedrock/nvidia.nemotron-super-3-120b","messages":[{"role":"user","content":"Hi"}],"max_tokens":3}' 2>/dev/null)

    if [[ -z "$response" ]]; then
        error "Model test failed (no response)"
        exit 1
    fi

    if echo "$response" | grep -q '"error"'; then
        error "Model test failed:"
        echo "$response" | jq -r '.error.message' 2>/dev/null || echo "$response"
        exit 1
    fi

    local content
    content=$(echo "$response" | jq -r '.choices[0].message.content' 2>/dev/null || echo "")
    success "Model OK: $content"
}

get_models() {
    grep 'model_name:' "$CONFIG_FILE" | sed 's/.*model_name:[[:space:]]*//' | tr -d '"'
}

cmd_warmup() {
    if ! is_running; then
        error "LiteLLM not running"
        exit 1
    fi

    local models
    models=$(get_models)
    local total
    total=$(echo "$models" | wc -l)
    local ok=0 fail=0

    info "Warming up $total models (parallel)..."

    local pids=()
    local tmpdir
    tmpdir=$(mktemp -d)

    for model in $models; do
        (
            local start_ms
            start_ms=$(date +%s%3N)
            local resp
            resp=$(curl -sf --max-time 120 "$BASE_URL/v1/chat/completions" \
                -H "Content-Type: application/json" \
                -H "Authorization: Bearer $API_KEY" \
                -d "{\"model\":\"$model\",\"messages\":[{\"role\":\"user\",\"content\":\"hi\"}],\"max_tokens\":3}" 2>&1)
            local rc=$?
            local end_ms
            end_ms=$(date +%s%3N)
            local elapsed=$(( end_ms - start_ms ))

            if [[ $rc -eq 0 ]] && echo "$resp" | grep -q '"choices"'; then
                echo "OK ${elapsed}ms" > "$tmpdir/$(echo "$model" | tr '/:' '__')"
            else
                echo "FAIL ${elapsed}ms" > "$tmpdir/$(echo "$model" | tr '/:' '__')"
            fi
        ) &
        pids+=($!)
    done

    for pid in "${pids[@]}"; do
        wait "$pid" 2>/dev/null || true
    done

    for model in $models; do
        local key
        key=$(echo "$model" | tr '/:' '__')
        if [[ -f "$tmpdir/$key" ]]; then
            local result
            result=$(cat "$tmpdir/$key")
            local status="${result%% *}"
            local elapsed="${result#* }"
            if [[ "$status" == "OK" ]]; then
                success "$model  ($elapsed)"
                ((ok++))
            else
                error "$model  ($elapsed)"
                ((fail++))
            fi
        else
            error "$model  (no result)"
            ((fail++))
        fi
    done

    rm -rf "$tmpdir"
    echo ""
    success "Warmup done: $ok OK, $fail failed (out of $total)"
}

cmd_health() {
    if ! is_running; then
        error "LiteLLM not running"
        exit 1
    fi

    info "Checking LiteLLM health..."
    if ! curl -sf "$BASE_URL/health" -H "Authorization: Bearer $API_KEY" >/dev/null; then
        error "Proxy health endpoint failed"
        exit 1
    fi
    success "Proxy OK ($BASE_URL)"
    echo ""

    local models
    models=$(get_models)
    local total
    total=$(echo "$models" | wc -l)
    local ok=0 fail=0 slow=0
    local SLOW_THRESHOLD_MS=10000

    info "Checking $total models..."
    echo ""
    printf "  %-50s  %8s  %s\n" "MODEL" "LATENCY" "STATUS"
    printf "  %-50s  %8s  %s\n" "-----" "-------" "------"

    for model in $models; do
        local start_ms
        start_ms=$(date +%s%3N)
        local resp
        resp=$(curl -sf --max-time 120 "$BASE_URL/v1/chat/completions" \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer $API_KEY" \
            -d "{\"model\":\"$model\",\"messages\":[{\"role\":\"user\",\"content\":\"ping\"}],\"max_tokens\":3}" 2>&1)
        local rc=$?
        local end_ms
        end_ms=$(date +%s%3N)
        local elapsed=$(( end_ms - start_ms ))

        if [[ $rc -eq 0 ]] && echo "$resp" | grep -q '"choices"'; then
            if [[ $elapsed -gt $SLOW_THRESHOLD_MS ]]; then
                printf "  %-50s  %6dms  ${YELLOW}SLOW${NC}\n" "$model" "$elapsed"
                ((ok++))
                ((slow++))
            else
                printf "  %-50s  %6dms  ${GREEN}OK${NC}\n" "$model" "$elapsed"
                ((ok++))
            fi
        else
            local err_msg=""
            if [[ -n "$resp" ]]; then
                err_msg=$(echo "$resp" | jq -r '.error.message // empty' 2>/dev/null || true)
            fi
            printf "  %-50s  %6dms  ${RED}FAIL${NC}" "$model" "$elapsed"
            [[ -n "$err_msg" ]] && printf "  %s" "$err_msg"
            printf "\n"
            ((fail++))
        fi
    done

    echo ""
    echo "  ──────────────────────────────────────────"
    echo "  Total: $total  OK: $ok  Slow: $slow  Fail: $fail"
    [[ $slow -gt 0 ]] && info "Slow threshold: ${SLOW_THRESHOLD_MS}ms (cold start is normal for first invoke)"
    [[ $fail -gt 0 ]] && error "Some models failed — check logs: ./litellm.sh logs --tail 50"
}

cmd_clean() {
    if is_running; then
        error "LiteLLM is still running"
        info "Stop first: ./litellm.sh stop"
        exit 1
    fi

    info "Cleaning up..."
    rm -f "$PID_FILE" "$LOG_FILE"
    success "Cleaned: PID file and logs"
    info "Database data preserved in PostgreSQL"
}

cmd_db() {
    info "Connecting to PostgreSQL..."
    PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME"
}

cmd_help() {
    cat <<EOF
Usage: $0 <command> [options]

Commands:
  start              Start LiteLLM with PostgreSQL
  stop               Stop LiteLLM
  restart            Restart LiteLLM
  status             Show running status and loaded models
  logs [--tail N]    Show logs (default: all, --tail N: last N lines, -f: follow)
  test               Test health and model API
  warmup             Warm up all models in parallel (trigger cold start)
  health             Check proxy and each model with latency report
  db                 Connect to PostgreSQL database
  clean              Remove PID file and logs (must stop first)
  help               Show this help

Environment variables:
  LITELLM_PORT          Port to listen on (default: 4000)
  LITELLM_HOST          Host to bind (default: 127.0.0.1)
  LITELLM_DB_HOST       PostgreSQL host (default: localhost)
  LITELLM_DB_PORT       PostgreSQL port (default: 5432)
  LITELLM_DB_NAME       Database name (default: litellm)
  LITELLM_DB_USER       Database user (default: litellm)
  LITELLM_DB_PASSWORD   Database password (default: litellm_password)
  AWS_ACCESS_KEY_ID     AWS credentials (required)
  AWS_SECRET_ACCESS_KEY
  AWS_DEFAULT_REGION    (default: us-west-2)

Setup:
  1. Install PostgreSQL: sudo apt install postgresql
  2. Create database: sudo bash setup_litellm_db.sh
  3. Start LiteLLM: ./litellm.sh start

Files:
  .litellm.pid       Process ID
  .litellm.log       Application logs
  PostgreSQL         Database at $DB_HOST:$DB_PORT/$DB_NAME

Examples:
  $0 start
  $0 status
  $0 db              # Connect to database
  $0 logs -f
  $0 test
  $0 stop
EOF
}

# Main
case "${1:-help}" in
    start)   cmd_start ;;
    stop)    cmd_stop ;;
    restart) cmd_restart ;;
    status)  cmd_status ;;
    logs)    shift; cmd_logs "$@" ;;
    test)    cmd_test ;;
    warmup)  cmd_warmup ;;
    health)  cmd_health ;;
    db)      cmd_db ;;
    clean)   cmd_clean ;;
    help|-h|--help) cmd_help ;;
    *)
        error "Unknown command: $1"
        echo ""
        cmd_help
        exit 1
        ;;
esac
