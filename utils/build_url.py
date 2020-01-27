import urllib.parse


def build_url(url_base, params: dict) -> str:
    url_parts = list(urllib.parse.urlparse(url_base))
    query = dict(urllib.parse.parse_qsl(url_parts[4]))
    query.update(params)

    url_parts[4] = urllib.parse.urlencode(query)

    url = urllib.parse.urlunparse(url_parts)

    return url
