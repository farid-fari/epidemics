#import random
import social

def generate_game(size):
    players = []
    for i in range(size):
        players.append(social.Player(int((i - size / 2) > 0)))
    graph = [[0 for _ in players] for _ in players]
    for i in range(size):
        for j in range(size):
            if i != j and (i - size / 2) * (j - size / 2) > 0:
                graph[i][j] = 2 / (size - 1)
    network = social.Network(players, {"a": 0.2, "b": .05}, {"a": 1.2, "b": 1.1}, graph=graph)
    return network

for _ in range(100):
    our_game = generate_game(30)
    for k in range(100):
        if k % 5 == 0:
            our_game.display()
        our_game.step()
    avega = sum([player.consumption["a"] + .5 for player in our_game.players]) / our_game.size
    avegb = sum([player.consumption["b"] + .5 for player in our_game.players]) / our_game.size
    print("{'a':" + str(round(avega, 2)) + ", 'b':" + str(round(avegb, 2)) + "}")
