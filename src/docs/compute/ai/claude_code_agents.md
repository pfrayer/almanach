---
description: "Claude Code multi-agent cheatsheet: subagents, agent teams (teammates), subagent vs teammate comparison, cross-session messaging and parallel git worktrees."
---

# Claude Code — agents & teammates

Delegating and parallelising work in [Claude Code](claude_code.md): subagents, agent teams and parallel sessions.

## Subagents

Subagents are specialised assistants with their own prompt, tools, and context window — useful for delegating focused tasks (code review, debugging, research) without polluting the main conversation. Define one as Markdown with YAML frontmatter (the `/agents` wizard is gone — ask Claude to create one, or edit `.claude/agents/` directly):

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

Built-in types include `Explore` (read-only codebase search), `Plan` (implementation planning) and `general-purpose`. A `fork` subagent inherits the full conversation and prompt cache instead of starting blank. In interactive sessions subagents run **in the background** by default: you keep working and get notified when they finish; Claude can resume one later with `SendMessage`.

## Subagents vs teammates (agent teams)

**Agent teams** (research preview) let several Claude instances collaborate as peers instead of one boss delegating to helpers. Enable them with:

```shell
$ export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

Each session then has one implicit team: you talk to the **lead**, which spawns **teammates** by giving the Agent tool a `name`. Teammates share a task list, message each other directly with `SendMessage`, and each shows up as its own pane or transcript (cycle with ++shift+down++).

| | Subagent | Teammate |
|---|----------|----------|
| Lifetime | One task, then returns a result | Long-lived, idles between tasks and can be re-tasked |
| Talks to | Only its caller (result comes back to the parent) | The lead **and** other teammates, by name (`name@team`) |
| Coordination | Parent orchestrates everything | Shared task list, teammates claim and complete tasks |
| Visibility | Summary in the main conversation | Own pane / transcript you can switch to and talk to directly |
| Context | Fresh context (or a `fork` of yours) | Own full context window per teammate |
| Model | `model` field of its definition | Lead's model unless the spawn names one |
| Cost | Cheap — only the result comes back | Token-intensive — N full sessions running in parallel |
| Good for | Search, review, isolated research | Parallel work that needs discussion: competing hypotheses while debugging, front/back/tests split, adversarial review |

Rule of thumb: if the workers only need to **report back**, use subagents; if they need to **talk to each other**, use a team.

```
Create an agent team to review PR #142: one teammate on security,
one on performance, one on test coverage. Have them challenge each
other's findings before reporting.
```

The `teammateMode` setting picks how teammates are displayed (`in-process` in the main terminal, or split panes with `tmux` / `iterm2`). Hook events `TeammateIdle`, `TaskCreated` and `TaskCompleted` let you enforce quality gates (e.g. exit `2` to send a teammate back to work).

!!! tip "Talking to other sessions"
    Beyond teams, any Claude Code sessions on your machines can message each other: `ListAgents` discovers them, `SendMessage` (or `@session-name` in the prompt) reaches them.

## Multi-agent with git worktrees

Run multiple independent Claude Code sessions in parallel using git worktrees. The built-in way:

```shell
$ claude -w feature-auth     # creates the worktree + branch and starts Claude in it
```

Or by hand:

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
