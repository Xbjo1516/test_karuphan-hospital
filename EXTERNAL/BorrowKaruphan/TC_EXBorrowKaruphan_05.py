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
    "value": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoibGNHbXhocGltT3FvM3loZU1VYi0zUENJaGFJeWpGdWwxMUVnbF82aldITEpfUzIxOXJmZmRXNlZvWFZqbWVnaVNvdEh0MjdlbEhDU3JmcUkxMTh5SEEifQ..RCYq70t8gX6PbQ2ONrE8VA.Pi7cJVbi3r2Sm8VcVwdM9WkktQlMy9lIC13c_G5Nd5Oz99nsF-AIZE1m3K5r4mLtcaBhRbxmbC60ul-EOOLKGeRV2cFOXuzo7L4Uz-aMgs9K1YHc812kcgfHBTlaljb8DGNosDvViuoRaEHVHEykXJB_Vu8rUNy59UfbEWwKEdE9J-ku-kTq1VbJ36SjoeLVD0blxbu3Zl_EFSGHrik7cxEQrL9lEvu8C1nX9XTSzTU.eOxAciP3Tmd_bivlrx1P-tnkyONZekDdPkw4JDtPKXw",  # token ของ role1-admin
    "path": "/",
}

cookie_external = {
    "name": "authjs.session-token",
    "value": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoibGNHbXhocGltT3FvM3loZU1VYi0zUENJaGFJeWpGdWwxMUVnbF82aldITEpfUzIxOXJmZmRXNlZvWFZqbWVnaVNvdEh0MjdlbEhDU3JmcUkxMTh5SEEifQ..xunMeUPMP0wg1Un1wdQxNg.G5R6gW3NZ7KY8ySqVQsRgjV__etlEGv3WWiuct9U7XXMwUpx78OOMwmo_XWY_leYIW0KMUljo9SeW9IKGNdCJ7ILgFQ4xGNdys8sOro1KMbQaIQhA4w-gkrenVPp_1AboTNYHFZQGoLfNXPweYfnEmnjAP12Susy25DYclXV__y5W-pxjXsuZT59Pf2Y1cV-nAOaGyhxVBbwRTvYAZYE94af_C1lZbnqqmll__YHCSybKbJcZhPL2mTntR6kpTX0X9HU7c_3WCpZQkjFmV-yTjKxC6Ex-E7oQ05R3lX3vsMxkdmTBv6_tmTFDRkC6FAAtsDaWzDZAb9joUmlXTE0m17Jrknc3xVKTjQ9VVazTEceScmPeH1WZBJVwvrOwBnh.Z6TE3ozbxNpfjyr0Q_Pkzx1QjKW8duhu-PPRfv4BHqs",  # token ของ role3-external
    "path": "/",
}

try:
    driver.get("http://localhost:3000")   
    driver.add_cookie(cookie_external)    
    driver.get("http://localhost:3000/role3-external")

    time.sleep(2)

    role = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[2]/p[2]"))).text
    assert role == "กลุ่มงานเทคนิคการแพทย์"
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
        EC.presence_of_element_located((By.XPATH, "//button[text()='รออนุมัติ']"))
    ).click()
    time.sleep(2)

    driver.save_screenshot(os.path.join(folder_name, "TC_EXBorrowKaruphan_05.png"))
    time.sleep(1)

finally:
    driver.quit()