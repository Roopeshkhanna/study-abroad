from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json

# Set up options
options = Options()
options.add_argument("--headless")  # Run without opening a browser
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36")

# Automatically download and use ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Base URL for the university
base_url = "https://nces.ed.gov/collegenavigator/?s=all&id="

# Load the cleaned JSON file
file_path = r"C:\Users\Nithish\AppData\Local\Microsoft\Windows\INetCache\IE\53AZP6ZA\new_uni_nces[1].json"
with open(file_path, "r", encoding="utf-8") as file:
    university_data = json.load(file)

# Extract only the NCES IDs
nces_ids = list(university_data.values())

# Sections to scrape
sections = [
    "#general", "#expenses", "#finaid", "#netprc", "#enrolmt", "#admsns", "#retgrad", 
    "#outcome", "#programs", "#service", "#sports", "#accred", "#crime", "#fedloans"
]

# Dictionary to store extracted content
data = {}

for uni_name, uni_id in university_data.items():
    print(f"🔹 Extracting data for {uni_name} (ID: {uni_id})")
    university_info = {}
    for section in sections:
        url = base_url + str(uni_id) + section
        driver.get(url)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        text_content = soup.get_text()
        university_info[section] = text_content
        print(f"✅ Extracted data for {section} of {uni_name}")
    
    data[uni_name] = university_info

# Save extracted data to a text file
with open("university_data.txt", "w", encoding="utf-8") as text_file:
    for uni_name, sections_data in data.items():
        text_file.write(f"\n=== Data for {uni_name} ===\n")
        for section, content in sections_data.items():
            text_file.write(f"\n=== {section} ===\n")
            text_file.write(content + "\n\n")

# Close the driver
driver.quit()

print("✅ Text content saved to university_data.txt")

# Check if all sections exist in the extracted text
missing_sections = [section for section in sections if not any(data[uni].get(section, '').strip() for uni in data)]

if missing_sections:
    print(f"⚠️ Missing data for sections: {', '.join(missing_sections)}")
else:
    print("✅ All sections extracted successfully.")
