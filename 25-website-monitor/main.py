import argparse
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def check_url(url: str, timeout: float = 5.0, opener=urlopen) -> dict:
    started = time.perf_counter()
    try:
        request = Request(url, headers={"User-Agent": "PythonPortfolioMonitor/1.0"})
        with opener(request, timeout=timeout) as response:
            status = response.status
        elapsed_ms = round((time.perf_counter() - started) * 1000, 1)
        return {"url": url, "available": status < 500, "status": status, "response_ms": elapsed_ms}
    except HTTPError as error:
        elapsed_ms = round((time.perf_counter() - started) * 1000, 1)
        return {"url": url, "available": error.code < 500, "status": error.code, "response_ms": elapsed_ms}
    except URLError as error:
        elapsed_ms = round((time.perf_counter() - started) * 1000, 1)
        return {"url": url, "available": False, "status": None, "response_ms": elapsed_ms, "error": str(error)}


def main() -> None:
    parser = argparse.ArgumentParser(description="Check website availability")
    parser.add_argument("url")
    parser.add_argument("--timeout", type=float, default=5.0)
    args = parser.parse_args()
    result = check_url(args.url, args.timeout)
    print(result)
    raise SystemExit(0 if result["available"] else 1)


if __name__ == "__main__":
    main()
