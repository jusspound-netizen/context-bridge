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
@mcp.tool(description="Retrieves recent GitHub Actions workflow runs for a repository.")
async def get_github_actions_runs(owner: str, repo: str, limit: int = 5) -> str:
    """Returns recent CI runs for a repo."""
    import asyncio, json as _j, os as _os
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError, URLError

    token = _os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")
    if not token:
        return _j.dumps({"error": "GITHUB_PERSONAL_ACCESS_TOKEN not set."})

    url = f"https://api.github.com/repos/{owner}/{repo}/actions/runs?per_page={limit}"

    def _fetch():
        req = Request(url, headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "context-bridge"
        })
        try:
            with urlopen(req, timeout=15) as resp:
                data = _j.loads(resp.read().decode())
                runs = data.get("workflow_runs", [])
                simplified = [
                    {"name": r.get("name"), "status": r.get("status"), "conclusion": r.get("conclusion"),
                     "branch": r.get("head_branch"), "url": r.get("html_url")}
                    for r in runs[:limit]
                ]
                return _j.dumps(simplified, indent=2)
        except HTTPError as e:
            return _j.dumps({"error": f"GitHub HTTP {e.code}", "details": str(e.read().decode("utf-8"))[:200]})
        except URLError as e:
            return _j.dumps({"error": f"GitHub URL error: {e.reason}"})
        except Exception as e:
            return _j.dumps({"error": f"GitHub error: {type(e).__name__}: {str(e)}"})

    return await asyncio.to_thread(_fetch)

if __name__ == "__main__":
    mcp.run()
