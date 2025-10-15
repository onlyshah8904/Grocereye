# from DrissionPage import Chromium
# def set_location_via_pincode(pincode):
#     """
#     Automate location setting using pincode.
#     Updates global headers['lat'], headers['lon'], and cookies_dict
#     """
#     global cookies_dict
#     browser = Chromium(9992)

#     try:
#         tab = browser.latest_tab
#         tab.get('https://www.bigbasket.com/')
#         tab.refresh()

#         # Click on location bar
#         tab('@class=AddressDropdown___StyledMenuButton-sc-i4k67t-1 iXeMGW').click()
#         # Type pincode
#         elee = tab.ele('xpath://div[@class="AddressDropdown___StyledDiv-sc-i4k67t-5 cicNbD"]').click()
#         if elee:
#             elee.input(pincode)
#             # print("yayy")
#             # ele
#         # else:
#             # print("fucked")
#         tab.wait(1)

#         eles = tab.eles('xpath://*[contains(@class, "AddressDropdown___StyledMenuItem-sc-i4k67t-7")]')

#         if eles:
#             eles[0].click()
#             print(f"✅ Selected location for pincode: {pincode}")
#         else:
#             print("❌ No location suggestion found!")
#             return False

#         # Wait for cookies to update
#         tab.wait(2)
#         cookies = tab.cookies()
#         cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}
#         return True

#     except Exception as e:
#         print(f"❌ Automation error: {e}")
#         return False
#     finally:
#         browser.quit()


# print(set_location_via_pincode())

# def set_location_via_pincode(pincode):
#     """
#     Automate location setting using pincode.
#     Updates global headers['lat'], headers['lon'], and cookies_dict
#     """
#     global cookies_dict
#     browser = Chromium(9993)

#     try:
#         tab = browser.latest_tab
#         tab.get('https://blinkit.com/')

#         # Click on location bar
#         tab('@class=LocationBar__Container-sc-x8ezho-6 gcLVHe').click()

#         # Type pincode
#         ele = tab.ele('@name=select-locality')
#         ele.input(pincode)
#         tab.wait(2)
#         eles = tab.eles('@class=LocationSearchList__LocationDetailContainer-sc-93rfr7-1 bBiSUM')

#         if eles:
#             eles[0].click()
#             print(f"✅ Selected location for pincode: {pincode}")
#         else:
#             print("❌ No location suggestion found!")
#             return False

#         # Wait for cookies to update
#         tab.wait(2)
#         cookies = tab.cookies()
#         cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}

#         # Update headers with lat and lon
#         # if 'gr_1_lat' in cookies_dict:
#             # headers['lat'] = cookies_dict['gr_1_lat']
#             # headers['lon'] = cookies_dict['gr_1_lon']

#         # print(f"📍 Location set: lat={headers.get('lat')}, lon={headers.get('lon')}")
#         return True

#     except Exception as e:
#         print(f"❌ Automation error: {e}")
#         return False
#     finally:
#         browser.quit()



# print(set_location_via_pincode("380007"))


# import requests
# import json

# # Your API key
# API_KEY = "AIzaSyA8zupRIY4Ks798nZWTwJsl6ZBX6TVVAZE"

# # Gemini REST API endpoint (using gemini-2.0-flash)
# url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key={API_KEY}"

# # Request payload
# payload = {
#     "contents": [
#         {
#             "parts": [
#                 {
#                     "text": "Explain how photosynthesis works in simple terms."
#                 }
#             ]
#         }
#     ]
# }

# # Send POST request
# response = requests.post(url, json=payload)

# # Check response
# if response.status_code == 200:
#     data = response.json()
#     # Extract the generated text
#     print(data["candidates"][0]["content"]["parts"][0]["text"])
# else:
#     print("Error:", response.status_code, response.text)


# # import requests
# # import os

# # API_KEY = "AIzaSyDBur80fP-rgXq2rwPzHVt--_e8XFjsrKo"
# # url = f"https://generativelanguage.googleapis.com/v1/models?key={API_KEY}"

# # resp = requests.get(url)
# # if resp.status_code == 200:
# #     models = [m["name"] for m in resp.json()["models"] if "gemini" in m["name"]]
# #     print("Available Gemini models:")
# #     for m in models:
# #         print("-", m)
# # else:
# #     print("Failed to fetch models:", resp.status_code, resp.text)


from curl_cffi import requests

