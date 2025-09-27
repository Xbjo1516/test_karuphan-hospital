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

try:
    driver.get("https://karuphan-hospital-production.up.railway.app/")
    
    signup = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, "//p[contains(text(),'เข้าสู่บัญชีของคุณ')]"))).text.strip()
    assert signup == "เข้าสู่บัญชีของคุณ"
    print("✅ Check the success words")

    driver.find_element(By.XPATH,"/html/body/div[1]/form/input").send_keys("admin@pcu.test")
    driver.find_element(By.XPATH,"/html/body/div[1]/form/div[1]/input").send_keys("Admin#1234")
    driver.find_element(By.XPATH,"/html/body/div[1]/form/button").click()
    time.sleep(2)
    
    Role = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, "//div[2]/p[1]"))).text.strip()
    assert Role == "ผู้ดูแลระบบครุภัณฑ์"
    print("✅ Check Role success")

    ADWaitapproval = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//table/tbody/tr[1]/td[4]"))
    ).text
    assert ADWaitapproval == "4540-001-0001/1"
    print("✅ Check the success Waitapproval-1")
    time.sleep(2)

#-------------------------------------------------------------#

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    driver.get("https://karuphan-hospital-production.up.railway.app/")
    time.sleep(1)

    driver.delete_all_cookies()
    driver.execute_script("window.localStorage.clear();")
    driver.execute_script("window.sessionStorage.clear();")
    time.sleep(0.5)

    driver.get("https://karuphan-hospital-production.up.railway.app/")
    time.sleep(3)

    driver.find_element(By.XPATH,"/html/body/div[1]/form/input").send_keys("weeraphat.s@example.com")
    driver.find_element(By.XPATH,"/html/body/div[1]/form/div[1]/input").send_keys("weeraphat1234")
    driver.find_element(By.XPATH,"/html/body/div[1]/form/button").click()
    time.sleep(2)

    role = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[2]/p[2]"))).text
    assert role == "กลุ่มงานเทคนิคการแพทย์"
    print("✅ Check Role success")

    driver.find_element(By.LINK_TEXT, "สถานะการยืมครุภัณฑ์").click()
    time.sleep(3)

#ADWaitapproval
    expected = ("4540-001-0001/1", "รออนุมัติ")

    row_id = driver.find_element(By.XPATH, "//section/div[2]/table/tbody/tr/td[4]").text.strip()
    row_status = driver.find_element(By.XPATH, "//section/div[2]/table/tbody/tr/td[6]/span").text.strip()
    assert (row_id, row_status) == expected, f"Got {(row_id, row_status)}"
    print("✅ Row values ADWaitapproval success")

finally:
    driver.quit()