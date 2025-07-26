# Promptfoo Installation Guide for Discernus

## Problem Solved
Successfully resolved `npm install promptfoo` failures due to `better-sqlite3` compilation errors caused by missing `xcodebuild` command on macOS systems with only Command Line Tools installed.

## Root Cause
- `promptfoo` depends on `better-sqlite3` which requires native compilation
- `node-gyp` (Node.js native compilation tool) requires `xcodebuild -version` to detect development environment
- `xcodebuild` command requires full Xcode application, not just Command Line Tools
- Systems with only Command Line Tools installed get `AttributeError: 'NoneType' object has no attribute 'groupdict'` when `node-gyp` tries to parse non-existent version output

## Solution Implemented
Created a mock `xcodebuild` script that provides the version information `node-gyp` expects, allowing native compilation to proceed using the available Command Line Tools.

## Installation Steps

### 1. Create Mock xcodebuild Script
```bash
mkdir -p ~/.local/bin
cat > ~/.local/bin/xcodebuild << 'EOF'
#!/bin/bash
if [[ "$1" == "-version" ]]; then
    echo "Xcode 15.0"
    echo "Build version 15A240d"
else
    echo "Error: Mock xcodebuild - install full Xcode for actual functionality" >&2
    exit 1
fi
EOF
chmod +x ~/.local/bin/xcodebuild
```

### 2. Update Shell Configuration
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### 3. Install Promptfoo
```bash
npm install promptfoo
```

### 4. Verify Installation
```bash
npx promptfoo --version
npx promptfoo init --no-interactive
```

## Verification Results
- ✅ `npx promptfoo --version` returns `0.117.3`
- ✅ `npx promptfoo init` creates working configuration files
- ✅ Installation completed without compilation errors
- ✅ Ready for integration with Discernus agents

## Integration with Discernus
The installation is ready to work with the Discernus agent system located at:
- **Agent Directory**: `/Volumes/code/discernus/discernus/agents/`
- **Python Virtual Environment**: `./venv/` (activated automatically)

## Future Considerations
- This workaround bypasses Xcode version detection but preserves all functionality needed for LLM evaluation
- If full Xcode development features are needed later, install Xcode from Mac App Store and remove the mock script
- The mock script only responds to `-version` flag; other `xcodebuild` commands will fail gracefully

## Troubleshooting
If issues persist:
1. Verify PATH includes `~/.local/bin`: `echo $PATH`
2. Check mock script permissions: `ls -la ~/.local/bin/xcodebuild`
3. Test mock script directly: `xcodebuild -version`
4. Clear npm cache: `npm cache clean --force`

## Environment Details
- **OS**: macOS (darwin 24.5.0)
- **Node.js**: v24.2.0
- **npm**: 11.4.2
- **Shell**: `/bin/zsh`
- **Development Tools**: Command Line Tools (no full Xcode)

---
**Mission Status: ✅ COMPLETED**
- Promptfoo successfully installed and verified
- Ready for implementation of Pillar 3 (Systematic Evals)
- Environment fixer agent mission accomplished 