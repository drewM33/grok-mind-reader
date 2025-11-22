# Grok Mind Reader 🧠

**Real-time visualization of xAI's Grok agentic workflows**

Watch Grok think, search the web, search X, and execute code - all in a beautiful terminal UI.

## What This Is

A Terminal User Interface (TUI) that provides **deep observability** into Grok's server-side agentic tool calling. Unlike traditional tool calling where you handle each invocation, xAI's agentic API manages the entire reasoning loop on the server. This tool visualizes that process in real-time.

## Why This Matters

xAI's agentic API is a black box by design - the server handles everything automatically. But for **debugging, optimization, and understanding** how Grok researches and reasons, you need visibility. This tool provides:

- 🧠 **Reasoning Tokens**: See Grok think in real-time
- 🔧 **Tool Execution**: Every web search, X search, and code execution
- 📊 **Token Metrics**: Input, output, reasoning, and cached tokens
- 🔄 **Multi-Step Workflows**: Full agentic loops from start to finish
- 📚 **Citations**: All sources Grok consulted

## Demo

```bash
# Install
pip install -r requirements_xai.txt

# Set API key
export XAI_API_KEY='your-key-here'

# Run
python3 grok_mind.py "What are the latest updates from xAI?"
```

## What You'll See

```
┌────────────────────────────────────────────────┐
│ 🧠 GROK MIND READER | Query: ...              │
├──────────────┬─────────────────────────────────┤
│ 📊 Stats     │ 🔧 Server-Side Tool Calls       │
│ Reasoning:   │ ┌────────┬──────────┬────────┐ │
│   1215       │ │ 09:45  │x_search  │ ...    │ │
│ Tools: 5     │ │ 09:46  │web_search│ ...    │ │
│              │ └────────┴──────────┴────────┘ │
│ 🧠 Reasoning │ 💬 Grok Response                │
│ ████████     │ Latest updates from xAI...     │
└──────────────┴─────────────────────────────────┘
```

## Installation

