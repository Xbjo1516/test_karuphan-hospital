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
    "value": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoibGNHbXhocGltT3FvM3loZU1VYi0zUENJaGFJeWpGdWwxMUVnbF82aldITEpfUzIxOXJmZmRXNlZvWFZqbWVnaVNvdEh0MjdlbEhDU3JmcUkxMTh5SEEifQ..lac3njMje46WCneeEjcb9w.cNLedmSN9j2qLhBpIGlVQFbRLHDicsZ09ZvjVZV4ms9yPFsYq7hkSOw7QKqfrfCARwIPQJg07JaurWL_ZZTOKoMu1psrIeMBdFYw2LE71JFEftHpE6tNKbzHqyYjvuhfgVgwgHCaKWwX6_vJ_bI2GTJPE3hGHGdUtNUIapDtOQP7PCvb-QQ3nxvY5ZxuqIZzuZVGoCn0BbCeaHujdZPuAnheNvZ8iUm6_K63fgJEGJYhCus53d_bBk_TdfnqQrEZE5oR00HoZ7SRLXNHL5McqHLK3KYnDXFMXfFYXe9PLK-8pOD9QGblmdXrpdiWYuaWP8j41NbOqqYz8ZlQEKkGMUEp-XQGPyOTS6cftF97kA22xENHYosAEJJoAob50xyzbfGUABcuslPy7JkOX7dMCFjdsiJjjyvLEi3vlpAsXL0.na-mBaIwCwWh2HAbcC6wS7bP6yYvt2A_2esU-bTmBS0",
    "path": "/",
})

try:
    #เปิดเว็บไซต์ และเช็กว่าเปิดแล้ว
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
    assert amount == "รวม 5 ชิ้น จาก 5 รายการ"
    print("✅ Check the success words")
    time.sleep(2)

    driver.find_element(By.XPATH, "//button[text()='ยกเลิกการยืม']").click()
    time.sleep(2)

    zero = driver.find_element(By.XPATH, "//span[@class='bg-red-100 text-red-800 text-sm font-medium px-2 py-1 rounded-full']").text
    #print(f"a = '{zero}'")
    assert zero == "0 ชิ้น"
    print("✅ Check the success words")

    driver.save_screenshot(os.path.join(folder_name, "TC_INBorrowKaruphan_04.png"))
    time.sleep(1)

finally:
    driver.quit()