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

try :
    driver.get("https://karuphan-hospital-production.up.railway.app/")
    driver.find_element(By.LINK_TEXT,"สมัครสมาชิก").click()

    signup = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, "//p[contains(text(),'สมัครบัญชีของคุณ')]"))).text.strip()
    assert signup == "สมัครบัญชีของคุณ"
    print("✅ Check the success words")

    dropdown = Select(driver.find_element(By.XPATH,"//form/select"))
    dropdown.select_by_visible_text("กลุ่มงานเวชกรรมฟื้นฟู")

    internal = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//form/p[2]"))).text
    assert internal == "ระบบจะกำหนดบทบาท: เจ้าหน้าที่นอกกลุ่มงาน (EXTERNAL)"
    print("✅ internal sign-up message displayed correctly")

    driver.find_element(By.XPATH, "//input[@placeholder='name']").send_keys("ณภัทร วงศ์วัฒนา")
    driver.find_element(By.XPATH,"//input[@placeholder='+66']").send_keys("0973334455")
    driver.find_element(By.XPATH,"//input[@placeholder='example@gmail.com']").send_keys("napat.wong@example.com")
    driver.find_element(By.XPATH,"//form/div[1]/input").send_keys("napat1234")
    driver.find_element(By.XPATH,"//form/div[2]/input").send_keys("napat")
    time.sleep(2)

    driver.find_element(By.XPATH,"//form/button").click()
    time.sleep(5)

    AlreadyUsed = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, "//form/div[1]"))).text.strip()
    assert AlreadyUsed == "รหัสผ่านไม่ตรงกัน"
    print("✅ Check the success words")

    driver.save_screenshot(os.path.join(folder_name, "TC_EXSignUp_03.png"))
    time.sleep(1)    

finally:
    driver.quit()