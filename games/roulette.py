# Roulette voor Casino de Gouden Driehoek

from random import randint

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from games.helpers import ask_for_bet

console = Console()


def show_roulette_options():
    """
    Show the options for the roulette table.
    :return:
    """
    table = Table(expand=True)
    table.add_column("Optie")
    table.add_column("Inzet")
    table.add_row("1", "Rood")
    table.add_row("2", "Zwart")
    table.add_row("3", "Even")
    table.add_row("4", "Oneven")
    table.add_row("0", "Stop")
    console.print(
        Panel.fit(
            table,
            title="Casino de Gouden Driehoek - roulette"
        )
    )


def determine_win(choice, color, odd_even):
    """
    Determine whether the player has won the roulette round.
    :param choice:
    :param color:
    :param odd_even:
    :return:
    """
    win = False
    if choice == 1 and color == "rood":
        win = True
    elif choice == 2 and color == "zwart":
        win = True
    elif choice == 3 and odd_even == "even":
        win = True
    elif choice == 4 and odd_even == "oneven":
        win = True
    return win


def play_roulette(balance):
    """
    Play multiple rounds of roulette.
    :param balance:
    :return:
    """
    while True:
        show_roulette_options()
        choice = int(input("Kies je gok (0 om te stoppen): "))

        if choice == 0:
            break

        if choice < 1 or choice > 4:
            console.print("[red]Ongeldige keuze, probeer opnieuw.[/red]")
            continue

        bet = ask_for_bet(balance)
        balance -= bet

        spin = randint(0, 36)
        if spin == 0:
            color = "groen"
            odd_even = "geen"
        elif spin <= 18:
            if spin % 2 == 0:
                color = "zwart"
                odd_even = "even"
            else:
                color = "rood"
                odd_even = "oneven"
        else:
            if spin % 2 == 0:
                color = "rood"
                odd_even = "even"
            else:
                color = "zwart"
                odd_even = "oneven"
        win = determine_win(choice, color, odd_even)

        if win:
            balance += bet * 2
            result = f"[green]Je wint € {bet:.2f}[/green]"
        else:
            result = f"[red]Je verliest € {bet:.2f}[/red]"

        console.print(
            Panel(
                f"De bal valt op [bold]{color} ({spin})[/bold].\n"
                f"{result}\n"
                f"Nieuw saldo: [green]€ {balance:.2f}[/green]",
                title="Output",
            )
        )

    return balance

