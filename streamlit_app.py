import streamlit as st
import requests

st.set_page_config(page_title="🛒 Grocereye", layout="centered")

st.title("🛒 Grocereye")
st.markdown("Your AI-powered grocery assistant")

# State
if "pincode" not in st.session_state:
    st.session_state.pincode = None

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
                    resp = requests.post(f"https://60b0f2190f07.ngrok-free.app/init-location?pincode={pincode_input}")
                    if resp.status_code == 200:
                        st.session_state.pincode = pincode_input
                        st.success(f"✅ Location set: {pincode_input}")
                        st.rerun()
                    else:
                        st.error("Failed to set location.")
                except Exception as e:
                    print(e)
                    st.error("❌ Cannot connect to API. Is `python api.py` running?")

# Step 2: Search
else:
    st.success(f"📍 Active Pincode: {st.session_state.pincode}")
    if st.button("⬅️ Change Pincode"):
        st.session_state.pincode = None
        st.rerun()

    st.subheader("🛍️ What do you need?")
    user_query = st.text_input("Describe your need:", placeholder="e.g., I want milk and bread")

    if st.button("🔍 Find Products"):
        if not user_query.strip():
            st.warning("Please enter a query.")
        else:
            with st.spinner("🧠 Understanding your needs..."):
                try:
                    # Get keywords
                    kw_resp = requests.get(f"https://60b0f2190f07.ngrok-free.app/keywords?query={requests.utils.quote(user_query)}")
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
                                f"https://60b0f2190f07.ngrok-free.app/search?keyword={kw}&pincode={st.session_state.pincode}"
                            )
                            if search_resp.status_code == 200:
                                data = search_resp.json()
                                for r in data["results"]:
                                    r["matched_keyword"] = kw
                                all_results.extend(data["results"])

                    # Filter out invalid results (all N/A)
                    def is_valid_product(p):
                        return not (
                            p.get("name") == "N/A" and
                            p.get("price") == "N/A" and
                            not p.get("image_url")
                        )

                    valid_results = [r for r in all_results if is_valid_product(r)]

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
                                    st.markdown(f"[View on {product['source']} 🛒]({product['url']})", unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Search failed: {str(e)}")