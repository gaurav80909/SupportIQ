import os
import sys
from pathlib import Path
import streamlit as st

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import (
    TOP_K,
    MIN_RETRIEVAL_SIMILARITY,
    MIN_CLASSIFIER_CONFIDENCE,
    EMBEDDINGS_DIR,
)

# --- Page Configuration ---
st.set_page_config(
    page_title="SupportIQ — AI Customer Support Agent",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Top 30 Brands from TWCS Dataset ---
TOP_30_BRANDS = [
    "@AmazonHelp",
    "@AppleSupport",
    "@Uber_Support",
    "@SpotifyCares",
    "@Delta",
    "@Tesco",
    "@AmericanAir",
    "@TMobileHelp",
    "@comcastcares",
    "@British_Airways",
    "@SouthwestAir",
    "@VirginTrains",
    "@Ask_Spectrum",
    "@XboxSupport",
    "@sprintcare",
    "@hulu_support",
    "@sainsburys",
    "@GWRHelp",
    "@AskPlayStation",
    "@ChipotleTweets",
    "@VerizonSupport",
    "@UPSHelp",
    "@ATVIAssist",
    "@O2",
    "@Safaricom_Care",
    "@idea_cares",
    "@AskTarget",
    "@AirAsiaSupport",
    "@BofA_Help",
    "@SW_Help",
]

SUPPORTED_BRANDS = ["@AppleSupport", "@AmazonHelp"]

# --- Premium Dark Mode SaaS Custom CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    .stApp {
        background-color: #0B0F19;
        color: #E2E8F0;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0E1322 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.07);
        padding-top: 1rem;
    }

    /* Top Navbar */
    .saas-navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 14px 24px;
        background: #111827;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
    }
    .navbar-left {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .saas-logo-badge {
        width: 38px;
        height: 38px;
        border-radius: 10px;
        background: linear-gradient(135deg, #2563EB 0%, #7C3AED 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
        box-shadow: 0 2px 10px rgba(37, 99, 235, 0.4);
    }
    .navbar-brand-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #FFFFFF;
        letter-spacing: -0.02em;
        line-height: 1.1;
    }
    .navbar-brand-sub {
        font-size: 0.76rem;
        color: #94A3B8;
        font-weight: 500;
    }
    .navbar-tagline {
        font-size: 0.8rem;
        color: #64748B;
        font-style: italic;
        margin-left: 16px;
        padding-left: 16px;
        border-left: 1px solid rgba(255, 255, 255, 0.1);
    }
    @media (max-width: 900px) {
        .navbar-tagline { display: none; }
    }
    .navbar-center {
        display: flex;
        gap: 18px;
    }
    .nav-link {
        color: #94A3B8;
        font-size: 0.86rem;
        font-weight: 500;
        text-decoration: none;
        padding: 4px 10px;
        border-radius: 6px;
        transition: all 0.2s;
    }
    .nav-link.active {
        color: #38BDF8;
        background: rgba(56, 189, 248, 0.08);
        font-weight: 600;
    }
    .navbar-right {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .user-avatar-circle {
        width: 34px;
        height: 34px;
        border-radius: 50%;
        background: linear-gradient(135deg, #1E293B, #334155);
        border: 1px solid rgba(255, 255, 255, 0.15);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
        font-weight: 700;
        color: #38BDF8;
    }

    /* Hero Section */
    .hero-container {
        padding: 6px 0 22px 0;
        text-align: left;
    }
    .hero-title {
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #FFFFFF 30%, #94A3B8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
    }
    .hero-desc {
        font-size: 0.98rem;
        color: #94A3B8;
        max-width: 780px;
        margin-bottom: 20px;
        line-height: 1.5;
    }

    /* Capability Cards */
    .cap-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 14px;
        margin-bottom: 24px;
    }
    @media (max-width: 800px) {
        .cap-grid { grid-template-columns: repeat(2, 1fr); }
    }
    .cap-card {
        background: linear-gradient(180deg, #151D2E 0%, #111726 100%);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 10px;
        padding: 14px 16px;
        transition: all 0.2s;
    }
    .cap-card:hover {
        border-color: rgba(59, 130, 246, 0.4);
        transform: translateY(-2px);
    }
    .cap-icon {
        font-size: 1.25rem;
        margin-bottom: 6px;
    }
    .cap-name {
        font-size: 0.9rem;
        font-weight: 600;
        color: #F1F5F9;
        margin-bottom: 2px;
    }
    .cap-sub {
        font-size: 0.77rem;
        color: #94A3B8;
    }

    /* Query Container */
    .saas-card {
        background: #111827;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 22px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    .card-header-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 3px;
    }
    .card-header-sub {
        font-size: 0.85rem;
        color: #94A3B8;
        margin-bottom: 14px;
    }

    /* KPI Summary Cards */
    .kpi-row {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 14px;
        margin-bottom: 24px;
    }
    @media (max-width: 800px) {
        .kpi-row { grid-template-columns: repeat(2, 1fr); }
    }
    .kpi-card {
        background: linear-gradient(180deg, #151D2E 0%, #101625 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 16px;
    }
    .kpi-label {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #94A3B8;
        margin-bottom: 6px;
        font-weight: 600;
    }
    .kpi-value {
        font-size: 1.25rem;
        font-weight: 700;
        color: #F8FAFC;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    /* Status Badges */
    .badge-auto {
        background: rgba(16, 185, 129, 0.16);
        color: #10B981;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.88rem;
        font-weight: 700;
        border: 1px solid rgba(16, 185, 129, 0.3);
        display: inline-block;
    }
    .badge-esc {
        background: rgba(239, 68, 68, 0.16);
        color: #EF4444;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.88rem;
        font-weight: 700;
        border: 1px solid rgba(239, 68, 68, 0.3);
        display: inline-block;
    }
    .badge-intent {
        background: rgba(59, 130, 246, 0.16);
        color: #60A5FA;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.88rem;
        font-weight: 600;
        border: 1px solid rgba(59, 130, 246, 0.3);
        display: inline-block;
    }

    /* AI Draft Reply Highlight Card */
    .reply-card {
        background: linear-gradient(180deg, #162035 0%, #111827 100%);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 22px;
        box-shadow: 0 4px 20px rgba(37, 99, 235, 0.1);
    }
    .reply-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }
    .reply-badge {
        font-size: 0.75rem;
        font-weight: 600;
        color: #38BDF8;
        background: rgba(56, 189, 248, 0.12);
        padding: 3px 8px;
        border-radius: 4px;
        border: 1px solid rgba(56, 189, 248, 0.25);
    }
    .reply-text {
        font-size: 1rem;
        line-height: 1.6;
        color: #F1F5F9;
        background: rgba(15, 23, 42, 0.6);
        padding: 14px 16px;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* Routing Decision Card */
    .decision-card-auto {
        background: rgba(16, 185, 129, 0.08);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 22px;
    }
    .decision-card-esc {
        background: rgba(239, 68, 68, 0.08);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 22px;
    }

    /* Historical Evidence Cards */
    .evidence-item {
        background: #151D2E;
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 8px;
        padding: 14px 16px;
        margin-bottom: 12px;
    }
    .evidence-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
        font-size: 0.8rem;
        color: #94A3B8;
    }
    .sim-pill {
        background: rgba(56, 189, 248, 0.15);
        color: #38BDF8;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.75rem;
    }

    /* Empty State Container */
    .empty-state-box {
        background: rgba(17, 24, 39, 0.5);
        border: 1px dashed rgba(255, 255, 255, 0.12);
        border-radius: 12px;
        padding: 42px 24px;
        text-align: center;
        margin: 16px 0 24px 0;
    }
    .empty-icon {
        font-size: 2.2rem;
        margin-bottom: 10px;
        opacity: 0.7;
    }
    .empty-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #E2E8F0;
        margin-bottom: 4px;
    }
    .empty-sub {
        font-size: 0.85rem;
        color: #94A3B8;
        max-width: 520px;
        margin: 0 auto;
    }

    /* System Status Card in Sidebar */
    .sys-status-card {
        background: #141A29;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 14px;
        margin-top: 12px;
    }
    .sys-status-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 5px 0;
        font-size: 0.82rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    .sys-status-row:last-child {
        border-bottom: none;
    }
    .sys-label {
        color: #94A3B8;
    }
    .sys-val-ok {
        color: #10B981;
        font-weight: 600;
    }
    .sys-val-warn {
        color: #F59E0B;
        font-weight: 600;
    }
    .sys-val-err {
        color: #EF4444;
        font-weight: 600;
    }

    /* Footer */
    .saas-footer {
        text-align: center;
        padding: 28px 0 16px 0;
        margin-top: 40px;
        border-top: 1px solid rgba(255, 255, 255, 0.07);
        color: #64748B;
        font-size: 0.82rem;
    }
    .saas-footer a {
        color: #94A3B8;
        text-decoration: none;
    }

    /* Primary Streamlit Button Glow */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(59, 130, 246, 0.5) !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.96rem !important;
        padding: 0.6rem 1.4rem !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35) !important;
        transition: all 0.2s !important;
    }
    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5) !important;
    }
    div.stButton > button[kind="secondary"] {
        background-color: #1A2234 !important;
        color: #E2E8F0 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 6px !important;
        font-size: 0.82rem !important;
        transition: all 0.15s !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        border-color: rgba(59, 130, 246, 0.4) !important;
        background-color: #202A40 !important;
    }
