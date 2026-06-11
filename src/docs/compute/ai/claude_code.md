---
description: "Claude Code cheatsheet: install, slash commands, subagents, hooks, MCP servers, permissions and the explore-plan-implement workflow."
---

# Claude Code

AI-powered coding agent in the terminal, built by Anthropic. Runs directly in your shell with full access to your codebase.

[Official docs](https://docs.claude.com/en/docs/claude-code){target=_blank} · [GitHub](https://github.com/anthropics/claude-code){target=_blank}

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
| ++esc++ | Interrupt Claude (stop the current operation) |
| ++esc++ ++esc++ | Rewind: edit a previous message / restore a checkpoint |
| ++shift+tab++ | Cycle permission mode (normal → auto-accept → plan) |
| ++ctrl+c++ | Cancel input, or quit when pressed twice |
| ++ctrl+l++ | Clear terminal |
| ++ctrl+r++ | Search command history |
| ++up++ ++down++ | Navigate conversation history |
| `@` | Reference files and include contents in context |
| `#` | Add a memory to `CLAUDE.md` |
| `!` | Run a bash command directly; its output is added to context |

## Slash commands

| Command | Description |
|---------|-------------|
| `/help` | Show available commands |
| `/clear` | Clear conversation history |
| `/compact` | Summarize history to reduce context usage |
| `/context` | Show current context window usage |
| `/model` | Select AI model |
| `/config` | Open the settings interface |
| `/review` | Run a code review on recent changes |
| `/init` | Generate `CLAUDE.md` for the current project |
| `/memory` | Edit `CLAUDE.md` memory files |
| `/agents` | Manage subagents |
| `/mcp` | Manage MCP servers and view their status |
| `/permissions` | View and edit tool permissions |
| `/add-dir` | Add a directory to the allowed list |
| `/resume` | Resume a previous conversation |
| `/cost` | Show token usage and cost for the session |
| `/vim` | Toggle vim keybindings in the input |
| `/doctor` | Diagnose and check the health of your install |
| `/quit` (or `/exit`) | Exit Claude Code |

## Non-interactive mode

Run a single prompt from the command line (useful for scripts and CI):

```shell
# Print mode — output goes to stdout
$ claude -p "Explain the use of context in Go"

# Pipe input
$ cat error.log | claude -p "What does this error mean?"

# With a specific model
$ claude -p "Summarize this file" --model claude-opus-4-8 @src/main.py

# Machine-readable output (useful in CI)
$ claude -p "List the exported functions" --output-format json

# Continue the most recent conversation non-interactively
$ claude -p --continue "Now add tests for that function"
```

Useful flags: `--model`, `--output-format` (`text`, `json`, `stream-json`), `--continue` / `--resume`, `--allowedTools`, `--add-dir`.

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

## Custom commands

Drop a Markdown file in `.claude/commands/` (project) or `~/.claude/commands/` (global) to create a reusable slash command. The filename becomes the command name, and `$ARGUMENTS` is substituted with whatever you pass.

```markdown
<!-- .claude/commands/fix-issue.md -->
Find and fix issue #$ARGUMENTS. Write a test that reproduces it,
then implement the fix and run the test suite.
```

```
/fix-issue 1234
```

## Subagents

Subagents are specialised assistants with their own prompt, tools, and context window — useful for delegating focused tasks (code review, debugging, research) without polluting the main conversation. Manage them interactively with `/agents`, or define one as a Markdown file with YAML frontmatter:

```markdown
<!-- .claude/agents/reviewer.md -->
---
name: reviewer
description: Reviews code for bugs and style issues
tools: Read, Grep, Glob
---

You are a meticulous code reviewer. Focus on correctness,
edge cases, and adherence to the project's conventions.
```

## Permissions

Claude Code asks before writing files or running commands. You can adjust this per session:

| Option | Description |
|--------|-------------|
| `--allowedTools` | Comma-separated list of tools to allow without prompting |
| `--disallowedTools` | Tools that are always denied |
| `/add-dir <path>` | Allow reads/writes in an extra directory |

!!! warning "Dangerous permissions"
    `--dangerously-skip-permissions` disables all permission checks. Only use this in isolated environments (containers, CI).

### Permission modes

Press ++shift+tab++ to cycle between modes during a session:

| Mode | Behavior |
|------|----------|
| Normal | Ask before edits and commands (default) |
| Auto-accept edits | Apply file edits without prompting |
| Plan | Read-only: Claude explores and proposes a plan, but makes no changes until you approve it |

Plan mode is ideal for "explore → plan → implement" workflows on anything non-trivial: let Claude analyse the codebase and lay out its approach before it touches a file. You can also start a session straight in plan mode with `claude --permission-mode plan`.

## Hooks

Hooks are shell commands that run automatically at key points in the Claude Code lifecycle. Define them in `~/.claude/settings.json` (global) or `.claude/settings.json` (project).

Each hook receives a JSON payload **on stdin** (containing the tool name, tool input, etc.) — parse it with `jq`. The environment variable `$CLAUDE_PROJECT_DIR` points at the project root.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '\"Claude is about to run: \" + .tool_input.command'"
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
            "command": "jq -r '.tool_input.file_path' | xargs -r prettier --write 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

A hook can also influence the flow by returning JSON on stdout (e.g. to block a tool call or feed a message back to Claude) or via its exit code — a non-zero exit surfaces stderr back to Claude.

### Hook events

| Event | Triggers when… |
|-------|----------------|
| `PreToolUse` | Before a tool call (can block it) |
| `PostToolUse` | After a tool call completes |
| `UserPromptSubmit` | When you submit a prompt (can inject context or block) |
| `Notification` | Claude sends a system notification |
| `Stop` | Claude finishes a response turn |
| `SubagentStop` | A subagent finishes its turn |
| `SessionStart` / `SessionEnd` | A session starts / ends |
| `PreCompact` | Before the conversation is compacted |

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

The quickest way to add one is the `claude mcp add` command, which writes the config for you:

```shell
# Local stdio server (scoped to you, on this machine)
$ claude mcp add filesystem -- npx -y @modelcontextprotocol/server-filesystem /projects

# Project-scoped server, shared with the team via .mcp.json
$ claude mcp add --scope project github \
    --env GITHUB_PERSONAL_ACCESS_TOKEN=<token> \
    -- npx -y @modelcontextprotocol/server-github

# A remote HTTP/SSE server
$ claude mcp add --transport http linear https://mcp.linear.app/mcp

$ claude mcp list      # list configured servers
```

Project-scoped servers are stored in a `.mcp.json` file at the repo root (commit it to share with the team):

```json
{
  "mcpServers": {
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

Manage and inspect servers at runtime with the `/mcp` slash command.

## Configuration

Settings are stored in `~/.claude/settings.json` (global) or `.claude/settings.json` (project-level):

```json
{
  "model": "claude-sonnet-4-6",
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
| `permissions` | `allow` / `deny` / `ask` rules for tools (see [Permissions](#permissions)) |
| `statusLine` | Command that renders a custom status line |
| `hooks` | Lifecycle hooks (see [Hooks](#hooks)) |

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

!!! tip "Use plan mode for steps 1–2"
    Press ++shift+tab++ to enter plan mode so Claude explores and proposes its approach without editing any files until you approve.

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
