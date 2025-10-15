# blinkit.py
from DrissionPage import Chromium
from curl_cffi import requests
import re
from datetime import datetime, timedelta

active_sessions = {}
SESSION_TTL = timedelta(minutes=10)

def clean_name(name):
    return re.sub(r'[^a-z0-9]+', '-', name.strip().lower()).strip('-')

def get_session(pincode):
    now = datetime.now()
    expired = [pc for pc, s in active_sessions.items() if now - s["created_at"] > SESSION_TTL]
    for pc in expired:
        close_session(pc)

    if pincode in active_sessions:
        active_sessions[pincode]["last_used"] = now
        return active_sessions[pincode]

    browser = Chromium(9993)
    try:
        tab = browser.latest_tab
        tab.get('https://blinkit.com/')
        tab('@class=LocationBar__Container-sc-x8ezho-6 gcLVHe').click()

        ele = tab.ele('@name=select-locality')
        ele.input(pincode)
        tab.wait(2)
        eles = tab.eles('@class=LocationSearchList__LocationDetailContainer-sc-93rfr7-1 bBiSUM')

        if eles:
            eles[0].click()
            print(f"✅ Selected location for pincode: {pincode}")
        else:
            browser.quit()
            return None

        tab.wait(2)
        cookiess = tab.cookies()
        cookies = {cookie['name']: cookie['value'] for cookie in cookiess}
        lat = cookies.get('gr_1_lat')
        lon = cookies.get('gr_1_lon')
        if not lat:
            browser.quit()
            return None

        session = {
            "browser": browser,
            "tab": tab,
            "cookies": cookies,
            "lat": lat,
            "lon": lon,
            "created_at": now,
            "last_used": now
        }
        active_sessions[pincode] = session
        return session

    except Exception as e:
        print("Blinkit init failed:", e)
        browser.quit()
        return None

def get_global_eta(pincode):
    try:
        session = get_session(pincode)
        if not session:
            return "N/A"

        resp = requests.get(
            'https://blinkit.com/v1/consumerweb/eta',
            headers={'lat': session["lat"], 'lon': session["lon"]},
            cookies=session["cookies"],
            impersonate="edge99"
        )
        if resp.status_code == 200:
            return f"{resp.json().get('eta_in_minutes', 'N/A')} mins"
        else:
            print(f"⚠️ ETA fetch failed: {resp.status_code}")
            return "N/A"
    except Exception as e:
        print(f"⚠️ ETA request error: {e}")
        return "N/A"

def search_in_active_session(keyword, pincode):
    session = get_session(pincode)
    if not session:
        return []

    try:
        params = {'q': keyword, 'offset': '0', 'limit': '10'}
        resp = requests.post(
            'https://blinkit.com/v1/layout/search',
            params=params,
            cookies=session["cookies"],
            headers={'lat': session["lat"], 'lon': session["lon"]},
            impersonate="edge101"
        )
        # print(resp.text)
        if resp.status_code != 200:
            return []

        data = resp.json()
        delivery_time = get_global_eta(pincode)

        products = []
        for s in data.get("response", {}).get("snippets", []):
            w = s.get("data", {})
            pid = w.get("identity", {}).get("id")
            if not pid: continue

            name_obj = w.get("display_name") or w.get("name", {})
            name = name_obj.get("text", "N/A")

            # Image
            image_url = w.get("image", {}).get('url') or ''
            

            slug = clean_name(name)
            url = f"https://blinkit.com/prn/{slug}/prid/{pid}"

            price = w.get("normal_price", {}).get("text", "N/A")
            mrp = w.get("mrp", {}).get("text", price)

            variant = w.get("variant", {}).get("text")
            unit = w.get("unit", "")
            quantity = variant or unit or "N/A"

            products.append({
                "source": "Blinkit",
                "name": name,
                "price": price,
                "mrp": mrp,
                "quantity": quantity,
                "delivery_time": delivery_time,
                "url": url,
                "image_url": image_url
            })
        return products
    except Exception as e:
        print("Blinkit search error:", e)
        return []

def close_session(pincode):
    if pincode in active_sessions:
        try:
            active_sessions[pincode]["browser"].quit()
            print(f"🗑️ Closed Blinkit session for {pincode}")
        except:
            pass
        finally:
            del active_sessions[pincode]