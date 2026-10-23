# -*- coding: utf-8 -*-
"""
Bo test tu dong Selenium cho website ban hang mau SauceDemo (https://www.saucedemo.com).
Gom 06 test case:
  TC01 - Dang nhap thanh cong
  TC02 - Dang nhap that bai (sai mat khau)
  TC03 - Them san pham vao gio hang
  TC04 - Sap xep san pham theo gia tang dan
  TC05 - Thanh toan (checkout) hoan tat don hang
  TC06 - Dang xuat

Tai khoan test (trang cung cap cong khai):
  standard_user / secret_sauce
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from conftest import BASE_URL, login, login_success, screenshot


def test_tc01_login_success(driver):
    """TC01: Dang nhap voi tai khoan dung -> vao trang danh sach san pham."""
    login_success(driver)
    assert "inventory.html" in driver.current_url
    assert driver.find_element(By.CLASS_NAME, "title").text == "Products"
    assert len(driver.find_elements(By.CLASS_NAME, "inventory_item")) == 6
    screenshot(driver, "tc01-login-success.png")


def test_tc02_login_wrong_password(driver):
    """TC02: Dang nhap sai mat khau -> hien thong bao loi, khong vao duoc trang chinh."""
    login(driver, password="wrong_password")
    error = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-test="error"]')))
    assert "Username and password do not match" in error.text
    assert "inventory.html" not in driver.current_url
    screenshot(driver, "tc02-login-fail.png")


def test_tc03_add_to_cart(driver):
    """TC03: Them 1 san pham vao gio -> badge gio hang = 1, gio chua dung san pham."""
    login_success(driver)
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    badge = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
    assert badge.text == "1"
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    WebDriverWait(driver, 15).until(EC.url_contains("cart.html"))
    item_name = driver.find_element(
        By.CSS_SELECTOR, ".cart_item .inventory_item_name").text
    assert item_name == "Sauce Labs Backpack"
    screenshot(driver, "tc03-cart.png")


def test_tc04_sort_by_price_low_to_high(driver):
    """TC04: Sap xep theo gia thap -> cao, danh sach gia phai tang dan."""
    login_success(driver)
    select = Select(driver.find_element(By.CLASS_NAME, "product_sort_container"))
    select.select_by_value("lohi")
    prices = [
        float(el.text.replace("$", ""))
        for el in driver.find_elements(By.CLASS_NAME, "inventory_item_price")
    ]
    assert prices == sorted(prices), f"Gia chua tang dan: {prices}"
    assert prices[0] == 7.99  # San pham re nhat: Sauce Labs Onesie
    screenshot(driver, "tc04-sort-price.png")


def test_tc05_checkout_complete(driver):
    """TC05: Mua hang den cuoi quy trinh -> nhan thong bao dat hang thanh cong."""
    login_success(driver)
    driver.find_element(By.ID, "add-to-cart-sauce-labs-bike-light").click()
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    WebDriverWait(driver, 15).until(EC.url_contains("cart.html"))
    driver.find_element(By.ID, "checkout").click()
    WebDriverWait(driver, 15).until(EC.url_contains("checkout-step-one"))
    driver.find_element(By.ID, "first-name").send_keys("Anh Son")
    driver.find_element(By.ID, "last-name").send_keys("Do")
    driver.find_element(By.ID, "postal-code").send_keys("100000")
    driver.find_element(By.ID, "continue").click()
    WebDriverWait(driver, 15).until(EC.url_contains("checkout-step-two"))
    driver.find_element(By.ID, "finish").click()
    header = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "complete-header")))
    assert header.text == "Thank you for your order!"
    screenshot(driver, "tc05-checkout-complete.png")


def test_tc06_logout(driver):
    """TC06: Dang xuat qua menu -> quay ve trang dang nhap."""
    login_success(driver)
    driver.find_element(By.ID, "react-burger-menu-btn").click()
    logout = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.ID, "logout_sidebar_link")))
    logout.click()
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "login-button")))
    assert driver.current_url == BASE_URL + "/"
    screenshot(driver, "tc06-logout.png")
