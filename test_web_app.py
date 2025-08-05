"""
Unit Tests untuk Temperature Converter Web App
Author: itsray3301
Description: Comprehensive testing untuk Flask application
"""

import unittest
import json
import sys
import os

# Add the parent directory to the path to import the modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from temperature_logic import TemperatureConverter, InputValidator

class TestTemperatureWebApp(unittest.TestCase):
    """Test cases untuk Flask web application"""
    
    def setUp(self):
        """Setup test environment"""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_homepage(self):
        """Test homepage loading"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Konversi Temperatur', response.data)
        self.assertIn(b'Masukkan Temperatur', response.data)
    
    def test_convert_api_success(self):
        """Test successful conversion via API"""
        data = {
            'temperature': '25',
            'conversion_type': 'Celcius ke Fahrenheit'
        }
        response = self.app.post('/convert',
                                data=json.dumps(data),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        json_data = json.loads(response.data)
        self.assertTrue(json_data['success'])
        self.assertEqual(json_data['result'], 77.0)
        self.assertEqual(json_data['formatted_result'], '25.0°C = 77.00°F')
    
    def test_convert_api_invalid_input(self):
        """Test API with invalid input"""
        data = {
            'temperature': 'invalid',
            'conversion_type': 'Celcius ke Fahrenheit'
        }
        response = self.app.post('/convert',
                                data=json.dumps(data),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        
        json_data = json.loads(response.data)
        self.assertFalse(json_data['success'])
        self.assertIn('error', json_data)
    
    def test_convert_api_empty_input(self):
        """Test API with empty input"""
        data = {
            'temperature': '',
            'conversion_type': 'Celcius ke Fahrenheit'
        }
        response = self.app.post('/convert',
                                data=json.dumps(data),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        
        json_data = json.loads(response.data)
        self.assertFalse(json_data['success'])
        self.assertEqual(json_data['error'], 'Masukkan nilai temperatur')
    
    def test_convert_api_invalid_conversion_type(self):
        """Test API with invalid conversion type"""
        data = {
            'temperature': '25',
            'conversion_type': 'Invalid Conversion'
        }
        response = self.app.post('/convert',
                                data=json.dumps(data),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        
        json_data = json.loads(response.data)
        self.assertFalse(json_data['success'])
        self.assertIn('not supported', json_data['error'])
    
    def test_conversions_api(self):
        """Test conversions options API"""
        response = self.app.get('/api/conversions')
        self.assertEqual(response.status_code, 200)
        
        json_data = json.loads(response.data)
        self.assertIsInstance(json_data, list)
        self.assertIn('Celcius ke Fahrenheit', json_data)
        self.assertIn('Fahrenheit ke Celcius', json_data)
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        
        json_data = json.loads(response.data)
        self.assertEqual(json_data['status'], 'healthy')
        self.assertEqual(json_data['service'], 'Temperature Converter API')
    
    def test_404_error(self):
        """Test 404 error handling"""
        response = self.app.get('/nonexistent-page')
        self.assertEqual(response.status_code, 404)
    
    def test_json_404_error(self):
        """Test 404 error for API requests"""
        response = self.app.get('/api/nonexistent',
                               headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 404)
        
        json_data = json.loads(response.data)
        self.assertEqual(json_data['error'], 'Endpoint not found')

class TestTemperatureLogicReuse(unittest.TestCase):
    """Test reused logic dari desktop version"""
    
    def test_temperature_converter_methods(self):
        """Test semua method konversi"""
        # Test Celsius conversions
        self.assertAlmostEqual(TemperatureConverter.celsius_to_fahrenheit(0), 32.0)
        self.assertAlmostEqual(TemperatureConverter.celsius_to_fahrenheit(100), 212.0)
        self.assertAlmostEqual(TemperatureConverter.celsius_to_kelvin(0), 273.15)
        self.assertAlmostEqual(TemperatureConverter.celsius_to_reamur(100), 80.0)
        
        # Test reverse conversions
        self.assertAlmostEqual(TemperatureConverter.fahrenheit_to_celsius(32), 0.0)
        self.assertAlmostEqual(TemperatureConverter.fahrenheit_to_celsius(212), 100.0)
        self.assertAlmostEqual(TemperatureConverter.kelvin_to_celsius(273.15), 0.0)
        self.assertAlmostEqual(TemperatureConverter.reamur_to_celsius(80), 100.0)
    
    def test_input_validator(self):
        """Test input validation"""
        # Valid inputs
        valid, value, msg = InputValidator.validate_temperature_input("25")
        self.assertTrue(valid)
        self.assertEqual(value, 25.0)
        self.assertEqual(msg, "")
        
        # Invalid inputs
        valid, value, msg = InputValidator.validate_temperature_input("")
        self.assertFalse(valid)
        self.assertEqual(msg, "Masukkan nilai temperatur")
        
        valid, value, msg = InputValidator.validate_temperature_input("abc")
        self.assertFalse(valid)
        self.assertEqual(msg, "Masukkan angka yang valid")
    
    def test_conversion_integration(self):
        """Test full conversion process"""
        result, formatted = TemperatureConverter.convert(0, "Celcius ke Fahrenheit")
        self.assertEqual(result, 32.0)
        self.assertEqual(formatted, "0°C = 32.00°F")
        
        result, formatted = TemperatureConverter.convert(100, "Celcius ke Kelvin")
        self.assertEqual(result, 373.15)
        self.assertEqual(formatted, "100°C = 373.15 K")

class TestAPIValidation(unittest.TestCase):
    """Test API validation dan edge cases"""
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_extreme_temperatures(self):
        """Test dengan temperatur ekstrem"""
        # Absolute zero
        data = {
            'temperature': '-273.15',
            'conversion_type': 'Celcius ke Kelvin'
        }
        response = self.app.post('/convert',
                                data=json.dumps(data),
                                content_type='application/json')
        
        json_data = json.loads(response.data)
        self.assertTrue(json_data['success'])
        self.assertAlmostEqual(json_data['result'], 0.0)
    
    def test_large_numbers(self):
        """Test dengan angka besar"""
        data = {
            'temperature': '1000000',
            'conversion_type': 'Celcius ke Fahrenheit'
        }
        response = self.app.post('/convert',
                                data=json.dumps(data),
                                content_type='application/json')
        
        json_data = json.loads(response.data)
        self.assertTrue(json_data['success'])
        self.assertIsInstance(json_data['result'], (int, float))
    
    def test_decimal_precision(self):
        """Test precision dengan decimal"""
        data = {
            'temperature': '25.6789',
            'conversion_type': 'Celcius ke Fahrenheit'
        }
        response = self.app.post('/convert',
                                data=json.dumps(data),
                                content_type='application/json')
        
        json_data = json.loads(response.data)
        self.assertTrue(json_data['success'])
        # Check that result maintains precision
        expected = 25.6789 * 9/5 + 32
        self.assertAlmostEqual(json_data['result'], expected, places=4)

if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
