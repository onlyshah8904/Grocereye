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


# VERSION 2
# streamlit_app.py
# import streamlit as st
# import requests
# import json
# from datetime import datetime



# def get_gemini_response(question: str, products: list) -> str:
#     from configs import API_KEY
#     import requests as http_requests

#     # Truncate if too many products
#     if len(products) > 50:
#         products = products[:50]

#     instruction = f"""
# You are a smart grocery assistant. Answer the user's question based ONLY on the product list below.
# Be concise and helpful.

# Product List:
# {json.dumps(products, indent=2)}

# User Question: {question}

# Rules:
# - If asked for cheapest, find lowest price.
# - If asked for fastest delivery, find shortest delivery time.
# - If asked for brand (e.g., Amul), filter by name.
# - If no product matches, say so.
# - Never make up products.
# - Return only the answer.
# """

#     headers = {
#         'Content-Type': 'application/json',
#         'X-goog-api-key': API_KEY,
#     }

#     json_data = {
#         "contents": [{"parts": [{"text": instruction}]}]
#     }

#     url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

#     try:
#         response = http_requests.post(url, headers=headers, json=json_data)
#         if response.status_code == 200:
#             data = response.json()
#             return data['candidates'][0]['content']['parts'][0]['text'].strip()
#         else:
#             return "Sorry, I couldn't fetch an answer right now."
#     except Exception as e:
#         return "Sorry, I'm having trouble connecting to the AI."


# # Page config
# st.set_page_config(page_title="🛒 Grocereye", layout="wide")

# # Session state
# if "pincode" not in st.session_state:
#     st.session_state.pincode = None
# if "search_results" not in st.session_state:
#     st.session_state.search_results = []
# if "chat_messages" not in st.session_state:
#     st.session_state.chat_messages = []

# # Title
# st.title("🛒 Grocereye")
# st.markdown("Your AI-powered grocery assistant")

# # Sidebar Chat (only if results exist)
# with st.sidebar:
#     st.header("💬 Ask About Products")
#     if not st.session_state.search_results:
#         st.write("Search for products to start chatting.")
#     else:
#         # Show chat
#         for msg in st.session_state.chat_messages:
#             with st.chat_message(msg["role"]):
#                 st.write(msg["content"])

#         # Input
#         if prompt := st.chat_input("Ask about the products..."):
#             st.session_state.chat_messages.append({"role": "user", "content": prompt})
#             with st.chat_message("user"):
#                 st.write(prompt)

#             # Get AI response
#             with st.chat_message("assistant"):
#                 with st.spinner("Thinking..."):
#                     try:
#                         # Prepare context from search results
#                         context = [
#                             {
#                                 "name": p["name"],
#                                 "price": p["price"],
#                                 "mrp": p["mrp"],
#                                 "quantity": p["quantity"],
#                                 "source": p["source"],
#                                 "delivery_time": p["delivery_time"],
#                                 "url": p["url"]
#                             }
#                             for p in st.session_state.search_results
#                         ]

#                         # Call Gemini
#                         response = get_gemini_response(prompt, context)
#                         st.write(response)
#                         st.session_state.chat_messages.append({"role": "assistant", "content": response})
#                     except Exception as e:
#                         error_msg = "Sorry, I couldn't process your request."
#                         st.write(error_msg)
#                         st.session_state.chat_messages.append({"role": "assistant", "content": error_msg})

# # === Main Flow ===

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
#                     resp = requests.post(f"https://28b7c00f2207.ngrok-free.app/init-location?pincode={pincode_input}")
#                     if resp.status_code == 200:
#                         st.session_state.pincode = pincode_input
#                         st.success(f"✅ Location set: {pincode_input}")
#                         st.rerun()
#                     else:
#                         st.error("Failed to set location.")
#                 except Exception as e:
#                     print(e)
#                     st.error("❌ Cannot connect to API. Is `python api.py` running?")
# else:
#     st.success(f"📍 Active Pincode: {st.session_state.pincode}")
#     if st.button("⬅️ Change Pincode"):
#         st.session_state.pincode = None
#         st.session_state.search_results = []
#         st.session_state.chat_messages = []
#         st.rerun()

#     st.subheader("🛍️ What do you need?")
#     user_query = st.text_input("Describe your need:", placeholder="e.g., I want milk and bread")

#     if st.button("🔍 Find Products"):
#         if not user_query.strip():
#             st.warning("Please enter a query.")
#         else:
#             with st.spinner("🧠 Understanding your needs..."):
#                 try:
#                     # Reset results
#                     st.session_state.search_results = []
#                     st.session_state.chat_messages = []

#                     # Get keywords
#                     kw_resp = requests.get(f"https://28b7c00f2207.ngrok-free.app/keywords?query={requests.utils.quote(user_query)}")
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
#                                 f"https://28b7c00f2207.ngrok-free.app/search?keyword={kw}&pincode={st.session_state.pincode}"
#                             )
#                             if search_resp.status_code == 200:
#                                 data = search_resp.json()
#                                 for r in data["results"]:
#                                     r["matched_keyword"] = kw
#                                 all_results.extend(data["results"])

#                     # Filter invalid results
#                     def is_valid_product(p):
#                         return not (
#                             p.get("name") == "N/A" and
#                             p.get("price") == "N/A" and
#                             not p.get("image_url")
#                         )

#                     valid_results = [r for r in all_results if is_valid_product(r)]
#                     st.session_state.search_results = valid_results  # Save for chat

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
#                                     source = product["source"].split()[0]
#                                     st.markdown(f"[View on {source} 🛒]({product['url']})", unsafe_allow_html=True)

#                 except Exception as e:
#                     st.error(f"Search failed: {str(e)}")


# # === Gemini Chat Function ===




# VERSION 3

