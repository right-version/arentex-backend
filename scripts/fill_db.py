import os
import sys
import random
import time
from pathlib import Path
import ast

parentdir = os.path.dirname(".")
sys.path.insert(0, parentdir)
sys.path.insert(0, "..")

import pandas as pd

from app.models.models import Store, Category, Subcategory, Product
from app.db import SessionLocal
from app.config import get_settings
settings = get_settings()

arenter = pd.read_csv(Path(settings.PROJECT_ROOT) / "scripts" / "arenter.csv", converters={"images": eval})

stores = (
    {
        "title": "Супер шеринг 1",
        "description": "Описание",
        "phone": "+7(989)612-19-98",
        "address": "Ростов-на-Дону, Михаила Нагибина, дом 32д, корпус 2",
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    },
    {
        "title": "Супер шеринг 2",
        "description": "Описание",
        "phone": "+7(989)612-19-98",
        "address": "Ростов-на-Дону, Пойменная, дом 1, корпус м",
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    },
    {
        "title": "Супер шеринг 3",
        "description": "Описание",
        "phone": "+7(989)612-19-98",
        "address": "Ростов-на-Дону, Космонавтов, дом 2, корпус 2",
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    },
    {
        "title": "Супер шеринг 4",
        "description": "Описание",
        "phone": "+7(989)612-19-98",
        "address": "Ростов-на-Дону, Малиновского, дом 27, корпус А",
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    },
    {
        "title": "Супер шеринг 5",
        "description": "Описание",
        "phone": "+7(989)612-19-98",
        "address": "Ростов-на-Дону, 40-летия Победы, дом 85",
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    },
    {
        "title": "Супер шеринг 6",
        "description": "Описание",
        "phone": "+7(989)612-19-98",
        "address": "Ростов-на-Дону, Толстого, дом 6, корпус а",
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    },
    {
        "title": "Супер шеринг 7",
        "description": "Описание",
        "phone": "+7(989)612-19-98",
        "address": "Ростов-на-Дону, проспект Сельмаш, дом 98/11",
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    },
    {
        "title": "Супер шеринг 8",
        "description": "Описание",
        "phone": "+7(989)612-19-98",
        "address": "Ростов-на-Дону, Ворошиловский, пр-кт, дом 87, корпус 65",
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    },
    {
        "title": "Супер шеринг 9",
        "description": "Описание",
        "phone": "+7(989)612-19-98",
        "address": "Ростов-на-Дону, Королева, дом 14, корпус А",
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    },
    {
        "title": "Супер шеринг 10",
        "description": "Описание",
        "phone": "+7(989)612-19-98",
        "address": "Ростов-на-Дону, Красноармейская, дом 157",
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    },
    {
        "title": "Супер шеринг 11",
        "description": "Описание",
        "phone": "+7(989)612-19-98",
        "address": "Ростов-на-Дону, Стачки, дом 25",
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    },
    {
        "title": "Супер шеринг 12",
        "description": "Описание",
        "phone": "+7(989)612-19-98",
        "address": "Ростов-на-Дону, Малиновского, дом 25",
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    },
    {
        "title": "Супер шеринг 13",
        "description": "Описание",
        "phone": "+7(989)612-19-98",
        "address": "Ростов-на-Дону, Михаила Нагибина, дом 17",
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    },
    {
        "title": "Супер шеринг 14",
        "description": "Описание",
        "phone": "+7(989)612-19-98",
        "address": "Ростов-на-Дону, Зорге, дом 33",
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    },
)

def rename_image_url(url):
    parts = url.split("/")
    return f"/{parts[1]}/{parts[-2]}/{parts[-1]}"


def str_time_prop(start, end, time_format, prop):

    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, "%m/%d/%Y %I:%M %p", prop)


if __name__ == "__main__":
    categories = arenter["category"].unique()
    subcategories = arenter["subcategory"].unique()

    db = SessionLocal()

    print("[1/4] Adding categories")
    for category in categories:
        exists = db.query(Category).filter_by(name=category).first() is not None
        if not exists:
            new_category = Category(name=category)
            db.add(new_category)
            db.commit()
            db.refresh(new_category)

    print("[2/4] Adding subcategories")
    categories = db.query(Category.id, Category.name).all()
    for category in categories:
        subcategories = arenter[arenter["category"] == category[1]]["subcategory"].unique()
        for subcategory in subcategories:
            exists = db.query(Subcategory).filter_by(name=subcategory).first() is not None
            if not exists:
                new_subcategory = Subcategory(name=subcategory, category_id=category[0])
                db.add(new_subcategory)
                db.commit()
                db.refresh(new_subcategory)
            # new_subcategory = Subcategory(name=subcategory, category_id=category[0])
    # for subcategory in subcategories:
    #     exists = db.query(Subcategory).filter_by(name=category).first() is not None
        # if not exists:
        #     new_subcategory = Subcategory(name=subcategory)
        #     db.add(new_subcategory)
        #     db.commit()
        #     db.refresh(new_subcategory)

    print("[3/4] Adding stores")
    for store in stores:
        exists = db.query(Store).filter_by(title=store["title"]).first() is not None
        if not exists:
            new_store = Store(**store)
            db.add(new_store)
            db.commit()
            db.refresh(new_store)

    categories = db.query(Category.id, Category.name).all()
    subcategories = db.query(Subcategory.id, Subcategory.name).all()
    stores = db.query(Store.id).all()

    store_id = (random.sample(stores, k=1))[0][0]

    print("[4/4] Adding products")
    for _, row in arenter.iterrows():
        store_id = (random.sample(stores, k=1))[0][0]
        category_id = next(c for c in categories if c[1] == row["category"])[0]
        subcategory_id = next(c for c in subcategories if c[1] == row["subcategory"])[0]

        row["images"] = [rename_image_url(url) for url in row["images"]]
        new_product = Product(
            title=row["title"],
            description=row["description"],
            price=random.uniform(200, 1500),
            images=row["images"],
            thumbnail=row["images"][0].replace("full", "thumb"),
            date=random_date("1/1/2021 1:30 PM", "1/11/2021 4:50 AM", random.random()),
            specifications=ast.literal_eval(row["specifications"]),
            store_id=store_id,
            category_id=category_id,
            subcategory_id=subcategory_id
        )
        if category_id in [11, 1, 5]:
            new_product.popularity = random.uniform(0.71, 0.999)
        else:
            new_product.popularity = random.uniform(0.4, 0.70)
        db.add(new_product)
        db.commit()
        db.refresh(new_product)

    db.close()
