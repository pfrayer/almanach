# Claude Code

AI-powered coding agent in the terminal, built by Anthropic. Runs directly in your shell with full access to your codebase.

[Official docs](https://docs.anthropic.com/en/docs/claude-code){target=_blank} · [GitHub](https://github.com/anthropics/claude-code){target=_blank}

## Install

```shell
$ npm install -g @anthropic-ai/claude-code
```

## Launch & authenticate

```shell
$ claude
```

On first launch, Claude Code opens a browser to authenticate via your [claude.ai](https://claude.ai){target=_blank} account (Pro or Max plan required).

Alternatively, set `ANTHROPIC_API_KEY` to use your own API key directly:

```shell
$ export ANTHROPIC_API_KEY="sk-ant-..."
$ claude
```

## Keyboard shortcuts

| Shortcut | Action |
|----------|--------|
| ++ctrl+c++ | Interrupt current operation |
| ++ctrl+l++ | Clear terminal |
| ++ctrl+r++ | Search command history |
| ++up++ ++down++ | Navigate conversation history |
| `@` | Reference files and include contents in context |
| `#` | Add a memory to `CLAUDE.md` |

## Slash commands

| Command | Description |
|---------|-------------|
| `/help` | Show available commands |
| `/clear` | Clear conversation history |
| `/compact` | Summarize history to reduce context usage |
| `/model` | Select AI model |
| `/review` | Run a code review on recent changes |
| `/init` | Generate `CLAUDE.md` for the current project |
| `/memory` | Open `CLAUDE.md` in your editor |
| `/add-dir` | Add a directory to the allowed list |
| `/vim` | Toggle vim keybindings in the input |
| `/quit` | Exit Claude Code |

## Non-interactive mode

Run a single prompt from the command line (useful for scripts and CI):

```shell
# Print mode — output goes to stdout
$ claude -p "Explain the use of context in Go"

# Pipe input
$ cat error.log | claude -p "What does this error mean?"

# With a specific model
$ claude -p "Summarize this file" --model claude-opus-4-5 @src/main.py
```

## File references

Use `@` to include file contents directly in your prompt:

```
What does this function do? @src/auth/login.py

Refactor @src/api/routes.ts to use async/await
```

Supports glob patterns:

```
Review all test files @tests/**/*.test.ts
```

## Custom instructions

Claude Code reads instructions from `CLAUDE.md` in the project root (and any parent directories up to `~`). Generate it with `/init`, or let Claude add entries on the fly with `#`.

```markdown
# Project conventions

- Use black for Python formatting
- Run pytest before every commit
- Prefer explicit error handling over bare except

# Commands

- Build: `make build`
- Test: `make test`
- Lint: `make lint`
```

Global instructions live at `~/.claude/CLAUDE.md`.

## Permissions

Claude Code asks before writing files or running commands. You can adjust this per session:

| Option | Description |
|--------|-------------|
| `--allowedTools` | Comma-separated list of tools to allow without prompting |
| `--disallowedTools` | Tools that are always denied |
| `/add-dir <path>` | Allow reads/writes in an extra directory |

!!! warning "Dangerous permissions"
    `--dangerously-skip-permissions` disables all permission checks. Only use this in isolated environments (containers, CI).

## Hooks

Hooks are shell commands that run automatically at key points in the Claude Code lifecycle. Define them in `~/.claude/settings.json` (global) or `.claude/settings.json` (project).

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"Claude is about to run: $CLAUDE_TOOL_INPUT_COMMAND\""
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write $CLAUDE_TOOL_INPUT_FILE_PATH 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

### Hook events

| Event | Triggers when… |
|-------|----------------|
| `PreToolUse` | Before any tool call |
| `PostToolUse` | After any tool call completes |
| `Notification` | Claude sends a system notification |
| `Stop` | Claude finishes a response turn |

### Hook matchers

The `matcher` field is a regex matched against the tool name:

| Matcher | Matches |
|---------|---------|
| `Bash` | Shell commands |
| `Write` | File writes (new files) |
| `Edit` | File edits (existing files) |
| `Read` | File reads |
| `.*` | All tools |

## MCP servers

Claude Code supports Model Context Protocol servers for extending available tools.

Configure in `~/.claude/settings.json` or `.claude/settings.json`:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/projects"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<token>"
      }
    }
  }
}
```

## Configuration

Settings are stored in `~/.claude/settings.json` (global) or `.claude/settings.json` (project-level):

```json
{
  "model": "claude-sonnet-4-5",
  "theme": "dark",
  "verbose": false,
  "cleanupPeriodDays": 30
}
```

### Key settings

| Key | Description |
|-----|-------------|
| `model` | Default model |
| `theme` | `dark`, `light`, `dark-daltonism`, `light-daltonism` |
| `verbose` | Show full tool outputs |
| `cleanupPeriodDays` | Days before conversation logs are purged (default: 30) |
| `env` | Environment variables passed to all sessions |

## Workflow: explore → plan → implement

```
# 1. Read the codebase without writing anything
Read the authentication module and tell me how sessions are managed.
Don't make any changes yet.

# 2. Plan
How would you add OAuth2 with Google? What files would need to change?

# 3. Implement
Go ahead and implement the plan.

# 4. Verify
Run the tests and fix any failures.

# 5. Commit
Commit these changes with a descriptive message.
```

## Multi-agent with git worktrees

Run multiple independent Claude Code sessions in parallel using git worktrees:

```shell
# Create worktrees for parallel tasks
$ git worktree add ../feature-auth -b feature/auth
$ git worktree add ../feature-api -b feature/api

# Launch agents in each
$ cd ../feature-auth && claude
$ cd ../feature-api && claude    # in another terminal
```

!!! tip "Isolate long-running tasks"
    Each worktree has its own working directory and git state, so agents can't interfere with each other.

## Update

```shell
$ npm update -g @anthropic-ai/claude-code
```
