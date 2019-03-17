import pygame
import pygame.freetype

NUM_ROWS = 10
NUM_COLS = 3
GRID_SIZE = (50, 50) # Width, Height
SEATS_START_AT = (1, 1) # x, y grid cordinates to start making the seats
HUMANS_START_AT = (0, 4)

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
    def __init__(self, i):
        self.seatNumber = ()
        self.x = HUMANS_START_AT[0] - i
        self.y = HUMANS_START_AT[1]
        self.color = (0, 255, 0) # Red, Green, Blue
        self.size = 15 # Radius
        self.walkingSpeed = 0.01


class Seat:
    def __init__(self, row, col):
        self.row = row # Row relative to this set of seats
        self.col = col # Col relative to this set of seats
        self.color = (0, 0, 255) # Red, Green, Blue
        self.size = (40, 40) # Width, Height
    
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
        self.size = self.weight, self.height = 640, 640 # Size of pygame window

        self.seats = [Seat(row, col) for row in range(NUM_ROWS) for col in range(NUM_COLS)] # Create list of all seats, instances of Seat class
        self.humans = [Human(i) for i in range(NUM_ROWS * NUM_COLS)] # Create human per seat, instances of Human class

    def on_init(self):
        pygame.init()
        self._surface = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._font = pygame.freetype.Font('fonts/Roboto-Medium.ttf', 16)
        pygame.display.set_caption("Py-Boarding")
        self._running = True
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        for human in self.humans:
            human.x += human.walkingSpeed

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
            pygame.draw.rect(self._surface, seat.color, [rectX, rectY, seat.size[0], seat.size[1]], 2)

            # Draw seat number near center of seat
            textX = gridCellX + (GRID_SIZE[0] / 2)
            textY = gridCellY + (GRID_SIZE[1] / 2)
            self._font.render_to(self._surface, (textX, textY), seat.seatNumber, (255, 255, 255))

        for human in self.humans:
            gridCellX = GRID_SIZE[0] * human.x
            gridCellY = GRID_SIZE[1] * human.y

            # Draw rectangle for human
            rectX = int(gridCellX + (GRID_SIZE[0] / 2))
            rectY = int(gridCellY + (GRID_SIZE[1] / 2))
            pygame.draw.circle(self._surface, human.color, (rectX, rectY), int(human.size))

            # Draw human seatNumber near center of human
            #textX = gridCellX + (GRID_SIZE[0] / 2)
            #textY = gridCellY + (GRID_SIZE[1] / 2)
            #self._font.render_to(self._surface, (textX, textY), str(human.seatNumber), (255, 255, 255))

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
