# Helperfuncties voor spelersprofielen in Casino de Gouden Driehoek

from datetime import date, datetime

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

MIN_AGE = 18

players = {}
current_player = None
console = Console()


# ================
# Getters/updaters
# ================

def get_current_profile():
    """
    Return the profile of the current player.
    :return:
    """
    return players[current_player]


def get_current_balance():
    """
    Return the balance of the current player.
    :return:
    """
    return get_current_profile()["saldo"]


def update_current_balance(balance):
    """
    Update the balance of the current player.
    :param balance:
    :return:
    """
    get_current_profile()["saldo"] = balance



#================
# Helper functies (en de oude functies)
#================

def register_played_game(game_name):
    """
    Register a played game and increase its play count.
    :param game_name:
    :return:
    """
    played_games = get_current_profile()["gespeelde_spellen"]
    if game_name in played_games:
        played_games[game_name] += 1
    else:
        played_games[game_name] = 1


def determine_salutation(name, gender):
    """
    Determine the player's form of address.
    :param name:
    :param gender:
    :return:
    """
    if gender == "m":
        return f"meneer {name}"
    elif gender == "v":
        return f"mevrouw {name}"
    else:
        return f"speler {name}"


def calculate_age(birthdate):
    """
    Calculate someone's age based on their birthdate.
    :param birthdate:
    :return:
    """

    birthdate_value = datetime.strptime(birthdate, "%d-%m-%Y").date()
    today_value = date.today()

    if birthdate_value > today_value:
        raise ValueError("De geboortedatum kan niet in de toekomst liggen.")

    age = today_value.year - birthdate_value.year

    # Verjaardag is dit jaar nog niet geweest
    if (today_value.month, today_value.day) < (birthdate_value.month, birthdate_value.day):
        age -= 1

    return age


def check_age(birthdate):
    """
    Check whether the player is at least 18 years old.
    :param birthdate:
    :return:
    """
    age = calculate_age(birthdate)
    if age < MIN_AGE:
        console.print("[red]Sorry, je moet 18 jaar of ouder zijn om deze applicatie te gebruiken.[/red]")
        exit(1)
    return birthdate


# =================
# Accountcreatie
# =================

def create_profile(name, birthdate, gender, balance):
    """
    Create a player profile as a dictionary.
    :param name:
    :param birthdate:
    :param gender:
    :param balance:
    :return:
    """
    return {
        "naam": name,
        "geboortedatum": birthdate,
        "gender": gender,
        "saldo": balance,
        "gespeelde_spellen": {},
    }


def create_start_players():
    """
    Create the initial collection of player profiles.
    :return:
    """
    return {
        "Banaan": create_profile("Banaan", "14-02-1998", "v", 50.0),
        "Appel": create_profile("Appel", "03-08-1997", "m", 30.0),
        "Kiwi": create_profile("Kiwi", "22-11-1999", "v", 40.0),
    }


def create_account(total_cost, name=None):
    """
    Create a new player account.
    :param total_cost:
    :param name:
    :return:
    """
    global current_player

    if name is None:
        name = input("Naam voor het nieuwe account: ").capitalize()
        if name in players:
            console.print("[red]Dit account bestaat al. Gebruik wissel account om het te openen.[/red]")
            return

    birthdate = check_age(input("Wat is je geboortedatum? (dd-mm-yyyy) "))
    gender = input("Wat is je gender? (m/v/x) ").strip().lower()
    start_balance = float(input("Met hoeveel geld begin je in Casino de Gouden Driehoek? € "))
    balance = start_balance - total_cost
    players[name] = create_profile(name, birthdate, gender, balance)
    current_player = name


def initialize_player(total_cost):
    """
    Initialize the player collection, select an account and show the welcome message.
    :param total_cost:
    :return:
    """
    global players
    global current_player

    players = create_start_players()
    name = input("Wat is je naam? ").capitalize()
    current_player = name

    if name in players:
        profile = players[current_player]
        salutation = determine_salutation(current_player, profile["gender"])
        console.print(
            Panel(
                f"Welkom terug, [bold]{salutation}[/bold]\n"
                f"Saldo: [green]€ {profile['saldo']:.2f}[/green]",
                title="Casino de Gouden Driehoek",
            )
        )
    else:
        create_account(total_cost, name)

        profile = players[current_player]
        balance = profile["saldo"]
        start_balance = balance + total_cost
        salutation = determine_salutation(current_player, profile["gender"])
        has_budget = total_cost <= start_balance
        conclusion = "Je hebt nog genoeg budget voor toegang tot het casino." \
            if has_budget \
            else "Je hebt niet voldoende budget voor toegang tot het casino."
        console.print(
            Panel(
                f"Welkom, [bold]{salutation}[/bold]\n\n"
                f"Startbudget: € {start_balance:.2f}\n"
                f"Vaste kosten: € {total_cost:.2f}\n"
                f"Saldo: [green]€ {balance:.2f}[/green]\n\n"
                f"{conclusion}",
                title="Casino de Gouden Driehoek",
            )
        )


def switch_account():
    """
    Select an existing account from the player collection.
    :return:
    """
    global current_player

    name = input("Welk account wil je gebruiken? ").capitalize()
    if name in players:
        current_player = name
        return True

    console.print("[red]Dat account bestaat niet.[/red]")
    return False


def show_account():
    """
    Show the current player statistics.
    :return:
    """
    profile = get_current_profile()
    console.print(
        Panel.fit(
            f"Huidige speler: [bold]{current_player}[/bold]\n"
            f"Saldo: [green]€ {profile['saldo']:.2f}[/green]\n"
            f"Gespeelde spellen: {profile['gespeelde_spellen']}\n"
            f"Beschikbare spelers: {list(players.keys())}",
            title="Casino de Gouden Driehoek - account",
        )
    )


def remove_account():
    """
    Remove a player profile when it exists.
    :return:
    """
    global current_player

    player_to_remove = input("Welke speler wil je verwijderen? ").capitalize()

    if player_to_remove in players:
        if len(players) == 1:
            console.print("[red]Het laatste account kan niet worden verwijderd.[/red]")
            return False
        del players[player_to_remove]
        if current_player == player_to_remove:
            current_player = list(players.keys())[0]
        return True

    console.print("[red]Dat account bestaat niet.[/red]")
    return False


def show_all_players():
    """
    Show all available player profiles.
    :return:
    """
    table = Table(expand=True)
    table.add_column("Naam")
    table.add_column("Saldo")
    for name, profile in players.items():
        table.add_row(name, f"€ {profile['saldo']:.2f}")
    console.print(
        Panel.fit(
            table,
            title="Overzicht spelers",
        )
    )
