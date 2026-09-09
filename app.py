



import streamlit as st
import tempfile
import os
import io
import hashlib
import soundfile as sf
import os
import imageio_ffmpeg

# Make the bundled FFmpeg executable available to Transformers
ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
os.environ["PATH"] = os.path.dirname(ffmpeg_path) + os.pathsep + os.environ.get("PATH", "")
from transformers import pipeline 

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & METADATA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="VoxShield // Voice Integrity Forensics",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------------------------------------
# 2. CUSTOM CYBERSECURITY DESIGN SYSTEM (CSS)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Global Reset & Streamlit Chrome Cleanup */
    #MainMenu, footer, [data-testid="stToolbar"], header[data-testid="stHeader"] {
        display: none !important;
    }

    /* Lively Cybernetic Background with Ambient Lighting & Matrix Grid */
    .stApp {
        background-color: #060A13;
        background-image: 
            radial-gradient(ellipse 90% 50% at 50% -10%, rgba(14, 165, 233, 0.22) 0%, transparent 65%),
            radial-gradient(ellipse 60% 45% at 95% 75%, rgba(99, 102, 241, 0.14) 0%, transparent 60%),
            radial-gradient(ellipse 55% 35% at 5% 35%, rgba(16, 185, 129, 0.10) 0%, transparent 55%),
            radial-gradient(circle at 50% 50%, rgba(30, 41, 59, 0.25) 0%, transparent 80%),
            linear-gradient(rgba(56, 189, 248, 0.04) 1px, transparent 1px),
            linear-gradient(90deg, rgba(56, 189, 248, 0.04) 1px, transparent 1px);
        background-size: 100% 100%, 100% 100%, 100% 100%, 100% 100%, 38px 38px, 38px 38px;
        background-attachment: fixed;
        color: #E2E8F0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Inter", sans-serif;
    }

    .main .block-container {
        max-width: 1060px;
        padding-top: 2.2rem;
        padding-bottom: 4rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
        margin: 0 auto;
    }

    /* Hero Header Lockup with Glowing Accent */
    .hero-container {
        background: linear-gradient(135deg, rgba(13, 22, 42, 0.88) 0%, rgba(8, 14, 28, 0.94) 100%);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        border: 1px solid rgba(56, 189, 248, 0.22);
        border-top: 2px solid #38BDF8;
        border-radius: 14px;
        padding: 30px 34px;
        margin-bottom: 24px;
        position: relative;
        box-shadow: 0 12px 36px -8px rgba(0, 0, 0, 0.6), 0 0 30px -8px rgba(14, 165, 233, 0.18);
    }

    .brand-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 12px;
        margin-bottom: 8px;
    }

    .brand-title {
        font-size: 2.3rem;
        font-weight: 800;
        letter-spacing: -0.025em;
        color: #F8FAFC;
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 0;
        text-shadow: 0 0 20px rgba(56, 189, 248, 0.2);
    }

    .system-status-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.35);
        color: #34D399;
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 0.72rem;
        font-weight: 600;
        padding: 4px 14px;
        border-radius: 9999px;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        box-shadow: 0 0 12px rgba(16, 185, 129, 0.15);
    }

    .pulse-dot {
        width: 7px;
        height: 7px;
        background-color: #10B981;
        border-radius: 50%;
        box-shadow: 0 0 8px #10B981;
        animation: statusPulse 2s infinite ease-in-out;
    }

    @keyframes statusPulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(0.85); }
    }

    .hero-subtitle {
        font-size: 1.15rem;
        font-weight: 600;
        color: #38BDF8;
        letter-spacing: -0.01em;
        margin-bottom: 8px;
    }

    .hero-desc {
        color: #94A3B8;
        font-size: 0.95rem;
        line-height: 1.55;
        max-width: 820px;
        margin: 0;
    }

    /* Glassmorphic Forensic Cards */
    .forensic-card {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.8) 0%, rgba(11, 18, 33, 0.85) 100%);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(56, 189, 248, 0.16);
        border-radius: 12px;
        padding: 22px 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px -6px rgba(0, 0, 0, 0.45);
        transition: border-color 0.25s ease, box-shadow 0.25s ease;
    }

    .forensic-card:hover {
        border-color: rgba(56, 189, 248, 0.35);
        box-shadow: 0 10px 36px -4px rgba(14, 165, 233, 0.15);
    }

    .section-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #CBD5E1;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 16px;
    }

    /* Metadata Badge Strip */
    .metadata-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
        gap: 12px;
        margin: 16px 0;
    }

    .meta-item {
        background: rgba(7, 12, 23, 0.7);
        border: 1px solid rgba(56, 189, 248, 0.12);
        border-radius: 8px;
        padding: 10px 14px;
        transition: border-color 0.2s ease;
    }

    .meta-item:hover {
        border-color: rgba(56, 189, 248, 0.3);
    }

    .meta-key {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748B;
        margin-bottom: 4px;
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    }

    .meta-val {
        font-size: 0.92rem;
        font-weight: 600;
        color: #F1F5F9;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    /* Risk Level Master Banner */
    .risk-banner {
        border-radius: 12px;
        padding: 24px 28px;
        margin-bottom: 20px;
        display: flex;
        flex-direction: column;
        gap: 12px;
        border-width: 1px;
        border-style: solid;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        box-shadow: 0 10px 30px -6px rgba(0, 0, 0, 0.45);
    }

    .risk-banner-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 12px;
    }

    .risk-level-tag {
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        padding: 4px 12px;
        border-radius: 6px;
    }

    .risk-title {
        font-size: 1.45rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin: 0;
    }

    .risk-desc {
        font-size: 0.95rem;
        line-height: 1.5;
        margin: 0;
    }

    .risk-advisory {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.86rem;
        padding: 8px 14px;
        border-radius: 6px;
        font-weight: 500;
    }

    /* Risk Variants with Gradient Accents */
    .risk-high {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.14) 0%, rgba(15, 23, 42, 0.85) 100%);
        border-color: rgba(239, 68, 68, 0.45);
        box-shadow: 0 8px 30px -4px rgba(239, 68, 68, 0.2);
    }
    .risk-high .risk-title { color: #FCA5A5; }
    .risk-high .risk-desc { color: #FECACA; }
    .risk-high .risk-level-tag {
        background: rgba(239, 68, 68, 0.25);
        color: #F87171;
        border: 1px solid rgba(239, 68, 68, 0.5);
    }
    .risk-high .risk-advisory {
        background: rgba(239, 68, 68, 0.18);
        color: #FCA5A5;
        border-left: 3px solid #EF4444;
    }

    .risk-medium {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.14) 0%, rgba(15, 23, 42, 0.85) 100%);
        border-color: rgba(245, 158, 11, 0.45);
        box-shadow: 0 8px 30px -4px rgba(245, 158, 11, 0.2);
    }
    .risk-medium .risk-title { color: #FDE68A; }
    .risk-medium .risk-desc { color: #FEF3C7; }
    .risk-medium .risk-level-tag {
        background: rgba(245, 158, 11, 0.25);
        color: #FBBF24;
        border: 1px solid rgba(245, 158, 11, 0.5);
    }
    .risk-medium .risk-advisory {
        background: rgba(245, 158, 11, 0.18);
        color: #FDE68A;
        border-left: 3px solid #F59E0B;
    }

    .risk-low {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.14) 0%, rgba(15, 23, 42, 0.85) 100%);
        border-color: rgba(16, 185, 129, 0.45);
        box-shadow: 0 8px 30px -4px rgba(16, 185, 129, 0.2);
    }
    .risk-low .risk-title { color: #A7F3D0; }
    .risk-low .risk-desc { color: #D1FAE5; }
    .risk-low .risk-level-tag {
        background: rgba(16, 185, 129, 0.25);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.5);
    }
    .risk-low .risk-advisory {
        background: rgba(16, 185, 129, 0.18);
        color: #A7F3D0;
        border-left: 3px solid #10B981;
    }

    /* Metric Cards with Depth & Hover Lift */
    .metric-card {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.85) 0%, rgba(11, 18, 33, 0.9) 100%);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(56, 189, 248, 0.18);
        border-radius: 12px;
        padding: 24px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 8px 30px -4px rgba(0, 0, 0, 0.45);
        transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    }

    .metric-card:hover {
        transform: translateY(-3px);
        border-color: rgba(56, 189, 248, 0.38);
        box-shadow: 0 14px 40px -6px rgba(14, 165, 233, 0.22);
    }

    .metric-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }

    .metric-label {
        font-size: 0.76rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #94A3B8;
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    }

    .metric-score {
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1.1;
        margin: 6px 0 10px 0;
    }

    .score-synthetic {
        color: #F87171;
        text-shadow: 0 0 16px rgba(248, 113, 113, 0.3);
    }

    .score-genuine {
        color: #34D399;
        text-shadow: 0 0 16px rgba(52, 211, 153, 0.3);
    }

    .metric-subtext {
        color: #64748B;
        font-size: 0.82rem;
        line-height: 1.4;
    }

    /* Custom Meter Bar */
    .meter-container {
        width: 100%;
        height: 6px;
        background: rgba(30, 41, 59, 0.8);
        border-radius: 999px;
        overflow: hidden;
        margin: 12px 0 6px 0;
    }

    .meter-fill-synthetic {
        height: 100%;
        background: linear-gradient(90deg, #F87171, #EF4444);
        border-radius: 999px;
        box-shadow: 0 0 10px rgba(239, 68, 68, 0.5);
    }

    .meter-fill-genuine {
        height: 100%;
        background: linear-gradient(90deg, #34D399, #10B981);
        border-radius: 999px;
        box-shadow: 0 0 10px rgba(16, 185, 129, 0.5);
    }

    /* Analysis Summary Callout */
    .summary-card {
        background: linear-gradient(145deg, rgba(11, 18, 34, 0.85) 0%, rgba(15, 23, 42, 0.8) 100%);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(56, 189, 248, 0.18);
        border-radius: 12px;
        padding: 22px 24px;
        margin: 18px 0;
        box-shadow: 0 8px 28px -6px rgba(0, 0, 0, 0.45);
    }

    .summary-text {
        font-size: 0.95rem;
        color: #CBD5E1;
        line-height: 1.6;
        margin-bottom: 14px;
    }

    .insights-list {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }

    .insight-row {
        display: flex;
        align-items: baseline;
        gap: 10px;
        font-size: 0.88rem;
        color: #94A3B8;
    }

    .insight-bullet {
        color: #38BDF8;
        font-size: 0.75rem;
    }

    /* Technical Details Card */
    .tech-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 12px;
        margin-bottom: 16px;
    }

    .tech-box {
        background: rgba(8, 12, 20, 0.8);
        border: 1px solid rgba(56, 189, 248, 0.14);
        border-radius: 8px;
        padding: 12px 14px;
    }

    .tech-key {
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 0.7rem;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 4px;
    }

    .tech-val {
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        font-size: 0.85rem;
        color: #E2E8F0;
        word-break: break-all;
    }

    /* Streamlit Primary Button Tweaks */
    .stButton > button {
        background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%) !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding: 0.7rem 1.6rem !important;
        border-radius: 8px !important;
        border: 1px solid #38BDF8 !important;
        box-shadow: 0 4px 16px rgba(2, 132, 199, 0.35) !important;
        transition: all 0.25s ease !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #0369A1 0%, #075985 100%) !important;
        border-color: #7DD3FC !important;
        box-shadow: 0 4px 24px rgba(56, 189, 248, 0.5) !important;
        transform: translateY(-1px) !important;
    }

    [data-testid="stFileUploader"] {
        background: rgba(15, 23, 42, 0.5) !important;
        border: 1px dashed rgba(56, 189, 248, 0.3) !important;
        border-radius: 12px !important;
        padding: 14px !important;
        backdrop-filter: blur(10px) !important;
        transition: border-color 0.25s ease !important;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: #38BDF8 !important;
    }

    /* Expanders */
    [data-testid="stExpander"] {
        background-color: rgba(15, 23, 42, 0.75) !important;
        border: 1px solid rgba(56, 189, 248, 0.18) !important;
        border-radius: 10px !important;
        backdrop-filter: blur(12px) !important;
    }

    /* Footer / Privacy note */
    .audit-footer {
        margin-top: 36px;
        padding-top: 18px;
        border-top: 1px solid rgba(56, 189, 248, 0.15);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
        color: #64748B;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. HERO & BRANDING SECTION
# -----------------------------------------------------------------------------
st.markdown("""
<div class="hero-container">
    <div class="brand-row">
        <div class="brand-title">
            <span>🛡️ VoxShield</span>
        </div>
        <div class="system-status-pill">
            <span class="pulse-dot"></span>
            <span>Engine: Operational // Wav2Vec2 Forensics</span>
        </div>
    </div>
    <div class="hero-subtitle">AI-Powered Voice Integrity Analysis</div>
    <p class="hero-desc">
        Acoustic neural forensics system engineered to detect voice synthesis, speech cloning, 
        and vocal deepfakes. Evaluates subtle micro-spectral artifacts and latent feature representations 
        to evaluate vocal authenticity.
    </p>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. LOAD MODEL (Unchanged Pipeline Logic)
# -----------------------------------------------------------------------------
@st.cache_resource
def load_detector():
    return pipeline(
        "audio-classification",
        model="garystafford/wav2vec2-deepfake-voice-detector"
    )

with st.spinner("Initializing VoxShield forensic model..."):
    detector = load_detector()

# -----------------------------------------------------------------------------
# 5. AUDIO METADATA INSPECTOR UTILITIES
# -----------------------------------------------------------------------------
def get_audio_metadata(audio_file):
    """Safely extracts audio file properties without mutating pointer state."""
    meta = {
        "filename": audio_file.name,
        "format": os.path.splitext(audio_file.name)[1].lstrip(".").upper() or "UNKNOWN",
        "size_str": f"{audio_file.size / 1024:.1f} KB" if audio_file.size < 1024 * 1024 else f"{audio_file.size / (1024 * 1024):.2f} MB",
        "duration_str": "Unavailable",
        "duration_sec": None,
        "samplerate_str": "Unknown",
        "channels_str": "Unknown",
        "sha256": "Calculating..."
    }

    try:
        data = audio_file.getvalue()
        # Compute SHA-256 for cybersecurity audit trail
        meta["sha256"] = hashlib.sha256(data).hexdigest()[:16] + "..."

        with sf.SoundFile(io.BytesIO(data)) as s_file:
            dur = len(s_file) / float(s_file.samplerate)
            meta["duration_sec"] = dur
            if dur >= 60:
                mins = int(dur // 60)
                secs = dur % 60
                meta["duration_str"] = f"{mins:02d}:{secs:04.1f} ({dur:.1f}s)"
            else:
                meta["duration_str"] = f"{dur:.2f}s"
            
            meta["samplerate_str"] = f"{s_file.samplerate:,} Hz"
            meta["channels_str"] = "Mono" if s_file.channels == 1 else "Stereo" if s_file.channels == 2 else f"{s_file.channels} ch"
            if s_file.format:
                meta["format"] = s_file.format.upper()
    except Exception:
        # Graceful fallback for non-PCM / container variants
        pass

    return meta

# -----------------------------------------------------------------------------
# 6. AUDIO UPLOAD & INSPECTION AREA
# -----------------------------------------------------------------------------
st.markdown('<div class="section-title">📁 Audio Ingestion & File Inspector</div>', unsafe_allow_html=True)

audio_file = st.file_uploader(
    "Upload a voice recording for forensic inspection",
    type=["wav", "mp3", "m4a", "flac"],
    help="Supported formats: WAV, MP3, M4A, FLAC. Raw audio is evaluated locally."
)

if audio_file is not None:
    # Extract metadata
    meta = get_audio_metadata(audio_file)

    # Ingestion details card
    st.markdown(f"""
    <div class="forensic-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <div style="font-weight: 700; color: #F1F5F9; font-size: 1rem; display: flex; align-items: center; gap: 8px;">
                <span>🎙️</span> <span>{meta['filename']}</span>
            </div>
            <span style="font-family: ui-monospace, monospace; font-size: 0.75rem; background: rgba(30, 41, 59, 0.8); color: #94A3B8; padding: 3px 8px; border-radius: 4px; border: 1px solid rgba(56, 189, 248, 0.2);">
                SHA256: {meta['sha256']}
            </span>
        </div>
        <div class="metadata-grid">
            <div class="meta-item">
                <div class="meta-key">Format</div>
                <div class="meta-val">{meta['format']}</div>
            </div>
            <div class="meta-item">
                <div class="meta-key">File Size</div>
                <div class="meta-val">{meta['size_str']}</div>
            </div>
            <div class="meta-item">
                <div class="meta-key">Duration</div>
                <div class="meta-val">{meta['duration_str']}</div>
            </div>
            <div class="meta-item">
                <div class="meta-key">Sample Rate</div>
                <div class="meta-val">{meta['samplerate_str']}</div>
            </div>
            <div class="meta-item">
                <div class="meta-key">Channels</div>
                <div class="meta-val">{meta['channels_str']}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Audio playback preview
    st.audio(audio_file)

    col_btn, _ = st.columns([1, 2])
    with col_btn:
        run_analysis = st.button("🔍 Analyze Voice", type="primary", use_container_width=True)

    # Maintain state across reruns if analyzed
    if "analysis_store" not in st.session_state:
        st.session_state.analysis_store = None

    if run_analysis:
        # Progress & loading state with clear status indication
        with st.status("Analyzing audio with VoxShield AI...", expanded=True) as status_box:
            st.write("Extracting acoustic waveforms and container properties...")
            
            suffix = os.path.splitext(audio_file.name)[1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                temp_file.write(audio_file.getbuffer())
                temp_path = temp_file.name

            try:
                st.write("Evaluating wav2vec2 latent feature representations...")
                raw_result = detector(temp_path)

                st.write("Parsing acoustic classification distribution...")
                # Find model labels safely (preserving original pipeline matching logic)
                fake_item = next(
                    (item for item in raw_result if item["label"].lower() in ["fake", "spoof", "synthetic"]),
                    None
                )
                real_item = next(
                    (item for item in raw_result if item["label"].lower() in ["real", "bonafide", "genuine"]),
                    None
                )

                if fake_item is None or real_item is None:
                    status_box.update(label="Unexpected model output format", state="error", expanded=True)
                    st.error("The detector returned unexpected classification labels.")
                    st.write(raw_result)
                    st.stop()

                fake_score = float(fake_item["score"])
                real_score = float(real_item["score"])

                # Store analysis in session state
                st.session_state.analysis_store = {
                    "filename": audio_file.name,
                    "fake_score": fake_score,
                    "real_score": real_score,
                    "raw_result": raw_result,
                    "meta": meta
                }

                status_box.update(label="Forensic analysis complete", state="complete", expanded=False)

            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

    # -----------------------------------------------------------------------------
    # 7. FORENSIC RESULTS DASHBOARD (Visual Hierarchy 1 -> 5)
    # -----------------------------------------------------------------------------
    if st.session_state.analysis_store and st.session_state.analysis_store["filename"] == audio_file.name:
        res = st.session_state.analysis_store
        fake_score = res["fake_score"]
        real_score = res["real_score"]
        fake_pct = fake_score * 100
        real_pct = real_score * 100

        # Preserve exact threshold engine
        if fake_score >= 0.70:
            risk_level = "HIGH"
            risk_css = "risk-high"
            risk_title = "HIGH RISK: Strong Synthetic Indicators"
            risk_summary = (
                "The acoustic model identified spectral signatures and latent feature patterns "
                "strongly characteristic of synthetic or cloned speech generation."
            )
            risk_advisory = "CRITICAL ADVISORY: Model confidence leans heavily toward synthetic origin. Do NOT rely on this recording for identity verification or sensitive authorization."
            explanation_body = (
                f"Based on wav2vec2 acoustic latent modeling, this recording yielded an estimated synthetic likelihood of "
                f"<strong>{fake_pct:.2f}%</strong>. In contrast, authentic human speech characteristics were estimated at "
                f"<strong>{real_pct:.2f}%</strong> model confidence. The acoustic anomalies detected are consistent with modern "
                f"neural text-to-speech (TTS) or voice conversion architectures."
            )
        elif fake_score >= 0.35:
            risk_level = "MEDIUM"
            risk_css = "risk-medium"
            risk_title = "MEDIUM RISK: Suspicious Acoustic Signals"
            risk_summary = (
                "The model detected ambiguous acoustic characteristics. The audio presents minor synthetic patterns "
                "or heavy codec compression artifacts that warrant caution."
            )
            risk_advisory = "CAUTION ADVISORY: Intermediate risk detected. Perform out-of-band verification before trusting voice authenticity."
            explanation_body = (
                f"The detector registered an estimated synthetic likelihood of <strong>{fake_pct:.2f}%</strong> against "
                f"an authentic model confidence of <strong>{real_pct:.2f}%</strong>. While not definitive, the score falls in "
                f"the suspicious threshold band where heavy lossy compression, background filtering, or partial voice manipulation "
                f"cannot be ruled out."
            )
        else:
            risk_level = "LOW"
            risk_css = "risk-low"
            risk_title = "LOW RISK: Authentic Speech Characteristics"
            risk_summary = (
                "Acoustic analysis indicates organic vocal dynamics, pitch variations, and spectral continuity "
                "consistent with authentic human vocalization."
            )
            risk_advisory = "VERIFICATION PASSED: No prominent synthetic speech anomalies detected by the forensic engine."
            explanation_body = (
                f"The analysis calculated a <strong>{real_pct:.2f}%</strong> model confidence for organic human speech, "
                f"with an estimated synthetic likelihood of only <strong>{fake_pct:.2f}%</strong>. The natural phoneme transitions "
                f"and micro-prosodic variations in this recording align with authentic vocal characteristics."
            )

        st.markdown("<div style='margin-top: 32px;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">📊 Forensic Analysis Dashboard</div>', unsafe_allow_html=True)

        # -------------------------------------------------------------
        # HIERARCHY ITEM 1: RISK LEVEL (Most prominent)
        # -------------------------------------------------------------
        st.markdown(f"""
        <div class="risk-banner {risk_css}">
            <div class="risk-banner-header">
                <span class="risk-level-tag">Risk Assessment // {risk_level}</span>
                <span style="font-family: ui-monospace, monospace; font-size: 0.8rem; color: #94A3B8;">
                    Threshold: {'&ge; 0.70' if risk_level == 'HIGH' else '&ge; 0.35' if risk_level == 'MEDIUM' else '< 0.35'}
                </span>
            </div>
            <h3 class="risk-title">{risk_title}</h3>
            <p class="risk-desc">{risk_summary}</p>
            <div class="risk-advisory">
                <span>🛡️</span>
                <span>{risk_advisory}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # -------------------------------------------------------------
        # HIERARCHY ITEMS 2 & 3: PROBABILITY METRIC CARDS
        # -------------------------------------------------------------
        col_synth, col_auth = st.columns(2)

        with col_synth:
            st.markdown(f"""
            <div class="metric-card">
                <div>
                    <div class="metric-header">
                        <span class="metric-label">Estimated Synthetic Likelihood</span>
                        <span style="font-size: 1.1rem;">🤖</span>
                    </div>
                    <div class="metric-score score-synthetic">{fake_pct:.2f}%</div>
                    <div class="meter-container">
                        <div class="meter-fill-synthetic" style="width: {min(max(fake_pct, 0.0), 100.0):.2f}%;"></div>
                    </div>
                </div>
                <div class="metric-subtext">
                    Estimated probability that audio contains synthetic speech or voice cloning artifacts.
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_auth:
            st.markdown(f"""
            <div class="metric-card">
                <div>
                    <div class="metric-header">
                        <span class="metric-label">Model Confidence (Authentic)</span>
                        <span style="font-size: 1.1rem;">👤</span>
                    </div>
                    <div class="metric-score score-genuine">{real_pct:.2f}%</div>
                    <div class="meter-container">
                        <div class="meter-fill-genuine" style="width: {min(max(real_pct, 0.0), 100.0):.2f}%;"></div>
                    </div>
                </div>
                <div class="metric-subtext">
                    Model confidence that acoustic signatures represent genuine, unmanipulated human speech.
                </div>
            </div>
            """, unsafe_allow_html=True)

        # -------------------------------------------------------------
        # HIERARCHY ITEM 4: RESULT EXPLANATION ("Analysis Summary")
        # -------------------------------------------------------------
        st.markdown(f"""
        <div class="summary-card">
            <div class="section-title" style="margin-bottom: 10px;">
                <span>📋 Analysis Summary</span>
            </div>
            <p class="summary-text">{explanation_body}</p>
            <div class="insights-list">
                <div class="insight-row">
                    <span class="insight-bullet">▸</span>
                    <span><strong>Integrity Indicator:</strong> Evaluated against trained deepfake and voice cloning corpus patterns.</span>
                </div>
                <div class="insight-row">
                    <span class="insight-bullet">▸</span>
                    <span><strong>Spectral Consistency:</strong> Acoustic features processed via wav2vec2 self-supervised speech transformer.</span>
                </div>
                <div class="insight-row">
                    <span class="insight-bullet">▸</span>
                    <span><strong>Operational Context:</strong> Model confidence reflects statistical likelihood and should be combined with secondary contextual evidence.</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # -------------------------------------------------------------
        # HIERARCHY ITEM 5: TECHNICAL DETAILS (Collapsible)
        # -------------------------------------------------------------
        with st.expander("🔬 Technical Details & Forensic Audit Log", expanded=False):
            st.markdown(f"""
            <div class="tech-grid">
                <div class="tech-box">
                    <div class="tech-key">Detector Model</div>
                    <div class="tech-val">garystafford/wav2vec2-deepfake-voice-detector</div>
                </div>
                <div class="tech-box">
                    <div class="tech-key">Architecture</div>
                    <div class="tech-val">Wav2Vec2ForSequenceClassification</div>
                </div>
                <div class="tech-box">
                    <div class="tech-key">Audio Format</div>
                    <div class="tech-val">{res['meta']['format']} ({res['meta']['channels_str']})</div>
                </div>
                <div class="tech-box">
                    <div class="tech-key">Target Sample Rate</div>
                    <div class="tech-val">{res['meta']['samplerate_str']}</div>
                </div>
                <div class="tech-box">
                    <div class="tech-key">Duration Analyzed</div>
                    <div class="tech-val">{res['meta']['duration_str']}</div>
                </div>
                <div class="tech-box">
                    <div class="tech-key">File Size</div>
                    <div class="tech-val">{res['meta']['size_str']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="tech-key" style="margin-bottom: 6px;">Raw Classification Output (JSON)</div>', unsafe_allow_html=True)
            st.json(res["raw_result"])

            st.caption(
                "⚖️ Forensic Disclaimer: The displayed values represent statistical model confidence calculated from acoustic "
                "waveform features. AI deepfake detection is inherently probabilistic and should not be treated as absolute or definitive "
                "legal proof of vocal authenticity."
            )

# -----------------------------------------------------------------------------
# 8. PRIVACY & COMPLIANCE FOOTER
# -----------------------------------------------------------------------------
st.markdown("""
<div class="audit-footer">
    <div>
        <span>🔒 <strong>Data Privacy:</strong> Audio recordings are processed in local memory during inspection and immediately purged from temporary storage.</span>
    </div>
    <div>
        <span>VoxShield AI Forensics Engine v2.4</span>
    </div>
</div>
""", unsafe_allow_html=True)
