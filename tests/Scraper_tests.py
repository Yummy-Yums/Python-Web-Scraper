import unittest
from unittest.mock import patch

import requests

from util.util import find_file, compare_content

from Scraper import (
    handle_url_requests,
    scraper,
    FILENAME,
    DIRECTORY_PATH
)


class MyTestCase(unittest.TestCase):

    # for some reason, a period is prepended before the path

    def setUp(self):
        path = '.' + DIRECTORY_PATH
        #     check if text file is created, if not create it
        self.check_for_test_file = find_file(path, "test.txt")
        self.check_for_test_html_file = find_file(path, FILENAME)

    def test_whether_resource_files_exist(self):
        expected = [
            "../resources/test.txt",
            "../resources/intermediate.html"
        ]
        self.assertEqual(self.check_for_test_file, expected[0])
        self.assertEqual(self.check_for_test_html_file, expected[1])

    @patch('sys.exit')
    def test_handle_url_requests(self, mock_exit):
        urls = [
            "https://lost.gh.org",

        ]
        failure_msg = 'Expected to find file before running'

        # run the handle url , check whether both files are identical

        with self.assertRaises(requests.exceptions.MissingSchema) as cm:
            handle_url_requests("")

        with self.assertRaises(requests.exceptions.ConnectionError) as cm2:
            handle_url_requests(urls[0])

        exception_one = cm.exception.args[0]
        exception_two = cm2.exception.args[0]

        error_msg1 = "Invalid URL '': No scheme supplied. Perhaps you meant https://?"
        error_msg2 = "MaxRetryError('HTTPSConnectionPool(host=\\'lost.gh.org\\', port=443): Max retries exceeded with url: / (Caused by NameResolutionError(\"<urllib3.connection.HTTPSConnection object at 0x7f6b01ff4d90>: Failed to resolve \\'lost.gh.org\\' ([Errno -2] Name or service not known)\"))')"

        start_index = error_msg2.find("MaxRetryError('HTTPSConnectionPool(host='")
        end_index = error_msg2.find("):") + 2

        extracted_message = error_msg2[start_index:end_index]

        self.assertEqual(exception_one, error_msg1)
        self.assertEqual(str(exception_two)[start_index:end_index], extracted_message)

    def test_scraper(self):
        Urls = [
            "https://edition.cnn.com/travel/article/scenic-airport-landings-2020/index.html",
            "https://www.washingtonpost.com/technology/2020/09/25/privacy-check-blacklight/",
            "https://www.reuters.com/article/us-health-coronavirus-global-deaths/global-coronavirus-deaths-pass-agonizing-milestone-of-1-million-idUSKBN26K08Y",
            "https://www.nytimes.com/2020/09/02/opinion/remote-learning-coronavirus.html?action=click&module=Opinion&pgtype=Homepage"
        ]

        for link in Urls:
            scraped_content = scraper(link)
            get_file = find_file('../resources/', "test.txt")
            content_compared = compare_content(get_file, scraped_content)

            self.assertEqual(content_compared, True)

    # test for util methods


if __name__ == '__main__':
    unittest.main()
