import streamlit as st
from config import OPENROUTER_API_KEY, STYLE_MODIFIERS
from generator import build_image_prompt, generate_poster
from storage import save_campaign, get_campaign_history, get_campaign_by_id

st.set_page_config(page_title="Campaign Poster Generator", page_icon="🎨", layout="wide")

st.markdown("""
<style>
    .main { background-color: #0f0f1a; }
    .stTextInput > div > div > input { background-color: #1a1a2e; color: white; }
    .stSelectbox > div > div { background-color: #1a1a2e; color: white; }
    h1 { color: #e94560; }
    .stButton > button {
        background-color: #e94560; color: white;
        border: none; border-radius: 8px;
        padding: 0.5rem 2rem; font-size: 1rem; font-weight: bold;
        width: 100%;
    }
    .stButton > button:hover { background-color: #c73652; }
</style>
""", unsafe_allow_html=True)

st.title("🎨 Campaign Poster Generator")
st.caption("Powered by OpenRouter · Gemini 2.0 Flash + FLUX 1.1 Pro")

if not OPENROUTER_API_KEY:
    st.error("OPENROUTER_API_KEY not set. Add it to your .env file.")
    st.stop()

# ── Layout ──────────────────────────────────────────────────────────────────
col_form, col_preview = st.columns([1, 1], gap="large")

with col_form:
    st.subheader("Campaign Details")
    restaurant_name = st.text_input("Restaurant Name")
    festival        = st.text_input("Festival / Occasion")
    offer           = st.text_input("Offer / Campaign Info")
    target_audience = st.text_input("Target Audience")
    duration        = st.text_input("Duration (days)")
    start_date      = st.text_input("Start Date (DD/MM/YY)")

    style_options = {"original": ""} | {label: mod for label, mod in STYLE_MODIFIERS.values()}
    style_label = st.selectbox("Poster Style", list(style_options.keys()))

    generate = st.button("Generate Poster")

with col_preview:
    st.subheader("Preview")
    preview_slot = st.empty()
    log_slot     = st.empty()

# ── Session state for campaign_id ────────────────────────────────────────────
if "campaign_id" not in st.session_state:
    st.session_state.campaign_id = None

# ── Generate ─────────────────────────────────────────────────────────────────
if generate:
    fields = {
        "restaurant_name": restaurant_name,
        "festival": festival,
        "offer": offer,
        "target_audience": target_audience,
        "duration": duration,
        "start_date": start_date,
    }

    if not all(fields.values()):
        st.warning("Please fill in all fields before generating.")
    else:
        style_modifier = style_options[style_label]
        campaign = dict(fields)
        if st.session_state.campaign_id:
            campaign["campaign_id"] = st.session_state.campaign_id

        with col_preview:
            with st.spinner("Step 1/3 — Building image prompt..."):
                image_prompt = build_image_prompt(campaign, style_modifier)

            log_slot.info(f"Prompt: {image_prompt[:200]}{'...' if len(image_prompt) > 200 else ''}")

            history_count = len(get_campaign_history())
            filename = f"{festival.replace(' ', '_')}_{style_label}_{history_count+1}.png"

            with st.spinner("Step 2/3 — Generating poster (may take ~30s)..."):
                image_path = generate_poster(image_prompt, filename)

            with st.spinner("Step 3/3 — Saving to history..."):
                st.session_state.campaign_id = save_campaign(
                    campaign, image_prompt, image_path, style_label
                )

            preview_slot.image(image_path, use_container_width=True)
            st.success(f"Done! Saved to `{image_path}`  |  Campaign ID: `{st.session_state.campaign_id}`")

# ── History tab ───────────────────────────────────────────────────────────────
st.divider()
with st.expander("📋 Campaign History"):
    history = get_campaign_history()
    if not history:
        st.write("No campaigns yet.")
    else:
        for entry in reversed(history[-20:]):
            c1, c2 = st.columns([2, 1])
            with c1:
                st.markdown(f"**{entry['inputs'].get('restaurant_name','?')}** — {entry['inputs'].get('festival','?')}")
                st.caption(f"Style: {entry['style']} | {entry['timestamp'][:19]} | ID: {entry['campaign_id']}")
            with c2:
                if entry.get("image_path") and __import__("os").path.exists(entry["image_path"]):
                    st.image(entry["image_path"], width=120)
