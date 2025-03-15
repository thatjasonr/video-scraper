from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json
import datetime

# Set up Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)

def fetch_all_video_data():
    """
    Fetches video data including title, runtime, categories, image URL, and entitlement.
    """
    driver.get("https://video.leedsunited.com/view?search=Latest%20Videos")

    # Wait for video cards to load
    videos = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "card-video-container"))
    )

    video_data = []
    for video in videos:
        try:
            # Extract runtime
            runtime = video.find_element(By.CLASS_NAME, "runtime").text
            
            # Extract title
            title = video.find_element(By.CLASS_NAME, "card-body__title").get_attribute("title")
            
            # Extract categories
            categories_div = video.find_element(By.CLASS_NAME, "card-body__categories")
            categories = [category.text for category in categories_div.find_elements(By.CLASS_NAME, "card-body__category")]
            
            # Extract image URL
            image_element = video.find_element(By.TAG_NAME, "img")
            image_url = image_element.get_attribute("src")
            
            # Extract entitlement (e.g., "premium" or "free")
            try:
                entitlement = video.find_element(By.CLASS_NAME, "entitlement").text
            except:
                entitlement = "free"  # Default to "free" if not found
            
            # Extract video URL
            try:
                parent_a_tag = video.find_element(By.XPATH, "./ancestor::a")  # Get the enclosing <a> tag
                video_url = parent_a_tag.get_attribute("href")
                if not video_url.startswith("http"):  # Handle relative URLs
                    video_url = f"https://video.leedsunited.com{video_url}"
            except:
                video_url = "N/A"  # Default if URL is not found

            # Add extracted data to the list
            video
