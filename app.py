
import streamlit as st
from decision import get_decision, OPTIONS, GUIDANCE

st.set_page_config(
    page_title="ProofPath | Think. Verify. Stay Safe.",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- DESIGN ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Nunito:wght@500;600;700;800;900&display=swap');

:root {
    --ink: #202653;
    --muted: #69749b;
    --purple: #6255ed;
    --mint: #e9fbf4;
    --line: #e7e8fb;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
.stApp {
    background:
        radial-gradient(ellipse at 4% 5%, #f9edff 0, transparent 27%),
        radial-gradient(ellipse at 98% 15%, #e9f4ff 0, transparent 28%),
        #fafbff;
    color: var(--ink);
}
.block-container {
    max-width: 1450px;
    padding-top: 1.3rem;
    padding-bottom: 2rem;
}
h1, h2, h3 {
    font-family: 'Nunito', sans-serif !important;
    color: var(--ink) !important;
}
p, label, li {
    color: #46527e;
}
[data-testid="stHeader"] {
    background: transparent;
}
#MainMenu, footer {
    visibility: hidden;
}
.brand {
    display: flex;
    align-items: center;
    gap: 13px;
    padding: 4px 0 15px;
}
.brand-icon {
    width: 54px;
    height: 54px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 18px;
    font-size: 29px;
    background: linear-gradient(135deg, #e7e3ff, #dff8ff);
    border: 1px solid #dcdcff;
    box-shadow: 0 5px 16px #6255ed12;
}
.brand-name {
    font-family: 'Nunito', sans-serif;
    font-weight: 900;
    font-size: 28px;
    letter-spacing: -1px;
    color: #202653;
    line-height: 1.15;
}
.brand-name span {
    color: #6255ed;
}
.brand-tag {
    color: #7580a5;
    font-size: 12px;
    letter-spacing: .5px;
}
.hero {
    background: linear-gradient(115deg, #f0edff 0%, #edf8ff 53%, #fff0fa 100%);
    border: 1px solid #e3e4ff;
    border-radius: 25px;
    padding: 29px 32px;
    margin: 6px 0 24px;
    box-shadow: 0 10px 30px #3d4c7b09;
}
.eyebrow {
    color: #6557e9;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.6px;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.hero-title {
    font-family: 'Nunito', sans-serif;
    font-size: clamp(27px, 3vw, 42px);
    font-weight: 900;
    line-height: 1.12;
    letter-spacing: -1.1px;
    color: #202653;
}
.hero-title span {
    color: #6557e9;
}
.hero-copy {
    font-size: 14px;
    line-height: 1.8;
    max-width: 680px;
    color: #536087;
    margin-top: 12px;
}
.hero-art {
    text-align: center;
    font-size: 82px;
    line-height: 1.3;
}
.hero-art p {
    color: #6255ed;
    font-family: 'Nunito', sans-serif;
    font-weight: 800;
    font-size: 16px;
}
.privacy {
    margin-top: 18px;
    background: #ffffffb8;
    border: 1px solid #d5e8ff;
    border-radius: 13px;
    padding: 12px 15px;
    color: #52638a;
    font-size: 12px;
    line-height: 1.6;
}
.section-card {
    background: #ffffffd9;
    border: 1px solid #e6e8fa;
    border-radius: 20px;
    padding: 21px;
    box-shadow: 0 7px 24px #37436b08;
    margin-bottom: 16px;
}
.section-heading {
    font-family: 'Nunito', sans-serif;
    color: #202653;
    font-size: 20px;
    font-weight: 900;
}
.section-sub {
    color: #7a84a6;
    font-size: 12px;
    margin-top: 3px;
    margin-bottom: 15px;
}
.result-card {
    background: linear-gradient(120deg, #e9fbf4, #f3fffb);
    border: 1px solid #c7f0df;
    border-radius: 17px;
    padding: 18px;
    margin: 9px 0 15px;
}
.result-label {
    color: #16805c;
    font-weight: 800;
    font-size: 11px;
    letter-spacing: .7px;
    text-transform: uppercase;
}
.result-action {
    font-family: 'Nunito', sans-serif;
    font-weight: 900;
    color: #165b48;
    font-size: 25px;
    margin: 5px 0;
}
.result-description {
    font-size: 13px;
    color: #477568;
    line-height: 1.6;
}
.metric-card {
    border: 1px solid #e5e8fb;
    border-radius: 16px;
    padding: 15px;
    background: white;
    min-height: 112px;
}
.metric-label {
    font-size: 12px;
    color: #7882a5;
    font-weight: 700;
}
.metric-value {
    font-family: 'Nunito', sans-serif;
    font-size: 26px;
    font-weight: 900;
    color: #202653;
    margin-top: 7px;
}
.small-note {
    font-size: 11px;
    color: #8992b0;
    line-height: 1.6;
}
.step {
    display: flex;
    gap: 12px;
    align-items: flex-start;
    margin: 12px 0;
    color: #46527e;
    font-size: 13px;
    line-height: 1.65;
}
.step-number {
    flex: 0 0 26px;
    height: 26px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 9px;
    background: #e9e7ff;
    color: #6255ed;
    font-size: 12px;
    font-weight: 900;
}
.disclaimer {
    background: #f3f0ff;
    border: 1px solid #e2dcff;
    color: #66628c;
    border-radius: 13px;
    padding: 13px;
    font-size: 11px;
    line-height: 1.7;
    margin-top: 16px;
}
.footer {
    text-align: center;
    border-top: 1px solid #e8e9f8;
    padding: 22px 0 8px;
    margin-top: 20px;
    color: #8189aa;
    font-size: 12px;
}
div.stButton > button {
    border-radius: 12px;
    border: 1px solid #e5e4fb;
    font-weight: 700;
    transition: all .15s ease;
}
div.stButton > button[kind="primary"] {
    background: linear-gradient(100deg, #6557ee, #8271fa);
    color: white;
    border: none;
    min-height: 49px;
    box-shadow: 0 6px 15px #6557ee25;
}
div.stButton > button[kind="primary"]:hover {
    background: linear-gradient(100deg, #5546df, #7260ef);
    box-shadow: 0 8px 20px #6557ee32;
}
div[data-testid="stTextArea"] textarea {
    border: 1px solid #e0e4f5;
    border-radius: 13px;
    background: #fff;
}
div[data-testid="stTextArea"] textarea:focus {
    border-color: #8b80f7;
    box-shadow: 0 0 0 2px #8b80f720;
}
div[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #6557ee, #45b9ee);
    border-radius: 99px;
}
hr {
    border-color: #eaebf7;
}
@media (max-width: 700px) {
    .hero { padding: 22px 18px; }
    .section-card { padding: 15px; }
    .brand-name { font-size: 24px; }
}
</style>
""", unsafe_allow_html=True)

# ---------- SAMPLE SCENARIOS ----------
SAMPLES = {
    "🎓  Scholarship offer": (
        "A scholarship message says I must pay an immediate processing "
        "fee before my award can be released."
    ),
    "💼  Internship offer": (
        "I received an internship offer from an unfamiliar company asking "
        "me to submit my identity documents through an unknown link."
    ),
    "📱  OTP request": (
        "Someone claiming to be customer support is asking me to share "
        "the OTP sent to my phone to prevent my account from being blocked."
    ),
    "✉️  Prize message": (
        "I received a message saying I won a prize and must click an "
        "unfamiliar link and pay a fee to claim it."
    ),
}

if "message_input" not in st.session_state:
    st.session_state.message_input = ""
if "proofpath_result" not in st.session_state:
    st.session_state.proofpath_result = None
if "last_message" not in st.session_state:
    st.session_state.last_message = ""

def choose_sample(sample_text):
    st.session_state.message_input = sample_text
    st.session_state.proofpath_result = None
    st.session_state.last_message = ""

# ---------- HEADER ----------
st.markdown("""
<div class="brand">
  <div class="brand-icon">🛡️</div>
  <div>
    <div class="brand-name">Proof<span>Path</span></div>
    <div class="brand-tag">THINK. VERIFY. STAY SAFE. ✦</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ---------- HERO ----------
hero_left, hero_right = st.columns([3, 1], vertical_alignment="center")
with hero_left:
    st.markdown("""
    <div class="hero">
      <div class="eyebrow">✦ YOUR DIGITAL SAFETY COMPANION</div>
      <div class="hero-title">
        Make safer choices,<br><span>one message at a time.</span>
      </div>
      <div class="hero-copy">
        Unsure about a scholarship, internship, payment request or suspicious
        message? ProofPath uses rule-based safety checks to identify common warning signs, recommend a cautious next step, and help you decide how to proceed.
      </div>
      <div class="privacy">
        🔒 <b>Privacy first:</b> Do not paste passwords, OTPs, bank details,
        identity numbers or other sensitive personal information.
      </div>
    </div>
    """, unsafe_allow_html=True)
with hero_right:
    st.markdown("""
    <div class="hero-art">
      🛡️
      <p>Pause. Check.<br>Choose wisely. ✨</p>
    </div>
    """, unsafe_allow_html=True)

# ---------- MAIN COLUMNS ----------
left, right = st.columns([0.96, 1.04], gap="large")

with left:
    st.markdown("""
    <div class="section-heading">💌 Analyze a message</div>
    <div class="section-sub">
      Describe what happened. We'll help you think through the next step.
    </div>
    """, unsafe_allow_html=True)

    st.text_area(
        "Message or situation",
        key="message_input",
        height=155,
        max_chars=4000,
        placeholder=(
            "Example: A scholarship message says I must pay a processing "
            "fee before my award can be released..."
        ),
        label_visibility="collapsed",
    )

    if st.button(
        "✨  Analyze with ProofPath  →",
        type="primary",
        use_container_width=True,
    ):
        message = st.session_state.message_input.strip()
        if not message:
            st.warning("Please enter a message or choose a sample scenario.")
        else:
            
            try:
                with st.spinner("Analyzing your situation..."):
                    result = get_decision(message)

                st.session_state.proofpath_result = {
                    "selected_action": result["selected_action"],
                    "confidence": result["confidence"],
                    "probabilities": result["probabilities"],
                    "needs_review": result["human_review"],
                    "meaning": result["meaning"],
                    "guidance": result["guidance"],
                    "analysis_mode": result["analysis_mode"],
                }
                st.session_state.last_message = message

            except Exception as error:
                st.error(f"Analysis failed: {error}")

            except Exception:
                st.warning(
                    "The Strands Decider service is unavailable. "
                    "Live analysis needs a hosted Decider endpoint."
                )
                st.info(
                    "You can explore the interface, but live AI analysis "
                    "is not available on this deployment yet."
                )

    st.markdown("---")
    st.markdown("""
    <div class="section-heading">✨ Try a sample scenario</div>
    <div class="section-sub">
      Choose an example to fill the analyzer. Review it before analyzing.
    </div>
    """, unsafe_allow_html=True)

    sample_items = list(SAMPLES.items())
    for start in range(0, len(sample_items), 2):
        sample_cols = st.columns(2, gap="small")
        for col, (sample_name, sample_text) in zip(
            sample_cols, sample_items[start:start + 2]
        ):
            with col:
                with st.container(border=True):
                    st.markdown(f"**{sample_name}**")
                    st.caption(sample_text)
                    st.button(
                        "Use this example ↗",
                        key=f"sample_{start}_{sample_name}",
                        use_container_width=True,
                        on_click=choose_sample,
                        args=(sample_text,),
                    )

with right:
    st.markdown("""
    <div class="section-heading">✦ Your decision dashboard</div>
    <div class="section-sub">
Rule-based safety analysis is active. Live AI analysis is not connected in this demo.
    </div>
    """, unsafe_allow_html=True)

    result_data = st.session_state.proofpath_result

    if not result_data:
        st.markdown("""
        <div class="result-card">
          <div class="result-label">✧ Ready when you are</div>
          <div class="result-action">Your next step starts here</div>
          <div class="result-description">
            Enter a situation and select <b>Analyze with ProofPath</b>.
            Your recommendation, confidence, probabilities and safety
            guidance will appear here.
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="section-card">
          <div class="section-heading">🌱 How ProofPath helps</div>
          <div class="step"><div class="step-number">1</div>
            <div><b>Describe</b><br>Share the situation without sensitive details.</div>
          </div>
          <div class="step"><div class="step-number">2</div>
            <div><b>Consider</b><br>The Decider selects a possible next action.</div>
          </div>
          <div class="step"><div class="step-number">3</div>
            <div><b>Verify</b><br>Review the guidance and check important claims independently.</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        action = result_data["selected_action"]
        confidence = result_data["confidence"]
        probabilities = result_data["probabilities"]
        needs_review = result_data["needs_review"]

        st.markdown(f"""
        <div class="result-card">
          <div class="result-label">🛡️ RECOMMENDED NEXT ACTION</div>
          <div class="result-action">{action.replace("_", " ")}</div>
          
          <div class="result-description">{result_data["meaning"]}</div>

        </div>
        """, unsafe_allow_html=True)

        metric_a, metric_b = st.columns(2, gap="small")
        with metric_a:
            st.markdown(f"""
            <div class="metric-card">
              <div class="metric-label">🎯 Decider confidence</div>
              <div class="metric-value">{confidence:.2%}</div>
              <div class="small-note">Model-reported confidence</div>
            </div>
            """, unsafe_allow_html=True)
        with metric_b:
            review_label = "Recommended" if needs_review else "Not flagged"
            st.markdown(f"""
            <div class="metric-card">
              <div class="metric-label">👀 Human review</div>
              <div class="metric-value" style="font-size:21px;">
                {review_label}
              </div>
              <div class="small-note">
                {"Human review is recommended for consequential decisions. This rule-based score is a heuristic, not a calibrated probability."}
              </div>
            </div>
            """, unsafe_allow_html=True)

        if needs_review:
            st.warning(
                "This recommendation is uncertain. Seek human review "
                "before taking consequential action."
            )
        else:
            st.info(
                "The review rule did not flag this result. This does not "
                "mean the message is safe."
            )

      
        st.markdown("#### 🎯 Rule-based confidence score")

        confidence = float(result_data["confidence"])

        st.progress(max(0.0, min(1.0, confidence)))
        st.markdown(
            f"<div style='text-align:right;font-weight:800;"
            f"color:#4f4b99;font-size:14px'>{confidence:.0%}</div>",
            unsafe_allow_html=True,
        )

        st.caption(
            "Heuristic score from keyword-based safety rules — "
            "not a calibrated probability or guarantee of correctness."
        )

        if result_data.get("reasons"):
            st.markdown("#### 🔎 Warning signs detected")
            for reason in result_data["reasons"]:
                st.markdown(f"- {reason}")


        st.markdown("#### 🧭 Recommended safety steps")
        
        for number, step in enumerate(result_data["guidance"], start=1):

            st.markdown(f"""
            <div class="step">
              <div class="step-number">{number}</div>
              <div>{step}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="disclaimer">
          <b>💜 A thoughtful reminder</b><br>
          ProofPath offers decision support, not a definitive fraud verdict.
          Model confidence and probabilities are not guarantees of correctness.
          Verify important claims through independent, trusted sources.
        </div>
        """, unsafe_allow_html=True)

        with st.expander("View the situation analyzed"):
            st.write(st.session_state.last_message)

# ---------- FOOTER ----------
st.markdown("""
<div class="footer">
  <b style="color:#6255ed;">🛡️ ProofPath</b>
  &nbsp; · &nbsp; Student digital safety project
  <br><br>
  💜 Verify sources &nbsp; · &nbsp; 🔎 Spot warning signs
  &nbsp; · &nbsp; 🤝 Ask for help &nbsp; · &nbsp; ✨ Make safer choices
  <br><br>
  <span style="font-size:10px;">
    Built with Python, Streamlit and Strands Decider.
    Bedrock integration is separate and is not claimed as active.
  </span>
</div>
""", unsafe_allow_html=True)
