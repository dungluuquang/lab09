# lab09
# Báo cáo thực hành: Kiểm thử tự động với Selenium WebDriver

> Môn: Kiểm định & Chất lượng Phần mềm — Bài thực hành công cụ Selenium
> Người thực hiện: Lưu Quang Dũng


## 1. Mục tiêu

- Tìm hiểu công cụ kiểm thử tự động **Selenium WebDriver**: kiến trúc, cách định vị phần tử
  (locator), cơ chế chờ (wait) và kiểm chứng kết quả (assertion).
- Xây dựng bộ test tự động gồm **06 test case** cho một website bán hàng mẫu, bao phủ các
  chức năng: đăng nhập, đăng nhập thất bại, thêm vào giỏ hàng, sắp xếp sản phẩm,
  thanh toán và đăng xuất.
- Chạy toàn bộ bộ test bằng **pytest**, ghi nhận kết quả và chụp ảnh minh hoạ cho từng test case.

## 2. Giới thiệu Selenium

**Selenium** là bộ công cụ mã nguồn mở phổ biến nhất cho kiểm thử tự động ứng dụng web.
Thành phần cốt lõi là **Selenium WebDriver**: một API cho phép chương trình điều khiển
trình duyệt thật (Chrome, Firefox, Edge...) giống hệt thao tác của người dùng —
mở trang, nhập liệu, nhấn nút, đọc nội dung — thông qua giao thức W3C WebDriver.

Các khái niệm đã sử dụng trong bài:

| Khái niệm | Ý nghĩa | Ví dụ trong bài |
|---|---|---|
| **WebDriver** | Đối tượng điều khiển trình duyệt | `webdriver.Chrome(options=...)` |
| **Locator** | Cách tìm phần tử trên trang: `By.ID`, `By.CLASS_NAME`, `By.CSS_SELECTOR` | `find_element(By.ID, "user-name")` |
| **Explicit Wait** | Chờ có điều kiện tới khi phần tử sẵn sàng, tránh lỗi do trang tải chậm | `WebDriverWait(driver, 15).until(EC.url_contains("inventory.html"))` |
| **Implicit Wait** | Thời gian chờ mặc định khi tìm phần tử | `driver.implicitly_wait(5)` |
| **Assertion** | Kiểm chứng kết quả thực tế so với mong đợi | `assert badge.text == "1"` |
| **Select** | Thao tác với thẻ `<select>` (dropdown) | `select_by_value("lohi")` |
| **Screenshot** | Chụp ảnh trình duyệt làm bằng chứng kết quả | `driver.save_screenshot(...)` |
| **pytest fixture** | Khởi tạo/dọn dẹp driver cho từng test case độc lập | `@pytest.fixture() def driver()` |

## 3. Môi trường thực hiện

| Thành phần | Phiên bản / Thông tin |
|---|---|
| Ngôn ngữ | Python 3.12 |
| Selenium | 4.51.0 |
| Test runner | pytest 9.1.1 |
| Trình duyệt | Chrome 152 (headless) |
| Hệ điều hành | Ubuntu (máy lab) |

## 4. Website mục tiêu: SauceDemo

