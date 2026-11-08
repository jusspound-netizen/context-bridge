# Context Bridge

**Context Bridge - one MCP endpoint for all your dev tools**

**Problem:**
* Tool sprawl across Jira, Sentry, GitHub, and CI systems.
* Context fragmentation makes it hard for AI agents to operate across tools.
* AI agents are currently blind to critical development context (Jira tickets, Sentry alerts, CI status).

**Setup:**
1. `pip install -r requirements.txt` (or necessary dependencies)
2. Set required environment variables (e.g., API keys for Jira/Sentry).
3. Add the running MCP server endpoint to your AI environment (e.g., Claude Code or Cursor) as a custom MCP server.

## Quick Start
To run the server:
1. `python server.py`
2. Ensure required environment variables are set.

## Example
A sample response from `get_jira_ticket`:
{"id": "PROJ-123", "summary": "Fix login bug", "status": "In Progress"}

**Tools:**
| Tool Name | Description | Status |
| :--- | :--- | :--- |
| `get_jira_ticket` | Retrieves mock Jira ticket data by ID. | ✅ Implemented |
| `get_sentry_alert` | Retrieves Sentry alerts. | ⏳ Planned |
| `get_github_actions_status` | Checks CI/CD status for a repo. | ⏳ Planned |
| `send_slack_notification` | Sends status updates to Slack. | ⏳ Planned |

**License:** MIT
