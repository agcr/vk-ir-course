import asyncio
import logging
import time

from runners.async_runner import AsyncRunner
from runners.multithreaded_runner import MultiThreadedRunner
from runners.simple_runner import SimpleRunner
from parsers.css_selector_parser import CssSelectorParser
from parsers.xpath_parser import XPathParser
from utils.file_sink import FileSink

def main():
    logging.basicConfig(
        format='[%(asctime)s] %(name)s %(levelname)s: %(message)s',
        datefmt='%d-%m-%y %H:%M:%S',
        level='INFO',
    )
    logger = logging.getLogger('Runner')
    # главная - https://books.toscrape.com/index.html
    seed_urls = ['https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html']
    parser = CssSelectorParser()
    # parser = XPathParser()
    sink = FileSink('./result.jsonl')
    # runner = SimpleRunner(parser, sink, logger, seed_urls)
    runner = MultiThreadedRunner(parser, sink, logger, seed_urls, max_parallel=5)
    start = time.time()
    runner.run()
    logger.info(f'Total duration is {time.time() - start}')
    # async def run_async_crawl():
    #     runner = AsyncRunner(parser, sink, logger, seed_urls, rate=100, max_tries=5, max_parallel=5)
    #     start = time.time()
    #     await runner.run()
    #     logger.info(f'Total duration is {time.time() - start}')
    # asyncio.run(run_async_crawl())

if __name__ == '__main__':
    main()