[SauceDemo](https://www.saucedemo.com) ("Swag Labs") là website bán hàng mẫu do Sauce Labs
xây dựng dành riêng cho việc học và thực hành kiểm thử tự động. Website có đầy đủ luồng
mua hàng: đăng nhập → xem/sắp xếp sản phẩm → giỏ hàng → thanh toán → hoàn tất.

Tài khoản kiểm thử (website cung cấp công khai): `standard_user` / `secret_sauce`.

## 5. Danh sách test case

| ID | Test case | Các bước chính | Kết quả mong đợi |
|---|---|---|---|
| TC01 | Đăng nhập thành công | Mở trang → nhập `standard_user`/`secret_sauce` → nhấn Login | Chuyển tới trang Products, hiển thị 6 sản phẩm |
| TC02 | Đăng nhập sai mật khẩu | Nhập mật khẩu sai → nhấn Login | Hiển thị lỗi "Username and password do not match...", ở lại trang đăng nhập |
| TC03 | Thêm sản phẩm vào giỏ hàng | Đăng nhập → Add to cart (Backpack) → mở giỏ hàng | Badge giỏ hàng = 1; giỏ chứa đúng "Sauce Labs Backpack" |
| TC04 | Sắp xếp giá tăng dần | Đăng nhập → chọn sort "Price (low to high)" | Danh sách giá tăng dần, sản phẩm rẻ nhất $7.99 ở đầu |
| TC05 | Thanh toán hoàn tất | Thêm Bike Light → Checkout → điền thông tin → Finish | Hiện thông báo "Thank you for your order!" |
| TC06 | Đăng xuất | Đăng nhập → mở menu → Logout | Quay về trang đăng nhập |

Mã nguồn: [`test_saucedemo.py`](test_saucedemo.py), cấu hình dùng chung trong [`conftest.py`](conftest.py).

## 6. Kết quả thực thi

Chạy toàn bộ bộ test bằng pytest:

```
test_saucedemo.py::test_tc01_login_success PASSED                        [ 16%]
test_saucedemo.py::test_tc02_login_wrong_password PASSED                 [ 33%]
test_saucedemo.py::test_tc03_add_to_cart PASSED                          [ 50%]
test_saucedemo.py::test_tc04_sort_by_price_low_to_high PASSED            [ 66%]
test_saucedemo.py::test_tc05_checkout_complete PASSED                    [ 83%]
test_saucedemo.py::test_tc06_logout PASSED                               [100%]

============================== 6 passed in 26.18s ==============================
```

**Kết quả: 6/6 test case PASSED (100%).**

### Hình ảnh minh hoạ

**TC01 — Đăng nhập thành công, trang danh sách sản phẩm:**

<img width="1280" height="757" alt="image" src="https://github.com/user-attachments/assets/ed6037cc-18d4-47f5-a55f-16382991761a" />


**TC02 — Thông báo lỗi khi đăng nhập sai mật khẩu:**

<img width="1280" height="757" alt="image" src="https://github.com/user-attachments/assets/fb4e2ca1-3999-48d1-9ba8-5db092fc1f46" />


**TC03 — Giỏ hàng chứa sản phẩm đã thêm:**

<img width="1280" height="757" alt="image" src="https://github.com/user-attachments/assets/9e189a81-bef0-432b-a8e3-658c29925072" />


**TC04 — Sản phẩm đã sắp xếp theo giá tăng dần:**

<img width="1280" height="757" alt="image" src="https://github.com/user-attachments/assets/8a5a9f0a-8f62-4f5a-8cea-b5f9b73f1731" />


**TC05 — Đặt hàng thành công:**

<img width="1280" height="757" alt="image" src="https://github.com/user-attachments/assets/fc7f6907-4abe-4bca-9bda-fb73e41e1858" />


**TC06 — Sau khi đăng xuất, quay về trang đăng nhập:**

<img width="1280" height="757" alt="image" src="https://github.com/user-attachments/assets/b8fb09da-5441-410a-aa89-f20b7fd22ee9" />


## 7. Nhận xét và kết luận

1. **Bộ test bao phủ trọn luồng nghiệp vụ chính** của một website bán hàng: xác thực
   (thành công + thất bại), thao tác giỏ hàng, sắp xếp dữ liệu, thanh toán đầu-cuối
   và đăng xuất — tất cả đều chạy tự động, không cần thao tác tay.
2. **Explicit Wait là yếu tố quyết định độ ổn định**: các bước chờ theo điều kiện
   (URL thay đổi, phần tử hiển thị/click được) giúp test không bị "flaky" do tốc độ tải trang.
   Trong quá trình làm, một test từng thất bại vì chỉ chờ phần tử *xuất hiện* thay vì
   *tương tác được* — đã sửa bằng `element_to_be_clickable`.
3. **Tổ chức code bằng pytest fixture** giúp mỗi test case chạy trong một phiên trình duyệt
   độc lập (đăng nhập mới, giỏ hàng trống), kết quả không ảnh hưởng lẫn nhau và dễ mở rộng thêm test case.
4. **Hướng phát triển**: áp dụng Page Object Model để tách locator khỏi logic test;
   bổ sung test case cho các tài khoản đặc biệt của SauceDemo (`locked_out_user`,
   `problem_user`); chạy song song bằng pytest-xdist và tích hợp CI (GitHub Actions).

**Kết luận**: Selenium WebDriver + pytest là bộ công cụ hiệu quả để tự động hoá kiểm thử
chức năng web. Bộ 06 test case xây dựng trong bài đều đạt (passed 100%) và có thể chạy lại
bất cứ lúc nào chỉ với một lệnh.

## 8. Cách chạy lại

```bash
# 1. Cai dat thu vien
pip install -r requirements.txt

# 2. Chay toan bo test (mo cua so trinh duyet)
HEADLESS=0 python -m pytest test_saucedemo.py -v

# 3. Chay khong giao dien (headless)
python -m pytest test_saucedemo.py -v
# Anh chup ket qua duoc luu vao thu muc screenshots/
```

Tuỳ chọn qua biến môi trường: `CHROME_BINARY` (đường dẫn Chrome tuỳ chỉnh),
`CHROME_PROXY` (proxy cho trình duyệt nếu mạng yêu cầu).

## 9. Cấu trúc thư mục

```
seleniumlab/
├── README.md            # Báo cáo này
├── conftest.py          # Fixture driver + hàm hỗ trợ (login, screenshot)
├── test_saucedemo.py    # 06 test case
├── requirements.txt     # selenium, pytest
└── screenshots/         # Ảnh minh hoạ kết quả từng test case
    ├── tc01-login-success.png
    ├── tc02-login-fail.png
    ├── tc03-cart.png
    ├── tc04-sort-price.png
    ├── tc05-checkout-complete.png
    └── tc06-logout.png
```