# streamlit_app.py
# import streamlit as st
# import requests
# import json
# from datetime import datetime

# # Page config
# st.set_page_config(page_title="🛒 Grocereye", layout="wide")

# # Session state initialization
# if "pincode" not in st.session_state:
#     st.session_state.pincode = None
# if "search_results" not in st.session_state:
#     st.session_state.search_results = []
# if "chat_messages" not in st.session_state:
#     st.session_state.chat_messages = []
# if "last_query" not in st.session_state:
#     st.session_state.last_query = ""

# # Title
# st.title("🛒 Grocereye")
# st.markdown("Your AI-powered grocery assistant")

# # === Gemini Chat Function ===
# def get_gemini_response(question: str, products: list = None) -> str:
#     from configs import API_KEY
#     import requests as http_requests

#     # Build context
#     if products and len(products) > 0:
#         product_context = "\n".join([
#             f"- {p['name']} | {p['price']} | {p.get('quantity', 'N/A')} | {p['source']} | {p['delivery_time']}"
#             for p in products
#         ])
#     else:
#         product_context = "(No recent products found)"

#     instruction = f"""
# You are Grocereye, a friendly and smart grocery assistant. Help the user with:
# - Answering questions about recently shown products
# - Suggesting groceries based on meals, diet, occasion
# - Comparing prices, delivery time
# - Giving healthy/economical alternatives

# Rules:
# - Be helpful, short, and clear.
# - If asked for "cheapest", "fastest", or "Amul", use product list.
# - If no products match, say so.
# - For suggestions (e.g., breakfast), suggest 3-5 real grocery items.
# - Never invent products or prices.
# - Use emojis sparingly.

# Recent Products:
# {product_context}

# User Question: {question}
# """

#     headers = {
#         'Content-Type': 'application/json',
#         'X-goog-api-key': API_KEY,
#     }

#     json_data = {
#         "contents": [{"parts": [{"text": instruction}]}],
#         "generationConfig": {
#             "temperature": 0.4,
#             "topP": 0.9,
#             "maxOutputTokens": 300
#         }
#     }

#     url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

#     try:
#         response = http_requests.post(url, headers=headers, json=json_data)
#         if response.status_code == 200:
#             data = response.json()
#             return data['candidates'][0]['content']['parts'][0]['text'].strip()
#         else:
#             return "I'm having trouble connecting to the AI right now. Please try again."
#     except Exception as e:
#         return "Sorry, I can't reach the AI. Check your Gemini API key."

# # === Sidebar: Chat History & Input ===
# with st.sidebar:
#     st.header("💬 Grocery Assistant")
#     st.caption("Ask anything about groceries!")

#     # Display chat history
#     for msg in st.session_state.chat_messages:
#         with st.chat_message(msg["role"]):
#             st.write(msg["content"])

#     # Chat input
#     if prompt := st.chat_input("Ask anything about groceries..."):
#         # Add user message
#         st.session_state.chat_messages.append({"role": "user", "content": prompt})

#         # Show immediately
#         with st.chat_message("user"):
#             st.write(prompt)

#         # Get AI response
#         with st.chat_message("assistant"):
#             with st.spinner("Thinking..."):
#                 response = get_gemini_response(
#                     question=prompt,
#                     products=st.session_state.search_results
#                 )
#                 st.write(response)
#                 st.session_state.chat_messages.append({"role": "assistant", "content": response})

# # === Main: Pincode & Search ===

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
#                     resp = requests.post(f"https://28b7c00f2207.ngrok-free.app/init-location?pincode={pincode_input}")
#                     if resp.status_code == 200:
#                         st.session_state.pincode = pincode_input
#                         st.success(f"✅ Location set: {pincode_input}")
#                         st.rerun()
#                     else:
#                         st.error("Failed to set location.")
#                 except Exception as e:
#                     print(e)
#                     st.error("❌ Cannot connect to API. Is `python api.py` running?")
# else:
#     st.success(f"📍 Active Pincode: {st.session_state.pincode}")
#     if st.button("⬅️ Change Pincode"):
#         st.session_state.pincode = None
#         st.session_state.search_results = []
#         st.session_state.chat_messages = []
#         st.session_state.last_query = ""
#         st.rerun()

#     st.subheader("🛍️ What do you need?")
#     user_query = st.text_input("Describe your need:", value=st.session_state.last_query, placeholder="e.g., I want milk and bread")

#     if st.button("🔍 Find Products"):
#         if not user_query.strip():
#             st.warning("Please enter a query.")
#         else:
#             # Save query
#             st.session_state.last_query = user_query

#             # Reset results (keep chat)
#             st.session_state.search_results = []

#             with st.spinner("🧠 Understanding your needs..."):
#                 try:
#                     # Get keywords
#                     kw_resp = requests.get(f"https://28b7c00f2207.ngrok-free.app/keywords?query={requests.utils.quote(user_query)}")
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
#                                 f"https://28b7c00f2207.ngrok-free.app/search?keyword={kw}&pincode={st.session_state.pincode}"
#                             )
#                             if search_resp.status_code == 200:
#                                 data = search_resp.json()
#                                 for r in data["results"]:
#                                     r["matched_keyword"] = kw
#                                 all_results.extend(data["results"])

#                     # Filter invalid
#                     def is_valid_product(p):
#                         return not (p.get("name") == "N/A" and p.get("price") == "N/A" and not p.get("image_url"))
#                     valid_results = [r for r in all_results if is_valid_product(r)]
#                     st.session_state.search_results = valid_results

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
#                                     source = product["source"].split()[0]
#                                     st.markdown(f"[View on {source} 🛒]({product['url']})", unsafe_allow_html=True)

#                 except Exception as e:
#                     st.error(f"Search failed: {str(e)}")

