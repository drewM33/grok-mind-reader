# Quick Start Guide

## 30-Second Setup

```bash
# 1. Install dependencies
pip install anthropic rich

# 2. Run demo (no API key needed)
python3 demo_mode.py
```

That's it! You'll see a simulated agent workflow.

## 2-Minute Setup (Full Version)

```bash
# 1. Get API key
# Visit: https://console.anthropic.com/

# 2. Set environment variable
export ANTHROPIC_API_KEY='your-key-here'

# 3. Run with real AI
python3 agent_mind.py "What's the weather in Tokyo and calculate 15 * 23?"
```

## What You'll See

```
┌─────────────────────────────────────────────┐
│  🧠 AGENT MIND READER | Query: ...          │
├──────────────┬──────────────────────────────┤
│ 📊 Stats     │  🔧 Tool Execution Log       │
│ • Iteration  │  ┌──────┬──────┬──────┐     │
│ • Tokens     │  │ 09:45│search│query │     │
│ • Tool Count │  │ 09:45│calc  │15*23 │     │
│              │  └──────┴──────┴──────┘     │
│ 🧠 Thinking  │  💬 Agent Response           │
│ ████████     │  The weather in Tokyo is...  │
└──────────────┴──────────────────────────────┘
```

## Understanding the Display

### Left Panel - Status Monitor
- **Iteration**: Current agent loop number
- **Tokens**: API usage (input/output)
- **Thinking**: Visual progress bar of reasoning

### Right Panel - Execution Timeline
- **Tool Log**: Every tool call with timing
- **Response**: Final answer streaming in real-time

### Color Coding
- 🔴 Red: Thinking/reasoning process
- 🟢 Green: Tool execution
- 🔵 Blue: Agent responses
- 🟡 Yellow: Tool inputs/parameters

## Common Use Cases

### 1. Debug Why Agent Used a Tool
```bash
python3 agent_mind.py "What's 5+5?"
```
Watch: Does it call calculator or answer directly?

### 2. Optimize Tool Definitions
```bash
# Try before/after changing tool descriptions
python3 agent_mind.py "Find information about Python"
```
Watch: Which tool does it choose? (search vs calculate)

### 3. Profile Performance
```bash
python3 agent_mind.py "Complex multi-step question"
```
Watch: How many iterations? Token usage per step?

## Demo vs Real Mode

| Feature | Demo Mode | Real Mode |
|---------|-----------|-----------|
| API Key | ❌ Not needed | ✅ Required |
| Real AI | ❌ Simulated | ✅ Claude API |
| Tool Execution | ❌ Fake results | ✅ Real (if implemented) |
| Token Tracking | ✅ Simulated | ✅ Actual usage |
| Speed | Fast | Depends on query |
| Cost | $0 | ~$0.01-0.10/query |

## Tips

1. **Start with demo mode** to understand the interface
2. **Use simple queries** when testing (faster iteration)
3. **Watch the thinking bar** - shows when agent is reasoning
4. **Monitor token counts** - longer = more expensive
5. **Try different phrasings** of same question - see what changes

## Keyboard Shortcuts

- `Ctrl+C`: Exit the visualizer
- No other controls needed - it's automatic!

## Next Steps

1. ✅ Run demo mode
2. ✅ Get API key and run real version  
3. ✅ Try examples from EXAMPLES.md
4. ✅ Read full README.md for architecture
5. ✅ Customize tools for your use case

## Troubleshooting

### "API key not set"
```bash
export ANTHROPIC_API_KEY='sk-ant-...'
```

### "Module not found"
```bash
pip install anthropic rich
```

### Display looks broken
- Increase terminal size (120x30 minimum)
- Use a modern terminal (iTerm2, Windows Terminal, etc.)

### Demo seems stuck
- It should run for ~10 seconds then wait
- Press `Ctrl+C` to exit

## Getting Help

- Read: `README.md` for detailed docs
- Check: `EXAMPLES.md` for more queries
- Issues? Check API key, internet connection, terminal size

**Ready to see an AI agent's brain? Let's go! 🧠🚀**
