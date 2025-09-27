from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

import time, glob, os, pyautogui

folder_name = "screenshots"
os.makedirs(folder_name, exist_ok=True)

# การเปิดหน้าเว็บโดยไม่ปิดเอง
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)
driver.maximize_window()

try:
    driver.get("https://karuphan-hospital-production.up.railway.app/")
    
    signin = driver.find_element(By.XPATH,"//form/h1").text
    assert signin == "ระบบครุภัณฑ์"
    print("✅ Check the success words")

    driver.find_element(By.XPATH,"/html/body/div[1]/form/input").send_keys("admin@pcu.test")
    driver.find_element(By.XPATH,"/html/body/div[1]/form/div[1]/input").send_keys("Admin#1234")
    driver.find_element(By.XPATH,"/html/body/div[1]/form/button").click()
    time.sleep(2)

    assert "karuphan-hospital" in driver.title
    print("✅ Home page loaded")
    time.sleep(1)

    Role = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, "//div[2]/p[1]"))).text.strip()
    assert Role == "ผู้ดูแลระบบครุภัณฑ์"
    print("✅ Check Role success")

    # คลิกเมนูรายงาน
    dropdown_button = driver.find_element(By.XPATH, "//button[span[text()='รายงานสรุปผล']]")
    dropdown_button.click()

    submenu_item = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//a[span[text()='รายงานสถานะของครุภัณฑ์']]"))
    )
    submenu_item.click()
    time.sleep(2)

    dropdown = Select(driver.find_element(By.XPATH, "//select"))
    dropdown.select_by_visible_text("ครุภัณฑ์ทางการแพทย์และวิทยาศาสตร์")
    time.sleep(2)

    # คลิกปุ่มดาวน์โหลด Excel
    excel_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='ดาวน์โหลด Excel']"))
    )
    excel_button.click()
    print("📥 กำลังดาวน์โหลดไฟล์ Excel...")
    time.sleep(5)
    
    # ✅ รอจนไฟล์โหลดเสร็จ (ไม่มี .crdownload ค้างอยู่)
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    while True:
        if not glob.glob(os.path.join(downloads_folder, "*.crdownload")):
            break
        time.sleep(1)

    list_of_files = glob.glob(os.path.join(downloads_folder, "*.csv"))
    latest_file = max(list_of_files, key=os.path.getctime)

    # ✅ เปิดไฟล์ Excel
    os.startfile(latest_file)
    print("📂 เปิดไฟล์ Excel แล้ว")
    time.sleep(10)
    # Screenshot
    screenshot_path = os.path.join(folder_name, "TC_ADSendDataBorrowStatus_02.png")
    pyautogui.screenshot(screenshot_path)
    time.sleep(1)

finally:
    driver.quit()
