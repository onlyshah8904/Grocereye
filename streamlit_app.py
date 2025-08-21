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
import streamlit as st
import requests
import re

# ======================
# Session State Initialization
# ======================
if "pincode" not in st.session_state:
    st.session_state.pincode = None
if "messages" not in st.session_state:
    st.session_state.messages = []  # role, content, products, keywords (optional)

# ======================
# Page Config
# ======================
st.set_page_config(page_title="🛒 Grocereye", layout="centered")
st.title("🛒 Grocereye")
st.markdown("Your AI-powered grocery assistant")

# ======================
# Gemini AI Response Function (Enhanced Context)
# ======================
def get_gemini_response(question: str, current_products=None, past_contexts=[]):
    from configs import API_KEY
    import requests as http_requests

    # Build current context
    current_ctx = "\n".join([
        f"- {p['name']} | {p['price']} | {p.get('quantity', 'N/A')} | {p['source']} | {p['delivery_time']}"
        for p in (current_products or [])
    ]) if current_products else "(No current products)"

    # Build past context (only keywords + count)
    past_ctx = "\n".join([
        f"- Past '{ctx['keywords']}': {len(ctx['products'])} products" for ctx in past_contexts
    ]) if past_contexts else "None"

    instruction = f"""
You are Grocereye, a helpful grocery assistant.
Answer based on current AND past product results.

Current Products:
{current_ctx}

Past Searches:
{past_ctx}

User Question: {question}

Rules:
- If user says 'earlier', 'before', 'previously', 'that Amul one', etc. → check Past Searches.
- If they mention a product type (e.g., 'chocolate'), and it was searched before → use those results.
- If they say 'cheapest', 'fastest', etc. → apply to the most relevant product list.
- NEVER invent products. Only use provided data.
- If unsure which list to use, ask for clarification.
- If user says 'new', 'instead', 'don’t want X' → trigger fresh search.
"""

    headers = {
        'Content-Type': 'application/json',
        'X-goog-api-key': API_KEY,
    }

    json_data = {
        "contents": [{"parts": [{"text": instruction}]}],
        "generationConfig": {"temperature": 0.4, "maxOutputTokens": 300}
    }

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

    try:
        response = http_requests.post(url, headers=headers, json=json_data)
        if response.status_code == 200:
            data = response.json()
            return data['candidates'][0]['content']['parts'][0]['text'].strip()
        else:
            return "I'm having trouble connecting to the AI."
    except Exception as e:
        return f"Sorry, I can't reach the AI. ({str(e)})"

# ======================
# Helper: Extract Keywords
# ======================
def get_keywords(query):
    try:
        resp = requests.get(f"https://28b7c00f2207.ngrok-free.app/keywords?query={requests.utils.quote(query)}")
        if resp.status_code == 200:
            return resp.json().get("keywords", [])
        else:
            return []
    except Exception as e:
        st.error(f"Keyword API failed: {e}")
        return []

# ======================
# Helper: Search Products
# ======================
def search_products(keywords, pincode):
    all_results = []
    try:
        for kw in keywords:
            search_resp = requests.get(
                f"https://28b7c00f2207.ngrok-free.app/search?keyword={requests.utils.quote(kw)}&pincode={pincode}"
            )
            if search_resp.status_code == 200:
                data = search_resp.json()
                for r in data["results"]:
                    r["matched_keyword"] = kw
                all_results.extend(data["results"])
    except Exception as e:
        st.error(f"Search failed: {e}")
        return []

    return [r for r in all_results if not (r.get("name") == "N/A" and r.get("price") == "N/A")]

