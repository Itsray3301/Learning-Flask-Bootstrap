"""
Flask Temperature Converter Web Application
Author: itsray3301
"""

from flask import Flask, render_template, request, jsonify
import sys
import os

# Add current directory to path to import temperature logic
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import logic dari temperature_logic.py
from temperature_logic import TemperatureConverter, InputValidator, CONVERSION_OPTIONS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'temperature-converter-secret-key-2024'

@app.route('/')
def index():
    """Homepage dengan form konversi"""
    return render_template('index.html', conversion_options=CONVERSION_OPTIONS)

@app.route('/convert', methods=['POST'])
def convert_temperature():
    """API endpoint untuk konversi temperatur"""
    try:
        # Get data from request
        data = request.get_json()
        temperature_input = data.get('temperature', '')
        conversion_type = data.get('conversion_type', '')
        
        # Validate input
        validator = InputValidator()
        is_valid, temperature, error_message = validator.validate_temperature_input(str(temperature_input))
        
        if not is_valid:
            return jsonify({
                'success': False,
                'error': error_message
            }), 400
        
        # Perform conversion
        converter = TemperatureConverter()
        result, formatted_result = converter.convert(temperature, conversion_type)
        
        return jsonify({
            'success': True,
            'result': result,
            'formatted_result': formatted_result,
            'input_temperature': temperature,
            'conversion_type': conversion_type
        })
        
    except ValueError as ve:
        return jsonify({
            'success': False,
            'error': str(ve)
        }), 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error dalam konversi: {str(e)}'
        }), 500

@app.route('/api/conversions')
def get_conversion_options():
    """API endpoint untuk mendapatkan opsi konversi"""
    return jsonify(CONVERSION_OPTIONS)

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Temperature Converter API',
        'version': '1.0.0'
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    if request.is_json:
        return jsonify({'error': 'Endpoint not found'}), 404
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    if request.is_json:
        return jsonify({'error': 'Internal server error'}), 500
    return render_template('500.html'), 500

if __name__ == '__main__':
    print("🌡️  Temperature Converter Web App")
    print("📍 Running on: http://localhost:5000")
    print("🔧 Debug mode: ON")
    print("-" * 40)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
