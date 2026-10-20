import os
from dotenv import load_dotenv
import requests
from rich.console import Console
from rich.panel import Panel

load_dotenv()

console = Console()
API_KEY = os.getenv("API_KEY")
EXCHANGE_RATE_URL = "https://v6.exchangerate-api.com/v6/{}/latest/{}"    # API-endpoint voor valuta wisselkoers

def get_exchange_request():
    while True:
        currency = input("Welke valuta wilt u wisselen? Gebruik een ISO 4217-valutacode (bijv. USD): ").strip().upper()
        if currency == "STOP":
            return None, None
        if len(currency) == 3:
            break
        else:
            print("Deze valuta wordt niet geaccepteerd, probeer het opnieuw of type 'stop' om terug te keren naar het hoofdmenu")
    while True:
        try:
            amount = float(input("Vul het bedrag in dat u wilt wisselen: "))
            break
        except ValueError:
            print("Dit is geen geldige invoer, probeer het opnieuw.")
    return amount, currency

def get_exchange_rate_for_currency(currency):
    if not API_KEY:
        print("Fout: API_KEY ontbreekt. Voeg deze toe aan het .env-bestand.")
        return None

    try:
        response = requests.get(EXCHANGE_RATE_URL.format(API_KEY, currency))
    except requests.exceptions.ConnectionError:
        print("Fout: Geen verbinding met de API")
        return None

    if response.status_code == 200:
        data = response.json()

        if "EUR" in data["conversion_rates"]:
            return data["conversion_rates"]["EUR"]
        else:
            print(f"Fout: EUR wisselkoers voor {currency} niet gevonden.")
            return None
    else:
        print(f"Fout: {response.status_code} - {response.text}")
        return None

def convert_to_euro(foreign_currency_amount, exchange_rate):
    return foreign_currency_amount * exchange_rate

def print_exchange_result(foreign_currency_amount, currency, exchange_rate, euro_amount):
    console.print(
        Panel(
            f"Bedrag: [bold]{foreign_currency_amount:.2f} {currency}[/bold]\n"
            f"Koers naar euro: [cyan]{exchange_rate}[/cyan]\n"
            f"Euro's: [bold green]€ {euro_amount:.2f}[/bold green]",
            title="Casino de Gouden Driehoek - wisselkassa",
        )
    )


def run_exchange():
    foreign_currency_amount, currency = get_exchange_request()
    if foreign_currency_amount is None and currency is None:
        return None  # terug naar hoofdmenu

    exchange_rate = get_exchange_rate_for_currency(currency)
    if exchange_rate is None:
        console.print("[red]Kon de eurokoers niet ophalen. Probeer een andere valuta.[/red]")
        return None
    else:
        euro_amount = convert_to_euro(foreign_currency_amount, exchange_rate)
        print_exchange_result(foreign_currency_amount, currency, exchange_rate, euro_amount)
        return euro_amount