# # === Optional: Add "Clear Chat" button
# with st.sidebar:
#     st.markdown("---")
#     if st.button("🗑️ Clear Chat"):
#         st.session_state.chat_messages = []
#         st.rerun()



# VERSION 4

# streamlit_app.py
# streamlit_app.py
# import streamlit as st
# import requests
# import json

# # ======================
# # Session State Initialization
# # ======================
# if "pincode" not in st.session_state:
#     st.session_state.pincode = None
# if "search_results" not in st.session_state:
#     st.session_state.search_results = []
# if "chat_messages" not in st.session_state:
#     st.session_state.chat_messages = []
# if "last_query" not in st.session_state:
#     st.session_state.last_query = ""

# # ======================
# # Page Config
# # ======================
# st.set_page_config(page_title="🛒 Grocereye", layout="wide")
# st.title("🛒 Grocereye")
# st.markdown("Your AI-powered grocery assistant")

# # ======================
# # Gemini AI Response Function
# # ======================
# def get_gemini_response(question: str, products: list):
#     from configs import API_KEY
#     import requests as http_requests

#     # Build context
#     if products:
#         product_context = "\n".join([
#             f"- {p['name']} | {p['price']} | {p.get('quantity', 'N/A')} | {p['source']} | {p['delivery_time']}"
#             for p in products
#         ])
#     else:
#         product_context = "(No recent products)"

#     instruction = f"""
# You are Grocereye, a helpful grocery assistant.
# Answer based on the products below. Be concise.
# also tell about calories and any other thing about any product if asked

# Recent Products:
# {product_context}

# User Question: {question}

# Rules:
# - For 'cheapest', find lowest price.
# - For 'fastest delivery', check delivery_time.
# - For brands like 'Amul', filter by name.
# - For suggestions, recommend 3-5 real grocery items.
# - Never invent products.
# """

#     headers = {
#         'Content-Type': 'application/json',
#         'X-goog-api-key': API_KEY,
#     }

#     json_data = {
#         "contents": [{"parts": [{"text": instruction}]}],
#         "generationConfig": {"temperature": 0.4, "maxOutputTokens": 300}
#     }

#     url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

#     try:
#         response = http_requests.post(url, headers=headers, json=json_data)
#         if response.status_code == 200:
#             data = response.json()
#             return data['candidates'][0]['content']['parts'][0]['text'].strip()
#         else:
#             return "I'm having trouble connecting to the AI."
#     except Exception as e:
#         return "Sorry, I can't reach the AI right now."

# # ======================
# # Sidebar: Chat (Persistent)
# # ======================
# with st.sidebar:
#     st.header("💬 Grocery Assistant")
#     st.caption("Ask about products or get suggestions!")

#     # Display chat messages
#     for msg in st.session_state.chat_messages:
#         with st.chat_message(msg["role"]):
#             st.write(msg["content"])

#     # Chat input
#     if prompt := st.chat_input("Ask about groceries..."):
#         # Add user message
#         st.session_state.chat_messages.append({"role": "user", "content": prompt})

#         # Show instantly
#         with st.chat_message("user"):
#             st.write(prompt)

#         # Get AI response
#         with st.chat_message("assistant"):
#             with st.spinner("Thinking..."):
#                 response = get_gemini_response(prompt, st.session_state.search_results)
#                 st.write(response)
#                 st.session_state.chat_messages.append({"role": "assistant", "content": response})

#     # Clear chat
#     if st.button("🗑️ Clear Chat"):
#         st.session_state.chat_messages = []
#         st.rerun()

# # ======================
# # Main: Pincode & Search
# # ======================

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
#                     resp = requests.post(f"https://28b7c00f2207.ngrok-free.app/init-location?pincode={pincode_input}")
#                     if resp.status_code == 200:
#                         st.session_state.pincode = pincode_input
#                         st.success(f"✅ Location set: {pincode_input}")
#                         st.rerun()
#                     else:
#                         st.error("Failed to set location.")
#                 except Exception as e:
#                     print(e)
#                     st.error("❌ Cannot connect to API. Is `python api.py` running?")
# else:
#     st.success(f"📍 Active Pincode: {st.session_state.pincode}")
#     if st.button("⬅️ Change Pincode"):
#         st.session_state.pincode = None
#         st.session_state.search_results = []
#         st.session_state.chat_messages = []
#         st.session_state.last_query = ""
#         st.rerun()

#     st.subheader("🛍️ What do you need?")
#     user_query = st.text_input("Describe your need:", value=st.session_state.last_query, placeholder="e.g., I want milk and bread")

#     if st.button("🔍 Find Products"):
#         st.session_state.last_query = user_query
#         with st.spinner("🧠 Understanding your needs..."):
#             try:
#                 # Fetch keywords
#                 kw_resp = requests.get(f"https://28b7c00f2207.ngrok-free.app/keywords?query={requests.utils.quote(user_query)}")
#                 if kw_resp.status_code != 200:
#                     st.error("Failed to understand your query.")
#                 else:
#                     keywords = kw_resp.json().get("keywords", [])
#                     if not keywords:
#                         st.info("No relevant products found.")
#                     else:
#                         st.markdown(f"**🔍 Searching for:** {', '.join(keywords)}")

#                         all_results = []
#                         for kw in keywords:
#                             with st.spinner(f"Searching for '{kw}'..."):
#                                 search_resp = requests.get(
#                                     f"https://28b7c00f2207.ngrok-free.app/search?keyword={kw}&pincode={st.session_state.pincode}"
#                                 )
#                                 if search_resp.status_code == 200:
#                                     data = search_resp.json()
#                                     for r in data["results"]:
#                                         r["matched_keyword"] = kw
#                                     all_results.extend(data["results"])

