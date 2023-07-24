import logging
import sys
import textwrap

from bs4 import BeautifulSoup

from util.LoggingColorized import ColorHandler
from util.util import extract_byline, find_file

FILENAME = "intermediate.html"
DIRECTORY_PATH = "./resources/"

logging.getLogger().setLevel(logging.DEBUG)

# Create an instance of ColorHandler
color_handler = ColorHandler()

# Add the ColorHandler to the root logger
logging.getLogger().addHandler(color_handler)


def handle_url_requests(input_url):
    import requests

    # this line will fail the tests
    retrieve_page = requests.get(input_url)

    if retrieve_page.status_code != 200:
        logging.error("Something is Wrong with the provided input Url. please open a browser and check whether it's valid")
        sys.exit()

    # with os.scandir(DIRECTORY_PATH) as entries:
    #     for entry in entries:
    #
    #         if entry.is_file():
    #             entry_name = entry.name
    #             print(entry_name)
    #             if entry_name == FILENAME:
    #                 logging.info("file found")
    #                 break
    #             else:
    #                 # create file
    #                 logging.warning("file not found. creating new file")
    #                 file = open(DIRECTORY_PATH + "intermediate.html", "w")
    #                 file.close()
    #                 logging.info("file created")

    check_for_file = find_file(DIRECTORY_PATH, "intermediate.html")
    entry_name = "intermediate.html"

    if check_for_file:
        logging.info("file found")
    else:
        # create file
        logging.warning("file not found. creating new file")
        file = open(DIRECTORY_PATH + "intermediate.html", "w")
        file.close()
        logging.info("file created")

    with open(DIRECTORY_PATH + entry_name, "w") as file:
        logging.info("writing contents of web page to file")
        file.write(str(retrieve_page.text))
        logging.info("done writing")
    file.close()


def scraper(input_url):
    """
    go into the file, find body
    :param input_url:
    :return: string
    """

    content = []

    # handle Url here
    handle_url_requests(input_url)

    file_path = DIRECTORY_PATH + FILENAME

    with open(file_path) as file:
        soup = BeautifulSoup(file, "html.parser")

    title = soup.title.text

    byline_name = extract_byline(soup)

    paragraphs = soup.body.find_all("p")

    if len(paragraphs) > 0:
        for p in paragraphs:
            content.append(p.text)

    body_content = "".join(paragraph for paragraph in content)
    body_content = textwrap.fill(body_content, width=100)

    scraped_content = f"""
        {title}
            
        {byline_name}
            
        {body_content}
    """

    # append the content to the file
    text_file_path = DIRECTORY_PATH + "test.txt"
    with open(text_file_path, "w") as file:
        file.write(scraped_content)
    file.close()

    # join the content, body and byline here

    return scraped_content


def main():
    """
    take input , pass it to scraper
    :return:
    """
    if len(sys.argv) < 2:
        logging.error("Url cannot be empty")
        sys.exit()

    url = sys.argv[1]

    # try doing it for 2 more links at the same time , use multithreading ?

    logging.info("Scraping has started")
    print(scraper(url))
    logging.info("Scraping has ended")


if __name__ == '__main__':
    # time it , perf improvement?
    main()
