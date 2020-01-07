from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from crawler.qqmail import QQMail
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

mail = QQMail("yangchun_he@qq.com","snbtdhhcsrxhdbdc")
subject = "Message from Andy's robot"
to = ["2388464282@qq.com","yangchun_he@hotmail.com"]
content = "Hello, \nI am Andy's robot! i want to let you know that your spiders completed all tasks\n"
if mail.sendTextMail(to,subject,content):
    print("Succeed!")


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
