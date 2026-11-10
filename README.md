<!-- mcp-name: io.github.jusspound-netizen/context-bridge -->

# Context Bridge

[![Glama MCP Server](https://glama.ai/mcp/servers/jusspound-netizen/context-bridge/badge)](https://glama.ai/mcp/servers/jusspound-netizen/context-bridge)

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
| `get_jira_ticket` | Fetches a Jira ticket by issue key via the Jira REST API. | âœ… Implemented |
| `get_sentry_issues` | Lists unresolved Sentry issues by project slug. | âœ… Implemented |
| `get_github_actions_runs` | Checks CI/CD status for a repo. | âœ… Implemented |

**License:** MIT

## Related projects

- [ghost-tracer](https://github.com/jusspound-netizen/ghost-trace) — local-first observability for AI agents
- [ghost-reason](https://github.com/jusspound-netizen/ghost-reason) — trace your agent's reasoning
- [agent-cost-auditor](https://github.com/jusspound-netizen/agent-cost-auditor) — audit an agent's log for wasted tokens
- [Agensi storefront](https://agensi.io/creators/context-bridge) — ready-to-use AI skills for Jira, Sentry, and DevOps
