#!/usr/bin/env python3
"""
Grok Mind Reader - Real-time TUI for visualizing xAI agentic workflows
Works with xAI's actual Grok API (server-side tools)
"""

import os
import sys
import time
from datetime import datetime
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.console import Group, Console

# Check if xai_sdk is available
try:
    from xai_sdk import Client
    from xai_sdk.chat import user
    from xai_sdk.tools import web_search, x_search, code_execution
    XAI_AVAILABLE = True
except ImportError:
    XAI_AVAILABLE = False
    print("⚠️  xai-sdk not installed. Install with: pip install xai-sdk")

# Configuration
API_KEY = os.getenv("XAI_API_KEY")
MODEL = "grok-4-fast"


def make_layout():
    """Define the TUI layout with 3 main sections"""
    layout = Layout(name="root")
    
    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="footer", size=3)
    )
    
    layout["main"].split_row(
        Layout(name="left", ratio=1),
        Layout(name="right", ratio=2)
    )
    
    return layout


def run_grok_agent(query: str):
    """Run the Grok agent with real-time visualization"""
    
    if not API_KEY:
        console = Console()
        console.print("[bold red]Error: XAI_API_KEY not set![/bold red]")
        console.print("Set it with: export XAI_API_KEY='your-key-here'")
        console.print("Get your key at: https://console.x.ai/")
        sys.exit(1)
    
    if not XAI_AVAILABLE:
        console = Console()
        console.print("[bold red]Error: xai-sdk not installed![/bold red]")
        console.print("Install with: pip install xai-sdk")
        sys.exit(1)
    
    client = Client(api_key=API_KEY)
    
    # Initialize layout
    layout = make_layout()
    
    # State tracking - use list to rebuild table each time
    tool_calls = []
    
    thinking_text = Text()
    response_text = Text()
    
    prompt_tokens = 0
    completion_tokens = 0
    reasoning_tokens = 0
    cached_tokens = 0
    tool_call_count = 0
    
    with Live(layout, refresh_per_second=20, screen=True) as live:
        
        # Update header
        layout["header"].update(
            Panel(
                Text(f"🧠 GROK MIND READER | Query: {query[:80]}...", style="bold magenta"),
                style="white on blue"
            )
        )
        
        # Create chat with server-side tools
        chat = client.chat.create(
            model=MODEL,
            tools=[
                web_search(),
                x_search(),
                code_execution(),
            ],
        )
        
        chat.append(user(query))
        
        is_thinking = True
        
        def build_tool_table():
            """Build the tool calls table from current state"""
            table = Table(show_header=True, header_style="bold cyan", expand=True, show_lines=True)
            table.add_column("Time", style="dim", width=8)
            table.add_column("Tool", style="green", width=20)
            table.add_column("Arguments", style="yellow")
            
            for call in tool_calls:
                table.add_row(call["time"], call["tool"], call["args"])
            
            return table
        
        try:
            # Stream the response
            for response, chunk in chat.stream():
                
                # Update status panel
                status_text = Text()
                status_text.append(f"Prompt Tokens: {prompt_tokens}\n", style="cyan")
                status_text.append(f"Completion: {completion_tokens}\n", style="green")
                status_text.append(f"Reasoning: {reasoning_tokens}\n", style="red")
                status_text.append(f"Cached: {cached_tokens}\n", style="yellow")
                status_text.append(f"Tool Calls: {tool_call_count}\n", style="magenta")
                
                layout["left"].update(Panel(
                    Group(
                        Panel(status_text, title="📊 Token Stats", border_style="cyan"),
                        Panel(thinking_text, title="🧠 Reasoning Process", border_style="red", height=15)
                    ),
                    title="Status Monitor"
                ))
                
                layout["right"].update(Panel(
                    Group(
                        Panel(build_tool_table(), title="🔧 Server-Side Tool Calls", border_style="yellow"),
                        Panel(response_text, title="💬 Grok Response", border_style="green")
                    ),
                    title="Execution Timeline"
                ))
                
                # Track tool calls from chunk
                if chunk.tool_calls:
                    for tool_call in chunk.tool_calls:
                        tool_call_count += 1
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        
                        tool_calls.append({
                            "time": timestamp,
                            "tool": tool_call.function.name,
                            "args": str(tool_call.function.arguments)[:50] + "..."
                        })
                        
                        thinking_text.append(
                            f"🔧 Calling {tool_call.function.name}\n",
                            style="yellow"
                        )
                
                # Track reasoning tokens
                if response.usage.reasoning_tokens:
                    new_reasoning = response.usage.reasoning_tokens - reasoning_tokens
                    reasoning_tokens = response.usage.reasoning_tokens
                    
                    if new_reasoning > 0 and is_thinking:
                        # Visual reasoning indicator
                        thinking_text.append("█" * (new_reasoning // 10), style="dim red")
                
                # Track other token counts
                if hasattr(response.usage, 'prompt_tokens'):
                    prompt_tokens = response.usage.prompt_tokens
                if hasattr(response.usage, 'completion_tokens'):
                    completion_tokens = response.usage.completion_tokens
                if hasattr(response.usage, 'cached_prompt_text_tokens'):
                    cached_tokens = response.usage.cached_prompt_text_tokens
                
                # Track content streaming
                if chunk.content:
                    if is_thinking:
                        is_thinking = False
                        thinking_text.append("\n\n✅ Reasoning complete!\n", style="bold green")
                    
                    response_text.append(chunk.content, style="white")
            
            # Final update with citations
            if hasattr(response, 'citations') and response.citations:
                citation_text = Text("\n\n📚 Citations:\n", style="bold blue")
                for i, citation in enumerate(response.citations[:5], 1):  # Show first 5
                    citation_text.append(f"{i}. {citation}\n", style="dim blue")
                if len(response.citations) > 5:
                    citation_text.append(f"... and {len(response.citations) - 5} more\n", style="dim")
                
                response_text.append(citation_text)
            
            # Show server-side tool usage summary
            if hasattr(response, 'server_side_tool_usage'):
                usage_text = Text("\n\n🔧 Tool Usage Summary:\n", style="bold yellow")
                for tool, count in response.server_side_tool_usage.items():
                    usage_text.append(f"  • {tool}: {count}x\n", style="yellow")
                response_text.append(usage_text)
            
        except Exception as e:
            thinking_text.append(f"\n❌ Error: {str(e)}\n", style="bold red")
        
        # Final footer
        layout["footer"].update(
            Panel(
                Text(
                    f"✅ Grok workflow complete | Total tools: {tool_call_count} | Press Ctrl+C to exit",
                    justify="center"
                ),
                style="dim white"
            )
        )
        
        # Keep display alive
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    # Example queries that will trigger tool use
    QUERIES = [
        "What are the latest updates from xAI?",
        "Search for recent AI developments and calculate the fibonacci of 10",
        "What's trending on X about artificial intelligence?"
    ]
    
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = QUERIES[0]
        print(f"Using default query: {query}")
        print("Tip: Run with your own query: python grok_mind.py 'your question here'\n")
        time.sleep(2)
    
    run_grok_agent(query)
