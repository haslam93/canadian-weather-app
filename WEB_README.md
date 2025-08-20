# 🌤️ Canadian Weather Web App

A modern, responsive web application that provides real-time weather information for Canadian postal codes. Built with Flask, Bootstrap, and vanilla JavaScript.

## 🚀 Features

### Web Interface
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Modern UI**: Clean, intuitive interface with Bootstrap 5 and custom CSS
- **Real-time Validation**: Instant postal code format validation and formatting
- **Interactive Elements**: Hover effects, animations, and smooth transitions
- **Accessibility**: WCAG compliant with proper ARIA labels and keyboard navigation

### Weather Data
- ✅ Current weather conditions for any Canadian postal code
- 🌡️ Temperature in both Celsius and Fahrenheit
- 🌤️ Detailed weather descriptions with icons
- 💨 Wind speed and direction information
- 💧 Humidity, visibility, and cloud cover data
- 📅 Today's forecast with high/low temperatures
- 🌅 Sunrise and sunset times
- 📍 Accurate location information

### Technical Features
- **RESTful API**: Clean JSON API endpoints
- **Error Handling**: Comprehensive error management with user-friendly messages
- **Input Validation**: Real-time postal code validation and formatting
- **Performance**: Optimized for fast loading and smooth interactions
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.6 or higher
- Internet connection

### Quick Start

1. **Clone or download the project**
```bash
cd "your-project-directory"
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Start the web application**
```bash
python web_app.py
```

4. **Open your browser**
Navigate to: http://localhost:5000

## 📱 Usage

### Web Interface

1. **Enter a Postal Code**: Type any valid Canadian postal code (e.g., K1A 0A6, M5V 3A8)
2. **Real-time Formatting**: The app automatically formats your input as you type
3. **Get Weather**: Click "Get Weather" or press Ctrl+Enter
4. **View Results**: See comprehensive weather information with beautiful visuals

### Quick Examples
- Click any of the example postal codes provided
- Try these popular locations:
  - **K1A 0A6** (Ottawa, ON)
  - **M5V 3A8** (Toronto, ON)  
  - **V6B 2W9** (Vancouver, BC)

### API Endpoints

#### GET /
Main web interface

#### POST /api/weather
Get weather data for a postal code
```json
{
  "postal_code": "K1A0A6"
}
```

#### POST /api/validate
Validate postal code format
```json
{
  "postal_code": "K1A0A6"
}
```

## 🎨 User Interface Features

### Modern Design
- **Gradient Backgrounds**: Beautiful gradient color schemes
- **Card-based Layout**: Clean, organized information display
- **Responsive Grid**: Adapts to any screen size
- **Custom Icons**: Font Awesome icons for visual appeal

### Interactive Elements
- **Hover Effects**: Smooth animations on buttons and cards
- **Loading States**: Visual feedback during data fetching
- **Form Validation**: Real-time input validation with visual cues
- **Smooth Scrolling**: Automatic scroll to results

### Accessibility
- **Keyboard Navigation**: Full keyboard support
- **Screen Reader Friendly**: Proper ARIA labels and structure
- **High Contrast**: Clear visibility for all users
- **Mobile Optimized**: Touch-friendly interface

## 🔧 Configuration

### Environment Variables
The app uses default settings but can be configured:
- **FLASK_ENV**: Set to 'development' or 'production'
- **FLASK_HOST**: Default is '0.0.0.0'
- **FLASK_PORT**: Default is 5000

### API Configuration
Located in `config.json`:
```json
{
  "api": {
    "provider": "wttr.in",
    "timeout": 10,
    "format": "j1"
  }
}
```

## 📁 Project Structure

```
canadian-weather-app/
├── web_app.py              # Flask application
├── weather_app.py          # Core weather logic (CLI)
├── requirements.txt        # Python dependencies
├── config.json            # Configuration settings
├── README.md              # Documentation
├── templates/             # HTML templates
│   ├── index.html         # Main interface
│   ├── 404.html          # Not found page
│   └── 500.html          # Error page
├── static/               # Static assets
│   ├── css/
│   │   └── style.css     # Custom styles
│   └── js/
│       └── app.js        # JavaScript functionality
└── .github/
    └── copilot-instructions.md
```

## 🌐 Browser Support

- **Chrome** 90+
- **Firefox** 88+
- **Safari** 14+
- **Edge** 90+
- **Mobile browsers** (iOS Safari, Chrome Mobile)

## 🔒 Security Features

- **Input Validation**: All inputs are validated and sanitized
- **CSRF Protection**: Flask secret key for session security
- **Error Handling**: No sensitive information exposed in errors
- **Rate Limiting**: Built-in Flask development server limitations

## 🎯 Performance

- **Fast Loading**: Minimal dependencies and optimized assets
- **Caching**: Browser caching for static assets
- **Responsive**: Quick API responses using free wttr.in service
- **Lightweight**: Small footprint with efficient code

## 🚀 Deployment Options

### Local Development
```bash
python web_app.py
```

### Production Deployment
Use a production WSGI server:
```bash
pip install gunicorn
gunicorn web_app:app
```

### Docker (Optional)
Could be containerized for cloud deployment

## 🆚 CLI vs Web Interface

| Feature | CLI App | Web App |
|---------|---------|---------|
| **Interface** | Terminal | Browser |
| **Accessibility** | Command line users | Everyone |
| **Visual Appeal** | Text-based | Modern GUI |
| **Device Support** | Any with Python | Any with browser |
| **Ease of Use** | Tech-savvy users | All users |
| **Sharing** | Copy/paste text | Share URL |

## 🔍 Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Module not found:**
```bash
pip install -r requirements.txt
```

**API timeout:**
- Check internet connection
- Wait and try again
- The wttr.in service may be temporarily unavailable

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **wttr.in**: Free weather API service
- **Bootstrap**: UI framework
- **Font Awesome**: Icon library
- **Flask**: Python web framework

---

**🌤️ Enjoy checking the weather across Canada!**
