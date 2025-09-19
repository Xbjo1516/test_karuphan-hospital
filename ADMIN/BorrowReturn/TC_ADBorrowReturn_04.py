from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
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

    driver.find_element(By.XPATH, "//button[text() = 'อนุมัติแล้ว/รอคืน']").click()
    time.sleep(2)

    driver.find_element(By.XPATH, "//button[text() = 'คืน']").click()
    time.sleep(2)
    
    dropdown = Select(driver.find_element(By.XPATH, "//table/tbody/tr/td[4]/select"))
    dropdown.select_by_visible_text("ปกติ")

    #dropdown1 = Select(driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div[2]/div/div/div[1]/table/tbody/tr[2]/td[4]/select"))
    #dropdown1.select_by_visible_text("ชำรุด")

    #dropdown2 = Select(driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div[2]/div/div/div[1]/table/tbody/tr[3]/td[4]/select"))
    #dropdown2.select_by_visible_text("รอจำหน่าย")
    time.sleep(2)
    driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div[2]/div/div/div[2]/div[2]/div[2]/textarea").send_keys("คืน")
    time.sleep(2)
    
    driver.find_element(By.XPATH, "//button[text() = 'ยกเลิก']").click()
    time.sleep(2)

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get("http://localhost:3000/role1-admin")

    driver.find_element(By.XPATH, "//button[text() = 'อนุมัติแล้ว/รอคืน']").click()
    time.sleep(5)

    driver.save_screenshot(os.path.join(folder_name, "TC_ADBorrowReturn_04.png"))
    time.sleep(1)
finally:
    driver.quit()