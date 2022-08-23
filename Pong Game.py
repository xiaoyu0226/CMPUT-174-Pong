# Pong version 3
# Xiao Yu
# Lab H04

# This version creates a game window, show two bars and 1 white ball moving and bounching on the screen, keeping the score points and let all bounce off the rectangle,with keypress the bar moves

# import pygame module
import pygame

def main():
    # program will be written here
    # initiate the pygame module
    pygame.init()
    # set the window display with 500 times 400 pixels 
    pygame.display.set_mode((500,400))
    # set the name of the game displayed on window top
    pygame.display.set_caption('Pong')
    # we will work on the surface of the window being displayed
    surface=pygame.display.get_surface()
    # create object of class game
    game=Game(surface)
    # call the play method of game
    game.play()
    # quit pygame
    pygame.quit()


class Game:
    # class game will be defined here
    def __init__(self,surface):
        # first initialize the Game class
        
        # set different properties associated with it
        self.surface=surface
        self.bg_color=pygame.Color('black')
        # close click indicate if player quit window or not
        # continue game indicate if game should be updated further
        self.close_click=False
        self.continue_game=True
        # maximum frame per second is 80
        self.FPS=80
        # set clock for the game
        self.game_Clock=pygame.time.Clock()
        # create 3 objects
        # dot from dot class
        self.dot_velocity=[3,1]
        self.dot=Dot('white',6,[200,150],self.dot_velocity,self.surface)
        # create two rectangle objects
        self.rec_size=[10,60]
        self.rec1_location=[80,170]
        self.rec2_location=[410,170]
        self.rec1=pygame.Rect(self.rec1_location,self.rec_size)
        self.rec2=pygame.Rect(self.rec2_location,self.rec_size)
        # assign initial score
        self.score_player1=0
        self.score_player2=0  
        # assign speed of rectangle
        self.rec1_speed = 0
        self.rec2_speed = 0
        
    def play(self):
        # define play method of game
        # while player did not close the window
        # run the rest of code
        while self.close_click==False:
            # first handle all events
            # second draw each frame
            # if the game should keep on continue
            # update the status if game continue
            # check if game continue is true or not
            # limit the max number of frame persecond to be 80
            self.handle_event()
            self.draw()
            if self.continue_game:
                self.update()
                self.decide_continue()
            self.game_Clock.tick(self.FPS)
            
    def handle_event(self):
        # method for game to handle event is defined here
        # capture all the events 
        # check each event, if event type is to quit the game
        # close_click will be true, the window will be closed
        # handle key up or key down events
        events=pygame.event.get()
        for event in events:
            if event.type==pygame.QUIT:
                self.close_click=True
            if event.type==pygame.KEYDOWN:
                self.handle_keydown(event.key)
            if event.type==pygame.KEYUP:
                self.handle_keyup(event.key)
                
    def handle_keydown(self,key):
        # this part handles keydown event
        # adds velocity to the rectangles for moving 
        # velocity direction depends on key pressed
        if key==pygame.K_q:
            self.rec1_speed=-5
        if key==pygame.K_p:
            self.rec2_speed=-5
        if key==pygame.K_a:
            self.rec1_speed=5
        if key==pygame.K_l:
            self.rec2_speed=5
            
    def handle_keyup(self,key):
        # if the key is up, then make rectangle stationary
        # change velocity according to which key pressed 
        # specific for specific rectangle
        if (key==pygame.K_q) or (key==pygame.K_a):
            self.rec1_speed=0
        if (key==pygame.K_p) or (key==pygame.K_l):
            self.rec2_speed=0        
        
    def rec_move(self):
        # move the rectangle according to new speed
        # if rec moving up only when rec top is not below 0
        # rec moving down only when rec bottom is not above the screen height
        bottom_edge=self.surface.get_height()
        if (self.rec1.top<=0 and self.rec1_speed<=0) or (self.rec1.bottom>=bottom_edge and self.rec1_speed>=0):
            self.rec1_speed=0
        if (self.rec2.top<=0 and self.rec2_speed<=0) or (self.rec2.bottom>=bottom_edge and self.rec2_speed>=0):
            self.rec2_speed=0
        self.rec1.top+=self.rec1_speed
        self.rec2.top+=self.rec2_speed
        
    def draw(self):
        # method for game to draw frames will be defined here
        # fill the surface with choosen backgroup color
        # draw the dot new position
        # draw the two rectangles
        # draw the score
        # update the display of the above drawing
        self.surface.fill(self.bg_color)
        self.dot.draw()
        pygame.draw.rect(self.surface,pygame.Color('white'),self.rec1)
        pygame.draw.rect(self.surface,pygame.Color('white'),self.rec2)
        self.draw_score()
        pygame.display.update()
    
    def draw_score(self):
        # drawing the score will be in here
        # set fg and bg color
        # set font size
        # create 2 text box for two scores
        fg=pygame.Color('white')
        bg=pygame.Color('Black')
        font=pygame.font.SysFont('',80)
        text_box_one=font.render(str(self.score_player1),True, fg, bg)
        text_box_two=font.render(str(self.score_player2),True, fg, bg)
        text_box_two_x=self.surface.get_width()-text_box_two.get_width()
        box_two_loation=(text_box_two_x,0)
        box_one_location=(0,0)
        self.surface.blit(text_box_one,box_one_location)
        self.surface.blit(text_box_two,(text_box_two_x,0))        
    
    def score_count(self):
        # the score will be counted and added here
        # get the x coordinate of dot location
        # assign left and right edge 
        # check if ball hit left or right edge and update score for players
        # return false for continue game if one score hit 11
        dot_location=self.dot.return_center()
        dot_location_x=dot_location[0]
        left_edge=self.dot.return_radius()
        right_edge=self.surface.get_width()-self.dot.return_radius()
        if dot_location_x<=left_edge:
            self.score_player2+=1
        if dot_location_x>=right_edge:
            self.score_player1+=1
        
    def paddle_bounce(self):
        # ball bounce off paddle defined here
        # get ball location
        # if ball moving left and hit rect1, change x component of velocity to opposite sign
        # if ball moving right and hit rec2, change x component of velocity to opposite sign
        ball_location=self.dot.return_center()
        if self.dot_velocity[0]<0 and self.rec1.collidepoint(ball_location):
            self.dot_velocity[0]=-self.dot_velocity[0]
        if self.dot_velocity[0]>0 and self.rec2.collidepoint(ball_location):
            self.dot_velocity[0]=-self.dot_velocity[0]
            
    def decide_continue(self):
        # check if score hit 11 and decide to continue game or not
        # return false for continue game if one score hit 11
        if self.score_player1==11 or self.score_player2==11:
            self.continue_game=False
            
    def update(self):
        # update of game will be here
        # update the dot new location by calling move method associated with dot object
        # update the moving of rectangle
        # update if ball bounces off paddle
        # update the score
        self.dot.move() 
        self.rec_move()
        self.paddle_bounce()
        self.score_count()
       
