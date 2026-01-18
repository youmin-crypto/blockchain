import streamlit as st
import hashlib
import time

# Page Configuration
st.set_page_config(page_title="Blockchain Pro Simulator", layout="wide")

# Custom CSS for look and feel
st.markdown("""
    <style>
    .block-card { padding: 20px; border-radius: 10px; border: 2px solid #4CAF50; margin-bottom: 10px; background-color: #f0fff0; }
    .hacked-card { padding: 20px; border-radius: 10px; border: 2px solid #FF4B4B; margin-bottom: 10px; background-color: #fff0f0; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("🚀 Crypto Mate Tech")
    st.info("ဤ Tool သည် Blockchain ၏ အခြေခံသဘောတရားကို လေ့လာရန်ဖြစ်ပါသည်။")
    if st.button("Reset Blockchain"):
        st.session_state.blockchain = []
        st.rerun()

st.title("⛓️ Blockchain Educational Simulator (Myanmar)")

# Initialize Blockchain
if 'blockchain' not in st.session_state or not st.session_state.blockchain:
    genesis_block = {
        'index': 0, 'timestamp': time.ctime(), 'data': 'Genesis Block',
        'prev_hash': '0' * 64, 'nonce': 0
    }
    # Simple Hash for Genesis
    genesis_block['hash'] = hashlib.sha256(str(genesis_block).encode()).hexdigest()
    st.session_state.blockchain = [genesis_block]

# Input Section
st.subheader("➕ Block အသစ်ထည့်ရန်")
col1, col2 = st.columns([3, 1])
with col1:
    user_data = st.text_input("အရောင်းအဝယ်မှတ်တမ်း ရိုက်ထည့်ပါ:", placeholder="ဥပမာ - ကျော်ကျော်က အောင်အောင်ကို 0.5 BTC ပေးသည်")
with col2:
    if st.button("Mine New Block", use_container_width=True):
        prev_block = st.session_state.blockchain[-1]
        new_block = {
            'index': len(st.session_state.blockchain),
            'timestamp': time.ctime(),
            'data': user_data,
            'prev_hash': prev_block['hash']
        }
        new_block['hash'] = hashlib.sha256(str(new_block).encode()).hexdigest()
        st.session_state.blockchain.append(new_block)

# Display Section
st.subheader("📦 လက်ရှိ Blockchain အခြေအနေ")

def check_integrity():
    for i in range(1, len(st.session_state.blockchain)):
        if st.session_state.blockchain[i]['prev_hash'] != st.session_state.blockchain[i-1]['hash']:
            return i # Return the index where it failed
    return -1

fail_index = check_integrity()

for i, block in enumerate(st.session_state.blockchain):
    is_valid = (fail_index == -1 or i < fail_index)
    
    card_class = "block-card" if is_valid else "hacked-card"
    status_icon = "✅ Valid" if is_valid else "❌ Broken/Hacked"
    
    with st.container():
        st.markdown(f"""<div class="{card_class}">
            <h3>Block #{block['index']} ({status_icon})</h3>
            <p><b>Data:</b> {block['data']}</p>
            <p style="font-size: 0.8em; color: gray;"><b>Hash:</b> {block['hash']}</p>
            <p style="font-size: 0.8em; color: gray;"><b>Prev Hash:</b> {block['prev_hash']}</p>
        </div>""", unsafe_allow_html=True)
        
        # Hack simulation button
        if st.button(f"Edit Data of Block #{i} (Hack)", key=f"hack_{i}"):
            st.session_state.blockchain[i]['data'] = "HACKED DATA! 😈"
            # Re-calculate only this block's hash to show breakage
            st.session_state.blockchain[i]['hash'] = hashlib.sha256(str(st.session_state.blockchain[i]).encode()).hexdigest()
            st.rerun()
