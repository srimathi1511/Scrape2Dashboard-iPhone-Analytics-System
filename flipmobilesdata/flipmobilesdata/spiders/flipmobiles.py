import scrapy

class FlipmobilesSpider(scrapy.Spider):
    name = "flipmobiles"

    start_urls = [
        "https://www.flipkart.com/search?q=iphone&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=1"
    ]

    def parse(self, response):
        products = response.css('div.ZFwe0M')

        for product in products:
            # ---------- SAFE INITIALIZATION ----------
            product_name = None
            color = None

            name = product.css('div.RG5Slk::text').get()

            if name:
                if '(' in name and ')' in name:
                    product_name = name.split('(')[0].strip()
                    inside = name.split('(')[1].split(')')[0]
                    color = inside.split(',')[0].strip()
                else:
                    product_name = name.strip()

            # ---------- SPECS ----------
            specs = product.css('ul.HwRTzP li::text').getall()
            specs_dict = {
                'ROM': specs[0] if len(specs) > 0 else None,
                'Display': specs[1] if len(specs) > 1 else None,
                'Camera': specs[2] if len(specs) > 2 else None,
                'Processor': specs[3] if len(specs) > 3 else None,
                'Warranty': specs[4] if len(specs) > 4 else None
            }

            # ---------- RATINGS & REVIEWS ----------
            text = ''.join(
                product.css('span.PvbNMB span span::text').getall()
            ).replace('\xa0', '').strip()

            ratings, reviews = None, None
            if 'Ratings' in text:
                parts = text.split('Ratings')
                ratings = parts[0].strip()
                reviews = parts[1].replace('&', '').replace('Reviews', '').strip() if len(parts) > 1 else None

            # ---------- YIELD ----------
            yield {
                'name': product_name,
                'colour': color,
                'specs': specs_dict,
                'selling_price': product.css('div.hZ3P6w::text').get(),
                'original_price': ''.join(
                    product.css('div.kRYCnD *::text').getall()
                ).strip(),
                'ratings_count': ratings,
                'reviews_count': reviews
            }

        # ---------- PAGINATION (till page 30) ----------
        current_page = int(response.url.split('page=')[-1])
        if current_page < 30:
            next_page = response.url.replace(
                f'page={current_page}', f'page={current_page + 1}'
            )
            yield response.follow(next_page, callback=self.parse)
