import requests as re
import xml.etree.ElementTree as ET

base_url = "https://api.deezer.com/chart/0/albums"

# Fetch data from Deezer API
response = re.get(base_url)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
else:
    print("Error fetching data:", response.status_code)

# Parse the JSON data
albums = data["data"]

# Prepare the records list
records = []

# Extract relevant information from each album
for album in albums:
    record = {
        "rank": album["position"],
        "name" : album["title"],
        "artist": album["artist"]["name"],
        "cover_medium" : album["cover_medium"]
    }
    records.append(record)

# Create XML structure
# <records>
root = ET.Element("top_albums")

for rec in records:
    # <record rank="1">
    record_el = ET.SubElement(root, "record")
    record_el.set("rank", str(rec["rank"]))

    # <name>Song</name>
    name_el = ET.SubElement(record_el, "name")
    name_el.text = str(rec["name"])

    # <artist>Artist</artist>
    artist_el = ET.SubElement(record_el, "artist")
    artist_el.text = str(rec["artist"])

    # <cover_medium>URL</cover_medium>
    cover_el = ET.SubElement(record_el, "cover_medium")
    cover_el.text = str(rec["cover_medium"])

# Turn the tree into an XML file
tree = ET.ElementTree(root)
ET.indent(tree, space="  ", level=0)  
tree.write("XML/top_records.xml", encoding="utf-8", xml_declaration=True)

    