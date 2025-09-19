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
    "value": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoibGNHbXhocGltT3FvM3loZU1VYi0zUENJaGFJeWpGdWwxMUVnbF82aldITEpfUzIxOXJmZmRXNlZvWFZqbWVnaVNvdEh0MjdlbEhDU3JmcUkxMTh5SEEifQ..26G55f08WZ4HLB5aG0op2w.E2QhOpdwIuLFqFrXvYFt9o-tJf9vBObaRRMasRclN1fVatG8A2BpqbbyOKa687Gf5qHCt-s1iHhJUDxVp-EeT--QZi3yYvSl8V09I3Z8pXXMp3fcVhxlCwhR_DBR41nmmkXjNldx8tztRcShxOUpGU-ARIb_iJ4hhnF49LH5FCM7rT-qQKyh8CGSK_9nDuqICJS2TdyM5BaNSkIAWfgbMsBpYANTf-I_J6A1woo36sk.77C_2e5mD5QCC0xgoXAYZKy1PwbijOzkm6FY1BF2QDc",
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

    dropdown_button = driver.find_element(By.XPATH, "//button[span[text()='รายงานสรุปผล']]")
    dropdown_button.click()

    submenu_item = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//a[span[text()='สรุปยอดครุภัณฑ์']]"))
    )   
    submenu_item.click()
    time.sleep(2)

    driver.find_element(By.XPATH,"//div[2]/div[2]/button").click()
    time.sleep(2)

    num = driver.find_element(By.XPATH , "//table/tbody/tr[1]/td[2]").text
    assert num == "1111-222-3333/01"

    name = driver.find_element(By.XPATH , "//table/tbody/tr[1]/td[3]").text
    assert name == "เครื่องชั่งดิจิทัล"

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get("http://localhost:3000/role1-admin")
    time.sleep(3)

    dropdown_button = driver.find_element(By.XPATH, "//button[span[text()='จัดการครุภัณฑ์']]")
    dropdown_button.click()

    submenu_item = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//a[span[text()='รายการครุภัณฑ์']]"))
    )   
    submenu_item.click()
    time.sleep(2)

    driver.find_element(By.XPATH , "//section/div[1]/div[2]/button[2]").click()
    time.sleep(2)

    num1 = driver.find_element(By.XPATH, "//section/div[2]/table/tbody/tr[1]/td[3]").text
    assert num1 == "1111-222-3333/01"

    name1 = driver.find_element(By.XPATH, "//section/div[2]/table/tbody/tr[1]/td[4]/div/span").text
    assert name1 == "เครื่องชั่งดิจิทัล"

    assert num == num1, f"❌ เลขครุภัณฑ์ไม่ตรงกัน! ({num} != {num1})"
    print("✅ เลขครุภัณฑ์ตรงกันทั้งสองแท็บ")

    assert name == name1, f"❌ ชื่อครุภัณฑ์ไม่ตรงกัน! ({name} != {name1})"
    print("✅ ชื่อครุภัณฑ์ตรงกันทั้งสองแท็บ")
    
finally:
    driver.quit()