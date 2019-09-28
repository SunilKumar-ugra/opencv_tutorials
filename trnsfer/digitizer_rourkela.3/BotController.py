import math
import Process
from Resource import resource
from BluetoothController import BluetoothController
class Bot:
	currentBotPos = (0,0)
	nextCheckpointPos = (0,0)
	nextCheckpointAngle = 0
	currentCheckpointPos = (0,0)
	currentBotAngle = 0
	direction = 'forward'
	updateProperties = True

	@staticmethod
	def checkForResource(listOfResources, pathList):
		for i in listOfResources:
			for j in pathList:
				if (i[1], i[2]) == j:
					return i[0]

	@staticmethod
	def traversePath(pathList):
		lastPoint = len(pathList) - 1
		for point in pathList:
			while Bot.distance(Bot.currentBotPos, point) >  0.10:
				while Bot.angleBetweenPoints(Bot.currentBotPos, point) not in range(20):
					Bot.moveDirection('right', True)
				Bot.moveDirection('forward', True)
				Bot.currentBotPos = Bot.currentPos()
			if Bot.distance(Bot.currentBotPos, point) < 0.10:
				Bot.Stop()
				typeOfRes = Bot.checkForResource(Process.get_resources,pathList)
				if typeOfRes is "triangle":
					Bot.Blink("H")
				elif typeOfRes is "square":
					Bot.Blink("G")
				if point is pathList[lastPoint]:
					Bot.Blink("H")
					Bot.Blink("G")
					Bot.Stop()
				else:
					continue

	@staticmethod			
	def Blink(color):
		BluetoothController.send_command(color)
	@staticmethod
	def Stop():
		BluetoothController.send_command("s")
	@staticmethod
	def distance(point1, point2):
		distance = math.sqrt((point2[1] - point1[1])**2 + (point2[2] - point1[2])**2)
		return distance

	@staticmethod
	def midPoint(point1, point2):
		midPoint = (((point1[1] + point2[1]) / 2), ((point1[2] + point2[2]) / 2))
		return midPoint

	@staticmethod
	def angleBetweenPoints(origin, position):
		'''
		param-origin [Type-Point], position [Type-Point]
		returns-angleInDegrees [Type-float], dist [Type-float]
		Uses simple tan inverse function to find the angle then maps it to a proper angle between 0 to 360.
		'''

		deltaY = position[2] - origin[2]
		deltaX = position[1] - origin[1]
		angleInDegrees = round(atan2(deltaY, deltaX) * float(180) / 3.14)
		if angleInDegrees < 0:
			# angle is in I and II Quad, ie between 0 to -180, so map it to 0,180
			angleInDegrees = Bot.map(angleInDegrees, 0, -180, 0, 180)
		else:
			# angle is in III and IV Quad, ie between 0 to -180, so map it to 360,180
			angleInDegrees = Bot.map(angleInDegrees, 0, 180, 360, 180)
		return angleInDegrees

	@staticmethod
	def map(value, in_min, in_max, out_min, out_max):
		return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

	@staticmethod
	def moveDirection(direction, updateProperties=True):
		'''
		param-direction [Type-str] - pass direction of the bot, updateProperties [Type-bool, default = True]
		returns-None
		Also, if the bot is not in the camera range, the updateProperties parameter is False so that the position is not
		updated again. Based on the direction that the bot had to run, it sends the command to move in that direction. Usually forward
		or any other direction
		'''
		# Bot.setBotSpeed(Config.moveSpeed)

		if Bot.direction == 'forward':
			BluetoothController.send_command('F', "Forward : ^^^^^^^^^^^^^^^^^ ")
		else:
			BluetoothController.send_command(Bot.direction, "direction: " + Bot.direction)
		if updateProperties == True:
			Bot.UpdateProperties()

	@staticmethod
	def get_bot_front():
		max_area = 0
		min_area = 10000

		colorName = "pink"
		upperColor = Color(colorName, 1)
		lowerColor = Color(colorName, 0)
		list_of_points = []
		Frame.capture_frame()
		resized = Frame.cut
		ratio = 1


		hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)

		#t = cv2.getTrackbarPos('t','img')

		mask = cv2.inRange(hsv, lowerColor.get_array(), upperColor.get_array())

		res = cv2.bitwise_and(resized, resized, mask=mask)
		gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
		blurred = cv2.GaussianBlur(gray, (5, 5), 0)
		b = cv2.threshold(blurred, float(lowerColor.T), 255, cv2.THRESH_BINARY)[1]

		kernel = np.ones((3, 3), np.uint8)
		gry = cv2.erode(b, kernel, iterations=1)
		gry = cv2.dilate(b, kernel, iterations=1)
		
		cnts = cv2.findContours(gry, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		cnts = cnts[0] if imutils.is_cv2() else cnts[1]

		area = 0
		cX = 0
		cY = 0
		for c in cnts:
			M = cv2.moments(c)
			if M["m00"] > 0:
				cX = int((M["m10"] / M["m00"] + 1e-7) * ratio)
				cY = int((M["m01"] / M["m00"] + 1e-7) * ratio)
				#shape = sd.detect(c)
				c = c.astype("float")
				c *= ratio
				c = c.astype("int")
				area = cv2.contourArea(c)
				rad = getRadFromArea(area)
				if area>300:
					#cv2.drawContours(resized, [c], -1, (255,0,0), 2)
					list_of_points.append((cX, cY))


		if len(list_of_points)>0:
			bot_front = list_of_points[0]
			return bot_front
		else:
			return get_bot_front()
	@staticmethod
	def get_bot_back():
		max_area = 0
		min_area = 10000

		colorName = "yellow"
		upperColor = Color(colorName, 1)
		lowerColor = Color(colorName, 0)

		list_of_points = []
		Frame.capture_frame()
		resized = Frame.cut
		ratio = 1

		hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)

		#t = cv2.getTrackbarPos('t','img')

		mask = cv2.inRange(hsv, lowerColor.get_array(), upperColor.get_array())

		res = cv2.bitwise_and(resized, resized, mask=mask)
		gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
		blurred = cv2.GaussianBlur(gray, (5, 5), 0)
		b = cv2.threshold(blurred, float(lowerColor.T), 255, cv2.THRESH_BINARY)[1]

		kernel = np.ones((3, 3), np.uint8)
		gry = cv2.erode(b, kernel, iterations=1)
		gry = cv2.dilate(b, kernel, iterations=1)
		
		cnts = cv2.findContours(gry, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		cnts = cnts[0] if imutils.is_cv2() else cnts[1]

		area = 0
		cX = 0
		cY = 0
		for c in cnts:
			M = cv2.moments(c)
			if M["m00"] > 0:
				cX = int((M["m10"] / M["m00"] + 1e-7) * ratio)
				cY = int((M["m01"] / M["m00"] + 1e-7) * ratio)
				#shape = sd.detect(c)
				c = c.astype("float")
				c *= ratio
				c = c.astype("int")
				area = cv2.contourArea(c)
				rad = getRadFromArea(area)
				if area>300:
					#cv2.drawContours(resized, [c], -1, (255,0,0), 2)
					list_of_points.append((cX, cY))
					if area > max_area:
						max_area = area
					elif area < min_area:
						if __name__ == '__main__':
							min_area = area

			k = cv2.waitKey(5) & 0xFF
			if k == 27:
				break
		if len(list_of_points)>0:
			bot_back = list_of_points[0]
			return bot_back
		else:
			return get_bot_back()
	@staticmethod
	def currentPos():
		bot_front = get_bot_front()

		bot_back = get_bot_back()
		bot_center = midPoint(bot_front,bot_back)
		return bot_center,bot_back,bot_front
	@staticmethod
	def UpdateProperties(nextPoint):
		botPosition = Bot.currentPos()
		botAngle = Bot.angleBetweenPoints(botPosition, nextPoint)
		return botPosition, botAngle


