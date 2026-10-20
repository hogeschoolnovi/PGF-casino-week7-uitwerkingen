# Week 7: Casino de Gouden Driehoek: Web-API requests

## Inleiding
Vorige week heb je een aantal externe libraries toegevoegd voor opmaak en specifieke functionaliteiten. Deze week ga je ook een ook een externe library toevoegen. Deze is specifiek voor het communiceren over HTTP. Je gaat namelijk een web-API gebruiken om een wisselkantoor te implementeren. Daarnaast ga je zorgen voor een veilige opslag van geheimen en een goede afhandeling van errors.

## Opdracht beschrijving

Breid je hoofdmenu uit met een vierde optie, namelijk een "wisselkantoor". De functionaliteiten van het wisselkantoor mag je in `exchange.py` schrijven. In `exchange.py` schrijf je meerdere functies, maar in `main.py` hoef je slechts één functie te importeren. Geef deze functie een logische naam, zoals `run_exchange`

In deze `run_exchange` functie, orkestreer je de wisselkantoor functionaliteit. Zorg dat je minstens de volgende functies in `exchange.py` hebt:
- De gebruiker vragen welke valuta deze wil wisselen en hoeveel geld.
- Ophalen van de actuele wisselkoers ten opzichte van de euro.
- Een functie om het bedrag om te rekenen naar euro's 
- Een functie om een mooie printout voor de gebruiker te maken.
- Een functie die alles orkestreert.

