# AI Agent with Tool Calling Capabilities

An intelligent chatbot that can automatically use external tools to solve problems it cannot answer on its own. This project demonstrates the core concept of AI agents - systems that can reason about when and how to use tools to accomplish tasks.

## Project Overview

The objective was to create a chatbot that extends beyond simple conversation by integrating with external tools through direct API calls. The bot needed to automatically decide when tools are necessary and seamlessly incorporate tool results into natural language responses.

The challenge was building a system where an AI can:
- Recognize when it needs external capabilities
- Choose the appropriate tool for each task
- Execute tools with correct parameters
- Integrate results into coherent responses

## Implementation Approach

### Foundation Architecture
Built a modular system with clear separation of concerns:
- **Configuration layer**: Secure API key management
- **Tool layer**: Independent, testable tool functions
- **Integration layer**: LLM API communication with tool calling support
- **Interface layer**: User-friendly chat experience

### Tool Development
Implemented three distinct tools that address different AI limitations:

**Calculator Tool**: Addresses the LLM's weakness with precise mathematical computation. Uses Abstract Syntax Tree (AST) parsing for safe expression evaluation, preventing code injection while supporting mathematical functions like sqrt, sin, cos, and constants like pi.

**Time Tool**: Provides real-time information that LLMs cannot access. Implements comprehensive timezone handling using the pytz library, supporting 500+ worldwide timezones with proper daylight saving time calculations.

**Web Search Tool**: Extends the AI's knowledge beyond its training data. Integrates with DuckDuckGo's Instant Answer API to provide current information, definitions, and factual data with structured result formatting.

### Tool Calling Integration
The most complex aspect was implementing the tool calling protocol. This involved:
- Defining tool schemas that describe each tool's capabilities to the LLM
- Parsing tool call requests from the LLM's structured responses
- Executing tools with provided parameters and handling errors gracefully
- Managing conversation history that includes tool calls and results
- Implementing a two-phase response system where the LLM first identifies needed tools, then formulates a final response with tool results

## Key Learning Outcomes

Through this project, I gained understanding of:
- **AI Agent Architecture**: How intelligent systems extend their capabilities through external tools
- **LLM API Integration**: Working with modern language model APIs and their tool calling features
- **Secure Code Execution**: Using AST parsing to safely evaluate user expressions without security risks
- **Error Resilience**: Building systems that gracefully handle network failures, API limits, and invalid inputs
- **API Design**: Creating tool schemas and interfaces that LLMs can understand and use effectively

The project highlighted the difference between simple chatbots and intelligent agents - the ability to take action in the world through tools fundamentally changes what AI systems can accomplish.

## Setup and Installation

### Prerequisites
- Python 3.8 or higher
- Internet connection
- Anthropic API key (from console.anthropic.com)

### Installation Steps

1. **Download and extract the project files**
   ```bash
   cd tool_calling_bot
   ```

2. **Set up Python environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API access**
   ```bash
   export ANTHROPIC_API_KEY="your-api-key-here"
   ```
   Alternatively, the bot will prompt for the key when started.

5. **Run the bot**
   ```bash
   python3 main.py
   ```

### Testing Tools Independently
```bash
# Test all tools
python3 tools.py

# Test error handling
python3 test_tools_detailed.py

# Debug tool calling mechanism
python3 debug_tool_calling.py
```

## Usage Examples

### Mathematical Computations
```
You: What's 15% of 847?
Bot: 15% of 847 is 127.05

You: Calculate the square root of 144
Bot: The square root of 144 is 12

You: If I have 3 apples and buy 7 more, then eat 4, how many do I have?
Bot: You would have 6 apples (3 + 7 - 4 = 6)
```

### Time Queries
```
You: What time is it in Tokyo right now?
Bot: The current time in Tokyo is Monday, August 04, 2025 at 06:30:45 AM JST

You: Show me the time in London and New York
Bot: London: Sunday, August 03, 2025 at 10:30:45 PM BST
     New York: Sunday, August 03, 2025 at 05:30:45 PM EDT
```

### Information Lookup
```
You: Search for information about Python programming
Bot: Python is a high-level, general-purpose programming language known for its simplicity and readability...

You: Find recent news about artificial intelligence
Bot: Recent developments in AI include advances in machine learning models and their applications...
```

### Complex Multi-Tool Queries
```
You: What time is it in Tokyo, and what's 25% of 200?
Bot: The current time in Tokyo is Monday, August 04, 2025 at 06:30:45 AM JST. 
     25% of 200 is 50.

You: Search for Python tips and calculate 8 * 7
Bot: Here are some Python programming tips... [search results]
     8 * 7 equals 56.
```

## Tool Implementation Details

### Calculator Tool
The calculator addresses a fundamental limitation of language models: precise mathematical computation. Rather than relying on the LLM's approximations, it provides exact calculations using Python's math engine.

The implementation prioritizes security through AST parsing, which allows safe evaluation of mathematical expressions without the risks of arbitrary code execution. It supports common mathematical operations and functions while preventing potential security vulnerabilities.

### Time Tool  
Language models lack access to real-time information, making time queries impossible to answer accurately. This tool bridges that gap by providing current time information with proper timezone handling.

The tool handles the complexity of worldwide timezones, including daylight saving time transitions and regional variations. It provides both local time and UTC reference for clarity and context.

### Web Search Tool
This tool extends the AI's knowledge beyond its training data by enabling real-time information retrieval. It integrates with DuckDuckGo's API to provide current information, definitions, and factual data.

The implementation handles the variability of web API responses gracefully, extracting meaningful information when available and providing appropriate feedback when results are limited.

## Why This Project Matters

This project demonstrates the evolution from simple AI chatbots to intelligent agents capable of taking action. Tool calling represents a fundamental shift in AI capabilities - from passive text generation to active problem-solving through external resources.

The architecture created here serves as a foundation for more sophisticated AI systems that can:
- Access real-time data
- Perform complex computations
- Integrate with external services
- Chain multiple tools together for complex tasks

Understanding tool calling is essential for modern AI development, as it bridges the gap between AI reasoning and practical problem-solving capabilities.

## Project Structure

```
tool_calling_bot/
├── main.py                    # Main chat interface with tool calling
├── tools.py                   # Tool implementations and schemas
├── config.py                  # API configuration management
├── test_tools_detailed.py     # Comprehensive testing suite
├── debug_tool_calling.py      # Tool calling debug utilities
├── requirements.txt           # Project dependencies
└── README.md                  # This documentation
```

The modular design ensures each component has a single responsibility, making the codebase maintainable and extensible for future enhancements.