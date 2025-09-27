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

    driver.find_element(By.LINK_TEXT,"แดชบอร์ด").click()

    total_IN = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//section/div[1]/div[2]/p"))).text
    time.sleep(1)
    total_IN = int(total_IN.strip())
    print(f"จำนวนบุคลากรภายใน (แท็บ 1): {total_IN}")

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get("https://karuphan-hospital-production.up.railway.app/")
    time.sleep(5)
    
    driver.find_element(By.LINK_TEXT,"จัดการบุคลากร").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//td[contains(normalize-space(), 'บุคลากรภายใน')]"))
    )

    personnel_elements = driver.find_elements(By.XPATH, "//td[contains(normalize-space(), 'บุคลากรภายใน')]")
    count_personnel = len(personnel_elements)
    print(f"จำนวนบุคลากรภายใน (แท็บ 2): {count_personnel}")

    if total_IN == count_personnel:
        print("✅ จำนวนบุคลากรภายในตรงกันทั้งสองแท็บ")
    else:
        print("❌ จำนวนบุคลากรภายในไม่ตรงกัน!")

    time.sleep(1)

finally:
    driver.quit()