#!/usr/bin/env python3
"""
GROK MIND CYBER - Matrix Interface
A glitchy, Matrix-style terminal interface for xAI queries
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, List, Any
import sys
import os

# For web server
import aiohttp
from aiohttp import web
import aiohttp_cors

# HTML Template (embedded)
MATRIX_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GROK MIND READER :: MATRIX INTERFACE</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            background: #000;
            color: #00ff00;
            font-family: 'Share Tech Mono', monospace;
            overflow: hidden;
            height: 100vh;
        }
        
        #matrix-rain {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            pointer-events: none;
            opacity: 0.1;
            z-index: 1;
        }
        
        .rain-column {
            position: absolute;
            top: -100%;
            font-size: 20px;
            animation: matrix-fall linear infinite;
            color: #0f0;
            text-shadow: 0 0 5px #0f0;
        }
        
        @keyframes matrix-fall {
            to { transform: translateY(200vh); }
        }
        
        .main-container {
            position: relative;
            z-index: 10;
            padding: 20px;
            height: 100vh;
            display: flex;
            flex-direction: column;
            background: radial-gradient(ellipse at center, rgba(0,255,0,0.05) 0%, rgba(0,0,0,0.9) 100%);
        }
        
        @keyframes glitch {
            0%, 100% {
                text-shadow: 
                    0.05em 0 0 rgba(255,0,0,.75),
                    -0.05em -0.025em 0 rgba(0,255,0,.75),
                    0.025em 0.05em 0 rgba(0,0,255,.75);
            }
            15% {
                text-shadow: 
                    -0.05em -0.025em 0 rgba(255,0,0,.75),
                    0.025em 0.025em 0 rgba(0,255,0,.75),
                    -0.05em -0.05em 0 rgba(0,0,255,.75);
            }
        }
        
        .glitch { animation: glitch 2s infinite; }
        
        .header {
            border: 3px solid #0f0;
            padding: 15px;
            margin-bottom: 20px;
            background: rgba(0,0,0,0.8);
            box-shadow: 0 0 20px #0f0, inset 0 0 20px rgba(0,255,0,0.1);
        }
        
        .header h1 {
            text-align: center;
            font-size: 24px;
            letter-spacing: 4px;
            color: #0f0;
        }
        
        .dashboard {
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 20px;
            flex: 1;
            overflow: hidden;
        }
        
        .panel {
            border: 2px solid #0f0;
            padding: 15px;
            background: rgba(0,0,0,0.9);
            position: relative;
            overflow: hidden;
        }
        
        .panel::after {
            content: '';
            position: absolute;
            top: 0; left: -100%;
            width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(0,255,0,0.2), transparent);
            animation: scan 3s infinite;
        }
        
        @keyframes scan {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        
        .stat-item {
            display: flex;
            justify-content: space-between;
            padding: 8px;
            margin: 5px 0;
            background: rgba(0,255,0,0.05);
            border-left: 3px solid #0f0;
        }
        
        .output-section {
            margin-top: 20px;
            padding: 15px;
            background: rgba(0,255,0,0.05);
            border: 1px solid #0f0;
            max-height: 400px;
            overflow-y: auto;
        }
        
        .status-bar {
            position: fixed;
            bottom: 0; left: 0; right: 0;
            background: #000;
            border-top: 2px solid #0f0;
            padding: 10px 20px;
            display: flex;
            justify-content: space-between;
            z-index: 100;
        }
        
        .query-input {
            width: 100%;
            padding: 10px;
            background: rgba(0,255,0,0.1);
            border: 1px solid #0f0;
            color: #0f0;
            font-family: inherit;
            margin-top: 10px;
        }
        
        .query-button {
            padding: 10px 20px;
            background: #0f0;
            color: #000;
            border: none;
            cursor: pointer;
            font-family: inherit;
            text-transform: uppercase;
            margin-top: 10px;
        }
        
        .query-button:hover {
            background: #0ff;
            box-shadow: 0 0 20px #0ff;
        }
    </style>
</head>
<body>
    <div id="matrix-rain"></div>
    
    <div class="main-container">
        <div class="header">
            <h1 class="glitch">⟨ GROK MIND READER :: NEURAL INTERFACE ⟩</h1>
        </div>
        
        <div class="dashboard">
            <div class="left-panel">
                <div class="panel">
                    <h3 style="color: #0ff; margin-bottom: 15px;">TOKEN STATS</h3>
                    <div id="stats-container">
                        <div class="stat-item">
                            <span>Prompt:</span>
                            <span id="prompt-tokens">7890</span>
                        </div>
                        <div class="stat-item">
                            <span>Output:</span>
                            <span id="output-tokens">1603</span>
                        </div>
                        <div class="stat-item">
                            <span>Think:</span>
                            <span id="think-tokens">308</span>
                        </div>
                        <div class="stat-item">
                            <span>Cache:</span>
                            <span id="cache-tokens">3777</span>
                        </div>
                        <div class="stat-item">
                            <span>Tools:</span>
                            <span id="tools-count">1</span>
                        </div>
                    </div>
                </div>
                
                <div class="panel" style="margin-top: 20px;">
                    <h3 style="color: #ff0080; margin-bottom: 15px;">NEURAL QUERY</h3>
                    <input type="text" id="query-input" class="query-input" placeholder="Enter query for xAI..." />
                    <button onclick="executeQuery()" class="query-button">EXECUTE</button>
                </div>
            </div>
            
            <div class="right-panel">
                <div class="panel">
                    <h3 style="color: #ffa500; margin-bottom: 15px;">TIMELINE :: TOOL CALLS</h3>
                    <div id="timeline-container">
                        <div style="color: #ffa500; margin: 5px 0;">
                            08:50:39 - x_keyword_search: {"query":"from:xai","limit":10}
                        </div>
                    </div>
                    
                    <div class="output-section">
                        <h3 style="color: #0f0; margin-bottom: 15px;">💬 GROK OUTPUT</h3>
                        <div id="output-content">
                            <div style="color: #fff; margin: 10px 0;">
                                ### Latest Posts from @xai (as of November 22, 2025)<br><br>
                                Ready to process queries...
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="status-bar">
        <div>
            <span style="color: #0f0;">✓ NEURAL SYNC: <span id="status">READY</span></span>
        </div>
        <div>
            <span style="color: #0f0;">Tools: <span id="tool-count">1</span> | Time: <span id="current-time"></span></span>
        </div>
    </div>
    
    <script>
        // WebSocket connection for real-time updates
        let ws = null;
        
        function connectWebSocket() {
            ws = new WebSocket('ws://localhost:8080/ws');
            
            ws.onopen = () => {
                console.log('Connected to Grok Mind');
                document.getElementById('status').textContent = 'CONNECTED';
            };
            
            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                updateInterface(data);
            };
            
            ws.onclose = () => {
                document.getElementById('status').textContent = 'DISCONNECTED';
                setTimeout(connectWebSocket, 3000);
            };
        }
        
        function updateInterface(data) {
            if (data.stats) {
                document.getElementById('prompt-tokens').textContent = data.stats.prompt || 7890;
                document.getElementById('output-tokens').textContent = data.stats.output || 1603;
                document.getElementById('think-tokens').textContent = data.stats.think || 308;
                document.getElementById('cache-tokens').textContent = data.stats.cache || 3777;
                document.getElementById('tools-count').textContent = data.stats.tools || 1;
            }
            
            if (data.timeline) {
                const timelineHtml = data.timeline.map(t => 
                    `<div style="color: #ffa500; margin: 5px 0;">
                        ${t.time} - ${t.tool}: ${t.args}
                    </div>`
                ).join('');
                document.getElementById('timeline-container').innerHTML = timelineHtml;
            }
            
            if (data.output) {
                document.getElementById('output-content').innerHTML += 
                    `<div style="color: #fff; margin: 10px 0;">${data.output}</div>`;
            }
        }
        
        function executeQuery() {
            const query = document.getElementById('query-input').value;
            if (query && ws && ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({ type: 'query', query: query }));
                document.getElementById('query-input').value = '';
            }
        }
        
        // Matrix rain effect
        function createMatrixRain() {
            const container = document.getElementById('matrix-rain');
            const columns = Math.floor(window.innerWidth / 20);
            
            for (let i = 0; i < columns; i++) {
                const column = document.createElement('div');
                column.className = 'rain-column';
                column.style.left = i * 20 + 'px';
                column.style.animationDuration = Math.random() * 3 + 2 + 's';
                column.style.animationDelay = Math.random() * 2 + 's';
                
                let chars = '';
                const charSet = '01ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ';
                for (let j = 0; j < 30; j++) {
                    chars += charSet[Math.floor(Math.random() * charSet.length)] + '<br>';
                }
                column.innerHTML = chars;
                container.appendChild(column);
            }
        }
        
        // Update time
        setInterval(() => {
            const now = new Date();
            document.getElementById('current-time').textContent = now.toTimeString().split(' ')[0];
        }, 1000);
        
        // Initialize
        document.addEventListener('DOMContentLoaded', () => {
            createMatrixRain();
            connectWebSocket();
        });
        
        // Enter key to execute
        document.getElementById('query-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') executeQuery();
        });
    </script>
</body>
</html>'''

class GrokMindAgent:
    """Main Grok Mind Agent with Matrix interface"""
    
    def __init__(self):
        self.stats = {
            'prompt': 7890,
            'output': 1603,
            'think': 308,
            'cache': 3777,
            'tools': 1
        }
        self.timeline = []
        self.websockets = set()
        
    async def run_grok_agent(self, query: str) -> Dict[str, Any]:
        """Simulate running the Grok agent (replace with your actual implementation)"""
        
        # Add to timeline
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.timeline.append({
            'time': timestamp,
            'tool': 'x_keyword_search',
            'args': f'{{"query": "{query}", "limit": 10}}'
        })
        
        # Simulate processing
        await asyncio.sleep(0.5)
        
        # Update stats
        self.stats['tools'] += 1
        self.stats['output'] += len(query) * 2
        
        # Generate response (replace with actual xAI API call)
        response = f"""### Latest Posts from @xai
        
