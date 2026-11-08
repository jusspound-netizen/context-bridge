from mcp.server.fastmcp import FastMCP
import json

# Initialize FastMCP
mcp = FastMCP()

# Define the get_jira_ticket tool
@mcp.tool(description="Retrieves a mock Jira ticket based on a ticket ID.")
def get_jira_ticket(ticket_id: str) -> str:
    """Returns mock JSON data for a given ticket ID."""
    if ticket_id == "JIRA-123":
        mock_data = {
            "id": "JIRA-123",
            "summary": "Implement MCP server skeleton",
            "status": "In Progress",
            "assignee": "jusspound-netizen",
            "priority": "High"
        }
        return json.dumps(mock_data)
    else:
        return json.dumps({"error": "Ticket not found", "id": ticket_id})

# Run the MCP server (this will block execution)
if __name__ == "__main__":
    print("Starting FastMCP server...")
    # In a real scenario, you might configure host/port. For this task, we just run it.
    mcp.run()