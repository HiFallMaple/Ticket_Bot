import threading
import time
import requests
import json
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, timedelta
from crypto import decrypt, encrypt
from captcha_resolver import solve_captcha
from config import CRYPTED_EVENTID, SCHEDULE_TIME, TICKET_COUNT, ENABLE_TICKET_AREA, INTERVAL


req = requests.Session()

headers = {
    'authority': 'apis.ticketplus.com.tw',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,tr;q=0.6,ja;q=0.5,zh-CN;q=0.4',
    'content-type': 'application/json',
    'dnt': '1',
    'origin': 'https://ticketplus.com.tw',
    'referer': 'https://ticketplus.com.tw/',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}


def get_timestamp() -> str:
    return str(int(time.time()*1000))


def get_login_payload() -> dict:
    with open("account.json", 'r', encoding='utf-8') as file:
        return json.load(file)


def verify_token(token: str) -> bool:
    params = {
        '_': get_timestamp(),
    }
    json_data = {
        'token': token,
    }
    response = req.post('https://apis.ticketplus.com.tw/user/api/v1/token',
                        params=params, headers=headers, json=json_data)
    result = json.loads(response.text)
    return result['errCode'] == '00'


def get_ticket_area_info(products: dict):
    params = {
        'ticketAreaId': ','.join([i["ticketAreaId"] for i in products["products"]]),
        'productId': ','.join([i["productId"] for i in products["products"]]),
        '_': get_timestamp(),
    }
    response = requests.get(
        'https://apis.ticketplus.com.tw/config/api/v1/get', params=params, headers=headers)
    data = json.loads(response.text)
    return data


def print_ticket_area_info(products: dict):
    data = get_ticket_area_info(products)
    # print(data)
    for i in data["result"]["ticketArea"]:
        print("ticketAreaName:", i["ticketAreaName"], end="")
        print(", price:", i["price"], end="")
        if "count" in i:
            print(", count:", i["count"])
        else:
            print()


def reserve_ticket(event: threading.Event, productId: str, captcha_key: str, captcha: str, ticket_area_name: str = None):
    params = {
        '_': get_timestamp(),
    }
    json_data = {
        'products': [
            {
                'productId': productId,
                'count': TICKET_COUNT,
            },
        ],
        'captcha': {
            'key': captcha_key,
            'ans': captcha,
        },
        "consecutiveSeats": True,
        "finalizedSeats": True,
        "reserveSeats": True
    }
    while not event.is_set():
        time.sleep(INTERVAL)
        response = req.post('https://apis.ticketplus.com.tw/ticket/api/v1/reserve',
                            params=params, headers=headers, json=json_data)
        data = json.loads(response.text)
        if ENABLE_TICKET_AREA:
            print(f"{ticket_area_name}: ", end="")
        print(f"{data}")
        if data["errCode"] == "00" or data["errCode"] == "111":
            event.set()
            return


def start_reserve(products: dict):
    product = products["products"][0]
    crypted_sessionId = product["sessionId"]
    
    captcha_key, captcha_svg = get_captcha(crypted_sessionId)
    captcha = solve_captcha(captcha_svg)
    print("CAPTCHA:", captcha)
    event = threading.Event()
    
    threads = []
    for i in range(len(products["products"])):
        thread = threading.Thread(target=reserve_ticket, args=(
           event, products["products"][i]["productId"], captcha_key, captcha, ticket_area_name[i] if ENABLE_TICKET_AREA else None,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


def get_captcha(crypted_sessionId: str, refresh: bool = False):
    params = {
        '_': get_timestamp(),
    }

    json_data = {
        'refresh': refresh,
        'sessionId': decrypt(crypted_sessionId),
    }

    response = req.post('https://apis.ticketplus.com.tw/captcha/api/v1/generate',
                        params=params, headers=headers, json=json_data)
    data = json.loads(response.text)
    captcha_key = data["key"]
    return captcha_key, str(data['data'])

def login():
    params = {
        '_': get_timestamp(),
    }

    json_data = get_login_payload()

    response = req.post('https://apis.ticketplus.com.tw/user/api/v1/login',
                        params=params, headers=headers, json=json_data)
    token = json.loads(response.text)["userInfo"]["access_token"]
    headers["Authorization"] = f"Bearer {token}"


def get_products():
    response = req.get(
        f'https://apis.ticketplus.com.tw/config/api/v1/getS3?path=event/{CRYPTED_EVENTID}/products.json',
        headers=headers,
    )
    return json.loads(response.text)


if __name__ == "__main__":
    scheduler = BlockingScheduler()
    # login
    scheduler.add_job(login, 'date', run_date=SCHEDULE_TIME-timedelta(seconds=30))
    # login()

    # get events info
    response = req.get(
        f'https://apis.ticketplus.com.tw/config/api/v1/getS3?path=event/{CRYPTED_EVENTID}/sessions.json',
        headers=headers,
    )

    data = json.loads(response.text)
    # for i in data["sessions"]:
    #     print(i)


    # get products
    products = get_products()
    
    for i in products["products"]:
        print(i)

    # ticketAreas
    if ENABLE_TICKET_AREA:
        print_ticket_area_info(products)
        ticket_area_name = [i["ticketAreaName"]
                            for i in get_ticket_area_info(products)["result"]["ticketArea"]]

    # start_reserve(products)

    # scheduler = BlockingScheduler()
    scheduler.add_job(start_reserve, 'date', run_date=SCHEDULE_TIME, args=(products,))
    scheduler.print_jobs()
    scheduler.start()