I've fetched the latest posts about: {query}

Post ID: {int(time.time() * 1000000)}
Content: "Processing query about {query}..."
Timestamp: {timestamp}
        """
        
        return {
            'stats': self.stats,
            'timeline': self.timeline[-5:],  # Last 5 entries
            'output': response
        }
    
    async def handle_websocket(self, request):
        """Handle WebSocket connections"""
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        self.websockets.add(ws)
        
        try:
            # Send initial stats
            await ws.send_json({
                'stats': self.stats,
                'timeline': self.timeline[-5:]
            })
            
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    data = json.loads(msg.data)
                    
                    if data.get('type') == 'query':
                        query = data.get('query', '')
                        result = await self.run_grok_agent(query)
                        
                        # Broadcast to all connected clients
                        for client_ws in self.websockets:
                            try:
                                await client_ws.send_json(result)
                            except:
                                pass
                                
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    print(f'WebSocket error: {ws.exception()}')
                    
        except Exception as e:
            print(f"WebSocket error: {e}")
        finally:
            self.websockets.discard(ws)
            
        return ws
    
    async def index_handler(self, request):
        """Serve the Matrix HTML interface"""
        return web.Response(text=MATRIX_HTML, content_type='text/html')
    
    async def api_handler(self, request):
        """REST API endpoint for queries"""
        data = await request.json()
        query = data.get('query', '')
        result = await self.run_grok_agent(query)
        return web.json_response(result)

def create_app():
    """Create the web application"""
    agent = GrokMindAgent()
    app = web.Application()
    
    # Setup CORS
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            allow_methods="*"
        )
    })
    
    # Routes
    app.router.add_get('/', agent.index_handler)
    app.router.add_get('/ws', agent.handle_websocket)
    app.router.add_post('/api/query', agent.api_handler)
    
    # Configure CORS on all routes
    for route in list(app.router.routes()):
        if not isinstance(route.resource, web.StaticResource):
            cors.add(route)
    
    return app

def main():
    """Main entry point"""
    print("""
    ╔════════════════════════════════════════════╗
    ║   GROK MIND CYBER :: MATRIX INTERFACE     ║
    ║   Neural Interface Activated               ║
    ╚════════════════════════════════════════════╝
    """)
    
    print("🟢 Starting Matrix Interface on http://localhost:8080")
    print("🔧 WebSocket endpoint: ws://localhost:8080/ws")
    print("📡 API endpoint: http://localhost:8080/api/query")
    print("\nPress Ctrl+C to exit\n")
    
    app = create_app()
    web.run_app(app, host='0.0.0.0', port=8080)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🔴 Neural link terminated")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        sys.exit(1)
