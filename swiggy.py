# from curl_cffi import requests
# import requests as r_requests
# from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
# import json
# from urllib.parse import quote
# from parsel import Selector
# import re

# HEADERS = {
#   'accept': '*/*',
#   'accept-language': 'en-US,en;q=0.9',
#   'content-type': 'application/json',
#   'matcher': '8887c8ecbcc77dag9dfceca',
#   'origin': 'https://www.swiggy.com',
#   'priority': 'u=1, i',
#   'referer': 'https://www.swiggy.com/instamart/search?custom_back=true',
#   'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
#   'sec-ch-ua-mobile': '?0',
#   'sec-ch-ua-platform': '"Windows"',
#   'sec-fetch-dest': 'empty',
#   'sec-fetch-mode': 'cors',
#   'sec-fetch-site': 'same-origin',
#   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
#   'x-build-version': '2.291.0',
# }
# PROXIES = {
#     "http": "http://51.222.241.206:8899",
#     "https": "http://51.222.241.206:8899"
# }

# class SwiggyKeyword:
#     def __init__(self, pincode, keyword=None, product_id=None, product_url=None):
#         self.pincode = pincode
#         self.keyword = keyword
#         self.product_id = product_id
#         self.product_url = product_url
#         self.request_calls = []
    
#     def pin_to_place(self):
#         try:
#             url = f"https://www.swiggy.com/dapi/misc/place-autocomplete?input={self.pincode}&types="
#             response = requests.get(url=url, headers=HEADERS)
#             selector = Selector(response.text)
#             address = selector.jmespath('data[0].description').get()
#             place_id = selector.jmespath('data[0].place_id').get()
#             if address and place_id:
#                 self.request_calls.append({'request': url, 'method': 'GET', 'name': 'PINCODE_TO_PLACE_ID'})

#                 return {
#                     "status": 200,
#                     "pincode": self.pincode,
#                     "address": address,
#                     "placeId": place_id
#                 }
#             else:
#                 return {
#                 "error": "ERROR_PLACE_NOT_FOUND",
#                 "pincode": self.pincode,
#                 "address": "",
#                 "placeId": ""
#             }

#         except Exception as e:
#             print("pin_to_place", e)
#             return {
#                 "error": "ERROR_FETCHING_PLACE",
#                 "pincode": self.pincode,
#                 "address": "",
#                 "placeId": ""
#             }

#     def place_id_to_lat_long(self, placeId):
#         try:
#             if placeId:
#                 url = f"https://www.swiggy.com/dapi/misc/address-recommend?place_id={placeId}"
#                 response = requests.get(url=url, headers=HEADERS)
#                 selector = Selector(response.text)
#                 self.address = selector.jmespath('data[0].formatted_address').get()
#                 self.lat = selector.jmespath('data[0].geometry.location.lat').get()
#                 self.long = selector.jmespath('data[0].geometry.location.lng').get()

#                 self.request_calls.append({'request': url, 'method': 'GET', 'name': 'PLACE_ID_TO_LAT_LONG'})
#                 return {
#                     "status": 200,
#                     "address": self.address,
#                     "placeId": placeId,
#                     "lat": self.lat,
#                     "long": self.long
#                 }
            
#             else:
#                 return {
#                     "error": "ERROR_PLACE_ID_IS NULL",
#                     "address": "",
#                     "placeId": placeId,
#                     "lat": "",
#                     "long": ""
#                 }
            
#         except Exception as e:
#             print("place_id_to_lat_long", e)
#             return  {
#                 "error": "ERROR_FETCHING_LAT_LONG",
#                 "address": "",
#                 "placeId": "",
#                 "lat": "",
#                 "long": ""
#             }
    
#     def encode_cookie_value(self, address, lat, long):
#         if address and lat and long:
#             user_location_str = json.dumps({'address': address, 'lat': lat, 'lng': long})
#             user_location_encoded = quote(user_location_str)
#             cookies = {'cookies': {
#                 'userLocation': user_location_encoded,
#                 '_device_id': 'd947c398-bb67-304e-dc06-40b7d5353ea7',
#                 'tid': 's%3A8a4b299d-d634-4b7c-a034-df172f6026ae.MPMXIaIGoYrbjlHQDVcjCChhgj5f52cWcJRt9WpsyNk',
#             }, 'address': address, 'lat': lat, 'long': long}

