# -*- coding: utf-8 -*-
"""
Cau hinh chung cho bo test Selenium:
- Fixture `driver`: khoi tao Chrome WebDriver cho moi test case.
- Ham ho tro: login(), screenshot().

Bien moi truong tuy chon:
- CHROME_BINARY : duong dan file chay Chrome/Chromium (mac dinh: Chrome cai san)
- CHROME_PROXY  : proxy cho trinh duyet, vd http://127.0.0.1:18080
- HEADLESS      : "1" (mac dinh) chay khong giao dien, "0" mo cua so trinh duyet
"""
import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = "https://www.saucedemo.com"
VALID_USER = "standard_user"
VALID_PASS = "secret_sauce"
SCREENSHOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screenshots")


@pytest.fixture()
def driver():
    opts = Options()
    binary = os.environ.get("CHROME_BINARY")
    if binary:
        opts.binary_location = binary
    if os.environ.get("HEADLESS", "1") == "1":
        opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1280,900")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    proxy = os.environ.get("CHROME_PROXY")
    if proxy:
        opts.add_argument(f"--proxy-server={proxy}")
        opts.add_argument("--ignore-certificate-errors")
    d = webdriver.Chrome(options=opts)
    d.implicitly_wait(5)
    yield d
    d.quit()


def login(driver, username=VALID_USER, password=VALID_PASS):
    """Mo trang chu va dang nhap voi tai khoan cho truoc."""
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 15)
    wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys(username)
    wait.until(EC.visibility_of_element_located((By.ID, "password"))).send_keys(password)
    wait.until(EC.element_to_be_clickable((By.ID, "login-button"))).click()


def login_success(driver):
    """Dang nhap hop le va cho den khi vao trang danh sach san pham."""
    login(driver)
    WebDriverWait(driver, 15).until(EC.url_contains("inventory.html"))


def screenshot(driver, filename):
    """Chup man hinh trinh duyet vao thu muc screenshots/."""
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    path = os.path.join(SCREENSHOT_DIR, filename)
    driver.save_screenshot(path)
    return path
