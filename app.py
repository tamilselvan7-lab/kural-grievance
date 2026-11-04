import streamlit as st
import pandas as pd

from core.ai_pipeline import analyze_complaint
from core.database import (
    initialize_database,
    add_complaint,
    get_all_complaints,
    get_complaint_by_id,
    update_complaint_status,
)

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Kural Grievance | AI Citizen Portal",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

initialize_database()

# =====================================================
# GLOBAL STYLE — NEON HORIZON LANDING PAGE
# =====================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    :root {
        --bg: #030907;
        --panel: #0b1512;
        --panel-2: #101d19;
        --teal: #32f5c2;
        --mint: #9bffd9;
        --text: #f2fff9;
        --muted: #9aafa7;
        --line: rgba(151, 255, 215, .14);
    }

    html, body, [data-testid="stAppViewContainer"] {
        background: var(--bg) !important;
        color: var(--text) !important;
        font-family: 'DM Sans', sans-serif;
    }

    [data-testid="stAppViewContainer"] {
        position: relative;
        background:
            radial-gradient(ellipse at 50% 0%, rgba(24, 105, 66, .16), transparent 48%),
            linear-gradient(rgba(85, 170, 125, .045) 1px, transparent 1px),
            linear-gradient(90deg, rgba(85, 170, 125, .045) 1px, transparent 1px),
            #030907 !important;
        background-size: auto, 34px 34px, 34px 34px, auto !important;
    }

    /* Fixed emerald dome: attached to the page background, not the hero card. */
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: fixed;
        z-index: 0;
        pointer-events: none;
        width: 122vw;
        height: 112vh;
        left: -11vw;
        bottom: -83vh;
        border-radius: 50% 50% 0 0 / 100% 100% 0 0;
        background: radial-gradient(ellipse at 50% 0%, rgba(9, 45, 28, .24), #020805 62%);
        border-top: 2px solid rgba(220, 255, 235, .94);
        box-shadow:
            0 -8px 22px rgba(175, 255, 205, .22),
            0 -20px 55px rgba(40, 235, 130, .36),
            0 -48px 115px rgba(20, 190, 100, .30),
            0 -80px 170px rgba(10, 130, 70, .20);
    }
    [data-testid="stAppViewContainer"]::after {
        content: "";
        position: fixed;
        z-index: 0;
        pointer-events: none;
        width: 122vw;
        height: 110vh;
        left: -11vw;
        bottom: -85vh;
        border-radius: 50% 50% 0 0 / 100% 100% 0 0;
        border-top: 2px solid transparent;
        background:
            linear-gradient(#020805, #020805) padding-box,
            linear-gradient(90deg,
                rgba(40, 190, 105, 0) 0%,
                rgba(70, 245, 145, .95) 18%,
                rgba(125, 255, 185, .98) 50%,
                rgba(70, 245, 145, .95) 82%,
                rgba(40, 190, 105, 0) 100%) border-box;
        filter: drop-shadow(0 -8px 24px rgba(60, 245, 140, .38));
    }

    [data-testid="stMain"] {
        position: relative;
        z-index: 1;
        background: transparent !important;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    [data-testid="stToolbar"] { right: 1rem; }

    .block-container {
        max-width: 1320px;
        padding-top: 1.2rem;
        padding-bottom: 2.5rem;
    }

    #MainMenu, footer { visibility: hidden; }

    /* Top navigation */
    .topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 8px 4px 15px;
        border-bottom: 1px solid rgba(165, 255, 215, .12);
        margin-bottom: 22px;
    }
    .brand {
        color: #f3fff9;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 21px;
        letter-spacing: -1px;
    }
    .brand span { color: var(--teal); }
    .brand-sub {
        color: #78968a;
        font-size: 9px;
        letter-spacing: 2px;
        margin-top: 2px;
    }
    .top-note {
        color: #a5bdb1;
        font-size: 11px;
        letter-spacing: 1.3px;
        text-transform: uppercase;
    }

    /* Hero content sits directly over the fixed page background. */
    .hero-stage {
        position: relative;
        z-index: 1;
        min-height: 590px;
        overflow: visible;
        isolation: auto;
        border: 1px solid rgba(109, 255, 194, .08);
        border-radius: 20px;
        background: linear-gradient(180deg, rgba(1, 7, 5, .62), rgba(1, 7, 5, .18));
        padding: 38px 24px 26px;
        text-align: center;
    }

    .hero-kicker {
        display: inline-block;
        color: #8dffcf;
        background: rgba(34, 255, 179, .075);
        border: 1px solid rgba(93, 255, 194, .24);
        border-radius: 30px;
        padding: 7px 13px;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1.8px;
        margin: 4px 0 17px;
    }
    .hero-title {
        color: #f5fff9;
        font-family: 'Space Grotesk', sans-serif;
        font-size: clamp(34px, 5vw, 58px);
        line-height: 1.08;
        letter-spacing: -2.8px;
        font-weight: 700;
        margin: 0 auto 13px;
        max-width: 820px;
        text-shadow: 0 0 30px rgba(160, 255, 218, .10);
    }
    .hero-description {
        color: #a8beb2;
        font-size: 14px;
        line-height: 1.8;
        max-width: 650px;
        margin: 0 auto 14px;
    }
    .language-line {
        color: #53f5bd;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 2px;
        margin-top: 15px;
    }

    /* Floating glass dashboard preview */
    .preview-wrap {
        position: relative;
        z-index: 2;
        width: min(850px, 92%);
        margin: 27px auto 0;
        text-align: left;
        border: 1px solid rgba(170, 255, 220, .25);
        border-radius: 13px 13px 0 0;
        background: linear-gradient(145deg, rgba(12, 23, 20, .94), rgba(3, 11, 8, .88));
        box-shadow:
            0 0 24px rgba(65, 225, 135, .12),
            0 0 58px rgba(35, 190, 105, .16),
            0 18px 55px rgba(0, 0, 0, .55);
        backdrop-filter: blur(18px);
        padding: 15px 17px 18px;
    }
    .preview-top {
        display: flex;
        justify-content: space-between;
        color: #c8ded3;
        font-size: 10px;
        padding-bottom: 12px;
        border-bottom: 1px solid rgba(160, 255, 213, .12);
        letter-spacing: .5px;
    }
    .preview-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 11px;
        margin-top: 13px;
    }
    .preview-stat {
        background: rgba(255,255,255,.035);
        border: 1px solid rgba(155,255,213,.12);
        border-radius: 8px;
        padding: 12px;
    }
    .preview-label {
        color: #8ca69a;
        font-size: 9px;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    .preview-value {
        color: #edfff5;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 24px;
        font-weight: 700;
        margin-top: 5px;
    }
    .preview-foot {
        color: #5af0bd;
        font-size: 9px;
        margin-top: 2px;
    }
    .preview-bottom {
        display: flex;
        justify-content: space-between;
        gap: 10px;
        margin-top: 11px;
        color: #9db4a8;
        font-size: 10px;
    }

    .section-heading {
        color: #effff7;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 23px;
        font-weight: 700;
        margin: 28px 0 4px;
    }
    .section-sub {
        color: var(--muted);
        font-size: 13px;
        margin-bottom: 16px;
    }
    .metric-card, .feature-card, .panel {
        background: linear-gradient(145deg, #102019, #09130f);
        border: 1px solid rgba(142, 255, 205, .15);
        border-radius: 13px;
        padding: 17px;
    }
    .metric-label {
        color: #91aa9d;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1.2px;
    }
    .metric-value {
        color: #f2fff8;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 29px;
        font-weight: 700;
        margin-top: 7px;
    }
    .metric-accent { color: #48edb6; font-size: 11px; margin-top: 2px; }
    .feature-card { min-height: 142px; }
    .feature-icon { font-size: 23px; margin-bottom: 8px; }
    .feature-card h3 { color: #effff7; font-size: 15px; margin: 0 0 7px; }
    .feature-card p { color: #9bb1a5; font-size: 12px; line-height: 1.6; margin: 0; }

    .stButton > button, .stFormSubmitButton > button {
        background: linear-gradient(100deg, #35eeb4, #a1ffd2) !important;
        color: #03110b !important;
        border: 0 !important;
        border-radius: 9px !important;
        font-weight: 700 !important;
        min-height: 42px;
        box-shadow: 0 0 18px rgba(57, 255, 184, .16);
    }
    .stButton > button:hover, .stFormSubmitButton > button:hover {
        box-shadow: 0 0 25px rgba(57, 255, 184, .38);
        transform: translateY(-1px);
    }
    .stTextInput input, .stTextArea textarea,
    .stSelectbox div[data-baseweb="select"],
    .stNumberInput input {
        background: #0c1913 !important;
        color: #effff7 !important;
        border-color: rgba(142,255,205,.22) !important;
        border-radius: 9px !important;
    }

    /* Submit Complaint: keep the form visually above the fixed dome. */
    [data-testid="stVerticalBlockBorderWrapper"]:has(form) {
        position: relative;
        z-index: 3;
        background: linear-gradient(145deg, rgba(8, 20, 15, .97), rgba(3, 12, 8, .96)) !important;
        border: 1px solid rgba(115, 255, 190, .22) !important;
        border-radius: 18px !important;
        box-shadow:
            0 14px 42px rgba(0, 0, 0, .30),
            0 0 28px rgba(42, 220, 135, .08) !important;
        backdrop-filter: blur(18px);
    }

    [data-testid="stVerticalBlockBorderWrapper"]:has(form) [data-testid="stForm"] {
        border: 1px solid rgba(142, 255, 205, .13);
        border-radius: 13px;
        padding: 18px;
        background: rgba(2, 9, 6, .42);
    }

    .stTextArea textarea {
        min-height: 165px !important;
        line-height: 1.65 !important;
        padding: 15px 16px !important;
        transition: border-color .2s ease, box-shadow .2s ease;
    }

    .stTextArea textarea:focus {
        border-color: rgba(65, 245, 180, .75) !important;
        box-shadow: 0 0 0 1px rgba(65, 245, 180, .22),
                    0 0 18px rgba(45, 225, 155, .10) !important;
    }

    .stTextArea textarea::placeholder {
        color: #8fa69a !important;
        opacity: 1;
    }

    .stFormSubmitButton > button {
        min-height: 52px !important;
        font-size: 15px !important;
        letter-spacing: .15px;
        transition: transform .2s ease, box-shadow .2s ease;
    }

    .form-intro {
        color: #9db7aa;
        font-size: 12px;
        line-height: 1.7;
        margin: -3px 0 15px;
    }

    .form-language-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin: 4px 0 14px;
    }

    .form-language-tags span {
        color: #8dffce;
        background: rgba(43, 230, 158, .075);
        border: 1px solid rgba(89, 245, 180, .19);
        border-radius: 30px;
        padding: 5px 10px;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: .5px;
    }

    @media (max-width: 700px) {
        [data-testid="stVerticalBlockBorderWrapper"]:has(form) [data-testid="stForm"] {
            padding: 12px;
        }
        .stTextArea textarea {
            min-height: 145px !important;
        }
    }
    [data-testid="stMetric"] {
        background: #0c1913;
        border: 1px solid rgba(142,255,205,.15);
        border-radius: 12px;
        padding: 13px;
    }
    [data-testid="stMetricLabel"] { color: #9bb1a5; }
    [data-testid="stMetricValue"] { color: #55f1bd; }
    [data-testid="stDataFrame"] { border: 1px solid rgba(142,255,205,.16); }
    label, .stMarkdown p { color: #d5e8dd; }
    div[data-testid="stAlert"] { border-radius: 10px; }
    hr { border-color: rgba(142,255,205,.15); }
    .footer {
        color: #708b7d;
        text-align: center;
        font-size: 10px;
        padding-top: 22px;
        margin-top: 30px;
        border-top: 1px solid rgba(142,255,205,.12);
        letter-spacing: .7px;
    }

    @media (max-width: 700px) {
        .hero-stage { min-height: 570px; padding: 25px 12px 22px; }
        .hero-title { letter-spacing: -1.5px; }
        .preview-wrap { width: 100%; padding: 11px; }
        .preview-grid { gap: 6px; }
        .preview-stat { padding: 8px; }
        .preview-value { font-size: 19px; }
        .preview-bottom { flex-direction: column; }
        .top-note { display: none; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# HELPER FUNCTIONS
# =====================================================

def show_heading(label, title, description):
    st.markdown(
        f"""
        <div style="color:#51efb9;font-size:10px;font-weight:700;
                    letter-spacing:1.8px;margin-bottom:8px">{label}</div>
        <div class="section-heading" style="margin-top:0">{title}</div>
        <div class="section-sub">{description}</div>
        """,
        unsafe_allow_html=True,
    )


def show_metric(label, value, caption):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-accent">{caption}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def get_complaint_statistics(complaints):
    total = len(complaints)
    pending = sum(
        1 for complaint in complaints
        if complaint["status"] in ["Submitted", "Under Review", "In Progress"]
    )
    resolved = sum(
        1 for complaint in complaints
        if complaint["status"] == "Resolved"
    )
    return total, pending, resolved


# =====================================================
# DATA AND NAVIGATION
# =====================================================

complaints = get_all_complaints()
total, pending, resolved = get_complaint_statistics(complaints)

st.markdown(
    """
    <div class="topbar">
        <div>
            <div class="brand">KURAL<span>.</span></div>
            <div class="brand-sub">AI GRIEVANCE INTELLIGENCE</div>
        </div>
        <div class="top-note">A clearer voice for every citizen&nbsp; ✦</div>
    </div>
    """,
    unsafe_allow_html=True,
)

page = st.radio(
    "Main navigation",
    ["Home", "Submit Complaint", "Track Complaint", "Officer Dashboard"],
    horizontal=True,
    label_visibility="collapsed",
)


# =====================================================
# HOME PAGE
# =====================================================

if page == "Home":
    st.markdown(
        f"""
        <section class="hero-stage">
            <div class="hero-kicker">✦ NEXT-GENERATION CIVIC TECHNOLOGY</div>
            <h1 class="hero-title">Every Voice Deserves<br>a Path to Action.</h1>
            <p class="hero-description">
                A multilingual AI grievance platform that helps citizens report
                civic issues in their own language. Kural translates, classifies
                and prioritizes complaints to support faster human review.
            </p>
            <div class="language-line">TAMIL &nbsp; • &nbsp; HINDI &nbsp; • &nbsp; ENGLISH</div>
            <div class="preview-wrap">
                <div class="preview-top">
                    <span>✦ KURAL INTELLIGENCE / LIVE OVERVIEW</span>
                    <span>● SYSTEM READY</span>
                </div>
                <div class="preview-grid">
                    <div class="preview-stat">
                        <div class="preview-label">Total complaints</div>
                        <div class="preview-value">{total}</div>
                        <div class="preview-foot">Recorded in database</div>
                    </div>
                    <div class="preview-stat">
                        <div class="preview-label">Pending / active</div>
                        <div class="preview-value">{pending}</div>
                        <div class="preview-foot">Awaiting completion</div>
                    </div>
                    <div class="preview-stat">
                        <div class="preview-label">Resolved</div>
                        <div class="preview-value">{resolved}</div>
                        <div class="preview-foot">Marked as resolved</div>
                    </div>
                </div>
                <div class="preview-bottom">
                    <span>🌐 Multilingual understanding</span>
                    <span>◈ AI-assisted classification</span>
                    <span>⚡ Priority assistance</span>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-heading">Intelligence for every citizen</div>'
        '<div class="section-sub">One simple platform. Three useful AI capabilities.</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    features = [
        ("🌐", "Multilingual AI", "Understand complaints written in Tamil, Hindi and English."),
        ("🧠", "Smart classification", "Organize each complaint into the appropriate service department."),
        ("⚡", "Priority assistance", "Generate an AI-assisted urgency score with an explanation."),
    ]
    for column, feature in zip((c1, c2, c3), features):
        with column:
            st.markdown(
                f"""
                <div class="feature-card">
                    <div class="feature-icon">{feature[0]}</div>
                    <h3>{feature[1]}</h3>
                    <p>{feature[2]}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div class="section-heading">How Kural works</div>'
        '<div class="section-sub">From a citizen’s message to a trackable grievance.</div>',
        unsafe_allow_html=True,
    )
    steps = [
        ("01", "Submit", "Write in your language"),
        ("02", "Analyze", "AI understands the issue"),
        ("03", "Organize", "Save and assign an ID"),
        ("04", "Track", "Follow complaint status"),
    ]
    cols = st.columns(4)
    for column, step in zip(cols, steps):
        with column:
            st.markdown(
                f"""
                <div class="panel" style="text-align:center;min-height:112px">
                    <div style="font-size:23px;color:#48edb6;font-weight:700">{step[0]}</div>
                    <div style="font-weight:700;margin-top:6px">{step[1]}</div>
                    <div style="font-size:11px;color:#9bb1a5;margin-top:5px">{step[2]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.info(
        "AI classifications and priority scores are decision-support suggestions. "
        "They do not replace human review or official decisions."
    )


# =====================================================
# SUBMIT COMPLAINT
# =====================================================

elif page == "Submit Complaint":
    show_heading(
        "CITIZEN SERVICES / NEW REQUEST",
        "Submit a grievance",
        "Describe your issue in Tamil, Hindi or English.",
    )

    with st.container(border=True):
        st.markdown("### 📝 Complaint details")
        st.markdown(
            '<div class="form-intro">'
            'Share what happened, where it happened and how long the issue has continued. '
            'Kural will analyze your message and prepare it for review.'
            '</div>'
            '<div class="form-language-tags">'
            '<span>தமிழ் · TAMIL</span><span>हिन्दी · HINDI</span>'
            '<span>ENGLISH</span></div>',
            unsafe_allow_html=True,
        )
        with st.form("complaint_form"):
            complaint_text = st.text_area(
                "Describe your complaint",
                placeholder="Example: எங்கள் பகுதியில் கடந்த மூன்று நாட்களாக குடிநீர் வரவில்லை.",
                help="Write the complaint in your preferred language. Include the location and relevant details when possible.",
            )
            st.caption("Your complaint will be translated and categorized with AI assistance.")
            submitted = st.form_submit_button(
                "✦ Analyze and Submit Complaint",
                use_container_width=True,
            )

        if submitted:
            if not complaint_text.strip():
                st.warning("Please enter your complaint first.")
            elif len(complaint_text.strip()) < 8:
                st.warning("Please provide a little more detail about the issue.")
            else:
                with st.spinner("AI is understanding and analyzing your complaint..."):
                    try:
                        analysis = analyze_complaint(complaint_text)
                        complaint_id = add_complaint(complaint_text, analysis)
                        st.session_state["last_complaint_id"] = complaint_id
                        st.session_state["last_analysis"] = analysis
                    except Exception as error:
                        st.error("Complaint submission failed. Please try again later.")
                        st.caption(str(error))

        if "last_complaint_id" in st.session_state:
            analysis = st.session_state["last_analysis"]
            complaint_id = st.session_state["last_complaint_id"]
            st.success("Your complaint has been submitted successfully!")
            st.markdown(f"### Complaint ID: `KG-{complaint_id:04d}`")
            st.caption("Save this ID to check your complaint status later.")
            st.divider()
            st.markdown("### AI analysis")
            a1, a2, a3 = st.columns(3)
            a1.metric("Detected language", analysis["detected_language"])
            a2.metric("Department", analysis["department"])
            a3.metric("Priority score", f'{analysis["priority_score"]}/100')
            st.markdown("**English translation**")
            st.info(analysis["translated_complaint"])
            st.markdown("**Priority explanation**")
            st.write(analysis["priority_reason"])
            st.caption(
                "AI output should be reviewed by an authorized officer. "
                "Priority scores are not official decisions."
            )


# =====================================================
# TRACK COMPLAINT
# =====================================================

elif page == "Track Complaint":
    show_heading(
        "CITIZEN SERVICES / TRACKING",
        "Track your complaint",
        "Enter your complaint ID to view its current status.",
    )

    with st.container(border=True):
        complaint_id_input = st.number_input(
            "Complaint ID", min_value=1, step=1, value=1
        )
        search_clicked = st.button("🔍 Find Complaint", use_container_width=True)

        if search_clicked:
            result = get_complaint_by_id(int(complaint_id_input))
            if result:
                st.success(f"Complaint KG-{result['id']:04d} found.")
                st.markdown("### Complaint information")
                st.write("**Original complaint:**")
                st.write(result["complaint_text"])
                st.write("**English translation:**")
                st.info(result["translated_complaint"])
                c1, c2, c3 = st.columns(3)
                c1.metric("Department", result["department"])
                c2.metric("Priority", f"{result['priority_score']}/100")
                c3.metric("Status", result["status"])
                st.caption(f"Submitted: {result['submitted_at']}")
            else:
                st.warning("No complaint found with that ID.")


# =====================================================
# OFFICER DASHBOARD
# =====================================================

elif page == "Officer Dashboard":
    show_heading(
        "ADMINISTRATION / OPERATIONS",
        "Officer dashboard",
        "Review and manage recorded citizen grievances.",
    )

    complaints = get_all_complaints()
    total, pending, resolved = get_complaint_statistics(complaints)
    d1, d2, d3 = st.columns(3)
    with d1:
        show_metric("TOTAL", total, "All recorded complaints")
    with d2:
        show_metric("ACTIVE", pending, "Awaiting completion")
    with d3:
        show_metric("RESOLVED", resolved, "Completed complaints")

    if complaints:
        st.markdown('<div class="section-heading">Complaint records</div>', unsafe_allow_html=True)
        df = pd.DataFrame(complaints)
        selected_department = st.selectbox(
            "Filter by department",
            ["All"] + sorted(df["department"].unique().tolist()),
        )
        if selected_department != "All":
            df = df[df["department"] == selected_department]

        display_columns = [
            "id", "detected_language", "department",
            "priority_score", "status", "submitted_at",
        ]
        st.dataframe(df[display_columns], use_container_width=True, hide_index=True)

        st.markdown('<div class="section-heading">Department distribution</div>', unsafe_allow_html=True)
        department_counts = pd.DataFrame(complaints)["department"].value_counts()
        st.bar_chart(department_counts)

        st.markdown('<div class="section-heading">Update complaint status</div>', unsafe_allow_html=True)
        selected_id = st.selectbox("Select complaint ID", [c["id"] for c in complaints])
        statuses = ["Submitted", "Under Review", "In Progress", "Resolved", "Rejected"]
        selected_status = st.selectbox("New status", statuses)

        if st.button("Update status", use_container_width=True):
            success = update_complaint_status(selected_id, selected_status)
            if success:
                st.success("Complaint status updated.")
                st.rerun()
            else:
                st.error("Unable to update complaint status.")
    else:
        st.info(
            "No complaints have been submitted yet. "
            "Submit a test complaint to populate this dashboard."
        )


# =====================================================
# FOOTER
# =====================================================

st.markdown(
    """
    <div class="footer">
        KURAL GRIEVANCE &nbsp; • &nbsp; AI FOR INCLUSIVE CITIZEN SERVICES
        <br><br>
        Every voice matters. Every complaint deserves action.
    </div>
    """,
    unsafe_allow_html=True,
)