#                         # Filter invalid
#                         def is_valid_product(p):
#                             return not (p.get("name") == "N/A" and p.get("price") == "N/A" and not p.get("image_url"))
#                         valid_results = [r for r in all_results if is_valid_product(r)]
#                         st.session_state.search_results = valid_results  # ✅ Save to session state

#                         if not valid_results:
#                             st.info("📭 No valid products found.")
#                         else:
#                             st.markdown(f"### 🎉 Found {len(valid_results)} products")

#             except Exception as e:
#                 st.error(f"Search failed: {str(e)}")

# # ======================
# # ✅ Always Render Products (Even After Chat)
# # ======================
# if st.session_state.search_results:
#     # Show products in 3-column grid
#     for i in range(0, len(st.session_state.search_results), 3):
#         cols = st.columns(3)
#         for j in range(3):
#             idx = i + j
#             if idx >= len(st.session_state.search_results):
#                 break
#             with cols[j]:
#                 product = st.session_state.search_results[idx]
#                 if product.get("image_url"):
#                     st.image(product["image_url"], width=100)
#                 st.markdown(f"**{product['name']}**")
#                 st.markdown(f"💰 {product['price']}")
#                 if product.get("mrp") and product["mrp"] != "N/A":
#                     st.markdown(f"~~{product['mrp']}~~")
#                 if product.get("quantity") and product["quantity"] != "N/A":
#                     st.markdown(f"📦 {product['quantity']}")
#                 if product.get("delivery_time") and product["delivery_time"] != "N/A":
#                     st.markdown(f"🚚 {product['delivery_time']}")
#                 source = product["source"].split()[0]
#                 st.markdown(f"[View on {source} 🛒]({product['url']})", unsafe_allow_html=True)



# version 5
# streamlit_app.py
# streamlit_app.py
# # streamlit_app.py
# import streamlit as st
# import requests
# import json

# # ======================
# # Session State Initialization
# # ======================
# if "pincode" not in st.session_state:
#     st.session_state.pincode = None
# if "chat_messages" not in st.session_state:
#     st.session_state.chat_messages = []
# if "search_results" not in st.session_state:
#     st.session_state.search_results = []

# # ======================
# # Page Config
# # ======================
# st.set_page_config(page_title="🛒 Grocereye", layout="wide")
# st.title("🛒 Grocereye")
# st.markdown("Your AI-powered grocery assistant")

# # ======================
# # Gemini AI Response Function
# # ======================
# def get_gemini_response(question: str, products: list = None):
#     try:
#         from configs import API_KEY
#         if not API_KEY.strip():
#             return "❌ Gemini API Key is missing in configs.py"
#     except:
#         return "❌ API Key not found. Check configs.py"

#     # Build product context
#     if products:
#         product_list = "\n".join([
#             f"- {p['name']} | {p['price']} | {p.get('quantity', 'N/A')} | {p['source']} | {p['delivery_time']}"
#             for p in products[:20] if p.get("name") != "N/A"
#         ])
#     else:
#         product_list = "(No recent products)"

#     instruction = f"""
# You are Grocereye, a helpful grocery assistant.
# Answer based on the products below. Be concise.

# Recent Products:
# {product_list}

# User Question: {question}

# Rules:
# - If asked for 'cheapest', 'fastest delivery', or a brand (e.g., Amul), use product list.
# - If user asks about new items (e.g., 'milk', 'bread'), respond with: SEARCH:<item>
# - If user wants to change pincode, respond with: PINCODE_CHANGE
# - Never invent products.
# - Keep answers short.
# """

#     headers = {
#         'Content-Type': 'application/json',
#         'X-goog-api-key': API_KEY,
#     }

#     json_data = {
#         "contents": [{"parts": [{"text": instruction}]}],
#         "generationConfig": {"temperature": 0.3, "maxOutputTokens": 300}
#     }

#     url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

#     try:
#         response = requests.post(url, headers=headers, json=json_data, timeout=30)
#         if response.status_code == 200:
#             data = response.json()
#             return data['candidates'][0]['content']['parts'][0]['text'].strip()
#         else:
#             return f"❌ AI Error: {response.status_code}"
#     except Exception as e:
#         return "❌ Cannot connect to Gemini AI. Check your internet and API key."

# # ======================
# # Product Search Function (Uses ngrok)
# # ======================
# def search_products(keywords: list, pincode: str):
#     all_results = []
#     for kw in keywords:
#         try:
#             # 🔥 Use your ngrok URL
#             resp = requests.get(
#                 f"https://28b7c00f2207.ngrok-free.app/search",
#                 params={"keyword": kw, "pincode": pincode, "key": "K8904AI"},
#                 timeout=60
#             )
#             if resp.status_code == 200:
#                 data = resp.json()
#                 for r in data.get("results", []):
#                     r["matched_keyword"] = kw
#                 all_results.extend(data["results"])
#             else:
#                 st.warning(f"Search failed for '{kw}': {resp.status_code}")
#         except Exception as e:
#             st.error(f"Request failed for '{kw}': {str(e)}")
#             continue
#     return all_results

# # ======================
# # Show Product Grid
# # ======================
# def show_product_grid(products):
#     st.markdown(f"### 🎉 Found {len(products)} products")
#     for i in range(0, len(products), 3):
#         cols = st.columns(3)
#         for j in range(3):
#             idx = i + j
#             if idx >= len(products):
#                 break
#             with cols[j]:
#                 p = products[idx]
#                 if p.get("image_url"):
#                     st.image(p["image_url"], width=100)
#                 st.markdown(f"**{p['name']}**")
#                 st.markdown(f"💰 {p['price']}")
#                 if p.get("mrp") and p["mrp"] != "N/A":
#                     st.markdown(f"~~{p['mrp']}~~")
#                 if p.get("quantity") and p["quantity"] != "N/A":
#                     st.markdown(f"📦 {p['quantity']}")
#                 if p.get("delivery_time") and p["delivery_time"] != "N/A":
#                     st.markdown(f"🚚 {p['delivery_time']}")
#                 source = p["source"].split()[0]
#                 st.markdown(f"[View on {source} 🛒]({p['url']})", unsafe_allow_html=True)

