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

    driver.find_element(By.XPATH,"/html/body/div[1]/form/input").send_keys("napass.sirikarn@gmail.com")
    driver.find_element(By.XPATH,"/html/body/div[1]/form/div[1]/input").send_keys("napass1234")
    driver.find_element(By.XPATH,"/html/body/div[1]/form/button").click()
    time.sleep(2)
    
    role = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[2]/p[2]"))).text
    assert role == "กลุ่มงานบริการด้านปฐมภูมิและองค์รวม"
    print("✅ Check Role success")

    driver.find_element(By.XPATH, "//table/tbody/tr[3]/td[7]/button").click()
    time.sleep(2)

    amount = driver.find_element(By.XPATH, "//table/tbody/tr/td[2]").text
    print(f"a = '{amount}'")
    assert amount == "1"
    print("✅ Check the success words")

    driver.save_screenshot(os.path.join(folder_name, "TC_INBorrowKaruphan_01.png"))
    time.sleep(1)

finally:
    driver.quit()