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

driver.get("http://localhost:3000")

driver.add_cookie({
    "name": "authjs.session-token",
    "value": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoibGNHbXhocGltT3FvM3loZU1VYi0zUENJaGFJeWpGdWwxMUVnbF82aldITEpfUzIxOXJmZmRXNlZvWFZqbWVnaVNvdEh0MjdlbEhDU3JmcUkxMTh5SEEifQ..Fl_cSt3yNZjODXzmBALLpg.bWmVv0sGJysR-S83_lGUyWv4piA7o_GKG-j3nmrE6CJmUaW0lLTmBNnJ5KldEPjoJMZtYKJWJW8B5ISAg8I6bXYW2Dg6lSfBOhiY2-O2WM2paHDIoz6K6LLp26Qh32xgc_fToqXXAIp7uwEA4pz1e75U0E-uwTnBES0lg8OuI6tUSaCeY9v4hfk0o4vKsnQIAFzn2sUED5pV3zubO1Mo8g.qHcu9yjY88Ccaz46INWP0w1TDIg-8ygy4_Rb1sVJWDw",
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

    driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div[1]/div/button[2]").click()

    ADBorrow1 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//table/tbody/tr[1]/td[4]"))
    ).text
    #print(f"a = '{ADBorrow1}'")
    assert ADBorrow1 == "CAT03-EQ004"
    print("✅ Check the success Borrow-1")

    ADBorrow = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//table/tbody/tr[2]/td[4]"))
    ).text
    #print(f"a = '{ADBorrow}'")
    assert ADBorrow in ["CAT02-EQ005, CAT03-EQ001"], f"Unexpected value : {ADBorrow}"
    print("✅ Check the success Borrow")

    time.sleep(2)

    driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div[1]/div/button[3]").click()

    ADReturn1 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//table/tbody/tr[2]/td[4]"))
    ).text
    #print(f"a = '{ADReturn1}'")
    assert ADReturn1 == "CAT01-EQ001"
    print("✅ Check the success Return-1")

    ADReturn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//table/tbody/tr[1]/td[4]"))
    ).text
    #print(f"a = '{ADReturn}'")
    assert ADReturn in ["CAT01-EQ005, CAT02-EQ003, CAT02-EQ004"], f"Unexpected value : {ADReturn}"
    print("✅ Check the success Return")

#-------------------------------------------------------------#

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    driver.get("http://localhost:3000")
    time.sleep(1)

    driver.delete_all_cookies()
    driver.execute_script("window.localStorage.clear();")
    driver.execute_script("window.sessionStorage.clear();")
    time.sleep(0.5)

    driver.get("http://localhost:3000")
    time.sleep(3)

    driver.find_element(By.XPATH,"/html/body/div[1]/form/input").send_keys("napass.sirikarn@gmail.com")
    driver.find_element(By.XPATH,"/html/body/div[1]/form/div[1]/input").send_keys("napass1234")
    driver.find_element(By.XPATH,"/html/body/div[1]/form/button").click()
    time.sleep(2)

    role = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[2]/p[2]"))).text
    assert role == "กลุ่มงานบริการด้านปฐมภูมิและองค์รวม"
    print("✅ Check Role success")

    driver.find_element(By.LINK_TEXT, "ประวัติการยืมครุภัณฑ์").click()
    time.sleep(3)
#-----การยืม : อนุมัติแล้ว/รอคืน
    expected = ("CAT03-EQ004", "อนุมัติแล้ว/รอคืน")

    row_id = driver.find_element(By.XPATH, "//table/tbody/tr[1]/td[5]").text.strip()
    row_status = driver.find_element(By.XPATH, "//table/tbody/tr[1]/td[8]/span").text.strip()
    assert (row_id, row_status) == expected, f"Got {(row_id, row_status)}"
    print("✅ Row values ADBorrow1 success")

    expected = ("CAT02-EQ005", "อนุมัติแล้ว/รอคืน")

    row_id = driver.find_element(By.XPATH, "//table/tbody/tr[3]/td[5]").text.strip()
    row_status = driver.find_element(By.XPATH, "//table/tbody/tr[3]/td[8]/span").text.strip()

    assert (row_id, row_status) == expected, f"Got {(row_id, row_status)}"
    print("✅ Row values ADBorrow success")

    driver.find_element(By.XPATH, "//section/div[1]/div/button").click()
#-----การคืน : คืนแล้ว
    expected = ("CAT01-EQ001", "คืนแล้ว")

    row_id = driver.find_element(By.XPATH, "//section/div[2]/table/tbody/tr[1]/td[5]").text.strip()
    row_status = driver.find_element(By.XPATH, "//section/div[2]/table/tbody/tr[1]/td[8]").text.strip()

    assert (row_id, row_status) == expected, f"Got {(row_id, row_status)}"
    print("✅ Row values ADReturn1 success")

    expected = ("CAT01-EQ005", "คืนแล้ว")

    row_id = driver.find_element(By.XPATH, "//section/div[2]/table/tbody/tr[5]/td[5]").text.strip()
    row_status = driver.find_element(By.XPATH, "//section/div[2]/table/tbody/tr[5]/td[8]/span").text.strip()

    assert (row_id, row_status) == expected, f"Got {(row_id, row_status)}"
    print("✅ Row values ADReturn success")

finally:
    driver.quit()