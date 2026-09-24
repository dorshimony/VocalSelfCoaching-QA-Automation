import os

import pytest

# כתובת האפליקציה. אפשר להחליף אותה בלי לגעת בקוד:
# Windows:  set APP_URL=http://localhost:8000/index.html
# Mac/Linux: export APP_URL=http://localhost:8000/index.html
APP_URL = os.environ.get("APP_URL", "https://dorselfvocalcoach.netlify.app/")


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """
    מפעיל את הדפדפן עם מיקרופון מדומה, כדי שאפשר יהיה לבדוק
    את המבחן הקולי בלי לדבר למיקרופון אמיתי.
    """
    args = dict(browser_type_launch_args)
    args["args"] = [
        "--use-fake-ui-for-media-stream",
        "--use-fake-device-for-media-stream",
        "--autoplay-policy=no-user-gesture-required",
    ]
    return args


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    מאשר מראש הרשאת מיקרופון לאתר.
    """
    args = dict(browser_context_args)
    args["permissions"] = ["microphone"]
    return args


@pytest.fixture
def app(page):
    """
    פותח את האפליקציה ומנקה נתונים שמורים, כדי שכל בדיקה
    תתחיל ממצב נקי — אבל אחרי מסך הפתיחה.
    """
    page.goto(APP_URL)
    page.evaluate("localStorage.clear()")
    # מסך הפתיחה מוצג רק למבקר חדש ומסתיר את הלשוניות.
    # רוב הבדיקות עוסקות בשאר האפליקציה, ולכן הן מתחילות אחריו.
    page.evaluate("localStorage.setItem('vsc_hero_seen_v1', '1')")
    page.reload()
    page.wait_for_selector("nav.tabs button")
    return page
