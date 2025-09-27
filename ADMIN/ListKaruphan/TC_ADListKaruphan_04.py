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

    dropdown_button = driver.find_element(By.XPATH, "//button[span[text()='จัดการครุภัณฑ์']]")
    dropdown_button.click()

    submenu_item = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//a[span[text()='รายการครุภัณฑ์']]"))
    )   
    submenu_item.click()
    time.sleep(2)
    
    driver.find_element(By.XPATH , "//section/div[1]/div[2]/button[2]").click()
    time.sleep(2)

    driver.find_element(By.XPATH,"//section/div[2]/table/tbody/tr/td[9]/button").click()
    time.sleep(2)

    dropdown = Select(driver.find_element(By.XPATH,"//form//div[2]//select"))
    dropdown.select_by_visible_text("ครุภัณฑ์ทางการแพทย์และวิทยาศาสตร์")
    numberKaru = driver.find_element(By.XPATH,"//input[@placeholder='0000-000-0000/0']")
    numberKaru.clear()
    numberKaru.send_keys("1111-222-3333/26")

    Id = driver.find_element(By.XPATH,"//input[@placeholder='กรอกเลข ID']")
    Id.clear()
    Id.send_keys("10015")
    date_input = driver.find_element(By.XPATH, "//input[@type='date']")
    date_input.clear()
    date_input.send_keys("2565-09-19")
    time.sleep(5)
    
    driver.find_element(By.XPATH, "//form/div[10]/button[1]").click()
    time.sleep(5)

    driver.save_screenshot(os.path.join(folder_name, "TC_ADListKaruphan_04.png"))
    time.sleep(1)

finally:
    driver.quit()