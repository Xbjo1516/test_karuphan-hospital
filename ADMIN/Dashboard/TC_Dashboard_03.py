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
    "value": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoibGNHbXhocGltT3FvM3loZU1VYi0zUENJaGFJeWpGdWwxMUVnbF82aldITEpfUzIxOXJmZmRXNlZvWFZqbWVnaVNvdEh0MjdlbEhDU3JmcUkxMTh5SEEifQ..e61kjT9I7PLmGdf3G7vUBw.8aJ-gCjXDNCo8r-1TtLB-dxfxnUhNJnC79IYk_l534xy7zxkY6q_2pnqSAbVnHj56_DK52BGIkuhvHOnjRxmif6NWWAPaBYLnCGU6xpwX5IUgv1ptSfY8STx1dPHHW0YPwPq_C0BvMzcVtdKYjCA-ma8ud02APF-3adfzLoRhDkDVDMXoTDcMS5OClRel1j3AGIQ3tmN5zkzS3M3z5zE3lZZiE2htzSmJW0ybIDaj5Y.suAyhyKYtWQOiTU7fEx84FBYPD0QcI0aM1Joukb8TjE",
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

    driver.find_element(By.LINK_TEXT,"แดชบอร์ด").click()

    total_EX = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//section/div[1]/div[3]/p"))).text
    time.sleep(1)
    total_EX = int(total_EX.strip())
    print(f"จำนวนบุคลากรภายนอก (แท็บ 1): {total_EX}")

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get("http://localhost:3000/role1-admin")
    time.sleep(5)

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