"""
MindCare Mental Health Bot - Streamlit Version
Deploy easily on Streamlit Cloud for FREE
"""

import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import re
from collections import defaultdict
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="MindCare - Mental Health Support",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for calming UI
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #E3F2FD 0%, #F0F4F8 100%);
    }
    
    .main-header {
        background: linear-gradient(135deg, #6B9BD1 0%, #5A8AC6 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stChatMessage {
        background-color: white;
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .user-message {
        background: linear-gradient(135deg, #6B9BD1 0%, #5A8AC6 100%);
        color: white;
    }
    
    .bot-message {
        background: white;
        border: 2px solid #E1E8ED;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .crisis-box {
        background: linear-gradient(135deg, #FFE0B2 0%, #FFB74D 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #FF9800;
    }
    
    .sos-button {
        background: #E57373;
        color: white;
        font-weight: bold;
        padding: 1rem 2rem;
        border-radius: 25px;
        border: none;
        cursor: pointer;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# Mental health patterns
MENTAL_HEALTH_PATTERNS = {
    'depression': [
        r'\b(sad|depressed|hopeless|worthless|empty|numb)\b',
        r'\b(no energy|tired|exhausted|fatigue)\b',
        r'\b(can\'t sleep|insomnia|sleeping too much)\b',
    ],
    'anxiety': [
        r'\b(anxious|worried|nervous|panic|fear|scared)\b',
        r'\b(can\'t breathe|heart racing|sweating|trembling)\b',
    ],
    'stress': [
        r'\b(overwhelmed|stressed|pressure|burden)\b',
        r'\b(can\'t cope|too much|breaking down)\b',
    ],
    'suicidal': [
        r'\b(suicide|kill myself|end my life|want to die)\b',
        r'\b(better off dead|no reason to live)\b',
    ]
}

SEVERITY_WEIGHTS = {
    'suicidal': 10,
    'depression': 6,
    'anxiety': 5,
    'stress': 4
}

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat_history_ids = None
    st.session_state.symptom_counts = defaultdict(int)
    st.session_state.severity_score = 0
    st.session_state.risk_level = 'low'
    st.session_state.conversation_count = 0

# Load model (cached)
@st.cache_resource
def load_model():
    """Load the AI model"""
    try:
        model_name = "microsoft/DialoGPT-medium"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        return tokenizer, model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None

def analyze_message(message):
    """Analyze message for mental health symptoms"""
    detected = []
    message_lower = message.lower()
    
    for symptom, patterns in MENTAL_HEALTH_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, message_lower, re.IGNORECASE):
                detected.append(symptom)
                st.session_state.symptom_counts[symptom] += 1
                break
    
    return detected

def calculate_severity():
    """Calculate severity score and risk level"""
    score = 0
    for symptom, count in st.session_state.symptom_counts.items():
        weight = SEVERITY_WEIGHTS.get(symptom, 3)
        score += weight * min(count, 3)
    
    st.session_state.severity_score = score
    
    # Determine risk level
    if score >= 25 or st.session_state.symptom_counts['suicidal'] > 0:
        st.session_state.risk_level = 'critical'
    elif score >= 15:
        st.session_state.risk_level = 'high'
    elif score >= 8:
        st.session_state.risk_level = 'moderate'
    else:
        st.session_state.risk_level = 'low'

def get_empathetic_response(message, symptoms):
    """Generate empathetic fallback response"""
    if 'suicidal' in symptoms:
        return ("I'm deeply concerned about what you're sharing. Your life has value, and you deserve support. "
                "Please reach out to a crisis counselor - call 988 (US) or your local emergency services. "
                "You're not alone in this.")
    
    if 'depression' in symptoms:
        return ("I hear that you're going through a really tough time. Your feelings are valid, and you don't "
                "have to face this alone. What's been the hardest part for you lately?")
    
    if 'anxiety' in symptoms:
        return ("It sounds like you're experiencing a lot of anxiety. Remember to breathe - you're safe right now. "
                "What's been triggering these anxious feelings?")
    
    responses = [
        "Thank you for sharing that with me. I'm here to listen. Tell me more about what's on your mind.",
        "I appreciate you opening up. Your feelings are valid. How are you feeling right now?",
        "That sounds really challenging. I'm glad you're talking about it. What would help you most right now?"
    ]
    
    return responses[len(message) % len(responses)]

# Header
st.markdown("""
<div class="main-header">
    <h1>🧠 MindCare - Mental Health Support</h1>
    <p>Your safe, judgment-free space for emotional support</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("💙 Mental Health Overview")
    
    # Risk level indicator
    risk_colors = {
        'low': '🟢',
        'moderate': '🟡',
        'high': '🟠',
        'critical': '🔴'
    }
    
    st.markdown(f"""
    <div class="metric-card">
        <h3>Risk Level: {risk_colors.get(st.session_state.risk_level, '⚪')} {st.session_state.risk_level.upper()}</h3>
        <p>Severity Score: {st.session_state.severity_score}</p>
        <p>Conversations: {st.session_state.conversation_count}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Crisis resources
    st.markdown("""
    <div class="crisis-box">
        <h3>🆘 Crisis Resources</h3>
        <p><strong>Suicide & Crisis Lifeline:</strong><br>988 (US) - 24/7 Support</p>
        <p><strong>Crisis Text Line:</strong><br>Text HOME to 741741</p>
        <p><strong>Emergency:</strong> 911</p>
        <p><strong>International:</strong><br>findahelpline.com</p>
    </div>
    """, unsafe_allow_html=True)
    
    # SOS Button
    if st.button("🔴 EMERGENCY SOS", type="primary", use_container_width=True):
        st.error("⚠️ If you're in immediate danger, please call 911 or go to your nearest emergency room.")
        st.warning("📞 Call 988 for the Suicide & Crisis Lifeline (24/7)")
        st.info("💬 Text HOME to 741741 for Crisis Text Line")
    
    st.markdown("---")
    
    # About section
    with st.expander("ℹ️ About MindCare"):
        st.write("""
        MindCare is an AI-powered mental health support bot designed to:
        - Provide emotional support
        - Detect concerning patterns
        - Offer resources and guidance
        - Connect you with professional help
        
        **Important:** This bot is a support tool, not a replacement for professional mental health care.
        """)
    
    # Detected symptoms
    if st.session_state.symptom_counts:
        with st.expander("📊 Detected Patterns"):
            for symptom, count in st.session_state.symptom_counts.items():
                st.write(f"• {symptom.title()}: {count} mentions")

# Main chat area
st.header("💬 Your Safe Space to Talk")

# Load model
tokenizer, model = load_model()

if tokenizer is None or model is None:
    st.error("Failed to load AI model. Using fallback responses.")

# Display welcome message
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown("""
        Hello! I'm here to listen and support you. 💙
        
        This is a safe, judgment-free space where you can share what's on your mind. 
        How are you feeling today?
        """)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything...", key="chat_input"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.conversation_count += 1
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Analyze message
    symptoms = analyze_message(prompt)
    calculate_severity()
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                if tokenizer and model:
                    # Encode input
                    new_input_ids = tokenizer.encode(prompt + tokenizer.eos_token, return_tensors='pt')
                    
                    # Generate with context
                    bot_input_ids = torch.cat([st.session_state.chat_history_ids, new_input_ids], dim=-1) if st.session_state.chat_history_ids is not None else new_input_ids
                    
                    # Generate response
                    st.session_state.chat_history_ids = model.generate(
                        bot_input_ids,
                        max_length=min(bot_input_ids.shape[-1] + 150, 1000),
                        pad_token_id=tokenizer.eos_token_id,
                        do_sample=True,
                        top_p=0.92,
                        top_k=50,
                        temperature=0.8,
                        no_repeat_ngram_size=3
                    )
                    
                    # Decode response
                    response = tokenizer.decode(
                        st.session_state.chat_history_ids[:, bot_input_ids.shape[-1]:][0],
                        skip_special_tokens=True
                    )
                    
                    # Ensure empathetic response for serious symptoms
                    if 'suicidal' in symptoms or not response.strip():
                        response = get_empathetic_response(prompt, symptoms)
                else:
                    response = get_empathetic_response(prompt, symptoms)
                
            except Exception as e:
                st.error(f"Error generating response: {e}")
                response = get_empathetic_response(prompt, symptoms)
        
        st.markdown(response)
    
    # Add bot response to history
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Check for crisis
    if st.session_state.risk_level == 'critical':
        st.error("⚠️ Your responses indicate you may be in crisis. Please reach out for immediate help.")
        st.warning("📞 Call 988 (Suicide & Crisis Lifeline) or 911 for emergencies")

# Footer
st.markdown("---")
st.caption("""
💙 Remember: You're not alone. Professional help is available.  
⚠️ This is a support tool, not a replacement for professional mental health care.  
🆘 For crisis: Call 988 (US) | Text HOME to 741741 | Emergency: 911
""")

# Reset button
if st.button("🔄 Start New Conversation"):
    st.session_state.messages = []
    st.session_state.chat_history_ids = None
    st.session_state.symptom_counts = defaultdict(int)
    st.session_state.severity_score = 0
    st.session_state.risk_level = 'low'
    st.session_state.conversation_count = 0
    st.rerun()
