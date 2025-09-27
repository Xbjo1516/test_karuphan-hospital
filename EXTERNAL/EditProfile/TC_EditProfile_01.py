from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import time
import os,re

folder_name = "screenshots"
os.makedirs(folder_name, exist_ok=True)

#การเปิดหน้าเว็บโดยไม่ปิดเอง
options = webdriver.ChromeOptions()
options.add_experimental_option("detach",True)
driver = webdriver.Chrome(options=options)
driver.maximize_window()

try:
    driver.get("https://karuphan-hospital-production.up.railway.app/")
    
    signup = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, "//p[contains(text(),'เข้าสู่บัญชีของคุณ')]"))).text.strip()
    assert signup == "เข้าสู่บัญชีของคุณ"
    print("✅ Check the success words")

    driver.find_element(By.XPATH,"/html/body/div[1]/form/input").send_keys("weeraphat.s@example.com")
    driver.find_element(By.XPATH,"/html/body/div[1]/form/div[1]/input").send_keys("weeraphat1234")
    driver.find_element(By.XPATH,"/html/body/div[1]/form/button").click()
    time.sleep(2)

    role = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[2]/p[2]"))).text
    assert role == "กลุ่มงานเทคนิคการแพทย์"
    print("✅ Check Role success")

    driver.find_element(By.LINK_TEXT,"แก้ไขโปรไฟล์").click()
    time.sleep(2)

    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[text() = 'แก้ไขข้อมูล']"))
    ).click()
    time.sleep(2)

    call = driver.find_element(By.XPATH , "//form/div[1]/div[4]/input")
    call.clear()
    call.send_keys("092-345-6789")

    driver.find_element(By.XPATH , "//button[text() = 'บันทึก']").click()
    time.sleep(2)

    driver.save_screenshot(os.path.join(folder_name, "TC_EXEditProfile_01.png"))
    time.sleep(1)


finally:
    driver.quit()