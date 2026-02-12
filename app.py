import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import date, timedelta
import plotly.express as px
import plotly.graph_objects as go
import base64
from PIL import Image
import io

from ml_model import train_model
from planner import generate_study_plan
from utils import calculate_days_remaining, get_weakest_subject
from pdf_generator import generate_pdf

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="AI Study Planner Pro", 
    page_icon="📚", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# CUSTOM CSS - BEAUTIFUL MODERN UI
# -----------------------------
def load_css():
    st.markdown("""
    <style>
        /* Global Styles */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {
            font-family: 'Inter', sans-serif;
        }
        
        /* Animated Gradient Background */
        .stApp {
            background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
        }
        
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* Glass Morphism Cards */
        .glass-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            border: 1px solid rgba(255, 255, 255, 0.18);
            margin-bottom: 1.5rem;
            transition: transform 0.3s ease;
        }
        
        .glass-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.5);
        }
        
        /* Main Header */
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2.5rem;
            border-radius: 30px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            animation: slideInDown 1s ease;
        }
        
        @keyframes slideInDown {
            from { transform: translateY(-50px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        .main-header h1 {
            font-size: 3.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        
        .main-header p {
            font-size: 1.2rem;
            opacity: 0.95;
            font-weight: 300;
        }
        
        /* Subject Cards */
        .subject-card {
            background: white;
            border-radius: 15px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            border-left: 5px solid #667eea;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
        }
        
        .subject-card:hover {
            border-left-width: 8px;
            box-shadow: 0 8px 15px rgba(102, 126, 234, 0.2);
        }
        
        /* Metric Cards */
        div[data-testid="stMetric"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 15px;
            color: white;
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        div[data-testid="stMetric"] label {
            color: rgba(255,255,255,0.9) !important;
            font-size: 1rem !important;
            font-weight: 400 !important;
        }
        
        div[data-testid="stMetric"] div {
            color: white !important;
            font-size: 1.8rem !important;
            font-weight: 700 !important;
        }
        
        /* Buttons */
        .stButton button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-weight: 600;
            border: none;
            padding: 0.75rem 2rem;
            border-radius: 50px;
            transition: all 0.3s ease;
            width: 100%;
            font-size: 1.1rem;
            letter-spacing: 0.5px;
            border: 1px solid rgba(255,255,255,0.2);
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }
        
        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        }
        
        /* Download Buttons */
        .stDownloadButton button {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            border-radius: 50px;
            font-weight: 600;
        }
        
        /* Input Fields */
        div[data-testid="stNumberInput"] input,
        div[data-testid="stDateInput"] input,
        div[data-testid="stSelectbox"] select,
        div[data-testid="stTextInput"] input {
            border-radius: 12px;
            border: 2px solid #e0e7ff;
            padding: 0.75rem 1rem;
            font-size: 1rem;
            transition: all 0.3s ease;
            background: white;
        }
        
        div[data-testid="stNumberInput"] input:focus,
        div[data-testid="stDateInput"] input:focus,
        div[data-testid="stSelectbox"] select:focus,
        div[data-testid="stTextInput"] input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
        }
        
        /* Sidebar */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
            padding: 2rem 1rem;
            border-right: 1px solid rgba(255,255,255,0.1);
        }
        
        section[data-testid="stSidebar"] .stMarkdown {
            color: white;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
            background: rgba(255,255,255,0.1);
            padding: 0.5rem;
            border-radius: 50px;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 50px;
            padding: 0.75rem 2rem;
            font-weight: 600;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        /* Progress Tracker */
        .progress-card {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            padding: 1.5rem;
            border-radius: 20px;
            color: white;
            margin-top: 2rem;
        }
        
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .fade-in {
            animation: fadeIn 0.6s ease-out;
        }
        
        /* Badge */
        .badge {
            display: inline-block;
            padding: 0.35rem 1rem;
            background: rgba(102, 126, 234, 0.2);
            color: #667eea;
            border-radius: 50px;
            font-size: 0.85rem;
            font-weight: 600;
            margin-right: 0.5rem;
        }
        
        /* Divider */
        .custom-divider {
            background: linear-gradient(90deg, #667eea, transparent);
            height: 2px;
            width: 100%;
            margin: 2rem 0;
        }
        
        /* Success Message */
        div[data-baseweb="notification"] {
            border-radius: 15px;
            border-left: 5px solid;
            animation: slideInRight 0.5s ease;
        }
        
        @keyframes slideInRight {
            from { transform: translateX(50px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        /* Footer */
        .footer {
            text-align: center;
            padding: 2rem;
            color: rgba(255,255,255,0.8);
            font-size: 0.9rem;
        }
        
        /* Tooltip */
        .tooltip {
            position: relative;
            display: inline-block;
            cursor: help;
        }
        
        .tooltip .tooltiptext {
            visibility: hidden;
            width: 200px;
            background: rgba(0,0,0,0.8);
            color: white;
            text-align: center;
            border-radius: 10px;
            padding: 0.5rem;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            margin-left: -100px;
            opacity: 0;
            transition: opacity 0.3s;
        }
        
        .tooltip:hover .tooltiptext {
            visibility: visible;
            opacity: 1;
        }
        
        /* Status Colors */
        .status-critical { color: #ff6b6b; }
        .status-warning { color: #ffd93d; }
        .status-success { color: #6bcf7f; }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .main-header h1 { font-size: 2rem; }
            .glass-card { padding: 1rem; }
        }
    </style>
    """, unsafe_allow_html=True)

