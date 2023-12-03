# import asyncio
# import re
# import aiohttp
# def extract_file_id_from_url(url):
#     # Regular expression pattern to extract the file ID
#     pattern = r"/file/d/([a-zA-Z0-9_-]+)"

#     # Find matches using the pattern
#     match = re.search(pattern, url)

#     if match:
#         file_id = match.group(1)
#         return file_id
#     else:
#         return None


# link ="https://drive.google.com/file/d/16uZ4cwjFr9FrHZGeNectwwLg5su1mXl0/view?usp=sharing"

# file_id = extract_file_id_from_url(link)

# async def get_file_metadata(file_id, api_key):
#     metadata_url = f"https://www.googleapis.com/drive/v3/files/{file_id}?fields=name&key={api_key}"

#     try:
#         async with aiohttp.ClientSession() as session:
#             async with session.get(metadata_url) as response:
#                 if response.status == 200:
#                     metadata = await response.json()
#                     return metadata.get('name')
#                 else:
#                     print(f"Failed to fetch metadata. Status code: {response.status}")
#                     return None

#     except Exception as e:
#         print(f"An error occurred while fetching metadata: {e}")
#         return None



# async def print_file_metadata(file_id, api_key):
#     file_name = await get_file_metadata(file_id, api_key)
#     if file_name:
#         print(f"File name: {file_name}")
#     else:
#         print("No metadata found")

# api_key = 'AIzaSyCBlVMt3uiyBu3F22Q_IO4VNuMn5byzVng'
# asyncio.run(print_file_metadata(file_id=file_id, api_key=api_key))