#             with open('cookie_mappings.json', 'r') as cm:
#                 cookie_mappings = json.loads(cm.read())

#             with open('cookie_mappings.json', 'w') as cm:
#                 cookie_mappings[self.pincode] = cookies
#                 cm.write(json.dumps(cookie_mappings))

#             return cookies['cookies']
#         else:
#             return None

#     def cookie_exists(self, pincode):
#         with open('cookie_mappings.json', 'r') as cm:
#             mappings = json.loads(cm.read())        
#         if pincode in mappings:
#             cookies = mappings[pincode]['cookies']
#             self.address = mappings[pincode]['address']
#             self.lat = mappings[pincode]['lat']
#             self.long = mappings[pincode]['long']
#             return cookies
#         else:
#             return None

#     @retry(
#     stop=stop_after_attempt(3),
#     wait=wait_exponential(multiplier=1, min=1, max=4),
#     retry=retry_if_exception_type(requests.RequestsError)
#     )
#     def _post_request(self, url, headers, cookies, data):
#         print(cookies)
#         response = requests.post(
#             url,
#             headers=headers,
#             cookies=cookies,
#             data=data,
#             proxies=PROXIES,
#             verify=False
#         )

#         if response.status_code >= 400:
#             response.raise_for_status()
        
#         return response

#     @retry(
#     stop=stop_after_attempt(3),
#     wait=wait_exponential(multiplier=1, min=1, max=4),
#     retry=retry_if_exception_type(requests.RequestsError)
#     )
#     def _get_request(self, url, headers, cookies):
#         response = r_requests.get(
#             url,
#             headers=headers,
#             cookies=cookies,
#             proxies=PROXIES,
#             verify=False
#         )

#         if response.status_code >= 400:
#             response.raise_for_status()
        
#         return response

#     def search_keyword(self, cookies, page_number=0, offset=0):
#         if cookies:
#             url = f"https://www.swiggy.com/api/instamart/search?pageNumber={page_number}&searchResultsOffset={offset}&limit=40&query={self.keyword}&pageType=INSTAMART_AUTO_SUGGEST_PAGE&isPreSearchTag=false"
#             payload = json.dumps({
#                 "facets": {},
#                 "sortAttribute": ""
#             })

#             try:
#                 self.response = self._post_request(url, HEADERS, cookies, payload)
#                 self.request_calls.append({'request': url, 'method': 'POST', 'name': 'SEARCH_KEYWORD'})
#             except requests.RequestsError as e:
#                 return {"error": "REQUEST_FAILED", "details": str(e)}
#         else:
#             return {
#                 "error": "ERROR_FETCHING_LISITNG_DATA"
#             }
        
#     def search_product(self, cookies, store_id=None):
#         if not cookies:
#             return {
#                 "error": "ERROR_FETCHING_PRODUCT_DATA_COOKIE_MISSING"
#             }
        
#         if not store_id:
#             return {
#                 "error": "ERROR_FETCHING_PRODUCT_DATA_STORE_ID_MISSING"
#             }
        
#         if self.product_id:
#             url = f"https://www.swiggy.com/api/instamart/item/{self.product_id}/widgets?storeId={store_id}&primaryStoreId={store_id}"
#         elif self.product_url:
#             params_split = self.product_url.split('?')
#             if len(params_split) > 1:
#                 url_path_split = params_split[0].split('/')
#                 if not url_path_split[0]:
#                     product_id = url_path_split[-2]
#                     url = f"https://www.swiggy.com/api/instamart/item/{product_id}/widgets?storeId={store_id}&primaryStoreId={store_id}"
#                 else:
#                     product_id = url_path_split[-1]
#                     url = f"https://www.swiggy.com/api/instamart/item/{product_id}/widgets?storeId={store_id}&primaryStoreId={store_id}"
#             else:
#                 url_path_split = params_split[0].split('/')
#                 if not url_path_split[-1]:
#                     product_id = url_path_split[-2]
#                     url = f"https://www.swiggy.com/api/instamart/item/{product_id}/widgets?storeId={store_id}&primaryStoreId={store_id}"
#                 else:
#                     product_id = url_path_split[-1]
#                     url = f"https://www.swiggy.com/api/instamart/item/{product_id}/widgets?storeId={store_id}&primaryStoreId={store_id}"
#         else:
#             return {"error": "PRODUCT_ID_OR_PRODUCT_URL_REQUIRED"}
        
