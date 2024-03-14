from typing import Mapping

def get_utm_params(params: Mapping[str, str]) -> str:
    utm_params = {
            'utm_source': params.get('utm_source'),
            'utm_medium': params.get('utm_medium'),
            'utm_campaign': params.get('utm_campaign'),
            'utm_content': params.get('utm_content'),
            'utm_term': params.get('utm_term')
            }
    utm_string = "&".join([f"{k}={v}" for k, v in utm_params.items() if v])
    return '?' + utm_string if utm_string else ''