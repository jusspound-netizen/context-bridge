from mcp.server.mcpserver import MCPServer
import json
import os
import urllib.request
import urllib.parse
import base64

mcp = MCPServer("context-bridge")

# ===== JIRA CONNECTOR =====
@mcp.tool(description="Retrieves a Jira ticket based on a ticket ID using the Jira REST API.")
async def get_jira_ticket(ticket_id: str) -> str:
    """Returns real JSON data for a given ticket ID from Jira."""
    import asyncio
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError, URLError
    import base64, json as _j

    base = os.environ.get("JIRA_BASE_URL")
    email = os.environ.get("JIRA_EMAIL")
    token = os.environ.get("JIRA_API_TOKEN")
    if not all([base, email, token]):
        return _j.dumps({"error": "Jira credentials not set."})

    url = f"{base}/rest/api/3/issue/{ticket_id}"
    creds = base64.b64encode(f"{email}:{token}".encode()).decode()

    def _fetch():
        req = Request(url, headers={"Authorization": f"Basic {creds}", "Accept": "application/json"})
        try:
            with urlopen(req, timeout=15) as resp:
                return resp.read().decode("utf-8")
        except HTTPError as e:
            return _j.dumps({"error": f"Jira HTTP {e.code}", "details": str(e.read().decode("utf-8"))[:200]})
        except URLError as e:
            return _j.dumps({"error": f"Jira URL error: {e.reason}"})
        except Exception as e:
            return _j.dumps({"error": f"Jira error: {type(e).__name__}: {str(e)}"})

    return await asyncio.to_thread(_fetch)
# ===== SENTRY CONNECTOR =====
if __name__ == "__main__":
    mcp.run()
