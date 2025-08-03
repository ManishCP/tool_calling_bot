# Tool Calling Bot - Assignment

AI chatbot that can use external tools to solve problems.

## Current Status: Task 1 Complete

- Basic chat interface working
- Anthropic Claude API integration
- Conversation history management
- Error handling for network/API issues
- Clean project structure

## Setup Instructions

### 1. Environment Setup
```bash
# Navigate to project
cd tool_calling_bot

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

## Current Status: Task 2 Complete ✅

- ✅ Basic chat interface working
- ✅ Anthropic Claude API integration  
- ✅ Conversation history management
- ✅ Error handling for network/API issues
- ✅ **Three tools implemented and tested**
- ⏳ Tool calling integration (Task 3)

## Available Tools

### 🧮 Calculator Tool
- **Purpose**: Safe mathematical expression evaluation
- **Supports**: Basic operations (+, -, *, /, **), functions (sqrt, sin, cos, tan, log), constants (pi, e)
- **Security**: Uses AST parsing to prevent code injection
- **Example**: `calculator_tool("sqrt(16) + 2 * 3")` → `"Result: 10"`

### 🕐 Time Tool  
- **Purpose**: Get current time in any timezone
- **Supports**: 500+ worldwide timezones
- **Format**: Human-readable with timezone abbreviations
- **Example**: `get_current_time("Asia/Tokyo")` → `"Current time in Asia/Tokyo: Saturday, August 03, 2024 at 12:30:45 AM JST"`

### 🔍 Web Search Tool
- **Purpose**: Search the web for information
- **Service**: DuckDuckGo Instant Answer API (free)
- **Returns**: Definitions, facts, related topics with sources
- **Example**: `web_search("Python programming", 2)` → Structured search results

## Testing Tools

Test tools independently:
```bash
python3 tools.py