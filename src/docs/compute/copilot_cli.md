# GitHub Copilot CLI

AI-powered coding assistant in the terminal. Uses the same agentic engine as GitHub's Copilot coding agent.

[Official docs](https://docs.github.com/copilot/concepts/agents/about-copilot-cli){target=_blank}

## Install

```shell
# macOS & Linux
$ curl -fsSL https://gh.io/copilot-install | bash

# Homebrew
$ brew install copilot-cli

# npm
$ npm install -g @github/copilot

# Windows (WinGet)
$ winget install GitHub.Copilot
```

Install a specific version to a custom path:

```shell
$ curl -fsSL https://gh.io/copilot-install | VERSION="v0.0.369" PREFIX="$HOME/custom" bash
```

## Launch & authenticate

```shell
$ copilot
```

On first launch, use `/login` to authenticate with GitHub. You need an active Copilot subscription.

You can also authenticate via a fine-grained PAT with the "Copilot Requests" permission, exported as `GH_TOKEN` or `GITHUB_TOKEN`.

## Keyboard shortcuts

| Shortcut | Action |
|----------|--------|
| ++shift+tab++ | Cycle modes (interactive → plan) |
| ++ctrl+s++ | Run command while preserving input |
| ++ctrl+t++ | Toggle model reasoning display |
| ++ctrl+c++ | Cancel / clear input / copy selection |
| ++ctrl+c++ ×2 | Exit the CLI |
| ++ctrl+d++ | Shutdown |
| ++ctrl+l++ | Clear screen |
| ++ctrl+g++ | Edit prompt in external editor |
| ++up++ ++down++ | Navigate command history |
| `@` | Mention files, include contents in context |
| `!` | Execute command in your local shell (bypass Copilot) |

## Slash commands

### Session

| Command | Description |
|---------|-------------|
| `/model` | Select AI model |
| `/diff` | Review changes in current directory |
| `/compact` | Summarize history to reduce context usage |
| `/context` | Show token usage |
| `/rewind` | Rewind last turn, revert file changes |
| `/resume` | Switch to a different session |
| `/share` | Export session to markdown or GitHub gist |
| `/clear` | Clear conversation history |

### Code & GitHub

| Command | Description |
|---------|-------------|
| `/pr` | Operate on pull requests for current branch |
| `/review` | Run code review agent |
| `/delegate` | Send session to GitHub to create a PR |
| `/research` | Deep research using GitHub search & web |
| `/plan` | Create an implementation plan before coding |
| `/ide` | Connect to an IDE workspace |

### Config

| Command | Description |
|---------|-------------|
| `/init` | Initialize Copilot instructions for the repo |
| `/mcp` | Manage MCP server configuration |
| `/lsp` | Manage language server configuration |
| `/allow-all` | Enable all permissions (tools, paths, URLs) |
| `/add-dir` | Add a directory to the allowed list |
| `/experimental` | Toggle experimental features |

## Custom instructions

Copilot reads instructions from these files (in order):

- `CLAUDE.md`, `GEMINI.md`, `AGENTS.md` (in git root & cwd)
- `.github/instructions/**/*.instructions.md`
- `.github/copilot-instructions.md`
- `$HOME/.copilot/copilot-instructions.md`

## MCP servers

Copilot ships with GitHub's MCP server by default. Add custom MCP servers via `/mcp` or by editing the config directly.

## LSP support

Copilot CLI supports Language Server Protocol for code intelligence (go-to-definition, hover, diagnostics). Servers are not bundled — install them separately.

Config at user level (`~/.copilot/lsp-config.json`) or repo level (`.github/lsp.json`):

```json
{
  "lspServers": {
    "typescript": {
      "command": "typescript-language-server",
      "args": ["--stdio"],
      "fileExtensions": {
        ".ts": "typescript",
        ".tsx": "typescript"
      }
    }
  }
}
```

## Update

```shell
$ copilot
# then
/update
```
