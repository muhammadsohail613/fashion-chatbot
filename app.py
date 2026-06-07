import base64
import streamlit as st
from modules.chatbot import FashionChatbot

st.set_page_config(
    page_title="StyleAI — Customer Support",
    page_icon="S",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── SVG avatars (no emojis) ────────────────────────────────────────────────────
_bot_svg = b"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 36 36">
<circle cx="18" cy="18" r="18" fill="#0f1924"/>
<text x="18" y="24" text-anchor="middle" font-size="15"
  fill="#c9a84c" font-family="Georgia,serif" font-style="italic">S</text>
</svg>"""

_user_svg = b"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 36 36">
<circle cx="18" cy="18" r="18" fill="#e8e4de"/>
<text x="18" y="24" text-anchor="middle" font-size="13"
  fill="#374151" font-family="Georgia,serif">U</text>
</svg>"""

BOT_AV  = "data:image/svg+xml;base64," + base64.b64encode(_bot_svg).decode()
USER_AV = "data:image/svg+xml;base64," + base64.b64encode(_user_svg).decode()

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"]  { font-family: 'Inter', sans-serif !important; }
#MainMenu, footer           { visibility: hidden; }
.block-container { padding-top: 2rem !important; padding-bottom: 0.5rem !important; }

/* ── Sidebar ────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: #f9f8f6 !important;
    border-right: 1px solid #e4e0d9;
}
[data-testid="stSidebar"] .stButton > button {
    background: #ffffff !important;
    border: 1px solid #e4e0d9 !important;
    color: #374151 !important;
    border-radius: 7px !important;
    font-size: 12.5px !important;
    text-align: left !important;
    padding: 9px 14px !important;
    transition: all 0.18s ease !important;
    font-weight: 400 !important;
    box-shadow: none !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    border-color: #b8912a !important;
    color: #b8912a !important;
    background: #fdf8ee !important;
    padding-left: 18px !important;
    box-shadow: none !important;
}

/* ── Intent badges ──────────────────────────────────── */
.itag {
    display: inline-block;
    font-size: 10px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 8px;
}
.i-order_tracking { background:#eff6ff; color:#1d4ed8; border:1px solid #bfdbfe; }
.i-recommendation { background:#f0fdf4; color:#166534; border:1px solid #bbf7d0; }
.i-returns        { background:#fffbeb; color:#b45309; border:1px solid #fde68a; }
.i-sizing         { background:#faf5ff; color:#6d28d9; border:1px solid #ddd6fe; }
.i-shipping       { background:#f0f9ff; color:#0369a1; border:1px solid #bae6fd; }
.i-general        { background:#f8fafc; color:#475569; border:1px solid #e2e8f0; }
.i-greeting       { background:#fdf2f8; color:#9d174d; border:1px solid #fbcfe8; }

/* ── Product cards ──────────────────────────────────── */
.pcard {
    background: #ffffff;
    border: 1px solid #e8e4de;
    border-radius: 12px;
    overflow: hidden;
    transition: all 0.22s ease;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.pcard:hover {
    transform: translateY(-3px);
    border-color: #b8912a;
    box-shadow: 0 8px 22px rgba(0,0,0,0.09);
}
.pcard-header {
    height: 100px;
    display: flex;
    align-items: center;
    justify-content: center;
}
.pcard-initial {
    font-family: 'Playfair Display', serif;
    font-size: 42px;
    font-weight: 500;
    font-style: italic;
    opacity: 0.45;
    color: #1a1a2e;
}
.pcard-body        { padding: 12px 13px 14px; }
.pcard-cat         { font-size: 9px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.2px; color: #b8912a; margin-bottom: 4px; }
.pcard-name        { font-size: 13px; font-weight: 500; color: #111827; margin-bottom: 6px; line-height: 1.3; font-family: 'Playfair Display', serif !important; }
.pcard-price       { font-size: 15px; font-weight: 600; color: #0f1924; }
.pcard-orig        { font-size: 11px; color: #d1d5db; text-decoration: line-through; margin-left: 5px; }
.pcard-sale        { font-size: 9px; background: #fef2f2; color: #dc2626; padding: 2px 6px; border-radius: 3px; margin-left: 5px; font-weight: 700; letter-spacing: 0.4px; }
.pcard-stars       { color: #f59e0b; font-size: 10px; margin-top: 5px; }
.pcard-chip        { display: inline-block; font-size: 10px; padding: 2px 7px; background: #f8f7f5; border: 1px solid #e8e5e0; border-radius: 3px; color: #6b7280; margin: 2px 2px 0 0; }
.pcard-divider     { border: none; border-top: 1px solid #f5f3f0; margin: 8px 0 6px; }
.pcard-sect        { font-size: 9px; color: #c4bfb7; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 3px; }

/* ── Sidebar pills & boxes ──────────────────────────── */
.opill {
    background: #ffffff;
    border: 1px solid #e4e0d9;
    border-radius: 7px;
    padding: 8px 11px;
    margin-bottom: 5px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.sbox {
    flex: 1;
    background: #ffffff;
    border: 1px solid #e4e0d9;
    border-radius: 7px;
    padding: 10px;
    text-align: center;
}
.snum { font-size: 17px; font-weight: 600; color: #0f1924; }
.slbl { font-size: 9px; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 2px; }

/* ── Pulse dot ──────────────────────────────────────── */
.pdot {
    width: 6px; height: 6px;
    background: #10b981; border-radius: 50%;
    display: inline-block; margin-right: 5px;
    animation: blink 2s infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.35} }

[data-testid="stChatMessage"] { padding: 4px 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Constants ──────────────────────────────────────────────────────────────────
CAT_COLORS = {
    "Shirts":      ("#dbeafe", "#93c5fd"),
    "Jeans":       ("#e0e7ff", "#a5b4fc"),
    "Dresses":     ("#fce7f3", "#f9a8d4"),
    "Knitwear":    ("#fef3c7", "#fcd34d"),
    "Jackets":     ("#d1fae5", "#6ee7b7"),
    "Activewear":  ("#ede9fe", "#c4b5fd"),
    "Accessories": ("#fff7ed", "#fdba74"),
    "Trousers":    ("#e0e7ff", "#a5b4fc"),
    "Tops":        ("#f0f9ff", "#7dd3fc"),
    "Coats":       ("#f3f4f6", "#d1d5db"),
    "Shoes":       ("#fdf4ff", "#e879f9"),
    "Skirts":      ("#fdf2f8", "#f0abfc"),
}

INTENT_LABEL = {
    "order_tracking": "Order Tracking",
    "recommendation": "Recommendation",
    "returns":        "Returns & Exchanges",
    "sizing":         "Sizing Guide",
    "shipping":       "Shipping Info",
    "general":        "General",
    "greeting":       "Welcome",
}

# ── Session state ──────────────────────────────────────────────────────────────
if "chatbot"   not in st.session_state: st.session_state.chatbot   = FashionChatbot()
if "msg_count" not in st.session_state: st.session_state.msg_count = 0
if "pending"   not in st.session_state: st.session_state.pending   = None
if "messages"  not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant", "intent": "greeting", "products": [],
        "content": (
            "Welcome to **StyleAI**. I'm here to assist you with all your fashion needs.\n\n"
            "I can help you with:\n"
            "- **Order tracking** — share your Order ID, e.g. `ORD-10034`\n"
            "- **Style recommendations** — tell me your occasion, budget or preference\n"
            "- **Sizing & fit guidance** with full measurements\n"
            "- **Shipping, returns & exchange policies**\n\n"
            "How may I assist you today?"
        )
    }]

# ── Product card renderer ──────────────────────────────────────────────────────
def render_product_cards(products):
    if not products:
        return
    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    cols = st.columns(min(len(products), 3), gap="small")
    for i, p in enumerate(products):
        with cols[i]:
            bg1, bg2 = CAT_COLORS.get(p["category"], ("#f3f4f6", "#d1d5db"))
            initial  = p["category"][0]
            price    = p["sale_price"] if p["sale_price"] else p["price"]
            orig     = (
                f'<span class="pcard-orig">£{p["price"]}</span>'
                f'<span class="pcard-sale">SALE</span>'
            ) if p["sale_price"] else ""
            stars = "★" * int(p["rating"]) + "☆" * (5 - int(p["rating"]))
            chips = "".join(
                f'<span class="pcard-chip">{c}</span>' for c in p["colors"][:3]
            )
            sizes = "".join(
                f'<span class="pcard-chip">{s}</span>' for s in p["sizes"][:3]
            )
            st.markdown(f"""
            <div class="pcard">
              <div class="pcard-header"
                   style="background:linear-gradient(135deg,{bg1},{bg2}55)">
                <span class="pcard-initial">{initial}</span>
              </div>
              <div class="pcard-body">
                <div class="pcard-cat">{p["category"]}</div>
                <div class="pcard-name">{p["name"]}</div>
                <div>
                  <span class="pcard-price">£{price}</span>{orig}
                </div>
                <div class="pcard-stars">
                  {stars}&nbsp;
                  <span style="color:#9ca3af;font-size:10px">
                    {p["rating"]}/5 ({p["reviews"]} reviews)
                  </span>
                </div>
                <div class="pcard-divider"></div>
                <div class="pcard-sect">Colors</div>
                <div>{chips}</div>
                <div style="margin-top:5px">
                  <div class="pcard-sect">Sizes</div>
                  {sizes}
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:

    # Brand mark
    st.markdown("""
    <div style="padding:22px 18px 16px;border-bottom:1px solid #e4e0d9;margin-bottom:14px">
      <div style="font-family:'Playfair Display',serif;font-size:20px;
                  color:#0f1924;font-weight:600;letter-spacing:0.2px">
        StyleAI
      </div>
      <div style="font-size:9px;color:#b8912a;margin-top:3px;
                  text-transform:uppercase;letter-spacing:1.2px;font-weight:600">
        Fashion Support
      </div>
      <div style="margin-top:10px;display:flex;align-items:center">
        <span class="pdot"></span>
        <span style="font-size:11px;color:#10b981;font-weight:500">Online</span>
        <span style="font-size:11px;color:#c4bfb7;margin-left:8px">
          &middot; avg reply &lt;1s
        </span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Quick actions
    st.markdown("""
    <div style="padding:0 18px 8px">
      <div style="font-size:9px;font-weight:700;color:#b8bec9;
                  text-transform:uppercase;letter-spacing:1px;margin-bottom:8px">
        Quick Actions
      </div>
    </div>
    """, unsafe_allow_html=True)

    for label, prompt in [
        ("Track an Order",        "I'd like to track my order"),
        ("Returns & Exchanges",   "How do I return or exchange an item?"),
        ("Size Guide",            "Show me the full size guide with measurements in cm"),
        ("Shipping & Delivery",   "What are your shipping options and delivery times?"),
        ("Payment Methods",       "What payment methods do you accept?"),
        ("Sale & Promotions",     "What items are currently on sale?"),
        ("Style Recommendations", "Recommend something smart casual, budget around £80"),
        ("Ethical Sourcing",      "Are your products ethically made and sustainable?"),
    ]:
        if st.button(label, use_container_width=True):
            st.session_state.pending = prompt

    # Stats
    n = st.session_state.msg_count
    st.markdown(f"""
    <div style="padding:0 18px;margin-top:4px">
      <div style="border-top:1px solid #e4e0d9;padding-top:14px;margin-top:10px">
        <div style="font-size:9px;font-weight:700;color:#b8bec9;
                    text-transform:uppercase;letter-spacing:1px;margin-bottom:8px">
          Session
        </div>
        <div style="display:flex;gap:8px;margin-bottom:4px">
          <div class="sbox">
            <div class="snum">{n}</div>
            <div class="slbl">Messages</div>
          </div>
          <div class="sbox">
            <div class="snum" style="font-size:12px;padding-top:3px">4o-mini</div>
            <div class="slbl">Model</div>
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Sample orders
    st.markdown("""
    <div style="padding:0 18px">
      <div style="border-top:1px solid #e4e0d9;padding-top:14px;margin-top:14px">
        <div style="font-size:9px;font-weight:700;color:#b8bec9;
                    text-transform:uppercase;letter-spacing:1px;margin-bottom:8px">
          Sample Order IDs
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    for oid, status, dot_col in [
        ("ORD-10034", "Shipped",          "#10b981"),
        ("ORD-10041", "Out for Delivery", "#f59e0b"),
        ("ORD-10055", "Processing",       "#3b82f6"),
        ("ORD-10021", "Delivered",        "#059669"),
        ("ORD-10070", "Returned",         "#ef4444"),
    ]:
        st.markdown(
            f'<div style="padding:0 18px">'
            f'<div class="opill">'
            f'<span style="display:flex;align-items:center;gap:7px">'
            f'<span style="width:6px;height:6px;background:{dot_col};'
            f'border-radius:50%;display:inline-block;flex-shrink:0"></span>'
            f'<span style="font-size:11.5px;color:#374151;'
            f'font-family:monospace,monospace">{oid}</span>'
            f'</span>'
            f'<span style="font-size:11px;color:#9ca3af">{status}</span>'
            f'</div></div>',
            unsafe_allow_html=True
        )

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # New conversation button
    if st.button("New Conversation", use_container_width=True):
        st.session_state.chatbot.reset()
        st.session_state.msg_count = 0
        st.session_state.messages = [{
            "role": "assistant", "intent": "greeting", "products": [],
            "content": "Welcome back. How may I assist you today?"
        }]
        st.rerun()

    st.markdown("""
    <div style="padding:12px 18px 6px;font-size:10px;color:#c4bfb7;line-height:1.9">
      StyleAI Demo &mdash; Upwork Proposal<br>
      <span style="color:#b8912a">Powered by GPT-4o-mini</span>
    </div>
    """, unsafe_allow_html=True)

# ── Main header ────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:#ffffff;border:1px solid #e8e4de;border-radius:14px;
            padding:26px 32px;margin-bottom:20px;
            box-shadow:0 1px 4px rgba(0,0,0,0.04)">
  <div style="display:flex;align-items:flex-start;justify-content:space-between">
    <div>
      <div style="font-family:'Playfair Display',serif;font-size:24px;
                  color:#0f1924;font-weight:600;line-height:1.2;letter-spacing:0.1px">
        Customer Support
      </div>
      <div style="font-size:12px;color:#9ca3af;margin-top:5px;letter-spacing:0.2px">
        Instant answers &nbsp;&middot;&nbsp; Order tracking &nbsp;&middot;&nbsp; Product recommendations
      </div>
      <div style="margin-top:14px;display:inline-flex;border-radius:7px;
                  overflow:hidden;border:1px solid #e4e0d9">
        <div style="padding:6px 16px;background:#0f1924;color:#fff;
                    font-size:11px;font-weight:500;letter-spacing:0.3px">
          StyleAI
        </div>
        <div style="padding:6px 16px;background:#fafaf8;color:#9ca3af;
                    font-size:11px;letter-spacing:0.2px">
          Fashion &amp; Clothing
        </div>
      </div>
    </div>
    <div style="text-align:right;padding-left:20px">
      <div style="font-family:'Playfair Display',serif;font-size:40px;
                  color:#b8912a;font-weight:500;font-style:italic;
                  opacity:0.35;line-height:1">S</div>
      <div style="font-size:9px;color:#c4bfb7;text-transform:uppercase;
                  letter-spacing:1px;margin-top:4px">AI Support</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Render chat history ────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    av = BOT_AV if msg["role"] == "assistant" else USER_AV
    with st.chat_message(msg["role"], avatar=av):
        if msg["role"] == "assistant":
            intent = msg.get("intent", "general")
            label  = INTENT_LABEL.get(intent, "General")
            st.markdown(
                f'<span class="itag i-{intent}">{label}</span>',
                unsafe_allow_html=True
            )
        st.markdown(msg["content"])
        if msg.get("products"):
            render_product_cards(msg["products"])

# ── Process message ────────────────────────────────────────────────────────────
def process(user_input: str):
    st.session_state.msg_count += 1
    st.session_state.messages.append({
        "role": "user", "content": user_input, "products": []
    })
    with st.chat_message("user", avatar=USER_AV):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar=BOT_AV):
        with st.spinner(""):
            result = st.session_state.chatbot.chat(user_input)
        intent   = result["intent"]
        products = result.get("products", [])
        label    = INTENT_LABEL.get(intent, "General")

        st.markdown(
            f'<span class="itag i-{intent}">{label}</span>',
            unsafe_allow_html=True
        )
        st.markdown(result["reply"])
        if products:
            render_product_cards(products)
        st.caption(f"{label}  ·  {result['tokens']} tokens")

    st.session_state.messages.append({
        "role":     "assistant",
        "content":  result["reply"],
        "intent":   intent,
        "products": products
    })

# ── Sidebar quick-action trigger ───────────────────────────────────────────────
if st.session_state.pending:
    process(st.session_state.pending)
    st.session_state.pending = None

# ── Chat input ─────────────────────────────────────────────────────────────────
if user_input := st.chat_input("Type your question here..."):
    process(user_input)