name: Insynsbot

on:
  workflow_dispatch:  # Manuell start via GitHub
  schedule:
    - cron: "0 * * * *"  # Kör varje timme (justera om du vill)

jobs:
  run:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          pip install requests beautifulsoup4

      - name: Download latest_trade.json artifact (om den finns)
        uses: actions/download-artifact@v4
        with:
          name: latest_trade
          path: ./
        continue-on-error: true  # Hoppa över fel om artifact saknas första gången

      - name: Run bot
        run: python insynsbot.py

      - name: Upload latest_trade.json artifact (för nästa körning)
        uses: actions/upload-artifact@v4
        with:
          name: latest_trade
          path: latest_trade.json
