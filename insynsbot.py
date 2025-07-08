import requests
from bs4 import BeautifulSoup
import json
import os

# URL till FI:s insynstransaktioner för Qiiwi Games
url = "https://marknadssok.fi.se/Publiceringsklient/sv-SE/Search/Search?SearchFunctionType=Insyn&Utgivare=qiiwi+games&PersonILedandeSt%C3%A4llningNamn=&Transaktionsdatum.From=&Transaktionsdatum.To=&Publiceringsdatum.From=&Publiceringsdatum.To=&button=search&Page=1"

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; DiscordBot/1.0)"
}

# Hämta sidan
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# Hitta tabellen med transaktionerna
table = soup.find("table", class_="table")
if not table:
    print("Inga insynstransaktioner hittades.")
    exit()

rows = table.find_all("tr")[1:]  # Hoppa över rubrikerna

# Hämta senaste transaktionen
latest_trade = rows[0].find_all("td")
latest_trade_data = {
    "date": latest_trade[1].text.strip(),
    "person": latest_trade[2].text.strip(),
    "issuer": latest_trade[3].text.strip(),
    "function": latest_trade[4].text.strip(),
    "instrument": latest_trade[5].text.strip(),
    "transaction_type": latest_trade[6].text.strip(),
    "volume": latest_trade[7].text.strip()
}

# Fil där senaste transaktionen sparas
storage_file = "latest_trade.json"

# Läs senaste sparade transaktion (om den finns)
if os.path.exists(storage_file):
    with open(storage_file, "r") as f:
        saved_trade = json.load(f)
else:
    saved_trade = {}

# Jämför – om ny transaktion, skicka till Discord
if latest_trade_data != saved_trade:
    # Discord Embed
    payload = {
        "embeds": [
            {
                "title": "📢 Ny insynstransaktion i Qiiwi Games!",
                "description": f"**Datum:** {latest_trade_data['date']}\n"
                               f"**Person:** {latest_trade_data['person']}\n"
                               f"**Funktion:** {latest_trade_data['function']}\n"
                               f"**Instrument:** {latest_trade_data['instrument']}\n"
                               f"**Typ:** {latest_trade_data['transaction_type']}\n"
                               f"**Volym:** {latest_trade_data['volume']}",
                "url": url,
                "color": 0x00ff00
            }
        ]
    }

    # Din Discord webhook URL (byt ut nedan mot din riktiga URL)
    discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if discord_webhook_url:
        response = requests.post(discord_webhook_url, json=payload)
        if response.status_code == 204:
            print("Meddelande skickat till Discord!")
        else:
            print(f"Fel vid Discord-sändning: {response.status_code}")
    else:
        print("DISCORD_WEBHOOK_URL är inte satt!")

    # Spara nya transaktionen
    with open(storage_file, "w") as f:
        json.dump(latest_trade_data, f)
else:
    print("Ingen ny insynstransaktion.")
