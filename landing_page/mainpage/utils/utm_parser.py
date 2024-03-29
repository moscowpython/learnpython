from typing import Iterator


def get_utm_params(params: Iterator[tuple[str, ...]]) -> str:
    utm_string = "&".join([f"{k}={v.encode('utf-8').decode('utf-8')}" for k, v in params if v and "utm_" in k])
    return '?' + utm_string if utm_string else ''
