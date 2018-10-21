import socket

TIMEOUT = 5


def get_ipv4() -> str:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(TIMEOUT)
            s.connect(('8.8.8.8', 80))

            return s.getsockname()[0]
    except Exception:
        return None


def get_ipv6():
    try:
        with socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) as s:
            s.settimeout(TIMEOUT)
            s.connect(('2001:4860:4860::8844', 80))

            return s.getsockname()[0]
    except Exception:
        return None
