# Doctor-AI Diagnostic Agreement System

A sophisticated diagnostic intelligence system that compares AI-based medical image analysis with physician-provided text diagnoses to identify diagnostic agreements and discrepancies in chest X-ray interpretation.

## 🎯 Overview

This project is designed for the SRM Hackathon and addresses a critical need in medical diagnostics: validating and enhancing the consistency between AI-driven image analysis and clinical physician assessments. The system processes chest X-ray images and corresponding medical reports to:

- Perform AI-driven image classification
- Extract diagnostic findings from physician reports
- Compare and validate agreement between both diagnoses
- Generate explainability visualizations via GradCAM
- Alert on critical diagnostic discrepancies

## ✨ Key Features

- **Dual Diagnosis Analysis**: Compares AI predictions from chest X-rays with physician clinical assessments
- **Agreement Detection**: Automatically identifies when AI and doctor diagnoses align or conflict
- **Visual Explainability**: Generates GradCAM heatmaps showing which regions influenced AI decisions
- **Real-time Processing**: Instant analysis of uploaded medical images and reports
- **Risk Assessment**: Evaluates risk levels based on diagnostic alignment
- **Detailed Findings**: Extracts and categorizes medical findings from clinical reports
- **RESTful API**: Full-featured backend API for integration with hospital systems
- **Interactive Web UI**: User-friendly interface for healthcare professionals

## 🏗️ System Architecture

```
Client (Web UI)
    ↓
FastAPI Server (api.py)
    ├─ Image Analysis (ResNet-18 on chest X-rays)
    ├─ Text Diagnosis Extraction
    ├─ Agreement Engine
    └─ GradCAM Visualization
```

### Component Overview

| Component | Purpose |
|-----------|---------|
| **predict_image.py** | ResNet-18 model for chest X-ray classification (NORMAL/PNEUMONIA) |
| **text_diagnosis.py** | NLP-based extraction of diagnoses from medical reports |
| **agreement_engine.py** | Compares AI and physician diagnoses, calculates agreement scores |
| **gradcam.py** | Generates visual explanations of AI predictions |
| **utils.py** | Utility functions for preprocessing and data handling |
| **web/index.html, style.css, app.js** | Interactive frontend interface |

## 📋 Prerequisites

- Python 3.11+
- CUDA-compatible GPU (optional, CPU supported)
- 4GB minimum RAM
- Pre-trained model file: `models/xray_model.pth`

## 🚀 Installation

### 1. Clone the Repository
```bash
cd doctor_ai_disagreement
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Verify Model File
Ensure the pre-trained model exists at:
```
models/xray_model.pth
```

## 🎮 Usage

### Start the Server
```bash
python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at: `http://localhost:8000`

### API Endpoints

#### 1. **Health Check**
```
GET /health
```
Response: `{"status": "ok"}`

#### 2. **Analyze Case**
```
POST /analyze
Content-Type: multipart/form-data

Parameters:
  - image: Chest X-ray image file (JPEG/PNG)
  - report: Physician's clinical report (text)
```

**Response:**
```json
{
  "status": "AGREEMENT or DISAGREEMENT",
  "risk_level": "LOW or CRITICAL",
  "agreement_score": 95.2,
  "alert_message": "AI and doctor diagnosis align",
  "alert_type": "success or critical",
  "timestamp": "20260215_143022",
  "image_analysis": {
    "prediction": "NORMAL or PNEUMONIA",
    "confidence": 92.5,
    "detailed_findings": [...]
  },
  "text_analysis": {
    "text_diagnosis": "NORMAL or PNEUMONIA",
    "confidence": 85.0,
    "detailed_findings": [...]
  },
  "discrepancies": [...],
  "gradcam_image": "/gradcam/image.png",
  "original_image": "/gradcam/original.jpg"
}
```

#### 3. **Serve UI**
```
GET /
```
Returns the interactive web interface

## 📊 Model Details

### Image Classification
- **Architecture**: ResNet-18
- **Input Resolution**: 224×224 pixels
- **Classes**: NORMAL, PNEUMONIA
- **Loss Function**: Cross-Entropy Loss
- **Optimization**: Trained on chest X-ray dataset

### Training Data Structure
```
data/chest_xray/
├── train/
│   ├── NORMAL/
│   └── PNEUMONIA/
├── val/
│   ├── NORMAL/
│   └── PNEUMONIA/
└── test/
    ├── NORMAL/
    └── PNEUMONIA/
```

## 🔧 Configuration

### Key Directories
- `models/` - Stores pre-trained model weights
- `data/` - Training, validation, and test datasets
- `src/` - Core application modules
- `web/` - Frontend files
- `temp/` - Temporary files and generated visualizations

