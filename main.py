import pygame
import pygame.freetype

NUM_ROWS = 3
NUM_COLS = 10
GRID_SIZE = (50, 50) # Width, Height
SEATS_START_AT = (1, 1) # x, y grid cordinates to start making the seats


class Human:
    def __init__(self, seatNumber):
        self.seatNumber = seatNumber
        self.x = None
        self.y = None


class Seat:
    def __init__(self, row, col):
        self.row = row # Row relative to this set of seats
        self.col = col # Col relative to this set of seats
        self.color = (0, 0, 255) # Red, Green, Blue
        self.size = (40, 40) # Width, Height
    
    @property
    def x(self):
        return SEATS_START_AT[0] + self.col
    
    @property
    def y(self):
        return SEATS_START_AT[1] + self.row
    
    @property
    def number(self):
        return (self.col * NUM_ROWS) + self.row + 1


class App:
    def __init__(self):
        self._running = True # Is app running
        self._surface = None # Pygame surface for drawing
        self.font = None # Font used for text
        self.size = self.weight, self.height = 640, 400 # Size of pygame window

        self.seats = [Seat(row, col) for row in range(NUM_ROWS) for col in range(NUM_COLS)] # Create list of all seats, instances of Seat class
        self.humans = [Human(i) for i in range(NUM_ROWS * NUM_COLS)] # Create human per seat, instances of Human class

    def on_init(self):
        pygame.init()
        self._surface = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.font = pygame.freetype.Font('fonts/Roboto-Medium.ttf', 16)
        pygame.display.set_caption("Py-Boarding")
        self._running = True
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        pass

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
            pygame.draw.rect(self._surface, (0, 0, 255), [rectX, rectY, seat.size[0], seat.size[1]], 2)

            # Draw seat number near center of seat
            textX = gridCellX + (GRID_SIZE[0] / 2)
            textY = gridCellY + (GRID_SIZE[1] / 2)
            self.font.render_to(self._surface, (textX, textY), str(seat.number), (255, 255, 255))

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
