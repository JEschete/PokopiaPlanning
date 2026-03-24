import csv
import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

# Configuration
BASE_URL = "https://www.serebii.net"
_DIR = Path(__file__).parent
URLS_FILE = _DIR / "pokopia_urls.txt"
OUTPUT_FILE = _DIR / "Pokopia.csv"
MAX_HABITATS = 3  # colspan="3" in the HTML suggests up to 3
LOCATIONS = [
    "Withered Wastelands",
    "Bleak Beach",
    "Rocky Ridges",
    "Sparkling Skylands",
    "Palette Town",
]

# Primary location mapping (from community research)
PRIMARY_LOCATION = {}
_loc_data = {
    "Withered Wastelands": [
        "Bulbasaur","Charmander","Squirtle","Oddish","Charizard","Scyther","Pinsir",
        "Bellsprout","Heracross","Timburr","Gurdurr","Sliggoo","Blastoise","Wartortle",
        "Slowpoke","Slowbro","Slowking","Pidgey","Pidgeotto","Hoothoot","Noctowl",
        "Venonat","Venomoth","Combee","Magby","Goomy","Cacturne","Vikavolt","Volbeat",
        "Illumise","Vespiquen","Ivysaur","Venusaur","Paras","Parasect","Cubone",
        "Marowak","Drilbur","Excadrill","Pichu","Drifloon","Charmeleon","Tyrogue",
        "Gulpin","Weepinbell","Victreebel","Hitmonchan","Hitmonlee","Hitmontop",
        "Shellos","Shellos East Sea","Axew","Fraxure","Haxorus","Litwick","Lampent",
        "Chandelure","Vileplume","Bellossom","Onix","Magnemite","Pidgeot","Cacnea",
        "Tangrowth","Goodra","Magikarp","Gastrodon","Gastrodon East Sea",
    ],
    "Bleak Beach": [
        "Spinarak","Grubbin","Ariados","Zubat","Golbat","Makuhita","Hariyama",
        "Wingull","Pelipper","Crobat","Wooper","Paldean Wooper","Clodsire","Mareep",
        "Pawmi","Zorua","Zoroark","Gloom","Exeggcute","Exeggutor","Lapras","Meowth",
        "Growlithe","Azurill","Trubbish","Garbodor","Magneton","Electabuzz","Magnezone",
        "Voltorb","Electrode","Pawmo","Empoleon","Torchic","Blaziken","Pawmot",
        "Tatsugiri","Tatsugiri Curly Form","Tatsugiri Droopy Form",
        "Tatsugiri Stretchy Form","Electivire","Haunter","Gengar","Flaaffy","Minccino",
        "Cinccino","Psyduck","Golduck","Combusken","Farfetch'd","Chansey","Peakychu",
        "Happiny","Charjabug","Elekid","Prinplup","Piplup","Marill","Azumarill",
        "Gastly","Audino","Smeargle","Mosslax","Mimikyu","Blissey","Absol","Ampharos",
        "Grimer","Muk",
    ],
    "Rocky Ridges": [
        "Scorbunny","Riolu","Cinderace","Kricketot","Diglett","Dugtrio","Bonsly",
        "Sudowoodo","Dartrix","Decidueye","Lotad","Lombre","Murkrow","Honchkrow",
        "Chatot","Machoke","Machamp","Cleffa","Fidough","Clefairy","Clefable",
        "Larvesta","Volcarona","Ekans","Arbok","Politoed","Igglybuff","Jigglypuff",
        "Tyranitar","Ludicolo","Larvitar","Graveler","Golem","Torkoal","Raboot",
        "Charcadet","Magmar","Steelix","Glimmet","Glimmora","Swalot","Dachsbun",
        "Magmortar","Toxel","Wigglytuff","Lucario","Kricketune","Stereo Rotom",
        "Gimmighoul","Arcanine","Carkol","Rolycoly","Coalossal","Greedent","Gholdengo",
        "Toxtricity Amped Form","Toxtricity Low Key Form","Ceruledge","Armarouge",
        "Aerodactyl","Cranidos","Rampardos","Shieldon","Bastiodon","Tyrunt",
        "Tyrantrum","Amaura","Aurorus",
    ],
    "Sparkling Skylands": [
        "Trapinch","Duskull","Vibrava","Swablu","Flygon","Sprigatito","Dreepy",
        "Pupitar","Drakloak","Froakie","Frogadier","Greninja","Corvisquire",
        "Kilowattrel","Wattrel","Corviknight","Cyndaquil","Quilava","Vulpix",
        "Rookidee","Misdreavus","Mismagius","Girafarig","Servine","Farigiraf",
        "Serperior","Dratini","Poliwhirl","Dragonair","Dragonite","Gyarados","Altaria",
        "Beldum","Typhlosion","Abra","Alakazam","Kadabra","Dusclops","Dusknoir",
        "Tinkaton","Floragato","Poliwrath","Mime Jr.","Mr. Mime","Ralts","Kirlia",
        "Noibat","Noivern","Poliwag","Gardevoir","Porygon-Z","Snivy","Porygon2",
        "Dragapult","Metang","Porygon","Meowscarada","Plusle","Minun","Dedenne",
        "Raichu","Conkeldurr","Gallade","Persian","Ninetales","Drifblim","Metagross",
    ],
    "Palette Town": [
        "Geodude","Scizor","Skwovet","Machop","Cramorant","Eevee","Rowlet","Pikachu",
        "Tinkatink","Tinkatuff","Munchlax","Snorlax","Weezing","Tangela","Koffing",
        "Mawile","Vaporeon","Jolteon","Flareon","Espeon","Umbreon","Leafeon","Glaceon",
        "Sylveon",
    ],
    "Dream Island": [
        "Articuno","Moltres","Zapdos","Entei","Raikou","Suicune","Ho-Oh","Lugia",
        "Kyogre","Mew","Mewtwo","Volcanion","Ditto","Professor Tangrowth",
    ],
}
for _loc, _names in _loc_data.items():
    for _name in _names:
        PRIMARY_LOCATION[_name] = _loc

