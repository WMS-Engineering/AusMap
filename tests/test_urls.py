import os
import re
import unittest
import xml.etree.ElementTree as ET

import requests


class TestAusmapUrls(unittest.TestCase):

    def setUp(self):
        self.urls = self._extract_urls_from_qlr()

    def _extract_urls_from_qlr(self):
        qlr_file = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "ausmap.qlr"
        )
        tree = ET.parse(qlr_file)
        root = tree.getroot()
        url_pattern = r"url=(https?://[^\s&]+)"
        urls = set()

        for source in root.iter("datasource"):
            datasource = source.text
            url_match = re.search(url_pattern, datasource)
            if url_match:
                urls.add(url_match.group(1))

        return urls

    def test_urls(self):
        for url in self.urls:
            with self.subTest(url=url):
                try:
                    response = requests.get(url)
                    self.assertEqual(
                        response.status_code,
                        200,
                        f"❌ Link {url} is not working!",
                    )
                except requests.exceptions.RequestException as e:
                    self.fail(f"❌ Request to {url} failed: {e}")


if __name__ == "__main__":
    unittest.main()
