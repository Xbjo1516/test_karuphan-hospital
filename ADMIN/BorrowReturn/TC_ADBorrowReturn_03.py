from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoAlertPresentException

import time
import os

folder_name = "screenshots"
os.makedirs(folder_name, exist_ok=True)

#การเปิดหน้าเว็บโดยไม่ปิดเอง
options = webdriver.ChromeOptions()
options.add_experimental_option("detach",True)
driver = webdriver.Chrome(options=options)
driver.maximize_window()

try:
    driver.get("https://karuphan-hospital-production.up.railway.app/")
    
    signin = driver.find_element(By.XPATH,"//form/h1").text
    assert signin == "ระบบครุภัณฑ์"
    print("✅ Check the success words")

    driver.find_element(By.XPATH,"/html/body/div[1]/form/input").send_keys("admin@pcu.test")
    driver.find_element(By.XPATH,"/html/body/div[1]/form/div[1]/input").send_keys("Admin#1234")
    driver.find_element(By.XPATH,"/html/body/div[1]/form/button").click()
    time.sleep(2)

    assert "karuphan-hospital" in driver.title
    print("✅ Home page loaded")
    time.sleep(1)

    Role = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, "//div[2]/p[1]"))).text.strip()
    assert Role == "ผู้ดูแลระบบครุภัณฑ์"
    print("✅ Check Role success")

    driver.find_element(By.XPATH, "//button[text() = 'อนุมัติ']").click()
    time.sleep(2)

    driver.find_element(By.XPATH,"//input[@placeholder='กรอกเหตุผลที่ไม่อนุมัติ']").send_keys("")
    time.sleep(2)

    driver.find_element(By.XPATH, "//button[text() = 'ไม่อนุมัติ']").click()
    time.sleep(2)

    driver.save_screenshot(os.path.join(folder_name, "TC_ADBorrowReturn_03.png"))
    time.sleep(1)
finally:
    driver.quit()