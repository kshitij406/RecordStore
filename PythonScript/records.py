import os
import requests
import xml.etree.ElementTree as ET

XML_FILE = "records.xml"

albums = [
    {"artist": "Jeff Buckley", "title": "Grace"},
    {"artist": "Pink Floyd", "title": "The Dark Side of the Moon"},
    {"artist": "The Beatles", "title": "Abbey Road"},
    {"artist": "Kanye West", "title": "Yeezus"},
    {"artist": "Tame Impala", "title": "Currents"},
    {"artist": "The Marías", "title": "Submarine"},
    {"artist": "Frank Ocean", "title": "Blonde"},
    {"artist": "Radiohead", "title": "The Bends"},
    {"artist": "The Smiths", "title": "The Queen is Dead"},
    {"artist": "Justin Hurwitz", "title": "La La Land (Original Motion Picture Soundtrack)"},
    {"artist": "Steve Lacy", "title": "Gemini Rights"},
    {"artist": "Daft Punk", "title": "Random Access Memories"},
    {"artist": "FINNEAS", "title": "Optimist"},
    {"artist": "Radiohead", "title": "OK Computer"},
    {"artist": "Phoebe Bridgers", "title": "Stranger in the Alps"},
    {"artist": "Kanye West", "title": "My Beautiful Dark Twisted Fantasy"},
    {"artist": "Mac DeMarco", "title": "Another One"},
    {"artist": "The Weeknd", "title": "Dawn FM"},
    {"artist": "Tyler, The Creator", "title": "IGOR"},
    {"artist": "Tory Lanez", "title": "Alone at Prom"},
    {"artist": "Kendrick Lamar", "title": "Mr. Morale & The Big Steppers"},
    {"artist": "Kanye West", "title": "Graduation"},
    {"artist": "American Football", "title": "Krystal"},
    {"artist": "Arctic Monkeys", "title": "AM"},
    {"artist": "Silk Sonic", "title": "An Evening with Silk Sonic"},
    {"artist": "Olivia Rodrigo", "title": "SOUR"},
    {"artist": "NIKI", "title": "These Two Windows"},
    {"artist": "Alec Benjamin", "title": "Narrated for You"}
]


# LOAD EXISTING XML (if present)

def load_existing_titles():
    """Return a set of titles already in records.xml."""
    if not os.path.exists(XML_FILE):
        return set()

    tree = ET.parse(XML_FILE)
    root = tree.getroot()
    titles = set()

    for album in root.findall("album"):
        title = album.find("title").text.strip()
        titles.add(title)

    return titles


# FETCH SINGLE ALBUM FROM DEEZER

def fetch_from_deezer(artist, title):
    query = f"{artist} {title}"
    url = f"https://api.deezer.com/search/album?q={query}"

    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        results = data.get("data", [])
        if results:
            return results[0]
    except:
        pass

    return None

# Load existing titles
existing_titles = load_existing_titles()
print("Already in XML:", existing_titles)

# Prepare XML root (load or create new)
if os.path.exists(XML_FILE):
    tree = ET.parse(XML_FILE)
    root = tree.getroot()
else:
    root = ET.Element("records")

# Process albums
for album in albums:
    title = album["title"]

    if title in existing_titles:
        print(f"Skipping (already exists): {title}")
        continue

    print(f"Fetching from Deezer: {album['artist']} - {title}")
    result = fetch_from_deezer(album["artist"], title)

    if result is None:
        print("  -> No result found")
        continue

    # Create album entry in XML
    a = ET.SubElement(root, "album")
    ET.SubElement(a, "title").text = result["title"]
    ET.SubElement(a, "artist").text = result["artist"]["name"]
    ET.SubElement(a, "id").text = str(result["id"])
    ET.SubElement(a, "cover_medium").text = result["cover_medium"]

    print("  -> Added:", result["title"])


# SAVE XML 

tree = ET.ElementTree(root)
ET.indent(tree, space="  ", level=0)
tree.write("XML/records.xml", encoding="utf-8", xml_declaration=True)

print("\n✓ records.xml updated successfully!")
