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
    "value": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoibGNHbXhocGltT3FvM3loZU1VYi0zUENJaGFJeWpGdWwxMUVnbF82aldITEpfUzIxOXJmZmRXNlZvWFZqbWVnaVNvdEh0MjdlbEhDU3JmcUkxMTh5SEEifQ..2I3EWaXJlPKFGgm3HENo_Q.f4yR6mmjkSc470CxlompHFncpV-W0iMRSzrSn4r5TOXP-J5H65dhugDZMdBtenlf-bKbDnaeJKBJx2uXYXp3eOnfHSUf5wDCEhB8I0llZ5KfHHwK7v2pYPc7OJUhV4N3c3Njh5bzlz4Ge17UPqTgfjWmjz-QvzLlzaXj8aW3JGAPCQvq0syiF35Ql0AB4S0RUINhpZfbjtOXF8ZqZQDy7LCh3TnKk3aCpstjRLdkpOo.yhH4jUfRN24Yb5tojpNv9AhBG_AZimn8sMOn0vD_Izw",
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

    driver.find_element(By.LINK_TEXT,"จัดการบุคลากร").click()
    time.sleep(2)
    
    people = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//section/div[2]/table/tbody/tr[5]/td[7]/button"))).click()

    try:
        alert = driver.switch_to.alert
        print("⚠️ Alert detected:", alert.text)
        alert.accept()  # กด OK / ยอมรับ
        print("✅ Alert accepted")
    except NoAlertPresentException:
        print("No alert present")   
        
    time.sleep(2)
    
    driver.save_screenshot(os.path.join(folder_name, "TC_ADManagePersonnel_03.png"))
    time.sleep(1)

finally:
    driver.quit()