from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider

from billboard.items import BillboardItem


class BillboardSpider(BaseSpider):
    name = 'billboard'
    allowed_domains = ['billboard.com']

    def __init__(self):
        super(BillboardSpider, self).__init__()
        
        self.start_urls = ['http://www.billboard.com/charts/hot-100']
        for x in range(1, 9):
            self.start_urls.append('http://www.billboard.com/charts/hot-100?page={0}'.format(x))
#     
    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        articles = hxs.select('//article')
        items = []
        for article in articles:
            try:
                title = article.select('header/h1/text()').extract()[0].strip()
            except IndexError:
                continue
            
            peak = article.select('header/ul[@class="chart_stats"]/li/text()[2]')[0].extract().strip()
            if (int(peak) > 10):
                continue
            
            position = article.select('header/span/text()').extract()[0].strip()
            
            try:
                artist = article.select('header/p[@class="chart_info"]/a/text()').extract()[0].strip()
            except IndexError:
                artist = article.select('header/p[@class="chart_info"]/text()').extract()[0].strip()
                
            assert(bool(title) == True)
            assert(bool(position) == True)
            assert(bool(artist) == True)
            assert(bool(peak) == True)
            
            item = BillboardItem()
            item['title'] = title
            item['position'] = position
            item['artist'] = artist
            item['peak'] = peak
            
            items.append(item)
        return items