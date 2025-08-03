import ast
import operator
import math
import requests
from datetime import datetime
import pytz
from typing import Dict, Any
import json
import re


def calculator_tool(expression: str) -> str:
    """
    Safely evaluate mathematical expressions.
    
    Args:
        expression: Math expression like "2 + 3 * 4" or "sqrt(16)"
    
    Returns:
        String with the calculation result
    """
    try:
        # Clean the input expression
        expression = expression.strip()

        if not expression:
            return "Error: Empty expression provided"
        
        # Replace common mathematical functions with math module equivalents
        # This allows users to write "sqrt(16)" instead of "math.sqrt(16)"
        replacements = {
            'sqrt': 'math.sqrt',
            'sin': 'math.sin',
            'cos': 'math.cos', 
            'tan': 'math.tan',
            'log': 'math.log',
            'ln': 'math.log',      # Natural logarithm
            'log10': 'math.log10', # Base 10 logarithm
            'abs': 'abs',          # Absolute value (built-in)
            'pi': 'math.pi',       # Pi constant
            'e': 'math.e',         # Euler's number
            'ceil': 'math.ceil',   # Ceiling function
            'floor': 'math.floor', # Floor function
            'pow': 'pow'           # Power function
        }

        # Apply replacements to make user-friendly functions work
        for old, new in replacements.items():
            # Use word boundaries to avoid replacing parts of words
            expression = re.sub(r'\b' + old + r'\b', new, expression)

        # Parse the expression into an Abstract Syntax Tree
        # This is MUCH safer than using eval() directly
        try:
            node = ast.parse(expression, mode='eval')
        except SyntaxError:
            return f"Error: Invalid mathematical syntax in '{expression}'"
        
        # Evaluate the AST safely
        # We only allow math operations and the math module
        allowed_names = {
            'math': math,
            'abs': abs,
            'pow': pow,
            'round': round,
            'min': min,
            'max': max
        }

        result = eval(compile(node, '<string>', 'eval'), 
                     {"__builtins__": {}, **allowed_names})

        # Format the result nicely
        if isinstance(result, float):
            # Round to reasonable precision
            if result.is_integer():
                result = int(result)
            else:
                result = round(result, 6)
        
        return f"Result: {result}"
    
    except ZeroDivisionError:
        return "Error: Division by zero is undefined"
    except OverflowError:
        return "Error: Number too large to calculate"
    except ValueError as e:
        return f"Error: Invalid value - {str(e)}"
    except TypeError as e:
        return f"Error: Invalid operation - {str(e)}"
    except Exception as e:
        return f"Error: Could not calculate '{expression}' - {str(e)}"


def get_current_time(timezone: str = "UTC") -> str:
    """
    Get current time in specified timezone.

    Args:
        timezone: Timezone string like "UTC", "US/Eastern", "Asia/Tokyo"

    Returns:
        Formatted time string with timezone info
    """
    try:
        # Get current UTC time first
        utc_now = datetime.now(pytz.UTC)

        # Handle timezone conversion
        if timezone.upper() == "UTC":
            target_tz = pytz.UTC
            local_time = utc_now
        else:
            try:
                # Try to get the specified timezone
                target_tz = pytz.timezone(timezone)
                local_time = utc_now.astimezone(target_tz)
            except pytz.exceptions.UnknownTimeZoneError:
                # Provide helpful error with suggestions
                return (f"Error: Unknown timezone '{timezone}'. "
                       f"Try: 'UTC', 'US/Eastern', 'US/Pacific', 'US/Central', "
                       f"'Europe/London', 'Asia/Tokyo', 'Australia/Sydney'")
            
        # Format the time in a user-friendly way
        formatted_time = local_time.strftime("%A, %B %d, %Y at %I:%M:%S %p %Z")

        # Add additional info for context
        if timezone.upper() == "UTC":
            result = f"Current UTC time: {formatted_time}"
        else:
            result = f"Current time in {timezone}: {formatted_time}"
            
            # Also show UTC for reference
            utc_formatted = utc_now.strftime("%I:%M:%S %p UTC")
            result += f"\n(UTC: {utc_formatted})"

        return result
    
    except Exception as e:
        return f"Error: Could not get time for timezone '{timezone}' - {str(e)}"


