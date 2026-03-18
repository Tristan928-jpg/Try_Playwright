import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture
def page(request):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        yield page
        context.tracing.stop(path="trace.zip")
        if request.node.rep_call.failed:
            page.screenshot(path=f"screenshots/{request.node.name}.png")

        browser.close()
