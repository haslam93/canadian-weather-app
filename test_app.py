#!/usr/bin/env python3
"""
Test script for the Canadian Weather CLI App
"""

from weather_app import WeatherApp

def test_postal_code_validation():
    """Test postal code validation"""
    app = WeatherApp()
    
    # Valid postal codes
    valid_codes = [
        "K1A 0A6",
        "K1A0A6",
        "M5V 3A8", 
        "M5V3A8",
        "V6B 2W9",
        "T2P2Y5"
    ]
    
    # Invalid postal codes
    invalid_codes = [
        "12345",
        "ABCDEF",
        "K1A 0A",
        "K1A 0A67",
        "Z1A 0A6",  # Z is not valid
        "K1D 0A6"   # D is not valid in second position
    ]
    
    print("Testing valid postal codes:")
    for code in valid_codes:
        result = app.validate_postal_code(code)
        print(f"  {code}: {'✅ VALID' if result else '❌ INVALID'}")
    
    print("\nTesting invalid postal codes:")
    for code in invalid_codes:
        result = app.validate_postal_code(code)
        print(f"  {code}: {'✅ VALID' if result else '❌ INVALID'}")

def test_postal_code_formatting():
    """Test postal code formatting"""
    app = WeatherApp()
    
    test_cases = [
        ("k1a0a6", "K1A 0A6"),
        ("K1A 0A6", "K1A 0A6"),
        ("m5v3a8", "M5V 3A8"),
        ("M5V  3A8", "M5V 3A8")
    ]
    
    print("\nTesting postal code formatting:")
    for input_code, expected in test_cases:
        result = app.format_postal_code(input_code)
        status = "✅ PASS" if result == expected else "❌ FAIL"
        print(f"  '{input_code}' -> '{result}' (expected: '{expected}') {status}")

def test_weather_fetch():
    """Test weather data fetching with a known postal code"""
    app = WeatherApp()
    
    print("\nTesting weather data fetch for K1A 0A6 (Ottawa):")
    print("This will make an actual API call...")
    
    weather_data = app.get_weather_data("K1A 0A6")
    
    if weather_data:
        print("✅ Successfully fetched weather data")
        print("Keys in response:", list(weather_data.keys()))
        
        if 'current_condition' in weather_data:
            current = weather_data['current_condition'][0]
            print(f"Current temperature: {current['temp_C']}°C")
            print(f"Weather condition: {current['weatherDesc'][0]['value']}")
        
        return True
    else:
        print("❌ Failed to fetch weather data")
        return False

if __name__ == "__main__":
    print("🧪 Running Canadian Weather CLI App Tests\n")
    
    # Run tests
    test_postal_code_validation()
    test_postal_code_formatting()
    
    # Ask user if they want to test API call
    import sys
    
    try:
        response = input("\nDo you want to test the weather API call? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            test_weather_fetch()
        else:
            print("Skipping API test.")
    except KeyboardInterrupt:
        print("\nTest interrupted by user.")
        sys.exit(0)
    
    print("\n🎉 Tests completed!")
