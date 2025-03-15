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
    Fetches video data including title, runtime, categories, image URL, entitlement, and video URL.
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
            video_data.append({
                "title": title,
                "runtime": runtime,
                "categories": categories,
                "image_url": image_url,
                "entitlement": entitlement,
                "video_url": video_url,  # Add URL to the data structure
            })

        except Exception as e:
            print(f"Skipped a video due to error: {e}")

    return video_data

def save_data_to_json(data, filename="video_data.json"):
    """
    Saves the extracted data to a JSON file, adding a timestamp.
    """
    # Add a timestamp to the data
    data_with_timestamp = {
        "timestamp": datetime.datetime.now().isoformat(),  # Add timestamp
        "videos": data
    }

    with open(filename, "w") as file:
        json.dump(data_with_timestamp, file, indent=4)
    print(f"Data saved to {filename}")

# Main function to fetch data and save it
def main():
    data = fetch_all_video_data()
    for video in data:
        print(f"Title: {video['title']}")
        print(f"Runtime: {video['runtime']}")
        print(f"Categories: {', '.join(video['categories'])}")
        print(f"Image URL: {video['image_url']}")
        print(f"Entitlement: {video['entitlement']}")
        print(f"Video URL: {video['video_url']}")
        print("-" * 40)

    # Save data to JSON
    save_data_to_json(data)

# Run the script
if __name__ == "__main__":
    main()

    # Close the browser
    driver.quit()
