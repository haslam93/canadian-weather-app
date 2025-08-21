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
        
    def validate_canadian_postal_code(self, postal_code: str) -> bool:
        """
        Validate Canadian postal code format (A1A 1A1 or A1A1A1)
        """
        # Remove spaces and convert to uppercase
        postal_code = postal_code.replace(" ", "").upper()
        
        # Canadian postal code pattern
        pattern = r'^[ABCEGHJ-NPRSTVXY]\d[ABCEGHJ-NPRSTV-Z]\d[ABCEGHJ-NPRSTV-Z]\d$'
        
        return bool(re.match(pattern, postal_code))
    
    def validate_us_zip_code(self, zip_code: str) -> bool:
        """
        Validate US zip code format (12345 or 12345-6789)
        """
        # Remove spaces and keep only digits and dashes
        zip_code = re.sub(r'[^\d-]', '', zip_code)
        
        # US zip code patterns: 5 digits or 5 digits + 4 digits
        pattern_5 = r'^\d{5}$'
        pattern_9 = r'^\d{5}-\d{4}$'
        
        return bool(re.match(pattern_5, zip_code) or re.match(pattern_9, zip_code))
    
    def validate_postal_code(self, postal_code: str) -> bool:
        """
        Validate postal code format (Canadian A1A 1A1 or US 12345/12345-6789)
        """
        return (self.validate_canadian_postal_code(postal_code) or 
                self.validate_us_zip_code(postal_code))
    
    def format_postal_code(self, postal_code: str) -> str:
        """
        Format postal code to standard format (A1A 1A1 for Canadian, 12345 or 12345-6789 for US)
        """
        # Check if it's a Canadian postal code first
        if self.validate_canadian_postal_code(postal_code):
            cleaned = postal_code.replace(" ", "").upper()
            if len(cleaned) == 6:
                return f"{cleaned[:3]} {cleaned[3:]}"
            return cleaned
        
        # Check if it's a US zip code
        elif self.validate_us_zip_code(postal_code):
            # Remove all non-digit, non-dash characters for US zip codes
            zip_cleaned = re.sub(r'[^\d-]', '', postal_code)
            
            # If already has dash and is valid, return as-is
            if '-' in zip_cleaned and self.validate_us_zip_code(zip_cleaned):
                return zip_cleaned
            
            # Format 9-digit zip codes with dash if not already present
            if len(zip_cleaned) == 9 and '-' not in zip_cleaned:
                return f"{zip_cleaned[:5]}-{zip_cleaned[5:]}"
            
            return zip_cleaned
        
        # Try to format as US zip code if it could be a 9-digit zip without dash or with spaces
        digits_only = re.sub(r'[^\d]', '', postal_code)
        if len(digits_only) == 9:
            return f"{digits_only[:5]}-{digits_only[5:]}"
        elif len(digits_only) == 5:
            return digits_only
        
        # Return as-is if not recognized format
        return postal_code
    
    def get_weather_data(self, postal_code: str) -> Optional[Dict]:
        """
        Fetch weather data for the given postal code (Canadian or US)
        """
        try:
            # Format the postal code for the API
            formatted_postal = self.format_postal_code(postal_code)
            
            # Determine the country based on postal code format
            if self.validate_canadian_postal_code(postal_code):
                # Use wttr.in API with JSON format for Canada
                url = f"{self.base_url}/{formatted_postal},Canada"
            elif self.validate_us_zip_code(postal_code):
                # Use wttr.in API with JSON format for US (let it auto-detect)
                url = f"{self.base_url}/{formatted_postal}"
            else:
                print("Error: Invalid postal/zip code format")
                return None
            
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
            print("❌ Invalid postal code format!")
            print("Please use one of these formats:")
            print("  Canadian: A1A 1A1 or A1A1A1 (e.g., K1A 0A6, M5V3A8)")
            print("  US: 12345 or 12345-6789 (e.g., 10001, 90210-1234)")
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
        description="Get weather information for Canadian postal codes and US zip codes",
        epilog="Examples: python weather_app.py K1A0A6 or python weather_app.py 10001"
    )
    
    parser.add_argument(
        'postal_code',
        help='Canadian postal code (A1A 1A1) or US zip code (12345 or 12345-6789)'
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