# # ======================
# # Sidebar: Pincode & Controls
# # ======================
# with st.sidebar:
#     st.header("📍 Delivery Location")

#     if st.session_state.pincode:
#         st.write(f"**Current Pincode:** `{st.session_state.pincode}`")
#         if st.button("🔄 Change Pincode"):
#             st.session_state.pincode = None
#             st.session_state.search_results = []
#             st.session_state.chat_messages = []
#             st.rerun()
#     else:
#         pincode_input = st.text_input("Enter 6-digit pincode:", max_chars=6)
#         if st.button("Set Pincode"):
#             if not pincode_input.isdigit() or len(pincode_input) != 6:
#                 st.error("❌ Enter a valid 6-digit pincode.")
#             else:
#                 with st.spinner("Setting location..."):
#                     try:
#                         resp = requests.post(
#                             f"https://28b7c00f2207.ngrok-free.app/init-location",
#                             params={"pincode": pincode_input, "key": "K8904AI"}
#                         )
#                         if resp.status_code == 200:
#                             st.session_state.pincode = pincode_input
#                             st.success("✅ Location set!")
#                             st.rerun()
#                         else:
#                             st.error(f"❌ Failed: {resp.status_code}")
#                     except Exception as e:
#                         st.error("⚠️ Cannot connect to API. Is it running?")

#     # Chat history preview
#     st.markdown("---")
#     st.header("💬 Chat History")
#     for msg in st.session_state.chat_messages[-10:]:
#         role = "👤" if msg["role"] == "user" else "🤖"
#         st.markdown(f"{role} {msg['content'][:30]}...")

#     if st.button("🧹 Clear Chat"):
#         st.session_state.chat_messages = []
#         st.session_state.search_results = []
#         st.rerun()

# # ======================
# # Chat Interface (Main Area)
# # ======================
# # Display chat history
# for msg in st.session_state.chat_messages:
#     with st.chat_message(msg["role"]):
#         content = msg["content"]
#         if content.startswith("PRODUCTS:"):
#             # Extract query safely
#             if "for '" in content:
#                 query = content.split("for '")[1].split("'")[0]
#             elif "for \"" in content:
#                 query = content.split('for "')[1].split('"')[0]
#             else:
#                 query = "this search"
#             st.markdown(f"🔍 Showing results for: **{query}**")
#             show_product_grid(st.session_state.search_results)
#         else:
#             st.write(content)

# # Chat input
# if prompt := st.chat_input("Ask for groceries or set pincode..."):
#     if not st.session_state.pincode:
#         st.error("Please set pincode first in the sidebar.")
#     else:
#         # Add user message
#         st.session_state.chat_messages.append({"role": "user", "content": prompt})
#         with st.chat_message("user"):
#             st.write(prompt)

#         # Get AI response
#         with st.chat_message("assistant"):
#             ai_resp = get_gemini_response(prompt, st.session_state.search_results)

#             if ai_resp.startswith("SEARCH:"):
#                 keyword = ai_resp.replace("SEARCH:", "").strip().split()[0]
#                 st.write(f"🔍 Searching for '{keyword}'...")

#                 # Expand keywords
#                 try:
#                     kw_resp = requests.get(
#                         f"https://28b7c00f2207.ngrok-free.app/keywords?query={keyword}"
#                     )
#                     keywords = kw_resp.json().get("keywords", [keyword]) if kw_resp.status_code == 200 else [keyword]
#                 except:
#                     keywords = [keyword]

#                 results = search_products(keywords, st.session_state.pincode)
#                 st.session_state.search_results = results

#                 if results:
#                     show_product_grid(results)
#                     msg = f"PRODUCTS: Showing results for '{keyword}'"
#                 else:
#                     msg = "📭 No products found. Try another item."

#             elif ai_resp == "PINCODE_CHANGE":
#                 st.session_state.pincode = None
#                 st.session_state.search_results = []
#                 st.session_state.chat_messages = st.session_state.chat_messages[:-1]
#                 st.rerun()
#             else:
#                 st.write(ai_resp)
#                 msg = ai_resp

#             st.session_state.chat_messages.append({"role": "assistant", "content": msg})




# version 6
# streamlit_app.py
# import streamlit as st
# import requests
# import json

# # ======================
# # Session State Initialization
# # ======================
# if "pincode" not in st.session_state:
#     st.session_state.pincode = None
# if "chat_messages" not in st.session_state:
#     st.session_state.chat_messages = []
# if "search_results" not in st.session_state:
#     st.session_state.search_results = []
# if "cart" not in st.session_state:
#     st.session_state.cart = []
# if "dark_mode" not in st.session_state:
#     st.session_state.dark_mode = False

# # ======================
# # Page Config
# # ======================
# st.set_page_config(page_title="🛒 Grocereye", layout="wide")

# # Dynamic theme
# if st.session_state.dark_mode:
#     st.markdown("""
#     <style>
#         body { color: #eee; background: #1e1e1e; }
#         .stApp { background: #1e1e1e; }
#         .css-1d391kg { color: #eee; }
#     </style>
#     """, unsafe_allow_html=True)

# st.title("🛒 Grocereye")
# st.markdown("Your AI-powered grocery assistant")

# # ======================
# # Gemini AI Response Function
# # ======================
# def get_gemini_response(question: str, products: list = None):
#     try:
#         from configs import API_KEY
#         if not API_KEY.strip():
#             return "❌ Gemini API Key is missing in configs.py"
#     except:
#         return "❌ API Key not found. Check configs.py"

