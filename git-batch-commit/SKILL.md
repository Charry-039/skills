---
name: git-batch-commit
description: "Automatically organize staged Git changes into unit-level, intent-based commits with gitmoji-style messages in English. Ideal when a single git add mixes multiple change types (eslint/deps/swagger/dto/styles/business) and you want clean, intent-based commits. Groups by intent rather than directory. Cross-platform on Windows/Linux/macOS."
license: MIT
---

# Git-Batch-Commit

This skill analyzes staged Git changes, groups them by intent, and produces clean, reviewable commit plans and messages. It prioritizes safety checks and explicit user confirmation before any commit execution.


IRON LAW: NEVER commit when confidence is low or sensitive files detected - suggest first, commit second.

## Anti-Patterns to Avoid

**This is the most important section - read before every run.**

- **DO NOT** blindly commit without showing the grouping plan first (unless user said "commit now")
- **DO NOT** mix unrelated intent into one commit (e.g., deps + business logic together)
- **DO NOT** skip the sensitive file check - `.env`, `*.pem`, `credentials*` must stop the process
- **DO NOT** use `--no-verify` or `git commit --amend` unless user explicitly asks
- **DO NOT** use `push --force`
- **DO NOT** commit binary artifacts, build outputs, or log files
- **DO NOT** group files only by directory - group by intent (a config change in the same dir as business logic is not the same commit)
- **DO NOT** skip unstaged file check - if the same file is both staged and unstaged, warn before proceeding
- **DO NOT** guess intent without reading the diff - look at `git diff --cached` patch content before labeling a group

## Workflow

### Step 0: Determine Mode (REQUIRED)

Ask: What mode did the user request?

| User said | Mode |
|---|---|
| "organize/split/batch my staged changes" (no "commit now") | **Suggestion mode** (default) |
| "split and commit now" / "no confirmation" | **Execution mode** |
| "group only" / "draft commit messages" | **Suggestion-only mode** |
| "preview" / "dry run" / "show me what would happen" | **Dry-run mode** |

Do NOT proceed until the mode is clear.

### Step 1: Pre-Check (BLOCKING)

WARNING - Run this before analyzing anything:

```bash
python3 scripts/check-staged.py
```

This script checks:
- Staged files exist
- No sensitive files (`.env`, `*.pem`, `credentials*`, etc.)
- No binary artifacts or build outputs
- No file is both staged and unstaged
- Branch state (unpushed commits, upstream tracking)

**If sensitive files found -> STOP. Tell the user which files and ask them to handle manually.**

**If no staged changes -> STOP. Tell the user the staging area is empty.**

**If staged + unstaged same-file conflict -> default to suggestion mode only and warn the user.**

**If there are unpushed commits on the current branch:**
- Warn: "This branch has N unpushed commits. A reset will rewrite history. Continue?"
- Do NOT auto-proceed - require user acknowledgment before Step 5.

**Cross-platform:** script works on Windows / Linux / macOS (Python 3 required).

### Step 2: Analyze Groups

REQUIRED - Read the actual diff content before labeling.

Load `references/grouping-rules.md` for detailed grouping strategy.

Ask these questions for each staged file:

1. **What is the intent?** (new feature, bug fix, config, deps, style, docs)
2. **Does this correlate with other files?** (controller + service + dto = same intent)
3. **Is this a high-confidence independent group?** (eslint config, package.json, style system = yes, almost always independent)
4. **Should this be grouped with something else, or stand alone?**

High-confidence independent groups:
- `eslint.config.js`, `.eslintrc*`, `tsconfig*`, `nest-cli.json` -> `chore(eslint)`
- `package.json` + lockfile (deps only) -> `build(deps)`
- `tailwind.config.*`, `*.theme.css`, `token*.css` -> `style(styles)`
- `swagger`, `openapi`, `*response.dto.ts`, `*pagination.dto.ts` -> `feat(api)` or `build(deps)`
- `*.spec.ts`, `test/**/*.ts` alongside source -> same intent as the source

Group scope priority: `auth`, `tasks`, `votes`, `summaries`, `discussions`, `companions`, `users`, `api`, `eslint`, `deps`, `build`, `styles`

### Step 3: Generate Commit Messages

Load `references/commit-types.md` for the type/gitmoji mapping and format rules.

Generate one message per group using format: `:gitmoji: type(scope): English description`

Rules:
- English language
- Describe the intent, not the files changed
- Scope from the priority list above
- If unsure about scope, use a broader category (`api`, `build`)

### Step 4: Present Plan + Gate (REQUIRED)

Present the plan in this format:

```markdown
I identified N suggested commits:

1. `<commit message>`
   - Files: ...
   - Reason: ...
   - Confidence: high/medium

2. ...

Confirm and I will commit in this order.
```

#### Medium-Confidence Groups - MUST resolve before proceeding

Ask the user explicitly for each medium-confidence group:

> **About group X (confidence: medium):**
> Files: ...
> Reason: ...
>
> Choose:
> A. Keep as a separate commit
> B. Merge into the previous/next group
> C. Split into other groups
> D. Cancel this group (do not commit now)

**Do NOT proceed to Step 5 until all medium-confidence groups have explicit user resolution.**

