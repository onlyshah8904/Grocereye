# bigbasket.py
from DrissionPage import Chromium
from curl_cffi import requests
from datetime import datetime, timedelta

active_sessions = {}
SESSION_TTL = timedelta(minutes=10)

headers = {
    'accept': '*/*',
    'x-channel': 'BB-WEB',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def get_session(pincode):
    now = datetime.now()
    expired = [pc for pc, s in active_sessions.items() if now - s["created_at"] > SESSION_TTL]
    for pc in expired:
        close_session(pc)

    if pincode in active_sessions:
        active_sessions[pincode]["last_used"] = now
        return active_sessions[pincode]

    browser = Chromium(9992)

    try:
        tab = browser.latest_tab
        tab.get('https://www.bigbasket.com/')
        tab.refresh()

        # Click on location bar
        tab('@class=AddressDropdown___StyledMenuButton-sc-i4k67t-1 iXeMGW').click()
        # Type pincode
        elee = tab.ele('xpath://div[@class="AddressDropdown___StyledDiv-sc-i4k67t-5 cicNbD"]').click()
        if elee:
            elee.input(pincode)
            # print("yayy")
            # ele
        # else:
            # print("fucked")
        tab.wait(1)

        eles = tab.eles('xpath://*[contains(@class, "AddressDropdown___StyledMenuItem-sc-i4k67t-7")]')

        if eles:
            eles[0].click()
            print(f"✅ Selected location for pincode: {pincode}")
        else:
            print("❌ No location suggestion found!")
            return False

        # Wait for cookies to update
        tab.wait(2)
        cookies = tab.cookies()
        cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}
        session = {
            "browser": browser,
            "tab": tab,
            "cookies": cookies_dict,
            "created_at": now,
            "last_used": now
        }
        active_sessions[pincode] = session
        return session
    except Exception as e:
        print("BigBasket init failed:", e)
        browser.quit()
        return None
    # finally:
        # browser.quit()

# def search_in_active_session(keyword, pincode):
#     session = get_session(pincode)
#     if not session:
#         return []

#     try:
#         params = {'type': 'ps', 'slug': keyword, 'page': '1', 'bucket_id': '56'}
#         resp = requests.get(
#             'https://www.bigbasket.com/listing-svc/v2/products',
#             params=params,
#             cookies=session["cookies"],
#             headers=headers,
#             impersonate="edge99"
#         )
#         if resp.status_code != 200:
#             return []

#         data = resp.json()
#         products = []
#         for tab in data.get("tabs", []):
#             for item in tab.get("product_info", {}).get("products", []):
#                 name = item.get("desc", "N/A")

#                 # ✅ Safe URL handling
#                 absolute_url = item.get("absolute_url")
#                 if not absolute_url:
#                     prod_id = item.get("id", "")
#                     absolute_url = f"/pd/{prod_id}/"
#                 url = f"https://www.bigbasket.com{absolute_url}"

#                 # Price
#                 price_val = item.get("pricing", {}).get("discount", {}).get("prim_price", {}).get("sp", "N/A")
#                 price = f"₹{price_val}" if isinstance(price_val, (int, float)) else str(price_val)

#                 products.append({
#                     "source": "BigBasket",
#                     "name": name,
#                     "price": price,
#                     "url": url
#                 })
#         return products
#     except Exception as e:
#         print("BigBasket search error:", e)
#         return []

def search_in_active_session(keyword, pincode):
    session = get_session(pincode)
    if not session:
        return []

    try:
        params = {'type': 'ps', 'slug': keyword, 'page': '1', 'bucket_id': '56'}
        resp = requests.get(
            'https://www.bigbasket.com/listing-svc/v2/products',
            params=params,
            cookies=session["cookies"],
            headers=headers,
            impersonate="edge110"
        )
        if resp.status_code != 200:
            return []

        data = resp.json()
        products = []
        for tab in data.get("tabs", []):
            for item in tab.get("product_info", {}).get("products", []):
                name = item.get("desc", "N/A")

                # URL
                absolute_url = item.get("absolute_url")
                if not absolute_url:
                    prod_id = item.get("id", "")
                    absolute_url = f"/pd/{prod_id}/"
                url = f"https://www.bigbasket.com{absolute_url.strip()}"

                # Pricing
                pricing = item.get("pricing", {})
                discount = pricing.get("discount", {})
                price_val = discount.get("prim_price", {}).get("sp", "N/A")
                mrp_val = discount.get("mrp", "N/A")
                price = f"₹{price_val}" if isinstance(price_val, (int, float)) else str(price_val)
                mrp = f"₹{mrp_val}" if isinstance(mrp_val, (int, float)) else str(mrp_val)

                # Quantity
                quantity = item.get("w", "N/A")

                # Delivery time
                availability = item.get("availability", {})
                delivery_time = availability.get("short_eta", "12 hrs")

                # Image (m size)
                images = item.get("images", [])
                image_url = images[0].get("m", "") if images else ""

                products.append({
                    "source": "BigBasket",
                    "name": name,
                    "price": price,
                    "mrp": mrp,
                    "quantity": quantity,
                    "delivery_time": delivery_time,
                    "url": url,
                    "image_url": image_url.strip()
                })
        return products
    except Exception as e:
        print("BigBasket search error:", e)
        return []

def close_session(pincode):
    if pincode in active_sessions:
        active_sessions[pincode]["browser"].quit()
        del active_sessions[pincode]