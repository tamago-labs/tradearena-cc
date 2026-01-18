"""
Custom views generation tools for TradeArena agents
"""

import asyncio
from datetime import datetime
from strands import tool

# Import views manager - we'll handle import error gracefully
try:
    from ..views_manager import views_manager
except ImportError:
    views_manager = None

@tool(
    name="create_custom_view",
    description="Create and save a custom HTML dashboard/view",
    inputSchema={
        "json": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The title of the custom view"
                },
                "html_content": {
                    "type": "string",
                    "description": "The HTML content for the view (can include CSS and JavaScript)"
                },
                "description": {
                    "type": "string",
                    "description": "Optional description of what the view shows"
                }
            },
            "required": ["title", "html_content"]
        }
    }
)
async def create_custom_view(title: str, html_content: str, description: str = "") -> str:
    """Create and save a custom HTML view.
    
    This tool allows agents to generate and save custom HTML dashboards or views.
    The view will be saved and can be accessed via a direct URL link.
    
    Args:
        title: The title for the view
        html_content: HTML content (can include inline CSS and JavaScript)
        description: Optional description of the view purpose
    
    Returns:
        Success message with direct URL to access the view
    """
    # Simulate async processing
    await asyncio.sleep(0.2)
    
    if views_manager is None:
        return "❌ Error: Views manager not available. Please check server configuration."
    
    try:
        # Create the view (without agent attribution)
        view_url = views_manager.create_view(
            title=title,
            html_content=html_content,
            description=description
        )
        
        # Return success message with clickable link
        full_url = f"http://127.0.0.1:8000{view_url}"
        return f"""✅ View created successfully!

📁 **Title:** {title}
🔗 **Access URL:** {full_url}

Click the link above to view your custom dashboard. The view will also appear in the main menu under "Views"."""
        
    except Exception as e:
        return f"❌ Error creating view: {str(e)}"

@tool(
    name="list_available_views",
    description="List all available custom views with their metadata",
    inputSchema={
        "json": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
)
async def list_available_views() -> str:
    """List all available custom views.
    
    Returns a list of all saved custom views with their metadata including
    creator agent, creation time, and access URLs.
    
    Returns:
        Formatted list of all available views
    """
    # Simulate async processing
    await asyncio.sleep(0.1)
    
    if views_manager is None:
        return "❌ Error: Views manager not available. Please check server configuration."
    
    try:
        all_views = views_manager.get_all_views()
        
        if not all_views:
            return "📋 No custom views available yet. Use the create_custom_view tool to create one!"
        
        result_lines = ["📋 **Available Custom Views:**\n"]
        
        for i, view in enumerate(all_views, 1):
            created_time = datetime.fromisoformat(view['created_at']).strftime("%Y-%m-%d %H:%M")
            view_url = f"http://127.0.0.1:8000/views/{view['filename']}"
            
            result_lines.append(f"{i}. **{view['title']}**")
            result_lines.append(f"   👤 Created by: {view['agent_name']}")
            result_lines.append(f"   🕒 Created: {created_time}")
            result_lines.append(f"   🔗 URL: {view_url}")
            if view.get('description'):
                result_lines.append(f"   📝 Description: {view['description']}")
            result_lines.append("")
        
        return "\n".join(result_lines)
        
    except Exception as e:
        return f"❌ Error listing views: {str(e)}"
