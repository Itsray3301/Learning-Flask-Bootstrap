"""
Temperature Converter Web App
Belajar Flask untuk konversi temperatur
"""

from flask import Flask, render_template, request, jsonify
import sys
import os

# Add current directory to path to import temperature logic
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import fungsi konversi dari file terpisah
from temperature_logic import TemperatureConverter, InputValidator, CONVERSION_OPTIONS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'temperature-converter-secret-key-2024'

@app.route('/')
def index():
    """Halaman utama dengan form konversi temperatur"""
    return render_template('index.html', conversion_options=CONVERSION_OPTIONS)

@app.route('/convert', methods=['POST'])
def convert_temperature():
    """Endpoint untuk memproses konversi temperatur via AJAX"""
    try:
        # Ambil data dari request JSON
        data = request.get_json()
        temperature_input = data.get('temperature', '')
        conversion_type = data.get('conversion_type', '')
        
        # Validasi input dari user
        validator = InputValidator()
        is_valid, temperature, error_message = validator.validate_temperature_input(str(temperature_input))
        
        if not is_valid:
            return jsonify({
                'success': False,
                'error': error_message
            }), 400
        
        # Lakukan konversi temperatur
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
    """Endpoint untuk mendapatkan daftar opsi konversi yang tersedia"""
    return jsonify(CONVERSION_OPTIONS)

@app.route('/health')
def health_check():
    """Endpoint untuk cek status aplikasi"""
    return jsonify({
        'status': 'healthy',
        'service': 'Temperature Converter API',
        'version': '1.0.0'
    })

@app.errorhandler(404)
def not_found(error):
    """Handler untuk error 404 - halaman tidak ditemukan"""
    if request.is_json:
        return jsonify({'error': 'Endpoint not found'}), 404
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handler untuk error 500 - server error"""
    if request.is_json:
        return jsonify({'error': 'Internal server error'}), 500
    return render_template('500.html'), 500

if __name__ == '__main__':
    print("🌡️  Temperature Converter Web App")
    print("📍 Running on: http://localhost:5000")
    print("🔧 Debug mode: ON")
    print("-" * 40)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
