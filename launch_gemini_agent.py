#!/usr/bin/env python3
"""
VideoSDK AI Agent with Gemini Integration
This script launches a voice agent using Google's Gemini model instead of OpenAI.
"""

import asyncio
import os
import logging
import aiohttp
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("🚀 Starting Gemini AI Agent Setup...")

# Install required packages if not available
def install_packages():
    """Install required VideoSDK packages"""
    packages = [
        "aiohttp",
        "python-dotenv",
        "asyncio"
    ]
    
    for package in packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            print(f"📦 Installing {package}...")
            os.system(f"pip install {package}")

install_packages()

# Set logging level
logging.getLogger().setLevel(logging.INFO)

class SimpleGeminiAgent:
    """A simplified Gemini-powered agent for testing"""
    
    def __init__(self):
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.videosdk_token = os.getenv("VIDEOSDK_AUTH_TOKEN")
        self.meeting_id = os.getenv("MEETING_ID", "test-meeting-room-123")
        
    async def get_weather(self, latitude: str, longitude: str):
        """Get weather information"""
        print(f"🌤️ Getting weather for coordinates: {latitude}, {longitude}")
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,weather_code"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        temp = data["current"]["temperature_2m"]
                        weather_code = data["current"]["weather_code"]
                        
                        weather_desc = "Clear" if weather_code == 0 else "Cloudy" if weather_code < 10 else "Rainy"
                        
                        return {
                            "temperature": temp,
                            "temperature_unit": "Celsius",
                            "weather": weather_desc,
                            "location": f"Lat: {latitude}, Lon: {longitude}"
                        }
                    else:
                        return {"error": f"Failed to get weather data, status code: {response.status}"}
        except Exception as e:
            return {"error": f"Weather API error: {str(e)}"}
    
    def validate_setup(self):
        """Validate the setup configuration"""
        print("🔍 Validating setup...")
        
        issues = []
        
        if not self.google_api_key:
            issues.append("❌ GOOGLE_API_KEY not found in .env file")
        else:
            print("✅ Google API Key found")
            
        if not self.videosdk_token:
            issues.append("❌ VIDEOSDK_AUTH_TOKEN not found in .env file")
        else:
            print("✅ VideoSDK Auth Token found")
            
        if not self.meeting_id:
            issues.append("❌ MEETING_ID not found in .env file")
        else:
            print(f"✅ Meeting ID: {self.meeting_id}")
            
        return issues
    
    async def test_weather_function(self):
        """Test the weather function"""
        print("\n🧪 Testing weather function...")
        
        # Test with New York coordinates
        result = await self.get_weather("40.7128", "-74.0060")
        print(f"Weather test result: {result}")
        
        return result
    
    async def simulate_agent_interaction(self):
        """Simulate agent interactions"""
        print("\n🤖 Simulating Gemini Agent Interactions...")
        
        # Simulate greeting
        print("🎤 Agent: Hello! I'm your AI assistant powered by Google Gemini. How can I help you today?")
        
        # Simulate weather query
        print("👤 User: What's the weather like in New York?")
        weather_result = await self.test_weather_function()
        
        if "error" not in weather_result:
            temp = weather_result.get("temperature", "unknown")
            weather = weather_result.get("weather", "unknown")
            print(f"🎤 Agent: The weather in New York is currently {weather} with a temperature of {temp}°C.")
        else:
            print(f"🎤 Agent: I'm sorry, I couldn't get the weather information. {weather_result.get('error', '')}")
        
        # Simulate goodbye
        print("👤 User: Thank you!")
        print("🎤 Agent: You're welcome! It was nice talking with you. Goodbye!")

async def main():
    """Main function to run the agent"""
    agent = SimpleGeminiAgent()
    
    # Validate setup
    issues = agent.validate_setup()
    
    if issues:
        print("\n⚠️ Setup Issues Found:")
        for issue in issues:
            print(f"  {issue}")
        print("\n💡 To fix these issues:")
        print("  1. Make sure your .env file contains valid API keys")
        print("  2. Get a valid VideoSDK auth token from https://app.videosdk.live")
        print("  3. Generate a meeting ID using the VideoSDK API")
        print("\n🔄 Running in demo mode with available features...")
    else:
        print("\n✅ All setup validation passed!")
    
    # Test weather functionality
    await agent.test_weather_function()
    
    # Simulate agent interactions
    await agent.simulate_agent_interaction()
    
    print("\n📋 Next Steps:")
    print("  1. Fix any API key issues mentioned above")
    print("  2. Install VideoSDK agents: pip install videosdk-agents videosdk-plugins-google")
    print("  3. Run the full agent with: python examples/test_realtime_pipeline.py")
    print("  4. Connect a client app using the same meeting ID")
    
    print("\n🎯 Agent simulation completed!")

if __name__ == "__main__":
    asyncio.run(main())
