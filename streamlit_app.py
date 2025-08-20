# import streamlit as st
# import requests

# st.set_page_config(page_title="🛒 Grocereye", layout="centered")

# st.title("🛒 Grocereye")
# st.markdown("Your AI-powered grocery assistant")

# # State
# if "pincode" not in st.session_state:
#     st.session_state.pincode = None

# # Step 1: Set Pincode
# if not st.session_state.pincode:
#     st.subheader("📍 Set Your Delivery Location")
#     pincode_input = st.text_input("Enter your pincode:", placeholder="e.g., 380007")
#     if st.button("Set Location"):
#         if not pincode_input.strip():
#             st.error("Pincode is required")
#         else:
#             with st.spinner("Setting location..."):
#                 try:
#                     resp = requests.post(f"https://60b0f2190f07.ngrok-free.app/init-location?pincode={pincode_input}")
#                     if resp.status_code == 200:
#                         st.session_state.pincode = pincode_input
#                         st.success(f"✅ Location set: {pincode_input}")
#                         st.rerun()
#                     else:
#                         st.error("Failed to set location.")
#                 except Exception as e:
#                     print(e)
#                     st.error("❌ Cannot connect to API. Is `python api.py` running?")

# # Step 2: Search
# else:
#     st.success(f"📍 Active Pincode: {st.session_state.pincode}")
#     if st.button("⬅️ Change Pincode"):
#         st.session_state.pincode = None
#         st.rerun()

#     st.subheader("🛍️ What do you need?")
#     user_query = st.text_input("Describe your need:", placeholder="e.g., I want milk and bread")

#     if st.button("🔍 Find Products"):
#         if not user_query.strip():
#             st.warning("Please enter a query.")
#         else:
#             with st.spinner("🧠 Understanding your needs..."):
#                 try:
#                     # Get keywords
#                     kw_resp = requests.get(f"https://60b0f2190f07.ngrok-free.app/keywords?query={requests.utils.quote(user_query)}")
#                     if kw_resp.status_code != 200:
#                         st.error("Failed to understand your query.")
#                         st.stop()
#                     keywords = kw_resp.json().get("keywords", [])
#                     if not keywords:
#                         st.info("No relevant products found.")
#                         st.stop()

#                     st.markdown(f"**🔍 Searching for:** {', '.join(keywords)}")

#                     # Search for all keywords
#                     all_results = []
#                     for kw in keywords:
#                         with st.spinner(f"Searching for '{kw}'..."):
#                             search_resp = requests.get(
#                                 f"https://60b0f2190f07.ngrok-free.app/search?keyword={kw}&pincode={st.session_state.pincode}"
#                             )
#                             if search_resp.status_code == 200:
#                                 data = search_resp.json()
#                                 for r in data["results"]:
#                                     r["matched_keyword"] = kw
#                                 all_results.extend(data["results"])

#                     # Filter out invalid results (all N/A)
#                     def is_valid_product(p):
#                         return not (
#                             p.get("name") == "N/A" and
#                             p.get("price") == "N/A" and
#                             not p.get("image_url")
#                         )

#                     valid_results = [r for r in all_results if is_valid_product(r)]

#                     if not valid_results:
#                         st.info("📭 No valid products found.")
#                     else:
#                         st.markdown(f"### 🎉 Found {len(valid_results)} products")

#                         # Show 3 per row
#                         for i in range(0, len(valid_results), 3):
#                             cols = st.columns(3)
#                             for j in range(3):
#                                 idx = i + j
#                                 if idx >= len(valid_results):
#                                     break
#                                 with cols[j]:
#                                     product = valid_results[idx]
#                                     if product.get("image_url"):
#                                         st.image(product["image_url"], width=100)
#                                     st.markdown(f"**{product['name']}**")
#                                     st.markdown(f"💰 {product['price']}")
#                                     if product.get("mrp") and product["mrp"] != "N/A":
#                                         st.markdown(f"~~{product['mrp']}~~")
#                                     if product.get("quantity") and product["quantity"] != "N/A":
#                                         st.markdown(f"📦 {product['quantity']}")
#                                     if product.get("delivery_time") and product["delivery_time"] != "N/A":
#                                         st.markdown(f"🚚 {product['delivery_time']}")
#                                     st.markdown(f"[View on {product['source']} 🛒]({product['url']})", unsafe_allow_html=True)

#                 except Exception as e:
#                     st.error(f"Search failed: {str(e)}")

# streamlit_app.py
import streamlit as st
import requests
import json
from datetime import datetime



def get_gemini_response(question: str, products: list) -> str:
    from configs import API_KEY
    import requests as http_requests

    # Truncate if too many products
    if len(products) > 50:
        products = products[:50]

    instruction = f"""
You are a smart grocery assistant. Answer the user's question based ONLY on the product list below.
Be concise and helpful.

Product List:
{json.dumps(products, indent=2)}

User Question: {question}

Rules:
- If asked for cheapest, find lowest price.
- If asked for fastest delivery, find shortest delivery time.
- If asked for brand (e.g., Amul), filter by name.
- If no product matches, say so.
- Never make up products.
- Return only the answer.
"""

    headers = {
        'Content-Type': 'application/json',
        'X-goog-api-key': API_KEY,
    }

    json_data = {
        "contents": [{"parts": [{"text": instruction}]}]
    }

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

    try:
        response = http_requests.post(url, headers=headers, json=json_data)
        if response.status_code == 200:
            data = response.json()
            return data['candidates'][0]['content']['parts'][0]['text'].strip()
        else:
            return "Sorry, I couldn't fetch an answer right now."
    except Exception as e:
        return "Sorry, I'm having trouble connecting to the AI."


