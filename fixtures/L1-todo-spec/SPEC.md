# todo.py — Command-line Todo Manager

Implement `todo.py` in this directory. It is invoked as `python3 todo.py <command> [args]`.

## Storage

- All todos are stored in `todos.json` in the current working directory.
- If the file does not exist, treat it as an empty list. Create it on first write.
- Persistence must survive across separate invocations.

## Commands

### `add <text>`

- Adds a todo with the given text.
- Ids start at 1 and increment by 1 for every added todo (ids are never reused).
- Prints exactly: `added <id>`
- Exit code 0.

### `list`

- Prints one line per todo, in the order they were added:
  - Not done: `<id> [ ] <text>`
  - Done: `<id> [x] <text>`
- If there are no todos, prints exactly: `no todos`
- Exit code 0.

### `done <id>`

- Marks the todo with that id as done.
- Prints exactly: `done <id>` — this also applies if it was already done (idempotent).
- If no todo has that id: prints exactly `not found` and exits with code 1.
- Exit code 0 on success.

## Notes

- Any other command or missing arguments: exit code is not tested; behave reasonably.
- Output must match the formats above exactly (single spaces, lowercase keywords).