Overall gate question: **Proceed with this plan (all medium-confidence groups resolved), or adjust?**

### Step 5: Execute Commits (only in execution mode)

After user confirms AND all medium-confidence groups are resolved:

**5a. Re-verify staged state** - run `git diff --cached --name-only` to confirm no new changes were added since Step 1.

**5b. Generate manifest file** `.git-batch-manifest.json`:

```json
{
  "commits": [
    {
      "message": ":sparkles: feat(api): add tasks module",
      "files": ["src/tasks/*.ts", "src/dto/task*.ts"]
    },
    {
      "message": ":wrench: chore(eslint): update ESLint config",
      "files": ["eslint.config.js", "package.json"]
    }
  ]
}
```

Write this to `.git-batch-manifest.json` in the repo root.

**5c. Offer dry-run before committing:**

Ask: **"Before executing, do you want a dry-run preview?"**

If yes:

```bash
python3 scripts/batch-commit.py --dry-run
```

Dry-run shows:
- The concrete file list per commit (after glob expansion)
- The git commands that would run
- Manifest is kept for later execution or adjustment

**5d. Execute:**

```bash
# Default: stop on failure, do not rollback
python3 scripts/batch-commit.py

# Optional: rollback all successful commits on failure
python3 scripts/batch-commit.py --rollback-on-fail
```

**Rollback behavior:**
- Before any commit, saves current HEAD
- If any commit fails, prompts whether to rollback
- With `--rollback-on-fail`: automatically rolls back to saved HEAD
- Successful commits are NOT automatically rolled back - user must choose

**If any commit fails:**
- STOP further commits
- Report which commit failed and why
- Report how many succeeded before failure
- Ask: "Rollback the successful commits?"

### Hook failure handling strategy

When `git commit` returns non-zero and stderr includes hook keywords:

| stderr keyword | Likely cause | Handling |
|---|---|---|
| `pre-commit` | lint/format checks failed | Explain which rule failed and how to fix, then re-run |
| `commit-msg` | commit message format invalid | Show required format, generate corrected message, re-commit |
| `post-commit` | non-critical hook failure | Warn user: commit succeeded but post-hook failed |
| `lint` / `eslint` / `prettier` | code checks failed | List failing files and rules, suggest fix commands |

**Handling flow:**

1. Parse stderr and identify hook type
2. If `commit-msg`: generate corrected message, ask user to confirm, re-commit
3. If `pre-commit` (lint/format): explain failure and fix commands, do not auto-rollback
4. If `post-commit`: commit succeeded, warn user only
5. If unrecognized: stop and report error text, ask user to handle manually

**Do not:**
- Do not use `--no-verify` to bypass hooks
- Do not rollback without analyzing the cause

### Step 6: Summary

After execution (or after presenting plan in suggestion mode):
- How many commits created
- Each commit message + short hash
- Any remaining staged/unstaged files and why they were not included

**Offer PR summary generation:**

After all commits succeed, ask: **"Do you want a PR title, description, or CHANGELOG entry?"**

If yes, generate from commit messages:

```markdown
## PR Title
feat(api): add response DTOs and Swagger docs

## PR Description
### Change Summary
- `:sparkles: feat(api): add response DTOs and Swagger docs`
- `:wrench: chore(eslint): update ESLint config and fix rule conflicts`

### Change Details
(Briefly explain each commit intent based on the messages)

### Testing Suggestions
(Based on changed files: DTO updates -> verify API response format; ESLint changes -> run lint)
```

**CHANGELOG entry generation:**

If the user asks for CHANGELOG:

```markdown
## Changelog

### [Unreleased]
#### Features
- Add response DTOs and Swagger docs
#### Chores
- Update ESLint config and fix rule conflicts
```

Rules for CHANGELOG:
- Group by conventional type: `Features`, `Bug Fixes`, `Chores`, `Refactors`, `Docs`
- Strip gitmoji and scope from commit message for readability
- Use `### [Unreleased]` section or append with today's date
- Title: use the most significant commit message (prefer `feat` > `fix` > others)
- Description: list all commit messages grouped by type
- Add "Testing Suggestions" based on files changed (not generic advice)

### Undo Last Batch

If the user says "undo last batch" / "undo" after a batch commit:

Ask: **How many commits do you want to undo?** (defaults to all in the last batch)

```bash
python3 scripts/batch-undo.py
```

The script:
- Shows the last batch's commits (from manifest) or asks for count
- Uses `git reset --soft HEAD~N` to undo (files return to staged state, not lost)
- Cleans up manifest file
- Defaults to interactive confirmation; use `--all` to skip confirmation

**Do NOT use `git reset --hard` for undo - that would discard changes.**

## Output Templates

### Suggestion mode output
```markdown
I identified N suggested commits:

1. `<msg>`
   - Files: ...
   - Reason: ...
   - Confidence: high/medium

2. ...

Confirm and I will commit in this order.
```

### Execution mode output
```markdown
Completed batch commits. Created N commits:

1. `<msg1>` (abc1234)
2. `<msg2>` (def5678)

If you want, I can:
- Check for remaining staged/unstaged changes
- Generate a PR summary / title
```