# ======================
# Retrieve Relevant Past Products
# ======================
def retrieve_relevant_products(query: str, messages):
    # Extract all assistant messages with products
    past_entries = []
    for msg in messages:
        if msg["role"] == "assistant" and "products" in msg and msg["products"]:
            if "keywords" in msg:  # if stored
                past_entries.append({"keywords": msg["keywords"], "products": msg["products"]})
            else:
                # Fallback: try to guess from content
                pass

    if not past_entries:
        return None

    query_lower = query.lower()

    # Try to match keywords in past searches
    for entry in reversed(past_entries):  # latest first
        for kw in entry["keywords"]:
            if kw.lower() in query_lower:
                return entry["products"]  # return matching past results

    # Fallback: if user says "earlier", "previous", "that one", return latest
    if re.search(r"\b(earlier|previous|before|that|one I saw|first|second)\b", query_lower):
        return past_entries[0]["products"]  # most recent

    return None  # no match

# ======================
# Chat Interface
# ======================

# Display messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if "products" in message and message["products"]:
            cols = st.columns(3)
            for i, p in enumerate(message["products"]):
                with cols[i % 3]:
                    if p.get("image_url"):
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

# ----------------------
# Pincode Setup
# ----------------------
if not st.session_state.pincode:
    st.divider()
    st.subheader("📍 Welcome! Set your delivery pincode")
    pincode_input = st.text_input("Enter your pincode:", placeholder="e.g., 380007")

    if st.button("Set Pincode"):
        if pincode_input.strip():
            try:
                resp = requests.post(f"https://28b7c00f2207.ngrok-free.app/init-location?pincode={pincode_input.strip()}")
                if resp.status_code == 200:
                    st.session_state.pincode = pincode_input.strip()
                    st.success(f"✅ Location set: {pincode_input}")
                    st.rerun()
                else:
                    st.error("Failed to set location.")
            except Exception as e:
                st.error("❌ Cannot connect to backend. Is `python api.py` running?")
        else:
            st.error("Pincode is required.")
else:
    st.divider()
    st.markdown(
        f"<div style='text-align: center; font-size: 0.9em; color: gray;'>"
        f"📍 Pincode: {st.session_state.pincode} | "
        f"<a href='#' onclick='window.location.reload()'>Change</a>"
        f"</div>",
        unsafe_allow_html=True
    )

    # Chat input
    if prompt := st.chat_input("Need groceries? Ask here..."):

        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            # Step 1: Get keywords for current query
            keywords = get_keywords(prompt)

            # Step 2: Decide: New search or use past?
            use_past_products = None
            is_new_search = True

            # Only try to retrieve if no new keywords (e.g., follow-up)
            if not keywords or re.search(r"\b(cheapest|fastest|earlier|previous|that|don't want|instead|change)\b", prompt.lower()):
                use_past_products = retrieve_relevant_products(prompt, st.session_state.messages)

            if use_past_products is not None:
                st.markdown("🔍 Using relevant past results...")
                products = use_past_products
                final_keywords = ["(referenced from history)"]
                is_new_search = False
            elif keywords:
                st.markdown(f"🔍 Searching for: *{', '.join(keywords)}*")
                products = search_products(keywords, st.session_state.pincode)
                final_keywords = keywords
                is_new_search = True
            else:
                response = "I didn't understand your request. Try mentioning a product."
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()

            if not products:
                response = "Sorry, I couldn't find any products for that."
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()

            # Step 3: Get AI response with full context
            ai_response = get_gemini_response(
                prompt,
                current_products=products,
                past_contexts=[
                    {"keywords": msg.get("keywords", ["unknown"]), "products": msg["products"]}
                    for msg in st.session_state.messages
                    if msg["role"] == "assistant" and "products" in msg
                ]
            )
            st.write(ai_response)

            # Step 4: Show products
            cols = st.columns(3)
            displayed = 0
            for i, p in enumerate(products[:9]):
                with cols[displayed % 3]:
                    if p.get("image_url"):
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
                displayed += 1

            # Step 5: Save assistant message
            msg = {
                "role": "assistant",
                "content": ai_response,
                "products": products[:9]
            }
            if is_new_search:
                msg["keywords"] = final_keywords  # for future reference
            st.session_state.messages.append(msg)

    # Clear chat
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()