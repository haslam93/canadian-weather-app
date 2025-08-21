#!/usr/bin/env python3
"""
Test script for the Canadian Weather CLI App
"""

from weather_app import WeatherApp

def test_postal_code_validation():
    """Test postal code validation"""
    app = WeatherApp()
    
    # Valid Canadian postal codes
    valid_canadian_codes = [
        "K1A 0A6",
        "K1A0A6",
        "M5V 3A8", 
        "M5V3A8",
        "V6B 2W9",
        "T2P2Y5"
    ]
    
    # Valid US zip codes
    valid_us_codes = [
        "10001",
        "90210",
        "12345-6789",
        "90210-1234",
        "00501"  # Holtsville, NY
    ]
    
    # Invalid postal codes
    invalid_codes = [
        "ABCDEF",
        "K1A 0A",
        "K1A 0A67",
        "Z1A 0A6",  # Z is not valid
        "K1D 0A6",   # D is not valid in second position
        "1234",      # Too short for US
        "123456",    # Too long for US (without dash)
        "12345-123", # Invalid US zip+4 format
        "ABCD-1234", # Invalid US format
        ""           # Empty string
    ]
    
    print("Testing valid Canadian postal codes:")
    for code in valid_canadian_codes:
        result = app.validate_postal_code(code)
        print(f"  {code}: {'✅ VALID' if result else '❌ INVALID'}")
    
    print("\nTesting valid US zip codes:")
    for code in valid_us_codes:
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
        # Canadian postal codes
        ("k1a0a6", "K1A 0A6"),
        ("K1A 0A6", "K1A 0A6"),
        ("m5v3a8", "M5V 3A8"),
        ("M5V  3A8", "M5V 3A8"),
        # US zip codes
        ("10001", "10001"),
        ("90210", "90210"),
        ("123456789", "12345-6789"),
        ("12345-6789", "12345-6789"),
        ("90210 1234", "90210-1234")
    ]
    
    print("\nTesting postal code formatting:")
    for input_code, expected in test_cases:
        result = app.format_postal_code(input_code)
        status = "✅ PASS" if result == expected else "❌ FAIL"
        print(f"  '{input_code}' -> '{result}' (expected: '{expected}') {status}")

def test_weather_fetch():
    """Test weather data fetching with known postal codes"""
    app = WeatherApp()
    
    test_locations = [
        ("K1A 0A6", "Ottawa, Canada"),
        ("10001", "New York, US")
    ]
    
    for postal_code, location_name in test_locations:
        print(f"\nTesting weather data fetch for {postal_code} ({location_name}):")
        print("This will make an actual API call...")
        
        weather_data = app.get_weather_data(postal_code)
        
        if weather_data:
            print("✅ Successfully fetched weather data")
            print("Keys in response:", list(weather_data.keys()))
            
            if 'current_condition' in weather_data:
                current = weather_data['current_condition'][0]
                print(f"Current temperature: {current['temp_C']}°C")
                print(f"Weather condition: {current['weatherDesc'][0]['value']}")
        else:
            print("❌ Failed to fetch weather data")
            return False
    
    return True

if __name__ == "__main__":
    print("🧪 Running Weather App Tests (Canadian & US Support)\n")
    
    # Run tests
    test_postal_code_validation()
    test_postal_code_formatting()
    
    # Ask user if they want to test API call
    import sys
    
    try:
        response = input("\nDo you want to test the weather API calls? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            test_weather_fetch()
        else:
            print("Skipping API test.")
    except KeyboardInterrupt:
        print("\nTest interrupted by user.")
        sys.exit(0)
    
    print("\n🎉 Tests completed!")
