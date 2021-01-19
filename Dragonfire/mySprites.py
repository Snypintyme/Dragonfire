''' Author: Gavin Tse 

    Date: May 28, 2019 
    
    Description: The sprite module for the Dragonfire game. It contains the Player, Portal, Fireball, Dragon, Treasure, ScoreKeeper, and Life sprites essential for the game logic.
'''

import pygame, random
            
class Player(pygame.sprite.Sprite):
    '''This class defines the player sprite that can duck, jump, move left, and right in stage 1 and can move up, down, left, and right in stage 2.'''
    def __init__(self, screen, stage, spawnLocation):
        '''This initializer takes the screen surface, stage, and spawnLocation as parameters. The player will be positioned at the given spawnLocation to start.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # Load player images
        self.playerLeft1 = pygame.image.load("myImages/playerLeft1.PNG").convert()
        self.playerLeft2 = pygame.image.load("myImages/playerLeft2.PNG").convert()        
        self.playerRight1 = pygame.image.load("myImages/playerRight1.PNG").convert()
        self.playerRight2 = pygame.image.load("myImages/playerRight2.PNG").convert()
        self.playerLeftCrouched = pygame.image.load("myImages/playerLeftCrouched.PNG").convert()
        self.playerRightCrouched = pygame.image.load("myImages/playerRightCrouched.PNG").convert()
       
        # Set initial image
        self.image = self.playerLeft1
       
        # Spawn the player on the right side of the drawbridge
        self.rect = self.image.get_rect()
        self.rect.right = spawnLocation[0] - 1
        self.rect.bottom = spawnLocation[1]

        # Set the initial x and y vectors for the player
        self.dx = 0
        self.dy = 0
        
        # Instance variables
        self.window = screen
        self.directionFacing = 1
        self.crouched = False
        self.imageChangeCounter = 0
        self.stage = stage
        
    def changeDirection(self, direction, xChange):
        '''This method changes the x and y vector of the player using the provided direction parameter and changes the image accordingly.'''
        if self.stage == 2:
            if xChange == 1:
                if direction[0] < 0:
                    self.image = self.playerLeft1
                    self.directionFacing = 1
                elif direction[0] > 0:
                    self.image = self.playerRight1
                    self.directionFacing = 0
                self.dx = direction[0]
            else:
                self.dy = direction[1]
        else:
            if self.crouched == False:
                if direction[0] < 0:
                    self.image = self.playerLeft1
                    self.directionFacing = 1
                elif direction[0] > 0:
                    self.image = self.playerRight1
                    self.directionFacing = 0
                self.dx = direction[0]
        
    def jump(self):
        '''This method increases the y vector of the player, causing it to jump.'''
        # Only jump if standing on the drawbridge
        if self.rect.bottom == 312:
            self.dy = 6
            
    def toggleCrouch(self):
        '''This method puts the player in a crouch position by changing the image if thay are standing, otherwise it will cause the player to stand up again.'''
        if self.crouched == False:
            if self.directionFacing == 1:
                self.image = self.playerLeftCrouched
            else:
                self.image = self.playerRightCrouched
            self.tempLeftRect = self.rect.left
            if self.rect.bottom != 312:
                self.tempBottomRect = self.rect.bottom
            else:
                self.tempBottomRect = 312
            self.rect = self.image.get_rect()
            self.rect.bottom = self.tempBottomRect
            self.rect.left = self.tempLeftRect
            self.dx = 0
            self.crouched = True            
                
        else:
            if self.directionFacing == 1:
                self.image = self.playerLeft1
            else:
                self.image = self.playerRight1 
            self.tempLeftRect = self.rect.left
            self.rect = self.image.get_rect()
            self.rect.bottom = 312
            self.rect.left = self.tempLeftRect
            self.dx = 0
            self.crouched = False
        
    def reset(self, spawnLocation):
        '''This method moves the player back to the desired spawn location.'''
        self.rect.right = spawnLocation[0] - 1
        self.rect.bottom = spawnLocation[1]
         
    def update(self):
        '''This method will be called automatically to reposition the player sprite on the screen and cycle between the running images.'''
        # Only move laterally if the player has not reached the sides of the screen
        if (self.rect.left > 0 and self.dx < 0) or (self.rect.right < self.window.get_width() and self.dx > 0):
            self.rect.left += self.dx  
            
        # Only move vertically if the player has not reached the top or bottom of the screem
        if (self.rect.top > 31 and self.dy > 0) or (self.rect.bottom < 370 and self.dy < 0):
            self.rect.top -= self.dy
        if self.rect.top < 31:
            self.rect.top = 31
        
        # Stage 1 Gravity
        if self.stage == 1:
            self.rect.bottom -= self.dy
            self.dy -= 1
            if self.rect.bottom > 312:
                self.rect.bottom = 312
                self.dy = 0
        
        # Cycle between images to create running effect  
        if self.dx != 0: 
            if self.imageChangeCounter > 1:
                if self.directionFacing == 1:
                    if self.image == self.playerLeft1:
                        self.image = self.playerLeft2
                    else:
                        self.image = self.playerLeft1
                else:
                    self.tempBottomRightRect = self.rect.bottomright 
                    if self.image == self.playerRight1:
                        self.image = self.playerRight2
                    else:
                        self.image = self.playerRight1
                    self.rect = self.image.get_rect()
                    self.rect.bottomright = self.tempBottomRightRect   
                self.imageChangeCounter = 0
            else:
                self.imageChangeCounter += 1
        elif self.stage == 2 and self.dy != 0:
            if self.imageChangeCounter > 1:
                if self.directionFacing == 1:
                    if self.image == self.playerLeft1:
                        self.image = self.playerLeft2
                    else:
                        self.image = self.playerLeft1
                else:
                    self.tempBottomRightRect = self.rect.bottomright 
                    if self.image == self.playerRight1:
                        self.image = self.playerRight2
                    else:
                        self.image = self.playerRight1
                    self.rect = self.image.get_rect()
                    self.rect.bottomright = self.tempBottomRightRect  
                self.imageChangeCounter = 0
            else:
                self.imageChangeCounter += 1
        else:
            if self.image != self.playerLeftCrouched and self.image != self.playerRightCrouched:
                if self.directionFacing == 1:
                    self.image = self.playerLeft1
                else:
                    self.image = self.playerRight1
            self.imageChangeCounter += 1        
            
            
class Portal(pygame.sprite.Sprite):
    '''This class defines the portal sprite that will spawn and hide the player as well as transport them to the next stage.'''
    def __init__(self, stage, location):
        '''This initializer takes the stage and location as parameters. The portal will be spawned at the specified location and be invisible in the first stage'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # Load Portal images
        self.openPortal = pygame.image.load("myImages/openPortal.PNG").convert()
        self.closedPortal = pygame.image.load("myImages/closedPortal.PNG").convert()
        
        # Set appropriate image
        if stage == 1:
            self.image = pygame.Surface((20, 35))
            self.image.fill((0, 0, 0))
            self.image.set_colorkey((0,0,0))
        else:
            self.image = self.openPortal
         
        # Spawn Portal in the specified location
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.bottom = location
        
    def toggleImage(self):
        '''This method swaps the current Portal image witht he other one.'''
        if self.image == self.openPortal:
            self.image = self.closedPortal
        else:
            self.image = self.openPortal
        
        
