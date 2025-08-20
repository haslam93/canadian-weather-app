#!/usr/bin/env python3
"""
Canadian Weather CLI App
A command-line tool to get weather information for Canadian postal codes.
Uses free APIs that don't require registration.
"""

import requests
import json
import sys
import re
import argparse
from typing import Dict, Optional

class WeatherApp:
    def __init__(self):
        # Using OpenWeatherMap's free tier (no API key needed for some endpoints)
        # Alternative: Using wttr.in which is completely free
        self.base_url = "https://wttr.in"
        
    def validate_postal_code(self, postal_code: str) -> bool:
        """
        Validate Canadian postal code format (A1A 1A1 or A1A1A1)
        """
        # Remove spaces and convert to uppercase
        postal_code = postal_code.replace(" ", "").upper()
        
        # Canadian postal code pattern
        pattern = r'^[ABCEGHJ-NPRSTVXY]\d[ABCEGHJ-NPRSTV-Z]\d[ABCEGHJ-NPRSTV-Z]\d$'
        
        return bool(re.match(pattern, postal_code))
    
    def format_postal_code(self, postal_code: str) -> str:
        """
        Format postal code to standard format (A1A 1A1)
        """
        postal_code = postal_code.replace(" ", "").upper()
        if len(postal_code) == 6:
            return f"{postal_code[:3]} {postal_code[3:]}"
        return postal_code
    
    def get_weather_data(self, postal_code: str) -> Optional[Dict]:
        """
        Fetch weather data for the given postal code
        """
        try:
            # Format the postal code for the API
            formatted_postal = self.format_postal_code(postal_code)
            
            # Use wttr.in API with JSON format
            url = f"{self.base_url}/{formatted_postal},Canada"
            
            # Request JSON format
            params = {
                'format': 'j1',  # JSON format
                'lang': 'en'     # English language
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error parsing weather data: {e}")
            return None
    
    def display_weather(self, weather_data: Dict, postal_code: str):
        """
        Display weather information in a formatted way
        """
        try:
            current = weather_data['current_condition'][0]
            location = weather_data['nearest_area'][0]
            
            print("\n" + "="*50)
            print(f"🌤️  WEATHER FOR {self.format_postal_code(postal_code)}")
            print("="*50)
            
            # Location information
            area_name = location.get('areaName', [{}])[0].get('value', 'Unknown')
            region = location.get('region', [{}])[0].get('value', 'Unknown')
            country = location.get('country', [{}])[0].get('value', 'Unknown')
            
            print(f"📍 Location: {area_name}, {region}, {country}")
            print(f"🌡️  Temperature: {current['temp_C']}°C ({current['temp_F']}°F)")
            print(f"🌤️  Condition: {current['weatherDesc'][0]['value']}")
            print(f"🌪️  Feels like: {current['FeelsLikeC']}°C ({current['FeelsLikeF']}°F)")
            print(f"💨 Wind: {current['windspeedKmph']} km/h {current['winddir16Point']}")
            print(f"💧 Humidity: {current['humidity']}%")
            print(f"🔍 Visibility: {current['visibility']} km")
            print(f"☁️  Cloud Cover: {current['cloudcover']}%")
            
            # Today's forecast
            if 'weather' in weather_data and weather_data['weather']:
                today = weather_data['weather'][0]
                print(f"\n📅 Today's Forecast:")
                print(f"   🌡️  High: {today['maxtempC']}°C ({today['maxtempF']}°F)")
                print(f"   🌡️  Low: {today['mintempC']}°C ({today['mintempF']}°F)")
                print(f"   🌅 Sunrise: {today['astronomy'][0]['sunrise']}")
                print(f"   🌇 Sunset: {today['astronomy'][0]['sunset']}")
            
            print("="*50)
            
        except KeyError as e:
            print(f"Error parsing weather data: Missing key {e}")
        except Exception as e:
            print(f"Error displaying weather: {e}")
    
    def run(self, postal_code: str):
        """
        Main method to run the weather app
        """
        # Validate postal code
        if not self.validate_postal_code(postal_code):
            print("❌ Invalid Canadian postal code format!")
            print("Please use format: A1A 1A1 or A1A1A1")
            print("Example: K1A 0A6 or M5V3A8")
            return False
        
        print(f"🔍 Fetching weather for {self.format_postal_code(postal_code)}...")
        
        # Get weather data
        weather_data = self.get_weather_data(postal_code)
        
        if weather_data is None:
            print("❌ Failed to fetch weather data. Please try again later.")
            return False
        
        # Display weather
        self.display_weather(weather_data, postal_code)
        return True

def main():
    parser = argparse.ArgumentParser(
        description="Get weather information for Canadian postal codes",
        epilog="Example: python weather_app.py K1A0A6"
    )
    
    parser.add_argument(
        'postal_code',
        help='Canadian postal code (format: A1A 1A1 or A1A1A1)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Canadian Weather CLI 1.0.0'
    )
    
    args = parser.parse_args()
    
    # Create and run the weather app
    app = WeatherApp()
    success = app.run(args.postal_code)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
