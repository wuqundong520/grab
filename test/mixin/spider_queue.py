from unittest import TestCase

from grab.spider import Spider, Task, Data
from ..util import FakeServerThread, BASE_URL, RESPONSE, SLEEP

class SpiderQueueMixin(object):
    class SimpleSpider(Spider):
        def prepare(self):
            self.url_history = []
            self.priority_history = []

        def task_page(self, grab, task):
            self.url_history.append(task.url)
            self.priority_history.append(task.priority)

    def test_basic_priority(self):
        bot = self.SimpleSpider()
        #self.setup_queue(bot)
        bot.setup_queue(backend='memory')
        requested_urls = {}
        for priority in (4, 2, 1, 5):
            url = BASE_URL + '?p=%d' % priority
            requested_urls[priority] = url
            bot.add_task(Task('page', url=url,
                              priority=priority))
        bot.run()
        urls = [x[1] for x in sorted(requested_urls.items(), 
                                     key=lambda x: x[0])]
        self.assertEqual(urls, bot.url_history)

    def test_queue_length(self):
        bot = self.SimpleSpider()
        self.setup_queue(bot)
        for x in xrange(5):
            bot.add_task(Task('page', url=BASE_URL))
        self.assertEqual(5, bot.taskq.size())
        bot.run()
        self.assertEqual(0, bot.taskq.size())
        bot.run()