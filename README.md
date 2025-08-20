# Canadian Weather CLI App 🌤️

A command-line weather application that displays current weather conditions and forecasts for Canadian postal codes using free APIs that don't require registration.

## Features

- ✅ Get current weather conditions for any Canadian postal code
- 🌡️ Display temperature in both Celsius and Fahrenheit
- 🌤️ Show weather condition descriptions
- 💨 Wind speed and direction information
- 💧 Humidity and visibility data
- 📅 Today's forecast with high/low temperatures
- 🌅 Sunrise and sunset times
- 🔍 Input validation for Canadian postal codes

## Installation

1. Make sure you have Python 3.6+ installed
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python weather_app.py <postal_code>
```

### Examples

```bash
# Ottawa, ON
python weather_app.py K1A0A6

# Toronto, ON
python weather_app.py M5V3A8

# Vancouver, BC
python weather_app.py V6B2W9

# With spaces in postal code
python weather_app.py "K1A 0A6"
```

### Help

```bash
python weather_app.py --help
```

### Version

```bash
python weather_app.py --version
```

## Postal Code Format

The app accepts Canadian postal codes in the following formats:
- `A1A 1A1` (with space)
- `A1A1A1` (without space)

Examples of valid postal codes:
- K1A 0A6 (Ottawa, ON)
- M5V 3A8 (Toronto, ON)
- V6B 2W9 (Vancouver, BC)
- T2P 2Y5 (Calgary, AB)

## API Information

This application uses the **wttr.in** API, which is:
- ✅ Completely free
- ✅ No registration required
- ✅ No API key needed
- ✅ Supports Canadian postal codes
- ✅ Provides comprehensive weather data

## Sample Output

```
==================================================
🌤️  WEATHER FOR K1A 0A6
==================================================
📍 Location: Ottawa, Ontario, Canada
🌡️  Temperature: 22°C (72°F)
🌤️  Condition: Partly cloudy
🌪️  Feels like: 24°C (75°F)
💨 Wind: 15 km/h NW
💧 Humidity: 65%
🔍 Visibility: 10 km
☁️  Cloud Cover: 25%

📅 Today's Forecast:
   🌡️  High: 26°C (79°F)
   🌡️  Low: 18°C (64°F)
   🌅 Sunrise: 06:15 AM
   🌇 Sunset: 07:45 PM
==================================================
```

## Error Handling

The app includes robust error handling for:
- Invalid postal code formats
- Network connectivity issues
- API response errors
- Data parsing errors

## Requirements

- Python 3.6+
- `requests` library (see requirements.txt)
- Internet connection

## License

This project is open source and available under the MIT License.
