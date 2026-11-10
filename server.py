from mcp.server.mcpserver import MCPServer
import json
import os
import urllib.request
import urllib.parse
import base64

mcp = MCPServer("context-bridge")

# ===== JIRA CONNECTOR =====
@mcp.tool(description="Retrieves a Jira ticket by its issue key (e.g. 'PROJ-123'). Returns JSON with id, summary, status, assignee, and description fields. Requires JIRA_BASE_URL, JIRA_EMAIL, and JIRA_API_TOKEN environment variables.")
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
@mcp.tool(description="Lists recent GitHub Actions workflow runs for a repository (owner/repo). Returns JSON array with run id, name, status, conclusion, head_branch, and html_url. Optional limit (default 5). Requires GITHUB_PERSONAL_ACCESS_TOKEN with actions:read scope.")
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

@mcp.tool(description="Lists recent unresolved issues from a Sentry project by project slug. Returns JSON array with issue id, title, culprit, count, and first_seen. Optional limit (default 5). Requires SENTRY_ORG_SLUG and SENTRY_AUTH_TOKEN environment variables.")
async def get_sentry_issues(project_slug: str, limit: int = 5) -> str:
    """Returns recent unresolved issues for a Sentry project."""
    import asyncio, json as _j, os as _os
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError, URLError
    org = _os.environ.get("SENTRY_ORG_SLUG")
    token = _os.environ.get("SENTRY_AUTH_TOKEN")
    if not all([org, token]):
        return _j.dumps({"error": "SENTRY_ORG_SLUG and SENTRY_AUTH_TOKEN must be set."})
    url = f"https://sentry.io/api/0/projects/{org}/{project_slug}/issues/?query=is:unresolved&limit={limit}"
    def _fetch():
        req = Request(url, headers={"Authorization": f"Bearer {token}", "Accept": "application/json"})
        try:
            with urlopen(req, timeout=15) as resp:
                data = _j.loads(resp.read().decode())
                return _j.dumps([{"title": i.get("title"), "id": i.get("id"), "status": i.get("status"), "count": i.get("count")} for i in data], indent=2)
        except HTTPError as e:
            return _j.dumps({"error": f"Sentry HTTP {e.code}", "details": str(e.read().decode("utf-8"))[:200]})
        except URLError as e:
            return _j.dumps({"error": f"Sentry URL error: {e.reason}"})
        except Exception as e:
            return _j.dumps({"error": f"Sentry error: {type(e).__name__}: {str(e)}"})
    return await asyncio.to_thread(_fetch)

if __name__ == "__main__":
    mcp.run()


def main():
    mcp.run()

if __name__ == "__main__":
    main()