# Load CSS
load_css()

# -----------------------------
# SIDEBAR - ENHANCED INFO PANEL
# -----------------------------
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; color: white; margin-bottom: 2rem;'>
        <h2 style='font-size: 2rem; margin-bottom: 0;'>🎯</h2>
        <h3 style='font-weight: 600; margin-bottom: 0.5rem;'>AI Study Planner Pro</h3>
        <p style='opacity: 0.8; font-size: 0.9rem;'>Version 2.0</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: rgba(255,255,255,0.1); padding: 1.5rem; border-radius: 15px; margin-bottom: 1.5rem;'>
        <h4 style='color: white; margin-bottom: 1rem;'>📊 Difficulty Levels</h4>
        <div style='color: rgba(255,255,255,0.9);'>
            <p style='margin-bottom: 0.5rem;'><span style='display: inline-block; width: 10px; height: 10px; background: #ff6b6b; border-radius: 50%; margin-right: 0.5rem;'></span> Weak - 3x weightage</p>
            <p style='margin-bottom: 0.5rem;'><span style='display: inline-block; width: 10px; height: 10px; background: #ffd93d; border-radius: 50%; margin-right: 0.5rem;'></span> Medium - 2x weightage</p>
            <p style='margin-bottom: 0.5rem;'><span style='display: inline-block; width: 10px; height: 10px; background: #6bcf7f; border-radius: 50%; margin-right: 0.5rem;'></span> Strong - 1x weightage</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: rgba(255,255,255,0.1); padding: 1.5rem; border-radius: 15px;'>
        <h4 style='color: white; margin-bottom: 1rem;'>💡 Pro Tips</h4>
        <div style='color: rgba(255,255,255,0.9);'>
            <p style='margin-bottom: 0.5rem;'>✓ Be consistent with daily goals</p>
            <p style='margin-bottom: 0.5rem;'>✓ Use Pomodoro technique</p>
            <p style='margin-bottom: 0.5rem;'>✓ Review weak subjects daily</p>
            <p style='margin-bottom: 0.5rem;'>✓ Take regular breaks</p>
            <p>✓ Stay hydrated</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# MAIN HEADER
