import anthropic
import sys
import json
from config import config
from tools import TOOL_SCHEMAS, execute_tool

class ToolCallingBot:
    """Enhanced chatbot with tool calling capabilities"""
    
    def __init__(self):
        """Initialize the bot with Claude API client and tool capabilities"""
        try:
            # Create Anthropic client with our API key
            self.client = anthropic.Anthropic(api_key=config.anthropic_api_key)
            
            # Initialize empty conversation history
            self.conversation_history = []
            
            # Tool call statistics for debugging
            self.tool_call_count = 0
            self.successful_tool_calls = 0
            
            # Success message
            print("🤖 Tool Calling Bot initialized successfully!")
            print("🛠️  Available tools: Calculator, Current Time, Web Search")
            print("🧠 Claude will automatically use tools when needed")
            print("🚪 Type 'quit', 'exit', or 'bye' to end")
            print("💡 Type 'stats' to see session statistics")
            print("-" * 70)
            
        except Exception as e:
            print(f"❌ Failed to initialize bot: {str(e)}")
            print("💡 Check your API key and internet connection")
            sys.exit(1)
    
    def chat_loop(self):
        """Main conversation loop with tool calling support"""
        print("🎯 Ready for tool-calling conversations!")
        print("💡 Try asking about math, time, or web searches...")
        print("Examples:")
        print("  • 'What's 15% of 847?'")
        print("  • 'What time is it in Tokyo?'") 
        print("  • 'Search for Python tutorials'")
        print("  • 'What time is it in London and what's 25% of 200?'")
        print()
        
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                # Handle quit commands
                if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                    self._show_session_stats()
                    print("👋 Thanks for testing the tool calling bot!")
                    break
                
                # Handle empty input
                if not user_input:
                    print("💭 Please enter a message to continue.")
                    continue
                
                # Handle special commands
                if user_input.lower() == 'stats':
                    self._show_session_stats()
                    continue
                
                if user_input.lower() == 'help':
                    self._show_help()
                    continue
                
                # Get response from Claude (with potential tool usage)
                print("🤔 Claude is thinking...")
                response = self.get_claude_response_with_tools(user_input)
                print(f"🤖 Bot: {response}\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Chat interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"❌ Unexpected error: {str(e)}")
                print("💡 Please try again or type 'quit' to exit.\n")
    
    def get_claude_response_with_tools(self, user_message):
        """Get response from Claude with tool calling support"""
        try:
            # Add user message to conversation history
            self.conversation_history.append({
                "role": "user",
                "content": user_message
            })
            
            # Make API call to Claude with tools available
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1500,
                messages=self.conversation_history,
                tools=TOOL_SCHEMAS  # This tells Claude about available tools
            )
            
            # Check if Claude wants to use tools
            if response.stop_reason == "tool_use":
                return self._handle_tool_calling_flow(response)
            else:
                return self._handle_regular_response(response)
                
        except anthropic.AuthenticationError:
            return "❌ Authentication failed. Please check your API key."
        except anthropic.RateLimitError:
            return "⏰ Rate limit exceeded. Please wait a moment and try again."
        except anthropic.APIConnectionError:
            return "🌐 Connection failed. Please check your internet connection."
        except anthropic.BadRequestError as e:
            return f"📝 Invalid request: {str(e)}"
        except Exception as e:
            return f"❌ Unexpected error: {str(e)}"
    
    def _handle_tool_calling_flow(self, response):
        """Handle the complete tool calling flow"""
        try:
            # Step 1: Add Claude's initial response (with tool calls) to history
            self.conversation_history.append({
                "role": "assistant",
                "content": response.content
            })
            
            # Step 2: Execute each tool call Claude requested
            tool_results = []
            tools_used = []
            
            for content_block in response.content:
                if content_block.type == "tool_use":
                    # Extract tool information
                    tool_name = content_block.name
                    tool_args = content_block.input
                    tool_id = content_block.id
                    
                    # Show user what tool is being used (for transparency)
                    print(f"🛠️  Using {tool_name} with: {tool_args}")
                    
                    # Execute the tool
                    tool_result = execute_tool(tool_name, tool_args)
                    tools_used.append(tool_name)
                    
                    # Track statistics
                    self.tool_call_count += 1
                    if not tool_result.startswith("❌ Error"):
                        self.successful_tool_calls += 1
                    
                    # Prepare tool result for Claude
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_id,
                        "content": tool_result
                    })
            
            # Step 3: Send tool results back to Claude
            self.conversation_history.append({
                "role": "user",
                "content": tool_results
            })
            
            # Step 4: Get Claude's final response incorporating tool results
            final_response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022", 
                max_tokens=1500,
                messages=self.conversation_history
            )
            
            # Step 5: Extract and return final response
            final_text = ""
            for content_block in final_response.content:
                if content_block.type == "text":
                    final_text += content_block.text
            
            # Add final response to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": final_response.content
            })
            
            # Add tool usage indicator to response
            tools_used_str = ", ".join(set(tools_used))
            return f"{final_text}\n\n🔧 (Used tools: {tools_used_str})"
            
        except Exception as e:
            return f"❌ Error during tool calling: {str(e)}"
    
    def _handle_regular_response(self, response):
        """Handle regular Claude response (no tools needed)"""
        try:
            # Extract text response
            response_text = ""
            for content_block in response.content:
                if content_block.type == "text":
                    response_text += content_block.text
            
            # Add to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": response.content
            })
            
            return response_text
            
        except Exception as e:
            return f"❌ Error processing response: {str(e)}"
    
    def _show_session_stats(self):
        """Show statistics about the current session"""
        user_messages = len([msg for msg in self.conversation_history if msg["role"] == "user"])
        # Subtract tool result messages from user message count
        tool_result_messages = len([msg for msg in self.conversation_history 
                                  if msg["role"] == "user" and isinstance(msg.get("content"), list)])
        actual_user_messages = user_messages - tool_result_messages
        
        assistant_messages = len([msg for msg in self.conversation_history if msg["role"] == "assistant"])
        
        print(f"\n📊 Session Statistics:")
        print(f"   💬 User messages: {actual_user_messages}")
        print(f"   🤖 Bot responses: {assistant_messages}")
        print(f"   🛠️  Total tool calls: {self.tool_call_count}")
        print(f"   ✅ Successful tool calls: {self.successful_tool_calls}")
        if self.tool_call_count > 0:
            success_rate = (self.successful_tool_calls / self.tool_call_count) * 100
            print(f"   📈 Tool success rate: {success_rate:.1f}%")
        print()
    
    def _show_help(self):
        """Show help information"""
        print("\n🆘 Help - Available Commands:")
        print("-" * 40)
        print("💬 Chat Commands:")
        print("  • 'quit', 'exit', 'bye' - End the conversation")
        print("  • 'stats' - Show session statistics")
        print("  • 'help' - Show this help message")
        print()
        print("🛠️  Tool Examples:")
        print("  Calculator:")
        print("    • 'What's 15% of 847?'")
        print("    • 'Calculate sqrt(144)'")
        print("    • 'If I have 3 apples and buy 7 more, then eat 4, how many do I have?'")
        print("  Time:")
        print("    • 'What time is it in Tokyo?'")
        print("    • 'Current time in New York?'")
        print("    • 'Show time in London and Paris'")
        print("  Web Search:")
        print("    • 'Search for Python tutorials'")
        print("    • 'Find information about artificial intelligence'")
        print("    • 'Look up the weather forecast'")
        print("  Multi-tool:")
        print("    • 'What time is it in Tokyo and what's 25% of 200?'")
        print("    • 'Search for Python tips and calculate 8 * 7'")
        print()

def main():
    """Main function to run the enhanced chatbot"""
    print("🚀 Starting Tool Calling Bot - FULL VERSION")
    print("📋 Task 3: Tool Calling Integration Complete")
    print("="*70)
    
    try:
        # Create and start the enhanced bot
        bot = ToolCallingBot()
        bot.chat_loop()
        
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Failed to start bot: {str(e)}")
        print("💡 Make sure you have a valid API key and internet connection")
        sys.exit(1)

if __name__ == "__main__":
    main()