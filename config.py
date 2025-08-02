import os
from typing import Optional

class Config:
    """Configuration class for API keys and settings"""

    def __init__(self):
        # Try to load from environment variables first
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')

        # If no key found in environment, prompt user
        if not self.anthropic_api_key:
            self._prompt_for_key()

    def _prompt_for_key(self):
        """Prompt user for API key if not found in environment"""
        print("\n" + "="*50)
        print("API Key Setup")
        print("="*50)
        print("No ANTHROPIC_API_KEY environment variable found.")
        print("Please enter your Anthropic API key.")
        print("(Get one from: https://console.anthropic.com/)")
        print("-"*50)

        self.anthropic_api_key = input("Enter your API key: ").strip()

        if not self.anthropic_api_key:
            raise ValueError("API key is required to run the bot")
        
        if not self.anthropic_api_key.startswith('sk-ant-'):
            print("Warning: API key should start with 'sk-ant-'")
            confirm = input("Continue anyway? (y/n): ").lower()
            if confirm != 'y':
                raise ValueError("Invalid API key format")
            
        print("API key configured successfully!")

#Global config instance that other files can import
config = Config()