</style>
""", unsafe_allow_html=True)


# --- TOP NAVBAR ---
st.markdown("""
<div class="saas-navbar">
    <div class="navbar-left">
        <div class="saas-logo-badge">⚡</div>
        <div>
            <div class="navbar-brand-title">SupportIQ</div>
            <div class="navbar-brand-sub">AI Customer Support Agent</div>
        </div>
        <div class="navbar-tagline">Real Conversations. Smarter Support. Powered by AI.</div>
    </div>
    <div class="navbar-center">
        <span class="nav-link active">Chat</span>
        <span class="nav-link">Analytics</span>
        <span class="nav-link">Evaluation</span>
        <span class="nav-link">About</span>
    </div>
    <div class="navbar-right">
        <div class="user-avatar-circle" title="SupportIQ Agent Core">AI</div>
    </div>
</div>
""", unsafe_allow_html=True)


# --- SIDEBAR ---
st.sidebar.markdown("### Brand Selection")

default_brand_idx = TOP_30_BRANDS.index("@AppleSupport") if "@AppleSupport" in TOP_30_BRANDS else 0
selected_brand = st.sidebar.selectbox(
    "Select Brand",
    options=TOP_30_BRANDS,
    index=default_brand_idx,
    help="Select an enterprise brand from the Twitter Customer Support (TWCS) dataset."
)

# Brand Status Badge
if selected_brand in SUPPORTED_BRANDS:
    st.sidebar.success(f"🟢 AI Ready ({selected_brand})")
else:
    st.sidebar.warning(f"🟡 Dataset Available / AI Resources Not Built")

st.sidebar.markdown("---")

# Navigation Menu
st.sidebar.markdown("### Navigation")
st.sidebar.radio(
    "Modules",
    options=["Chat & RAG Agent", "Analytics Dashboard", "Golden Set Evaluation", "Brand Insights", "Settings"],
    index=0,
    label_visibility="collapsed"
)

st.sidebar.markdown("---")

# Resource & Environment Checking
api_key = os.getenv("OPENAI_API_KEY")
api_key_configured = bool(api_key and api_key.strip() and not api_key.startswith("your_openai_"))

if selected_brand == "@AppleSupport":
    idx_path = EMBEDDINGS_DIR / "index.faiss"
    meta_path = EMBEDDINGS_DIR / "metadata.pkl"
    faiss_ready = idx_path.exists() and meta_path.exists()
elif selected_brand == "@AmazonHelp":
    idx_path = EMBEDDINGS_DIR / "amazonhelp" / "index.faiss"
    meta_path = EMBEDDINGS_DIR / "amazonhelp" / "metadata.pkl"
    faiss_ready = idx_path.exists() and meta_path.exists()
else:
    faiss_ready = False

# System Status Card
st.sidebar.markdown("### System Status")
api_status_html = '<span class="sys-val-ok">Configured</span>' if api_key_configured else '<span class="sys-val-err">Missing</span>'
faiss_status_html = '<span class="sys-val-ok">Ready</span>' if faiss_ready else '<span class="sys-val-warn">Not Built</span>'
brand_status_html = f'<span class="sys-val-ok">{selected_brand}</span>' if selected_brand in SUPPORTED_BRANDS else f'<span class="sys-val-warn">Pending</span>'

st.sidebar.markdown(f"""
<div class="sys-status-card">
    <div class="sys-status-row">
        <span class="sys-label">OpenAI API</span>
        {api_status_html}
    </div>
    <div class="sys-status-row">
        <span class="sys-label">FAISS Index</span>
        {faiss_status_html}
    </div>
    <div class="sys-status-row">
        <span class="sys-label">Selected Brand</span>
        {brand_status_html}
    </div>
    <div class="sys-status-row">
        <span class="sys-label">App Version</span>
        <span style="color: #94A3B8; font-weight: 500;">v1.2.0</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.caption(f"Config: Top-K={TOP_K} | MinSim={MIN_RETRIEVAL_SIMILARITY} | MinConf={MIN_CLASSIFIER_CONFIDENCE}")