class Dot:
    # class dot will be defined here
    def __init__(self, dot_color, dot_radius, dot_center, dot_velocity, surface):
        # first initalize dot class and give dot object different properties
        # these include color, radius, center location, velocity of dot moving and surface its on
        self.color=pygame.Color(dot_color)
        self.radius=dot_radius
        self.center=dot_center
        self.velocity=dot_velocity
        self.surface=surface
    
    def return_radius(self):
        # this method returns the value of dot radius
        return self.radius
    
    def return_center(self):
        # this method returns the value of dot center
        return self.center
    
    def draw(self):
        # method draw for dot object will be defined here
        # draw a circle on surface with specific color, center, radius
        pygame.draw.circle(self.surface,self.color,self.center,self.radius)
    
    def move(self):
        # method move for dot object will be defined here
        # obtain the size of screen
        size_screen=self.surface.get_size()
        # move center of dot according to velocity vector of dot project
        # also check location if collide with side of screen
        for index in range(0,2):
            self.center[index]=self.center[index]+self.velocity[index]
            # if dot collide to left or top of the screen
            # corresponding component of velocity vector switch sign
            if self.center[index]<=self.radius:
                self.velocity[index]=-self.velocity[index]
            # if dot collide to bottom or right side of screen
            # switch sign of corresponding veloctity vector component
            if self.center[index]+self.radius>=size_screen[index]:
                self.velocity[index]=-self.velocity[index]
# recal the main function    
main()
