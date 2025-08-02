import anthropic
import sys
from config import config

class BasicChatBot:
    """Basic chatbot for Task 1 - Foundatin without tool calling"""

    def __init__(self):
        """Initialize the bot with Claude API client"""
        try:
            # Create Anthropic cliet with our API key
            self.client = anthropic.Anthropic(api_key=config.anthropic_api_key)

            #Initialize empty conversation history
            self.conversation_history = []

            # Success message
            print("Basic Chat Bot initialized successfully!")
            print("You can now chat with Claude")
            print("Type 'quit', 'exit', or 'bye' to end")
            print("- "*60)

        except Exception as e:
            print(f"Failed to initialize bot: {str(e)}")
            print("Check your API key and internet connection")
            sys.exit(1)

    def chat_loop(self):
        """Main conversation loop - keeps running until user quits"""
        print("Chat Started! Say hello to begin.\n")

        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()

                # Handle quit commands
                if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                    print("\n Thanks for chatting! Goodbye!")
                    break

                # Handle empty input:
                if not user_input:
                    print("\n Please enter a message to continue.")
                    continue

                print(" Thinking...")
                response = self.get_claude_response(user_input)
                print(f"Bot: {response}\n")

            except KeyboardInterrupt:
                print("\n\n Chat interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"Unexcepted error: {str(e)}")
                print("Please try again or type 'quit' to exit. \n")

    
    def get_claude_response(self, user_message):
        """Get response from Claude API with error handling"""

        try:
            # Add user message to conversation history
            self.conversation_history.append({
                "role": "user",
                "content": user_message
            })

            reponse = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                messages=self.conversation_history
            )

            # Extract the text response from Claude's response
            response_text = reponse.content[0].text

            # Add Claude's response to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": response_text
            })

            return response_text
        
        except anthropic.AuthenticationError:
            return "Authentication failed. Please check your API key is correct."
        
        except anthropic.RateLimitError:
            return "Rate limit exceeded. Please wait a moment and try again."
        
        except anthropic.APIConnectionError:
            return "Connection failed. Please check your internet connection."
        
        except anthropic.BadRequestError as e:
            return f"Invalid request: {str(e)}"
        
        except Exception as e:
            return f"Unexpected error occurred: {str(e)}"

    def get_conversation_stats(self):
        """Helper method to show conversation statistics"""
        user_messages = len([msg for msg in self.conversation_history if msg["role"] == "user"])
        bot_messages = len([msg for msg in self.conversation_history if msg["role"] == "assistant"])
        return f"Conversation: {user_messages} user messages, {bot_messages} bot reponses"


def main():
    """Main funciton to run the chatbot"""
    print("Starting Tool Calling Bot - Foundation")
    print("Task 1: Basic Chat Interface")
    print("="*60)

    try:
        #Create and start the bot
        bot = BasicChatBot()
        bot.chat_loop()

        # Show stats when conversation ends
        print(bot.get_conversation_stats())

    except KeyboardInterrupt:
        print("\n Goodbye!")
    except Exception as e:
        print(f"Failed to start bot: {str(e)}")
        print("Make sure you have a valid API key and internet connection")
        sys.exit(1)


if __name__ == "__main__":
    main()