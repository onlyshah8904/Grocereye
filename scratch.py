from DrissionPage import Chromium
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
import requests
resp = requests.post(f"https://ea945e4019e3.ngrok-free.app/init-location?pincode=560001")

print(resp.status_code)
print(resp.text)