#!/usr/bin/env python3
"""
Flask Web UI for Canadian Weather CLI App
A web interface for the weather application using Flask
"""

from flask import Flask, render_template, request, jsonify
import json
from weather_app import WeatherApp
import os

app = Flask(__name__)
app.secret_key = 'canadian_weather_app_secret_key_2025'

# Initialize the weather app
weather_app = WeatherApp()

@app.route('/')
def index():
    """Main page with weather form"""
    return render_template('index.html')

@app.route('/api/weather', methods=['POST'])
def get_weather():
    """API endpoint to get weather data"""
    try:
        data = request.get_json()
        postal_code = data.get('postal_code', '').strip()
        
        if not postal_code:
            return jsonify({
                'success': False,
                'error': 'Please enter a postal code'
            }), 400
        
        # Validate postal code
        if not weather_app.validate_postal_code(postal_code):
            return jsonify({
                'success': False,
                'error': 'Invalid postal code format. Please use Canadian format (A1A 1A1) or US format (12345 or 12345-6789)'
            }), 400
        
        # Get weather data
        weather_data = weather_app.get_weather_data(postal_code)
        
        if weather_data is None:
            return jsonify({
                'success': False,
                'error': 'Failed to fetch weather data. Please try again later.'
            }), 500
        
        # Parse and format the weather data for web display
        formatted_data = format_weather_for_web(weather_data, postal_code)
        
        return jsonify({
            'success': True,
            'data': formatted_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        }), 500

def format_weather_for_web(weather_data, postal_code):
    """Format weather data for web display"""
    try:
        current = weather_data['current_condition'][0]
        location = weather_data['nearest_area'][0]
        
        # Location information
        area_name = location.get('areaName', [{}])[0].get('value', 'Unknown')
        region = location.get('region', [{}])[0].get('value', 'Unknown')
        country = location.get('country', [{}])[0].get('value', 'Unknown')
        
        # Current weather
        current_weather = {
            'postal_code': weather_app.format_postal_code(postal_code),
            'location': f"{area_name}, {region}, {country}",
            'temperature_c': current['temp_C'],
            'temperature_f': current['temp_F'],
            'condition': current['weatherDesc'][0]['value'],
            'feels_like_c': current['FeelsLikeC'],
            'feels_like_f': current['FeelsLikeF'],
            'wind_speed': current['windspeedKmph'],
            'wind_direction': current['winddir16Point'],
            'humidity': current['humidity'],
            'visibility': current['visibility'],
            'cloud_cover': current['cloudcover']
        }
        
        # Today's forecast
        forecast = None
        if 'weather' in weather_data and weather_data['weather']:
            today = weather_data['weather'][0]
            forecast = {
                'max_temp_c': today['maxtempC'],
                'max_temp_f': today['maxtempF'],
                'min_temp_c': today['mintempC'],
                'min_temp_f': today['mintempF'],
                'sunrise': today['astronomy'][0]['sunrise'],
                'sunset': today['astronomy'][0]['sunset']
            }
        
        return {
            'current': current_weather,
            'forecast': forecast
        }
        
    except KeyError as e:
        raise Exception(f"Error parsing weather data: Missing key {e}")

@app.route('/api/validate', methods=['POST'])
def validate_postal_code():
    """API endpoint to validate postal code"""
    try:
        data = request.get_json()
        postal_code = data.get('postal_code', '').strip()
        
        is_valid = weather_app.validate_postal_code(postal_code)
        formatted = weather_app.format_postal_code(postal_code) if is_valid else postal_code
        
        return jsonify({
            'valid': is_valid,
            'formatted': formatted
        })
        
    except Exception as e:
        return jsonify({
            'valid': False,
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    
    os.makedirs(templates_dir, exist_ok=True)
    os.makedirs(static_dir, exist_ok=True)
    os.makedirs(os.path.join(static_dir, 'css'), exist_ok=True)
    os.makedirs(os.path.join(static_dir, 'js'), exist_ok=True)
    
    print("🌤️ Starting Canadian Weather Web App...")
    print("📍 Open your browser and go to: http://localhost:5000")
    print("🔍 Press Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
