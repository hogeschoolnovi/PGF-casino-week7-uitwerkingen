# Week 6 oplossing: Casino de Gouden Driehoek met Rich, random en datumverwerking

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from games.blackjack import play_blackjack
from games.fruitmachine import play_fruitmachine
from games.roulette import play_roulette
from profiles import (
    create_account,
    get_current_balance,
    initialize_player,
    register_played_game,
    remove_account,
    show_account,
    show_all_players,
    switch_account,
    update_current_balance,
)
from exchange import run_exchange

TICKET_PRICE = 10.00
CONSUMPTION_PRICE = 4.50
GAMBLING_TAX = 2.00
TOTAL_COST = TICKET_PRICE + CONSUMPTION_PRICE + GAMBLING_TAX

console = Console()


def show_main_menu():
    """
    Show the casino's main menu.
    :return:
    """
    table = Table(expand=True)
    table.add_column("Optie")
    table.add_column("Actie")
    table.add_row("1", "Spellen")
    table.add_row("2", "Saldo")
    table.add_row("3", "Account")
    table.add_row("4","Wisselkantoor")
    table.add_row("0", "Stop")
    console.print(
        Panel.fit(
            table,
            title="Casino de Gouden Driehoek - hoofdmenu"
        )
    )


def show_games_menu():
    """
    Show the game menu.
    :return:
    """
    table = Table(expand=True)
    table.add_column("Optie")
    table.add_column("Spel")
    table.add_row("1", "Fruitmachine")
    table.add_row("2", "Roulette")
    table.add_row("3", "Blackjack")
    table.add_row("0", "Terug")
    console.print(
        Panel.fit(
            table,
            title="Casino de Gouden Driehoek - spellen"
        )
    )


def show_account_menu():
    """
    Show the account menu.
    :return:
    """
    table = Table(expand=True)
    table.add_column("Optie")
    table.add_column("Actie")
    table.add_row("1", "Toon alle accounts")
    table.add_row("2", "Nieuw account")
    table.add_row("3", "Wissel account")
    table.add_row("4", "Verwijder account")
    table.add_row("0", "Terug")
    console.print(
        Panel.fit(
            table,
            title="Casino de Gouden Driehoek - accountmenu"
        )
    )


def show_balance(balance):
    """
    Show the player's current balance.
    :param balance:
    :return:
    """
    console.print(
        Panel(
            f"Huidig saldo: [bold green]€ {balance:.2f}[/bold green]",
            title="Casino de Gouden Driehoek - saldo",
        )
    )


def main():
    initialize_player(TOTAL_COST)

    while True:
        show_main_menu()
        choice = int(input("Kies een optie: "))

        match choice:
            case 0:  # stop
                break
            case 1:  # spellen
                show_games_menu()
                game_choice = int(input("Kies een spel: "))

                match game_choice:
                    case 0:  # terug
                        pass
                    case 1:  # fruitmachine
                        balance = play_fruitmachine(get_current_balance())
                        update_current_balance(balance)
                        register_played_game("fruitmachine")
                    case 2:  # roulette
                        balance = play_roulette(get_current_balance())
                        update_current_balance(balance)
                        register_played_game("roulette")
                    case 3:  # blackjack
                        balance = play_blackjack(get_current_balance())
                        update_current_balance(balance)
                        register_played_game("blackjack")
                    case _:  # ongeldig
                        console.print("[red]Ongeldige spelkeuze, probeer opnieuw.[/red]")
            case 2:  # saldo
                show_balance(get_current_balance())
            case 3:  # account
                show_account()
                show_account_menu()
                account_choice = int(input("Kies een accountoptie: "))

                match account_choice:
                    case 0:  # terug
                        pass
                    case 1:  # tonen
                        show_all_players()
                    case 2:  # nieuw
                        create_account(TOTAL_COST)
                    case 3:  # wisselen
                        switch_account()
                    case 4:  # verwijderen
                        remove_account()
                    case _:  # ongeldig
                        console.print("[red]Ongeldige accountkeuze.[/red]")
            case 4: # wisselkantoor
                euro_amount = run_exchange()
                if euro_amount is not None:
                    update_current_balance(get_current_balance() + euro_amount)
            case _:  # ongeldig
                console.print("[red]Ongeldige keuze, probeer opnieuw.[/red]")

    console.print(f"[bold]Eindsaldo: € {get_current_balance():.2f}[/bold]")


main()