#         try:
#             self.response = self._get_request(url, headers=HEADERS, cookies=cookies)

#             self.request_calls.append({'request': url, 'method': 'GET', 'name': 'SEARCH_PRODUCT'})
#         except requests.RequestsError as e:
#                 return {"error": "REQUEST_FAILED", "details": str(e)}
    
#     def get_store_id(self, cookies):
#         url = "https://www.swiggy.com/instamart"
#         try:
#             self.response = self._get_request(url, headers=HEADERS, cookies=cookies)
#         except requests.RequestsError as e:
#                 return {"error": "REQUEST_FAILED", "details": str(e)}
#         try:
#             store_ids = re.findall(r'"storeId":"(\d+)"|"podId":"(\d+)"', self.response.text)
#             if store_ids:
#                 self.request_calls.append({'request': url, 'method': 'GET', 'name': 'STORE_ID'})
#                 if store_ids[0][0]:
#                     return store_ids[0][0]
#                 else:
#                     return store_ids[0][-1]

#             else:
#                 return None
#         except Exception as e:
#                 return None
        
#     def parse_listing_page(self):
#         try:
#             if self.response.status_code == 200:
#                 selector = Selector(self.response.text)
#                 if selector.jmespath('statusCode').get() == 0:
#                     items = []
#                     data_type = selector.jmespath('data.widgets[0].widgetInfo.widgetType').get()
#                     item_count = selector.jmespath('data.widgets[0].widgetInfo.itemCount').get()
#                     hasMorePages = selector.jmespath('data.hasMorePages').get()
#                     offset = selector.jmespath('data.searchResultsOffset').get()
#                     page_number = selector.jmespath('data.pageNumber').get()
#                     lisitngs = selector.jmespath('data.widgets[0].data').getall()
#                     for listing in lisitngs:
#                         if not len(listing['variations']) > 1:
#                             final = listing['variations'][0]
#                             listing.pop('variations')
#                             final.update(listing)
#                             final['images'] = ["https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_252,h_272/" + url for url in final['images']]
#                             items.append(final)

#                     result = {
#                         'pincode': self.pincode,
#                         'address': self.address,
#                         'lat': self.lat,
#                         'long': self.long,
#                         'data_type': data_type,
#                         'item_count': item_count,
#                         'items': items,
#                         'page_number': page_number,
#                         'hasMorePages': hasMorePages,
#                         'offset': offset
#                     }

#                     return result
#                 else:
#                     return {
#                         'error': 'ERROR_FETCHING_LISITNG_DATA',
#                         'result': ''
#                     }
#             else:
#                 return {
#                         'error': 'ERROR_FETCHING_LISITNG_DATA',
#                         'result': ''
#                     }
#         except Exception as e:
#             print(e)
#             return {
#                 "error": "ERROR_PARSING_LISTING_DATA",
#                 "result": '',
#                 "details": str(e)
#             }

#     def parse_product_page(self):
#         try:
#             if self.response.status_code == 200:
#                 selector = Selector(self.response.text)
#                 if selector.jmespath('statusCode').get() == 0:
#                     item = selector.jmespath('data.item').get()
#                     if not len(item['variations']) > 1:
#                         final = item['variations'][0]
#                         item.pop('variations')
#                         final.update(item)
#                         final['images'] = ["https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_252,h_272/" + url for url in final['images']]
#                         final['store_details'] = selector.jmespath('data.storeDetails').get()
#                         return final
#                     else:
#                         for variation in item["variations"]:
#                             variation['images'] = ["https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_252,h_272/" + url for url in variation['images']]
#                         item['store_details'] = selector.jmespath('data.storeDetails').get()
#                         return item

