import time
import requests
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def check_image_size(url):
    try:
        response = requests.head(url)
        size = int(response.headers.get('content-length', 0))
        return size > 5 * 1024  # 5KB in bytes
    except:
        return False

def get_image_urls(query, max_images=10):
    # Configure headless browser
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")

    # Initialize browser
    CHROMEDRIVER_PATH = r"C:\Users\Satyam Thakur\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
    service = Service(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    image_urls = []

    try:
        # Open Google Images
        driver.get(f"https://www.google.com/search?q={quote(query)}&tbm=isch")
        print(f"Searching for {query} images...")

        # Scroll to load initial images
        for _ in range(2):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1.5)

        # Find image elements
        img_elements = driver.find_elements(By.CSS_SELECTOR, 'img.YQ4gaf')
        print(f"Found {len(img_elements)} potential images")

        # Collect only HTTPS URLs with size > 5KB
        for img in img_elements:
            if len(image_urls) >= max_images:
                break

            img_url = img.get_attribute("src")
            if img_url and img_url.startswith('http'):
                if check_image_size(img_url):
                    image_urls.append(img_url)
                    print(f"Found valid image URL: {img_url}")
                else:
                    print(f"Skipped small image: {img_url}")

        print(f"\nCollected {len(image_urls)} valid image URLs")
        return image_urls

    finally:
        driver.quit()
        print("Browser closed")

if __name__ == "__main__":
    urls = get_image_urls("Tiger")
    print("\nFinal URL list:")
    print(urls)