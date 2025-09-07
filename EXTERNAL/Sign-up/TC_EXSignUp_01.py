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
    driver.get("http://localhost:3000/")
    driver.find_element(By.LINK_TEXT,"สมัครสมาชิก").click()

    signup = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, "//p[contains(text(),'สมัครบัญชีของคุณ')]"))).text.strip()
    assert signup == "สมัครบัญชีของคุณ"
    print("✅ Check the success words")

    dropdown = Select(driver.find_element(By.XPATH,"//form/select"))
    dropdown.select_by_visible_text("กลุ่มงานเทคนิคการแพทย์")

    internal = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//form/p[2]"))).text
    assert internal == "ระบบจะกำหนดบทบาท: เจ้าหน้าที่นอกกลุ่มงาน (EXTERNAL)"
    print("✅ internal sign-up message displayed correctly")

    driver.find_element(By.XPATH, "//input[@placeholder='name']").send_keys("วีรภัทร สุวรรณศรี")
    driver.find_element(By.XPATH,"//input[@placeholder='+66']").send_keys("0923456789")
    driver.find_element(By.XPATH,"//input[@placeholder='example@gmail.com']").send_keys("weeraphat.s@example.com")
    driver.find_element(By.XPATH,"//form/div[1]/input").send_keys("weeraphat1234")
    driver.find_element(By.XPATH,"//form/div[2]/input").send_keys("weeraphat1234")
    time.sleep(2)

    driver.find_element(By.XPATH,"//form/button").click()
    time.sleep(5)

    name = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[2]/p[1]"))).text
    assert name == "วีรภัทร สุวรรณศรี"
    print("✅ Check Name success")

    role = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH , "//div[2]/p[2]"))).text
    assert role == "กลุ่มงานเทคนิคการแพทย์"
    print("✅ Check Role success")

    driver.save_screenshot(os.path.join(folder_name, "TC_EXSignUp_01.png"))
    time.sleep(1)    

finally:
    driver.quit()