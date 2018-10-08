import urllib.request

TIMEOUT = 5


def get_ipv4() -> str:
    try:
        with urllib.request.urlopen('http://ipv4.myexternalip.com/raw', timeout=TIMEOUT) as f:
            if f.status != 200:
                raise Exception
            return f.read().decode().strip()
    except Exception:
        return None


def get_ipv6():
    try:
        with urllib.request.urlopen('http://ipv6.myexternalip.com/raw', timeout=TIMEOUT) as f:
            if f.status != 200:
                raise Exception
            return f.read().decode().strip()
    except Exception:
        return None
