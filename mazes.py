import requests


class Maze:

    move_url = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token="

    def __init__(self, token, game_status):
        """ Constructor """

        self.path = []
        self.current_location = game_status["current_location"]
        self.width = game_status["maze_size"][0]
        self.height = game_status["maze_size"][1]
        self.grid = [[0 for x in range(self.width)] for y in range(self.height)]
        self.token = token
        self.move_url = Maze.move_url + token

    def move(self, direction):
        """ Move from current location in the specified location, if in bounds

            Keyword arguments:
            direction -- the direction in which to move
            check_already_visited -- whether to check if we have already
                visited a maze cell before moving there
        """

        new_x = self.current_location[0]
        new_y = self.current_location[1]

        if direction == "RIGHT":
            new_x += 1
        elif direction == "LEFT":
            new_x -= 1
        elif direction == "UP":
            new_y -= 1
        else:  # down
            new_y += 1

        # Tests that we are in bounds and the space hasn't yet been visited
        if 0 <= new_x < self.width and 0 <= new_y < self.height\
                and self.grid[new_y][new_x] == 0:
            ret = requests.post(self.move_url, data={"action": direction})
            result_code = ret.json()["result"]
            # Mark the path and space if we successfully moved
            if result_code == "SUCCESS":
                self.grid[new_y][new_x] = 1
                self.path.append([new_x, new_y])
                self.current_location = [new_x, new_y]
            if result_code == "WALL":
                self.grid[new_y][new_x] = 2
        else:
            result_code = "OUT_OF_BOUNDS"

        return result_code

    def retrace_step(self):
        """ Move to the previous location we were at """

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

        # We know the move will be valid since we were already there
        requests.post(self.move_url, data={"action": direction})
        self.current_location = previous_location

    def solve(self):
        """ Solve the current maze """

        self.grid[self.current_location[1]][self.current_location[0]] = 1
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
            # If we haven't moved in any of the 4 directions, we need to
		        # retrace our steps until we are able to move
            if start == self.current_location:
                self.retrace_step()


def get_game_state(token):
    """Get information about the maze"""

    url = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token=" + token
    ret = requests.get(url)
    data = ret.json()
    return data


def main():
    """ Main method """

    url = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/session"

    ret = requests.post(url, data={"uid": "204915219"})
    data = ret.json()
    token = data["token"]

    game = get_game_state(token)
    print(game)
    status = ""

    # Loop until we've finished solving all 12 mazes
    while status != "FINISHED":
        maze = Maze(token, get_game_state(token))
        maze.solve()
        game = get_game_state(token)
        status = game["status"]
        print(game)
    print("Finished solving all mazes!")


if __name__ == "__main__":
    main()
