import requests
import pandas as pd
import certifi
from scrapy.http import TextResponse
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as bs
import urllib.request as ur
import numpy as np
from config import get_secret

from models.information import Information
from pymongo import MongoClient
from config import MONGO_URL


from search_restaurant_url import restaurant, inform_restaurant


if __name__ == "__main__":
    ca = certifi.where()
    client = MongoClient(MONGO_URL, tlsCAFile=ca)

    db = client["test"]
    # print(db)
    urls = restaurant("충무로", 1)  # 3*n개의 url이 나옴
    # df = pd.DataFrame(columns=["이름", "분류", "분위기(테마키워드)", "주요 메뉴", "평균 가격", "평점", "리뷰 수"])
    for url in urls:

        result = inform_restaurant(url)
        # name = result["이름"]
        # sort = result["분류"]
        # mood = result["분위기(테마키워드)"]
        # menu = result["주요 메뉴"]
        # mean_price = result["평균 가격"]
        # point = result["평점"]
        # reviews = result["리뷰 수"]

        info = {
            "name": result["이름"],
            "sort": result["분류"],
            "mood": str(result["분위기(테마키워드)"]),
            "menu": result["주요 메뉴"],
            "mean_price": result["평균 가격"],
            "point": float(result["평점"]),
            "reviews": int(result["리뷰 수"]),
        }
        print(info)
        dpInsert = db.inform.insert_one(info)
        # df = pd.concat([df, pd.DataFrame(result)], ignore_index=False)
    print("finish!")
    print(info)
