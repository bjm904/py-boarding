import random
import pygame
import pygame.freetype

NUM_ROWS = 20
NUM_COLS = 5
GRID_SIZE = (40, 40) # Width, Height
SEATS_START_AT = (1, 1) # x, y grid cordinates to start making the seats
HUMANS_START_AT = (0, NUM_COLS + 1)

def colToLetter(col):
    if (col == 0):
        return 'A'
    if (col == 1):
        return 'B'
    if (col == 2):
        return 'C'
    if (col == 3):
        return 'D'
    if (col == 4):
        return 'E'
    return 'F'

class Human:
    def __init__(self, row, col):
        #self.x = HUMANS_START_AT[0] - ((row * NUM_COLS) + col)
        self.x = HUMANS_START_AT[0] - (row + col * (NUM_ROWS))
        self.y = HUMANS_START_AT[1]
        self.color = (0, 255, 0) # Red, Green, Blue
        self.size = round((GRID_SIZE[0] * 0.7) / 2) # Radius
        #self.walkingSpeed = 0.04 + (random.random() / 10)
        self.walkingSpeed = 0.05
        self.seat = Seat(row, col)
        self.inSeat = False

    def nowInSeat(self):
        self.inSeat = True
        self.color = (0, 125, 0)

class Seat:
    def __init__(self, row, col):
        self.row = row # Row relative to this set of seats
        self.col = col # Col relative to this set of seats
        self.color = (0, 0, 255) # Red, Green, Blue
        self.size = (GRID_SIZE[0] * 0.8, GRID_SIZE[1] * 0.8) # Width, Height
    
    @property
    def x(self):
        return SEATS_START_AT[0] + self.row
    
    @property
    def y(self):
        return SEATS_START_AT[1] + self.col
    
    @property
    def seatNumber(self):
        return str(self.row) + colToLetter(self.col)


class App:
    def __init__(self):
        self._running = True # Is app running
        self._surface = None # Pygame surface for drawing
        self._font = None # Font used for text
        screenWidth = (NUM_ROWS + 2) * GRID_SIZE[0]
        screenHeight = (NUM_COLS + 3) * GRID_SIZE[1]
        self.size = self.weight, self.height = screenWidth, screenHeight # Size of pygame window

        self.seats = [Seat(row, col) for row in range(NUM_ROWS) for col in range(NUM_COLS)] # Create list of all seats, instances of Seat class
        self.humans = [Human(row, col) for row in range(NUM_ROWS) for col in range(NUM_COLS)] # Create human per seat, instances of Human class

        

    def on_init(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        self._surface = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._font = pygame.freetype.Font('fonts/Roboto-Medium.ttf', GRID_SIZE[0] * 0.3)
        pygame.display.set_caption("Py-Boarding")
        self._running = True

        pygame.mixer.init()
        self.inSeatSound = pygame.mixer.Sound('inSeat.wav')
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        for human in self.humans:
            if (human.inSeat == False):
                diffToSeatX = (human.seat.row + SEATS_START_AT[0]) - human.x
                diffToSeatY = (human.seat.col + SEATS_START_AT[1]) - human.y
                if (diffToSeatX != 0):
                    if (diffToSeatX > 0):
                        human.x += min(human.walkingSpeed, diffToSeatX)
                    else :
                        human.x += max(-human.walkingSpeed, diffToSeatX)
                elif (diffToSeatY != 0):
                    if (diffToSeatY > 0):
                        human.y += min(human.walkingSpeed, diffToSeatY)
                    else :
                        human.y += max(-human.walkingSpeed, diffToSeatY)
                else:
                    human.nowInSeat()
                    self.inSeatSound.play()
            

    def on_render(self):
        self._surface.fill((0,0,0)) # Fill black backgounrd, also for clearing
        for seat in self.seats:
            gridCellX = GRID_SIZE[0] * seat.x
            gridCellY = GRID_SIZE[1] * seat.y

            # Draw rectangle for seat
            centeringOffsetX = (GRID_SIZE[0] - seat.size[0]) / 2
            centeringOffsetY = (GRID_SIZE[1] - seat.size[1]) / 2
            rectX = gridCellX + centeringOffsetX
            rectY = gridCellY + centeringOffsetY
            pygame.draw.rect(self._surface, seat.color, [rectX, rectY, seat.size[0], seat.size[1]], 3)

            # Draw seat number near center of seat
            textSurface, textRect = self._font.render(seat.seatNumber, (255, 255, 255))
            textX = gridCellX + (GRID_SIZE[0] / 2) - (textRect.width / 2)
            textY = gridCellY + (GRID_SIZE[1] / 2) - (textRect.height / 2)
            self._surface.blit(textSurface, (textX, textY))

        for human in self.humans:
            gridCellX = GRID_SIZE[0] * human.x
            gridCellY = GRID_SIZE[1] * human.y

            # Draw rectangle for human
            rectX = int(gridCellX + (GRID_SIZE[0] / 2))
            rectY = int(gridCellY + (GRID_SIZE[1] / 2))
            pygame.draw.circle(self._surface, human.color, (rectX, rectY), int(human.size))

            # Draw human seatNumber near center of human
            textSurface, textRect = self._font.render(human.seat.seatNumber, (0, 0, 0))
            textX = rectX - (textRect.width / 2)
            textY = rectY - (textRect.height / 2)
            self._surface.blit(textSurface, (textX, textY))

        pygame.display.flip() # Render whole screen

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