class Fireball(pygame.sprite.Sprite):
    '''This class defines the Fireball sprite that can kill the player.'''
    def __init__(self, stage, direction, level):
        '''This initializer takes the stage, direction, and level as parameters. The appropriate image will be loaded based on the stage and the direction and speed will be calculated.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # Load Fireball Images
        self.sideFireball1 = pygame.image.load("myImages/sideFireball1.PNG").convert()
        self.sideFireball2 = pygame.image.load("myImages/sideFireball2.PNG").convert() 
        self.upFireball1 = pygame.image.load("myImages/upFireball1.PNG").convert()   
        self.upFireball2 = pygame.image.load("myImages/upFireball2.PNG").convert()   
        
        # Set appropriate image
        if stage == 1:
            self.image = self.sideFireball1
        else:
            self.image = self.upFireball1
        
        # Spawn Fireball in the specified location 
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.bottom = direction[0]
        
        # Calculate x and y vectors
        if stage == 1:
            if direction[0][1] == direction[1][1] == 305:
                self.dx = ((direction[1][0] - direction[0][0]) / 70) + level
                self.dy = ((direction[1][1] - direction[0][1]) / 70)
            else:
                self.dx = ((direction[1][0] - direction[0][0]) / 30) + level
                self.dy = ((direction[1][1] - direction[0][1]) / 30)  
        else:
            self.dx = 0
            self.dy = -7 - level
        
        # Instance Variables
        self.imageChangeCounter = 0
        self.stage = stage
        self.endLocation = direction[1]
        
    def update(self):
        '''This method will be called automatically to reposition the Fireball sprite on the screen and cycle between the Fireball images.'''
        # Change image location
        self.rect.left += self.dx
        self.rect.top += self.dy
        
        # Kill Fireball if it has reached the end of it's path
        if self.stage == 1:
            if self.rect.left >= self.endLocation[0]:
                self.kill()
        else:
            if self.rect.top <= self.endLocation[1]:
                self.kill()
        
        # Cycle between images 
        if self.imageChangeCounter > 1:
            if self.stage == 1:
                if self.image == self.sideFireball1:
                    self.image = self.sideFireball2
                else:
                    self.image = self.sideFireball1
            else:
                if self.image == self.upFireball1: 
                    self.image = self.upFireball2
                else:
                    self.image = self.upFireball1
            self.imageChangeCounter = 0
        else:
            self.imageChangeCounter += 1
            
            
class Dragon(pygame.sprite.Sprite):
    '''This class defines the Dragon sprite that will move horizontally at the bottom of the screen and can shoot Fireballs.'''
    def __init__(self, screen, level):
        '''This initializer takes the screen surface and level as parameters. The Dragon will be spawned at the bottom of the screen with a speed that increases with level.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # Load Dragon Images
        self.dragonLeft1 = pygame.image.load("myImages/dragonLeft1.PNG").convert()
        self.dragonLeft2 = pygame.image.load("myImages/dragonLeft2.PNG").convert()
        self.dragonLeft3 = pygame.image.load("myImages/dragonLeft3.PNG").convert()
        self.dragonRight1 = pygame.image.load("myImages/dragonRight1.PNG").convert()
        self.dragonRight2 = pygame.image.load("myImages/dragonRight2.PNG").convert()
        self.dragonRight3 = pygame.image.load("myImages/dragonRight3.PNG").convert()
        self.dragonLeftShoot = pygame.image.load("myImages/dragonLeftShoot.PNG").convert()
        self.dragonRightShoot = pygame.image.load("myImages/dragonRightShoot.PNG").convert()
        
        # Set initial image
        self.image = self.dragonRight1
        
        # Spawn the dragon on the bottom of the screen
        self.rect = self.image.get_rect()
        self.rect.left = 100
        self.rect.bottom = 424
        
        # Set the initial x vector
        self.dx = 10 + level
        
        # Instance variables
        self.window = screen
        self.imageCounter = 1
        self.directionFacing = 0
        self.imageChangeCounter = 0
        self.fireballCooldown = 0
        self.shooting = False
        self.shootChangeCounter = 0
        
    def setShooting(self):
        '''This method set the shooting instance variable to True.'''
        self.shooting = True
                
    def update(self):
        '''This method will be called automatically to reposition the Dragon sprite on the screen and cycle between Dragon images.'''
        # Move the Dragon
        self.rect.left += self.dx
        
        # If the Dragon has reached the sides of the screen, reverse its direction
        if self.rect.left <= 0:
            self.dx = -self.dx
            self.directionFacing = 0
        elif self.rect.right >= self.window.get_width():
            self.dx = -self.dx
            self.directionFacing = 1
        
        # Cycle between walking and shooting images when appropriate
        if self.shooting == False:
            if self.imageChangeCounter > 2:
                if self.directionFacing == 1:
                    if self.imageCounter == 1:
                        self.image = self.dragonLeft2
                    elif self.imageCounter == 2:
                        self.image = self.dragonLeft3
                    else:
                        self.image = self.dragonLeft1            
                else:
                    if self.imageCounter == 1:
                        self.image = self.dragonRight2
                    elif self.imageCounter == 2:
                        self.image = self.dragonRight3
                    else:
                        self.image = self.dragonRight1
                self.imageChangeCounter = 0
            else:
                self.imageChangeCounter += 1
            self.imageCounter += 1
            if self.imageCounter > 3: 
                self.imageCounter = 1
        else:
            if self.directionFacing == 1:
                self.image = self.dragonLeftShoot
            else:
                self.image = self.dragonRightShoot
            if self.shootChangeCounter == 5:
                self.shooting = False
                self.imageCounter = 1
                self.shootChangeCounter = 0
            else:
                self.shootChangeCounter += 1
            
        
