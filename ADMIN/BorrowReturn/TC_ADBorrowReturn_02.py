from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoAlertPresentException

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
    "value": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoibGNHbXhocGltT3FvM3loZU1VYi0zUENJaGFJeWpGdWwxMUVnbF82aldITEpfUzIxOXJmZmRXNlZvWFZqbWVnaVNvdEh0MjdlbEhDU3JmcUkxMTh5SEEifQ..auF41StOgIcpo9ituFgKiw.z4BoJEVgV4tnSOlxtK7IFeIZZHjD0RZaaBLq1u9Kslpylo4BLsuutN--ET4RzvhL9clp0djKC899AOaTIF2Edw-99zSSbt-NJZwnehQMn6_-MVq_yBvtNAkgEfRHuwySOPvuaYlMfU6GIN8jYLBWHVFi6iG0VEJROhaDN4Cr8yYjpclZ_BNpc6vNkDBnpglX7hE70lhKTqFWQg1NXP7v8rWEOI4D2ozwLNffTT_Pju8.poi0ZqZDhWhrV6BFqhXtdcy9MkwbaoA-C5icRoa3gy0",
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

    driver.find_element(By.XPATH, "//button[text() = 'อนุมัติ']").click()
    time.sleep(2)

    driver.find_element(By.XPATH,"//input[@placeholder='เหตุผลไม่อนุมัติ']").send_keys("ไม่อนุมัติ")
    time.sleep(2)

    driver.find_element(By.XPATH, "//button[text() = 'ไม่อนุมัติ']").click()
    time.sleep(2)

    try:
        alert = driver.switch_to.alert
        print("⚠️ Alert detected:", alert.text)
        alert.accept()  # กด OK / ยอมรับ
        print("✅ Alert accepted")
    except NoAlertPresentException:
        print("No alert present")
    
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get("http://localhost:3000/role1-admin")

    driver.find_element(By.XPATH, "//button[text() = 'ไม่อนุมัติ/ยกเลิก']").click()
    time.sleep(2)

    driver.save_screenshot(os.path.join(folder_name, "TC_ADBorrowReturn_02.png"))
    time.sleep(1)
finally:
    driver.quit()