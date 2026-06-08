import logging

logger = logging.getLogger('metrics')

_metrics = {'total': 0, '2xx': 0, '4xx': 0, '5xx': 0}


class MetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        _metrics['total'] += 1
        status = response.status_code
        if 200 <= status < 300:
            _metrics['2xx'] += 1
        elif 400 <= status < 500:
            _metrics['4xx'] += 1
        elif 500 <= status < 600:
            _metrics['5xx'] += 1
        logger.info(
            f"[METRICS] total={_metrics['total']} | "
            f"2xx={_metrics['2xx']} | "
            f"4xx={_metrics['4xx']} | "
            f"5xx={_metrics['5xx']} | "
            f"last: {request.method} {request.path} -> {status}"
        )
        return response