#                 else:
#                     print(self.response.status_code, self.response.text)
#                     return {
#                         'error': 'ERROR_FETCHING_PRODUCT_DATA',
#                         'result': ''
#                     }    
#             else:
#                 return {
#                         'error': 'ERROR_FETCHING_PRODUCT_DATA',
#                         'result': ''
#                     }
#         except Exception as e:
#             print(e)
#             return {
#                 "error": "ERROR_PARSING_PRODUCT_DATA",
#                 "result": ''
#             }

# def main(pincode=None, keyword=None, product_id=None, product_url=None, page_number=0, offset=0):
#     swiggy = SwiggyKeyword(pincode=pincode, keyword=keyword, product_id=product_id, product_url=product_url)
    

#     check_cookie_exists = swiggy.cookie_exists(pincode=pincode)
#     cookie_cache = False
#     if check_cookie_exists:
#         cookies = check_cookie_exists
#         cookie_cache = True
#     else:
#         place = swiggy.pin_to_place()
#         place_info = swiggy.place_id_to_lat_long(place['placeId'])
#         cookies = swiggy.encode_cookie_value(address=place_info['address'], lat=place_info['lat'], long=place_info['long'])

#     if keyword:
#         swiggy.search_keyword(cookies=cookies, page_number=0, offset=0)
#         result = swiggy.parse_listing_page()
#         result['requests'] = {'request_calls': swiggy.request_calls, 'total_requests': len(swiggy.request_calls), 'is_cookie_cached': cookie_cache}
#         return result
    
#     elif product_id or product_url:
#         store_id = swiggy.get_store_id(cookies=cookies)
#         print(store_id)
#         swiggy.search_product(cookies=cookies, store_id=store_id)
#         result = swiggy.parse_product_page()
#         result['requests'] = {'request_calls': swiggy.request_calls, 'total_requests': len(swiggy.request_calls), 'is_cookie_cached': cookie_cache}
#         return result
#     else:
#         return None



# result = main(pincode="560001", keyword="milk")
# print(result)
# swiggy.py
from curl_cffi import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from parsel import Selector
import json
import re
from datetime import datetime, timedelta

# ======================
# Global Config
# ======================
HEADERS = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'matcher': '8887c8ecbcc77dag9dfceca',
    'origin': 'https://www.swiggy.com',
    'priority': 'u=1, i',
    'referer': 'https://www.swiggy.com/instamart/search?custom_back=true',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'x-build-version': '2.291.0',
}

PROXIES = {
    "http": "http://51.222.241.206:8899",
    "https": "http://51.222.241.206:8899"
}

SESSION_TTL = timedelta(minutes=30)
active_sessions = {}

# ======================
# Retry Decorator
# ======================
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=4),
    retry=retry_if_exception_type(requests.RequestsError)
)
def _post_request(url, headers, cookies, data):
    response = requests.post(
        url,
        headers=headers,
        cookies=cookies,
        data=data,
        proxies=PROXIES,
        impersonate="edge99",
        timeout=30
    )
    if response.status_code >= 400:
        response.raise_for_status()
    return response

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=4),
    retry=retry_if_exception_type(requests.RequestsError)
)
def _get_request(url, headers, cookies):
    response = requests.get(
        url,
        headers=headers,
        cookies=cookies,
        proxies=PROXIES,
        impersonate="edge99",
        timeout=30
    )
    if response.status_code >= 400:
        response.raise_for_status()
    return response


