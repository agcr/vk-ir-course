from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

from parsers.common import num_stars_to_rating_mapping

class CssSelectorParser:
    def _get_text_content(self, root, selector, attribute=None, regex=None):
        result = root.select_one(selector)
        if not result:
            return None
        if attribute is not None:
            result = result.attrs.get(attribute)
            if result is None:
                return None
        else:
            result = result.text
        if not regex:
            return result.strip()
        match = re.search(regex, result)
        if match:
            return match.group().strip()

    def _parse_product_page(self, root):
        result = {}
        result['title'] = self._get_text_content(root, 'title')
        result['description'] = self._get_text_content(root, 'meta[name="description"]', attribute='content')
        result['genre'] = self._get_text_content(root, '.breadcrumb > li:nth-child(3) > a')
        product_main = root.select_one('div.product_main')
        price_text = self._get_text_content(product_main, 'p.price_color', regex='[0-9\.]+')
        if price_text is None:
            raise RuntimeError('Failed to parse price')
        result['price'] = float(price_text)
        instock_text = self._get_text_content(product_main, 'p.instock.availability', regex='\d+')
        if instock_text is None:
            raise RuntimeError('Failed to parse available_stock')
        result['available_stock'] = int(instock_text)
        num_stars_elem = product_main.select_one('.product_main .star-rating')
        if not num_stars_elem:
            raise RuntimeError('Failed to parse rating')
        result['rating'] = num_stars_to_rating_mapping.get(num_stars_elem.attrs.get('class', [None, None])[1])
        return result

    def _get_next_links(self, root, cur_page_url):

        def get_url(elem):
            url = elem.attrs.get('href')
            if url:
                return urljoin(cur_page_url, url)
        next = []
        # ссылки на товары
        for elem in root.select('.product_pod a[title]'):
            url = get_url(elem)
            if url:
                next.append(url)
        # след. страница
        next_page = root.select_one('li.next > a')
        if next_page is not None:
            url = get_url(next_page)
            if url:
                next.append(url)
        return next

    def parse(self, content, cur_page_url):
        soup = BeautifulSoup(content, 'html.parser')
        product_page_root = soup.select_one('article.product_page')
        result = None
        if product_page_root:
            result = self._parse_product_page(soup)
            return result, []
        next = self._get_next_links(soup, cur_page_url)
        return None, next
