import streamlit as st
import hashlib
import time

st.set_page_config(page_title="Blockchain Simulator", layout="wide")

st.title("⛓️ မြန်မာ Blockchain Simulator")
st.write("Blockchain ဘယ်လိုအလုပ်လုပ်သလဲဆိုတာ ဒီမှာ ကိုယ်တိုင်စမ်းကြည့်ပါ!")

if 'blockchain' not in st.session_state:
    st.session_state.blockchain = [{
        'index': 0,
        'data': 'Genesis Block',
        'prev_hash': '0',
        'hash': '0000000abc123...',
        'timestamp': time.ctime()
    }]

# စာသားရိုက်ရန်
user_data = st.text_input("Block ထဲ ထည့်ချင်တဲ့ စာသားရိုက်ပါ (ဥပမာ- ငွေလွှဲစာရင်း):", "A sent 1 BTC to B")

if st.button("Block အသစ်ကို Mine လုပ်မည်"):
    prev_block = st.session_state.blockchain[-1]
    new_index = prev_block['index'] + 1
    
    # Simple Hash Calculation
    new_timestamp = time.ctime()
    raw_data = str(new_index) + user_data + prev_block['hash'] + new_timestamp
    new_hash = hashlib.sha256(raw_data.encode()).hexdigest()
    
    new_block = {
        'index': new_index,
        'data': user_data,
        'prev_hash': prev_block['hash'],
        'hash': new_hash,
        'timestamp': new_timestamp
    }
    st.session_state.blockchain.append(new_block)
    st.success(f"Block #{new_index} ကို အောင်မြင်စွာ ထည့်သွင်းပြီးပါပြီ!")

# ပြသရန်
for block in reversed(st.session_state.blockchain):
    with st.expander(f"📦 Block #{block['index']} - [Hash: {block['hash'][:15]}...]"):
        st.write(f"**အချိန်:** {block['timestamp']}")
        st.write(f"**ပါဝင်တဲ့အချက်အလက်:** {block['data']}")
        st.info(f"**ရှေ့က Block ရဲ့ Hash:** {block['prev_hash']}")
        st.warning(f"**ဒီ Block ရဲ့ Hash:** {block['hash']}")

