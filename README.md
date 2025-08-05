# 🌡️ Temperature Converter Web App

Aplikasi web untuk konversi temperatur menggunakan Flask + Bootstrap 5.

## ✨ Fitur

- **Konversi Multi-Unit**: Celsius, Fahrenheit, Kelvin, Reamur
- **Responsive Design**: Bootstrap 5 dengan modern UI/UX
- **Real-time Validation**: Client-side dan server-side validation
- **AJAX Requests**: Konversi tanpa reload halaman
- **Keyboard Shortcuts**: Ctrl+Enter untuk konversi, Escape untuk clear
- **Error Handling**: Comprehensive error handling dan user feedback
- **Modern Animations**: Smooth transitions dan loading states
- **Mobile Friendly**: Optimized untuk semua device sizes

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip (Python package installer)

### Installation

1. **Clone atau download project ini**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run aplikasi:**
   ```bash
   python app.py
   ```

4. **Buka browser dan akses:**
   ```
   http://localhost:5000
   ```

## 📁 Struktur Project

```
Temperature_Web/
├── app.py                 # Main Flask application
├── temperature_logic.py   # Logic konversi temperatur
├── requirements.txt       # Python dependencies
├── README.md             # Documentation
├── templates/
│   ├── index.html        # Main page template
│   ├── 404.html         # Error 404 page
│   └── 500.html         # Error 500 page
└── static/
    ├── css/
    │   └── style.css     # Custom CSS styles
    └── js/
        └── app.js        # Custom JavaScript
```

## 🛠️ API Endpoints

### GET `/`
Homepage dengan form konversi

### POST `/convert`
API endpoint untuk konversi temperatur
- **Request Body:**
  ```json
  {
    "temperature": "25",
    "conversion_type": "Celcius ke Fahrenheit"
  }
  ```
- **Response:**
  ```json
  {
    "success": true,
    "result": 77.0,
    "formatted_result": "25°C = 77.00°F",
    "input_temperature": 25.0,
    "conversion_type": "Celcius ke Fahrenheit"
  }
  ```

### GET `/api/conversions`
Mendapatkan daftar opsi konversi yang tersedia

### GET `/health`
Health check endpoint untuk monitoring

## ⌨️ Keyboard Shortcuts

- **Ctrl + Enter**: Konversi temperatur
- **Escape**: Bersihkan form
- **Ctrl + I**: Tampilkan informasi konversi

## 🎨 Teknologi yang Digunakan

- **Backend**: Flask (Python web framework)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript ES6+
- **Icons**: Font Awesome 6
- **Styling**: Custom CSS dengan CSS Variables dan Animations

## 🔧 Konfigurasi

### Environment Variables (Opsional)
Buat file `.env` untuk konfigurasi:
```
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
PORT=5000
```

### Production Deployment
Untuk production, gunakan WSGI server seperti Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🧪 Testing

Jalankan unit tests (jika tersedia):
```bash
pytest
```

## 📱 Browser Support

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ Mobile browsers

## 🎯 Formula Konversi

### Dari Celsius:
- **ke Fahrenheit**: °F = (°C × 9/5) + 32
- **ke Kelvin**: K = °C + 273.15
- **ke Reamur**: °Re = °C × 4/5

### Ke Celsius:
- **dari Fahrenheit**: °C = (°F - 32) × 5/9
- **dari Kelvin**: °C = K - 273.15
- **dari Reamur**: °C = °Re × 5/4

## 🐛 Troubleshooting

### Common Issues:

1. **Port 5000 sudah digunakan:**
   ```bash
   python app.py --port 8000
   ```

2. **Module tidak ditemukan:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Template tidak ditemukan:**
   Pastikan folder `templates/` ada dan berisi file HTML

## 🚀 Future Enhancements

- [ ] Dark mode toggle
- [ ] Conversion history
- [ ] Export results (PDF/Excel)
- [ ] Multi-language support
- [ ] Unit tests coverage
- [ ] Docker containerization
- [ ] Database integration
- [ ] User authentication
- [ ] API rate limiting
- [ ] Caching dengan Redis

## 📄 License

Developed by itsray3301 for educational purposes.

## 🤝 Contributing

Silakan buat pull request atau report issues untuk improvement.

---

**Happy Converting! 🌡️**