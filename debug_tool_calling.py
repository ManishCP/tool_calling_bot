from tools import calculator_tool, get_current_time, web_search, execute_tool

def test_tool_execution_directly():
    """Test the execute_tool function that Claude will use"""
    print("🔧 Testing Tool Execution Function")
    print("=" * 50)
    
    test_cases = [
        # Calculator tests
        ("calculator_tool", {"expression": "2 + 3 * 4"}),
        ("calculator_tool", {"expression": "sqrt(16)"}),
        ("calculator_tool", {"expression": "15 * 847 / 100"}),
        
        # Time tests  
        ("get_current_time", {"timezone": "UTC"}),
        ("get_current_time", {"timezone": "Asia/Tokyo"}),
        ("get_current_time", {}),  # Test default parameter
        
        # Web search tests
        ("web_search", {"query": "Python programming"}),
        ("web_search", {"query": "AI", "num_results": 2}),
        
        # Error tests
        ("nonexistent_tool", {"param": "value"}),
        ("calculator_tool", {"wrong_param": "value"}),
    ]
    
    for tool_name, tool_args in test_cases:
        print(f"\n🛠️  Testing: {tool_name} with {tool_args}")
        result = execute_tool(tool_name, tool_args)
        print(f"   Result: {result[:100]}{'...' if len(result) > 100 else ''}")

def simulate_claude_tool_calls():
    """Simulate the exact tool calls Claude would make"""
    print("\n🎭 Simulating Claude Tool Call Scenarios")
    print("=" * 50)
    
    scenarios = [
        {
            "user_query": "What's 15% of 847?",
            "expected_tool": "calculator_tool",
            "expected_args": {"expression": "15 * 847 / 100"}
        },
        {
            "user_query": "What time is it in Tokyo?", 
            "expected_tool": "get_current_time",
            "expected_args": {"timezone": "Asia/Tokyo"}
        },
        {
            "user_query": "Search for Python tutorials",
            "expected_tool": "web_search", 
            "expected_args": {"query": "Python tutorials", "num_results": 3}
        }
    ]
    
    for scenario in scenarios:
        print(f"\n📝 Scenario: '{scenario['user_query']}'")
        print(f"   Expected tool: {scenario['expected_tool']}")
        print(f"   Expected args: {scenario['expected_args']}")
        
        result = execute_tool(scenario['expected_tool'], scenario['expected_args'])
        print(f"   Tool result: {result[:80]}{'...' if len(result) > 80 else ''}")

def test_tool_schemas():
    """Test that tool schemas are properly formatted"""
    from tools import TOOL_SCHEMAS
    
    print("\n📋 Testing Tool Schemas")
    print("=" * 50)
    
    for i, schema in enumerate(TOOL_SCHEMAS):
        print(f"\n🛠️  Tool {i+1}: {schema['name']}")
        print(f"   Description: {schema['description'][:60]}...")
        print(f"   Parameters: {list(schema['input_schema']['properties'].keys())}")
        print(f"   Required: {schema['input_schema'].get('required', [])}")

if __name__ == "__main__":
    test_tool_execution_directly()
    simulate_claude_tool_calls()
    test_tool_schemas()