import requests

class mazeClass:

	# Initialize a grid to fit the maze
	def __init__(self, size):
		self.width = size[0]
		self.height = size[1]
		self.matrix = []
		for x in range(self.width):
			matrixRow = []
			self.matrix.append(matrixRow)
			for y in range(self.height):
				self.matrix[x].append(0)

	# Mark a space as visited in the maze
	def visit(self, location):
		self.matrix[location[0]][location[1]] = 1

	# Check if we've already visited a space in the maze
	def isSpaceVisited(self, location):
		if self.matrix[location[0]][location[1]] == 1:
			return True
		return False

# Get information about the maze
def getStatus(token):
	getUrl = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token=" + token
	getRequest = requests.get(getUrl)
	data = getRequest.json()
	return data

# Moves in a specific direction
def move(token, direction):
	moveUrl = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token=" + token
	moveRequest = requests.post(moveUrl, data={"action":direction})
	data = moveRequest.json()
	print data["result"]
	return data["result"]

# Solves the current maze we're on
def solveMaze(token, maze):
	status = getStatus(token)
	print status
	currLoc = status["current_location"]
	maze.visit(currLoc)

	# Try to move up
	code = move(token, "UP")
	status = getStatus(token)
	newLoc = status["current_location"]
	if code == "SUCCESS" and maze.isSpaceVisited(newLoc):
		move(token, "DOWN") # move back if we've already visited
	elif code == "SUCCESS":
		solveMaze(token, maze)
	elif code == "END":
		print "SOLVED MAZE++++++"

	# Try to move right
	code = move(token, "RIGHT")
	status = getStatus(token)
	newLoc = status["current_location"]
	if code == "SUCCESS" and maze.isSpaceVisited(newLoc):
		print "returned true"
		print currLoc
		move(token, "LEFT")
	elif code == "SUCCESS":
		solveMaze(token, maze)
	elif code == "END":
		print "SOLVED MAZE++++++"

	# Try to move left
	code = move(token, "LEFT")
	status = getStatus(token)
	newLoc = status["current_location"]
	if code == "SUCCESS" and maze.isSpaceVisited(newLoc):
		move(token, "RIGHT")
	elif code == "SUCCESS":
		solveMaze(token, maze)
	elif code == "END":
		print "SOLVED MAZE++++++"

	# Try to move down
	code = move(token, "DOWN")
	status = getStatus(token)
	newLoc = status["current_location"]
	if code == "SUCCESS" and maze.isSpaceVisited(newLoc):
		move(token, "UP")
	elif code == "SUCCESS":
		solveMaze(token, maze)
	elif code == "OUT_OF_BOUNDS":
		return
	elif code == "END":
		print "SOLVED MAZE++++++"

# Main method
def main():
	tokenUrl = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/session"

	tokenRequest = requests.post(tokenUrl, data={"uid":"204915219"})
	data = tokenRequest.json()
	token = data["token"]

	status = getStatus(token)
	maze = mazeClass(status["maze_size"])
	solveMaze(token, maze)

if __name__ == "__main__":
	main()
