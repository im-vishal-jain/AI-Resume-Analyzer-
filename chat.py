"""
🤖 AI-POWERED RESUME ANALYZER
Advanced Resume Analysis with Groq AI
Features: Skills Extraction, ATS Score, Improvement Suggestions, Career Match
"""

import streamlit as st
from groq import Groq
import PyPDF2
import docx2txt
import pandas as pd
from datetime import datetime
import time
import re
from typing import Dict, List, Tuple
import plotly.graph_objects as go
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import json

# ============================================
# CONFIGURATION & SETUP
# ============================================

# Groq API Configuration
GROQ_API_KEY = "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"

# Page configuration
st.set_page_config(
    page_title="AI Resume Analyzer | Smart Career Tool",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/resume-analyzer',
        'Report a bug': 'https://github.com/yourusername/resume-analyzer/issues',
        'About': '# AI Resume Analyzer\nAdvanced resume analysis powered by Groq AI'
    }
)

# Initialize Groq client
try:
    client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    st.error(f"⚠️ Failed to initialize Groq client: {e}")
    st.stop()

# ============================================
# ADVANCED CSS STYLESHEET
# ============================================

st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', 'Space Grotesk', sans-serif;
    }
    
    /* Animated Gradient Background */
    .stApp {
        background: linear-gradient(-45deg, #1a1a2e, #16213e, #0f3460, #1a1a2e);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Premium Header */
    .premium-header {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur(20px);
        border-radius: 30px;
        padding: 35px;
        margin-bottom: 30px;
        border: 1px solid rgba(255,255,255,0.2);
        animation: slideDown 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    }
    
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-60px) scale(0.95);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    
    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.15);
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
    }
    
    /* Score Card */
    .score-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 25px;
        padding: 30px;
        text-align: center;
        color: white;
        animation: fadeInUp 0.6s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .score-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .score-number {
        font-size: 4rem;
        font-weight: 800;
        margin: 10px 0;
        position: relative;
        z-index: 1;
    }
    
    /* Analysis Container */
    .analysis-container {
        background: #FFFFFF;
        border-radius: 25px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    /* Skill Tags */
    .skill-tag {
        display: inline-block;
        background: linear-gradient(135deg, #667eea20, #764ba220);
        color: #667eea;
        padding: 5px 15px;
        border-radius: 20px;
        margin: 5px;
        font-size: 0.85rem;
        font-weight: 500;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .skill-tag:hover {
        transform: scale(1.05);
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
        border: 1px solid #e9ecef;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
        margin: 10px 0;
    }
    
    /* Typing Animation */
    .typing-indicator {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 12px 20px;
        background: #f8f9fa;
        border-radius: 20px;
        margin: 10px 0;
    }
    
    .typing-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #667eea;
        animation: typingBounce 1.4s infinite;
    }
    
    @keyframes typingBounce {
        0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
        30% { transform: translateY(-10px); opacity: 1; }
    }
    
    /* Progress Bar */
    .progress-bar-container {
        background: rgba(255,255,255,0.2);
        border-radius: 10px;
        height: 10px;
        overflow: hidden;
        margin: 10px 0;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 10px;
        transition: width 1s ease;
        animation: progressAnimation 1s ease-out;
    }
    
    @keyframes progressAnimation {
        from { width: 0; }
        to { width: var(--width); }
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Button Animations */
    .stButton button {
        transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55) !important;
        border-radius: 25px !important;
        font-weight: 600 !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* File Uploader */
    .upload-area {
        border: 2px dashed rgba(102,126,234,0.5);
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .upload-area:hover {
        border-color: #667eea;
        background: rgba(102,126,234,0.05);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .premium-header {
            padding: 20px;
        }
        
        .score-number {
            font-size: 2.5rem;
        }
    }
    
    /* Floating Animation */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .floating {
        animation: float 3s ease-in-out infinite;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# RESUME ANALYSIS FUNCTIONS
# ============================================

def extract_text_from_pdf(file) -> str:
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"

def extract_text_from_docx(file) -> str:
    """Extract text from DOCX file"""
    try:
        text = docx2txt.process(file)
        return text
    except Exception as e:
        return f"Error extracting DOCX: {str(e)}"

def extract_text_from_txt(file) -> str:
    """Extract text from TXT file"""
    try:
        text = file.read().decode('utf-8')
        return text
    except Exception as e:
        return f"Error extracting TXT: {str(e)}"

def analyze_resume_with_ai(resume_text: str, job_role: str = "") -> Dict:
    """Analyze resume using Groq AI"""
    
    analysis_prompt = f"""You are an expert resume analyzer and career coach. Analyze the following resume and provide a comprehensive evaluation:

RESUME TEXT:
{resume_text[:8000]}  # Limit text length

{f'JOB ROLE: {job_role}' if job_role else ''}

Please provide a detailed analysis in the following JSON format:

{{
    "ats_score": (0-100 score based on ATS compatibility),
    "overall_score": (0-100 overall resume quality score),
    "strengths": ["strength1", "strength2", ...],
    "weaknesses": ["weakness1", "weakness2", ...],
    "skills": ["skill1", "skill2", ...],
    "experience_years": (estimated years of experience),
    "education_level": (highest education level detected),
    "missing_keywords": ["keyword1", "keyword2", ...],
    "improvement_suggestions": ["suggestion1", "suggestion2", ...],
    "format_score": (0-100 formatting score),
    "content_score": (0-100 content quality score),
    "impact_score": (0-100 achievement impact score),
    "summary": "Brief executive summary of the resume",
    "recommended_job_titles": ["title1", "title2", "title3"],
    "industry_fit": (0-100 industry relevance score)
}}

Be thorough and objective in your analysis."""
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": analysis_prompt}],
            temperature=0.3,
            max_tokens=2048,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        st.error(f"AI Analysis Error: {str(e)}")
        return None

def generate_word_cloud(text: str):
    """Generate word cloud from resume text"""
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        colormap='viridis',
        max_words=100,
        contour_width=1,
        contour_color='#667eea'
    ).generate(text)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    return fig

def create_score_gauge(score: int, title: str):
    """Create a gauge chart for scores"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        title = {'text': title, 'font': {'size': 14}},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1},
            'bar': {'color': "#667eea"},
            'steps': [
                {'range': [0, 40], 'color': "#ff6b6b"},
                {'range': [40, 70], 'color': "#ffd93d"},
                {'range': [70, 100], 'color': "#6bcf7f"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20))
    return fig

def extract_skills_advanced(text: str) -> List[str]:
    """Advanced skill extraction using pattern matching"""
    skills = []
    
    # Common tech skills
    tech_skills = [
        'Python', 'Java', 'JavaScript', 'React', 'Angular', 'Vue', 'Node.js',
        'SQL', 'MongoDB', 'AWS', 'Azure', 'Docker', 'Kubernetes', 'TensorFlow',
        'PyTorch', 'Machine Learning', 'AI', 'Data Science', 'Analytics', 'Git',
        'Agile', 'Scrum', 'Project Management', 'Leadership', 'Communication'
    ]
    
    # Extract skills from text
    for skill in tech_skills:
        if skill.lower() in text.lower():
            skills.append(skill)
    
    return list(set(skills))

def calculate_ats_score(resume_text: str) -> int:
    """Calculate ATS compatibility score"""
    score = 0
    
    # Check for standard sections
    sections = ['education', 'experience', 'skills', 'summary', 'projects']
    for section in sections:
        if section in resume_text.lower():
            score += 10
    
    # Check for keywords
    keywords = ['achieved', 'increased', 'improved', 'reduced', 'developed', 'managed', 'led']
    for keyword in keywords:
        if keyword in resume_text.lower():
            score += 5
    
    # Check for formatting issues
    if len(resume_text.split()) > 300:  # Sufficient length
        score += 10
    
    # Check for contact info
    if re.search(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', resume_text):
        score += 10
    if re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', resume_text):
        score += 10
    
    return min(100, score)

# ============================================
# UI COMPONENTS
# ============================================

def render_header():
    """Render premium header"""
    st.markdown("""
    <div class="premium-header">
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap;">
            <div>
                <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 10px;">
                    <div style="font-size: 3rem; animation: float 3s ease-in-out infinite;">📄</div>
                    <div>
                        <h1 style="color: white; margin: 0; font-size: 2.5rem; font-weight: 800;">
                            AI Resume Analyzer
                        </h1>
                        <p style="color: rgba(255,255,255,0.9); margin: 5px 0 0 0;">
                            <span style="background: rgba(102,126,234,0.5); padding: 2px 8px; border-radius: 12px; font-size: 0.8rem;">
                                🤖 AI-Powered Analysis
                            </span>
                            <span style="background: rgba(102,126,234,0.5); padding: 2px 8px; border-radius: 12px; font-size: 0.8rem; margin-left: 8px;">
                                ⚡ Instant Insights
                            </span>
                            <span style="background: rgba(102,126,234,0.5); padding: 2px 8px; border-radius: 12px; font-size: 0.8rem; margin-left: 8px;">
                                🎯 Career Match
                            </span>
                        </p>
                    </div>
                </div>
            </div>
            <div style="display: flex; gap: 12px;">
                <div style="background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 25px; text-align: center;">
                    <div style="font-size: 1.2rem; font-weight: 700;">Groq AI</div>
                    <div style="font-size: 0.7rem;">Deep Analysis</div>
                </div>
                <div style="background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 25px; text-align: center;">
                    <div style="font-size: 1.2rem; font-weight: 700;">ATS Ready</div>
                    <div style="font-size: 0.7rem;">Optimized</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render sidebar with options"""
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="font-size: 2.5rem;">🎯</div>
            <h2 style="color: white; margin: 5px 0;">Analysis Settings</h2>
        </div>
        """, unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### 📝 Job Context")
            
            job_role = st.text_input(
                "Target Job Role",
                placeholder="e.g., Data Scientist, Software Engineer",
                help="Specify job role for targeted analysis"
            )
            
            industry = st.selectbox(
                "Industry",
                ["Technology", "Healthcare", "Finance", "Marketing", "Education", "Other"]
            )
            
            experience_level = st.select_slider(
                "Target Experience Level",
                options=["Entry", "Junior", "Mid-Level", "Senior", "Lead/Manager"],
                value="Mid-Level"
            )
            st.markdown('</div>', unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### ⚙️ Analysis Options")
            
            analyze_format = st.checkbox("Format Analysis", value=True)
            analyze_content = st.checkbox("Content Analysis", value=True)
            analyze_ats = st.checkbox("ATS Compatibility", value=True)
            generate_suggestions = st.checkbox("Improvement Suggestions", value=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### 📊 Sample Resumes")
            
            if st.button("📄 Load Sample Resume", use_container_width=True):
                sample_text = """
                JOHN DOE
                Senior Software Engineer
                
                SUMMARY
                Experienced software engineer with 8+ years in full-stack development.
                Expertise in Python, React, and cloud technologies. Led teams of 5+ developers.
                
                EXPERIENCE
                Senior Software Engineer | Tech Corp | 2020-Present
                - Led development of microservices architecture serving 1M+ users
                - Improved system performance by 40% through optimization
                - Mentored 3 junior developers
                
                Software Engineer | Startup Inc | 2016-2020
                - Built REST APIs serving 500K daily requests
                - Implemented CI/CD pipeline reducing deployment time by 60%
                
                EDUCATION
                MS in Computer Science | University of Technology | 2016
                BS in Software Engineering | State University | 2014
                
                SKILLS
                Python, JavaScript, React, Node.js, AWS, Docker, Kubernetes, MongoDB, PostgreSQL
                """
                st.session_state.sample_loaded = sample_text
                st.success("Sample resume loaded!")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        return job_role, industry, experience_level, analyze_format, analyze_content, analyze_ats, generate_suggestions

def render_analysis_results(analysis: Dict, resume_text: str, job_role: str):
    """Render comprehensive analysis results"""
    
    if not analysis:
        return
    
    # Main Score Card
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="score-card">', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="position: relative; z-index: 1;">
            <div>🎯 Overall Score</div>
            <div class="score-number">{analysis.get('overall_score', 0)}</div>
            <div>/100</div>
            <div class="progress-bar-container" style="margin-top: 15px;">
                <div class="progress-bar" style="width: {analysis.get('overall_score', 0)}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="score-card">', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="position: relative; z-index: 1;">
            <div>🤖 ATS Score</div>
            <div class="score-number">{analysis.get('ats_score', 0)}</div>
            <div>/100</div>
            <div class="progress-bar-container" style="margin-top: 15px;">
                <div class="progress-bar" style="width: {analysis.get('ats_score', 0)}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="score-card">', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="position: relative; z-index: 1;">
            <div>💼 Industry Fit</div>
            <div class="score-number">{analysis.get('industry_fit', 0)}</div>
            <div>/100</div>
            <div class="progress-bar-container" style="margin-top: 15px;">
                <div class="progress-bar" style="width: {analysis.get('industry_fit', 0)}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Detailed Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("📝 **Format Score**")
        st.markdown(f'<div class="metric-value">{analysis.get("format_score", 0)}</div>', unsafe_allow_html=True)
        st.markdown(f'<small>{ "Excellent" if analysis.get("format_score", 0) > 70 else "Needs Improvement" }</small>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("📄 **Content Score**")
        st.markdown(f'<div class="metric-value">{analysis.get("content_score", 0)}</div>', unsafe_allow_html=True)
        st.markdown(f'<small>{ "Rich & Detailed" if analysis.get("content_score", 0) > 70 else "Needs More Details" }</small>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("⚡ **Impact Score**")
        st.markdown(f'<div class="metric-value">{analysis.get("impact_score", 0)}</div>', unsafe_allow_html=True)
        st.markdown(f'<small>{ "Strong Achievements" if analysis.get("impact_score", 0) > 70 else "Add More Metrics" }</small>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Executive Summary
    with st.container():
        st.markdown('<div class="analysis-container">', unsafe_allow_html=True)
        st.markdown("### 📋 Executive Summary")
        st.markdown(f'<p style="font-size: 1rem; line-height: 1.6;">{analysis.get("summary", "No summary available")}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Strengths & Weaknesses
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="analysis-container">', unsafe_allow_html=True)
        st.markdown("### ✅ Strengths")
        for strength in analysis.get("strengths", [])[:5]:
            st.markdown(f'<div style="margin: 10px 0;">✓ {strength}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="analysis-container">', unsafe_allow_html=True)
        st.markdown("### ⚠️ Areas for Improvement")
        for weakness in analysis.get("weaknesses", [])[:5]:
            st.markdown(f'<div style="margin: 10px 0;">• {weakness}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Skills Section
    with st.container():
        st.markdown('<div class="analysis-container">', unsafe_allow_html=True)
        st.markdown("### 🛠️ Skills Detected")
        
        skills = analysis.get("skills", [])
        cols = st.columns(4)
        for idx, skill in enumerate(skills):
            col_idx = idx % 4
            with cols[col_idx]:
                st.markdown(f'<div class="skill-tag">{skill}</div>', unsafe_allow_html=True)
        
        if not skills:
            st.info("No skills detected. Consider adding a dedicated skills section.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Missing Keywords
    if analysis.get("missing_keywords"):
        with st.container():
            st.markdown('<div class="analysis-container">', unsafe_allow_html=True)
            st.markdown("### 🔍 Missing Keywords (Add These!)")
            missing_keywords = analysis.get("missing_keywords", [])
            for keyword in missing_keywords[:8]:
                st.markdown(f'<span style="background: #ff6b6b20; padding: 5px 12px; border-radius: 20px; margin: 5px; display: inline-block;">+ {keyword}</span>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Improvement Suggestions
    if analysis.get("improvement_suggestions"):
        with st.container():
            st.markdown('<div class="analysis-container">', unsafe_allow_html=True)
            st.markdown("### 💡 Actionable Improvements")
            for i, suggestion in enumerate(analysis.get("improvement_suggestions", [])[:8], 1):
                st.markdown(f'<div style="margin: 12px 0;">{i}. {suggestion}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Career Recommendations
    with st.container():
        st.markdown('<div class="analysis-container">', unsafe_allow_html=True)
        st.markdown("### 🎯 Career Recommendations")
        
        if analysis.get("recommended_job_titles"):
            st.markdown("**Recommended Job Titles:**")
            for title in analysis.get("recommended_job_titles", [])[:3]:
                st.markdown(f'<div class="skill-tag">{title}</div>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="margin-top: 20px;">
            <strong>Experience Level:</strong> {analysis.get("experience_years", "N/A")} years<br>
            <strong>Education Level:</strong> {analysis.get("education_level", "N/A")}
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Word Cloud
    with st.container():
        st.markdown('<div class="analysis-container">', unsafe_allow_html=True)
        st.markdown("### 🌟 Resume Word Cloud")
        
        try:
            fig = generate_word_cloud(resume_text)
            st.pyplot(fig)
        except Exception as e:
            st.warning(f"Could not generate word cloud: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

def render_upload_area():
    """Render file upload area"""
    uploaded_file = st.file_uploader(
        "📄 Upload Your Resume",
        type=['pdf', 'docx', 'txt'],
        help="Supported formats: PDF, DOCX, TXT"
    )
    
    if uploaded_file:
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        with st.spinner("📄 Extracting text from resume..."):
            if file_extension == 'pdf':
                resume_text = extract_text_from_pdf(uploaded_file)
            elif file_extension == 'docx':
                resume_text = extract_text_from_docx(uploaded_file)
            else:
                resume_text = extract_text_from_txt(uploaded_file)
            
            if "Error" in resume_text:
                st.error(resume_text)
                return None
            
            st.success(f"✅ Successfully extracted {len(resume_text)} characters")
            return resume_text
    
    return None

# ============================================
# MAIN APPLICATION
# ============================================

def main():
    """Main application entry point"""
    
    # Render header
    render_header()
    
    # Render sidebar and get settings
    job_role, industry, experience_level, analyze_format, analyze_content, analyze_ats, generate_suggestions = render_sidebar()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📄 Upload Your Resume")
        st.markdown("Upload your resume in PDF, DOCX, or TXT format for AI-powered analysis")
        
        # File upload area
        resume_text = render_upload_area()
        
        # Check for sample resume
        if 'sample_loaded' in st.session_state and not resume_text:
            resume_text = st.session_state.sample_loaded
            st.info("📄 Sample resume loaded. Click 'Analyze Resume' to see results.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🚀 Quick Start")
        st.markdown("""
        **What we analyze:**
        - ✅ ATS Compatibility Score
        - ✅ Skills Detection
        - ✅ Experience Level
        - ✅ Format & Structure
        - ✅ Content Quality
        - ✅ Achievement Impact
        - ✅ Missing Keywords
        - ✅ Improvement Suggestions
        
        **Supported Formats:**
        - PDF (.pdf)
        - Word (.docx)
        - Text (.txt)
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Analyze button
    if resume_text:
        if st.button("🔍 Analyze Resume", use_container_width=True, type="primary"):
            
            # Show analysis progress
            progress_placeholder = st.empty()
            status_placeholder = st.empty()
            
            # Step 1: Basic analysis
            status_placeholder.markdown('<div class="typing-indicator"><div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div><span>📊 Performing initial analysis...</span></div>', unsafe_allow_html=True)
            time.sleep(1)
            
            # Step 2: AI Analysis
            status_placeholder.markdown('<div class="typing-indicator"><div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div><span>🤖 AI is analyzing your resume...</span></div>', unsafe_allow_html=True)
            
            analysis = analyze_resume_with_ai(resume_text, job_role)
            
            # Add additional metrics
            if analysis:
                analysis['ats_score'] = calculate_ats_score(resume_text)
                analysis['skills'] = extract_skills_advanced(resume_text)
            
            # Step 3: Complete
            status_placeholder.markdown('<div class="typing-indicator"><div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div><span>✅ Analysis complete! Generating insights...</span></div>', unsafe_allow_html=True)
            time.sleep(1)
            
            status_placeholder.empty()
            
            if analysis:
                # Store in session state
                st.session_state.analysis_results = analysis
                st.session_state.resume_text = resume_text
                st.rerun()
            else:
                st.error("Analysis failed. Please try again.")
    
    # Display results if available
    if 'analysis_results' in st.session_state:
        st.markdown("---")
        st.markdown("## 📊 Analysis Results")
        render_analysis_results(
            st.session_state.analysis_results,
            st.session_state.resume_text,
            job_role
        )
        
        # Export options
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📥 Download Report", use_container_width=True):
                report = f"""
                Resume Analysis Report
                ======================
                Overall Score: {st.session_state.analysis_results.get('overall_score', 0)}/100
                ATS Score: {st.session_state.analysis_results.get('ats_score', 0)}/100
                
                Summary: {st.session_state.analysis_results.get('summary', 'N/A')}
                
                Strengths:
                {chr(10).join(['- ' + s for s in st.session_state.analysis_results.get('strengths', [])])}
                
                Improvements Needed:
                {chr(10).join(['- ' + w for w in st.session_state.analysis_results.get('weaknesses', [])])}
                
                Skills Detected:
                {', '.join(st.session_state.analysis_results.get('skills', []))}
                
                Recommendations:
                {chr(10).join([f"{i+1}. {s}" for i, s in enumerate(st.session_state.analysis_results.get('improvement_suggestions', []))])}
                """
                st.download_button(
                    label="💾 Download Report",
                    data=report,
                    file_name=f"resume_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        
        with col2:
            if st.button("🔄 New Analysis", use_container_width=True):
                del st.session_state.analysis_results
                del st.session_state.resume_text
                st.rerun()
        
        with col3:
            if st.button("📧 Email Report", use_container_width=True):
                st.info("Report export feature coming soon!")
    
    # Footer
    st.markdown("""
    <div style="text-align: center; padding: 20px; margin-top: 30px; background: rgba(0,0,0,0.3); border-radius: 20px;">
        <p style="margin: 0; color: rgba(255,255,255,0.9);">
            🚀 <strong>AI Resume Analyzer v1.0</strong> | Powered by Vishal Kumar | Intelligent Career Insights
        </p>
        <p style="margin: 5px 0 0 0; font-size: 0.75rem; color: rgba(255,255,255,0.6);">
            Optimize your resume for ATS | Get personalized improvement suggestions | Land your dream job
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()