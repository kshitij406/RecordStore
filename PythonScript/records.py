import os
import random
import requests
import xml.etree.ElementTree as ET
from dotenv import load_dotenv

# CONFIG 

# Always point to the XML folder version
XML_FILE = os.path.join("XML", "records.xml")
load_dotenv()

# Spotify API credentials
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "YOUR_SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "YOUR_SPOTIFY_CLIENT_SECRET")

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
    {"artist": "Alec Benjamin", "title": "Narrated for You"},
]

# ============= HELPERS =============


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
    """Get album data from Deezer (for cover + basic info)."""
    query = f"{artist} {title}"
    url = f"https://api.deezer.com/search/album?q={query}"

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
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


def get_spotify_token(client_id, client_secret):
    """Get an app access token from Spotify."""
    url = "https://accounts.spotify.com/api/token"
    data = {"grant_type": "client_credentials"}

    resp = requests.post(url, data=data, auth=(client_id, client_secret), timeout=10)
    resp.raise_for_status()
    return resp.json()["access_token"]


def fetch_spotify_album_id(artist, title, token):
    """Search Spotify for the album and return its ID (or None)."""
    url = "https://api.spotify.com/v1/search"
    # use album + artist in query to make it precise
    query = f"album:{title} artist:{artist}"
    params = {"q": query, "type": "album", "limit": 1}
    headers = {"Authorization": f"Bearer {token}"}

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        items = data.get("albums", {}).get("items", [])
        if not items:
            # fallback: more relaxed query
            params["q"] = f"{title} {artist}"
            resp = requests.get(url, headers=headers, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            items = data.get("albums", {}).get("items", [])
            if not items:
                return None
        return items[0]["id"]
    except Exception as e:
        print("  -> Error calling Spotify:", e)
        return None


# ============= MAIN SCRIPT =============

def main():
    # Load existing titles
    existing_titles = load_existing_titles()
    print("Already in XML:", existing_titles)

    # Prepare XML root (load or create new)
    if os.path.exists(XML_FILE):
        tree = ET.parse(XML_FILE)
        root = tree.getroot()
    else:
        root = ET.Element("records")
        tree = ET.ElementTree(root)

    # Get Spotify token once
    if CLIENT_ID == "YOUR_SPOTIFY_CLIENT_ID" or CLIENT_SECRET == "YOUR_SPOTIFY_CLIENT_SECRET":
        print("WARNING: Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET (env vars or constants).")
        spotify_token = None
    else:
        try:
            spotify_token = get_spotify_token(CLIENT_ID, CLIENT_SECRET)
            print("Spotify token fetched successfully.")
        except Exception as e:
            print("Error getting Spotify token:", e)
            spotify_token = None

    # Process albums
    for album in albums:
        title = album["title"]
        artist = album["artist"]

        if title in existing_titles:
            print(f"Skipping (already exists): {title}")
            continue

        print(f"\nFetching from Deezer: {artist} - {title}")
        deezer_result = fetch_from_deezer(artist, title)

        if deezer_result is None:
            print("  -> No Deezer result found")
            continue

        # Create album entry in XML
        a = ET.SubElement(root, "album")
        ET.SubElement(a, "title").text = deezer_result["title"]
        ET.SubElement(a, "artist").text = deezer_result["artist"]["name"]
        ET.SubElement(a, "id").text = str(deezer_result["id"])
        ET.SubElement(a, "cover_medium").text = deezer_result["cover_medium"]
        ET.SubElement(a, "price").text = generate_random_price()

        # Spotify embed (if token available)
        if spotify_token:
            print("  -> Searching Spotify…")
            album_id = fetch_spotify_album_id(artist, title, spotify_token)
            if album_id:
                embed_url = f"https://open.spotify.com/embed/album/{album_id}?utm_source=generator"
                ET.SubElement(a, "spotify_embed").text = embed_url
                print(f"  -> Spotify album ID found: {album_id}")
            else:
                print("  -> No Spotify album found")
        else:
            print("  -> Skipping Spotify (no token)")

        print("  -> Added:", deezer_result["title"])

    # SAVE XML
    ET.indent(tree, space="  ", level=0)
    os.makedirs(os.path.dirname(XML_FILE), exist_ok=True)
    tree.write(XML_FILE, encoding="utf-8", xml_declaration=True)

    print("\n✓ records.xml updated successfully!")


if __name__ == "__main__":
    main()
