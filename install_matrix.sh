#!/bin/bash

echo "Installing GROK MIND CYBER Matrix Interface..."

# Create the main Python file
cat > grok_mind_cyber_matrix.py << 'ENDOFFILE'
[PASTE THE FULL PYTHON CODE FROM THE FILE ABOVE]
ENDOFFILE

# Create requirements.txt
cat > requirements.txt << 'ENDOFFILE'
aiohttp==3.9.1
aiohttp-cors==0.7.0
ENDOFFILE

echo "✅ Files created!"
echo "Installing dependencies..."
pip3 install aiohttp aiohttp-cors

echo "🟢 Ready! Run: python3 grok_mind_cyber_matrix.py"