class Treasure(pygame.sprite.Sprite):
    '''This class defines the Treasure sprite that spawns in random location with a random image and value.'''
    def __init__(self, previousTreasures):
        '''This initializer takes a list of previous treasures as a parameter. The location, image, and value will be picked at random until it has a its own unique location not shared by any previous treasures.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # Set random image
        self.value = random.randrange(10, 60, 10)
        self.image = pygame.image.load("myImages/treasure%d.PNG" % (self.value/10)).convert()
        
        # Set random initial location
        self.rect = self.image.get_rect()
        self.rect.bottom = random.randrange(50, 370)
        self.rect.left = random.randrange(10, 500)
        
        # Check if the chosen location is already occupied
        while pygame.sprite.spritecollide(self, previousTreasures, False):
            self.rect.bottom = random.randrange(50, 370)
            self.rect.left = random.randrange(10, 500)   
            
    def move(self):
        '''This method moves the treasure off the screen so the player can't collide with it anymore.'''
        self.rect.bottom = 500
        
        
class ScoreKeeper(pygame.sprite.Sprite):
    '''This class defines the scoreKeeper sprite that records and displays the player's current or highscore.'''
    def __init__(self, highScore, score):
        '''This initializer takes the score and highscore as parameters and loads the custom font "Pixelated" to display it on the screen.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
 
        # Load the custom font
        self.font = pygame.font.Font("Pixelated.ttf", 30)
        
        # Instance variables
        self.score = score
        self.highScore = highScore
 
    def addScore(self, score):
        '''This method adds the appropritate amount to the player's score.'''
        self.score += score
     
    def update(self):
        '''This method will be called automatically to display the current or highscore at the bottom of the screen.'''
        # Adjust the message depending on whether it is a current or highscore being displayed
        if self.highScore == True:
            message = "High Score: %d" % self.score
            self.image = self.font.render(message, 1, (255, 255, 255))
            self.rect = self.image.get_rect()
            self.rect.center = (150, 451)
        else:
            message = "Score: %d" % self.score
            self.image = self.font.render(message, 1, (255, 255, 255))
            self.rect = self.image.get_rect()
            self.rect.center = (500, 451)            
        
        
class Life(pygame.sprite.Sprite):
    '''This class defines the Life sprite that keeps track of and displays the amount of lives remaining.'''
    def __init__(self, livesRemaining):
        '''This initializer takes the amount of lives remaining and displays the correct amount of lives on the bottom of the screen.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # Set the Life image
        self.image = pygame.image.load("myImages/playerLife.png").convert()
        
        # Spawn the lives at the bottom of the screen
        self.rect = self.image.get_rect()
        self.rect.left = 198 + 30 * livesRemaining
        self.rect.bottom = 477