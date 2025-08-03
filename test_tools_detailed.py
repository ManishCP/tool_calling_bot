from tools import calculator_tool, get_current_time, web_search

def test_calculator_errors():
    """Test calculator error handling"""
    print("🧮 Calculator Error Tests:")
    print("-" * 40)
    
    error_tests = [
        ("", "Empty expression"),
        ("2 + + 3", "Syntax error"),
        ("10 / 0", "Division by zero"),
        ("sqrt(-1)", "Invalid operation"),
        ("hello + world", "Invalid variables"),
        ("import os", "Security test"),
        ("2 ** 1000", "Very large number"),
        (")", "Unmatched parenthesis")
    ]
    
    for test_expr, description in error_tests:
        result = calculator_tool(test_expr)
        print(f"  Test: {description}")
        print(f"    Input: '{test_expr}'")
        print(f"    Result: {result}")
        print()

def test_time_errors():
    """Test time tool error handling"""
    print("🕐 Time Error Tests:")
    print("-" * 40)
    
    error_tests = [
        ("Invalid/Timezone", "Invalid timezone format"),
        ("Mars/Central", "Non-existent timezone"), 
        ("", "Empty timezone"),
        ("12345", "Numeric timezone"),
        ("US/InvalidCity", "Invalid US timezone")
    ]
    
    for test_tz, description in error_tests:
        result = get_current_time(test_tz)
        print(f"  Test: {description}")
        print(f"    Input: '{test_tz}'")
        print(f"    Result: {result}")
        print()

def test_search_errors():
    """Test web search error handling"""
    print("🔍 Search Error Tests:")
    print("-" * 40)
    
    error_tests = [
        ("", "Empty query"),
        ("   ", "Whitespace only"),
        ("a" * 100, "Very long query"),
        ("!@#$%^&*()", "Special characters only")
    ]
    
    for test_query, description in error_tests:
        result = web_search(test_query, 1)
        print(f"  Test: {description}")
        print(f"    Input: '{test_query[:20]}{'...' if len(test_query) > 20 else ''}'")
        print(f"    Result: {result[:80]}{'...' if len(result) > 80 else ''}")
        print()

def test_calculator_success():
    """Test calculator with valid inputs"""
    print("✅ Calculator Success Tests:")
    print("-" * 40)
    
    success_tests = [
        ("2 + 3 * 4", "Order of operations"),
        ("sqrt(16)", "Square root"),
        ("sin(pi/2)", "Trigonometry"),
        ("15 * 847 / 100", "Percentage calculation"),
        ("abs(-5)", "Absolute value"),
        ("ceil(4.2)", "Ceiling function"),
        ("floor(4.8)", "Floor function")
    ]
    
    for test_expr, description in success_tests:
        result = calculator_tool(test_expr)
        print(f"  Test: {description}")
        print(f"    Input: '{test_expr}'")
        print(f"    Result: {result}")
        print()

def test_time_success():
    """Test time tool with valid inputs"""
    print("✅ Time Success Tests:")
    print("-" * 40)
    
    success_tests = [
        ("UTC", "Coordinated Universal Time"),
        ("US/Eastern", "US Eastern Time"),
        ("US/Pacific", "US Pacific Time"),
        ("Asia/Tokyo", "Japan Standard Time"),
        ("Europe/London", "British Time"),
        ("Australia/Sydney", "Australian Eastern Time")
    ]
    
    for test_tz, description in success_tests:
        result = get_current_time(test_tz)
        print(f"  Test: {description}")
        print(f"    Input: '{test_tz}'")
        print(f"    Result: {result}")
        print()

def test_search_success():
    """Test web search with valid inputs"""
    print("✅ Search Success Tests:")
    print("-" * 40)
    
    success_tests = [
        ("Python programming", "Programming language"),
        ("artificial intelligence", "AI topic"),
        ("Albert Einstein", "Famous person"),
        ("Tokyo", "City/place"),
        ("2024", "Year/date")
    ]
    
    for test_query, description in success_tests:
        result = web_search(test_query, 2)
        print(f"  Test: {description}")
        print(f"    Input: '{test_query}'")
        print(f"    Result: {result[:100]}{'...' if len(result) > 100 else ''}")
        print()

def run_comprehensive_tests():
    """Run all tests - both error cases and success cases"""
    print("🧪 COMPREHENSIVE TOOL TESTING")
    print("=" * 60)
    print("Testing error handling and normal functionality")
    print("=" * 60)
    
    # Test error handling first
    test_calculator_errors()
    test_time_errors()
    test_search_errors()
    
    print("\n" + "=" * 60)
    print("Now testing normal functionality")
    print("=" * 60)
    
    # Test normal functionality
    test_calculator_success()
    test_time_success()
    test_search_success()
    
    print("🎉 ALL TESTS COMPLETED!")
    print("📋 Summary:")
    print("  ✅ Calculator: Error handling + math operations")
    print("  ✅ Time: Error handling + timezone conversions")
    print("  ✅ Search: Error handling + web API integration")

if __name__ == "__main__":
    run_comprehensive_tests()