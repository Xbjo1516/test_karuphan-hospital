from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
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

    dropdown_button = driver.find_element(By.XPATH, "//button[span[text()='รายงานสรุปผล']]")
    dropdown_button.click()

    submenu_item = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//a[span[text()='สรุปยอดครุภัณฑ์']]"))
    )   
    submenu_item.click()
    time.sleep(2)

    driver.find_element(By.XPATH,"//div[2]/div[2]/button").click()
    time.sleep(2)

    driver.find_element(By.XPATH, "//button").click()
    time.sleep(2)

    num = driver.find_element(By.XPATH , "//table/tbody/tr[1]/td[3]").text
    assert num == "1111-222-3333/01"

    name = driver.find_element(By.XPATH , "//table/tbody/tr[1]/td[5]").text
    assert name == "อุปกรณ์วัดน้ำหนัก"

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get("https://karuphan-hospital-production.up.railway.app/role1-admin")
    time.sleep(3)

    dropdown_button = driver.find_element(By.XPATH, "//button[span[text()='จัดการครุภัณฑ์']]")
    dropdown_button.click()

    submenu_item = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//a[span[text()='รายการครุภัณฑ์']]"))
    )   
    submenu_item.click()
    time.sleep(2)
    
    driver.find_element(By.XPATH, "//button[2]").click()
    time.sleep(2)

    num1 = driver.find_element(By.XPATH, "//table/tbody/tr[1]/td[3]").text
    assert num1 == "1111-222-3333/01"

    name1 = driver.find_element(By.XPATH, "//table/tbody/tr[1]/td[5]").text
    assert name1 == "อุปกรณ์วัดน้ำหนัก"

    assert num == num1, f"❌ เลขครุภัณฑ์ไม่ตรงกัน! ({num} != {num1})"
    print("✅ เลขครุภัณฑ์ตรงกันทั้งสองแท็บ")

    assert name == name1, f"❌ ชื่อครุภัณฑ์ไม่ตรงกัน! ({name} != {name1})"
    print("✅ ชื่อครุภัณฑ์ตรงกันทั้งสองแท็บ")
    
finally:
    driver.quit()