# Page config
st.set_page_config(page_title="🛒 Grocereye", layout="wide")

# Session state
if "pincode" not in st.session_state:
    st.session_state.pincode = None
if "search_results" not in st.session_state:
    st.session_state.search_results = []
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# Title
st.title("🛒 Grocereye")
st.markdown("Your AI-powered grocery assistant")

# Sidebar Chat (only if results exist)
with st.sidebar:
    st.header("💬 Ask About Products")
    if not st.session_state.search_results:
        st.write("Search for products to start chatting.")
    else:
        # Show chat
        for msg in st.session_state.chat_messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        # Input
        if prompt := st.chat_input("Ask about the products..."):
            st.session_state.chat_messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        # Prepare context from search results
                        context = [
                            {
                                "name": p["name"],
                                "price": p["price"],
                                "mrp": p["mrp"],
                                "quantity": p["quantity"],
                                "source": p["source"],
                                "delivery_time": p["delivery_time"],
                                "url": p["url"]
                            }
                            for p in st.session_state.search_results
                        ]

                        # Call Gemini
                        response = get_gemini_response(prompt, context)
                        st.write(response)
                        st.session_state.chat_messages.append({"role": "assistant", "content": response})
                    except Exception as e:
                        error_msg = "Sorry, I couldn't process your request."
                        st.write(error_msg)
                        st.session_state.chat_messages.append({"role": "assistant", "content": error_msg})

# === Main Flow ===

# Step 1: Set Pincode
if not st.session_state.pincode:
    st.subheader("📍 Set Your Delivery Location")
    pincode_input = st.text_input("Enter your pincode:", placeholder="e.g., 380007")
    if st.button("Set Location"):
        if not pincode_input.strip():
            st.error("Pincode is required")
        else:
            with st.spinner("Setting location..."):
                try:
                    resp = requests.post(f"https://28b7c00f2207.ngrok-free.app/init-location?pincode={pincode_input}")
                    if resp.status_code == 200:
                        st.session_state.pincode = pincode_input
                        st.success(f"✅ Location set: {pincode_input}")
                        st.rerun()
                    else:
                        st.error("Failed to set location.")
                except:
                    st.error("❌ Cannot connect to API. Is `python api.py` running?")
else:
    st.success(f"📍 Active Pincode: {st.session_state.pincode}")
    if st.button("⬅️ Change Pincode"):
        st.session_state.pincode = None
        st.session_state.search_results = []
        st.session_state.chat_messages = []
        st.rerun()

    st.subheader("🛍️ What do you need?")
    user_query = st.text_input("Describe your need:", placeholder="e.g., I want milk and bread")

    if st.button("🔍 Find Products"):
        if not user_query.strip():
            st.warning("Please enter a query.")
        else:
            with st.spinner("🧠 Understanding your needs..."):
                try:
                    # Reset results
                    st.session_state.search_results = []
                    st.session_state.chat_messages = []

                    # Get keywords
                    kw_resp = requests.get(f"https://28b7c00f2207.ngrok-free.app/keywords?query={requests.utils.quote(user_query)}")
                    if kw_resp.status_code != 200:
                        st.error("Failed to understand your query.")
                        st.stop()
                    keywords = kw_resp.json().get("keywords", [])
                    if not keywords:
                        st.info("No relevant products found.")
                        st.stop()

                    st.markdown(f"**🔍 Searching for:** {', '.join(keywords)}")

                    # Search for all keywords
                    all_results = []
                    for kw in keywords:
                        with st.spinner(f"Searching for '{kw}'..."):
                            search_resp = requests.get(
                                f"https://28b7c00f2207.ngrok-free.app/search?keyword={kw}&pincode={st.session_state.pincode}"
                            )
                            if search_resp.status_code == 200:
                                data = search_resp.json()
                                for r in data["results"]:
                                    r["matched_keyword"] = kw
                                all_results.extend(data["results"])

                    # Filter invalid results
                    def is_valid_product(p):
                        return not (
                            p.get("name") == "N/A" and
                            p.get("price") == "N/A" and
                            not p.get("image_url")
                        )

                    valid_results = [r for r in all_results if is_valid_product(r)]
                    st.session_state.search_results = valid_results  # Save for chat

                    if not valid_results:
                        st.info("📭 No valid products found.")
                    else:
                        st.markdown(f"### 🎉 Found {len(valid_results)} products")

                        # Show 3 per row
                        for i in range(0, len(valid_results), 3):
                            cols = st.columns(3)
                            for j in range(3):
                                idx = i + j
                                if idx >= len(valid_results):
                                    break
                                with cols[j]:
                                    product = valid_results[idx]
                                    if product.get("image_url"):
                                        st.image(product["image_url"], width=100)
                                    st.markdown(f"**{product['name']}**")
                                    st.markdown(f"💰 {product['price']}")
                                    if product.get("mrp") and product["mrp"] != "N/A":
                                        st.markdown(f"~~{product['mrp']}~~")
                                    if product.get("quantity") and product["quantity"] != "N/A":
                                        st.markdown(f"📦 {product['quantity']}")
                                    if product.get("delivery_time") and product["delivery_time"] != "N/A":
                                        st.markdown(f"🚚 {product['delivery_time']}")
                                    source = product["source"].split()[0]
                                    st.markdown(f"[View on {source} 🛒]({product['url']})", unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Search failed: {str(e)}")


# === Gemini Chat Function ===