# --- MAIN HERO SECTION ---
st.markdown(f"""
<div class="hero-container">
    <div class="hero-title">SupportIQ — AI Customer Support Agent</div>
    <div class="hero-desc">Ask a customer support question and get an AI-powered response based on real historical conversations.</div>
    <div class="cap-grid">
        <div class="cap-card">
            <div class="cap-icon">📁</div>
            <div class="cap-name">Real Support Data</div>
            <div class="cap-sub">From Twitter (TWCS)</div>
        </div>
        <div class="cap-card">
            <div class="cap-icon">🎯</div>
            <div class="cap-name">Intent Classification</div>
            <div class="cap-sub">Data-driven intents</div>
        </div>
        <div class="cap-card">
            <div class="cap-icon">🔍</div>
            <div class="cap-name">Semantic Search</div>
            <div class="cap-sub">FAISS Vector Retrieval</div>
        </div>
        <div class="cap-card">
            <div class="cap-icon">🛡️</div>
            <div class="cap-name">Grounded Responses</div>
            <div class="cap-sub">Based on real cases</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# Pre-flight Notifications for Unsupported Brands or Missing Keys
if selected_brand not in SUPPORTED_BRANDS:
    st.warning(
        f"ℹ️ **Dataset Available / AI Resources Not Built for {selected_brand}**\n\n"
        f"SupportIQ has fully configured indexes and intent taxonomies for `@AppleSupport` and `@AmazonHelp`. "
        f"To query `{selected_brand}`, run the dedicated dataset extraction and FAISS index pipeline. "
        f"SupportIQ will never return cross-brand or fabricated data."
    )
elif not api_key_configured:
    st.error("⚠️ **OpenAI API Key Missing:** Please set `OPENAI_API_KEY` in `.env` to enable LLM classification and generation.")
elif not faiss_ready:
    st.warning(f"⚠️ **Retrieval Index In Progress or Missing:** Pre-computed FAISS index not found at `{idx_path}`. The embedding pipeline must finish before retrieval is active.")


# --- CUSTOMER QUERY CARD ---
if "customer_query" not in st.session_state:
    st.session_state["customer_query"] = ""

st.markdown("""
<div class="card-header-title">Customer Query</div>
<div class="card-header-sub">Enter a customer support question, or try an example below.</div>
""", unsafe_allow_html=True)

# Example Buttons Grid
st.caption("Quick Example Queries:")
ex_col1, ex_col2, ex_col3, ex_col4 = st.columns(4)

if selected_brand == "@AppleSupport":
    with ex_col1:
        if st.button("🔋 Battery Drain", use_container_width=True, help="Apple battery drain inquiry"):
            st.session_state["customer_query"] = "My iPhone battery drains very quickly after the latest update."
            st.rerun()
    with ex_col2:
        if st.button("🎧 Return AirPods", use_container_width=True, help="Apple return inquiry"):
            st.session_state["customer_query"] = "How do I return my AirPods at an Apple Store if I bought them online 10 days ago?"
            st.rerun()
    with ex_col3:
        if st.button("🔄 iOS Update Issue", use_container_width=True, help="Apple iOS update problem"):
            st.session_state["customer_query"] = "I'm having issues after an iOS update. My screen froze and won't respond."
            st.rerun()
    with ex_col4:
        if st.button("🔐 Apple ID Sign In", use_container_width=True, help="Apple account access issue"):
            st.session_state["customer_query"] = "I can't sign in to my Apple ID. It says my account has been locked."
            st.rerun()
elif selected_brand == "@AmazonHelp":
    with ex_col1:
        if st.button("📦 Package Delayed", use_container_width=True, help="Amazon delivery tracking"):
            st.session_state["customer_query"] = "My package was marked as delivered yesterday, but it is nowhere to be found."
            st.rerun()
    with ex_col2:
        if st.button("⚠️ Damaged Item", use_container_width=True, help="Amazon damaged/defective product"):
            st.session_state["customer_query"] = "I received a damaged package with missing items. Need a replacement."
            st.rerun()
    with ex_col3:
        if st.button("⭐ Cancel Prime", use_container_width=True, help="Amazon Prime subscription"):
            st.session_state["customer_query"] = "How do I cancel my Amazon Prime membership and get a refund for remaining time?"
            st.rerun()
    with ex_col4:
        if st.button("💳 Payment Charged", use_container_width=True, help="Amazon billing and payments"):
            st.session_state["customer_query"] = "Why was my credit card charged twice for order #408-3265294?"
            st.rerun()
else:
    with ex_col1:
        if st.button("📦 General Order Query", use_container_width=True):
            st.session_state["customer_query"] = f"Hello {selected_brand}, I need an update on my recent order."
            st.rerun()
    with ex_col2:
        if st.button("🔐 Account Issue", use_container_width=True):
            st.session_state["customer_query"] = f"Hello {selected_brand}, I am locked out of my account."
            st.rerun()
    with ex_col3:
        if st.button("💳 Billing Dispute", use_container_width=True):
            st.session_state["customer_query"] = f"Can someone from {selected_brand} please check my refund status?"
            st.rerun()
    with ex_col4:
        if st.button("💬 Contact Support", use_container_width=True):
            st.session_state["customer_query"] = f"How can I talk to a human support agent at {selected_brand}?"
            st.rerun()

# Large Text Area with live character count
user_input = st.text_area(
    "Customer Support Query",
    value=st.session_state["customer_query"],
    placeholder="Type your customer support message here...",
    height=120,
    key="customer_query_input",
    label_visibility="collapsed"
)

# Sync manual typing to session state
if user_input != st.session_state["customer_query"]:
    st.session_state["customer_query"] = user_input

# Character Count Display
char_count = len(user_input)
st.markdown(
    f"<div style='text-align: right; color: #64748B; font-size: 0.78rem; margin-top: -6px; margin-bottom: 12px;'>"
    f"Character count: <strong>{char_count}</strong> characters"
    f"</div>",
    unsafe_allow_html=True
)

# Primary CTA Button
analyze_button = st.button("✨ Analyze & Draft Reply →", type="primary", use_container_width=True)


# --- Cached Agent Loader ---
@st.cache_resource(show_spinner=False)
def load_support_agent(brand_name: str):
    from src.pipeline.agent import SupportAgent
    return SupportAgent(brand=brand_name)


# --- Pipeline Execution & Results Section ---
if analyze_button:
    query_text = user_input.strip()
    if not query_text:
        st.warning("Please type a customer message or select an example query above.")
    elif selected_brand not in SUPPORTED_BRANDS:
        st.error(
            f"Cannot run pipeline: {selected_brand} is available in TWCS dataset, but its AI resources have not been built yet. "
            f"SupportIQ will not generate fake or cross-brand responses."
        )
    elif not api_key_configured:
        st.error("Cannot proceed: A valid `OPENAI_API_KEY` is required in `.env`.")
    elif not faiss_ready:
        st.error(f"Cannot proceed: Pre-computed FAISS index is not ready at `{idx_path}`. Please wait for index build to finish.")
    else:
        with st.spinner(f"Analyzing message with SupportIQ pipeline for {selected_brand} (Classification → RAG Retrieval → Reply Generation → Escalation Policy)..."):
            try:
                agent = load_support_agent(selected_brand)
                response = agent.handle(query_text)
            except Exception as e:
                st.error(f"Runtime error during pipeline execution: {e}")
                response = None

        if response is not None:
            st.markdown("---")
            st.markdown("### Analysis & Response Dashboard")

            # 4 Summary KPI Cards
            conf_str = f"{response.confidence:.1%}" if isinstance(response.confidence, (int, float)) else str(response.confidence)
            retrieval_quality = f"{len(response.retrieved_examples)} turns"
            if response.retrieved_examples:
                avg_sim = sum(ex.get("similarity", 0.0) for ex in response.retrieved_examples) / len(response.retrieved_examples)
                retrieval_quality = f"High ({avg_sim:.2f} avg)"

            decision_badge = '<span class="badge-auto">🟢 AUTO_HANDLE</span>' if response.decision == "AUTO_HANDLE" else '<span class="badge-esc">🔴 ESCALATE</span>'

            st.markdown(f"""
            <div class="kpi-row">
                <div class="kpi-card">
                    <div class="kpi-label">Intent</div>
                    <div class="kpi-value"><span class="badge-intent">{response.intent}</span></div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Confidence</div>
                    <div class="kpi-value">{conf_str}</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Decision</div>
                    <div class="kpi-value">{decision_badge}</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Retrieval Quality</div>
                    <div class="kpi-value">{retrieval_quality}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # --- D. Routing Decision Status Card ---
            if response.decision == "AUTO_HANDLE":
                st.markdown(f"""
                <div class="decision-card-auto">
                    <div style="display: flex; align-items: center; gap: 8px; font-weight: 700; color: #10B981; font-size: 1.05rem;">
                        🟢 Status: AUTO_HANDLE — Ready for Automated Dispatch
                    </div>
                    <div style="color: #CBD5E1; font-size: 0.88rem; margin-top: 6px;">
                        <strong>Escalation Policy Assessment:</strong> {response.reason}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="decision-card-esc">
                    <div style="display: flex; align-items: center; gap: 8px; font-weight: 700; color: #EF4444; font-size: 1.05rem;">
                        🔴 Status: ESCALATE — Routed to Human Support Specialist
                    </div>
                    <div style="color: #CBD5E1; font-size: 0.88rem; margin-top: 6px;">
                        <strong>Escalation Policy Assessment:</strong> {response.reason}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # --- C. AI Draft Reply Card ---
            st.markdown(f"""
            <div class="reply-card">
                <div class="reply-header">
                    <div style="font-weight: 700; font-size: 1.05rem; color: #FFFFFF;">AI Draft Reply</div>
                    <div class="reply-badge">⚡ Grounded in historical support conversations</div>
                </div>
                <div class="reply-text">{response.reply}</div>
            </div>
            """, unsafe_allow_html=True)

            # --- A. Intent Classification Details ---
            with st.expander("🎯 Section A: Intent Classification Details", expanded=True):
                col_i1, col_i2 = st.columns([1, 2])
                with col_i1:
                    st.markdown(f"**Predicted Intent:** `{response.intent}`")
                    st.markdown(f"**Confidence Score:** `{conf_str}`")
                with col_i2:
                    st.markdown(f"**Classification Context:**")
                    st.caption(f"Intent classified by SupportIQ using the data-driven taxonomy for {selected_brand}.")

            # --- B. Historical Similar Conversations (FAISS) ---
            with st.expander(f"🔍 Section B: Historical Similar Conversations ({len(response.retrieved_examples)} retrieved via FAISS)", expanded=True):
                if not response.retrieved_examples:
                    st.info("No historical conversations exceeded the minimum similarity threshold.")
                else:
                    for idx, ex in enumerate(response.retrieved_examples, 1):
                        sim = ex.get("similarity", 0.0)
                        t_id = ex.get("tweet_id", "N/A")
                        cust_text = ex.get("customer_message", "")
                        brand_text = ex.get("brand_response", "")
                        
                        st.markdown(f"""
                        <div class="evidence-item">
                            <div class="evidence-header">
                                <span>Evidence Turn #{idx} (Tweet ID: <code>{t_id}</code>)</span>
                                <span class="sim-pill">Cosine Similarity: {sim:.4f}</span>
                            </div>
                            <div style="font-size: 0.88rem; margin-bottom: 6px; color: #CBD5E1;">
                                <strong style="color: #94A3B8;">Customer:</strong> {cust_text}
                            </div>
                            <div style="font-size: 0.88rem; color: #93C5FD; border-left: 2px solid #3B82F6; padding-left: 8px; margin-top: 4px;">
                                <strong style="color: #60A5FA;">Brand Response:</strong> {brand_text}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

else:
    # --- EMPTY STATE ---
    st.markdown("""
    <div class="empty-state-box">
        <div class="empty-icon">💬</div>
        <div class="empty-title">Ready to analyze</div>
        <div class="empty-sub">Submit a customer query to see intent classification, historical matches, AI response, and routing decision.</div>
    </div>
    """, unsafe_allow_html=True)


# --- FOOTER ---
st.markdown("""
<div class="saas-footer">
    <strong>SupportIQ • AI Customer Support Agent</strong><br>
    Built for the Hiver SDE Intern Take-Home Assignment • Powered by FAISS, SentenceTransformers & OpenAI
</div>
""", unsafe_allow_html=True)
