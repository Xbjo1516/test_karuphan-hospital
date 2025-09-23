from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import time
import os
import re

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
    "value": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoibGNHbXhocGltT3FvM3loZU1VYi0zUENJaGFJeWpGdWwxMUVnbF82aldITEpfUzIxOXJmZmRXNlZvWFZqbWVnaVNvdEh0MjdlbEhDU3JmcUkxMTh5SEEifQ..Fl_cSt3yNZjODXzmBALLpg.bWmVv0sGJysR-S83_lGUyWv4piA7o_GKG-j3nmrE6CJmUaW0lLTmBNnJ5KldEPjoJMZtYKJWJW8B5ISAg8I6bXYW2Dg6lSfBOhiY2-O2WM2paHDIoz6K6LLp26Qh32xgc_fToqXXAIp7uwEA4pz1e75U0E-uwTnBES0lg8OuI6tUSaCeY9v4hfk0o4vKsnQIAFzn2sUED5pV3zubO1Mo8g.qHcu9yjY88Ccaz46INWP0w1TDIg-8ygy4_Rb1sVJWDw",
    "path": "/",
})

try:
    #เปิดเว็บไซต์ และเช็กว่าเปิดแล้ว
    driver.get("http://localhost:3000/role1-admin")
    
    signin = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH,"//p[contains(@class, 'text-white')]"))
    ).text.strip()

    assert signin in ["ผู้ใช้ระบบครุภัณฑ์", "System Admin"], f"Unexpected value: {signin}"
    print("✅ Check the success words")
    time.sleep(2)

    driver.find_element(By.LINK_TEXT, "แดชบอร์ด").click()
    time.sleep(2)

    total = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//section/div[1]/div[1]/p[1]"))).text
    time.sleep(1)
    total = int(total.strip())
    print(f"จำนวนครุภัณฑ์ (แท็บ 1): {total}")
    
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get("http://localhost:3000/role1-admin")
    
    time.sleep(5)
    dropdown_button = driver.find_element(By.XPATH, "//button[span[text()='จัดการครุภัณฑ์']]")
    dropdown_button.click()
    time.sleep(2)

    submenu_item = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//a[span[text()='รายการครุภัณฑ์']]"))
    )   
    submenu_item.click()
    time.sleep(2)
    text = driver.find_element(By.XPATH, "//*[contains(text(),'แสดง')]").text
    print("ข้อความที่เจอ:", text)

# ใช้ regex หาเลขตัวสุดท้าย (จำนวนทั้งหมด)
    match = re.search(r"จาก\s+(\d+)", text)
    if match:
        totals = int(match.group(1))
        print("จำนวนครุภัณฑ์ (แท็บ 2):", totals)
    else:
        print("ไม่เจอจำนวนทั้งหมด")

    if total == totals:
        print("✅ จำนวนครุภัณฑ์ตรงกันทั้งสองแท็บ")
    else:
        print("❌ จำนวนครุภัณฑ์ไม่ตรงกัน!")

finally:
    driver.quit()