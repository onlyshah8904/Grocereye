# scraper.py
from blinkit import search_in_active_session as search_blinkit
from bigbasket import search_in_active_session as search_bigbasket
from threading import Thread

def scraper(keyword, pincode):
    r1, r2 = [], []
    t1 = Thread(target=lambda: r1.extend(search_blinkit(keyword, pincode)))
    t2 = Thread(target=lambda: r2.extend(search_bigbasket(keyword, pincode)))
    t1.start(); t2.start(); t1.join(); t2.join()
    return r1 + r2