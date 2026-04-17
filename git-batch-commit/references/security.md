# Security & Boundaries

## Sensitive File List

The following files in staged changes must **immediately stop** and prompt user to handle manually:

- `.env` (and variants `.env.local`, `.env.production`, etc.)
- `*.pem`, `*.key` (private key files)
- `credentials*.json`
- `id_rsa*`
- `.npmrc` (may contain tokens)
- `secrets.*`
- `*.p12`, `*.pfx` (certificates)
- `aws_*.json` (AWS credentials)
- `gcp-*.json` (GCP credentials)
- `azure-*.json`
- Any file with `secret`, `private`, `credential` in filename

## Mandatory Rules (NEVER)

- **NEVER** commit sensitive files
- **NEVER** use `--no-verify`
- **NEVER** use `git commit --amend` unless user explicitly requests
- **NEVER** use `push --force`
- If hook fails, analyze the failure reason first, then fix and create **new commit**

## Pre-Check Items

Must verify before execution:
1. Staged changes exist
2. No sensitive files present
3. No binary artifacts, build outputs, log files, cache files
4. No same file exists in both staged and unstaged (avoid workflow accidentally affecting working tree state)

## Low-Confidence Grouping

If unable to determine grouping with 100% confidence: show the plan to user first, **do not commit directly**.