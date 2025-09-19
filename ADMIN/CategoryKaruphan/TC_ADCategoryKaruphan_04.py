from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoAlertPresentException

import time
import os
import pyautogui

folder_name = "screenshots"
os.makedirs(folder_name, exist_ok=True)

options = webdriver.ChromeOptions()
options.add_experimental_option("detach",True)
driver = webdriver.Chrome(options=options)
driver.maximize_window()

driver.get("http://localhost:3000")

driver.add_cookie({
    "name": "authjs.session-token",
    "value": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoibGNHbXhocGltT3FvM3loZU1VYi0zUENJaGFJeWpGdWwxMUVnbF82aldITEpfUzIxOXJmZmRXNlZvWFZqbWVnaVNvdEh0MjdlbEhDU3JmcUkxMTh5SEEifQ..26G55f08WZ4HLB5aG0op2w.E2QhOpdwIuLFqFrXvYFt9o-tJf9vBObaRRMasRclN1fVatG8A2BpqbbyOKa687Gf5qHCt-s1iHhJUDxVp-EeT--QZi3yYvSl8V09I3Z8pXXMp3fcVhxlCwhR_DBR41nmmkXjNldx8tztRcShxOUpGU-ARIb_iJ4hhnF49LH5FCM7rT-qQKyh8CGSK_9nDuqICJS2TdyM5BaNSkIAWfgbMsBpYANTf-I_J6A1woo36sk.77C_2e5mD5QCC0xgoXAYZKy1PwbijOzkm6FY1BF2QDc",
    "path": "/",
})

try:
    driver.get("http://localhost:3000/role1-admin")
    
    signin = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH,"//p[contains(@class, 'text-white')]"))
    ).text.strip()

    assert signin in ["ผู้ใช้ระบบครุภัณฑ์", "System Admin"], f"Unexpected value: {signin}"
    print("✅ Check the success words")
    time.sleep(2)

    dropdown_button = driver.find_element(By.XPATH, "//button[span[text()='จัดการครุภัณฑ์']]")
    dropdown_button.click()

    submenu_item = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//a[span[text()='เพิ่มหมวดหมู่ครุภัณฑ์']]"))
    )   
    submenu_item.click()
    time.sleep(2)

    driver.find_element(By.XPATH,"//button[@title='ลบ']").click()
    time.sleep(1)

    try:
        alert = driver.switch_to.alert
        print("⚠️ Alert detected:", alert.text)
        alert.accept()  # กด OK / ยอมรับ
        print("✅ Alert accepted")
    except NoAlertPresentException:
        print("No alert present")

    time.sleep(2)
    
    screenshot_path = os.path.join(folder_name, "TC_ADCategoryKaruphan_04.png")
    pyautogui.screenshot(screenshot_path)
    time.sleep(1)

finally:
    driver.quit()
