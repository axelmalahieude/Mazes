import requests
from typing import List


class Maze:

    move_url = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token="

    def __init__(self, token: str):
        """Constructor"""

        self.locations_visited = []
        self.game_status = get_game_state(token)
        self.width = self.game_status["maze_size"][0]
        self.height = self.game_status["maze_size"][1]
        self.token = token

    def move(self, direction: str, check_already_visited: bool = True) -> str:
        """Move from current location in the specified location, if in bounds

            Keyword arguments:
            direction -- the direction in which to move
            check_already_visited -- whether to check if we have already
                visited a maze cell before moving there
        """

        current_location = self.locations_visited[len(self.locations_visited) - 1]

        new_x = current_location[0]
        new_y = current_location[1]

        if direction == "RIGHT":
            new_x += 1
        elif direction == "LEFT":
            new_x -= 1
        elif direction == "UP":
            new_y -= 1
        elif direction == "DOWN":
            new_y += 1

        # Makes use of short-circuit evaluation to determine whether we've already
        # visited the location we want to move to, while also checking boundaries
        if new_x < self.width and new_y < self.height \
                and (not check_already_visited or [new_x, new_y] not in self.locations_visited):
            ret = requests.post(Maze.move_url, data={"action": direction})
            result_code = ret.json()["result"]
            if result_code == "SUCCESS":
                self.locations_visited.append([new_x, new_y])
        else:
            result_code = "OUT_OF_BOUNDS"

        return result_code

    def retrace_step(self):
        """Move to the previous location we were at"""

        # Nowhere to retrace to if we haven't moved at least once
        if len(self.locations_visited) <= 1:
            return

        current_location = self.locations_visited[len(self.locations_visited) - 1]
        previous_location = self.locations_visited[len(self.locations_visited) - 2]
        direction = ""

        if current_location[0] > previous_location[0]:
            direction = "LEFT"
        elif current_location[0] < previous_location[0]:
            direction = "RIGHT"
        elif current_location[1] > previous_location[1]:
            direction = "UP"
        elif current_location[1] < previous_location[1]:
            direction = "DOWN"
        else:
            return

        self.move(direction, False) # flag move() to ignore maze cell visitation check


def get_game_state(token: str) -> List[str]:
    """Get information about the maze"""

    url = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token=" + token
    ret = requests.get(url)
    data = ret.json()
    return data


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

    maze = Maze(token)

if __name__ == "__main__":
    main()
