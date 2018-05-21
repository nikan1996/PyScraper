import unittest
from scrapy import signals
from scrapy.utils.test import get_crawler

from PyScraper.middlewares.extensions.addslot import AddSlot, NotConfigured

try:
    from unittest import mock
except ImportError:
    import mock


class AddSlotTest(unittest.TestCase):

    @mock.patch('crawl_engine.extensions.addslot.Slot')
    def test_add_slot(self, mock_slot):
        settings = {
            'SPIDER_CLOSE_DELAY': 10,
            'ADDSLOT_ENABLED': True,
            'RANDOMIZE_DOWNLOAD_DELAY': True,
            'SLOTS': {
                'your_slot1': {'concurrency': 2, 'delay': 0},
                'your_slot2': {'concurrency': 3, 'delay': 1}
            }
        }
        def side_effect(*args, **kwargs):
            if args[1] == 0:  # your_slot1.delay
                return {'concurrency': 2, 'delay': 0}
            if args[1] == 1:  # your_slot2.delay
                return {'concurrency': 3, 'delay': 1}
        crawler = get_crawler(settings_dict=settings)
        crawler.engine = mock.Mock()
        pptmk = mock.PropertyMock(return_value={})
        type(crawler.engine.downloader).slots = pptmk
        add_slot = AddSlot.from_crawler(crawler)
        mock_slot.side_effect = side_effect
        assert add_slot is not None
        add_slot.spider_opened(None)
        assert add_slot.downloader_slots.get('your_slot1') is not None
        assert add_slot.downloader_slots.get('your_slot2') is not None
        assert add_slot.downloader_slots.get('your_slot1').get('concurrency') is 2
        assert add_slot.downloader_slots.get('your_slot1').get('delay') is 0

    def test_notconfigured(self):
        crawler = get_crawler()
        self.assertRaises(NotConfigured, AddSlot.from_crawler, crawler)

    def test_init(self):
        settings = {
            'ADDSLOT_ENABLED': True,
            'RANDOMIZE_DOWNLOAD_DELAY': False
        }
        crawler = get_crawler(settings_dict=settings)
        crawler.signals.connect = mock.Mock()
        obj = AddSlot(crawler)
        self.assertFalse(obj.randomize_delay)
        crawler.signals.connect.assert_called_with(obj.spider_opened, signal=signals.spider_opened)
