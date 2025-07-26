"""HappyBird Watcher Widget - Displays happybird.txt files from SyftBox filesystem"""

from syft_widget import APIDisplay


class HappyBirdWatcher(APIDisplay):
    """Widget that watches for and displays happybird.txt files in the SyftBox filesystem"""

    def __init__(self, refresh_interval=5):
        """
        Initialize the HappyBird Watcher widget

        Args:
            refresh_interval: How often to check for new files (seconds)
        """
        # Call parent constructor with the API endpoints this widget needs
        super().__init__(
            endpoints=["/api/happybird/files", "/api/happybird/content"]
        )
        self.refresh_interval = refresh_interval

    def render_content(self, data, server_type="checkpoint"):
        """Render the widget content showing found happybird.txt files

        This method is called to generate the initial HTML display.

        Args:
            data: Dictionary with endpoint data, e.g. {"/api/happybird/files": {...}}
            server_type: Current server mode ("checkpoint", "thread", or "syftbox")
        """

        # Extract data from the endpoints
        files_data = data.get("/api/happybird/files", {})
        files = files_data.get("files", [])
        total_count = files_data.get("total_count", 0)

        content_data = data.get("/api/happybird/content", {})
        selected_file = content_data.get("selected_file", None)
        file_content = content_data.get("content", "")

        # Server type badge - shows which mode we're in
        badge_color = {
            "checkpoint": "#6c757d",  # Gray for mock data
            "thread": "#28a745",      # Green for dev server
            "syftbox": "#007bff"      # Blue for production
        }.get(server_type, "#6c757d")

        server_label = {
            "checkpoint": "📁 Checkpoint", 
            "thread": "🧵 Thread Server", 
            "syftbox": "📦 SyftBox"
        }.get(server_type, server_type)

        # Build file list HTML
        file_list_html = ""
        if files:
            for file_info in files:
                path = file_info.get("path", "")
                modified = file_info.get("modified", "")
                size = file_info.get("size", 0)
                owner = file_info.get("owner", "unknown")

                file_list_html += f"""
                <div onclick="window.selectHappyBirdFile_{id(self)}('{path}')" 
                     style="padding: 10px; margin: 5px 0; background: white; border: 1px solid #ddd; 
                            border-radius: 4px; cursor: pointer; transition: all 0.2s;"
                     onmouseover="this.style.background='#f0f0f0'" 
                     onmouseout="this.style.background='white'">
                    <div style="font-weight: bold; color: #333;">🐦 {owner}</div>
                    <div style="font-size: 12px; color: #666; margin-top: 4px;">
                        Modified: {modified} | Size: {size} bytes
                    </div>
                </div>
                """
        else:
            file_list_html = """
            <div style="padding: 20px; text-align: center; color: #666;">
                <div style="font-size: 48px; margin-bottom: 10px;">🔍</div>
                <div>No happybird.txt files found in SyftBox filesystem</div>
                <div style="font-size: 12px; margin-top: 10px;">
                    Files will appear here when users create happybird.txt in their SyftBox folders
                </div>
            </div>
            """

        # Build content display for selected file
        content_html = ""
        if selected_file and file_content:
            content_html = f"""
            <div style="margin-top: 20px;">
                <h4 style="margin: 0 0 10px 0; color: #333;">
                    Content of {selected_file}:
                </h4>
                <pre style="background: #f8f9fa; padding: 15px; border-radius: 4px; 
                           overflow-x: auto; white-space: pre-wrap; word-wrap: break-word;
                           border: 1px solid #dee2e6; font-family: monospace; font-size: 14px;">
{file_content}
                </pre>
            </div>
            """

        # Return the complete widget HTML
        return f"""
        <div style="font-family: -apple-system, sans-serif; padding: 20px; background: #f8f9fa; 
                    border-radius: 8px; position: relative; min-height: 300px;">
            <div style="position: absolute; top: 10px; right: 10px; background: {badge_color}; 
                        color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">
                {server_label}
            </div>

            <h3 style="margin: 0 0 20px 0; color: #333;">
                🐦 HappyBird Watcher
            </h3>

            <div style="background: #e3f2fd; padding: 10px 15px; border-radius: 4px; 
                        margin-bottom: 20px; border-left: 4px solid #2196f3;">
                <div style="font-weight: bold; color: #1976d2;">
                    Found {total_count} happybird.txt file{'s' if total_count != 1 else ''}
                </div>
                <div style="font-size: 12px; color: #666; margin-top: 4px;">
                    Auto-refreshing every {self.refresh_interval} seconds
                </div>
            </div>

            <div style="max-height: 300px; overflow-y: auto;">
                {file_list_html}
            </div>

            {content_html}
        </div>
        """

    def get_update_script(self):
        """JavaScript for dynamic updates

        This JavaScript runs on every update to refresh the widget display.
        It has access to:
        - currentData: Latest data from all endpoints
        - currentServerType: Current server mode
        - element: The widget's DOM element
        """
        return f"""
        // Get data from endpoints
        const filesData = currentData['/api/happybird/files'] || {{}};
        const files = filesData.files || [];
        const totalCount = filesData.total_count || 0;

        // Server type badge
        const badgeColors = {{checkpoint: "#6c757d", thread: "#28a745", syftbox: "#007bff"}};
        const serverLabels = {{checkpoint: "📁 Checkpoint", thread: "🧵 Thread Server", syftbox: "📦 SyftBox"}};
        const badgeColor = badgeColors[currentServerType] || "#6c757d";
        const serverLabel = serverLabels[currentServerType] || currentServerType;

        // Build file list HTML
        let fileListHtml = '';
        if (files.length > 0) {{
            files.forEach(fileInfo => {{
                const path = fileInfo.path || '';
                const modified = fileInfo.modified || '';
                const size = fileInfo.size || 0;
                const owner = fileInfo.owner || 'unknown';

                fileListHtml += `
                <div onclick="window.selectHappyBirdFile_{id(self)}('${{path}}')" 
                     style="padding: 10px; margin: 5px 0; background: white; border: 1px solid #ddd; 
                            border-radius: 4px; cursor: pointer; transition: all 0.2s;"
                     onmouseover="this.style.background='#f0f0f0'" 
                     onmouseout="this.style.background='white'">
                    <div style="font-weight: bold; color: #333;">🐦 ${{owner}}</div>
                    <div style="font-size: 12px; color: #666; margin-top: 4px;">
                        Modified: ${{modified}} | Size: ${{size}} bytes
                    </div>
                </div>
                `;
            }});
        }} else {{
            fileListHtml = `
            <div style="padding: 20px; text-align: center; color: #666;">
                <div style="font-size: 48px; margin-bottom: 10px;">🔍</div>
                <div>No happybird.txt files found in SyftBox filesystem</div>
                <div style="font-size: 12px; margin-top: 10px;">
                    Files will appear here when users create happybird.txt in their SyftBox folders
                </div>
            </div>
            `;
        }}

        // Update the widget HTML
        element.innerHTML = `
        <div style="font-family: -apple-system, sans-serif; padding: 20px; background: #f8f9fa; 
                    border-radius: 8px; position: relative; min-height: 300px;">
            <div style="position: absolute; top: 10px; right: 10px; background: ${{badgeColor}}; 
                        color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">
                ${{serverLabel}}
            </div>

            <h3 style="margin: 0 0 20px 0; color: #333;">
                🐦 HappyBird Watcher
            </h3>

            <div style="background: #e3f2fd; padding: 10px 15px; border-radius: 4px; 
                        margin-bottom: 20px; border-left: 4px solid #2196f3;">
                <div style="font-weight: bold; color: #1976d2;">
                    Found ${{totalCount}} happybird.txt file${{totalCount !== 1 ? 's' : ''}}
                </div>
                <div style="font-size: 12px; color: #666; margin-top: 4px;">
                    Auto-refreshing every {self.refresh_interval} seconds
                </div>
            </div>

            <div style="max-height: 300px; overflow-y: auto;">
                ${{fileListHtml}}
            </div>
        </div>
        `;

        // Re-attach file selection handler
        window.selectHappyBirdFile_{id(self)} = function(filepath) {{
            console.log('File selected:', filepath);
            // TODO: Implement file content loading
        }};
        """