# CSV column order
CSV_HEADERS = [
    "Number",
    "Name",
    "Primary Location",
    "Specialty 1",
    "Specialty 2",
    "Ideal Habitat",
    "Favorite 1",
    "Favorite 2",
    "Favorite 3",
    "Favorite 4",
    "Favorite 5",
    "Favorite 6",
]
# Dynamically add habitat columns (up to MAX_HABITATS)
for i in range(1, MAX_HABITATS + 1):
    CSV_HEADERS.append(f"Habitat {i}")
    for loc in LOCATIONS:
        CSV_HEADERS.append(f"Habitat {i} {loc}")
    CSV_HEADERS.extend([
        f"Habitat {i} Rarity",
        f"Habitat {i} Time",
        f"Habitat {i} Weather",
    ])


def get_soup(url):
    """Fetches a URL and returns a BeautifulSoup object."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def scrape_pokemon(url):
    """Scrapes all relevant data from a single Pokemon page."""
    soup = get_soup(url)

    row = {h: "" for h in CSV_HEADERS}

    # --- Number & Name from <h1> e.g. "#001 Bulbasaur" ---
    h1 = soup.find("h1")
    if not h1:
        print(f"  WARNING: No <h1> found on {url}")
        return None

    parts = h1.text.strip().split(" ", 1)
    row["Number"] = parts[0]
    row["Name"] = parts[1] if len(parts) > 1 else ""
    row["Primary Location"] = PRIMARY_LOCATION.get(row["Name"], "")

    # --- Stats table: Specialty, Ideal Habitat, Favorites ---
    stats_header = soup.find("h2", string="Stats")
    if stats_header:
        stats_table = stats_header.find_parent("table")
        if stats_table:
            # Find the header row with "Specialty"
            spec_td = stats_table.find("td", string=lambda x: x and "Specialty" in x)
            if spec_td:
                header_row = spec_td.find_parent("tr")
                data_row = header_row.find_next_sibling("tr")
                if data_row:
                    cols = data_row.find_all("td", recursive=False)

                    # Specialty (col 0) — extract link text(s)
                    if len(cols) >= 1:
                        spec_links = cols[0].find_all("u")
                        for j, link in enumerate(spec_links[:2]):
                            row[f"Specialty {j + 1}"] = link.text.strip()

                    # Ideal Habitat (col 1)
                    if len(cols) >= 2:
                        u_tag = cols[1].find("u")
                        if u_tag:
                            row["Ideal Habitat"] = u_tag.text.strip()
                        else:
                            row["Ideal Habitat"] = cols[1].get_text(strip=True)

                    # Favorites (col 2) — separated by <br />
                    if len(cols) >= 3:
                        favs = [s.strip() for s in cols[2].stripped_strings]
                        for j, fav in enumerate(favs[:6]):
                            row[f"Favorite {j + 1}"] = fav

    # --- Habitats & Locations table ---
    hab_header = soup.find("h2", string=lambda t: t and "Habitats" in t)
    if hab_header:
        hab_table = hab_header.find_parent("table")
        if hab_table:
            all_rows = hab_table.find_all("tr")

            # Row structure (after the header row):
            #   Row 0: habitat names (fooevo cells with links)
            #   Row 1: habitat images
            #   Row 2: locations per habitat
            #   Row 3: rarity per habitat
            #   Row 4: time/weather per habitat
            # We skip the first row (the h2 header row)
            data_rows = [r for r in all_rows if not r.find("h2")]

            # Find habitat name row — cells with class "fooevo" containing <a> to habitatdex
            habitat_names = []
            name_row_idx = None
            for idx, tr in enumerate(data_rows):
                fooevo_cells = tr.find_all("td", class_="fooevo")
                if fooevo_cells and any(
                    c.find("a", href=lambda h: h and "habitatdex" in h)
                    for c in fooevo_cells
                ):
                    for cell in fooevo_cells:
                        a = cell.find("a")
                        habitat_names.append(a.text.strip() if a else cell.get_text(strip=True))
                    name_row_idx = idx
                    break

            num_habitats = len(habitat_names)
            for j, name in enumerate(habitat_names):
                row[f"Habitat {j + 1}"] = name

            # Now parse the remaining rows after the name row
            # We look for cells with class "fooinfo" which contain Location, Rarity, Time/Weather
            if name_row_idx is not None:
                remaining = data_rows[name_row_idx + 1:]

                # Collect all fooinfo rows (skip image row which uses class "cen")
                location_cells = []
                rarity_cells = []
                time_weather_cells = []

                for tr in remaining:
                    info_cells = tr.find_all("td", class_="fooinfo")
                    if not info_cells:
                        continue

                    # Determine what type of data by checking content
                    first_text = info_cells[0].get_text()
                    if "Location" in first_text:
                        location_cells = info_cells
                    elif "Rarity" in first_text:
                        rarity_cells = info_cells
                    elif info_cells[0].find("table"):
                        # Time/Weather is in a nested table
                        time_weather_cells = info_cells

                # Parse locations as Yes/No per known location
                for j, cell in enumerate(location_cells[:num_habitats]):
                    loc_links = cell.find_all("a")
                    found_locations = {a.text.strip() for a in loc_links}
                    for loc in LOCATIONS:
                        row[f"Habitat {j + 1} {loc}"] = (
                            "Yes" if loc in found_locations else "No"
                        )

                # Parse rarity
                for j, cell in enumerate(rarity_cells[:num_habitats]):
                    text = cell.get_text()
                    # Extract just the rarity value after "Rarity:"
                    match = re.search(r"Rarity\s*:\s*(.+)", text, re.DOTALL)
                    if match:
                        row[f"Habitat {j + 1} Rarity"] = match.group(1).strip()

                # Parse time/weather
                for j, cell in enumerate(time_weather_cells[:num_habitats]):
                    inner_table = cell.find("table")
                    if not inner_table:
                        continue
                    inner_cells = inner_table.find_all("td", attrs={"valign": "top"})
                    if len(inner_cells) >= 2:
                        times = [s.strip() for s in inner_cells[0].stripped_strings if s.strip()]
                        weathers = [s.strip() for s in inner_cells[1].stripped_strings if s.strip()]
                        row[f"Habitat {j + 1} Time"] = ", ".join(times)
                        row[f"Habitat {j + 1} Weather"] = ", ".join(weathers)

    return row


def main():
    # Load URLs
    with open(URLS_FILE, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    print(f"Loaded {len(urls)} URLs from {URLS_FILE}")

    with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        writer.writeheader()

        for i, url in enumerate(urls, 1):
            print(f"[{i}/{len(urls)}] {url}")
            try:
                data = scrape_pokemon(url)
                if data:
                    writer.writerow(data)
                    f.flush()
                else:
                    print("  SKIPPED (no data)")
            except Exception as e:
                print(f"  ERROR: {e}")

            time.sleep(0.5)

    print(f"\nDone! Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
