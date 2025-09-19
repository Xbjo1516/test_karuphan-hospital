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
    "value": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoibGNHbXhocGltT3FvM3loZU1VYi0zUENJaGFJeWpGdWwxMUVnbF82aldITEpfUzIxOXJmZmRXNlZvWFZqbWVnaVNvdEh0MjdlbEhDU3JmcUkxMTh5SEEifQ..xunMeUPMP0wg1Un1wdQxNg.G5R6gW3NZ7KY8ySqVQsRgjV__etlEGv3WWiuct9U7XXMwUpx78OOMwmo_XWY_leYIW0KMUljo9SeW9IKGNdCJ7ILgFQ4xGNdys8sOro1KMbQaIQhA4w-gkrenVPp_1AboTNYHFZQGoLfNXPweYfnEmnjAP12Susy25DYclXV__y5W-pxjXsuZT59Pf2Y1cV-nAOaGyhxVBbwRTvYAZYE94af_C1lZbnqqmll__YHCSybKbJcZhPL2mTntR6kpTX0X9HU7c_3WCpZQkjFmV-yTjKxC6Ex-E7oQ05R3lX3vsMxkdmTBv6_tmTFDRkC6FAAtsDaWzDZAb9joUmlXTE0m17Jrknc3xVKTjQ9VVazTEceScmPeH1WZBJVwvrOwBnh.Z6TE3ozbxNpfjyr0Q_Pkzx1QjKW8duhu-PPRfv4BHqs",
    "path": "/",
})

try:
    #เปิดเว็บไซต์ และเช็กว่าเปิดแล้ว
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
    assert amount == "รวม 5 ชิ้น จาก 5 รายการ"
    print("✅ Check the success words")
    time.sleep(2)

    driver.find_element(By.XPATH, "//button[text()='ยกเลิกการยืม']").click()
    time.sleep(2)

    zero = driver.find_element(By.XPATH, "//span[@class='bg-red-100 text-red-800 text-sm font-medium px-2 py-1 rounded-full']").text
    #print(f"a = '{zero}'")
    assert zero == "0 ชิ้น"
    print("✅ Check the success words")

    driver.save_screenshot(os.path.join(folder_name, "TC_EXBorrowKaruphan_04.png"))
    time.sleep(1)

finally:
    driver.quit()