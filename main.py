import requests

from tabulate import tabulate

TOKEN = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IkNBdXdPcWRMN2YyXzlhTVhZX3ZkbEcyVENXbVV4aklXV1MwNVB4WHljcUkifQ.eyJpc3MiOiJodHRwczovL2xvZ2luLmxhbGlnYS5lcy8zMzUzMTZlYi1mNjA2LTQzNjEtYmI4Ni0zNWE3ZWRjZGNlYzEvdjIuMC8iLCJleHAiOjE2NjkxMDc1NTIsIm5iZiI6MTY2OTAyMTE1MiwiYXVkIjoiZmVjOWUzZmQtOGY4OC00NWFiLThjYmQtYjcwYjlkNjVkZGUwIiwiZW1haWwiOiJ0aGVmMWRhbmlAZ21haWwuY29tIiwiZ2l2ZW5fbmFtZSI6IkRhbmkiLCJmYW1pbHlfbmFtZSI6IkdvbnphbGV6IiwibmFtZSI6Ikdvb2dsZSB1c2VyIiwiaWRwIjoiZ29vZ2xlLmNvbSIsInN1YiI6IjRiOWZlNTA1LTZmOTItNGI4MS05NDQ5LTI0ZWU4NjE0ZDMzOCIsImV4dGVuc2lvbl9FbWFpbFZlcmlmaWVkIjp0cnVlLCJleHRlbnNpb25fVXNlclByb2ZpbGVJZCI6ImJjMGVmMjI3LTVkNTYtNDRmZS1hNTIwLTY3YWU5YWJlMTZlNCIsIm9pZCI6ImJjMGVmMjI3LTVkNTYtNDRmZS1hNTIwLTY3YWU5YWJlMTZlNCIsImF6cCI6ImZlYzllM2ZkLThmODgtNDVhYi04Y2JkLWI3MGI5ZDY1ZGRlMCIsInZlciI6IjEuMCIsImlhdCI6MTY2OTAyMTE1Mn0.lH9fQZG4GPm5Afm9tmlV1Sa4cfrfZ6uylX7iDU1PLSOS1dl3N07YoZK3q7OGv_nnQ7ak5BBy9gHK9HCoBTpPY8mdPsYKLjK3AvEot-yYJvSXofEIC5KnL6aVZvqJs3FFEaxGmSynqrn8QvE4b06bbGh56r00cESZ1T6Pio7KO8Au0Nt7diTjygNBJUChKKejgq76F2Yc6CirGR1gzqgMwEGW5npLOj6BxEm_9wNKHY81-tFn-XqxPCVsrybtQFw3S0-k5mkTrWn3SpQb03zbEEfVywm-SiNdEBZs2MCC2aPb4woQ8oJF80J2q7hS31-ydJWUi5KrxSdBDDxVbQN2lw"

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


def get_players():
    url = "https://api.laligafantasymarca.com/api/v4/leagues/012408899/ranking?x-lang=es"
    data = requests.get(url,headers={'authorization': TOKEN}).json()
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


def check_players_operations(players):
    i = 1
    operaciones = []
    while True:
        data = requests.get(f"https://api.laligafantasymarca.com/api/v3/leagues/012408899/news/{i}?x-lang=es", headers={'authorization':TOKEN}).json()
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
    players = get_players()
    check_players_operations(players)
    print_players_value(players)


if __name__ == '__main__':
    main()


