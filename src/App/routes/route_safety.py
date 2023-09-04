import unicodedata

def url_has_allowed_host_and_scheme(url, allowed_hosts, require_https=False):
    if url is not None:
        url = url.strip()
    if not url:
        return False
    if allowed_hosts is None:
        allowed_hosts = set()
    elif isinstance(allowed_hosts, str):
        allowed_hosts = {allowed_hosts}
    # Chrome treats \ completely as / in paths but it could be part of some
    # basic auth credentials so we need to check both URLs.
    return (
        _url_has_allowed_host_and_scheme(url, allowed_hosts, require_https=require_https) and
        _url_has_allowed_host_and_scheme(url.replace('\\', '/'), allowed_hosts, require_https=require_https)
    )

def _url_has_allowed_host_and_scheme(url, allowed_hosts, require_https):
    print(f'_url_has_allowed_host_and_scheme(url={url})')
    print(f'_url_has_allowed_host_and_scheme(allowed_hosts={allowed_hosts})')
    print(f'_url_has_allowed_host_and_scheme(require_https={require_https})')
    return True
