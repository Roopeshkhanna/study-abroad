import sys
import codecs
import json
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Set UTF-8 encoding for console output
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer)

# Set up Selenium options
options = Options()
options.add_argument("--headless")  # Run in headless mode (no browser window)
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36")

# Initialize Selenium WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Base URL for university data
base_url = "https://nces.ed.gov/collegenavigator/?s=all&id="

# Load university data JSON file
file_path = r"C:\\Users\\roope\\OneDrive\\Desktop\\proj_sa\\study-abroad\\university_code.json"
with open(file_path, "r", encoding="utf-8") as file:
    university_data = json.load(file)

# Sections to scrape
sections = ["#finaid"]

# Dictionary to store extracted data
data = {}

# Regular expression pattern to extract content from "General Information" to "College Navigator Home |"
info_pattern = re.compile(r"General Information(.*?)College Navigator Home", re.DOTALL)

def extract_relevant_info(text):
    match = info_pattern.search(text)
    return match.group(1).strip() if match else "❌ No relevant section found."

# Start scraping
for uni_name, uni_id in university_data.items():
    try:
        print(f"🔹 Extracting data for {uni_name} (ID: {uni_id})")
        university_info = {}

        for section in sections:
            url = base_url + str(uni_id) + section
            driver.get(url)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, "html.parser")
            text_content = soup.get_text().strip()

            # Extract relevant content
            extracted_info = extract_relevant_info(text_content)

            university_info[section] = extracted_info
            print(f"✅ Extracted data for {section} of {uni_name}")

        data[uni_name] = university_info

    except Exception as e:
        print(f"❌ Error extracting data for {uni_name}: {e}")

# Save extracted data to a text file
output_file = r"C:\\Users\\roope\\OneDrive\\Desktop\\proj_sa\\study-abroad\\university_data.txt"
with open(output_file, "w", encoding="utf-8") as text_file:
    for uni_name, sections_data in data.items():
        text_file.write(f"\n=== Data for {uni_name} ===\n")
        for section, content in sections_data.items():
            text_file.write(content + "\n\n")

# Close the Selenium driver
driver.quit()

print("✅ Text content saved to university_data.txt")

# Check if all sections exist in the extracted text
missing_sections = [section for section in sections if not any(data[uni].get(section, '').strip() for uni in data)]

if missing_sections:
    print(f"⚠️ Missing data for sections: {', '.join(missing_sections)}")
else:
    print("✅ All sections extracted successfully.")
