#!/usr/bin/env python3

import folium
import requests

# 1. Skapa en grundkarta centrerad över Europa (eller vilken startpunkt du vill)
m = folium.Map(location=[55.6, 13.0], zoom_start=4)

# 2. Läs in IP-adresser från fil
# Skapa en fil som heter ips.txt med en IP-adress per rad
try:
    with open("ips.txt", "r") as file:
        ip_list = [line.strip() for line in file if line.strip()]
except FileNotFoundError:
    print("Hittade ingen 'ips.txt'-fil. Skapa en och lägg till IP-adresser.")
    ip_list = []

# 3. Gå igenom varje IP och hämta position
for ip in ip_list:
    try:
        # Använder ett gratis, öppet API för geolokalisering
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        data = response.json()

        if data["status"] == "success":
            lat = data["lat"]
            lon = data["lon"]
            country = data["country"]
            city = data["city"]

            # Lägg till en markör på kartan
            popup_text = f"IP: {ip}<br>Stad: {city}<br>Land: {country}"
            folium.Marker([lat, lon], popup=popup_text).add_to(m)
            print(f"Lade till {ip} ({city}, {country})")
        else:
            print(f"Kunde inte hitta position för IP: {ip}")
    except Exception as e:
        print(f"Ett fel uppstod för {ip}: {e}")

# 4. Spara kartan som en HTML-fil
m.save("ip_karta.html")
print("Kartan har sparats som 'ip_karta.html'! Öppna filen i din webbläsare.")
