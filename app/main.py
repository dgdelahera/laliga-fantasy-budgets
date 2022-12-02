import requests

from app.auth import get_token
from tabulate import tabulate

USERNAME = "your_username"
PASSWORD = "your_password"
USE_TOKEN = False
TOKEN = ""
LEAGUE_ID = "1234"


class Player:
    def __init__(self, name: str, team_value: int):
        self.name = name
        self.budget = 100000000 # 100M
        self.team_value = team_value

    def sell(self,amount: int):
        self.budget += amount

    def buy(self, amount: int):
        self.budget -= amount

    def get_budget(self):
        return self.budget

    def get_total_value(self):
        return self.budget + self.team_value


def print_players_value(players):
    print_result = []
    for player in players:
        print_result.append([player.name, player.get_budget(), player.get_total_value()])
    print_result = sorted(print_result, key=lambda k: float(k[2]), reverse=True)
    for element in print_result:
        element[1] = f'{element[1]:,}€'
        element[2] = f'{element[2]:,}€'
    print(tabulate(print_result, headers=['Player', 'Budget', 'Total Value'], tablefmt='orgtbl'))


def get_players(token):
    url = f"https://api.laligafantasymarca.com/api/v4/leagues/{LEAGUE_ID}/ranking?x-lang=es"
    data = requests.get(url,headers={'authorization': token}).json()
    players = []
    for team in data:
        players.append(Player(name=team['team']['manager']['managerName'], team_value=team['team']['teamValue']))
    return players


def update_players_budget(players, player_sell, player_buy, amount):
    if player_sell != "LaLiga":
        found = False
        for player in players:
            if player.name == player_sell:
                player.sell(amount)
                found = True
        if not found:
            print(f"Player not found: {player_sell}")
    if player_buy != "LaLiga":
        found = False
        for player in players:
            if player.name == player_buy:
                player.buy(amount)
                found = True
        if not found:
            print(f"Player not found: {player_buy}")


def check_players_operations(players, token):
    i = 1
    operaciones = []
    while True:
        data = requests.get(f"https://api.laligafantasymarca.com/api/v3/leagues/012408899/news/{i}?x-lang=es", headers={'authorization':token}).json()
        if not data:
            break
        operaciones = operaciones + data
        i += 1
    print(f"Updating {len(operaciones)} operations")
    for operacion in operaciones:
        if operacion['title'] == 'Operación de mercado':
            operacion_title = operacion['msg']
            if "ha vendido" in operacion_title:
                player_sell = operacion_title.split("ha vendido")[0].strip()
                player_buy = operacion_title.split("por")[0].rstrip().split(" ")[-1].strip()
                amount = operacion_title.split("por")[1]
            elif "ha comprado" in operacion_title:
                player_buy = operacion_title.split("ha comprado")[0].strip()
                player_sell = operacion_title.split("por")[0].rstrip().split(" ")[-1].strip()
                amount = operacion_title.split("por")[1]
            else:
                print(f"Bad operation: {operacion_title}")
                continue
            amount = int(amount.replace("€","").replace(".",""))
            update_players_budget(players, player_sell, player_buy, amount)


def main():
    if USE_TOKEN:
        token = TOKEN
    else:
        token = get_token()
    players = get_players(token)
    check_players_operations(players, token)
    print_players_value(players)


if __name__ == '__main__':
    main()


