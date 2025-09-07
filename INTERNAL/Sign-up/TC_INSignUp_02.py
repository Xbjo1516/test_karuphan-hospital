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

try :
    driver.get("http://localhost:3000/")
    driver.find_element(By.LINK_TEXT,"สมัครสมาชิก").click()

    signup = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, "//p[contains(text(),'สมัครบัญชีของคุณ')]"))).text.strip()
    assert signup == "สมัครบัญชีของคุณ"
    print("✅ Check the success words")

    driver.find_element(By.XPATH, "//input[@placeholder='name']").send_keys("")
    driver.find_element(By.XPATH,"//input[@placeholder='+66']").send_keys("")
    driver.find_element(By.XPATH,"//input[@placeholder='example@gmail.com']").send_keys("")
    driver.find_element(By.XPATH,"//form/div[1]/input").send_keys("")
    driver.find_element(By.XPATH,"//form/div[2]/input").send_keys("")
    time.sleep(2)

    driver.find_element(By.XPATH,"//form/button").click()
    time.sleep(5)

    Incomplete = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, "//form/div[1]"))).text.strip()
    assert Incomplete == "กรอกชื่อ-นามสกุล"
    print("✅ Check the success words")

    driver.save_screenshot(os.path.join(folder_name, "TC_INSignUp_02.png"))
    time.sleep(1)    

finally:
    driver.quit()