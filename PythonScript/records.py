import os
import random
import requests
import xml.etree.ElementTree as ET

# Always point to the XML folder version
XML_FILE = os.path.join("XML", "records.xml")

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
    {"artist": "Matt Maltese", "title": "Krystal"},
    {"artist": "Arctic Monkeys", "title": "AM"},
    {"artist": "Silk Sonic", "title": "An Evening with Silk Sonic"},
    {"artist": "Olivia Rodrigo", "title": "SOUR"},
    {"artist": "Alec Benjamin", "title": "These Two Windows"},
    {"artist": "Alec Benjamin", "title": "Narrated for You"}
]


def load_existing_titles():
    """Return a set of titles already in records.xml."""
    if not os.path.exists(XML_FILE):
        return set()

    tree = ET.parse(XML_FILE)
    root = tree.getroot()
    titles = set()

    for album in root.findall("album"):
        title_el = album.find("title")
        if title_el is not None and title_el.text:
            titles.add(title_el.text.strip())

    return titles


def fetch_from_deezer(artist, title):
    query = f"{artist} {title}"
    url = f"https://api.deezer.com/search/album?q={query}"

    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        results = data.get("data", [])
        if results:
            return results[0]
    except Exception as e:
        print("  -> Error calling Deezer:", e)

    return None


def generate_random_price():
    """Generate a random price between 12.99 and 39.99, formatted with 2 decimals."""
    value = random.uniform(12.99, 39.99)
    return f"{value:.2f}"


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
    # New: random price
    ET.SubElement(a, "price").text = generate_random_price()

    print("  -> Added:", result["title"])

# SAVE XML
tree = ET.ElementTree(root)
ET.indent(tree, space="  ", level=0)
tree.write(XML_FILE, encoding="utf-8", xml_declaration=True)

print("\n✓ records.xml updated successfully!")
