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
    "value": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoibGNHbXhocGltT3FvM3loZU1VYi0zUENJaGFJeWpGdWwxMUVnbF82aldITEpfUzIxOXJmZmRXNlZvWFZqbWVnaVNvdEh0MjdlbEhDU3JmcUkxMTh5SEEifQ..Fl_cSt3yNZjODXzmBALLpg.bWmVv0sGJysR-S83_lGUyWv4piA7o_GKG-j3nmrE6CJmUaW0lLTmBNnJ5KldEPjoJMZtYKJWJW8B5ISAg8I6bXYW2Dg6lSfBOhiY2-O2WM2paHDIoz6K6LLp26Qh32xgc_fToqXXAIp7uwEA4pz1e75U0E-uwTnBES0lg8OuI6tUSaCeY9v4hfk0o4vKsnQIAFzn2sUED5pV3zubO1Mo8g.qHcu9yjY88Ccaz46INWP0w1TDIg-8ygy4_Rb1sVJWDw",
    "path": "/",
})

try:
    #เปิดเว็บไซต์ และเช็กว่าเปิดแล้ว
    driver.get("http://localhost:3000/role1-admin")
    
    signin = driver.find_element(By.XPATH,"//p[contains(@class, 'text-white')]").text
    assert signin == "ผู้ดูแลระบบครุภัณฑ์"
    print("✅ Check the success words")

    dropdown_button = driver.find_element(By.XPATH, "//button[span[text()='จัดการครุภัณฑ์']]")
    dropdown_button.click()

    submenu_item = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//a[span[text()='รายการครุภัณฑ์']]"))
    )   
    submenu_item.click()
    time.sleep(2)

    driver.find_element(By.XPATH,"//section/div[1]/div/button[1]").click()
    time.sleep(2)

    dropdown = Select(driver.find_element(By.XPATH,"//form//div[2]//select"))
    dropdown.select_by_visible_text("ครุภัณฑ์การแพทย์และวิทยาศาสตร์")
    driver.find_element(By.XPATH,"//input[@placeholder='0000-000-0000/0']").send_keys("1111-222-3333/12")
    driver.find_element(By.XPATH,"//input[@placeholder='กรอกเลข ID']").send_keys("10005")
    driver.find_element(By.XPATH,"//input[@placeholder='ชุดแอลกอฮอลเท้าเหยียบ']").send_keys("เครื่องชั่งดิจิทัล")
    driver.find_element(By.XPATH,"//textarea[@placeholder='เป็นสแตนเลส แบบเท้าเหยียบ']").send_keys("อุปกรณ์วัดน้ำหนัก")
    driver.find_element(By.XPATH,"//input[@placeholder='60,000']").send_keys("1200")
    
    date_input = driver.find_element(By.XPATH, "//input[@type='date']")
    #date_input.clear()
    date_input.send_keys("08/01/2550")  

    driver.find_element(By.XPATH,"//form/div[10]/button[2]").click()
    time.sleep(5)
    
    driver.save_screenshot(os.path.join(folder_name, "TC_ADListKaruphan_02.png"))
    time.sleep(1)

finally:
    driver.quit()