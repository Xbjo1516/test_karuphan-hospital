from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import time
import os

folder_name = "screenshots"
os.makedirs(folder_name, exist_ok=True)

#การเปิดหน้าเว็บโดยไม่ปิดเอง
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
driver.maximize_window()

try:
    driver.get("https://karuphan-hospital-production.up.railway.app/")
    
    signup = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, "//p[contains(text(),'เข้าสู่บัญชีของคุณ')]"))
    ).text.strip()
    assert signup == "เข้าสู่บัญชีของคุณ"
    print("✅ Check the success words")

    driver.find_element(By.XPATH, "/html/body/div[1]/form/input").send_keys("admin@pcu.test")
    driver.find_element(By.XPATH, "/html/body/div[1]/form/div[1]/input").send_keys("Admin#1234")
    driver.find_element(By.XPATH, "/html/body/div[1]/form/button").click()
    time.sleep(2)
    
    Role = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, "//div[2]/p[1]"))
    ).text.strip()
    assert Role == "ผู้ดูแลระบบครุภัณฑ์"
    print("✅ Check Role success")

    driver.find_element(By.XPATH, "//button[2]").click()
    time.sleep(2)

    ADBorrow1 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//table/tbody/tr[3]/td[4]"))
    ).text
    assert ADBorrow1 == "3920-005-1103/5"
    print("✅ Check the success Borrow-1")

    # หลายรายการ
    ADBorrow = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//table/tbody/tr[1]/td[4]"))
    ).text
    assert "7110-006-0007/292" in ADBorrow or "7110-001-0007/31" in ADBorrow, f"Unexpected value: {ADBorrow}"
    print("✅ Check the success Borrow")

    time.sleep(2)

    driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div[1]/div/button[3]").click()

    ADReturn1 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//table/tbody/tr[2]/td[4]"))
    ).text
    assert ADReturn1 == "0000-001-0001/1"
    print("✅ Check the success Return-1")

    # หลายรายการ
    ADReturn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//table/tbody/tr[1]/td[4]"))
    ).text
    assert "7440-001-0006/124" in ADReturn or "1111-001-0025/12" in ADReturn, f"Unexpected value: {ADReturn}"
    print("✅ Check the success Return")

    #-------------------------------------------------------------#

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    driver.get("https://karuphan-hospital-production.up.railway.app/")
    time.sleep(1)

    driver.delete_all_cookies()
    driver.execute_script("window.localStorage.clear();")
    driver.execute_script("window.sessionStorage.clear();")
    time.sleep(0.5)

    driver.get("https://karuphan-hospital-production.up.railway.app/")
    time.sleep(3)

    driver.find_element(By.XPATH, "/html/body/div[1]/form/input").send_keys("napass.sirikarn@gmail.com")
    driver.find_element(By.XPATH, "/html/body/div[1]/form/div[1]/input").send_keys("napass1234")
    driver.find_element(By.XPATH, "/html/body/div[1]/form/button").click()
    time.sleep(2)

    role = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[2]/p[2]"))
    ).text
    assert role == "กลุ่มงานบริการด้านปฐมภูมิและองค์รวม"
    print("✅ Check Role success")

    driver.find_element(By.LINK_TEXT, "ประวัติการยืมครุภัณฑ์").click()
    time.sleep(3)

    #----- การยืม/คืน: ใช้ฟังก์ชันกลาง
    def check_row(row_xpath, expected_id, expected_status):
        row_id = driver.find_element(By.XPATH, f"{row_xpath}/td[4]").text.strip()
        row_status = driver.find_element(By.XPATH, f"{row_xpath}/td[6]/span").text.strip()
        row_ids = [x.strip() for x in row_id.split(",")]  # รองรับหลาย ID
        assert expected_id in row_ids, f"Got IDs {row_ids}, expected {expected_id}"
        assert row_status == expected_status, f"Got status {row_status}, expected {expected_status}"

    # ใช้งาน
    check_row("//table/tbody/tr[4]", "3920-005-1103/5", "อนุมัติแล้ว/รอคืน")
    check_row("//table/tbody/tr[2]", "7110-006-0007/292", "อนุมัติแล้ว/รอคืน")
    check_row("//table/tbody/tr[3]", "0000-001-0001/1", "คืนแล้ว")
    check_row("//table/tbody/tr[1]", "7440-001-0006/124", "คืนแล้ว")

finally:
    driver.quit()
