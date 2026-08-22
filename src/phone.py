
#!/usr/bin/env python3

import phonenumbers
from phonenumbers import carrier, geocoder, timezone


def search_number(phone_input: str, output_dest=None):
    try:
        phoneNumber = phonenumbers.parse(phone_input)

        if not phonenumbers.is_valid_number(phoneNumber):
            result = "Error: The entered phone number is not valid."
        else:
            timeZone = timezone.time_zones_for_number(phoneNumber)
            geolocation = geocoder.description_for_number(phoneNumber, "en")
            service_provider = carrier.name_for_number(phoneNumber, "en")

            result = (
                f"Timezone        : {', '.join(timeZone)}\n"
                f"Location        : {geolocation if geolocation else 'Unknown'}\n"
                f"Service Provider: {service_provider if service_provider else 'Unknown'}"
            )

    except phonenumbers.NumberParseException as e:
        result = f"Error parsing number: {e}"

    # Hantera Tkinter UI-komponenter
    if hasattr(output_dest, "config"):
        output_dest.config(text=result)
    # Hantera filutskrift
    elif isinstance(output_dest, str) and output_dest != "console":
        with open(output_dest, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"Resultatet har sparats i: {output_dest}")
    # Standard-fallback till konsol
    else:
        print(result)


if __name__ == "__main__":
    number = input("Enter phone number with country code (e.g., +14155552671): ")
    dest = input("Enter output destination (type 'console' or a filename like 'output.txt'): ")

    search_number(number, dest)
