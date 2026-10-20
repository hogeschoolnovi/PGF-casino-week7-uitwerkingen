# Fruitmachine voor Casino de Gouden Driehoek

from random import choice

from rich.console import Console
from rich.panel import Panel

from games.helpers import ask_for_bet

console = Console()
SYMBOLS = ["kers", "citroen", "ster", "meloen", "peer"]


def determine_rolls():
    """
    Determine three random fruit machine rolls.
    :return:
    """
    return choice(SYMBOLS), choice(SYMBOLS), choice(SYMBOLS)


def determine_payout(rol1, rol2, rol3, bet):
    """
    Determine the payout for the three fruit machine rolls.
    :param rol1:
    :param rol2:
    :param rol3:
    :param bet:
    :return:
    """
    if rol1 == rol2 == rol3:
        return bet * 3
    if rol1 == rol2 or rol1 == rol3 or rol2 == rol3:
        return bet
    return 0.0


def play_fruitmachine(balance):
    """
    Play one or more rounds of the fruit machine.
    :param balance:
    :return:
    """
    while True:
        console.print(
            Panel(
                f"Huidig saldo: [green]€ {balance:.2f}[/green]",
                title="Casino de Gouden Driehoek - fruitmachine",
            )
        )

        action = input("Druk op enter om te spelen of typ stop om terug te gaan: ").strip().lower()
        if action == "stop":
            return balance

        bet = ask_for_bet(balance)
        balance -= bet
        rol1, rol2, rol3 = determine_rolls()
        console.print(f"Rollen: [bold]{rol1} | {rol2} | {rol3}[/bold]")

        payout = determine_payout(rol1, rol2, rol3, bet)
        if payout > 0:
            balance += payout
            if rol1 == rol2 == rol3:
                print_text = f"[bold green]Drie dezelfde! Je wint € {payout:.2f}[/bold green]"
            else:
                print_text = f"[green]Twee dezelfde! Je wint € {payout:.2f}[/green]"
        else:
            print_text = f"[red]Geen match. Je verliest € {bet:.2f}[/red]"
        console.print(
            Panel(
                f"{print_text}\nNieuw saldo: [green]€ {balance:.2f}[/green]",
                title="Output"
            )
        )