### Prerequisites
- Python 3.8+
- xAI API key ([get one here](https://console.x.ai/))

### Setup

```bash
# Install dependencies
pip install -r requirements_xai.txt

# Or manually
pip install xai-sdk rich

# Set your API key
export XAI_API_KEY='your-key-here'

# Run it
python3 grok_mind.py
```

## How It Works

This tool hooks into xAI's streaming API to capture:

1. **Tool Call Events**: Every `x_search`, `web_search`, `code_execution` call
2. **Reasoning Tokens**: The "thinking" process before responses
3. **Response Streaming**: Final answer as it's generated
4. **Citations**: All sources consulted during research
5. **Usage Metrics**: Token breakdown including cached tokens

### Key Features

**Server-Side Tool Visualization**
- Real-time display of tool calls as Grok makes them
- Arguments passed to each tool
- Tool execution timeline

**Token Tracking**
- **Reasoning Tokens**: Grok's internal thinking
- **Prompt Tokens**: Cumulative input across all steps
- **Completion Tokens**: Final output
- **Cached Tokens**: Efficiency from prompt caching

**Citations**
- Automatic collection from web/X searches
- Full URL list of consulted sources
- Traceability for fact-checking

## xAI-Specific Implementation

This uses xAI's real agentic API features:

```python
from xai_sdk import Client
from xai_sdk.tools import web_search, x_search, code_execution

# Server-side tools - Grok handles execution
chat = client.chat.create(
    model="grok-4-fast",
    tools=[
        web_search(),      # Real-time web search
        x_search(),        # Search X posts/users
        code_execution(),  # Python code execution
    ],
)

# Stream with real-time observability
for response, chunk in chat.stream():
    # Watch tool calls happen
    for tool_call in chunk.tool_calls:
        print(f"Calling: {tool_call.function.name}")
    
    # Track reasoning
    print(f"Thinking: {response.usage.reasoning_tokens}")
    
    # Stream response
    if chunk.content:
        print(chunk.content, end="")
```

## Use Cases

### 1. Developer Tools
- Debug why Grok chose specific tools
- Optimize queries for better tool selection
- Profile token usage across workflows

### 2. Research
- Study Grok's decision-making patterns
- Compare search strategies across queries
- Analyze multi-step reasoning chains

### 3. Cost Optimization
- Monitor tool invocation costs
- Track prompt caching efficiency
- Identify expensive query patterns

## Architecture

```
┌─────────────────────────────────────┐
│         Terminal UI (Rich)          │
│  ┌─────────────┬─────────────────┐ │
│  │  Status &   │   Tool Calls &  │ │
│  │  Reasoning  │   Response      │ │
│  └─────────────┴─────────────────┘ │
└───────────────┬─────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│     Event Processing (Real-time)    │
│  • Parse streaming chunks           │
│  • Track tool calls                 │
│  • Update token counts              │
└───────────────┬─────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│      xAI Streaming API              │
│  • Server-side tool execution       │
│  • Autonomous reasoning loop        │
│  • Real-time progress events        │
└─────────────────────────────────────┘
```

## Technical Deep Dive

### Token Breakdown

xAI's agentic API has unique token accounting:

- **`reasoning_tokens`**: Internal reasoning, excludes output
- **`prompt_tokens`**: Cumulative across all inference steps
- **`completion_tokens`**: Final output only
- **`cached_prompt_text_tokens`**: Served from cache (cost savings)

The high `prompt_tokens` is expected - each agentic step includes full conversation history, but prompt caching makes this efficient.

### Tool Usage Tracking

Two key metrics:

1. **`tool_calls`**: All attempted calls (includes failures)
2. **`server_side_tool_usage`**: Successful calls (what you're billed for)

They differ when tools fail (bad URL, deleted post, etc.).

### Server-Side vs Client-Side

xAI supports mixing both:
- **Server-side**: `web_search`, `x_search`, `code_execution` - handled by Grok
- **Client-side**: Custom tools - you execute and return results

This visualizer focuses on server-side tools for observability.

## Examples

```bash
# Basic query
python3 grok_mind.py "What's trending in AI?"

# Complex multi-tool query
python3 grok_mind.py "Search X for xAI updates, find their latest blog post, and summarize"

# Custom query
python3 grok_mind.py "your question here"
```

## Comparison to Alternatives

| Feature | Grok Mind Reader | LangSmith | W&B Traces |
|---------|------------------|-----------|------------|
| Real-time TUI | ✅ | ❌ | ❌ |
| Zero setup | ✅ | ❌ | ❌ |
| xAI-native | ✅ | ❌ | ❌ |
| Tool visualization | ✅ | ✅ | ✅ |
| Cost | Free | Paid | Paid |
| Local-first | ✅ | ❌ | ❌ |

## Performance

- **Refresh Rate**: 20 FPS for smooth updates
- **Memory**: Minimal (~50 MB)
- **Latency**: ~0ms overhead (visualizes existing calls)
- **Network**: Only what Grok uses

## Extending This

Want to build on this? Ideas:

- **Add Collections Search**: Visualize knowledge base queries
- **MCP Tool Support**: Show remote tool calls
- **Export Metrics**: Save to JSON/CSV for analysis
- **Web Dashboard**: Port to web UI
- **Cost Calculator**: Real-time $ tracking
- **Comparison Mode**: Run same query on different models

## Troubleshooting

**"XAI_API_KEY not set"**
```bash
export XAI_API_KEY='xai-...'
```

**"xai-sdk not installed"**
```bash
pip install xai-sdk>=1.4.0
```

**Display issues**
- Terminal size: 120x30 minimum
- Modern terminal required (iTerm2, Windows Terminal, etc.)

## Requirements

- **xAI SDK**: Version 1.4.0+ (for `get_tool_call_type`)
- **Python**: 3.8+
- **Terminal**: Modern with 256 colors

## Contributing

Built in <24 hours as a proof-of-concept. Production-ready with:
- Error handling
- Real API integration
- Professional layout
- Token tracking

Want to improve it? Fork and submit PRs!

## License

MIT - Use it, break it, build on it.

## Credits

Built with:
- [xAI SDK](https://docs.x.ai) - Official Grok API
- [Rich](https://github.com/Textualize/rich) - Terminal UI library

---

**Made with 🧠 to see inside Grok's agentic mind**

**For xAI Hackathon 2025** 🚀
