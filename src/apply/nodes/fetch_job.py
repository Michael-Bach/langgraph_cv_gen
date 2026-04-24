import httpx
from bs4 import BeautifulSoup
from apply.state import ApplyState

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}


def fetch_job(state: ApplyState) -> dict:
    """Fetch job posting text from a URL, or pass through pasted text.

    GETs the URL with httpx, strips HTML with BeautifulSoup (removes script/style).
    Falls back to state["job_text"] if the URL is empty or the request fails.
    Returns: {"job_text": str}
    """
    url = state.get("job_url", "")
    if not url:
        return {"job_text": state.get("job_text", "")}

    try:
        response = httpx.get(url, timeout=15, follow_redirects=True, headers=_HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        return {"job_text": soup.get_text(separator="\n", strip=True)}
    except Exception:  # intentionally broad: covers HTTP errors, parse failures, and timeouts
        return {"job_text": state.get("job_text", "")}