#     if products:
#         product_list = "\n".join([
#             f"- {p['name']} | {p['price']} | {p.get('quantity', 'N/A')} | {p['source']} | {p['delivery_time']}"
#             for p in products[:20] if p.get("name") != "N/A"
#         ])
#     else:
#         product_list = "(No recent products)"

#     instruction = f"""
# You are Grocereye, a helpful grocery assistant.
# Answer based on the products below. Be concise.

# Recent Products:
# {product_list}

# User Question: {question}

# Rules:
# - If asked for 'cheapest', 'fastest delivery', or a brand (e.g., Amul), use product list.
# - If user asks about new items (e.g., 'milk', 'bread'), respond with: SEARCH:<item>
# - If user wants to change pincode, respond with: PINCODE_CHANGE
# - Never invent products.
# - Keep answers short.
# """

#     headers = {
#         'Content-Type': 'application/json',
#         'X-goog-api-key': API_KEY,
#     }

#     json_data = {
#         "contents": [{"parts": [{"text": instruction}]}],
#         "generationConfig": {"temperature": 0.3, "maxOutputTokens": 300}
#     }

#     url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

#     try:
#         response = requests.post(url, headers=headers, json=json_data, timeout=30)
#         if response.status_code == 200:
#             data = response.json()
#             return data['candidates'][0]['content']['parts'][0]['text'].strip()
#         else:
#             return f"❌ AI Error: {response.status_code}"
#     except Exception as e:
#         return "❌ Cannot connect to Gemini AI. Check your internet and API key."

# # ======================
# # Product Search Function
# # ======================
# def search_products(keywords: list, pincode: str):
#     all_results = []
#     for kw in keywords:
#         try:
#             resp = requests.get(
#                 f"https://28b7c00f2207.ngrok-free.app/search",
#                 params={"keyword": kw, "pincode": pincode, "key": "K8904AI"},
#                 timeout=60
#             )
#             if resp.status_code == 200:
#                 data = resp.json()
#                 for r in data.get("results", []):
#                     r["matched_keyword"] = kw
#                 all_results.extend(data["results"])
#         except Exception as e:
#             st.error(f"Request failed for '{kw}': {str(e)}")
#             continue
#     return all_results

# # ======================
# # Filter Invalid Products
# # ======================
# def is_valid_product(p):
#     return (
#         p.get("name") and p["name"] != "N/A" and
#         p.get("price") and p["price"] != "N/A" and
#         p.get("image_url")
#     )

# # ======================
# # Show Product Grid with Add to Cart
# # ======================
# def show_product_grid(products):
#     valid_products = [p for p in products if is_valid_product(p)]
#     if not valid_products:
#         st.info("📭 No valid products found.")
#         return

#     st.markdown(f"### 🎉 Found {len(valid_products)} products")

#     for i in range(0, len(valid_products), 3):
#         cols = st.columns(3)
#         for j in range(3):
#             idx = i + j
#             if idx >= len(valid_products):
#                 break
#             with cols[j]:
#                 p = valid_products[idx]
#                 st.image(p["image_url"], width=100)
#                 st.markdown(f"**{p['name']}**")
#                 st.markdown(f"💰 {p['price']}")
#                 if p.get("mrp") and p["mrp"] != "N/A":
#                     st.markdown(f"~~{p['mrp']}~~")
#                 if p.get("quantity") and p["quantity"] != "N/A":
#                     st.markdown(f"📦 {p['quantity']}")
#                 if p.get("delivery_time") and p["delivery_time"] != "N/A":
#                     st.markdown(f"🚚 {p['delivery_time']}")
#                 source = p["source"].split()[0]
#                 st.markdown(f"[View on {source} 🛒]({p['url']})", unsafe_allow_html=True)

#                 # Add to Cart Button
#                 if st.button(f"🛒 Add to Cart", key=f"add_{p['source']}_{p['name']}_{idx}"):
#                     st.session_state.cart.append(p)
#                     st.success(f"✅ {p['name']} added!")

#     return valid_products

# # ======================
# # Sidebar: Pincode & Controls
# # ======================
# with st.sidebar:
#     st.header("📍 Delivery Location")

#     if st.session_state.pincode:
#         st.write(f"**Current Pincode:** `{st.session_state.pincode}`")
#         if st.button("🔄 Change Pincode"):
#             st.session_state.pincode = None
#             st.session_state.search_results = []
#             st.session_state.chat_messages = []
#             st.session_state.cart = []
#             st.rerun()
#     else:
#         pincode_input = st.text_input("Enter 6-digit pincode:", max_chars=6)
#         if st.button("Set Pincode"):
#             if not pincode_input.isdigit() or len(pincode_input) != 6:
#                 st.error("❌ Enter a valid 6-digit pincode.")
#             else:
#                 with st.spinner("Setting location..."):
#                     try:
#                         resp = requests.post(
#                             f"https://28b7c00f2207.ngrok-free.app/init-location",
#                             params={"pincode": pincode_input, "key": "K8904AI"}
#                         )
#                         if resp.status_code == 200:
#                             st.session_state.pincode = pincode_input
#                             st.success("✅ Location set!")
#                             st.rerun()
#                         else:
#                             st.error(f"❌ Failed: {resp.status_code}")
#                     except Exception as e:
#                         st.error("⚠️ Cannot connect to API.")

#     # Cart
#     st.markdown("---")
#     st.header("🛒 Your Cart")
#     if st.session_state.cart:
#         for i, item in enumerate(st.session_state.cart):
#             st.markdown(f"{i+1}. {item['name']} - {item['price']}")
#         if st.button("📦 Checkout (Simulate)"):
#             st.info(f"✅ Ordered {len(st.session_state.cart)} items!")
#     else:
#         st.markdown("Your cart is empty.")

