from selenium.common import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

mobile_emulation = {
    "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
    "userAgent": "Chrome/122.0.6261.94"
}

chrome_options = Options()
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://m.twitch.tv/")
wait = WebDriverWait(driver, timeout=10)


def test_twitch():
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Close']"))).click()
    driver.find_element(By.XPATH, "//a[@href='/search']").click()
    driver.find_element(By.XPATH, "//input[@type='search']").send_keys("StarCraft II")
    driver.find_element(By.XPATH, "//p[@title='StarCraft II']").click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//p[text()='View All']"))).click()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.tw-link")))
    all_visible_streams = driver.find_elements(By.CSS_SELECTOR, "a.tw-link")
    driver.execute_script("arguments[0].scrollIntoView();", all_visible_streams[3])
    driver.execute_script("arguments[0].scrollIntoView();", all_visible_streams[6])
    all_visible_streams = driver.find_elements(By.CSS_SELECTOR, "a.tw-link")
    all_visible_streams[1].click()
    wait.until(EC.presence_of_element_located((By.XPATH, "//video[@controls]")))
    try:
        start_watching = driver.find_element(By.XPATH, "//div[text() = 'Start Watching']")
        start_watching.click()
    except NoSuchElementException:
        pass
    driver.save_screenshot("screenshot.png")

