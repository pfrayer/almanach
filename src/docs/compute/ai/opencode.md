---
description: "OpenCode cheatsheet: install, agents, slash commands, the plan-then-build workflow, MCP servers, LSP and custom commands."
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
| **Plan** | Read-only agent for analysis and code exploration (edits denied by default) |

### Subagents

Invoked automatically or via `@mention` in messages.

| Agent | Description |
|-------|-------------|
| **General** | Full-access agent for complex searches and multi-step tasks |
| **Explore** | Fast, read-only agent for codebase exploration |

### Custom agents

Define custom agents in `opencode.json` or as markdown files in `.opencode/agents/` (project) or `~/.config/opencode/agents/` (global):

```json
{
  "agent": {
    "code-reviewer": {
      "description": "Reviews code for best practices",
      "mode": "subagent",
      "model": "anthropic/claude-sonnet-4-5",
      "tools": { "write": false, "edit": false }
    }
  }
}
```

## Keyboard shortcuts

OpenCode uses a **leader key** (default: ++ctrl+x++) for most shortcuts. Press the leader, then the action key.

| Shortcut | Action |
|----------|--------|
| ++ctrl+c++ | Quit |
| ++ctrl+x++ `n` | New session |
| ++ctrl+x++ `l` | List / switch sessions |
| ++ctrl+x++ `m` | Select model |
| ++ctrl+x++ `e` | Open external editor |
| ++ctrl+x++ `u` | Undo last message + file changes |
| ++ctrl+x++ `r` | Redo |
| ++ctrl+x++ `c` | Compact (summarize) session |
| ++ctrl+x++ `s` | Share session |
| ++ctrl+x++ `b` | Toggle sidebar |
| ++ctrl+x++ `h` | Help |
| ++tab++ | Cycle agents (Build ↔ Plan) |
| ++escape++ | Cancel / close overlay |
| `@` | Reference files (fuzzy search) |
| `!` | Run shell command directly |

## Slash commands

| Command | Description |
|---------|-------------|
| `/connect` | Add a provider |
| `/models` | List / select model |
| `/init` | Generate `AGENTS.md` for the project |
| `/new` | Start a new session |
| `/sessions` | List and switch sessions |
| `/undo` | Undo last message and revert file changes |
| `/redo` | Redo a previously undone message |
| `/compact` | Summarize conversation to reduce context |
| `/share` | Share session via link |
| `/unshare` | Remove shared session |
| `/export` | Export conversation to markdown |
| `/editor` | Compose message in external `$EDITOR` |
| `/themes` | Switch UI theme |
| `/thinking` | Toggle model reasoning visibility |
| `/help` | Show help |
| `/exit` | Quit |

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
  "model": "anthropic/claude-sonnet-4-5",
  "small_model": "anthropic/claude-haiku-4-5",
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
| `glob` | Find files by pattern |
| `grep` | Search file contents |
| `ls` | List directory contents |
| `view` | View file contents |
| `write` | Write to files |
| `edit` | Edit files |
| `patch` | Apply diffs to files |
| `diagnostics` | Get LSP diagnostics |

### Other

| Tool | Description |
|------|-------------|
| `bash` | Execute shell commands |
| `fetch` | Fetch data from URLs |
| `sourcegraph` | Search code across public repos |
| `agent` | Delegate sub-tasks to a subagent |

## Non-interactive mode

Run a single prompt without the TUI:

```shell
$ opencode run "Explain the use of context in Go"

# JSON output
$ opencode run "Explain context in Go" -f json

# Quiet (no spinner)
$ opencode run "Explain context in Go" -q
```

## LSP support

OpenCode uses LSP for code intelligence. Install the server for your language, then configure:

```json
{
  "lsp": {
    "python": { "command": "pylsp" },
    "go": { "command": "gopls" },
    "typescript": {
      "command": "typescript-language-server",
      "args": ["--stdio"]
    }
  }
}
```

## MCP servers

OpenCode supports MCP via `stdio`, `http`, and `sse` transports:

```json
{
  "mcp": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer $GH_PAT"
      }
    },
    "filesystem": {
      "type": "stdio",
      "command": "node",
      "args": ["/path/to/mcp-server.js"]
    }
  }
}
```

## Custom instructions

OpenCode reads project instructions from `AGENTS.md` at the project root. Generate it with `/init`.

You can also provide global instructions at `~/.config/opencode/agents/`.

## Copilot CLI vs OpenCode

| Feature | Copilot CLI | OpenCode |
|---------|-------------|----------|
| License | Proprietary | Open source (MIT) |
| Auth | GitHub subscription | API keys (any provider) |
| Multi-provider | GitHub models only | 75+ providers (Anthropic, OpenAI, Gemini, Groq, Bedrock, Azure…) |
| MCP | ✅ (`stdio`) | ✅ (`stdio`, `http`, `sse`) |
| LSP | ✅ | ✅ |
| TUI | Minimal | Rich (Bubble Tea) |
| Desktop app | ❌ | ✅ (beta) |
| GitHub integration | Native (PRs, issues, search) | Via MCP |
| Session management | ✅ | ✅ |
| Plan mode | ✅ `/plan` | ✅ Plan agent (++tab++) |
| Fleet / parallel agents | ✅ `/fleet` | ❌ |
| Custom commands | ❌ | ✅ |
| Themes | ❌ | ✅ |
| Undo / redo file changes | `/rewind` | `/undo` `/redo` (git-based) |