#     # Chat history
#     st.header("💬 Chat History")
#     for msg in st.session_state.chat_messages[-10:]:
#         role = "👤" if msg["role"] == "user" else "🤖"
#         st.markdown(f"{role} {msg['content'][:30]}...")

#     if st.button("🧹 Clear Chat"):
#         st.session_state.chat_messages = []
#         st.session_state.search_results = []
#         st.rerun()

# # ======================
# # Chat Interface
# # ======================
# for msg in st.session_state.chat_messages:
#     with st.chat_message(msg["role"]):
#         content = msg["content"]
#         if content.startswith("PRODUCTS:"):
#             if "for '" in content:
#                 query = content.split("for '")[1].split("'")[0]
#             elif 'for "' in content:
#                 query = content.split('for "')[1].split('"')[0]
#             else:
#                 query = "this search"
#             st.markdown(f"🔍 Showing results for: **{query}**")
#             show_product_grid(st.session_state.search_results)
#         else:
#             st.write(content)

# # Chat input
# if prompt := st.chat_input("Ask for groceries or set pincode..."):
#     if not st.session_state.pincode:
#         st.error("Please set pincode first in the sidebar.")
#     else:
#         st.session_state.chat_messages.append({"role": "user", "content": prompt})
#         with st.chat_message("user"):
#             st.write(prompt)

#         with st.chat_message("assistant"):
#             ai_resp = get_gemini_response(prompt, st.session_state.search_results)

#             if ai_resp.startswith("SEARCH:"):
#                 keyword = ai_resp.replace("SEARCH:", "").strip().split()[0]
#                 st.write(f"🔍 Searching for '{keyword}'...")

#                 try:
#                     kw_resp = requests.get(
#                         f"https://28b7c00f2207.ngrok-free.app/keywords?query={keyword}"
#                     )
#                     keywords = kw_resp.json().get("keywords", [keyword]) if kw_resp.status_code == 200 else [keyword]
#                 except:
#                     keywords = [keyword]

#                 results = search_products(keywords, st.session_state.pincode)
#                 st.session_state.search_results = results
#                 show_product_grid(results)
#                 msg = f"PRODUCTS: Showing results for '{keyword}'"

#             elif ai_resp == "PINCODE_CHANGE":
#                 st.session_state.pincode = None
#                 st.session_state.search_results = []
#                 st.session_state.chat_messages = st.session_state.chat_messages[:-1]
#                 st.rerun()
#             else:
#                 st.write(ai_resp)
#                 msg = ai_resp

#             st.session_state.chat_messages.append({"role": "assistant", "content": msg})




# streamlit_app.py
# streamlit_app.py
import streamlit as st
import requests
import json
import time
from typing import List, Dict

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
st.set_page_config(page_title="🧠 Grocereye AI", layout="wide")

