#!/bin/bash
# Canadian Weather CLI App - Shell Script
# Usage: ./weather.sh <postal_code>

if [ $# -eq 0 ]; then
    echo "Usage: ./weather.sh <postal_code>"
    echo "Example: ./weather.sh K1A0A6"
    echo ""
    echo "Canadian postal code formats:"
    echo "  A1A 1A1 (with space)"
    echo "  A1A1A1 (without space)"
    exit 1
fi

python3 weather_app.py "$1"
