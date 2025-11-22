# Agent Mind Reader - Examples

## Basic Examples

### 1. Simple Tool Use
```bash
python3 agent_mind.py "What's the weather in New York?"
```

**What to watch for:**
- Agent receives query
- Calls `get_weather` tool
- Returns formatted response

### 2. Multi-Tool Orchestration
```bash
python3 agent_mind.py "What's the weather in SF and calculate 15 * 23?"
```

**What to watch for:**
- Agent calls TWO tools: `get_weather` AND `calculate`
- May call them sequentially or reason about both
- Shows multi-step thinking process

### 3. Complex Multi-Step Query
```bash
python3 agent_mind.py "Search for AI developments, check weather in Tokyo, and calculate fibonacci of 8"
```

**What to watch for:**
- Multiple iterations
- 3 different tool calls
- Token count increases each iteration
- Final synthesis of all information

## Advanced Examples

### 4. Debugging Tool Selection
```bash
python3 agent_mind.py "Tell me about the weather" 
```

**Observation:** Watch which location it assumes or if it asks for clarification

### 5. No Tool Needed
```bash
python3 agent_mind.py "What is 2+2?"
```

**Observation:** Agent may NOT call the calculator - it knows simple math

### 6. Tool Chain Dependency
```bash
python3 agent_mind.py "Calculate 50% of 200, then search for restaurants in that price range"
```

**Observation:** 
- First iteration: calls `calculate` 
- Second iteration: uses result (100) in `search_web`
- Shows context passing between tool calls

## Custom Tool Examples

Want to add your own tools? Here's how:

### Adding a Database Query Tool

```python
{
    "name": "query_database",
    "description": "Query a SQL database",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "SQL query to execute"
            },
            "database": {
                "type": "string",
                "description": "Database name"
            }
        },
        "required": ["query"]
    }
}
```

Add to the `TOOLS` list in `agent_mind.py` and implement in `simulate_tool_response`.

### Adding an API Call Tool

```python
{
    "name": "call_api",
    "description": "Make HTTP API requests",
    "input_schema": {
        "type": "object",
        "properties": {
            "endpoint": {
                "type": "string",
                "description": "API endpoint URL"
            },
            "method": {
                "type": "string",
                "enum": ["GET", "POST", "PUT", "DELETE"]
            },
            "payload": {
                "type": "object",
                "description": "Request payload"
            }
        },
        "required": ["endpoint", "method"]
    }
}
```

## Performance Testing

### Token Efficiency
```bash
# Compare token usage across similar queries
python3 agent_mind.py "Weather in NYC"
python3 agent_mind.py "What is the current weather in New York City?"
```

**Observation:** Longer queries = more input tokens, but similar output

### Iteration Count
```bash
# Single-step (1 iteration expected)
python3 agent_mind.py "Calculate 5 * 5"

# Multi-step (2-3 iterations expected)  
python3 agent_mind.py "Calculate 5 * 5, then search for that number of items"
```

## Demo Mode Examples

No API key? Use demo mode:

```bash
# Default demo
python3 demo_mode.py

# Custom query (simulated)
python3 demo_mode.py "Find me information about quantum computing"
```

**Note:** Demo mode simulates the TUI but doesn't make real API calls.

## Recording Sessions

Want to save sessions for later analysis?

```bash
# Using script command (Unix/Linux)
script -c "python3 agent_mind.py 'your query'" session.log

# Review later
cat session.log
```

## Troubleshooting Examples

### Issue: Agent doesn't call expected tool

**Test:**
```bash
python3 agent_mind.py "What's 2+2?"
```

**Expected:** Agent knows simple math, won't call calculator
**Fix:** Use harder math: "Calculate the 50th fibonacci number"

### Issue: Too many iterations

**Test:**
```bash
python3 agent_mind.py "Solve world peace"
```

**Expected:** Vague queries may cause multiple tool calls
**Fix:** Be specific: "Search for peace treaties from 2020"

### Issue: Missing tools

**Test:**
```bash
python3 agent_mind.py "Send an email to john@example.com"
```

**Expected:** No email tool available - agent will explain limitation
**Fix:** Add email tool to `TOOLS` list

## Visualization Tips

### Best Queries for Demo Videos

1. **Quick & Clear** (10 seconds):
   ```bash
   python3 agent_mind.py "Weather in Paris and calculate 12*12"
   ```

2. **Complex & Impressive** (30 seconds):
   ```bash
   python3 agent_mind.py "Search for recent AI breakthroughs, calculate average year, check weather in 3 cities"
   ```

3. **Educational** (shows agent reasoning):
   ```bash
   python3 agent_mind.py "I need to paint a room that's 12ft by 15ft. How many gallons of paint?"
   ```
   *Watch it reason about calculation, then possibly search for coverage rates*

### Screen Recording Settings

- Terminal size: 120x30 minimum for full layout
- Font size: 14-16pt for readability
- Theme: Dark background shows colors better
- Speed: Record at 1x, can speed up in editing

## Next Steps

Once you're comfortable:

1. **Add Real Tools**: Replace simulated responses with actual API calls
2. **Export Metrics**: Log token counts, timing to CSV
3. **Compare Models**: Run same query on different models, compare
4. **Build Web UI**: Port the TUI concept to a web dashboard

Happy exploring! 🧠
