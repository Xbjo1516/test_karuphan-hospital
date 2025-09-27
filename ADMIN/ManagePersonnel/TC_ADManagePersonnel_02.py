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

    driver.find_element(By.LINK_TEXT,"จัดการบุคลากร").click()
    time.sleep(2)
    
    people = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//section/div[2]/table/tbody/tr[5]/td[6]/button"))).click()

    role = Select(driver.find_element(By.XPATH, "//form//div[1]//div[2]//div[1]/select"))
    role.select_by_visible_text("EXTERNAL")

    agency = Select(driver.find_element(By.XPATH, "//form/div[1]/div[2]/div[2]/select"))
    agency.select_by_visible_text("กลุ่มงานเทคนิคการแพทย์ (1)")

    call = driver.find_element(By.XPATH, "//form/div[1]/div[3]/input")
    call.clear()
    call.send_keys("0859875625")

    driver.find_element(By.XPATH, "//form/div[2]/button[1]").click()
    time.sleep(5)
    
    driver.save_screenshot(os.path.join(folder_name, "TC_ADManagePersonnel_02.png"))
    time.sleep(1)

finally:
    driver.quit()