from apply.state import ApplyState


def fetch_job(state: ApplyState) -> dict:
    """Fetch and return job posting text.

    If state["job_url"] is set, fetch via httpx and parse with BeautifulSoup.
    If the URL is blocked or empty, fall back to state["job_text"] as-is.
    Returns: {"job_text": str}
    """
    raise NotImplementedError
