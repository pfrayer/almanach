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

## Plan mode

Plan mode lets you structure an implementation **before** writing any code. Models achieve higher success rates when following a concrete plan.

### Activate plan mode

- ++shift+tab++ to toggle between normal mode and plan mode
- Or use `/plan` directly from normal mode:

```
/plan Add OAuth2 authentication with Google and GitHub providers
```

### What happens

1. Copilot analyzes the request and the codebase
2. **Asks clarifying questions** to align on requirements
3. Creates a structured plan with checkboxes in `plan.md`
4. **Waits for your approval** before implementing

You can edit the plan with ++ctrl+y++ before starting implementation.

### Recommended workflow

```
# 1. Explore the existing code (read-only)
Read the authentication files but don't write code yet

# 2. Plan
/plan Implement password reset flow

# 3. Review and adjust the plan, then implement
Proceed with the plan

# 4. Verify
Run the tests and fix any failures

# 5. Commit
Commit these changes with a descriptive message
```

### When to use `/plan`

| Situation | `/plan` ? |
|-----------|-----------|
| Multi-file feature | ✅ |
| Refactoring with many touch points | ✅ |
| Complex new feature | ✅ |
| Quick bug fix | ❌ |
| Single file change | ❌ |

!!! tip "Rule of thumb"
    The bigger the task, the more useful the plan. For a one-liner, `/plan` is overkill.

## Fleet mode

Fleet mode lets Copilot break a complex task into subtasks **executed in parallel** by subagents. Each subagent has its own context window.

### Usage

Prefix your prompt with `/fleet`:

```
/fleet Refactor all API endpoints to use the new middleware, add tests for each
```

### How it works

1. The main agent analyzes the prompt and identifies independent subtasks
2. It orchestrates subagents, each working on its part in parallel
3. Results are gathered once all subagents are done

### When to use `/fleet`

| Situation | `/fleet` ? |
|-----------|-----------|
| Refactoring multiple independent files | ✅ |
| Creating test suites for multiple modules | ✅ |
| Multi-component migration | ✅ |
| Sequential task (each step depends on the previous one) | ❌ |

### Combining with plan + autopilot

The most powerful workflow for large tasks:

1. ++shift+tab++ → plan mode, create the implementation plan
2. Notice the plan has parallelizable elements
3. Select **Accept plan and build on autopilot + /fleet**

!!! warning "Premium request consumption"
    Each subagent interacts independently with the LLM. `/fleet` may therefore consume more premium requests than sequential processing. Check your quota with `/usage`.

### Choose model per subtask

By default subagents use a lightweight model. You can specify a model in the prompt:

```
/fleet Use Claude Opus 4.5 to analyze the auth module.
Use GPT-5.3-Codex to generate the migration scripts.
Use @test-writer to create unit tests.
```

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

Config at user level (`~/.copilot/lsp-config.json`) or repo level (`.github/lsp.json`). For instance for Python:

```shell
$ pip install python-lsp-server
```

```json
{
  "lspServers": {
    "python": {
      "command": "pylsp",
      "args": [],
      "fileExtensions": {
        ".py": "python"
      }
    }
  }
}
```

## Chronicle

!!! note "Experimental"
    `/chronicle` requires experimental mode. Enable it with `/experimental on` or `copilot --experimental`.

The `/chronicle` slash command leverages your local session history (stored in `~/.copilot/session-state/` and indexed in a SQLite session store) to generate insights about your work.

### Subcommands

| Subcommand | Description |
|------------|-------------|
| `/chronicle standup` | Generate a standup report from recent sessions |
| `/chronicle tips` | Get personalized tips based on your usage patterns |
| `/chronicle improve` | Suggest improvements for your custom instructions file |
| `/chronicle reindex` | Rebuild the session store index from session files |

### `/chronicle standup`

Generates a short report grouped by completion status, based on branches worked on, accomplishments, and linked PRs/issues. Defaults to the last 24 hours.

```
/chronicle standup
/chronicle standup for the last 3 days
```

Example output:

```text
Standup for March 13 2026:

✅ Done
  myapp-repo repo maintenance (main branch)
   - Synced local, cleaned files, audited deps, reviewed architecture

🚧 In Progress
  MyApp configuration (suppress-start-message branch)
   - Suppressing startup init prompt message
```

### `/chronicle tips`

Analyzes your recent sessions — prompts, tools used, features you haven't tried — and provides 3–5 personalized recommendations. You can focus on a specific area:

```
/chronicle tips
/chronicle tips for better prompting
```

### `/chronicle improve`

Deep-dives into your session history to find friction signals: repeated test failures, build errors, back-and-forth corrections. Generates targeted suggestions for your `.github/copilot-instructions.md` file.

```
/chronicle improve
```

After presenting recommendations, Copilot lets you toggle which ones to apply (arrow keys + space), then creates or updates the instructions file.

!!! tip "Scope"
    Unlike other chronicle subcommands, `improve` is scoped to the **current repository** only.

### Asking free-form questions

You don't need `/chronicle` for every history query. Copilot automatically searches the session store when you ask about past work:

```
Using what you know about my sessions, what type of tasks give me one-shot successes?
Based on my previous CLI sessions, how could I prompt you in a way that would cost less?
Have I worked on anything related to the payments API?
```

### Session data privacy

All session data stays on your local machine in `~/.copilot/session-state/`. Nothing is uploaded beyond normal AI model interactions. Delete a session by removing its directory, then run `/chronicle reindex`.

## Update

```shell
$ copilot
# then
/update
```
