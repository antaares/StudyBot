import re

def extract_file_id_from_url(url):
    # Regular expression pattern to extract the file ID
    pattern = r"/file/d/([a-zA-Z0-9_-]+)"

    # Find matches using the pattern
    match = re.search(pattern, url)

    if match:
        file_id = match.group(1)
        return file_id
    else:
        return None

# Example URL
url = "https://drive.google.com/file/d/1jVC7kOJ5OdxmaVj05uxuO1kXvYzpWoay/view?usp=drive_link"

file_id = extract_file_id_from_url(url)
if file_id:
    print(f"Extracted File ID: {file_id}")
else:
    print("File ID not found in the URL.")
