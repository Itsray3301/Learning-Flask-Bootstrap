// Temperature Converter - Express Server
// Proyek pembelajaran web development dengan Node.js dan Express

const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware untuk parsing JSON dan form data
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static files (CSS, JS, images)
app.use('/static', express.static(path.join(__dirname, 'static')));

// Set view engine untuk HTML templates
app.set('views', path.join(__dirname, 'templates'));
app.set('view engine', 'html');

// Custom HTML rendering (karena Express tidak support .html secara default)
app.engine('html', (filePath, options, callback) => {
  const fs = require('fs');
  fs.readFile(filePath, (err, content) => {
    if (err) return callback(err);
    
    // Simple template replacement
    let rendered = content.toString();
    Object.keys(options).forEach(key => {
      const regex = new RegExp(`{{\\s*${key}\\s*}}`, 'g');
      rendered = rendered.replace(regex, options[key] || '');
    });
    
    return callback(null, rendered);
  });
});

// Fungsi konversi suhu (dipindah dari temperature_logic.py)
function celsiusToFahrenheit(celsius) {
  return (celsius * 9/5) + 32;
}

function fahrenheitToCelsius(fahrenheit) {
  return (fahrenheit - 32) * 5/9;
}

function celsiusToKelvin(celsius) {
  return celsius + 273.15;
}

function kelvinToCelsius(kelvin) {
  return kelvin - 273.15;
}

function fahrenheitToKelvin(fahrenheit) {
  const celsius = fahrenheitToCelsius(fahrenheit);
  return celsiusToKelvin(celsius);
}

function kelvinToFahrenheit(kelvin) {
  const celsius = kelvinToCelsius(kelvin);
  return celsiusToFahrenheit(celsius);
}

// Route utama - halaman home
app.get('/', (req, res) => {
  res.render('index', {
    title: 'Temperature Converter',
    result: '',
    error: ''
  });
});

// Route untuk konversi suhu (POST)
app.post('/convert', (req, res) => {
  try {
    const { temperature, from_unit, to_unit } = req.body;
    
    // Validasi input
    if (!temperature || isNaN(temperature)) {
      return res.render('index', {
        title: 'Temperature Converter',
        result: '',
        error: 'Masukkan angka yang valid untuk suhu!'
      });
    }
    
    const temp = parseFloat(temperature);
    let result;
    
    // Logika konversi berdasarkan unit asal dan tujuan
    if (from_unit === to_unit) {
      result = temp;
    } else if (from_unit === 'celsius') {
      if (to_unit === 'fahrenheit') {
        result = celsiusToFahrenheit(temp);
      } else if (to_unit === 'kelvin') {
        result = celsiusToKelvin(temp);
      }
    } else if (from_unit === 'fahrenheit') {
      if (to_unit === 'celsius') {
        result = fahrenheitToCelsius(temp);
      } else if (to_unit === 'kelvin') {
        result = fahrenheitToKelvin(temp);
      }
    } else if (from_unit === 'kelvin') {
      if (to_unit === 'celsius') {
        result = kelvinToCelsius(temp);
      } else if (to_unit === 'fahrenheit') {
        result = kelvinToFahrenheit(temp);
      }
    }
    
    // Format hasil dengan 2 desimal
    const formattedResult = result.toFixed(2);
    const unitNames = {
      'celsius': 'Celsius (°C)',
      'fahrenheit': 'Fahrenheit (°F)',
      'kelvin': 'Kelvin (K)'
    };
    
    const resultMessage = `${temp}° ${unitNames[from_unit]} = ${formattedResult}° ${unitNames[to_unit]}`;
    
    res.render('index', {
      title: 'Temperature Converter',
      result: resultMessage,
      error: ''
    });
    
  } catch (error) {
    console.error('Error dalam konversi:', error);
    res.render('index', {
      title: 'Temperature Converter',
      result: '',
      error: 'Terjadi kesalahan dalam konversi. Coba lagi!'
    });
  }
});

// API endpoint untuk konversi (JSON response)
app.post('/api/convert', (req, res) => {
  try {
    const { temperature, from_unit, to_unit } = req.body;
    
    if (!temperature || isNaN(temperature)) {
      return res.status(400).json({
        success: false,
        error: 'Invalid temperature value'
      });
    }
    
    const temp = parseFloat(temperature);
    let result;
    
    // Sama seperti route POST di atas
    if (from_unit === to_unit) {
      result = temp;
    } else if (from_unit === 'celsius') {
      if (to_unit === 'fahrenheit') {
        result = celsiusToFahrenheit(temp);
      } else if (to_unit === 'kelvin') {
        result = celsiusToKelvin(temp);
      }
    } else if (from_unit === 'fahrenheit') {
      if (to_unit === 'celsius') {
        result = fahrenheitToCelsius(temp);
      } else if (to_unit === 'kelvin') {
        result = fahrenheitToKelvin(temp);
      }
    } else if (from_unit === 'kelvin') {
      if (to_unit === 'celsius') {
        result = kelvinToCelsius(temp);
      } else if (to_unit === 'fahrenheit') {
        result = kelvinToFahrenheit(temp);
      }
    }
    
    res.json({
      success: true,
      original: temp,
      result: parseFloat(result.toFixed(2)),
      from_unit: from_unit,
      to_unit: to_unit
    });
    
  } catch (error) {
    console.error('API Error:', error);
    res.status(500).json({
      success: false,
      error: 'Internal server error'
    });
  }
});

// Error handling untuk 404
app.use((req, res) => {
  res.status(404).render('404', {
    title: '404 - Halaman Tidak Ditemukan'
  });
});

// Error handling untuk 500
app.use((err, req, res, next) => {
  console.error('Server Error:', err);
  res.status(500).render('500', {
    title: '500 - Server Error'
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`🌡️ Temperature Converter Server berjalan di http://localhost:${PORT}`);
  console.log(`📍 Environment: ${process.env.NODE_ENV || 'development'}`);
  console.log(`🚀 Server siap menerima request!`);
});

module.exports = app;