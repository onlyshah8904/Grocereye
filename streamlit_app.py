# version 6
# streamlit_app.py
import streamlit as st
import requests
import json

# ======================
# Session State Initialization
# ======================
if "pincode" not in st.session_state:
    st.session_state.pincode = None
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "search_results" not in st.session_state:
    st.session_state.search_results = []
if "cart" not in st.session_state:
    st.session_state.cart = []
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# ======================
# Page Config
# ======================
st.set_page_config(page_title="🛒 Grocereye", layout="wide")

# Dynamic theme
if st.session_state.dark_mode:
    st.markdown("""
    <style>
        body { color: #eee; background: #1e1e1e; }
        .stApp { background: #1e1e1e; }
        .css-1d391kg { color: #eee; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛒 Grocereye")
st.markdown("Your AI-powered grocery assistant")

# ======================
# Gemini AI Response Function
# ======================
def get_gemini_response(question: str, products: list = None):
    try:
        from configs import API_KEY
        if not API_KEY.strip():
            return "❌ Gemini API Key is missing in configs.py"
    except:
        return "❌ API Key not found. Check configs.py"

    if products:
        product_list = "\n".join([
            f"- {p['name']} | {p['price']} | {p.get('quantity', 'N/A')} | {p['source']} | {p['delivery_time']}"
            for p in products[:20] if p.get("name") != "N/A"
        ])
    else:
        product_list = "(No recent products)"

    instruction = f"""
You are Grocereye, a helpful grocery assistant.
Answer based on the products below. Be concise.

Recent Products:
{product_list}

User Question: {question}

Rules:
- If asked for 'cheapest', 'fastest delivery', or a brand (e.g., Amul), use product list.
- If user asks about new items (e.g., 'milk', 'bread'), respond with: SEARCH:<item>
- If user wants to change pincode, respond with: PINCODE_CHANGE
- If user says "hungry", respond with: SEARCH:snacks, chips, biscuits, noodles
- If user mentions "making aloo ki sabji", respond with: SEARCH:potato, onion, tomato, spices, oil
- If user expresses sadness, respond with: SEARCH:chocolates, ice cream, comfort food
- If user says "party" or "celebration", respond with: SEARCH:chips, soda, cake, snacks, drinks
- Never invent products.
- Keep answers short.
"""

    headers = {
        'Content-Type': 'application/json',
        'X-goog-api-key': API_KEY,
    }

    json_data = {
        "contents": [{"parts": [{"text": instruction}]}],
        "generationConfig": {"temperature": 0.3, "maxOutputTokens": 300}
    }

    url = "https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent"

    try:
        response = requests.post(url, headers=headers, json=json_data, timeout=30)
        if response.status_code == 200:
            data = response.json()
            return data['candidates'][0]['content']['parts'][0]['text'].strip()
        else:
            return f"❌ AI Error: {response.status_code}"
    except Exception as e:
        return "❌ Cannot connect to Gemini AI. Check your internet and API key."

# ======================
# Product Search Function
# ======================
def search_products(keywords: list, pincode: str):
    all_results = []
    for kw in keywords:
        try:
            resp = requests.get(
                f"https://682d706b2f2c.ngrok-free.app/search",
                params={"keyword": kw, "pincode": pincode, "key": "K8904AI"},
                timeout=60
            )
            # all_results.append([resp.status_code])
            print(resp.status_code, resp.text)
            if resp.status_code == 200:
                data = resp.json()
                for r in data.get("results", []):
                    r["matched_keyword"] = kw
                all_results.extend(data["results"])
        except Exception as e:
            st.error(f"Request failed for '{kw}': {str(e)}")
            continue
    return all_results

# ======================
# Filter Invalid Products
# ======================
def is_valid_product(p):
    return (
        p.get("name") and p["name"] != "N/A" and
        p.get("price") and p["price"] != "N/A" and
        p.get("image_url")
    )

# ======================
# Show Product Grid with Add to Cart
# ======================
def show_product_grid(products):
    valid_products = [p for p in products if is_valid_product(p)]
    # valid_products= [p for p in products]
    if not valid_products:
        st.info(f"📭 No valid products found.{valid_products}")
        return

    st.markdown(f"### 🎉 Found {len(valid_products)} products")

    for i in range(0, len(valid_products), 3):
        cols = st.columns(3)
        for j in range(3):
            idx = i + j
            if idx >= len(valid_products):
                break
            with cols[j]:
                p = valid_products[idx]
                st.image(p["image_url"], width=100)
                st.markdown(f"**{p['name']}**")
                st.markdown(f"💰 {p['price']}")
                if p.get("mrp") and p["mrp"] != "N/A":
                    st.markdown(f"~~{p['mrp']}~~")
                if p.get("quantity") and p["quantity"] != "N/A":
                    st.markdown(f"📦 {p['quantity']}")
                if p.get("delivery_time") and p["delivery_time"] != "N/A":
                    st.markdown(f"🚚 {p['delivery_time']}")
                source = p["source"].split()[0]
                st.markdown(f"[View on {source} 🛒]({p['url']})", unsafe_allow_html=True)

    return valid_products

# ======================
# Sidebar: Pincode & Controls
# ======================
with st.sidebar:
    st.header("📍 Delivery Location")

    if st.session_state.pincode:
        st.write(f"**Current Pincode:** `{st.session_state.pincode}`")
        if st.button("🔄 Change Pincode"):
            st.session_state.pincode = None
            st.session_state.search_results = []
            st.session_state.chat_messages = []
            st.session_state.cart = []
            st.rerun()
    else:
        pincode_input = st.text_input("Enter 6-digit pincode:", max_chars=6)
        if st.button("Set Pincode"):
            if not pincode_input.isdigit() or len(pincode_input) != 6:
                st.error("❌ Enter a valid 6-digit pincode.")
            else:
                with st.spinner("Setting location..."):
                    try:
                        resp = requests.post(
                            f"https://682d706b2f2c.ngrok-free.app/init-location",
                            params={"pincode": pincode_input, "key": "K8904AI"}
                        )
                        if resp.status_code == 200:
                            st.session_state.pincode = pincode_input
                            st.success("✅ Location set!")
                            st.rerun()
                        else:
                            st.error(f"❌ Failed: {resp.status_code}")
                    except Exception as e:
                        st.error("⚠️ Cannot connect to API.")
    # Chat history
    st.header("💬 Chat History")
    for msg in st.session_state.chat_messages[-10:]:
        role = "👤" if msg["role"] == "user" else "🤖"
        st.markdown(f"{role} {msg['content'][:30]}...")

    if st.button("🧹 Clear Chat"):
        st.session_state.chat_messages = []
        st.session_state.search_results = []
        st.rerun()

# ======================
# Chat Interface
# ======================
for msg in st.session_state.chat_messages:
    with st.chat_message(msg["role"]):
        content = msg["content"]
        if content.startswith("PRODUCTS:"):
            if "for '" in content:
                query = content.split("for '")[1].split("'")[0]
            elif 'for "' in content:
                query = content.split('for "')[1].split('"')[0]
            else:
                query = "this search"
            st.markdown(f"🔍 Showing results for: **{query}**")
            show_product_grid(st.session_state.search_results)
        else:
            st.write(content)

# Chat input
if prompt := st.chat_input("Ask for groceries or set pincode..."):
    if not st.session_state.pincode:
        st.error("Please set pincode first in the sidebar.")
    else:
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            ai_resp = get_gemini_response(prompt, st.session_state.search_results)

            if ai_resp.startswith("SEARCH:"):
                keyword = ai_resp.replace("SEARCH:", "").strip().split()[0]
                st.write(f"🔍 Searching for '{keyword}'...")

                try:
                    kw_resp = requests.get(
                        f"https://682d706b2f2c.ngrok-free.app/keywords?query={keyword}"
                    )
                    keywords = kw_resp.json().get("keywords", [keyword]) if kw_resp.status_code == 200 else [keyword]
                except:
                    keywords = [keyword]
                # st.write(kw_resp.status_code, kw_resp.text, st.session_state.pincode,ai_resp)
                results = search_products(keywords, st.session_state.pincode)
                st.session_state.search_results = results
                show_product_grid(results)
                msg = f"PRODUCTS: Showing results for '{keyword}'"

            elif ai_resp == "PINCODE_CHANGE":
                st.session_state.pincode = None
                st.session_state.search_results = []
                st.session_state.chat_messages = st.session_state.chat_messages[:-1]
                st.rerun()
            else:
                st.write(ai_resp)
                msg = ai_resp

            st.session_state.chat_messages.append({"role": "assistant", "content": msg})