cookies = {
    '_gcl_au': '1.1.530568912.1753891512',
    '_fbp': 'fb.1.1753891517738.984019593957639801',
    'gr_1_deviceId': 'df39f219-9301-4ecf-823d-b60c0d05dfd8',
    'city': 'Ahmedabad',
    '__cf_bm': 'vVxyDNp6KrLmobCfgZkkRley41Ys29klj35IyvSjvqs-1760516700-1.0.1.1-5ZfEwNLLjyA5UYO9PnV9Szf4y3vd.TC.wVw0F59jpklW1JOWCI1g9nMiQj_q2GC7bh5lb0HIE.fj9j_iUzGAfGVUzj5Y7GJ3vUxbFf6Stms',
    '__cfruid': '23e907cbbeb80f4e6072555847bad3a6fcaadc29-1760516700',
    '_cfuvid': 'HX5bc6KVs2bIB2E1HAuebH8omqVgGD_bBuhCZkKnV9A-1760516700351-0.0.1.1-604800000',
    'gr_1_lat': '23.004474500000004',
    'gr_1_lon': '72.55311549999999',
    'gr_1_locality': 'Ahmedabad',
    'gr_1_landmark': 'undefined',
    '_gid': 'GA1.2.1564244292.1760516710',
    '_gat_UA-85989319-1': '1',
    '_ga': 'GA1.2.1673436691.1753891126',
    '_ga_DDJ0134H6Z': 'GS2.2.s1760516711$o8$g1$t1760516727$j44$l0$h0',
    '_ga_JSMJG966C7': 'GS2.1.s1760516710$o8$g0$t1760516727$j43$l0$h0',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'access_token': 'null',
    'app_client': 'consumer_web',
    'app_version': '1010101010',
    'auth_key': 'c761ec3633c22afad934fb17a66385c1c06c5472b4898b866b7306186d0bb477',
    # 'content-length': '0',
    'content-type': 'application/json',
    'device_id': '2a2ebd233ec0e3c1',
    'dnt': '1',
    'lat': '23.004474500000004',
    'lon': '72.55311549999999',
    'origin': 'https://blinkit.com',
    'priority': 'u=1, i',
    'referer': 'https://blinkit.com/s/?q=milk',
    'rn_bundle_version': '1009003012',
    'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'session_uuid': 'dfaa4a46-d67a-4145-9e07-fa6c3e3639e8',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
    'web_app_version': '1008010016',
    # 'cookie': '_gcl_au=1.1.530568912.1753891512; _fbp=fb.1.1753891517738.984019593957639801; gr_1_deviceId=df39f219-9301-4ecf-823d-b60c0d05dfd8; city=Ahmedabad; __cf_bm=vVxyDNp6KrLmobCfgZkkRley41Ys29klj35IyvSjvqs-1760516700-1.0.1.1-5ZfEwNLLjyA5UYO9PnV9Szf4y3vd.TC.wVw0F59jpklW1JOWCI1g9nMiQj_q2GC7bh5lb0HIE.fj9j_iUzGAfGVUzj5Y7GJ3vUxbFf6Stms; __cfruid=23e907cbbeb80f4e6072555847bad3a6fcaadc29-1760516700; _cfuvid=HX5bc6KVs2bIB2E1HAuebH8omqVgGD_bBuhCZkKnV9A-1760516700351-0.0.1.1-604800000; gr_1_lat=23.004474500000004; gr_1_lon=72.55311549999999; gr_1_locality=Ahmedabad; gr_1_landmark=undefined; _gid=GA1.2.1564244292.1760516710; _gat_UA-85989319-1=1; _ga=GA1.2.1673436691.1753891126; _ga_DDJ0134H6Z=GS2.2.s1760516711$o8$g1$t1760516727$j44$l0$h0; _ga_JSMJG966C7=GS2.1.s1760516710$o8$g0$t1760516727$j43$l0$h0',
}

params = {
    'offset': '12',
    'limit': '12',
    'last_snippet_type': 'product_card_snippet_type_2',
    'last_widget_type': 'listing_container',
    'page_index': '1',
    'q': 'milk',
    'search_count': '62',
    'search_method': 'basic',
    'search_type': 'type_to_search',
    'total_entities_processed': '1',
    'total_pagination_items': '62',
}

response = requests.post('https://blinkit.com/v1/layout/search', params=params, cookies=cookies, headers=headers,impersonate="edge101")
print(response.text)
print(response.status_code)
