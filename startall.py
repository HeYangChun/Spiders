from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from crawler.spiders.hslt import HsltSpider
from crawler.spiders.mllt import MlltSpider
from crawler.spiders.tpysylt import TpysyltSpider

process = CrawlerProcess(get_project_settings())
#spiders to crawl
process.crawl(HsltSpider)
process.crawl(MlltSpider)
process.crawl(TpysyltSpider)
#start
process.start()

#from twisted.internet import reactor
#from scrapy.crawler import CrawlerRunner
#from scrapy.utils.log import configure_logging
#from scrapy.utils.project import get_project_settings
#from crawler.spiders.hslt import HsltSpider
#from crawler.spiders.mllt import MlltSpider
#from crawler.spiders.tpysylt import TpysyltSpider
#
#runner = CrawlerRunner(get_project_settings())
#runner.crawl(HsltSpider)
#runner.crawl(MlltSpider)
#runner.crawl(TpysyltSpider)
#
#d = runner.join()
#
#d.addBoth(lambda _: reactor.stop())
#
#reactor.run()