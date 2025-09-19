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

driver.get("http://localhost:3000")

driver.add_cookie({
    "name": "authjs.session-token",
    "value": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoibGNHbXhocGltT3FvM3loZU1VYi0zUENJaGFJeWpGdWwxMUVnbF82aldITEpfUzIxOXJmZmRXNlZvWFZqbWVnaVNvdEh0MjdlbEhDU3JmcUkxMTh5SEEifQ..eoAelVwdW1lTWMHwZNxV9A.SFc_FtY7B0-fDEOXWBodWAMSef371u7Xw-tOfNlOvawjJqB0PFz1su6qfBTjfZjbHIiDNYDzpjt6ze0Si98HkvejU_um0CvjRaBYhU1KkCU9Jm6pJDO_mImbI8fV6Z8k92RnQTnfFY0TLZ5-8NGl1w_TJNv91mSnV6XdWVS7MDlUF9a6kDL-Z3eml4GxMrbqAYxraD6iaeLvZyR2ae1EojMdKZaT5ZFNnJL66iyyKzzJT54r6cqiaDDpimVa_L_-PKALCIYQ74aY0pzYz9bB890iXPYo8Vyg1Qjpx2Oo8Oa23opY02vBkV0WAZWe5zfiytW2BhYIiYUvRTo_k09Jq7mbtvfGrlqiwszzMKAhOUUWcAGSWq--jt-WD3EXzAPyN2VauwoRbZ3QKtNLGfycIfqyVhWJ9xXqQRuD-4nmPx0.6IWiGKtlHwyQ7ngwJrAMPSY0V-RhjVJn2EOUH4fz4jI",
    "path": "/",
})

try:
    #เปิดเว็บไซต์ และเช็กว่าเปิดแล้ว
    driver.get("http://localhost:3000/role2-internal")
    
    signin = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH,"//p[contains(@class, 'text-white')]"))
    ).text.strip()
    time.sleep(2)

    role = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[2]/p[2]"))).text
    assert role == "กลุ่มงานบริการด้านปฐมภูมิและองค์รวม"
    print("✅ Check Role success")

    driver.find_element(By.LINK_TEXT,"แก้ไขโปรไฟล์").click()
    time.sleep(2)

    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[text() = 'แก้ไขข้อมูล']"))
    ).click()
    time.sleep(2)

    dropdown = Select(driver.find_element(By.XPATH, "//form/div[1]/div[2]/select"))
    dropdown.select_by_visible_text("กลุ่มงานเทคนิคการแพทย์")

    driver.find_element(By.XPATH, "//form/div[1]/div[3]/input").send_keys("0000")

    call = driver.find_element(By.XPATH , "//form/div[1]/div[4]/input")
    call.clear()
    call.send_keys("0859875625")
    time.sleep(2)
    
    driver.find_element(By.XPATH , "//button[text() = 'ยกเลิก']").click()
    time.sleep(2)

    driver.save_screenshot(os.path.join(folder_name, "TC_INEditProfile_02.png"))
    time.sleep(1)


finally:
    driver.quit()