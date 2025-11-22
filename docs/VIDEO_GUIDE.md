# Video Recording Guide

## The 60-Second Demo Video

### Goal
Show the tool in action - let the visualization speak for itself. No voiceover needed.

### Pre-Recording Checklist

1. **Terminal Setup**
   - [ ] Size: 120x30 or larger
   - [ ] Font: 14-16pt (readable in video)
   - [ ] Theme: Dark background
   - [ ] Clean: Close other terminal tabs

2. **Recording Software**
   - macOS: QuickTime, Screen Studio
   - Windows: OBS Studio, ShareX
   - Linux: SimpleScreenRecorder, OBS
   - Recommended: Asciinema (creates shareable terminal recordings)

3. **Test Run**
   ```bash
   # Practice once to know timing
   python3 demo_mode.py
   ```

### Recording Script

#### Take 1: Simple Demo (20 seconds)

```bash
# Start recording
python3 demo_mode.py "What's the weather in SF and calculate 15 * 23?"

# Let it run completely
# Stop recording after it finishes
```

**What to capture:**
- Clean startup
- Tool calls appearing in table
- Thinking process bars
- Final response streaming
- Completion message

#### Take 2: Complex Demo (45 seconds)

```bash
# Start recording
python3 demo_mode.py "Search for AI developments, check weather in 3 cities, and calculate averages"

# Let it show multiple iterations
# Stop after complete
```

**What to capture:**
- Multiple tool calls
- 2-3 iterations visible
- Higher token counts
- Multiple thinking phases

#### Take 3: Real API (if you have key)

```bash
# Start recording
export ANTHROPIC_API_KEY='your-key'
python3 agent_mind.py "What's the weather in Tokyo and what's trending in AI?"

# Real API calls with actual responses
```

**What to capture:**
- Real thinking (not simulated)
- Actual API latency
- Live tool execution
- Real responses

### Editing Tips

1. **Trim Dead Space**
   - Cut first 2 seconds (terminal startup)
   - Cut last 5 seconds (after completion message)

2. **Speed Control**
   - Keep thinking phases at 1x (shows process)
   - Can speed up tool execution to 1.5x
   - NEVER speed up final response (looks natural)

3. **Add Text Overlays** (optional)
   - 0:00 - "Agent Mind Reader - Real-time AI Observability"
   - 0:05 - "Watch: Tool selection, thinking process, token usage"
   - 0:50 - "Built in <24hrs | Works with any agentic API"

4. **Music** (optional)
   - Lo-fi beats or minimal tech music
   - Keep volume low (focus on visuals)
   - Fade out at end

### Using Asciinema (Recommended for Devs)

```bash
# Install
pip install asciinema

# Record
asciinema rec demo.cast

# Run your demo
python3 demo_mode.py

# Ctrl+D to stop

# Upload and share
asciinema upload demo.cast
```

**Why Asciinema?**
- True terminal recording (not video)
- Shareable link
- Text is selectable in playback
- Tiny file size
- Can convert to GIF/video later

### Converting Asciinema to GIF

```bash
# Install converter
npm install -g asciicast2gif

# Convert
asciicast2gif demo.cast demo.gif

# Or use online: https://dstein64.github.io/gifcast/
```

### Platform-Specific Tips

#### YouTube/Twitter
- Length: 30-60 seconds (attention span)
- Resolution: 1920x1080
- Format: MP4
- Captions: Optional but helpful

#### LinkedIn/GitHub
- Length: 20-40 seconds
- Add title card at start
- End with link to repo
- Professional tone

#### Demo Reel / Portfolio
- Length: 45-90 seconds
- Show multiple examples
- Include "behind the scenes" (code snippet)
- Add your contact info at end

### Example Storyboard

**0:00-0:05** - Terminal opens, command runs
```
$ python3 demo_mode.py "Complex query here"
🚀 Starting Agent Mind Reader...
```

**0:05-0:20** - Interface loads, first iteration
```
[Stats panel updates]
[Thinking bar fills]
[First tool call appears]
```

**0:20-0:40** - Multiple tool calls, iterations
```
[Second iteration]
[More tools called]
[Token counts increase]
```

**0:40-0:55** - Final response streams
```
[Response panel fills with text]
[All tools marked as DONE]
```

**0:55-1:00** - Completion
```
✅ Workflow complete
[Hold on final frame]
```

### Advanced: Picture-in-Picture

Show both the TUI and your code:

```
┌─────────────────┬──────────────┐
│                 │  agent_mind. │
│   TUI Demo      │  py          │
│   Running       │              │
│                 │  def run_... │
│                 │              │
└─────────────────┴──────────────┘
```

Use OBS Studio with multiple sources to achieve this.

### Quick Checklist

Before hitting record:

- [ ] Terminal font readable?
- [ ] Full screen or consistent size?
- [ ] Sound off (no notifications)?
- [ ] Tested the command?
- [ ] Battery/power connected?
- [ ] Ready to let it run completely?

After recording:

- [ ] Trim beginning/end?
- [ ] Add title/description?
- [ ] Export in right format?
- [ ] File size reasonable (<50MB)?
- [ ] Tested playback?

### Sample Descriptions

**For YouTube:**
```
Agent Mind Reader - Real-time visualization of AI agent workflows

Watch as Claude thinks, selects tools, and generates responses.
Built in <24 hours to showcase deep understanding of agentic AI.

🔧 Tech: Python, Anthropic API, Rich TUI
⭐ GitHub: [your-link]
🚀 Try it: See README
```

**For Twitter:**
```
Built a real-time TUI to visualize AI agents' "brains" 🧠

Watch it think, call tools, and respond - all live.

<24hr build for xAI hackathon 🚀

[video]
```

**For LinkedIn:**
```
Excited to share my latest project: Agent Mind Reader

A developer tool for visualizing agentic AI workflows in real-time.
Shows thinking process, tool selection, and token usage - critical for 
debugging and optimizing AI systems.

Built with Python & Anthropic API as a proof-of-concept for the
xAI hackathon.

#AI #DeveloperTools #MachineLearning
```

### File Naming

```
agent_mind_reader_demo.mp4          # Main demo
agent_mind_reader_short.mp4         # 15-sec version
agent_mind_reader_github.gif        # For README
agent_mind_reader_demo_4k.mp4       # High quality
```

---

**Remember:** The tool speaks for itself. Keep it clean, let it run, and the visualization will impress. Good luck! 🎬