# -----------------------------
st.markdown("""
<div class="main-header fade-in">
    <h1>📚 AI Study Planner Pro</h1>
    <p>Smart timetable generator powered by artificial intelligence • Optimize your study schedule for maximum efficiency</p>
    <div style='margin-top: 1rem;'>
        <span class='badge'>🎯 AI-Powered</span>
        <span class='badge'>⚡ Real-time Analytics</span>
        <span class='badge'>📊 Performance Prediction</span>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# MAIN CONTENT CONTAINER
# -----------------------------
with st.container():
    st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
    
    # -----------------------------
    # USER INPUT SECTION - BEAUTIFUL LAYOUT
    # -----------------------------
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("<h3 style='color: #1a1a2e; margin-bottom: 1rem;'>📋 Study Configuration</h3>", unsafe_allow_html=True)
        
        num_subjects = st.number_input(
            "📚 Number of Subjects",
            min_value=1,
            max_value=10,
            value=3,
            step=1,
            help="Enter the total number of subjects you need to study"
        )
        
        total_hours = st.number_input(
            "⏰ Daily Study Hours",
            min_value=1,
            max_value=24,
            value=4,
            step=1,
            help="How many hours can you study per day?"
        )
        
        exam_date = st.date_input(
            "📅 Exam Date",
            min_value=date.today(),
            value=date.today() + timedelta(days=30),
            help="Select your exam date"
        )
    
    with col2:
        st.markdown("<h3 style='color: #1a1a2e; margin-bottom: 1rem;'>⚡ Quick Stats</h3>", unsafe_allow_html=True)
        
        # Placeholder for stats
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); padding: 1.5rem; border-radius: 15px;'>
            <p style='margin-bottom: 0.5rem;'><span style='font-size: 1.5rem; margin-right: 0.5rem;'>🎯</span> Ready to optimize your study plan</p>
            <p style='margin-bottom: 0.5rem;'><span style='font-size: 1.5rem; margin-right: 0.5rem;'>⚡</span> Enter subject details to begin</p>
            <p><span style='font-size: 1.5rem; margin-right: 0.5rem;'>📊</span> Get AI-powered recommendations</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # -----------------------------
    # SUBJECT DETAILS SECTION
    # -----------------------------
    st.markdown("<h3 style='color: #1a1a2e; margin-bottom: 1.5rem;'>📘 Subject Details</h3>", unsafe_allow_html=True)
    
    subjects = []
    weights = []
    
    difficulty_map = {
        "Weak": 3,
        "Medium": 2,
        "Strong": 1
    }
    
    # Create beautiful subject cards
    for i in range(num_subjects):
        with st.container():
            cols = st.columns([1, 1, 0.1])
            
            with cols[0]:
                subject = st.text_input(
                    f"Subject {i+1} Name",
                    key=f"name_{i}",
                    placeholder=f"e.g., Mathematics, Physics, Literature...",
                    help=f"Enter the name of subject {i+1}"
                )
            
            with cols[1]:
                difficulty = st.selectbox(
                    f"Subject {i+1} Difficulty Level",
                    ["Weak", "Medium", "Strong"],
                    key=f"diff_{i}",
                    help="Select your current proficiency level"
                )
            
            if subject.strip() != "":
                subjects.append(subject)
                weights.append(difficulty_map[difficulty])
    
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# GENERATE PLAN BUTTON
# -----------------------------
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    generate_button = st.button(
        "🎯 Generate AI-Powered Study Plan",
        use_container_width=True
    )

# -----------------------------
# STUDY PLAN RESULTS
# -----------------------------
if generate_button:
    if len(subjects) == 0:
        st.error("⚠️ Please enter at least one subject name to generate your study plan.")
        st.stop()
    
    with st.spinner('🤖 AI is generating your personalized study plan...'):
        # Generate study plan
        df, allocated_hours = generate_study_plan(subjects, weights, total_hours)
        days_remaining = calculate_days_remaining(exam_date)
        weakest_subject = get_weakest_subject(subjects, weights)
    
    # Success animation
    st.balloons()
    st.success("✅ Study plan generated successfully! Your personalized schedule is ready.")
    
    # -----------------------------
    # RESULTS IN BEAUTIFUL CARDS
    # -----------------------------
    st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)
    
    # Metrics Row
    st.markdown("<h3 style='color: #1a1a2e; margin-bottom: 1.5rem;'>📊 Study Plan Overview</h3>", unsafe_allow_html=True)
    
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    
    with col_m1:
        st.metric("📆 Days Remaining", f"{days_remaining} days", 
                 delta=f"{'⚠️ Urgent' if days_remaining < 7 else '✅ On track'}")
    
    with col_m2:
        st.metric("📚 Total Subjects", f"{len(subjects)}")
    
    with col_m3:
        avg_hours = np.mean(allocated_hours)
        st.metric("⏰ Avg Daily/Subject", f"{avg_hours:.1f} hrs")
    
    with col_m4:
        total_study_hours = total_hours * days_remaining
        st.metric("🎯 Total Study Time", f"{total_study_hours} hrs")
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # -----------------------------
    # STUDY PLAN TABLE
    # -----------------------------
    st.markdown("<h4 style='color: #1a1a2e; margin-bottom: 1rem;'>📅 Daily Study Allocation</h4>", unsafe_allow_html=True)
    
    # Style the dataframe
    styled_df = df.style\
        .background_gradient(subset=['Daily Allocated Hours'], cmap='Blues')\
        .format({'Daily Allocated Hours': '{:.1f} hrs'})\
        .set_properties(**{
            'background-color': 'white',
            'color': '#1a1a2e',
            'border-color': '#e0e7ff',
            'font-size': '1rem',
            'padding': '0.75rem'
        })
    
    st.dataframe(styled_df, use_container_width=True)
    
    # -----------------------------
    # DOWNLOAD SECTION
    # -----------------------------
    st.markdown("<h4 style='color: #1a1a2e; margin-bottom: 1rem;'>📥 Download Options</h4>", unsafe_allow_html=True)
    
    col_d1, col_d2, col_d3 = st.columns([1, 1, 1])
    
    with col_d1:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📊 Download CSV",
            data=csv,
            file_name=f"study_plan_{date.today().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col_d2:
        try:
            pdf_file = generate_pdf(df)
            st.download_button(
                label="📄 Download PDF",
                data=pdf_file,
                file_name=f"study_plan_{date.today().strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except:
            st.button("📄 PDF (Coming Soon)", disabled=True, use_container_width=True)
    
    with col_d3:
        st.button("📧 Email Plan", disabled=True, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # -----------------------------
    # VISUALIZATIONS
    # -----------------------------
    col_v1, col_v2 = st.columns(2)
    
    with col_v1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='color: #1a1a2e;'>⏲️ Time Distribution</h4>", unsafe_allow_html=True)
        
        # Enhanced pie chart
        fig1, ax1 = plt.subplots(figsize=(6, 4), facecolor='white')
        colors = plt.cm.Purples(np.linspace(0.4, 0.8, len(subjects)))
        wedges, texts, autotexts = ax1.pie(
            allocated_hours, 
            labels=subjects, 
            autopct='%1.1f%%',
            colors=colors,
            startangle=90,
            explode=[0.05] * len(subjects),
            shadow=True,
            textprops={'fontsize': 10, 'weight': 'bold'}
        )
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(9)
            autotext.set_weight('bold')
        
        ax1.axis('equal')
        plt.tight_layout()
        st.pyplot(fig1, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_v2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='color: #1a1a2e;'>📈 Subject Priority</h4>", unsafe_allow_html=True)
        
        # Enhanced bar chart
        fig2, ax2 = plt.subplots(figsize=(8, 4), facecolor='white')
        bars = ax2.bar(subjects, allocated_hours, color=colors, edgecolor='white', linewidth=2)
        
        # Add value labels on bars
        for bar, hours in zip(bars, allocated_hours):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{hours:.1f}h', ha='center', va='bottom', fontweight='bold')
        
        ax2.set_xlabel("Subjects", fontsize=11, fontweight='semibold')
        ax2.set_ylabel("Daily Study Hours", fontsize=11, fontweight='semibold')
        ax2.set_title("Recommended Daily Hours per Subject", fontsize=12, fontweight='bold')
        ax2.grid(axis='y', alpha=0.3, linestyle='--')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # -----------------------------
    # SMART SUGGESTIONS
    # -----------------------------
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h4 style='color: #1a1a2e;'>💡 AI-Powered Recommendations</h4>", unsafe_allow_html=True)
    
    col_s1, col_s2 = st.columns(2)
    
    with col_s1:
        st.info(f"⚡ **Primary Focus:** {weakest_subject}")
        st.markdown(f"""
        - **Priority Level:** High
        - **Daily Hours:** {max(allocated_hours):.1f}h
        - **Recommendation:** Focus on fundamentals and practice problems
        """)
    
    with col_s2:
        strongest_subject = subjects[weights.index(min(weights))] if weights else subjects[0]
        st.success(f"✅ **Maintain Strength:** {strongest_subject}")
        st.markdown(f"""
        - **Current Level:** Strong
        - **Daily Hours:** {min(allocated_hours):.1f}h
        - **Recommendation:** Regular revision and advanced topics
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # -----------------------------
    # ML PERFORMANCE PREDICTION
    # -----------------------------
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h4 style='color: #1a1a2e;'>🤖 AI Performance Prediction</h4>", unsafe_allow_html=True)
    
    try:
        model = train_model()
        avg_difficulty = float(np.mean(weights))
        prediction = model.predict([[total_hours, days_remaining, avg_difficulty]])
        predicted_score = round(float(prediction[0]), 2)
        
        col_p1, col_p2 = st.columns([1, 1])
        
        with col_p1:
            # Create a gauge chart using matplotlib
            fig3, ax3 = plt.subplots(figsize=(6, 3), facecolor='white')
            
            # Define colors for gauge
            if predicted_score < 50:
                color = '#ff6b6b'
                status = "⚠️ At Risk"
            elif predicted_score < 75:
                color = '#ffd93d'
                status = "📚 On Track"
            else:
                color = '#6bcf7f'
                status = "🔥 Excellent"
            
            # Create horizontal gauge
            ax3.barh([0], [predicted_score], color=color, height=0.3)
            ax3.barh([0], [100], color='#e0e0e0', height=0.3, alpha=0.3)
            ax3.set_xlim(0, 100)
            ax3.set_ylim(-0.5, 0.5)
            ax3.set_yticks([])
            ax3.set_xticks([0, 25, 50, 75, 100])
            ax3.set_xlabel('Predicted Score (%)', fontsize=10, fontweight='semibold')
            
            # Add value text
            ax3.text(predicted_score, 0, f'  {predicted_score}%', 
                    ha='left', va='center', fontsize=12, fontweight='bold')
            
            plt.tight_layout()
            st.pyplot(fig3, use_container_width=True)
        
        with col_p2:
            st.markdown(f"""
            <div style='padding: 1.5rem; background: linear-gradient(135deg, {color}15, {color}05); border-radius: 15px;'>
                <h5 style='margin-bottom: 0.5rem; color: {color};'>{status}</h5>
                <p style='font-size: 2.5rem; font-weight: 700; color: {color};'>{predicted_score}%</p>
                <p style='color: #666;'>Expected Performance Score</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Recommendation based on score
        if predicted_score < 50:
            st.error("⚠️ **Critical:** Increase study hours and focus more on weak subjects. Consider using active recall techniques.")
        elif predicted_score < 75:
            st.warning("📚 **Moderate:** You're on the right track. Stay consistent and practice more problems.")
        else:
            st.success("🎯 **Excellent:** Great preparation level! Keep up the good work and help peers.")
            
    except Exception as e:
        st.info("🤖 ML model will be available for predictions after training on your data.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# DAILY PROGRESS TRACKER
# -----------------------------
st.markdown('<div class="glass-card progress-card">', unsafe_allow_html=True)
st.markdown("<h4 style='color: white; margin-bottom: 1.5rem;'>📊 Daily Study Progress Tracker</h4>", unsafe_allow_html=True)

col_t1, col_t2 = st.columns([2, 1])

with col_t1:
    today_hours = st.number_input(
        "Enter hours studied today",
        min_value=0.0,
        max_value=24.0,
        value=0.0,
        step=0.5,
        help="Track your daily study progress",
        key="progress_input"
    )

with col_t2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("➕ Add Today's Progress", use_container_width=True):
        if "progress_data" not in st.session_state:
            st.session_state.progress_data = []
        st.session_state.progress_data.append(today_hours)
        st.success(f"✅ Added {today_hours} hours to your progress!")

# Display progress chart
if "progress_data" in st.session_state and len(st.session_state.progress_data) > 0:
    st.markdown("<h5 style='color: white; margin-top: 1.5rem;'>📈 Your Study Consistency</h5>", unsafe_allow_html=True)
    
    progress_df = pd.DataFrame({
        "Day": range(1, len(st.session_state.progress_data) + 1),
        "Hours Studied": st.session_state.progress_data
    })
    
    # Enhanced progress chart
    fig4, ax4 = plt.subplots(figsize=(10, 4), facecolor='none')
    
    # Plot line with markers
    ax4.plot(progress_df["Day"], progress_df["Hours Studied"], 
            marker='o', linewidth=3, markersize=10, color='white',
            markerfacecolor='white', markeredgecolor='#667eea', markeredgewidth=2)
    
    # Fill area under curve
    ax4.fill_between(progress_df["Day"], progress_df["Hours Studied"], 
                     alpha=0.3, color='white')
    
    # Add target line
    ax4.axhline(y=total_hours, color='#ffd93d', linestyle='--', 
                linewidth=2, label=f'Daily Target ({total_hours}h)')
    
    ax4.set_xlabel("Day", fontsize=11, fontweight='semibold', color='white')
    ax4.set_ylabel("Hours Studied", fontsize=11, fontweight='semibold', color='white')
    ax4.set_title("Study Consistency Graph", fontsize=12, fontweight='bold', color='white')
    ax4.legend(loc='upper left', facecolor='none', edgecolor='white', labelcolor='white')
    ax4.grid(True, alpha=0.2, linestyle='--', color='white')
    
    # Style ticks
    ax4.tick_params(colors='white')
    for spine in ax4.spines.values():
        spine.set_edgecolor('white')
        spine.set_alpha(0.3)
    
    plt.tight_layout()
    st.pyplot(fig4, use_container_width=True)
    
    # Progress summary
    total_studied = sum(st.session_state.progress_data)
    avg_studied = np.mean(st.session_state.progress_data)
    target_achievement = (total_studied / (total_hours * len(st.session_state.progress_data))) * 100
    
    col_s1, col_s2, col_s3 = st.columns(3)
    
    with col_s1:
        st.metric("📊 Total Hours", f"{total_studied:.1f}h", 
                 delta=f"{total_studied - (total_hours * len(st.session_state.progress_data)):.1f}h vs target")
    
    with col_s2:
        st.metric("📈 Daily Average", f"{avg_studied:.1f}h",
                 delta=f"{avg_studied - total_hours:.1f}h vs target")
    
    with col_s3:
        st.metric("🎯 Target Achievement", f"{target_achievement:.1f}%")
else:
    st.info("📝 No progress tracked yet. Start by adding your study hours for today!")

st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("""
<div class="footer">
    <div style='margin-bottom: 1rem;'>
        <span style='margin: 0 1rem;'>📚 AI Study Planner Pro</span>
        <span style='margin: 0 1rem;'>•</span>
        <span style='margin: 0 1rem;'>⚡ Version 2.0</span>
        <span style='margin: 0 1rem;'>•</span>
        <span style='margin: 0 1rem;'>👨‍💻 Developed by Ishant Kshirsagar</span>
    </div>
    <p style='opacity: 0.7; font-size: 0.8rem;'>
        © 2026 Ishant Kshirsagar. All Rights Reserved. 
        AI Study Planner Pro is designed to optimize your learning journey using Artificial Intelligence.
    </p>
</div>

""", unsafe_allow_html=True)