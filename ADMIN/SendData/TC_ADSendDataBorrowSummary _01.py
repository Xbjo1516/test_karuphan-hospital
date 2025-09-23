from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import time, glob, os, pyautogui

folder_name = "screenshots"
os.makedirs(folder_name, exist_ok=True)

# การเปิดหน้าเว็บโดยไม่ปิดเอง
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
driver.maximize_window()

driver.get("http://localhost:3000")

driver.add_cookie({
    "name": "authjs.session-token",
    "value": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoibGNHbXhocGltT3FvM3loZU1VYi0zUENJaGFJeWpGdWwxMUVnbF82aldITEpfUzIxOXJmZmRXNlZvWFZqbWVnaVNvdEh0MjdlbEhDU3JmcUkxMTh5SEEifQ..auF41StOgIcpo9ituFgKiw.z4BoJEVgV4tnSOlxtK7IFeIZZHjD0RZaaBLq1u9Kslpylo4BLsuutN--ET4RzvhL9clp0djKC899AOaTIF2Edw-99zSSbt-NJZwnehQMn6_-MVq_yBvtNAkgEfRHuwySOPvuaYlMfU6GIN8jYLBWHVFi6iG0VEJROhaDN4Cr8yYjpclZ_BNpc6vNkDBnpglX7hE70lhKTqFWQg1NXP7v8rWEOI4D2ozwLNffTT_Pju8.poi0ZqZDhWhrV6BFqhXtdcy9MkwbaoA-C5icRoa3gy0",
    "path": "/",
})

try:
    # เปิดเว็บไซต์ และเช็กว่าเปิดแล้ว
    driver.get("http://localhost:3000/role1-admin")
    
    signin = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//p[contains(@class, 'text-white')]"))
    ).text.strip()

    assert signin in ["ผู้ใช้ระบบครุภัณฑ์", "System Admin"], f"Unexpected value: {signin}"
    print("✅ Check the success words")
    time.sleep(2)

    # คลิกเมนูรายงาน
    dropdown_button = driver.find_element(By.XPATH, "//button[span[text()='รายงานสรุปผล']]")
    dropdown_button.click()

    submenu_item = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//a[span[text()='สรุปยอดครุภัณฑ์']]"))
    )
    submenu_item.click()
    time.sleep(2)

    # คลิกปุ่มดาวน์โหลด Excel
    excel_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='ดาวน์โหลด Excel']"))
    )
    excel_button.click()
    print("📥 กำลังดาวน์โหลดไฟล์ Excel...")

    # ✅ รอจนไฟล์โหลดเสร็จ (ไม่มี .crdownload ค้างอยู่)
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    while True:
        if not glob.glob(os.path.join(downloads_folder, "*.crdownload")):
            break
        time.sleep(1)

    list_of_files = glob.glob(os.path.join(downloads_folder, "*.csv"))
    latest_file = max(list_of_files, key=os.path.getctime)

    # ✅ เปิดไฟล์ Excel
    os.startfile(latest_file)
    print("📂 เปิดไฟล์ Excel แล้ว")
    time.sleep(10)

    # Screenshot
    screenshot_path = os.path.join(folder_name, "TC_ADSendDataBorrowSummary _01.png")
    pyautogui.screenshot(screenshot_path)
    time.sleep(1)

finally:
    driver.quit()
