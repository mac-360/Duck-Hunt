import pygame
import sys
import os
import random
# Declare global variables
screen = None
clock = None
FPS = 30
black = (0, 0, 0)
HEIGHT=800
WIDTH=1000
FONT_SIZE=20
WHITE=(255,255,255)
ORANGE = (255, 165, 0)
GREEN =(0,255,0)

Cursor_pos_x=0
Cursor_pos_y=0
direction_x_lst=['east', 'west']
direction_y_lst=['north','west']
AfterHowmuchTime=4
NoofBullets:int=3
GameOver:bool=False
TOTALSCORE:str='0'
TotalDelayTaken:int=0
def initialize():
    global screen, clock, black

    pygame.init()
    pygame.mixer.init()

    screen_width, screen_height = 1000, 800

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Duck Hunt")

    clock = pygame.time.Clock()

def DuckHuntDisplayScreen(duration_ms):
    global screen, clock, black, FPS

    script_dir = os.path.dirname(os.path.abspath(__file__))

    font_path = os.path.join(script_dir, r"press_start_2p\PressStart2P.ttf")

    duck_hunt_font_size = 120
    mac_font_size = 30

    duck_hunt_font = pygame.font.Font(font_path, duck_hunt_font_size)
    mac_font = pygame.font.Font(font_path, mac_font_size)

    pink_color_value = 0
    color_direction = 1

    duck_text = "DUCK"
    hunt_text = "HUNT"

    space_between_line_and_words = 200
    vertical_space = 20

    start_time = pygame.time.get_ticks()

    while pygame.time.get_ticks() - start_time < duration_ms:
        
        GameQuit()

        pink_color_value += color_direction
        if pink_color_value >= 255 or pink_color_value <= 0:
            color_direction *= -1

        screen.fill(black)

        text_duck = duck_hunt_font.render(duck_text, True, (255, pink_color_value, 180))
        screen.blit(text_duck, (screen.get_width() // 4 - duck_hunt_font_size, screen.get_height() // 2 - duck_hunt_font_size))

        text_hunt = duck_hunt_font.render(hunt_text, True, (255, pink_color_value, 180))
        screen.blit(text_hunt, (screen.get_width() // 4 , screen.get_height() // 2))

        text_2024_mac = mac_font.render("© 2024 MAC", True, (255, 255, 255))
        screen.blit(text_2024_mac, (screen.get_width() // 3, screen.get_height() - 3 * text_2024_mac.get_height()))

        pygame.display.flip()
        clock.tick(FPS)
        PlayDuckHuntThemeSong()

def play_audio(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def PlayDuckHuntThemeSong():
    audio_file = 'Title Screen.mp3'
    try:
        play_audio(audio_file)
    except pygame.error as e:
        print(f"Error: {e}")
        sys.exit()


def PlayGunShotAudio():
    global TotalDelayTaken
    audio_file = 'Gunshot.mp3'
    try:
        play_audio(audio_file)
        TotalDelayTaken+=2000
    except pygame.error as e:
        print(f"Error: {e}")
        sys.exit()

def PersonShooted():
    region_rect = pygame.Rect(WIDTH // 6 + 160, HEIGHT // 6 + 25, 350, 450)
    mouse_x, mouse_y=GetCursorPosition()
    for event in pygame.event.get():
        GameQuit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if region_rect.collidepoint(mouse_x, mouse_y):
                DisplayBlock((45, 166, 142))
                DisplayPerson()
                Display1PGame()
                pygame.display.flip()
                PlayGunShotAudio()
                DelayFunc(1000)

                return True
    return False

def DelayFunc(time:int):
    pygame.time.delay(time)
def DisplayBlock(Color):
    pygame.draw.rect(screen, Color, (WIDTH // 6 +160, HEIGHT // 6 +25, 350, 450))

def DisplayPerson():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, "BluePerson.png")  
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (300, 300))  
    screen.blit(image, (WIDTH // 6+190 ,50+ HEIGHT // 6))

def DisplayText(text, y,color,FONT_SIZE):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(script_dir, "press_start_2p", "PressStart2P.ttf")
    font = pygame.font.Font(font_path, FONT_SIZE)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, y))
    screen.blit(text_surface, text_rect)


def GameQuit():
    for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()


def Display1PGame():
    text="1-PLAYER"
    FONT_SIZE=30
    DisplayText(text,HEIGHT //1.5 - FONT_SIZE,GREEN,FONT_SIZE)
    text="  GAME  "
    DisplayText(text,HEIGHT //1.35 - FONT_SIZE,GREEN,FONT_SIZE)

def GetCursorPosition():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    return mouse_x, mouse_y

def DisplayCrossHair():
   
    global Cursor_pos_x, Cursor_pos_y
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, "crosshair.png")  
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (50, 50))  # Adjust the size as needed
    Cursor_pos_x, Cursor_pos_y = GetCursorPosition()
    screen.blit(image, (Cursor_pos_x - image.get_width() / 2, Cursor_pos_y - image.get_height() / 2))

def play_audio_in_background(filename:str):
    pygame.mixer.music.load(filename) 
    pygame.mixer.music.play()


def DisplayCredit():
    text="CREDIT 01"
    FONT_SIZE=30
    DisplayText(text,HEIGHT //1.05 - FONT_SIZE,WHITE,FONT_SIZE)

def MakeCursorInvisible():
    pygame.mouse.set_visible(False)
    return

def FireandStartDisplay():
    MakeCursorInvisible()
    while not PersonShooted():
        
        GameQuit()
        screen.fill((0, 0, 0))

        DisplayText("AIM AND FIRE", HEIGHT //10 - FONT_SIZE,WHITE,FONT_SIZE)
        DisplayText("TO START GAME", HEIGHT //10 + FONT_SIZE,WHITE,FONT_SIZE)

        DisplayBlock(ORANGE)
        DisplayPerson()
        Display1PGame()
        DisplayCredit()
        DisplayCrossHair()
        pygame.display.flip()

        pygame.time.Clock().tick(FPS*2)
    screen.fill(black)
    


def DisplayCredentials():
    text="PLAYER 1"
    font_size=30
    GameQuit()
    DisplayText(text,HEIGHT //4-font_size,WHITE,font_size)
    text=" READY "
    DisplayText(text,HEIGHT //3-font_size,WHITE,font_size)
    text="ROUND 01"
    DisplayText(text,HEIGHT //2.2-font_size,WHITE,font_size)
    text="3 SHOTS PER PERSON  ÔÔÔ"
    DisplayText(text,HEIGHT //1.72-font_size,WHITE,font_size)
    pygame.display.flip()
    pygame.time.Clock().tick(FPS*2)

def PlayIntroAudio():
    audio_file = 'Duck Hunt Intro.mp3'
    try:
        play_audio_in_background(audio_file)
    except pygame.error as e:
        print(f"Error: {e}")
        sys.exit()


def DisplayCredentialsScreen():
    start_time = pygame.time.get_ticks()
    PlayIntroAudio()
    while pygame.time.get_ticks() - start_time < 2000:  
        DisplayCrossHair()
        DisplayCredentials()
        screen.fill(black)
        
def Get_Img(sheet,frame,width,height,scale,color):
    image=pygame.Surface((width,height)).convert_alpha()
    image.blit(sheet,(0,0),((frame*width),0,width,height))
    image=pygame.transform.scale(image,(width*scale,height*scale))
    image.set_colorkey(color)
    return image

def DisplayStartofTheGame():
    sprite_sheet_img=pygame.image.load('NewSprite.png').convert_alpha()
    velocity_x=0
    latest_pos_x=0
    while velocity_x !=400:
        for i in range(0,5):
            DisplayBackGround()
            curr_frame=Get_Img(sprite_sheet_img,i%5,60,50,2.9,black)
            screen.blit(curr_frame,(WIDTH//20+velocity_x,HEIGHT//1.35))
            pygame.display.update()
            velocity_x+=10
            latest_pos_x=WIDTH//20+velocity_x
            DelayFunc(100)
            
            GameQuit()
    
    sprite_sheet_img=pygame.image.load('NewSprite2.png').convert_alpha()
    DisplayBackGround()
    curr_frame=Get_Img(sprite_sheet_img,0,60,61,2.9,black)
    screen.blit(curr_frame,(WIDTH//20+velocity_x,HEIGHT//1.45))
    pygame.display.update()
    DelayFunc(2000)
    velocity_y=0


    DisplayBackGround()
    velocity_y+=180
            
    curr_frame=Get_Img(sprite_sheet_img,1,60,61,2.9,black)
    screen.blit(curr_frame,(latest_pos_x,HEIGHT//1.45-velocity_y))
    pygame.display.update()
    Bark()

    


    
    DisplayBackGround()
    velocity_y-=80
    curr_frame=Get_Img(sprite_sheet_img,2,60,61,2.9,black)
    screen.blit(curr_frame,(latest_pos_x,HEIGHT//1.45-velocity_y))
    pygame.display.update()
    Bark()

    
    DisplayBackGround()
    pygame.display.update()

    

    
    
def Bark():
    audio_file = 'Bark.mp3'
    try:
        play_audio(audio_file)
    except pygame.error as e:
        print(f"Error: {e}")
        sys.exit()


    




def DisplayBackGround():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, "Background.jpg")
    image = pygame.image.load(image_path)

    # Calculate the scaling factors
    scale_x = 1000 / image.get_width()
    scale_y = 800 / image.get_height()

    new_size = (int(image.get_width() * scale_x), int(image.get_height() * scale_y))
    image = pygame.transform.scale(image, new_size)
    screen.blit(image, (0, 0))



class Duck():
    def __init__(self,pos_x,pos_y,speed,kind,x_direction,velocity_x,Duck_created_at,velocity_y,y_direction,score,img,aliveornot,Falling,CompleteFall,music_played):
        global direction_lst
        self.Falling=False
        self.music_played=False
        self.CompleteFall=False
        self.aliveornot=True
        self.pos_x=random.randint(0,900)
        self.pos_y=600
        self.Duck_created_at=pygame.time.get_ticks()
        self.kind=random.choices([1,2,3],weights=[0.45, 0.35, 0.20])[0]
        self.SetSpeed()
        self.SetScore()
        self.x_direction=self.Get_New_X_Direction()
        self.y_direction='north'
        self.SetDuckImg()

  

    def __eq__(self, other):
        if isinstance(other, Duck):
            return (
                self.pos_x == other.pos_x and
                self.pos_y == other.pos_y and
                self.speed == other.speed and
                self.kind == other.kind and
                self.x_direction == other.x_direction and
                self.velocity_x == other.velocity_x and
                self.Duck_created_at == other.Duck_created_at and
                self.velocity_y == other.velocity_y and
                self.y_direction == other.y_direction and
                self.score == other.score and
                self.img == other.img
            )
        return False


    def Get_New_X_Direction(self):
        global direction_x_lst
        return direction_x_lst[random.randint(0, (len(direction_x_lst) - 1))]
    
    def Get_New_Y_Direction(self):
        global direction_y_lst
        return direction_y_lst[random.randint(0, (len(direction_y_lst) - 1))]
    
    def LoadImage(self,filename:str,frameno:int=0):
        self.img=pygame.image.load(filename).convert_alpha()
        self.img=Get_Img(self.img,frameno,36,47,2.9,WHITE)
    
    def DisplayDuck(self):
        screen.blit(self.img,(self.pos_x,self.pos_y))
        pygame.display.update()
        
    def SetVelocity(self,velocity_x:int,velocity_y:int):
        self.velocity_x=velocity_x
        self.velocity_y=velocity_y

    def UpdatePosition(self):
        self.pos_x+=self.velocity_x
        self.pos_y+=self.velocity_y

   
    def CheckTimeExceedorNot(self):
        global AfterHowmuchTime
        if ((pygame.time.get_ticks()-self.Duck_created_at)/1000.0)>=AfterHowmuchTime:
            self.ChangeDirection()
            self.Duck_created_at=pygame.time.get_ticks()
        
    def CheckBoundaryReachedOrNot(self):
        if self.pos_x < 10:
            self.x_direction='east'
        if self.pos_x>WIDTH-100:
            self.x_direction='west'
        if self.pos_y>HEIGHT-500:
            self.y_direction='north'
        if self.pos_y<1:
            self.y_direction='south'

    def PlayBirdFlap(self):
        audio_file = 'Duck Flapping.mp3'
        try:
            play_audio_in_background(audio_file)
        except pygame.error as e:
            print(f"Error: {e}")
            sys.exit() 
    def SetDuckImg(self,i=0):
        if self.aliveornot==True:
            self.CheckTimeExceedorNot()
            self.CheckBoundaryReachedOrNot()
            self.PlayBirdFlap()
            if self.kind==1 and self.x_direction=='west' and self.y_direction=='north':
                self.LoadImage('Brown_Duck_Flying_Left.png',i)
                self.SetVelocity(-(self.speed),-(self.speed))
                self.UpdatePosition()
            
            
            elif self.kind==1 and self.x_direction=='west' and self.y_direction=='south':
                self.LoadImage('Brown_Duck_Flying_Left.png',i)
                self.SetVelocity(-(self.speed),(self.speed))
                self.UpdatePosition()

            elif self.kind==1 and self.x_direction=='east'and self.y_direction=='north':
                self.LoadImage('Brown_Duck_Flying_Right.png',i)
                self.SetVelocity((self.speed),-(self.speed))
                self.UpdatePosition()
            elif self.kind==1 and self.x_direction=='east'and self.y_direction=='south':
                self.LoadImage('Brown_Duck_Flying_Right.png',i)
                self.SetVelocity((self.speed),(self.speed))
                self.UpdatePosition() 








            elif self.kind==2:
                if self.kind==2 and self.x_direction=='west' and self.y_direction=='north':
                    self.LoadImage('Blue_Duck_Flying_Left.png',i)
                    self.SetVelocity(-(self.speed),-(self.speed))
                    self.UpdatePosition()
            
            
                elif self.kind==2 and self.x_direction=='west' and self.y_direction=='south':
                    self.LoadImage('Blue_Duck_Flying_Left.png',i)
                    self.SetVelocity(-(self.speed),(self.speed))
                    self.UpdatePosition()

                elif self.kind==2 and self.x_direction=='east'and self.y_direction=='north':
                    self.LoadImage('Blue_Duck_Flying_Right.png',i)
                    self.SetVelocity((self.speed),-(self.speed))
                    self.UpdatePosition()
                elif self.kind==2 and self.x_direction=='east'and self.y_direction=='south':
                    self.LoadImage('Blue_Duck_Flying_Right.png',i)
                    self.SetVelocity((self.speed),(self.speed))
                    self.UpdatePosition() 





            elif self.kind==3:
                if self.kind==3 and self.x_direction=='west' and self.y_direction=='north':
                    self.LoadImage('Red_Duck_Flying_Left.png',i)
                    self.SetVelocity(-(self.speed),-(self.speed))
                    self.UpdatePosition()
            
            
                elif self.kind==3 and self.x_direction=='west' and self.y_direction=='south':
                    self.LoadImage('Red_Duck_Flying_Left.png',i)
                    self.SetVelocity(-(self.speed),(self.speed))
                    self.UpdatePosition()

                elif self.kind==3 and self.x_direction=='east'and self.y_direction=='north':
                    self.LoadImage('Red_Duck_Flying_Right.png',i)
                    self.SetVelocity((self.speed),-(self.speed))
                    self.UpdatePosition()
                elif self.kind==3 and self.x_direction=='east'and self.y_direction=='south':
                    self.LoadImage('Red_Duck_Flying_Right.png',i)
                    self.SetVelocity((self.speed),(self.speed))
                    self.UpdatePosition() 





        elif self.aliveornot==False:
            self.DisplayHittedDuck()

        

   

    def SetScore(self):
        if self.kind==1:
            self.score=50
        elif self.kind==2:
            self.score=100
        else:
            self.score=200
    
    def ChangeDirection(self):
        self.Get_New_X_Direction()
        self.Get_New_Y_Direction()
        
    def SetSpeed(self):
        if self.kind==1:
            self.speed=10
        elif self.kind==2:
            self.speed=15
        else:
            self.speed=20
    
    def OutofBullets(self):
        if NoofBullets <= 0:
            print(NoofBullets)
            GameOver = True
            return True
        return False

    def TriggerPulled(self):
        global NoofBullets
        mouse_x, mouse_y = GetCursorPosition()
        run = self.OutofBullets()
        if not run:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    PlayGunShotAudio()
                    print('fired')
                    NoofBullets -= 1
                    return True, mouse_x, mouse_y

        return False, -1, -1
        

    def CheckifDuckwasKilled(self, mouse_x, mouse_y):
        image_size = self.img.get_size()
        width, height = image_size
        width*=6
        height*=6
        return (self.pos_x-10 <= mouse_x <= self.pos_x + width+10) and (self.pos_y-10<= mouse_y <= self.pos_y + height+10)

    def PlayQuack(self):
        audio_file = 'Quack.mp3'
        try:
            play_audio_in_background(audio_file)
        except pygame.error as e:
            print(f"Error: {e}")
            sys.exit() 
    
    def PlayFallingDuck(self):
        audio_file = 'Dead Duck Falls.mp3'
        try:
            pygame.mixer.Sound(audio_file).play()
        except pygame.error as e:
            print(f"Error: {e}")
            sys.exit()
    
    def PlayDuckLands(self):
        audio_file = 'Dead Duck Lands.mp3'
        try:
            pygame.mixer.Sound(audio_file).play()
        except pygame.error as e:
            print(f"Error: {e}")
            sys.exit()

    def DisplayHittedDuck(self):
        global TotalDelayTaken
        self.AnyOtherDuckIsShooted()
        if self.aliveornot==False and (not self.Falling):
            if self.kind==1:
                self.LoadImage('Brown_Duck_After_Hit.png',0)
            elif self.kind==2:
                self.LoadImage('Blue_Duck_After_Hit.png',0)
            else:
                self.LoadImage('Red_Duck_After_Hit.png',0)
            #self.SetVelocity(-(10),-(30))
            self.UpdatePosition()
            self.DisplayDuck()
            self.PlayQuack()
            DelayFunc(500)
            TotalDelayTaken+=500
            self.Falling=True
            
        if self.Falling and (not self.CompleteFall) :
            if self.kind==1:
                self.img=pygame.image.load('Brown_Duck_After_Hit_Fall.png').convert_alpha()
            elif self.kind==2:
                self.img=pygame.image.load('Blue_Duck_After_Hit_Fall.png').convert_alpha()
            else:
                self.img=pygame.image.load('Red_Duck_After_Hit_Fall.png').convert_alpha()

            self.img=Get_Img(self.img,random.randint(0,3),25,48,2.9,WHITE)
            self.SetVelocity(-(0),(50))
            self.pos_y+=10
            self.DisplayDuck()
            if not self.music_played and not self.CompleteFall:
                self.PlayFallingDuck()
                self.music_played=True
            if self.pos_y>=500:
                self.PlayDuckLands()
                self.music_played=False
                self.CompleteFall=True
        
    def AnyOtherDuckIsShooted(self):
        global ducks,ducks_to_remove,ducks
        for otherduck in ducks:
            if not otherduck.CompleteFall:
                if otherduck!=self:
                    killed = otherduck.DuckKilled()
                    if killed:
                        UpdateTotalScore(self.score)
                        if len(ducks)==0:
                            ducks = [Duck(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0) for _ in range(random.randint(1,4))] 
                        otherduck.aliveornot = False
                        otherduck.DisplayHittedDuck()
                    if otherduck.CompleteFall:    
                        ducks_to_remove.append(self)





        

    def DuckKilled(self):
        condition, mouse_x, mouse_y = self.TriggerPulled()
        if condition:
            killedornot = self.CheckifDuckwasKilled(mouse_x, mouse_y)
            return killedornot
        return False

def DisplayRectangle(box_color, border_color, border_size, box_position, box_dimensions):
    pygame.draw.rect(screen, border_color, (box_position[0] - border_size, box_position[1] - border_size, box_dimensions[0] + 2 * border_size, box_dimensions[1] + 2 * border_size))
    pygame.draw.rect(screen, box_color, (box_position[0], box_position[1], box_dimensions[0], box_dimensions[1]))



def DisplayString(text, font_size, text_color, pos_x, pos_y):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(script_dir, "press_start_2p", "PressStart2P.ttf")
    # Create font object
    font = pygame.font.Font(font_path, font_size)

    # Render the text
    text_surface = font.render(text, True, text_color)

    # Blit the text surface onto the main surface
    screen.blit(text_surface, (pos_x, pos_y))


def DisplayScore():
    DisplayRectangle(black,WHITE,10,(WIDTH-200,HEIGHT-120),(140,80))
    DisplayString(TOTALSCORE,28,WHITE,WIDTH-180,HEIGHT-100)

def UpdateTotalScore(score):
    global TOTALSCORE
    tscr=int(TOTALSCORE)+score
    TOTALSCORE=str(tscr)

initialize()
ducks = [Duck(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0)] 
ducks_to_remove = []
def DisplayClock(Clock:str):
    DisplayRectangle(black,WHITE,10,(WIDTH-600,HEIGHT-120),(250,80))
    DisplayString(Clock,28,WHITE,WIDTH-540,HEIGHT-100)


def NotTimeFinished(start_time,timer_duration):
    global TotalDelayTaken
    elapsed_time = pygame.time.get_ticks() - (start_time+TotalDelayTaken)
    time_remaining = max(0, timer_duration - elapsed_time)

    minutes_left = time_remaining // (60 * 1000)
    seconds_left = (time_remaining % (60 * 1000)) // 1000

    # Convert minutes and seconds to a formatted string
    clock_str = f"{minutes_left:02}:{seconds_left:02}"

    DisplayClock(clock_str)

    if elapsed_time >= timer_duration:
        return False
    else:
        return True

def DisplayBulltes():
    global NoofBullets
    bullet_str=''
    for i in range(NoofBullets):
        bullet_str+='ô'
    # Assuming WIDTH and HEIGHT are defined earlier in your code

    # Display rectangle to the left
    DisplayRectangle(black, WHITE, 10, (20, HEIGHT - 120), (150, 80))

    # Calculate the center of the rectangle
    rectangle_center_x = 50

    # Display string inside the rectangle
    DisplayString(bullet_str, 28, (255,0,0), rectangle_center_x, HEIGHT - 100)

def DisplayGameOver():
    screen.fill(black)
    window_center_x=WIDTH//2
    window_center_x-=240
    window_center_y=HEIGHT//2
    GameOverstr="G A M E   O V E R"
    font_size=64
    padding=0
    play_audio_in_background('Game Over.mp3')
    for char in GameOverstr:
        DisplayString(char, font_size, (255, 0, 0), window_center_x+padding-len(GameOverstr), window_center_y)
        padding+=30
        pygame.display.update()
        DelayFunc(120)
    DelayFunc(500)
    pygame.quit()
    sys.exit()


def Rand():
    global NoofBullets, GameOver,ducks,ducks_to_remove,TotalDelayTaken

    
    # Create a list of ducks
    i = 0
    start_time = pygame.time.get_ticks()
    timer_duration=1* 60 * 1000
    while  NotTimeFinished(start_time,timer_duration):
            if NoofBullets <= 0:
                while NoofBullets!=3:
                    DelayFunc(100)
                    TotalDelayTaken+=100
                    NoofBullets+=1
                    DisplayBulltes()
                    play_audio_in_background('Reloading.mp3')
                    pygame.display.update()
            if len(ducks)==0:
                
                ducks = [Duck(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0) for _ in range(random.randint(1,3))] 
                
            DisplayBackGround()
            DisplayCrossHair()
            DisplayScore()
            NotTimeFinished(start_time,timer_duration)
            DisplayBulltes()
            for duck in ducks:
                if not duck.CompleteFall:
                    duck.SetDuckImg(i % 3)
                    duck.DisplayDuck()

                    killed = duck.DuckKilled()
                    if killed:
                        UpdateTotalScore(duck.score)
                        duck.aliveornot = False
                        duck.DisplayHittedDuck()
                    if duck.CompleteFall:    
                        ducks_to_remove.append(duck)

            for duck_to_remove in ducks_to_remove:
                ducks.remove(duck_to_remove)

            # Clear the ducks_to_remove list
            ducks_to_remove = []
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    PlayGunShotAudio()
                    print('fired')
                    NoofBullets -= 1

            i += 1
            DelayFunc(100)
            TotalDelayTaken+=100
            GameQuit()

    DisplayGameOver()
    

initialize()
DuckHuntDisplayScreen(duration_ms=4000)  
FireandStartDisplay()
DisplayCredentialsScreen()
DisplayStartofTheGame()

Rand()




