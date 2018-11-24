import requests


class Maze:

    move_url = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token="

    def __init__(self, token, game_status):
        """Constructor"""

        self.locations_visited = []
        self.path = []
        self.current_location = game_status["current_location"]
        self.width = game_status["maze_size"][0]
        self.height = game_status["maze_size"][1]
        self.token = token

    def move(self, direction):
        """Move from current location in the specified location, if in bounds

            Keyword arguments:
            direction -- the direction in which to move
            check_already_visited -- whether to check if we have already
                visited a maze cell before moving there
        """

        current_location = self.current_location

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

        if new_x < self.width and new_y < self.height and [new_x, new_y] not in self.locations_visited:
            ret = requests.post(Maze.move_url + self.token, data={"action": direction})
            result_code = ret.json()["result"]
            if result_code == "SUCCESS":
                self.locations_visited.append([new_x, new_y])
                self.path.append([new_x, new_y])
                self.current_location = [new_x, new_y]
        else:
            result_code = "OUT_OF_BOUNDS"

        return result_code

    def retrace_step(self):
        """Move to the previous location we were at"""

        current_location = self.path.pop()
        previous_location = self.path[len(self.path) - 1]

        if current_location[0] > previous_location[0]:
            direction = "LEFT"
        elif current_location[0] < previous_location[0]:
            direction = "RIGHT"
        elif current_location[1] > previous_location[1]:
            direction = "UP"
        else:
            direction = "DOWN"

        requests.post(Maze.move_url + self.token, data={"action": direction})
        self.current_location = previous_location

    def solve(self):
        self.locations_visited.append(self.current_location)
        self.path.append(self.current_location)

        while True:
            start = self.current_location
            if self.move("RIGHT") == "END":
                return
            if self.move("UP") == "END":
                return
            if self.move("LEFT") == "END":
                return
            if self.move("DOWN") == "END":
                return
            if start == self.current_location:
                self.retrace_step()


def get_game_state(token):
    """Get information about the maze"""

    url = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token=" + token
    ret = requests.get(url)
    data = ret.json()
    return data


# Main method
def main():
    url = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/session"

    ret = requests.post(url, data={"uid": "204915219"})
    data = ret.json()
    token = data["token"]

    status = ""
    while status != "FINISHED":
        maze = Maze(token, get_game_state(token))
        maze.solve()
        game = get_game_state(token)
        status = game["status"]
        print(game)


if __name__ == "__main__":
    main()
