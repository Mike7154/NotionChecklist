import requests
import json
import mlfiles
import datetime
import mldates
import mlnotion

token = mlfiles.load_setting("Gen","token")
items_id = mlfiles.load_setting("Gen","checklist_items")
instance_id = mlfiles.load_setting("Gen","checklist_instance")
headers = {
  "Authorization": "Bearer " + token,
  "Content-Type": "application/json",
  "Notion-Version": "2021-05-13"
}

# Define a filter object that matches pages where Archive and add_next are both true
filter_obj = {
  "filter": {
    "and": [
      {
        "property": "Archive",
        "checkbox": {
          "equals": False
        }
      },
      {
        "property": "add_next",
        "checkbox": {
          "equals": True
        }
      }
    ]
  }
}

# Query the pages in the source database that match the filter
query_url = f"https://api.notion.com/v1/databases/{items_id}/query"
res = requests.post(query_url, headers=headers, data=json.dumps(filter_obj))
results = res.json()["results"]

# Query the pages in the destination database
dest_query_url = f"https://api.notion.com/v1/databases/{instance_id}/query"
dest_res = requests.post(dest_query_url, headers=headers)
dest_results = dest_res.json()["results"]

# Loop through each page in the source database and create a copy in the destination database
for page in results:
  # Get the page id and name
  try:
    page_id = page["id"]
    name = page["properties"]["Name"]["title"][0]["plain_text"]
    # Create a relation object that links to the original page
    relation = [{"id": page_id}]
    interval_type = page['properties']['Type']['select']['name']
    if interval_type != 'Daily':
      nth = page['properties']['on']['rich_text'][0]['plain_text']
      units = page['properties']['Units']['select']['name']
    dates = mldates.next_date_matching_list(nth, units, interval_type)
    for next_date in dates:
      # Check if there is an entry with the same date and checklist item in the destination database
      exist = False
      if next_date != dates[0] and (next_date > (datetime.datetime.now().date() + datetime.timedelta(days=30))):
        exist = True
        break
      today = next_date.isoformat()
      for dest_page in dest_results:
        # Get the date and relation properties of the destination page
        dest_date = dest_page["properties"]["Date"]["date"]["start"]
        dest_relation = dest_page["properties"]["Checklist Item"]["relation"][0]["id"]
        # Compare with the current date and relation
        if dest_date == today and dest_relation == page_id:
          exist = True
          break
      # If there is no entry with the same date and checklist item, create a new page in the destination database with only the name, relation and date properties
      if not exist:
        create_url = "https://api.notion.com/v1/pages"
        new_page_data = {
          "parent": {"database_id": instance_id},
          "properties": {
            "Name": {"title": [{"text": {"content": name}}]},
            "Checklist Item": {"relation": relation},
            "Date": {"date": {"start": today}} # Set the date property to today's date in MST
          }
        }
        res = requests.post(create_url, headers=headers, data=json.dumps(new_page_data))
        data = res.json()
        page_id2 = data.get("id")
        res2 = mlnotion.copy_blocks(page_id,page_id2,token)
        if res2 != None:
          print(res2)
  except IndexError as e:
    # If there is an IndexError, print it and continue to the next item
    print("Error:", e)
    continue