# ======================
# Session Management
# ======================
def get_session(pincode: str):
    now = datetime.now()

    # Cleanup expired sessions
    expired = [pc for pc, s in active_sessions.items() if now - s["created_at"] > SESSION_TTL]
    for pc in expired:
        close_session(pc)

    if pincode in active_sessions:
        active_sessions[pincode]["last_used"] = now
        return active_sessions[pincode]

    # Fetch place_id from pincode
    try:
        place_url = f"https://www.swiggy.com/dapi/misc/place-autocomplete?input={pincode}&types="
        resp = requests.get(place_url, headers=HEADERS, impersonate="edge99")
        selector = Selector(resp.text)
        description = selector.jmespath('data[0].description').get()
        place_id = selector.jmespath('data[0].place_id').get()

        if not place_id:
            print(f"❌ Swiggy: No place found for pincode {pincode}")
            return None

        # Get lat/long
        geo_url = f"https://www.swiggy.com/dapi/misc/address-recommend?place_id={place_id}"
        resp = requests.get(geo_url, headers=HEADERS, impersonate="edge99")
        selector = Selector(resp.text)
        lat = selector.jmespath('data[0].geometry.location.lat').get()
        lng = selector.jmespath('data[0].geometry.location.lng').get()
        address = selector.jmespath('data[0].formatted_address').get()

        if not lat or not lng:
            print("❌ Swiggy: Failed to get coordinates")
            return None

        # Encode cookie
        user_location_str = json.dumps({'address': address, 'lat': lat, 'lng': lng})
        user_location_encoded = requests.utils.quote(user_location_str)
        cookies = {
            'userLocation': user_location_encoded,
            '_device_id': 'd947c398-bb67-304e-dc06-40b7d5353ea7',
            'tid': 's%3A8a4b299d-d634-4b7c-a034-df172f6026ae.MPMXIaIGoYrbjlHQDVcjCChhgj5f52cWcJRt9WpsyNk',
        }

        # Get storeId
        home_url = "https://www.swiggy.com/instamart"
        resp = _get_request(home_url, headers=HEADERS, cookies=cookies)
        store_ids = re.findall(r'"storeId":"(\d+)"|"podId":"(\d+)"', resp.text)
        store_id = store_ids[0][0] if store_ids and store_ids[0][0] else (store_ids[0][1] if store_ids else None)

        if not store_id:
            print("❌ Swiggy: Could not find storeId")
            return None

        session = {
            "cookies": cookies,
            "lat": lat,
            "long": lng,
            "address": address,
            "store_id": store_id,
            "created_at": now,
            "last_used": now
        }
        active_sessions[pincode] = session
        print(f"✅ Swiggy session created for pincode {pincode}")
        return session

    except Exception as e:
        print(f"❌ Swiggy init failed: {e}")
        return None


def close_session(pincode: str):
    if pincode in active_sessions:
        print(f"🗑️ Closed Swiggy session for {pincode}")
        del active_sessions[pincode]


# ======================
# Search Function
# ======================
def search_in_active_session(keyword: str, pincode: str):
    session = get_session(pincode)
    if not session:
        return []

    try:
        url = f"https://www.swiggy.com/api/instamart/search?pageNumber=0&searchResultsOffset=0&limit=40&query={keyword}&pageType=INSTAMART_AUTO_SUGGEST_PAGE&isPreSearchTag=false"
        payload = json.dumps({"facets": {}, "sortAttribute": ""})

        resp = _post_request(url, HEADERS, session["cookies"], payload)
        if resp.status_code != 200:
            return []

        selector = Selector(resp.text)
        if selector.jmespath('statusCode').get() != 0:
            return []

        items_data = selector.jmespath('data.widgets[0].data').getall()
        products = []

        for item in items_data:
            if not item.get("variations"):
                continue

            # Use first variation if single
            if len(item["variations"]) == 1:
                var = item["variations"][0]
                var.update({k: v for k, v in item.items() if k != "variations"})
                item = var

            name = item.get("name", "N/A")
            price = f"₹{item.get('pricing', {}).get('price', 'N/A')}"
            mrp_val = item.get("pricing", {}).get("mrp", "N/A")
            mrp = f"₹{mrp_val}" if mrp_val != "N/A" else "N/A"
            quantity = item.get("quantity", "N/A")

            images = item.get("images", [])
            image_url = f"https://media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,w_252,h_272/{images[0]}" if images else ""

            product_id = item.get("id", "")
            url = f"https://www.swiggy.com/product/{product_id}?storeId={session['store_id']}"

            products.append({
                "source": "Swiggy Instamart",
                "name": name,
                "price": price,
                "mrp": mrp,
                "quantity": quantity,
                "delivery_time": "8-15 mins",  # Instamart default
                "url": url,
                "image_url": image_url
            })

        return products

    except Exception as e:
        print(f"❌ Swiggy search error: {e}")
        return []