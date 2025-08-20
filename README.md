# 📱 Smartphone Price Prediction

A machine learning-powered web application that predicts smartphone resale prices based on device specifications, condition, and market data. Built with React frontend and Flask backend, featuring a modern dark theme UI.

## 🚀 Features

- **AI-Powered Predictions**: Machine learning model with 96.07% accuracy
- **Searchable Interface**: Type to search brands and models
- **Real-time Analysis**: Instant price predictions with confidence scoring
- **Professional UI**: Modern dark theme with responsive design
- **Comprehensive Form**: Covers all aspects of smartphone condition and specifications

## 🏗️ Architecture

```
smartphone_price_prediction/
├── app.py                          # Flask backend API
├── models/                         # ML models and encoders
│   ├── final_model.pkl            # Trained Random Forest model
│   └── brand_encoder.pkl          # Brand label encoder
├── frontend/                       # React frontend application
│   ├── src/                       # React source code
│   ├── public/                    # Static assets
│   └── package.json               # Node.js dependencies
├── data/                          # Training and test data
│   ├── raw/                       # Original datasets
│   └── processed/                 # Preprocessed data
├── notebooks/                     # Jupyter notebooks for analysis
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 🛠️ Technology Stack

### Backend
- **Python 3.8+**
- **Flask** - Web framework
- **Scikit-learn** - Machine learning
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing

### Frontend
- **React 18** - JavaScript framework
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client
- **Material-UI Icons** - Icon library

### Machine Learning
- **Random Forest Regressor** - Main prediction model
- **Label Encoding** - Categorical feature encoding
- **Feature Engineering** - Custom preprocessing pipeline

## 📊 Model Performance

- **Accuracy**: 96.07%
- **Training Samples**: 3,260+
- **Features**: 12 comprehensive smartphone attributes
- **Prediction Time**: < 100ms

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/smartphone-price-prediction.git
cd smartphone-price-prediction

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start Flask server
python app.py
```

### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

### Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8501

## 📋 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/brands` | GET | Get available smartphone brands |
| `/api/models/<brand>` | GET | Get models for a specific brand |
| `/api/options` | GET | Get form options and ranges |
| `/predict` | POST | Submit prediction request |
| `/health` | GET | Health check endpoint |

## 🎯 How It Works

1. **Data Input**: Users fill out a comprehensive form with device specifications
2. **Feature Processing**: Backend processes and encodes categorical features
3. **ML Prediction**: Random Forest model generates price prediction
4. **Confidence Scoring**: Model provides confidence level for each prediction
5. **Result Display**: Frontend shows prediction with detailed analysis

## 📱 Form Fields

### Device Information
- Brand & Model
- Storage & RAM
- Device Age
- Warranty Status

### Physical Condition
- Screen Condition
- Body Condition
- Water Damage
- Battery Health

### Technical Status
- Core Feature Faults
- Accessories Kit

## 🔧 Development

### Project Structure
```
frontend/src/
├── components/
│   └── SmartphonePricePredictor.js  # Main form component
├── App.js                            # Root component
└── index.js                          # Entry point
```

### Key Components
- **SmartphonePricePredictor**: Main form with searchable inputs
- **Dark Theme**: Professional styling with Tailwind CSS
- **Responsive Design**: Works on all device sizes
- **Real-time Search**: Type to find brands and models

### Styling
- **Tailwind CSS CDN**: No build process required
- **Dark Theme**: Professional appearance
- **Responsive Grid**: Adaptive layout system
- **Modern UI**: Clean, industrial design

## 📈 Model Training

To retrain the model with new data:

```bash
python retrain_and_save_model.py
```

This will:
- Load training data from `data/processed/resale.csv`
- Train a new Random Forest model
- Save updated models to `models/` directory
- Update feature encoders

## 🧪 Testing

### Backend Testing
```bash
# Test API endpoints
curl http://localhost:8501/health
curl http://localhost:8501/api/brands
```

### Frontend Testing
```bash
cd frontend
npm test
```

## 📦 Deployment

### Production Build
```bash
cd frontend
npm run build
```

### Docker (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["python", "app.py"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Scikit-learn** for machine learning capabilities
- **React** for the frontend framework
- **Tailwind CSS** for the styling system
- **Flask** for the backend API

## 📞 Support

For support and questions:
- Create an issue in the GitHub repository
- Contact: [your-email@example.com]
- Project Link: [https://github.com/yourusername/smartphone-price-prediction](https://github.com/yourusername/smartphone-price-prediction)

---

**Made with ❤️ for the smartphone market analysis community**