def web_search(query: str, num_results: int = 3) -> str:
    """
    Search the web and return top results using DuckDuckGo Instant Answer API.
    
    Args:
        query: Search terms
        num_results: Number of results to return (1-5)
    
    Returns:
        Formatted string with search results
    """
    try:
        # Validate inputs
        if not query.strip():
            return "Error: Empty search query provided"
        
        # Limit num_results to reasonable range
        num_results = max(1, min(5, num_results))
        
        # Clean the query
        query = query.strip()
        
        # Use DuckDuckGo Instant Answer API (free, no key required)
        url = "https://api.duckduckgo.com/"
        params = {
            'q': query,           # Query string
            'format': 'json',     # Want JSON response
            'no_html': '1',       # No HTML in responses
            'skip_disambig': '1'  # Skip disambiguation pages
        }
        
        # Make the API request
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        data = response.json()
        
        # Try to extract meaningful results from DuckDuckGo's response
        results = []
        
        # Check for instant answer (direct factual response)
        if data.get('Answer'):
            results.append(f"📋 Direct Answer: {data['Answer']}")
        
        # Check for abstract/definition
        if data.get('Abstract'):
            abstract = data['Abstract']
            # Limit length to keep response manageable
            if len(abstract) > 200:
                abstract = abstract[:197] + "..."
            results.append(f"📖 Definition: {abstract}")
            
            # Add source if available
            if data.get('AbstractURL'):
                results.append(f"🔗 Source: {data['AbstractURL']}")
        
        # Check for related topics (usually the most useful for general queries)
        if data.get('RelatedTopics'):
            for i, topic in enumerate(data['RelatedTopics'][:num_results]):
                if isinstance(topic, dict) and topic.get('Text'):
                    topic_text = topic['Text']
                    # Limit length
                    if len(topic_text) > 150:
                        topic_text = topic_text[:147] + "..."
                    
                    results.append(f"🔍 Result {i+1}: {topic_text}")
                    
                    # Add URL if available
                    if topic.get('FirstURL'):
                        results.append(f"   🔗 {topic['FirstURL']}")
        
        # Check for infobox data (useful for entities like people, places)
        if data.get('Infobox') and data['Infobox'].get('content'):
            infobox_items = []
            for item in data['Infobox']['content'][:3]:  # Limit to first 3 items
                if item.get('label') and item.get('value'):
                    infobox_items.append(f"{item['label']}: {item['value']}")
            
            if infobox_items:
                results.append(f"ℹ️  Quick Facts: {'; '.join(infobox_items)}")
        
        # If we found good results, format them nicely
        if results:
            result_text = f"🔎 Search results for '{query}':\n\n"
            result_text += "\n\n".join(results)
            return result_text
        
        # If no structured results, provide a basic response
        else:
            return (f"🔎 Searched for '{query}' but didn't find detailed instant answers. "
                   f"This is normal with DuckDuckGo's API - it provides structured data "
                   f"for some queries but not others. The search was successful though!")
            
    except requests.exceptions.ConnectionError:
        return "🌐 Error: Could not connect to search service. Check your internet connection."
    
    except requests.exceptions.Timeout:
        return "⏰ Error: Search request timed out. Please try again."
    
    except requests.exceptions.RequestException as e:
        return f"🔍 Error: Search service issue - {str(e)}"
    
    except json.JSONDecodeError:
        return "📄 Error: Could not parse search results. Please try again."
    
    except Exception as e:
        return f"❌ Error: Could not perform web search - {str(e)}"


# Tool registry - maps tool names to functions
TOOL_FUNCTIONS = {
    "calculator_tool": calculator_tool,
    "get_current_time": get_current_time,
    "web_search": web_search
}

def execute_tool(tool_name: str, tool_args: Dict[str, Any]) -> str:
    """
    Execute a tool by name with given arguments.
    
    Args:
        tool_name: Name of the tool to execute
        tool_args: Dictionary of arguments to pass to the tool
    
    Returns:
        String result from the tool execution
    """
    if tool_name not in TOOL_FUNCTIONS:
        available_tools = ", ".join(TOOL_FUNCTIONS.keys())
        return f"❌ Error: Unknown tool '{tool_name}'. Available tools: {available_tools}"
    
    try:
        tool_function = TOOL_FUNCTIONS[tool_name]
        result = tool_function(**tool_args)
        return result
    except TypeError as e:
        return f"❌ Error: Invalid arguments for tool '{tool_name}' - {str(e)}"
    except Exception as e:
        return f"❌ Error: Tool '{tool_name}' failed - {str(e)}"

# Test function to verify tools work correctly
def test_all_tools():
    """Test all tools to verify they work correctly"""
    print("🧪 Testing All Tools")
    print("=" * 50)
    
    # Test calculator
    print("🧮 Calculator Tests:")
    calc_tests = ["2 + 3 * 4", "sqrt(16)", "sin(pi/2)", "15 * 847 / 100"]
    for test in calc_tests:
        result = calculator_tool(test)
        print(f"  {test} → {result}")
    
    print("\n🕐 Time Tests:")
    time_tests = ["UTC", "US/Eastern", "Asia/Tokyo"]
    for test in time_tests:
        result = get_current_time(test)
        print(f"  {test} → {result}")
    
    print("\n🔍 Web Search Tests:")
    search_tests = ["Python programming", "artificial intelligence"]
    for test in search_tests:
        result = web_search(test, 2)
        print(f"  '{test}' → {result[:100]}...")

if __name__ == "__main__":
    # Run tests when tools.py is executed directly
    test_all_tools()