from mcp.server.mcpserver import MCPServer
import json
import os
import urllib.request
import urllib.parse

# Initialize FastMCP
mcp = MCPServer("context-bridge")

# Environment variables expected: JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN

# Define the get_jira_ticket tool
@mcp.tool(description="Retrieves a Jira ticket based on a ticket ID using the Jira REST API.")
def get_jira_ticket(ticket_id: str) -> str:
    """Returns real JSON data for a given ticket ID from Jira."""
    
    jira_base_url = os.environ.get("JIRA_BASE_URL")
    jira_email = os.environ.get("JIRA_EMAIL")
    jira_api_token = os.environ.get("JIRA_API_TOKEN")

    if not all([jira_base_url, jira_email, jira_api_token]):
        return json.dumps({"error": "Jira credentials (JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN) not set in environment variables."})

    url = f"{jira_base_url}/rest/api/3/issue/{ticket_id}"
    
    # Basic Auth setup
    import base64
    credentials = base64.b64encode(f"{jira_email}:{jira_api_token}".encode()).decode()
    auth = urllib.request.build_opener(urllib.request.HTTPHandler)
    auth.addheaders = [('Authorization', f'Basic {credentials}')]

    try:
        with urllib.request.urlopen(url, timeout=15, opener=auth) as response:
            if response.getcode() == 200:
                data = response.read().decode('utf-8')
                return data
            else:
                # Handle non-200 responses from Jira API
                error_data = response.read().decode('utf-8')
                return json.dumps({"error": f"Jira API returned status code {response.getcode()}", "details": error_data})
    except urllib.error.HTTPError as e:
        return json.dumps({"error": f"HTTP Error accessing Jira: {e.code}", "details": str(e.read().decode('utf-8'))})
    except urllib.error.URLError as e:
        return json.dumps({"error": f"URL Error accessing Jira: {e.reason}"})
    except Exception as e:
        return json.dumps({"error": f"An unexpected error occurred: {str(e)}"})

# Run the MCP server (this will block execution)
if __name__ == "__main__":
    print("Starting MCP server...")
    # In a real scenario, you might configure host/port. For this task, we just run it.
    mcp.run()