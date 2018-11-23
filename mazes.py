import requests
from typing import List


# Get information about the maze
def get_game_state(token: str) -> List[str]:
    url = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token=" + token
    ret = requests.get(url)
    data = ret.json()
    return data


# Moves in a specific direction
def move(token: str, direction: str) -> str:
    url = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token=" + token
    ret = requests.post(url, data={"action": direction})
    data = ret.json()
    return data["result"]


# Solves the current maze we're on
def solve_maze(token: str) -> List[str]:
    game = get_game_state(token)
    start = game["current_location"]

    stack = [start]
    visited_locs = [start]

    width = game["maze_size"][0]
    height = game["maze_size"][1]

    while True:
        loc = stack.pop()
        x_loc = loc[0]
        y_loc = loc[1]

        # Try moving right
        # Check that we'd be in bounds
        if x_loc + 1 < width and [x_loc + 1, y_loc] not in visited_locs:
            code = move(token, "RIGHT")
            print(code)
            if code == "SUCCESS":
                visited_locs.append([x_loc + 1, y_loc])
                stack.append([x_loc + 1, y_loc])
                game = get_game_state(token)
                print("Moved right!")
                print(game)
            elif code == "END":
                return
            elif code == "WALL":
                visited_locs.append([x_loc + 1, y_loc])

        # Try moving up
        # Check that we'd be in bounds
        if y_loc - 1 >= 0 and [x_loc, y_loc - 1] not in visited_locs:
            code = move(token, "UP")
            if code == "SUCCESS":
                visited_locs.append([x_loc, y_loc - 1])
                stack.append([x_loc, y_loc - 1])
                game = get_game_state(token)
                print("Moved up!")
                print(game)
            elif code == "END":
                return
            elif code == "WALL":
                visited_locs.append([x_loc, y_loc - 1])

        # Try moving left
        # Check that we'd be in bounds
        if x_loc - 1 >= 0 and [x_loc - 1, y_loc] not in visited_locs:
            code = move(token, "LEFT")
            if code == "SUCCESS":
                visited_locs.append([x_loc - 1, y_loc])
                stack.append([x_loc - 1, y_loc])
                game = get_game_state(token)
                print("Moved left!")
                print(game)
            elif code == "END":
                return
            elif code == "WALL":
                visited_locs.append([x_loc - 1, y_loc])

        # Try moving down
        # Check that we'd be in bounds
        if y_loc + 1 < height and [x_loc, y_loc + 1] not in visited_locs:
            code = move(token, "DOWN")
            if code == "SUCCESS":
                visited_locs.append([x_loc, y_loc + 1])
                stack.append([x_loc, y_loc + 1])
                game = get_game_state(token)
                print("Moved down!")
                print(game)
            elif code == "END":
                return
            elif code == "WALL":
                visited_locs.append([x_loc, y_loc + 1])


# Main method
def main():
    url = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/session"

    ret = requests.post(url, data={"uid": "204915219"})
    data = ret.json()
    token = data["token"]

    solve_maze(token)
    game = get_game_state(token)
    print(game)


if __name__ == "__main__":
    main()
