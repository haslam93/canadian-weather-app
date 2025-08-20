// Canadian Weather App - JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const weatherForm = document.getElementById('weatherForm');
    const postalCodeInput = document.getElementById('postalCode');
    const searchBtn = document.getElementById('searchBtn');
    const loading = document.getElementById('loading');
    const errorAlert = document.getElementById('errorAlert');
    const errorMessage = document.getElementById('errorMessage');
    const weatherResults = document.getElementById('weatherResults');
    const exampleButtons = document.querySelectorAll('.example-btn');

    // Form submission handler
    weatherForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const postalCode = postalCodeInput.value.trim();
        if (postalCode) {
            getWeather(postalCode);
        }
    });

    // Example button handlers
    exampleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const postalCode = this.dataset.postal;
            postalCodeInput.value = postalCode;
            getWeather(postalCode);
        });
    });

    // Real-time postal code validation and formatting
    postalCodeInput.addEventListener('input', function() {
        let value = this.value.toUpperCase().replace(/[^A-Z0-9]/g, '');
        
        // Format as A1A 1A1
        if (value.length > 3) {
            value = value.substring(0, 3) + ' ' + value.substring(3, 6);
        }
        
        this.value = value;
        
        // Visual validation feedback
        if (value.length >= 6) {
            validatePostalCode(value.replace(' ', ''));
        } else {
            this.classList.remove('is-valid', 'is-invalid');
        }
    });

    // Function to validate postal code via API
    async function validatePostalCode(postalCode) {
        try {
            const response = await fetch('/api/validate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ postal_code: postalCode })
            });

            const data = await response.json();
            
            if (data.valid) {
                postalCodeInput.classList.remove('is-invalid');
                postalCodeInput.classList.add('is-valid');
            } else {
                postalCodeInput.classList.remove('is-valid');
                postalCodeInput.classList.add('is-invalid');
            }
        } catch (error) {
            console.error('Validation error:', error);
        }
    }

    // Main function to get weather data
    async function getWeather(postalCode) {
        // Show loading state
        showLoading();
        hideError();
        hideResults();

        try {
            const response = await fetch('/api/weather', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ postal_code: postalCode })
            });

            const data = await response.json();

            if (data.success) {
                displayWeather(data.data);
            } else {
                showError(data.error);
            }
        } catch (error) {
            console.error('Weather fetch error:', error);
            showError('Network error. Please check your connection and try again.');
        } finally {
            hideLoading();
        }
    }

    // Display weather data
    function displayWeather(weatherData) {
        const { current, forecast } = weatherData;

        // Update current weather
        document.getElementById('locationName').textContent = current.location;
        document.getElementById('currentTemp').textContent = current.temperature_c;
        document.getElementById('weatherCondition').textContent = current.condition;
        document.getElementById('feelsLike').textContent = current.feels_like_c;
        document.getElementById('windInfo').textContent = `${current.wind_speed} km/h ${current.wind_direction}`;
        document.getElementById('humidity').textContent = `${current.humidity}%`;
        document.getElementById('visibility').textContent = `${current.visibility} km`;
        document.getElementById('cloudCover').textContent = `${current.cloud_cover}%`;

        // Update forecast if available
        if (forecast) {
            document.getElementById('maxTemp').textContent = `${forecast.max_temp_c}°C`;
            document.getElementById('minTemp').textContent = `${forecast.min_temp_c}°C`;
            document.getElementById('sunrise').textContent = forecast.sunrise;
            document.getElementById('sunset').textContent = forecast.sunset;
            document.getElementById('forecastCard').style.display = 'block';
        } else {
            document.getElementById('forecastCard').style.display = 'none';
        }

        // Show results with animation
        showResults();
        
        // Scroll to results
        weatherResults.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'start' 
        });

        // Update page title
        document.title = `🌤️ ${current.temperature_c}°C in ${current.location.split(',')[0]} - Canadian Weather`;
    }

    // UI Helper functions
    function showLoading() {
        loading.style.display = 'block';
        searchBtn.disabled = true;
        searchBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Loading...';
    }

    function hideLoading() {
        loading.style.display = 'none';
        searchBtn.disabled = false;
        searchBtn.innerHTML = '<i class="fas fa-search me-2"></i>Get Weather';
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorAlert.style.display = 'block';
        errorAlert.classList.add('show');
        
        // Auto-hide error after 5 seconds
        setTimeout(() => {
            hideError();
        }, 5000);
    }

    function hideError() {
        errorAlert.style.display = 'none';
        errorAlert.classList.remove('show');
    }

    function showResults() {
        weatherResults.style.display = 'block';
    }

    function hideResults() {
        weatherResults.style.display = 'none';
    }

    // Add keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + Enter to submit form
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            weatherForm.dispatchEvent(new Event('submit'));
        }
        
        // Escape to clear form
        if (e.key === 'Escape') {
            postalCodeInput.value = '';
            hideResults();
            hideError();
            postalCodeInput.focus();
        }
    });

    // Add geolocation support (if available)
    if ('geolocation' in navigator) {
        // Could add a feature to detect location and suggest nearby postal codes
        console.log('Geolocation is available');
    }

    // Focus on input when page loads
    postalCodeInput.focus();

    // Add some fun weather-based background changes
    function updateBackgroundBasedOnWeather(condition) {
        const body = document.body;
        const conditionLower = condition.toLowerCase();
        
        // Remove existing weather classes
        body.classList.remove('sunny', 'cloudy', 'rainy', 'snowy', 'stormy');
        
        if (conditionLower.includes('sunny') || conditionLower.includes('clear')) {
            body.classList.add('sunny');
        } else if (conditionLower.includes('cloud')) {
            body.classList.add('cloudy');
        } else if (conditionLower.includes('rain') || conditionLower.includes('drizzle')) {
            body.classList.add('rainy');
        } else if (conditionLower.includes('snow') || conditionLower.includes('blizzard')) {
            body.classList.add('snowy');
        } else if (conditionLower.includes('storm') || conditionLower.includes('thunder')) {
            body.classList.add('stormy');
        }
    }

    // Enhanced displayWeather function to include background changes
    const originalDisplayWeather = displayWeather;
    displayWeather = function(weatherData) {
        originalDisplayWeather(weatherData);
        updateBackgroundBasedOnWeather(weatherData.current.condition);
    };

    // Add service worker registration for PWA capabilities (future enhancement)
    if ('serviceWorker' in navigator) {
        // Could register a service worker for offline capabilities
        console.log('Service Worker support detected');
    }

    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined') {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
});

// Utility functions
function formatTemperature(celsius) {
    const fahrenheit = (celsius * 9/5) + 32;
    return {
        celsius: Math.round(celsius),
        fahrenheit: Math.round(fahrenheit)
    };
}

function getWeatherIcon(condition) {
    const conditionLower = condition.toLowerCase();
    
    if (conditionLower.includes('sunny') || conditionLower.includes('clear')) {
        return 'fas fa-sun';
    } else if (conditionLower.includes('partly cloudy')) {
        return 'fas fa-cloud-sun';
    } else if (conditionLower.includes('cloud')) {
        return 'fas fa-cloud';
    } else if (conditionLower.includes('rain')) {
        return 'fas fa-cloud-rain';
    } else if (conditionLower.includes('snow')) {
        return 'fas fa-snowflake';
    } else if (conditionLower.includes('storm')) {
        return 'fas fa-bolt';
    } else {
        return 'fas fa-cloud';
    }
}

// Export functions for potential testing
window.WeatherApp = {
    getWeather,
    formatTemperature,
    getWeatherIcon
};
