import random
import social


def generate_game(size):
    players = []
    for _ in range(size):
        players.append(social.Player(random.random()))
    network = social.Network(players, {"a": 7, "b": 0.5}, {
        "a": 9, "b": 5})
    return network

for _ in range(100):
    our_game = generate_game(100)
    for _ in range(100):
        our_game.display()
        our_game.step()
    avega = sum([player.consumption["a"]
                 for player in our_game.players]) / our_game.size
    avegb = sum([player.consumption["b"]
                 for player in our_game.players]) / our_game.size
    print("{'a':" + str(round(avega, 2)) +
          ", 'b':" + str(round(avegb, 2)) + "}")
