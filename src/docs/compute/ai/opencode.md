---
description: "OpenCode cheatsheet: install, agents, slash commands, permissions, skills, the plan-then-build workflow, MCP servers, LSP and custom commands."
---

# OpenCode

Open-source AI coding agent in the terminal. Built by [Anomaly](https://anomaly.co){target=_blank}, 100% provider-agnostic.

[Official docs](https://opencode.ai/docs){target=_blank} · [GitHub](https://github.com/anomalyco/opencode){target=_blank}

## Install

=== "Install script"

    ```shell
    $ curl -fsSL https://opencode.ai/install | bash
    ```

=== "Homebrew"

    ```shell
    $ brew install anomalyco/tap/opencode
    ```

=== "npm"

    ```shell
    $ npm install -g opencode-ai@latest
    ```

=== "Arch Linux"

    ```shell
    $ sudo pacman -S opencode      # Stable
    $ paru -S opencode-bin          # Latest (AUR)
    ```

=== "Windows"

    ```shell
    $ scoop install opencode
    $ choco install opencode
    ```

=== "Nix"

    ```shell
    $ nix run nixpkgs#opencode
    ```

A desktop app is also available at [opencode.ai/download](https://opencode.ai/download){target=_blank}.

## Launch & authenticate

```shell
$ opencode
```

On first launch, use `/connect` to add a provider and enter your API key. OpenCode supports 75+ providers via the [AI SDK](https://ai-sdk.dev/){target=_blank}.

Alternatively, set API keys via environment variables:

| Variable | Provider |
|----------|----------|
| `ANTHROPIC_API_KEY` | Anthropic |
| `OPENAI_API_KEY` | OpenAI |
| `GEMINI_API_KEY` | Google Gemini |
| `GROQ_API_KEY` | Groq |
| `OPENROUTER_API_KEY` | OpenRouter |
| `GITHUB_TOKEN` | GitHub Copilot |
| `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` | AWS Bedrock |
| `AZURE_OPENAI_API_ENDPOINT` / `AZURE_OPENAI_API_KEY` | Azure OpenAI |

## Agents

OpenCode includes built-in agents you can switch between with ++tab++.

### Primary agents

| Agent | Description |
|-------|-------------|
| **Build** | Default agent, full tool access for development work |
| **Plan** | Analysis and planning agent (file edits and bash default to `ask`) |

### Subagents

Invoked automatically (via the `task` tool) or with an `@mention` in messages, e.g. `@general`. Each runs in a child session: enter it with ++ctrl+x++ ++down++, cycle siblings with ++left++ / ++right++, go back to the parent with ++up++.

| Agent | Description |
|-------|-------------|
| **General** | Full-access agent for research and multi-step tasks, can run work in parallel |
| **Explore** | Fast, read-only agent for finding files and searching code |
| **Scout** | Read-only agent for external docs and dependency research |

### Custom agents

Define custom agents in `opencode.json`, as markdown files in `.opencode/agents/` (project) or `~/.config/opencode/agents/` (global), or interactively with `opencode agent create`:

```json
{
  "agent": {
    "code-reviewer": {
      "description": "Reviews code for best practices",
      "mode": "subagent",
      "model": "anthropic/claude-sonnet-5-5",
      "prompt": "{file:./prompts/review.txt}",
      "permission": { "edit": "deny", "bash": "ask" }
    }
  }
}
```

The old `tools` map is deprecated — restrict an agent with `permission` instead. `hidden: true` hides a subagent from the `@` menu.

## Keyboard shortcuts

OpenCode uses a **leader key** (default: ++ctrl+x++) for most shortcuts. Press the leader, then the action key.

| Shortcut | Action |
|----------|--------|
| ++ctrl+p++ | Command palette |
| ++ctrl+t++ | Cycle model variants (reasoning effort) |
| ++ctrl+c++ | Quit |
| ++ctrl+x++ `n` | New session |
| ++ctrl+x++ `l` | List / switch sessions |
| ++ctrl+x++ `m` | Select model |
| ++ctrl+x++ `e` | Open external editor |
| ++ctrl+x++ `u` | Undo last message + file changes |
| ++ctrl+x++ `r` | Redo |
| ++ctrl+x++ `c` | Compact (summarize) session |
| ++ctrl+x++ `x` | Export conversation to Markdown |
| ++ctrl+x++ `t` | Switch theme |
| ++ctrl+x++ `b` | Toggle sidebar |
| ++ctrl+x++ `q` | Quit |
| ++tab++ | Cycle primary agents (Build ↔ Plan) |
| ++escape++ | Cancel / close overlay |
| `@` | Reference files (fuzzy search) |
| `!` | Run shell command directly |

## Slash commands

| Command | Description |
|---------|-------------|
| `/connect` | Add a provider |
| `/models` | List / select model |
| `/init` | Create or update `AGENTS.md` for the project (guided) |
| `/new` (alias `/clear`) | Start a new session |
| `/sessions` (`/resume`, `/continue`) | List and switch sessions |
| `/undo` | Undo last message and revert file changes (needs a Git repo) |
| `/redo` | Redo a previously undone message |
| `/compact` (alias `/summarize`) | Summarize conversation to reduce context |
| `/share` | Share session via link |
| `/unshare` | Remove shared session |
| `/export` | Export conversation to markdown |
| `/editor` | Compose message in external `$EDITOR` |
| `/themes` | Switch UI theme |
| `/thinking` | Show / hide reasoning blocks (use ++ctrl+t++ to change the reasoning level) |
| `/details` | Toggle tool execution details |
| `/help` | Show help |
| `/exit` (`/quit`, `/q`) | Quit |

## Configuration

OpenCode uses JSON (or JSONC) config files, merged in this order (later overrides earlier):

1. Remote config (`.well-known/opencode`)
2. Global: `~/.config/opencode/opencode.json`
3. Custom: `$OPENCODE_CONFIG`
4. Project: `opencode.json` in project root

TUI-specific settings go in a separate `tui.json`.

### Example config

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "anthropic/claude-sonnet-5-5",
  "small_model": "anthropic/claude-haiku-5-5",
  "autoupdate": true,
  "provider": {
    "anthropic": {
      "options": {
        "timeout": 600000
      }
    }
  }
}
```

### TUI config

```json
{
  "$schema": "https://opencode.ai/tui.json",
  "theme": "tokyonight",
  "mouse": true,
  "scroll_speed": 3,
  "diff_style": "auto",
  "keybinds": {
    "leader": "ctrl+x"
  }
}
```

## Workflow: plan then build

```
# 1. Switch to Plan mode
<Tab>

# 2. Describe the feature
When a user deletes a note, flag it as deleted in the DB.
Create a screen showing recently deleted notes with restore/permanent delete.

# 3. Iterate on the plan
Use this design as reference. [drag & drop image]

# 4. Switch back to Build mode
<Tab>

# 5. Implement
Sounds good! Go ahead and make the changes.
```

## Custom commands

Define reusable prompts as commands in `opencode.json` or as markdown files in `.opencode/commands/`:

```json
{
  "command": {
    "test": {
      "template": "Run the full test suite with coverage. Show failures and suggest fixes.",
      "description": "Run tests with coverage",
      "agent": "build"
    }
  }
}
```

Then run with `/test` in the TUI. Commands support `$ARGUMENTS`, `$1`/`$2` positional params, file references with `@`, and shell output with `` !`command` ``.

## Tools available to the AI

### File & code

| Tool | Description |
|------|-------------|
| `read` | Read file contents (or a line range) |
| `write` | Create or overwrite files |
| `edit` | Replace exact text in a file |
| `apply_patch` | Apply a patch to the codebase |
| `glob` | Find files by pattern (sorted by modification time) |
| `grep` | Search file contents with regex |
| `lsp` | Definitions, references, hover via LSP (experimental) |

### Other

| Tool | Description |
|------|-------------|
| `bash` | Execute shell commands |
| `webfetch` | Fetch and read a web page |
| `websearch` | Search the web |
| `task` | Delegate a sub-task to a subagent |
| `skill` | Load a skill's `SKILL.md` |
| `todowrite` | Track a task list during the session |
| `question` | Ask you a question mid-task |

## Permissions

Each tool can be set to `allow`, `ask` or `deny`, globally or per agent, with glob patterns for commands:

```json
{
  "permission": {
    "edit": "ask",
    "bash": { "git push*": "ask", "rm -rf*": "deny", "*": "allow" },
    "webfetch": "allow"
  }
}
```

`opencode --auto` auto-approves everything not explicitly denied — sandboxes only.

## Skills

Skills are folders with a `SKILL.md` (frontmatter `name` matching the folder, plus `description`), loaded on demand through the `skill` tool. OpenCode discovers them in `.opencode/skills/`, `.agents/skills/` and `.claude/skills/` (project, walking up to the git root) and in `~/.config/opencode/skills/`, `~/.agents/skills/`, `~/.claude/skills/` (global) — so Claude Code skills work as-is.

## Non-interactive mode

Run a single prompt without the TUI:

```shell
$ opencode run "Explain the use of context in Go"

# Raw JSON events
$ opencode run --format json "Explain context in Go"

# Attach files, pick model / agent / reasoning variant
$ opencode run -f src/main.py -m anthropic/claude-opus-5-5 --variant high "Review this file"

# Continue the last session
$ opencode run -c "Now add tests"
```

### Other CLI commands

```shell
$ opencode serve               # Headless server (attach with `opencode attach <url>` or `run --attach`)
$ opencode web                 # Server + web UI
$ opencode pr 142              # Check out PR #142 and start opencode on it
$ opencode github install      # Set up the GitHub agent (runs in GitHub Actions)
$ opencode stats               # Token usage and cost
$ opencode models              # List available models
$ opencode mcp add             # Add an MCP server
$ opencode plugin <module>     # Install a plugin and update the config
$ opencode upgrade             # Self-update
```

## LSP support

OpenCode ships built-in LSP servers (some auto-installed; disable downloads with `OPENCODE_DISABLE_LSP_DOWNLOAD`). LSP is **disabled by default** — once enabled, a server starts when a matching file is opened. Add or disable servers under `lsp`:

```json
{
  "lsp": {
    "custom-lsp": {
      "command": ["custom-lsp-server", "--stdio"],
      "extensions": [".custom"]
    },
    "typescript": { "disabled": true }
  }
}
```

## MCP servers

OpenCode supports `local` (stdio) and `remote` (HTTP, with OAuth auto-detection) MCP servers:

```json
{
  "mcp": {
    "github": {
      "type": "remote",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer {env:GH_PAT}"
      }
    },
    "filesystem": {
      "type": "local",
      "command": ["npx", "-y", "@modelcontextprotocol/server-filesystem", "/projects"],
      "environment": { "MY_ENV_VAR": "value" },
      "enabled": true
    }
  }
}
```

Note that `command` is an **array**. Each server also accepts `timeout` (ms, default 5000); remote ones take an `oauth` object (or `false`).

## Custom instructions

OpenCode reads project instructions from `AGENTS.md` (walking up from the current directory) and global ones from `~/.config/opencode/AGENTS.md`. Generate the project file with `/init`.

For Claude Code compatibility it falls back to `CLAUDE.md` / `~/.claude/CLAUDE.md` when no `AGENTS.md` exists (disable with `OPENCODE_DISABLE_CLAUDE_CODE=1`). Extra files (paths, globs or URLs) can be added with the `instructions` config key:

```json
{ "instructions": ["CONTRIBUTING.md", "docs/guidelines/*.md"] }
```

## Copilot CLI vs OpenCode

| Feature | Copilot CLI | OpenCode |
|---------|-------------|----------|
| License | Proprietary | Open source (MIT) |
| Auth | GitHub subscription | API keys (any provider) |
| Multi-provider | GitHub models only | 75+ providers (Anthropic, OpenAI, Gemini, Groq, Bedrock, Azure…) |
| MCP | ✅ (`stdio`) | ✅ (`local`, `remote` + OAuth) |
| LSP | ✅ | ✅ |
| TUI | Minimal | Rich (OpenTUI), plus web UI and headless server |
| Desktop app | ❌ | ✅ (beta) |
| GitHub integration | Native (PRs, issues, search) | Via MCP |
| Session management | ✅ | ✅ |
| Plan mode | ✅ `/plan` | ✅ Plan agent (++tab++) |
| Fleet / parallel agents | ✅ `/fleet` | Subagents (`@general`, `task` tool) |
| Custom commands | ❌ | ✅ |
| Themes | ❌ | ✅ |
| Undo / redo file changes | `/rewind` | `/undo` `/redo` (git-based) |
