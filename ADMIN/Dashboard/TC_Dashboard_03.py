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

driver.get("http://localhost:3000")

driver.add_cookie({
    "name": "authjs.session-token",
    "value": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoibGNHbXhocGltT3FvM3loZU1VYi0zUENJaGFJeWpGdWwxMUVnbF82aldITEpfUzIxOXJmZmRXNlZvWFZqbWVnaVNvdEh0MjdlbEhDU3JmcUkxMTh5SEEifQ..Fl_cSt3yNZjODXzmBALLpg.bWmVv0sGJysR-S83_lGUyWv4piA7o_GKG-j3nmrE6CJmUaW0lLTmBNnJ5KldEPjoJMZtYKJWJW8B5ISAg8I6bXYW2Dg6lSfBOhiY2-O2WM2paHDIoz6K6LLp26Qh32xgc_fToqXXAIp7uwEA4pz1e75U0E-uwTnBES0lg8OuI6tUSaCeY9v4hfk0o4vKsnQIAFzn2sUED5pV3zubO1Mo8g.qHcu9yjY88Ccaz46INWP0w1TDIg-8ygy4_Rb1sVJWDw",
    "path": "/",
})

try:
    #เปิดเว็บไซต์ และเช็กว่าเปิดแล้ว
    driver.get("http://localhost:3000/role1-admin")
    
    signin = driver.find_element(By.XPATH,"//p[contains(@class, 'text-white')]").text
    assert signin == "ผู้ดูแลระบบครุภัณฑ์"
    print("✅ Check the success words")

    driver.find_element(By.LINK_TEXT,"แดชบอร์ด").click()

    total_EX = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//section/div[1]/div[3]/p"))).text
    time.sleep(1)
    total_EX = int(total_EX.strip())
    print(f"จำนวนบุคลากรภายนอก (แท็บ 1): {total_EX}")

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get("http://localhost:3000/role1-admin")

    driver.find_element(By.LINK_TEXT,"จัดการบุคลากร").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//td[contains(normalize-space(), 'บุคลากรภายนอก')]"))
    )

    personnel_elements = driver.find_elements(By.XPATH, "//td[contains(normalize-space(), 'บุคลากรภายนอก')]")
    count_personnel = len(personnel_elements)
    print(f"จำนวนบุคลากรภายนอก (แท็บ 2): {count_personnel}")

    if total_EX == count_personnel:
        print("✅ จำนวนบุคลากรภายนอกตรงกันทั้งสองแท็บ")
    else:
        print("❌ จำนวนบุคลากรภายนอกไม่ตรงกัน!")

    time.sleep(1)

finally:
    driver.quit()