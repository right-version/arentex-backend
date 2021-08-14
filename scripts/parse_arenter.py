from bs4 import BeautifulSoup
import bs4
import requests
import pandas as pd
from tqdm import tqdm


def parse_product_images(page: bs4.BeautifulSoup) -> list[str]:
    images = page.select(".product-simple__thumbslider-i>img")
    if not images:
        images.append(page.select(".product-simple__bigslider-i>a")[0]["href"])
    else:
        images = [image["src"].replace("thumb", "full") for image in images]
    return images


def parse_specs(page: bs4.BeautifulSoup):
    specs = {}
    for spec in page.select(".product-simple__spec-i"):
        specs[spec.select(".product-simple__spec-i-name")[0].getText().strip()] = (
            spec.select(".product-simple__spec-i-val")[0].getText().strip()
        )
    return specs


def parse_product(url: str):
    r = requests.get(url)
    page = BeautifulSoup(r.content, features="lxml")
    return {
        "название": page.select("ol.breadcrumbs>li")[-1].getText().strip(),
        "категория": page.select("ol.breadcrumbs>li")[-3].getText().strip(),
        "подкатегория": page.select("ol.breadcrumbs>li")[-2].getText().strip(),
        "описание": page.select(".product-simple__fulldesc-text")[0].getText(),
        "картинки": parse_product_images(page),
        "характеристики": parse_specs(page),
    }


def get_categories(url: str) -> dict[str, str]:
    r = requests.get(url)
    page = BeautifulSoup(r.content, features="lxml")

    categories = {}
    for category in page.select(".catlist__content"):
        content = category.select(".link_catalog")[0]
        categories[content.getText().strip()] = content["href"]

    return categories


def get_products_links(page: bs4.BeautifulSoup) -> list[str]:
    links = [link["href"] for link in page.select(".product-i__name")]
    return links


if __name__ == "__main__":

    url_base = "https://arenter.ru"

    categories = get_categories(f"{url_base}/catalog/")
    links = []
    print("[1/2] Парсинг ссылок на страницы товаров\n")
    for category, category_url in categories.items():
        print(f"Получение ссылок для категории: {category}")

        url = f"{url_base}{category_url}"

        r = requests.get(url)
        page = BeautifulSoup(r.content, features="lxml")
        pagination = page.select(".pagination__page")

        links.extend(get_products_links(page))

        for pagination_page in pagination[1:]:
            url = f"{url_base}{pagination_page['href']}"
            r = requests.get(url)
            page = BeautifulSoup(r.content, features="lxml")
            links.extend(get_products_links(page))

    print("[2/2] Парсинг страниц товаров\n")
    products = []
    for link in tqdm(links):
        product_link = f"{url_base}{link}"
        try:
            products.append(parse_product(product_link))
        except Exception as e:
            print(e)

    products = pd.DataFrame(products)
    products.to_csv("arenter.csv", index=False)
