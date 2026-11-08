# Security

## Credentials

Context Bridge never stores credentials in the repository.

All credentials are read from environment variables at runtime:

| Variable | Used by | Purpose |
|---|---|---|
| JIRA_BASE_URL | get_jira_ticket | Your Jira instance URL |
| JIRA_EMAIL | get_jira_ticket | Your Jira account email |
| JIRA_API_TOKEN | get_jira_ticket | Jira API token (Basic Auth) |
| SENTRY_ORG_SLUG | get_sentry_issues | Sentry organization slug |
| SENTRY_AUTH_TOKEN | get_sentry_issues | Sentry auth token (Bearer) |
| GITHUB_PERSONAL_ACCESS_TOKEN | get_github_actions_runs | GitHub PAT (Bearer) |

Set them in your agent's environment before connecting the MCP server.

PowerShell:
$env:JIRA_BASE_URL = "https://yourcompany.atlassian.net"
$env:JIRA_EMAIL = "you@example.com"
$env:JIRA_API_TOKEN = "your-token"

Bash:
export JIRA_BASE_URL="https://yourcompany.atlassian.net"
export JIRA_EMAIL="you@example.com"
export JIRA_API_TOKEN="your-token"

## What the server does with credentials

- Reads them from os.environ at call time
- Uses them only for the outbound API request
- Never logs them
- Never returns them in tool output
- Never writes them to disk

## Reporting a vulnerability

Open an issue at https://github.com/jusspound-netizen/context-bridge/issues
