# Algemene hulpfuncties voor Casino de Gouden Driehoek

from rich.console import Console

console = Console()


def ask_for_bet(balance):
    """
    Ask the player for a valid bet.
    :param balance:
    :return:
    """
    while True:
        bet = float(input("Je inzet: € "))
        if bet <= 0:
            console.print("[red]De inzet moet groter zijn dan 0.[/red]")
            continue
        if bet > balance:
            console.print("[red]Je hebt niet genoeg saldo voor deze inzet.[/red]")
            continue
        return bet
