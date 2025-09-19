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
    dropdown.select_by_visible_text("ครุภัณฑ์งานแพทย์และวิทยาศาสตร์")
    numberKaru = driver.find_element(By.XPATH,"//input[@placeholder='0000-000-0000/0']")
    numberKaru.clear()
    numberKaru.send_keys("1111-222-3333/00")

    Id = driver.find_element(By.XPATH,"//input[@placeholder='กรอกเลข ID']")
    Id.clear()
    Id.send_keys("10000")
    date_input = driver.find_element(By.XPATH, "//input[@type='date']")
    date_input.clear()
    date_input.send_keys("2565-09-19")
    time.sleep(5)
    
    driver.find_element(By.XPATH, "//button[text()='ยกเลิก']").click()
    time.sleep(5)

    driver.save_screenshot(os.path.join(folder_name, "TC_ADListKaruphan_05.png"))
    time.sleep(1)

finally:
    driver.quit()