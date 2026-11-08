from mcp.server.mcpserver import MCPServer
import json
import os
import urllib.request
import urllib.parse
import base64

mcp = MCPServer("context-bridge")

# ===== JIRA CONNECTOR =====
@mcp.tool(description="Retrieves a Jira ticket based on a ticket ID using the Jira REST API.")
def get_jira_ticket(ticket_id: str) -> str:
    """Returns real JSON data for a given ticket ID from Jira."""
    jira_base_url = os.environ.get("JIRA_BASE_URL")
    jira_email = os.environ.get("JIRA_EMAIL")
    jira_api_token = os.environ.get("JIRA_API_TOKEN")
    if not all([jira_base_url, jira_email, jira_api_token]):
        return json.dumps({"error": "Jira credentials not set."})
    url = f"{jira_base_url}/rest/api/3/issue/{ticket_id}"
    credentials = base64.b64encode(f"{jira_email}:{jira_api_token}".encode()).decode()
    auth = urllib.request.build_opener(urllib.request.HTTPHandler)
    auth.addheaders = [("Authorization", f"Basic {credentials}")]
    try:
        with urllib.request.urlopen(url, timeout=15, opener=auth) as response:
            return response.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        return json.dumps({"error": f"Jira HTTP {e.code}", "details": str(e.read().decode("utf-8"))[:200]})
    except Exception as e:
        return json.dumps({"error": str(e)})

# ===== SENTRY CONNECTOR =====
if __name__ == "__main__":
    mcp.run()
