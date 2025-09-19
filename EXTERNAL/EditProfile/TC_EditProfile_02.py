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
    "value": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoibGNHbXhocGltT3FvM3loZU1VYi0zUENJaGFJeWpGdWwxMUVnbF82aldITEpfUzIxOXJmZmRXNlZvWFZqbWVnaVNvdEh0MjdlbEhDU3JmcUkxMTh5SEEifQ..9fX6KrmuzMO6IECh7UpK9Q.24b09nFhBRzakhh7jy5HSkIt927Wqst0s1e5G9LJf22Sl6IbwtzgNesMurX7han-aTiNU72mBO7lNW1Z7RrRyFD3aWK_7aYCa06v3iCPId5yzC6MXD9u_uotMUNZHmhBeGx96CcLgv7901xBNEK7o9EFyVqWNewwXC2WTn5evSMEUqZjHUFFxdQizE7V3Lak0muE9ZObOmab3VQShYxDt212aEw_zwO6x1ivR0mxjiqFdITM4rt83S_5G2XzFJm2sCPqWc14g-mQlCPfsHrr6GETe1RDqRbfCoz3mhSlwClfZdmgW8aLHLjAr_NdAnyuWbXvqRBlLI_0RMs74C3TnWizC-a3kowqsW90HOnSju6YmbYjKNHr5_wNXk9-0w_i.GJpKFJcW1GPGimq4Rb0URBW5foqIHogK0Fq2aIV0fQY",
    "path": "/",
})

try:
    #เปิดเว็บไซต์ และเช็กว่าเปิดแล้ว
    driver.get("http://localhost:3000/role3-external")
    
    signin = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH,"//p[contains(@class, 'text-white')]"))
    ).text.strip()
    time.sleep(2)

    role = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[2]/p[2]"))).text
    assert role == "กลุ่มงานเทคนิคการแพทย์"
    print("✅ Check Role success")

    driver.find_element(By.LINK_TEXT,"แก้ไขโปรไฟล์").click()
    time.sleep(2)

    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[text() = 'แก้ไขข้อมูล']"))
    ).click()
    time.sleep(2)

    dropdown = Select(driver.find_element(By.XPATH, "//form/div[1]/div[2]/select"))
    dropdown.select_by_visible_text("กลุ่มงานบริการด้านปฐมภูมิและองค์รวม")

    driver.find_element(By.XPATH, "//form/div[1]/div[3]/input").send_keys("0000")

    call = driver.find_element(By.XPATH , "//form/div[1]/div[4]/input")
    call.clear()
    call.send_keys("0923456789")
    time.sleep(2)

    driver.find_element(By.XPATH , "//button[text() = 'ยกเลิก']").click()
    time.sleep(2)

    driver.save_screenshot(os.path.join(folder_name, "TC_EXEditProfile_02.png"))
    time.sleep(1)


finally:
    driver.quit()