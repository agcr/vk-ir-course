import aiohttp
import asyncio
import time

from utils.simple_rate_limiter import SimpleRateLimiter
from runners.utils import Item


class AsyncRunner:
    def __init__(self, parser, sink, logger, seed_urls, rate=100, max_parallel=5, max_tries=5):
        self._logger = logger.getChild('AsyncRunner')
        self._parser = parser
        self._sink = sink

        self._semaphore = asyncio.Semaphore(max_parallel)
        self._in_air = set()
        self._rate_limiter = SimpleRateLimiter(rate)
        self._seen = set()
        self._seed_urls = seed_urls
        self._max_tries = max_tries
        self._future_to_item = {}

    def _submit(self, item):
        item.start = time.time()
        future = asyncio.ensure_future(self._download(item))
        self._in_air.add(future)
        self._future_to_item[future] = item
        self._logger.info(f'Start: {item.url}')
        self._seen.add(item.url)

    async def _download(self, item):
        async with self._semaphore:
            await asyncio.sleep(self._rate_limiter.get_delay())
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60)) as session:
                async with session.get(item.url) as resp:
                    resp.raise_for_status()
                    content = await resp.text()
                    return self._parser.parse(content.encode(), str(resp.url))

    async def run(self):
        for elem in self._seed_urls:
            self._submit(Item(elem))
        while len(self._in_air) > 0:
            done, in_air = await asyncio.wait(self._in_air, return_when=asyncio.FIRST_COMPLETED)
            self._in_air = in_air
            for future in done:
                item = self._future_to_item.pop(future)
                try:
                    result, next = future.result()
                except Exception as e:
                    duration = time.time() - item.start
                    item.tries += 1
                    if item.tries > self._max_tries:
                        self._write(item, error=str(e))
                        self._logger.exception(f'Fail: {item.url} {e}. Tries = {item.tries}. Duration: {duration}s')
                        continue
                    self._submit(item)
                    self._logger.warning(f'Postpone: {item.url} {e}. Tries = {item.tries}. Duration: {duration}s')
                    continue
                if result is not None:
                    self._write(item, result=result)
                for elem in next:
                    if elem in self._seen:
                        continue
                    self._submit(Item(elem))
                self._logger.info(f'Success: {item.url}. Tries = {item.tries}. Duration: {time.time() - item.start}s')

    def _write(self, item, result=None, error=None):
        if result is None and error is None:
            raise RuntimeError('Invalid result. Both result and error are None')
        to_write = {'tries': item.tries, 'result': result, 'error': error}
        self._sink.write(to_write)
