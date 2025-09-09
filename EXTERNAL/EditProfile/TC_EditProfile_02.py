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
    "value": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoibGNHbXhocGltT3FvM3loZU1VYi0zUENJaGFJeWpGdWwxMUVnbF82aldITEpfUzIxOXJmZmRXNlZvWFZqbWVnaVNvdEh0MjdlbEhDU3JmcUkxMTh5SEEifQ..Sb6edBfNFUUY9RUt56_nZw.F02KzET9ZmgrTsEVWoP6E5HeQbtztC0Byu-MIHxS_DMmIELgrktjOcjaGLpByKSZibGRWGc-KcbVpJDq242eD9BPrB_VGZd3H-Hm31lt2Qf_sciUs6JTZt4LXaYbPcRc_-3s3X4nDY5FmTcxB6kf97_0W6e8cMy0GUfiLBkXzcDnwwS5RhwAHwPiXdh6PQuPUM-WEN-GJ_-gy6QRSfEvcP_IpVdIRYZOPINkE6YmzkVT0LtRFwP4_97WwaTh6Lq8EMc9Vs1Br3wTc0b3m4TSWb0lwknCQWiGskTzStcF_EwzpNeoyiPnFkK9oW689wRmcAN6a0iJoPsh0tLsjQseegbOjRZzQ5ZHrXllLRc2VxZitERxxMQ_dpZn3ViFDq4j.pzVxVZbMHZaGLh8ls-X-8bPXk45LutsDf0Gevpv-mTQ",
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

    driver.save_screenshot(os.path.join(folder_name, "TC_EditProfile_02.png"))
    time.sleep(1)


finally:
    driver.quit()