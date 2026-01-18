"""
Views Manager for TradeArena
Handles file-based storage and retrieval of custom HTML views
"""

import os
import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

class ViewsManager:
    """Manages custom HTML views with flat file structure"""
    
    def __init__(self, views_dir: str = "views"):
        self.views_dir = Path(views_dir)
        self.views_dir.mkdir(exist_ok=True)
        self.index_file = self.views_dir / "index.json"
        
    def _sanitize_filename(self, title: str) -> str:
        """Sanitize title for safe filename"""
        # Remove special characters, replace spaces with underscores
        sanitized = re.sub(r'[^\w\s-]', '', title)
        sanitized = re.sub(r'[-\s]+', '_', sanitized)
        return sanitized.strip('_')
    
    def _get_timestamp(self) -> str:
        """Get current timestamp for filename"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def _load_index(self) -> Dict[str, Any]:
        """Load views index from JSON file"""
        if not self.index_file.exists():
            return {"views": []}
        
        try:
            with open(self.index_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {"views": []}
    
    def _save_index(self, index_data: Dict[str, Any]) -> None:
        """Save views index to JSON file"""
        try:
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(index_data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            raise Exception(f"Failed to save views index: {e}")
    
    def create_view(self, title: str, html_content: str, description: str = "") -> str:
        """
        Create a new HTML view
        
        Args:
            title: View title
            html_content: HTML content for view
            description: Optional description
        
        Returns:
            URL path to access the view
        """
        # Generate filename
        sanitized_title = self._sanitize_filename(title)
        timestamp = self._get_timestamp()
        filename = f"{sanitized_title}_{timestamp}.html"
        filepath = self.views_dir / filename
        
        # Create HTML content with metadata header
        html_with_metadata = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="generator" content="TradeArena Custom View">
    <meta name="created-at" content="{datetime.now().isoformat()}">
    <meta name="description" content="{description}">
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }}
        .header {{
            background: #2c3e50;
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .title {{
            font-size: 1.5em;
            font-weight: bold;
        }}
        .meta {{
            font-size: 0.9em;
            opacity: 0.8;
        }}
        .content {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="title">{title}</div>
        <div class="meta">
            Created on {datetime.now().strftime("%Y-%m-%d %H:%M")}
        </div>
    </div>
    <div class="content">
        {html_content}
    </div>
</body>
</html>"""
        
        # Save HTML file
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_with_metadata)
        except IOError as e:
            raise Exception(f"Failed to save view file: {e}")
        
        # Update index
        index_data = self._load_index()
        view_entry = {
            "filename": filename,
            "title": title,
            "created_at": datetime.now().isoformat(),
            "description": description
        }
        index_data["views"].append(view_entry)
        self._save_index(index_data)
        
        # Return URL path
        return f"/views/{filename}"
    
    def get_all_views(self) -> List[Dict[str, Any]]:
        """Get list of all views with metadata"""
        index_data = self._load_index()
        # Sort by creation time (newest first)
        return sorted(index_data["views"], key=lambda x: x["created_at"], reverse=True)
    
    def get_view_content(self, filename: str) -> Optional[str]:
        """Get HTML content of a specific view"""
        filepath = self.views_dir / filename
        if not filepath.exists() or not filename.endswith('.html'):
            return None
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except IOError:
            return None
    
    def delete_view(self, filename: str) -> bool:
        """Delete a specific view"""
        filepath = self.views_dir / filename
        index_data = self._load_index()
        
        # Remove file
        if filepath.exists():
            try:
                filepath.unlink()
            except IOError:
                return False
        
        # Remove from index
        index_data["views"] = [
            view for view in index_data["views"] 
            if view["filename"] != filename
        ]
        self._save_index(index_data)
        
        return True

# Global views manager instance
views_manager = ViewsManager()
