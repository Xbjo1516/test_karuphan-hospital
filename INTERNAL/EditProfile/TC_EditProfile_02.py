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
    "value": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoibGNHbXhocGltT3FvM3loZU1VYi0zUENJaGFJeWpGdWwxMUVnbF82aldITEpfUzIxOXJmZmRXNlZvWFZqbWVnaVNvdEh0MjdlbEhDU3JmcUkxMTh5SEEifQ..5nVkKiO8jrSDdSIdnpF-PQ.04YaHDOK9mmeGAuGhoQ13_FMnKHCN01rQ5UqavMCqLekvRrggragi170lwrxfs4S9BUmCfZkc1gWPCzz3MdrY6By288OVZVscJyGZY08qtHbpvsQh6WNeqCf6skbFucKHS3gnMso3zmAbXdgbS-ZAPmLpVTfuevqxJrle4TO_zyL-vfaCt3cAN_uMWt4lqkBwURFyhhI_2o7z7YQqnYaS1Xr3urgFQRRSSlU-WqEDWBFSerxqcK3wVeko0YVWk4NcApb_l9RHuOr0mZv5UrROVYi1tlEPO7cTBJ3uG_Z7DyA2Ohh_N-px2moow8_viJn4Pe4PU6Pbrmvb19A5XGHdI-lFIsjcrfAORBZt19U7ON9oikfR4oKPveELjpFNw4Nf6VHktEXgMNkcpMAcqxEHXC9dudEvf-oSYGYIUPcprE.bjlepB4BM4uYj5WIYWeOsHZHq0Flh0bVS6NfSRAb6Jw",
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
    assert role == "กลุ่มงานบริการด้านปฐมภูมิและองค์รวม"
    print("✅ Check Role success")

    driver.find_element(By.LINK_TEXT,"แก้ไขโปรไฟล์").click()
    time.sleep(2)

    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[text() = 'แก้ไขข้อมูล']"))
    ).click()
    time.sleep(2)

    dropdown = Select(driver.find_element(By.XPATH, "//form/div[1]/div[2]/select"))
    dropdown.select_by_visible_text("กลุ่มงานเทคนิคการแพทย์")

    driver.find_element(By.XPATH, "//form/div[1]/div[3]/input").send_keys("0000")

    call = driver.find_element(By.XPATH , "//form/div[1]/div[4]/input")
    call.clear()
    call.send_keys("0859875625")
    time.sleep(2)
    
    driver.find_element(By.XPATH , "//button[text() = 'ยกเลิก']").click()
    time.sleep(2)

    driver.save_screenshot(os.path.join(folder_name, "TC_INEditProfile_02.png"))
    time.sleep(1)


finally:
    driver.quit()