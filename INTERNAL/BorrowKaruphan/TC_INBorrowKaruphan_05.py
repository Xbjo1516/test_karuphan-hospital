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

cookie_admin = {
    "name": "authjs.session-token",
    "value": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoibGNHbXhocGltT3FvM3loZU1VYi0zUENJaGFJeWpGdWwxMUVnbF82aldITEpfUzIxOXJmZmRXNlZvWFZqbWVnaVNvdEh0MjdlbEhDU3JmcUkxMTh5SEEifQ..VTKp1TDp8rRiSLBkWDjCUg.Uoia6LJHR5N-pGzQ0wUqOuuJj71eF3ZellCT0mM_bpfepsuYzyvVU8tvKCmGkw82pdVGA8cc7862mhrEYvc7ZkNaXQM0ud6no2hepArIuhOotkL4GS4san-ctF3ByOvUd-5Zm448jPrhANjszo-bPbzf44uXW8XzKlNW9x-P7XIiIU_sl9P9m7ZPRfhJ7USYtK6EJQIUlNW0jZJvbr0kz0m6vVqkGoPPsOOPTLBtyU4.0msaWb91YkpU6fg7ohEbbrFfR4UnYnFe2gnaPr1Q3K8", 
    "path": "/",
}

cookie_internal = {
    "name": "authjs.session-token",
    "value": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoibGNHbXhocGltT3FvM3loZU1VYi0zUENJaGFJeWpGdWwxMUVnbF82aldITEpfUzIxOXJmZmRXNlZvWFZqbWVnaVNvdEh0MjdlbEhDU3JmcUkxMTh5SEEifQ..lac3njMje46WCneeEjcb9w.cNLedmSN9j2qLhBpIGlVQFbRLHDicsZ09ZvjVZV4ms9yPFsYq7hkSOw7QKqfrfCARwIPQJg07JaurWL_ZZTOKoMu1psrIeMBdFYw2LE71JFEftHpE6tNKbzHqyYjvuhfgVgwgHCaKWwX6_vJ_bI2GTJPE3hGHGdUtNUIapDtOQP7PCvb-QQ3nxvY5ZxuqIZzuZVGoCn0BbCeaHujdZPuAnheNvZ8iUm6_K63fgJEGJYhCus53d_bBk_TdfnqQrEZE5oR00HoZ7SRLXNHL5McqHLK3KYnDXFMXfFYXe9PLK-8pOD9QGblmdXrpdiWYuaWP8j41NbOqqYz8ZlQEKkGMUEp-XQGPyOTS6cftF97kA22xENHYosAEJJoAob50xyzbfGUABcuslPy7JkOX7dMCFjdsiJjjyvLEi3vlpAsXL0.na-mBaIwCwWh2HAbcC6wS7bP6yYvt2A_2esU-bTmBS0",
    "path": "/",
}

try:
    driver.get("http://localhost:3000")   
    driver.add_cookie(cookie_internal)    
    driver.get("http://localhost:3000/role2-internal")

    time.sleep(2)

    role = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[2]/p[2]"))).text
    assert role == "กลุ่มงานบริการด้านปฐมภูมิและองค์รวม"
    print("✅ Check Role success")

    driver.find_element(By.XPATH, "//section/div[2]/table/thead/tr/th[1]/input").click()
    time.sleep(2)

    driver.find_element(By.XPATH, "//section/div[3]/button").click()

    amount = driver.find_element(By.XPATH, "//div[2]//div[3]/p").text
    #print(f"a = '{amount}'")
    assert amount == "รวม 5 ชิ้น จาก 5 รายการ"
    print("✅ Check the success words")
    time.sleep(2)

    driver.find_element(By.XPATH, "//button[text()='ยืนยันการยืม']").click()
    time.sleep(2)

    popup = driver.find_element(By.XPATH, "//div[contains(@class,'bg-white') and contains(@class,'rounded-2xl')]")
    borrowlist = driver.find_element(By.XPATH,".//h2[text()='รายการยืมที่ต้องการ']").text
    assert borrowlist == "รายการยืมที่ต้องการ"
    print("✅ Check the success words")

    driver.find_element(By.XPATH, "//form/div[2]/div/input").send_keys("10/20/2025")
    driver.find_element(By.XPATH, "//form/div[3]/div/textarea").send_keys("ยืม")

    driver.find_element(By.XPATH, "//button[text()='บันทึก']").click()
    time.sleep(2)

    try:
        alert = driver.switch_to.alert
        print("⚠️ Alert detected:", alert.text)
        alert.accept()  # กด OK / ยอมรับ
        print("✅ Alert accepted")
    except NoAlertPresentException:
        print("No alert present")
    
# ---------------- Admin Login แทนการใส่ cookie ----------------
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

# ไปหน้า login ของระบบ
    driver.get("http://localhost:3000")
    time.sleep(1)

# ล้างทุกอย่างให้แน่ใจ
    driver.delete_all_cookies()
    driver.execute_script("window.localStorage.clear();")
    driver.execute_script("window.sessionStorage.clear();")
    time.sleep(0.5)

# โหลดหน้า login ใหม่อีกรอบเพื่อให้ไม่มี token
    driver.get("http://localhost:3000")
    time.sleep(3)

# กรอกอีเมลและรหัสผ่าน admin
    driver.find_element(By.XPATH,"/html/body/div[1]/form/input").send_keys("admin@pcu.local")
    driver.find_element(By.XPATH,"/html/body/div[1]/form/div[1]/input").send_keys("Admin#1234")
    driver.find_element(By.XPATH,"/html/body/div[1]/form/button").click()
    time.sleep(2)

# ตรวจสอบ role ของ admin
    role_text = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[2]/p[2]"))
    ).text
    print("👤 ตอนนี้อยู่ role:", role_text)


# ดำเนินการต่อกับปุ่มอนุมัติ
    approve_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[text()='อนุมัติแล้ว/รอคืน']"))
    ).click()
    time.sleep(2)

    driver.save_screenshot(os.path.join(folder_name, "TC_INBorrowKaruphan_05.png"))
    time.sleep(1)

finally:
    driver.quit()