### CORS Configuration
The API accepts requests from all origins:
```python
allow_origins=["*"]
allow_methods=["*"]
allow_headers=["*"]
```

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| FastAPI | 0.104.1 | Web framework |
| Uvicorn | 0.24.0 | ASGI server |
| PyTorch | 2.1.0 | Deep learning framework |
| TorchVision | 0.16.0 | Computer vision models |
| Pillow | 10.1.0 | Image processing |
| OpenCV | 4.8.1.78 | Image manipulation |
| NumPy | 1.24.3 | Numerical operations |
| Matplotlib | 3.8.0 | Visualization |

## 🎓 How It Works

### Workflow
1. **User Uploads** X-ray image and physician's clinical report
2. **Image Processing** - Image resized and preprocessed for model input
3. **AI Prediction** - ResNet-18 classifies as NORMAL or PNEUMONIA with confidence
4. **Text Extraction** - Keywords extracted from physician report
5. **Agreement Check** - Compares AI prediction with extracted diagnosis
6. **Discrepancy Analysis** - Identifies misalignments and potential risks
7. **Visualization** - Generates GradCAM heatmap for explainability
8. **Response** - Returns comprehensive analysis with all findings

### Agreement Scoring
```
Score = (1 - |AI_Confidence - Doctor_Confidence|) × 100
```

### Risk Assessment
- **LOW RISK**: AI and physician diagnoses align
- **CRITICAL RISK**: Diagnostic mismatch detected

## 🧪 Testing

Run test scripts to validate components:
```bash
# Test agreement engine
python -m src.test_agreement

# Test text diagnosis extraction
python -m src.test_text_diagnosis
```

## 🎨 Web Interface Features

- **Image Upload**: Drag-and-drop X-ray image upload
- **Report Input**: Text area for physician's clinical findings
- **Real-time Analysis**: Instant processing and results display
- **Visual Feedback**: Color-coded alerts for agreement status
- **GradCAM Visualization**: Click to view AI decision heatmap
- **Detailed Report**: Comprehensive analysis breakdown

## 📈 Performance Metrics

The system provides:
- Prediction confidence levels
- Agreement scores
- Risk assessments
- Detailed finding listings
- Visual explanations

## ⚠️ Important Notes

- **Medical Use**: This system is designed for research and hackathon purposes. Do not use for actual medical diagnosis without proper validation and clinical trials.
- **Model Accuracy**: Performance depends on chest X-ray quality and dataset representativeness
- **Discrepancy Review**: All diagnostic discrepancies should be reviewed by qualified medical professionals
- **Data Privacy**: Ensure compliance with HIPAA and local data protection regulations when handling medical data

## 🔒 Security Considerations

- Input validation on all uploads
- File type checking for images
- Temporary file cleanup
- CORS enabled for development (configure for production)
- Error handling without sensitive information leakage

## 🚀 Deployment

For production deployment:
1. Use a production ASGI server (Gunicorn with Uvicorn workers)
2. Set `--reload` to False
3. Configure CORS appropriately
4. Implement authentication/authorization
5. Set up proper logging and monitoring
6. Use environment variables for sensitive configuration

Example production command:
```bash
gunicorn --workers 4 --worker-class uvicorn.workers.UvicornWorker api:app
```

## 📝 Project Structure

```
doctor_ai_disagreement/
├── api.py                          # Main FastAPI application
├── requirements.txt                # Python dependencies
├── models/
│   └── xray_model.pth             # Pre-trained model weights
├── data/
│   └── chest_xray/                # Dataset directory
├── src/
│   ├── __init__.py
│   ├── predict_image.py            # Image classification
│   ├── text_diagnosis.py           # Text extraction
│   ├── agreement_engine.py         # Agreement logic
│   ├── gradcam.py                  # Visualization
│   ├── utils.py                    # Utilities
│   ├── train_image_model.py        # Training script
│   ├── test_agreement.py           # Testing
│   └── __pycache__/
├── web/
│   ├── index.html                  # Main UI
│   ├── style.css                   # Styling
│   └── app.js                      # Client logic
├── temp/                           # Temporary files
└── README.md                       # This file
```

## 🤝 Contributing

Contributions are welcome! Please:
1. Create a feature branch
2. Implement changes with proper documentation
3. Ensure code follows project conventions
4. Submit a pull request with detailed description

## 📞 Support

For issues or questions:
- Check the API health endpoint: `/health`
- Review server logs for error messages
- Verify model file exists at `models/xray_model.pth`
- Ensure all dependencies are properly installed

## 📄 License

This project is created for the SRM Hackathon 2026.

## 🏥 Disclaimer

This system is an AI-assisted diagnostic tool for research purposes. It should not replace professional medical judgment. Always consult qualified healthcare professionals for medical decisions. The developers assume no liability for misuse or medical outcomes.

---

**Last Updated**: February 15, 2026  
**Project Status**: Active Development