### Gegevens opvragen van de gebruiker
Je wilt van de gebruiker weten welke valuta deze wil wisselen. Zorg dat je valideert dat de input van de gebruiker overeenkomt met de [ISO 4217-valutacode](https://nl.iban.com/currency-codes). Dit kun je simpel en oppervlakkig doen door te checken of het 3 lang is, of je kunt een hele exacte check doen met een API of library. Als de gebruikersinput niet aan deze voorwaarde voldoet, vraag dan de gebruiker om het opnieuw te proberen. Geef de gebruiker ook de optie om "stop" in te vullen om terug te keren naar het hoofdmenu, voor het geval de gebruiker bitcoins wil wisselen, er achter komt dat dat niet kan en zich bedenkt.

Daarnaast wil je ook van de gebruiker weten hoeveel geld er gewisseld moet worden. Zorg dat je hier alleen een float als input accepteert. Als het geen float is, vraag je de gebruiker opnieuw.

### Wisselkoers ophalen

Voor het ophalen van de wisselkoers gebruik je https://www.exchangerate-api.com/. Als je hier nog geen (gratis) API sleutel voor hebt aangevraagd in de les, is het nu de tijd om dat te doen. Het is verstandig om dit te doen met je school e-amail adres.

Sla deze API sleutel veilig op in je applicatie op één van de drie manieren:
- Hardcoded in je code
- Als variabele in een apart python bestand
- In een .env bestand (de veiligste optie)

In de wisselkoers functie wil je ook controleren of deze API steutel aanwezig is of niet. Als dat niet zo is, kun je namelijk geen request versturen en moet je de gebruiker een foutmelding toenen.

Zoek vervolgens het juiste API endpoint om exchange rates op te vragen in de [documentatie](https://www.exchangerate-api.com/docs/overview) van de API. En lees ook hoe je het endpoint moet gebruiken, zoals welke URL-variabelen, parameters of headers je er bij kunt of moet meegeven.

Wanneer je het juiste endpoint gevonden hebt, schrijf je code om de juiste wisselkoers op te vragen van de vreemde valuta naar de euro. Zorg er hierbij voor dat je rekening houd met de juiste statuscode en zorg er ook voor dat je een eventuele "ConnectionError" netjes afhandeld.

### Convert to euro

Bedrag keer wisselkoers

### De print

Om de functionaliteit goed af te sluiten, wil je natuurlijk een mooie samenvatting aan de gebruiker tonen. Die dit in dezelfde Rich opmaak als we vorige week gebruikt hebben. Toon ten minste:
- Het originele bedrag en de originele valuta
- De actuele wisselkoers
- Het omgerekende bedrag in euros


## Output
Je kunt de output bijvoorbeeld zo opbouwen:

```text
┌─ Casino de Gouden Driehoek - hoofdmenu ─┐
│ ┌────────────┬────────────────────────┐ │
│ │ Optie      │ Actie                  │ │
│ ├────────────┼────────────────────────┤ │
│ │ 1          │ Spellen                │ │
│ │ 2          │ Saldo                  │ │
│ │ 3          │ Account                │ │
│ │ 4          │ Wisselkantoor          │ │
│ │ 0          │ Stop                   │ │
│ └────────────┴────────────────────────┘ │
└─────────────────────────────────────────┘
Kies een optie: 4
Welke valuta wilt u wisselen? Gebruik een ISO 4217-valutacode (bijv. USD): USD
Vul het bedrag in dat u wilt wisselen: 100
┌────────────────── Casino de Gouden Driehoek - wisselkassa ──────────────────┐
│ Bedrag: 100.00 USD                                                          │
│ Koers naar euro: 0.8952                                                     │
│ Euro's: € 89.52                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```


## Randvoorwaarden
- De gebruiker kan geld omwisselen van vreemde valutas naar euros.
- Het gewisselde bedrag word bij het **saldo** van de gebruiker opgeteld.
- Je gebruikt de requests library om de exchangerate api aan te spreken.
- Je hebt een `exchange.py` voor alle wisselkantoor functionaliteiten.



## Stappenplan
1. Neem de bestaande structuur van week 6 over, zodat alle bestanden blijven bestaan.
2. Maak een `exchange.py` in je root folder.
3. Zet hier de volgende functies in:
   -  get_exchange_request()
   - get_exchange_rate_for_currency(currency)
   - convert_to_euro(foreign_currency_amount, exchange_rate)
   - print_exchange_result(foreign_currency_amount, currency, exchange_rate, euro_amount)
   - run_exchange()
4. Voeg een vierde optie voor "wisselkantoor" toe aan de functie `main.py/show_main_menu`
5. In de main functie van `main.py` voeg je een `case 4` toe aan het match statement.
6. In deze case roep je `run_exchange` aan. Deze functie retourneert het euro bedrag, sla dat op in een variabele.
7. Vervolgens check je of dit euro bedrag niet `None` is en tel het dan op bij het saldo van de gebruiker met de `update_current_balance` functie.
8. In de `run_exchange` functie roep je als eerst `get_exchange_request()` aan. Deze functie vraagt de valuta en het bedrag van de gebruiker en retourneert daarom ook twee waardes. Sla deze waardes op als `foreign_currency_amount`en `currency`.
9. In de `get_exchange_request` functie heb je twee `while True` loops.
   - De eerste loop gebruikt `input` om de gebruiker te vragen welke valute deze wil wisselen. Normaliseer deze input met `strip` en `upper`. Check of de gegeven input "STOP" is, als dat zo is dan mag je returnen met `None, None`. Check daarna of de input wel goed gevormd is (len(currency == 3) of gebruik een library), als dat goed is, dan mag je `break` doen, maar als het niet goed is, moet je de gebruiker opnieuw bevragen.
   - De tweede loop vraagt de gebruiker om het bedrag dat deze wil wisselen. Zorg dat je deze input omzet naar een float, door de input in `float()` te wikkelen en `break` als dat goed gaat. Zet de input ook in een `try` statement en maak een `except` voor een `ValueError` waarin je een error message print en daarna de gebruiker opnieuw bevraagd.
10. In de `run_exchange` functie check je vervolgens of de `foreign_currency_amount`en `currency` allebij niet None zijn. Als dat wel zo is, dan mag je terug gaan naar het hoofdmenu.
11. Vervolgens roep je de `get_exchange_rate_for_currency` functie aan en sla je de uitkomst op als `exchange_rate`
12. Voor deze functie heb je een API_KEY nodig. Sla deze op in een .env bestand en laad het in met `load_dotenv()`. Vervolgens kun je de API_KEY waarde uit je omgeving halen met `os.getenv()`.
13. Sla de juiste url () op in een constante `EXCHANGE_RATE_URL`. Plak daar API_KEY en de vreemde valuta in op de juiste plek. Dit doe je door `{}` op de plek te zetten waar je een variabele wil. Je maakt er dan geen f-string van, maar je roept `EXCHANGE_RATE_URL.format(API_KEY, currency)`aan. Met deze ge-formatte url maak je vervolgens een get request.
14. Zet het get request in een `try` statement en vang in de `except` een `connectionerror` op. Print een bericht dat de API onbereikbaar is als deze error plaats vind en return `None`
15. Als alles wel goed is gegaan, dan kun je controleren of je een 200 status terug hebt gekregen. Zo niet, dan print je weer een error message en return je `None`.
16. Als je wel een 200 status hebt, dan kun je de json er uit halen. Vervolgens de "conversion rates" uit die json halen en dan de "EUR" waarde uit de conversion rates. Return de waarde die je hier vind, dat is de exchange rate.
17. In `run_exchange` kun je nu checken of de `exchange_rate` die je hebt teruggekregen niet `None` is. Als dat wel zo is, dan print je een error message voor de gebruiker dat de exchange rate niet gevonden kon worden en return je `None` zodat de gebruiker weer teruggestuurd wordt naar het hoofdmenu. Als de `exchange_rate` niet `None` is, dan is alles dus geod gegaan en kun je verder.
18. Gebruik de `convert_to_euro` functie om het initiele bedrag om te rekenen naar euros. Dit is simpelweg `foreign_currency_amount * exchange_rate`
19. Gebruik daarna de `print_exchange_result` functie om alles in een mooie print te zetten. Deze functie ontvangt alle variabelen die je in `run_exchange` hebt gemaakt als parameter, dus `foreign_currency_amount`, `currency`, `exchange_rate` en `euro_amount`. Zorg dat je hier netjes Console en Panel gebruikt, zoals je dat in de vorige huiswerkopdracht hebt gedaan. Schroom ook niet om wat kleur en opmaak toe te voegen aan de printout.
20. Als laatste is het belangrijk om je `.gitignore` en je `requirements.txt` te updaten.
