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
    
    signup = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, "//p[contains(text(),'เข้าสู่บัญชีของคุณ')]"))).text.strip()
    assert signup == "เข้าสู่บัญชีของคุณ"
    print("✅ Check the success words")

    #Test-05 เช็กอีเมลและรหัสเป็นค่าว่าง In
    driver.find_element(By.XPATH,"/html/body/div[1]/form/input").send_keys("")
    driver.find_element(By.XPATH,"/html/body/div[1]/form/div[1]/input").send_keys("")
    driver.find_element(By.XPATH,"/html/body/div[1]/form/button").click()
    time.sleep(2)

    invalid = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'อีเมลหรือรหัสผ่านไม่ถูกต้อง')]"))).text.strip()
    assert "อีเมลหรือรหัสผ่านไม่ถูกต้อง" in invalid
    print("✅ Invalid login message displayed correctly")

    
    driver.save_screenshot(os.path.join(folder_name, "TC_INLogin_05.png"))
    time.sleep(1)

finally:
    driver.quit()