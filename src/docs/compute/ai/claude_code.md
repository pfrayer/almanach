---
description: "Claude Code cheatsheet: install, slash commands, skills, subagents, hooks, plugins, MCP servers, permissions, extended thinking and the explore-plan-implement workflow."
---

# Claude Code

AI-powered coding agent in the terminal, built by Anthropic. Runs directly in your shell with full access to your codebase.

[Official docs](https://docs.claude.com/en/docs/claude-code){target=_blank} · [GitHub](https://github.com/anthropics/claude-code){target=_blank}

## Install

=== "npm"

    ```shell
    $ npm install -g @anthropic-ai/claude-code
    ```

=== "Native installer"

    ```shell
    # macOS & Linux
    $ curl -fsSL https://claude.ai/install.sh | bash

    # Windows (PowerShell)
    $ irm https://claude.ai/install.ps1 | iex
    ```

=== "Homebrew"

    ```shell
    $ brew install --cask claude-code
    ```

!!! tip "Migrate off npm"
    If you installed via npm and want to switch to the self-updating native binary, run `claude migrate-installer`.

## Launch & authenticate

```shell
$ claude
```

On first launch, Claude Code opens a browser to authenticate via your [claude.ai](https://claude.ai){target=_blank} account (Pro or Max plan). Manage the session later with `/login` and `/logout`.

Alternatively, set `ANTHROPIC_API_KEY` to use the API directly (pay-as-you-go):

```shell
$ export ANTHROPIC_API_KEY="sk-ant-..."
$ claude
```

For CI or scripts that can't open a browser, generate a long-lived token:

```shell
$ claude setup-token
```

## Keyboard shortcuts

| Shortcut | Action |
|----------|--------|
| ++esc++ | Interrupt Claude (stop the current operation) |
| ++esc++ ++esc++ | Rewind: edit a previous message / restore a checkpoint |
| ++shift+tab++ | Cycle permission mode (normal → auto-accept → plan) |
| ++ctrl+b++ | Move the current task to the background |
| ++ctrl+c++ | Cancel input, or quit when pressed twice |
| ++ctrl+d++ | Exit Claude Code |
| ++ctrl+l++ | Clear terminal |
| ++ctrl+r++ | Search command history |
| ++ctrl+o++ | Toggle verbose output |
| ++ctrl+v++ | Paste an image from the clipboard |
| ++up++ ++down++ | Navigate conversation history |
| `@` | Reference files / MCP resources, include contents in context |
| `#` | Add a memory to `CLAUDE.md` |
| `!` | Run a bash command directly; its output is added to context |
| `/` | Start a slash command |

## Slash commands

### Session & context

| Command | Description |
|---------|-------------|
| `/help` | Show available commands |
| `/clear` | Clear conversation history (start fresh) |
| `/compact` | Summarize history to reduce context usage |
| `/context` | Visualize the current context window usage |
| `/rewind` | Restore the conversation and/or files to an earlier checkpoint |
| `/resume` | Resume a previous conversation |
| `/export` | Export the current conversation to a file |
| `/cost` · `/usage` | Show token usage, cost and plan limits |

### Model & workflow

| Command | Description |
|---------|-------------|
| `/model` | Select the AI model |
| `/fast` | Toggle fast mode (faster Opus output, same model) |
| `/agents` | Manage subagents |
| `/review` | Review a GitHub pull request |
| `/code-review` | Review the current working diff for bugs and cleanups |
| `/simplify` | Cleanup-only review of the current diff |
| `/security-review` | Security review of pending changes |
| `/verify` | Build & run the change to confirm it works |
| `/run` | Launch and drive the project's app |

### Config & extend

| Command | Description |
|---------|-------------|
| `/init` | Generate `CLAUDE.md` for the current project |
| `/memory` | Edit `CLAUDE.md` memory files |
| `/config` | Open the settings interface |
| `/permissions` | View and edit tool permissions |
| `/add-dir` | Add a directory to the allowed list |
| `/mcp` | Manage MCP servers and view their status |
| `/hooks` | Browse configured hooks |
| `/plugin` | Manage plugins and marketplaces |
| `/output-style` | Switch the response style (default, explanatory, learning) |
| `/statusline` | Configure the status line |

### Utilities

| Command | Description |
|---------|-------------|
| `/doctor` | Diagnose and check the health of your install |
| `/team-onboarding` | Generate a teammate ramp-up guide (`ONBOARDING.md`) from your local usage, shareable via a link |
| `/bug` | Report a bug to Anthropic |
| `/release-notes` | Show what changed in recent versions |
| `/terminal-setup` | Configure ++shift+enter++ for newlines |
| `/vim` | Toggle vim keybindings in the input |
| `/quit` (or `/exit`) | Exit Claude Code |

!!! tip "Discover installed commands"
    `/help` lists everything available in the current project, including custom commands, bundled skills and anything a plugin adds — so it stays accurate even as the tool evolves.

## Extended thinking

Ask Claude to reason harder before acting by including a thinking keyword in your prompt. This allocates a larger reasoning budget — useful for architecture decisions, tricky debugging or multi-step planning.

```
Think about how to make this service resilient to a Postgres failover, then propose a design.

ultrathink about the race condition in the worker pool before touching anything.
```

Roughly ascending budget: `think` → `think hard` → `think harder` → `ultrathink`. Keep it off for routine edits — it costs tokens and time.

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

### Useful flags

| Flag | Description |
|------|-------------|
| `-p`, `--print` | Print mode: run once and exit (headless) |
| `--model` | Model for the session (`opus`, `sonnet`, `haiku`, or a full ID) |
| `--fallback-model` | Model to fall back to if the primary is overloaded |
| `-c`, `--continue` | Continue the most recent conversation |
| `-r`, `--resume` | Resume a specific session |
| `--output-format` | `text`, `json`, or `stream-json` |
| `--input-format` | `text` or `stream-json` (for piping structured input) |
| `--allowedTools` / `--disallowedTools` | Allow / deny tools without prompting |
| `--permission-mode` | Start in a given mode (`plan`, `acceptEdits`, …) |
| `--dangerously-skip-permissions` | Skip all permission checks (sandboxes only) |
| `--append-system-prompt` | Append extra instructions to the system prompt |
| `--add-dir` | Grant access to an extra working directory |
| `--mcp-config` | Load MCP servers from a specific file |
| `--agents` | Define subagents inline as JSON |
| `--session-id` | Use a fixed session ID |
| `--max-turns` | Cap the number of agentic turns |
| `--verbose` | Show full tool inputs and outputs |

### CLI subcommands

```shell
$ claude update                # Update to the latest version
$ claude doctor                # Diagnose the installation
$ claude config               # Read / write settings from the shell
$ claude mcp list              # Manage MCP servers (see below)
$ claude migrate-installer     # Move from the npm install to the native binary
$ claude --version             # Print the version
```

## File references

Use `@` to include file contents directly in your prompt:

```
What does this function do? @src/auth/login.py

Refactor @src/api/routes.ts to use async/await
```

Supports glob patterns, and — when MCP servers expose resources — `@server:resource` mentions:

```
Review all test files @tests/**/*.test.ts
```

## Custom instructions (`CLAUDE.md`)

Claude Code reads instructions from `CLAUDE.md` files, loaded from your home directory down to the working directory (later files take precedence):

1. **Enterprise policy** — a system-managed file (IT-deployed)
2. **User** — `~/.claude/CLAUDE.md` (applies to every project)
3. **Parent directories** — walking up from the project
4. **Project** — `./CLAUDE.md` at the repo root (commit it to share)
5. **Local** — `./CLAUDE.local.md` (personal, gitignore it)

Generate the project file with `/init`, or let Claude add entries on the fly with `#`.

```markdown
# Project conventions

- Format Python with ruff; never leave unused imports
- Run pytest before every commit
- Prefer explicit error handling over bare except

# Commands

- Build: `make build`
- Test: `poetry run pytest`
- Lint: `ruff check .`

# Imports

@docs/architecture.md
@~/.claude/my-personal-style.md
```

`@path` imports pull another file's contents into the instructions (up to 5 levels deep) — handy for sharing a common style file across repos.

## Custom commands

Drop a Markdown file in `.claude/commands/` (project) or `~/.claude/commands/` (global) to create a reusable slash command. The filename becomes the command name.

```markdown
<!-- .claude/commands/fix-issue.md -->
---
argument-hint: <issue-number>
description: Reproduce, fix and test a GitHub issue
allowed-tools: Bash(git*), Edit, Read
---

Find and fix issue #$1. Write a test that reproduces it,
then implement the fix and run the test suite.
```

```
/fix-issue 1234
```

Inside a command you can use `$ARGUMENTS` (everything passed), positional `$1` / `$2`, embed shell output with `` !`command` ``, and reference files with `@path`.

## Skills

Skills package a repeatable workflow, checklist or reference so Claude can pull it in exactly when it's relevant. A skill is a folder with a `SKILL.md` describing when and how to use it, plus any supporting scripts or files.

```markdown
<!-- .claude/skills/pytest-fix/SKILL.md -->
---
name: pytest-fix
description: Run the test suite and fix failures one by one. Use when tests are red.
allowed-tools: Bash, Read, Edit
---

1. Run `poetry run pytest -x` to stop at the first failure.
2. Read the traceback, locate the cause, apply a minimal fix.
3. Re-run until green. Never delete a test to make it pass.
```

Skills live in `.claude/skills/` (project) or `~/.claude/skills/` (global). Claude invokes a skill automatically when your request matches its `description`, or you can trigger it explicitly with `/skill-name`.

!!! tip "Skill vs subagent"
    A **skill** loads instructions into the current conversation — great for procedures and conventions. A **subagent** runs in its own context window — great for isolating heavy work (research, review) so it doesn't crowd the main thread.

## Subagents

Subagents are specialised assistants with their own prompt, tools, and context window — useful for delegating focused tasks (code review, debugging, research) without polluting the main conversation. Manage them with `/agents`, or define one as Markdown with YAML frontmatter:

```markdown
<!-- .claude/agents/reviewer.md -->
---
name: reviewer
description: Reviews code for bugs and style issues
tools: Read, Grep, Glob
model: haiku
---

You are a meticulous code reviewer. Focus on correctness,
edge cases, and adherence to the project's conventions.
```

The optional `model` field lets a subagent run on a cheaper/faster model than the main session. Claude delegates to a subagent automatically when the task fits its `description`, or you can ask for it by name.

## Output styles

Change how Claude formats its responses without touching the underlying behaviour:

| Style | Behaviour |
|-------|-----------|
| `default` | Concise, task-focused (the standard) |
| `explanatory` | Adds insight into *why* it made each choice |
| `learning` | Interactive — leaves small `TODO`s for you to implement |

Switch with `/output-style`, or set a default in settings: `"outputStyle": "explanatory"`.

## Plugins

Plugins bundle skills, subagents, commands, hooks and MCP servers into one installable package, distributed through marketplaces (a Git repo or URL).

```shell
# Add a marketplace, then install from it
$ claude plugin marketplace add anthropics/claude-code
$ claude plugin install <name>@<marketplace>
```

Manage everything interactively with `/plugin`. Enabled plugins are recorded in settings under `enabledPlugins`, so a project can ship a curated toolset to the whole team.

## Permissions

Claude Code asks before writing files or running commands. You can adjust this per session:

| Option | Description |
|--------|-------------|
| `--allowedTools` | Comma-separated list of tools to allow without prompting |
| `--disallowedTools` | Tools that are always denied |
| `/add-dir <path>` | Allow reads/writes in an extra directory |

Persist rules in settings under `permissions`, using tool-specific matchers:

```json
{
  "permissions": {
    "allow": ["Bash(poetry run pytest:*)", "Read(~/.config/**)"],
    "ask":   ["Bash(git push:*)"],
    "deny":  ["Read(.env)", "Bash(rm -rf:*)"]
  }
}
```

!!! warning "Dangerous permissions"
    `--dangerously-skip-permissions` disables all permission checks. Only use this in isolated environments (containers, CI).

### Permission modes

Press ++shift+tab++ to cycle between modes during a session:

| Mode | Behavior |
|------|----------|
| Normal | Ask before edits and commands (default) |
| Auto-accept edits | Apply file edits without prompting (`acceptEdits`) |
| Plan | Read-only: Claude explores and proposes a plan, but makes no changes until you approve (`plan`) |
| Bypass | Skip every permission prompt (`bypassPermissions`) |

Plan mode is ideal for "explore → plan → implement" workflows on anything non-trivial. Start a session straight in a mode with `claude --permission-mode plan`.

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
            "command": "jq -r '.tool_input.file_path' | xargs -r ruff format 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

A hook can also influence the flow by returning JSON on stdout (e.g. `{"decision": "block", "reason": "..."}` to stop a tool call and feed a message back to Claude) or via its exit code — exit `2` blocks and surfaces stderr to Claude; any other non-zero exit is a non-blocking error.

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

Claude Code supports Model Context Protocol servers for extending available tools (and exposing resources you can `@`-mention).

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

Settings are stored in `~/.claude/settings.json` (global) or `.claude/settings.json` (project-level). A `settings.local.json` holds personal, gitignored overrides.

```json
{
  "model": "claude-sonnet-4-6",
  "theme": "dark",
  "includeCoAuthoredBy": true,
  "cleanupPeriodDays": 30
}
```

### Key settings

| Key | Description |
|-----|-------------|
| `model` | Default model |
| `theme` | `dark`, `light`, `dark-daltonism`, `light-daltonism` |
| `outputStyle` | Default response style (see [Output styles](#output-styles)) |
| `includeCoAuthoredBy` | Add a `Co-Authored-By: Claude` trailer to commits |
| `cleanupPeriodDays` | Days before conversation logs are purged (default: 30) |
| `env` | Environment variables passed to all sessions |
| `apiKeyHelper` | Script that prints an API key/token (for rotation) |
| `permissions` | `allow` / `deny` / `ask` rules for tools (see [Permissions](#permissions)) |
| `enabledPlugins` | Plugins to enable for this project |
| `statusLine` | Command that renders a custom status line |
| `hooks` | Lifecycle hooks (see [Hooks](#hooks)) |

## Background tasks

Long-running commands (dev servers, test watchers, builds) can run in the background so the session stays interactive. Press ++ctrl+b++ while a command runs to detach it; Claude keeps a handle on its output and can check on it, read logs, or kill it later. Useful when you want Claude to start `poetry run uvicorn` and then keep working against the running server.

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

## Tips & recommended patterns

A few habits that pay off, especially on a Python/backend + CI workflow:

- **Give it a `CLAUDE.md` early.** Pin the package manager (Poetry), the test command, the linter (ruff), and any project quirks. It stops Claude from guessing on every session. Run `/init` to bootstrap it.
- **Auto-format on write.** A `PostToolUse` hook running `ruff format` / `ruff check --fix` on `Write|Edit` keeps the diff clean without you asking.
- **Plan mode for anything multi-file.** Migrations, refactors touching many modules, a new endpoint across schema + service + tests — let it lay out the approach first (++shift+tab++), review, then let it build.
- **Package repeatable reviews as skills.** You already lean on skills (SonarQube review, schema building). Anything you re-explain more than twice — a review checklist, a project scaffold, a release procedure — belongs in a `SKILL.md`.
- **Use the built-in review commands before pushing.** `/code-review` for bugs, `/security-review` for vulnerabilities, `/verify` to actually run the change end-to-end (not just the tests).
- **Restrict a review subagent to read-only tools** (`Read, Grep, Glob`) and put it on `haiku` — cheap, fast, and it can't accidentally edit anything.
- **Wire it into CI / git hooks.** `claude -p "..." --output-format json` in a pipeline, or a `pre-commit` hook that asks Claude to sanity-check the staged diff.
- **Add the GitHub MCP server** so Claude can read issues and PRs directly instead of you pasting them.
- **Manage context deliberately.** `/clear` between unrelated tasks, `/compact` when a long session gets sluggish, `/context` to see what's eating the window.
- **Reach for `ultrathink`** on genuinely hard design or debugging problems — and skip it for routine edits, since it costs tokens and time.

## Update

```shell
$ claude update
# or, if installed via npm
$ npm update -g @anthropic-ai/claude-code
```