# Dynamic Dark Mode
if st.session_state.dark_mode:
    st.markdown("""
    <style>
        body { color: #eee; background: #111; }
        .stApp { background: #111; }
        .css-1d391kg { color: #eee; }
        .product-card { background: #222; padding: 10px; border-radius: 12px; }
        .cart-item { padding: 10px; margin: 6px 0; border-bottom: 1px solid #444; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 Grocereye AI")
st.markdown("Your intelligent grocery assistant. Powered by AI, driven by intent.")

# ======================
# 🧠 AI Core: Unified Search + Rank + Chat
# ======================
class GroceryAI:
    def __init__(self, ngrok_url: str, api_key: str):
        self.ngrok_url = ngrok_url
        self.api_key = api_key

    def search(self, query: str, pincode: str) -> List[Dict]:
        """Search and rank products with AI"""
        try:
            resp = requests.get(
                f"{self.ngrok_url}/search",
                params={"keyword": query, "pincode": pincode, "key": self.api_key},
                timeout=60
            )
            if resp.status_code != 200:
                return []

            data = resp.json().get("results", [])
            products = [
                p for p in data
                if p.get("name") and p["name"] != "N/A"
                and p.get("price") and p["price"] != "N/A"
            ]

            # 🧠 AI Ranking: Score by price, delivery, value
            for p in products:
                price_val = self._extract_price(p["price"])
                mrp_val = self._extract_price(p.get("mrp", "0"))
                discount = (mrp_val - price_val) / mrp_val if mrp_val > 0 else 0

                # Extract delivery time in minutes
                delivery = self._extract_delivery_time(p.get("delivery_time", ""))

                # Score: high discount, low price, fast delivery
                p["ai_score"] = (
                    (100 - price_val) * 0.4 +
                    (delivery * -1) * 0.3 +
                    (discount * 100) * 0.3
                )

            # Sort by AI score
            return sorted(products, key=lambda x: x["ai_score"], reverse=True)

        except Exception as e:
            st.warning(f"Search error: {e}. Using AI reasoning.")
            return []

    def chat(self, question: str, products: List[Dict]) -> str:
        """AI chat with context-aware reasoning"""
        context = json.dumps([
            {
                "name": p["name"],
                "price": p["price"],
                "mrp": p.get("mrp", "N/A"),
                "quantity": p.get("quantity", "N/A"),
                "source": p["source"],
                "delivery_time": p["delivery_time"]
            }
            for p in products[:20]
        ], indent=2) if products else "(No products)"

        prompt = f"""
You are Grocereye AI, a smart grocery assistant.
Use deep reasoning to answer based on product list.

Product List:
{context}

User Question: {question}

Rules:
- If asked for 'cheapest', find lowest price.
- If 'fastest delivery', find shortest delivery time.
- If 'Amul', filter by brand.
- If 'best value', use price + discount + delivery.
- Never invent products.
- Be concise, helpful, and intelligent.

Answer:
"""

        try:
            from configs import API_KEY
            headers = {
                'Content-Type': 'application/json',
                'X-goog-api-key': API_KEY,
            }
            json_data = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.2, "maxOutputTokens": 300}
            }
            url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
            response = requests.post(url, headers=headers, json=json_data, timeout=30)
            if response.status_code == 200:
                return response.json()['candidates'][0]['content']['parts'][0]['text'].strip()
            else:
                return self._fallback_response(question, products)
        except:
            return self._fallback_response(question, products)

    def _fallback_response(self, question: str, products: List[Dict]) -> str:
        """Smart fallback when AI fails"""
        q = question.lower()
        if not products:
            return "I found no products. Try searching first."

        if "cheapest" in q:
            cheapest = min(products, key=lambda x: self._extract_price(x["price"]))
            return f"The cheapest is **{cheapest['name']}** at {cheapest['price']} from {cheapest['source']}."

        if "fastest" in q or "quick" in q or "soon" in q:
            fastest = min(products, key=lambda x: self._extract_delivery_time(x["delivery_time"]))
            return f"Fastest delivery: **{fastest['name']}** in {fastest['delivery_time']}."

        if any(brand in q for brand in ["amul", "parle", "nestle", "dairy milk"]):
            brand_prods = [p for p in products if q.split()[0] in p["name"].lower()]
            if brand_prods:
                return f"I found {len(brand_prods)} items: " + ", ".join([p["name"] for p in brand_prods[:3]])
            return f"No products from that brand."

        if "value" in q or "best deal" in q:
            best = max(products, key=lambda x: (self._extract_price(x.get("mrp", "0")) - self._extract_price(x["price"])))
            return f"Best value: **{best['name']}** saves ₹{self._extract_price(best['mrp']) - self._extract_price(best['price'])}."

        return "I can help with price, delivery, brand, and value comparisons."

    def _extract_price(self, price: str) -> float:
        try:
            return float(''.join(filter(str.isdigit, price.replace('₹', ''))))
        except:
            return float('inf')

    def _extract_delivery_time(self, dt: str) -> int:
        try:
            return int(''.join(filter(str.isdigit, dt)))
        except:
            return 30  # default

# ======================
# Initialize AI Engine
# ======================
try:
    from configs import API_KEY
except:
    API_KEY = ""

ai_engine = GroceryAI(
    ngrok_url="https://28b7c00f2207.ngrok-free.app",
    api_key=API_KEY
)

# ======================
# Show Product Grid
# ======================
def show_product_grid(products: List[Dict]):
    if not products:
        st.info("📭 No products found. Try another query.")
        return

    st.markdown(f"### 🎯 Found {len(products)} products (AI-ranked)")

    for i in range(0, len(products), 3):
        cols = st.columns(3)
        for j in range(3):
            idx = i + j
            if idx >= len(products):
                break
            with cols[j]:
                p = products[idx]
                st.markdown(f"**{p['name']}**")
                st.markdown(f"💰 {p['price']} | ~~{p.get('mrp', 'N/A')}~~")
                if p.get("quantity") and p["quantity"] != "N/A":
                    st.markdown(f"📦 {p['quantity']}")
                st.markdown(f"🚚 {p['delivery_time']}")
                source = p["source"].split()[0]
                if p.get("image_url"):
                    st.image(p["image_url"], width=100)
                st.markdown(f"[View on {source} 🛒]({p['url']})", unsafe_allow_html=True)

                # Add to Cart
                item_id = f"{p['name']}_{p['price']}_{p['source']}"
                if st.button("🛒 Add to Cart", key=f"add_{hash(item_id) % 1e6}_{idx}"):
                    st.session_state.cart.append(p)
                    st.success("✅ Added!")
                    st.rerun()

# ======================
# Sidebar: Pincode & Cart
# ======================
with st.sidebar:
    st.header("📍 Delivery Location")

    if st.session_state.pincode:
        st.write(f"`{st.session_state.pincode}`")
        if st.button("🔄 Change Pincode"):
            st.session_state.pincode = None
            st.session_state.search_results = []
            st.session_state.cart = []
            st.session_state.chat_messages = []
            st.rerun()
    else:
        pincode_input = st.text_input("Enter pincode:", max_chars=6)
        if st.button("Set Pincode"):
            if pincode_input.isdigit() and len(pincode_input) == 6:
                st.session_state.pincode = pincode_input
                st.success("✅ Location set!")
                st.rerun()
            else:
                st.error("❌ Enter valid 6-digit pincode.")

    # Cart
    st.markdown("---")
    st.header("🛒 Your Cart")
    if st.session_state.cart:
        total = sum(ai_engine._extract_price(item["price"]) for item in st.session_state.cart)
        for i, item in enumerate(st.session_state.cart):
            st.markdown(f"{item['name']} - {item['price']}")
        st.markdown(f"**Total: ₹{total:.2f}**")
        if st.button("📦 Checkout"):
            st.info(f"✅ Ordered {len(st.session_state.cart)} items!")
    else:
        st.markdown("Empty")

    # Dark Mode
    if st.button("🎨 Toggle Dark Mode"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# ======================
# Chat Interface
# ======================
for msg in st.session_state.chat_messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
if prompt := st.chat_input("Ask or search..."):
    if not st.session_state.pincode:
        st.error("Set pincode first.")
    else:
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            # If it's a search query
            if any(word in prompt.lower() for word in ["search", "find", "get", "want", "need"]):
                with st.spinner("🧠 Searching with AI..."):
                    results = ai_engine.search(prompt, st.session_state.pincode)
                    st.session_state.search_results = results
                    show_product_grid(results)
                    msg = f"PRODUCTS: Showing results for '{prompt}'"
            else:
                # AI chat about existing results
                response = ai_engine.chat(prompt, st.session_state.search_results)
                st.write(response)
                msg = response

            st.session_state.chat_messages.append({"role": "assistant", "content": msg})