# MindCare - AI-Powered Mental Health Support Bot

A compassionate, AI-powered chatbot designed to support individuals experiencing mental health challenges. Built with empathy, safety, and user well-being at its core.

## 🌟 Features

### 1. **Advanced AI Conversation**
- Uses HuggingFace's mental health therapy model (Mistral-7B fine-tuned)
- Empathetic, non-judgmental responses
- Context-aware conversations that remember previous interactions

### 2. **Soothing UI/UX**
- Calming color palette (soft blues, mint greens, gentle pinks)
- Smooth animations and transitions
- Professional, clean design
- Mobile-responsive layout

### 3. **Intelligent Pattern Recognition**
- Automatically detects mental health symptoms:
  - Depression indicators
  - Anxiety patterns
  - Stress markers
  - Trauma signals
  - Self-harm mentions
  - Suicidal ideation
- Real-time conversation analysis

### 4. **Mental Health Analysis Dashboard**
- Comprehensive mental health overview
- Risk level assessment (Low, Moderate, High, Critical)
- Severity scoring system
- Conversation tracking
- Personalized recommendations

### 5. **Emergency SOS System**
- One-click emergency alert
- Automatic notification to pre-configured emergency contacts
- Triggered automatically when critical risk levels detected
- Immediate crisis resource information

### 6. **Crisis Resources**
- 24/7 crisis hotline information
- International support resources
- Emergency contact integration
- Direct links to professional help

## 🎨 UI Design Principles

### Color Psychology
- **Soft Blue (#6B9BD1)**: Calming, trustworthy
- **Mint Green (#A8D5BA)**: Peaceful, healing
- **Soft Pink (#F4C2C2)**: Warm, comforting
- **Light Gray (#F0F4F8)**: Clean, spacious

### Features
- Clear, readable typography (Poppins font)
- Smooth gradient backgrounds
- Gentle shadows and rounded corners
- Intuitive navigation
- Accessible design

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Step 1: Clone or Download

```bash
# Create project directory
mkdir mindcare-bot
cd mindcare-bot
```

### Step 2: Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### Step 3: Download AI Model

The application will automatically download the required model on first run. Initial setup may take 5-10 minutes depending on your internet connection.

**Model Options:**
- **Production**: `Amod/mental-health-therapy-mistral-7b-ins-SFT` (Recommended, ~14GB)
- **Development**: `microsoft/DialoGPT-medium` (Faster, ~350MB)

### Step 4: Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## 📁 Project Structure

```
mindcare-bot/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Frontend UI
├── static/               # (Optional) Static files
├── README.md             # Documentation
└── venv/                 # Virtual environment
```

## 🔧 Configuration

### Emergency Contacts Setup

Users should configure emergency contacts during sign-up. Modify the `/api/register` endpoint:

```python
# Example emergency contact structure
emergency_contacts = [
    {
        'name': 'John Doe',
        'email': 'john@example.com',
        'phone': '+1234567890',
        'relation': 'Family'
    }
]
```

### Email/SMS Integration

For production deployment, integrate actual email/SMS services:

1. **Email**: Use SMTP with services like Gmail, SendGrid, or AWS SES
2. **SMS**: Integrate Twilio, AWS SNS, or similar services

Update the `send_emergency_message()` function in `app.py`.

## 🤖 AI Model Details

### Primary Model
**Model**: `Amod/mental-health-therapy-mistral-7b-ins-SFT`
- Fine-tuned Mistral-7B for mental health counseling
- Trained on mental health counseling conversations
- Empathetic and supportive responses

### Model Features
- Context-aware conversations
- Symptom detection
- Crisis recognition
- Supportive language generation

## 📊 Mental Health Analysis System

### Risk Levels
1. **Low (0-7 points)**: General support needed
2. **Moderate (8-14 points)**: Professional consultation recommended
3. **High (15-24 points)**: Immediate professional help advised
4. **Critical (25+ points)**: Emergency intervention required

### Severity Scoring
- Each symptom category has a weight (1-10)
- Score accumulates based on frequency and severity
- Automatic SOS triggered at critical levels

### Symptom Categories
- Depression
- Anxiety
- Stress
- Trauma
- Self-harm
- Suicidal ideation

## 🛡️ Safety Features

### 1. Automatic Crisis Detection
- Real-time message analysis
- Pattern recognition for crisis indicators
- Immediate alert system

### 2. Resource Provision
- 24/7 crisis hotlines displayed
- Emergency contact quick access
- Professional help recommendations

### 3. Data Privacy
- Session-based user tracking
- No permanent storage of sensitive data (can be modified for production)
- Secure communication

## 💡 Usage Guidelines

### For Users
1. **Be Honest**: Share your genuine feelings
2. **Take Your Time**: No rush in conversations
3. **Seek Professional Help**: This bot supplements, not replaces, professional care
4. **Emergency**: If in immediate danger, call 911 or local emergency services

### For Developers
1. **Test Thoroughly**: Ensure all safety features work
2. **Monitor Performance**: Track model response quality
3. **Update Models**: Keep AI models current
4. **Privacy First**: Implement proper data protection

## 🔒 Security Considerations

### Production Deployment Checklist
- [ ] Change Flask secret key
- [ ] Implement HTTPS
- [ ] Add user authentication
- [ ] Secure emergency contact storage
- [ ] Implement rate limiting
- [ ] Add CSRF protection
- [ ] Set up proper logging
- [ ] Configure CORS properly
- [ ] Use environment variables for secrets
- [ ] Implement data encryption

## 🌐 Deployment

### Local Testing
```bash
python app.py
```

### Production Deployment

**Recommended Platforms:**
- Heroku
- AWS EC2
- Google Cloud Platform
- DigitalOcean

**Steps:**
1. Set up production server
2. Configure environment variables
3. Use production WSGI server (Gunicorn)
4. Set up reverse proxy (Nginx)
5. Configure SSL/TLS
6. Set up monitoring and logging

## 📝 API Endpoints

### POST `/api/chat`
Send a message and receive AI response
```json
{
  "message": "I'm feeling anxious today"
}
```

### GET `/api/analysis`
Get user's mental health analysis
```json
{
  "severity_score": 12,
  "risk_level": "moderate",
  "symptom_counts": {...},
  "recommendation": {...}
}
```

### POST `/api/sos`
Trigger emergency SOS
```json
{
  "emergency_contacts": [...]
}
```

### POST `/api/register`
Register user and emergency contacts
```json
{
  "user_id": "user123",
  "emergency_contacts": [...]
}
```

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Enhanced AI models
- Additional language support
- Improved symptom detection
- Mobile app development
- Integration with healthcare systems

## ⚠️ Disclaimer

**IMPORTANT**: This chatbot is a support tool and does not replace professional mental health care. If you or someone you know is in crisis:

- **US**: Call 988 (Suicide & Crisis Lifeline)
- **Text**: HOME to 741741 (Crisis Text Line)
- **International**: Visit findahelpline.com
- **Emergency**: Call 911 or local emergency services

## 📜 License

This project is created for educational and supportive purposes. Please ensure compliance with healthcare regulations (HIPAA, GDPR) before production deployment.

## 👥 Support

For questions, issues, or suggestions:
- Open an issue on GitHub
- Contact: support@mindcare.example.com
- Documentation: docs.mindcare.example.com

## 🙏 Acknowledgments

- HuggingFace for providing mental health AI models
- Mental health professionals who reviewed the approach
- Open-source community for tools and libraries
- Crisis support organizations for resources

---

**Remember**: You're not alone. Help is available, and it's okay to ask for support. 💙

