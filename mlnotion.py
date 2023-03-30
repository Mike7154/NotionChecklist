import requests

def copy_blocks(source_page_id, dest_page_id, notion_api_key):
    # A function that copies the blocks of text from one page in notion to another page in notion
    # source_page_id: a string containing the ID of the source page
    # dest_page_id: a string containing the ID of the destination page
    # notion_api_key: a string containing your notion api key
    
    # Define the headers for the API requests using the notion api key
    headers = {
        "Authorization": f"Bearer {notion_api_key}",
        "Notion-Version": "2021-05-13",
        "Content-Type": "application/json"
    }
    
    # Get the list of blocks from the source page
    source_url = f"https://api.notion.com/v1/blocks/{source_page_id}/children"
    source_response = requests.get(source_url, headers=headers)
    source_blocks = source_response.json().get("results", [])
    
    # Append the blocks to the destination page
    dest_url = f"https://api.notion.com/v1/blocks/{dest_page_id}/children"
    
    # Create a payload for appending the blocks
    payload = {
        "children": source_blocks
    }
    
    # Make a patch request to append the blocks
    dest_response = requests.patch(dest_url, headers=headers, json=payload)
    print(dest_response)
    
    # Check if the request was successful
    if dest_response.status_code == 200:
        # Get the json data from the response
        data = dest_response.json()
        
        # Get the list of appended blocks
        appended_blocks = data.get("results", [])
        
        # Return the list of appended blocks
        return appended_blocks
        print("YAY")
    
    else:
        # Raise an exception if the request failed
        raise Exception(f"Request failed with status code {dest_response.status_code}")