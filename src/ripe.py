
import json
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import requests


def query_ripe(ip_address, result_label):
  # Rensa bort eventuella mellanslag
  ip_address = ip_address.strip()

  if not ip_address:
    messagebox.showerror("Fel", "Var god ange en IP-adress.")
    return

  try:
    # 1. Hämta nätverksinfo / AS
    ipinfo = requests.get(
        f"https://stat.ripe.net/data/network-info/data.json?resource={ip_address}"
    )
    ipinfo_data = json.loads(ipinfo.text)

    if not ipinfo_data["data"]["asns"]:
      as_text = "None"
      asinfo_result = "No AS information found"
    else:
      as_number = ipinfo_data["data"]["asns"]
      as_text = "".join(as_number)

      asinfo = requests.get(
          f"https://stat.ripe.net/data/as-overview/data.json?resource=AS{as_text}"
      )
      asinfo_data = json.loads(asinfo.text)
      asinfo_result = asinfo_data["data"]["holder"]

    # 2. Hämta Reverse DNS
    rev_dns = requests.get(
        f"https://stat.ripe.net/data/reverse-dns-ip/data.json?resource={ip_address}"
    )
    rev_dns_data = json.loads(rev_dns.text)
    rev_dns_result = rev_dns_data["data"]["result"]

    if rev_dns_result is None:
      rev_dns_record = "No reverse record found"
    else:
      rev_dns_record = "".join(rev_dns_result)

    # 3. Hämta Geolocation
    geoloc = requests.get(
        f"https://stat.ripe.net/data/geoloc/data.json?resource={ip_address}"
    )
    geoloc_data = json.loads(geoloc.text)
    location = geoloc_data["data"]["located_resources"]
    if location:
      location_data = dict(location[0])
      locations = location_data["locations"]
      country = locations[0]["country"] if locations else "Unknown"
    else:
      country = "Unknown"

    # Formatera resultatet
    result_text = f"""Resultat för IP: {ip_address}
CIDR: {ipinfo_data['data']['prefix']}
AS: {as_text}
Ägare: {asinfo_result}
Rev DNS: {rev_dns_record}
Land: {country}"""

    # Uppdatera gränssnittet med resultatet
    result_label.config(text=result_text)

  except Exception as e:
    messagebox.showerror("Ett fel uppstod", str(e))
