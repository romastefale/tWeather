import aiohttp

_session = None


async def get_http_session():
    global _session

    if _session is None or _session.closed:
        _session = aiohttp.ClientSession()

    return _session


async def close_http_session():
    global _session

    if _session and not _session.closed:
        await _session.close()
