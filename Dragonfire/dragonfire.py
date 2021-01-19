''' Author: Gavin Tse 

    Date: May 28, 2019 
    
    Description: The game logic for the Dragonfire game.
'''

# I - Import and Initialize
import pygame, mySprites
pygame.init()
pygame.mixer.init()

 
def stageOne(screen, score, highScore, lives, level):
    '''This function defines the first stage in the Dragonfire game.'''
    
    # E - Entities
    background = pygame.image.load("myImages/backgroundStage1.jpg").convert()
    screen.blit(background, (0, 0))
    
    # Sound Effects
    death = pygame.mixer.Sound("soundEffects/death.ogg")
    fireballShooting = pygame.mixer.Sound("soundEffects/fireball.ogg")
    
    # Sprites
    startPortal = mySprites.Portal(1, (599, 312))
    
    endPortal = mySprites.Portal(1, (28, 312))
    
    player = mySprites.Player(screen, 1, (startPortal.rect.left, startPortal.rect.bottom))
    
    scoreKeeper = mySprites.ScoreKeeper(False, score)
    
    highScoreKeeper = mySprites.ScoreKeeper(True, highScore)
    
    playerLives = []
    for number in range(1, lives + 1):
        life = mySprites.Life(number)
        playerLives.append(life)    
    
    # Sprite groups
    fireballGroup = pygame.sprite.Group()
    allSprites = pygame.sprite.OrderedUpdates(scoreKeeper, highScoreKeeper, playerLives, startPortal, endPortal, player)
     
    # A - Action (broken into ALTER steps)
     
    # A - Assign values
    clock = pygame.time.Clock()
    keepGoing = True
    endGame = False
    topFireballCounter = 30
    bottomFireballCounter = 80
    livesRemaining = lives
    
    # L - Loop
    while keepGoing:
     
        # T - Timer
        clock.tick(30)
     
        # E - Event handling
        keysPressed = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                endGame = True
                keepGoing = False
            # Movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    if player not in allSprites:
                        allSprites.add(player)
                        player.reset((startPortal.rect.left, startPortal.rect.bottom))
                    player.changeDirection((-8 - level, 0), 1)
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    player.changeDirection((8 + level, 0), 1)
                if event.key == pygame.K_w or event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    player.jump()
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    player.toggleCrouch()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    player.toggleCrouch()
                    if keysPressed[pygame.K_a] or keysPressed[pygame.K_LEFT]:  
                        player.changeDirection((-8 - level, 0), 1)
                    if keysPressed[pygame.K_d] or keysPressed[pygame.K_RIGHT]:
                        player.changeDirection((8 + level, 0), 1)                     
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    if player.directionFacing == 1:
                        player.changeDirection((0, 0), 1)  
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT: 
                    if player.directionFacing == 0:
                        player.changeDirection((0, 0), 1) 
        
        # Spawn top fireball   
        if topFireballCounter >= 60 - level:
            topFireball = mySprites.Fireball(1, ((endPortal.rect.right, 280), (550, 280)), level)
            allSprites.add(topFireball)
            fireballGroup.add(topFireball)
            topFireballCounter = 0
            fireballShooting.play()
        else:
            topFireballCounter += 1
        
        # Spawn bottom fireball   
        if bottomFireballCounter >= 110 - level:
            bottomFireball = mySprites.Fireball(1, ((endPortal.rect.right, 305), (550, 305)), level)
            allSprites.add(bottomFireball)
            fireballGroup.add(bottomFireball)
            bottomFireballCounter = 0
            fireballShooting.play()
        else:
            bottomFireballCounter += 1
        
        # Check if the player has been killed by a fireball  
        collisions = pygame.sprite.spritecollide(player, fireballGroup, False)
        for fireball in collisions:
            fireball.kill()
            player.reset((startPortal.rect.left, startPortal.rect.bottom))
            livesRemaining -= 1
            allSprites.remove(playerLives[livesRemaining])
            allSprites.clear(screen, background)
            allSprites.update()
            allSprites.draw(screen)
            death.play()
        
        # Hide the player if they touch the spawn portal   
        if player in allSprites:
            if player.rect.right >= startPortal.rect.left:
                allSprites.remove(player)
                player.rect.top = 0
        
        # Transport the player to second stage if the player touches the end portal    
        if player.rect.left <= endPortal.rect.right:
            keepGoing = False
        
        # Check if player has died    
        if livesRemaining == 0:
            endGame = True
            keepGoing = False

        # R - Refresh display
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()
    
    # Return variables
    return endGame, scoreKeeper.score, livesRemaining  
          
 
 
def stageTwo(screen, score, highScore, lives, level):
    '''This function defines the second stage in the Dragonfire game.'''
    # E - Entities
    background = pygame.image.load("myImages/backgroundStage2.PNG").convert()
    screen.blit(background, (0, 0))
    
    # Sound Effects
    death = pygame.mixer.Sound("soundEffects/death.ogg")
    fireballShooting = pygame.mixer.Sound("soundEffects/fireball.ogg")
    collectTreasure = pygame.mixer.Sound("soundEffects/ding.ogg")
    
    # Sprites
    startPortal = mySprites.Portal(2, (560, 270))
    
    player = mySprites.Player(screen, 2, (startPortal.rect.left, startPortal.rect.bottom))
    
    dragon = mySprites.Dragon(screen, level)
    
    scoreKeeper = mySprites.ScoreKeeper(False, score)
    
    highScoreKeeper = mySprites.ScoreKeeper(True, highScore)
    
    playerLives = []
    for number in range(1, lives + 1):
        life = mySprites.Life(number)
        playerLives.append(life)
    
    treasures = []
    for i in range(10):
        treasure = mySprites.Treasure(treasures)
        treasures.append(treasure)
    
    # Sprite groups
    treasureGroup = pygame.sprite.OrderedUpdates(treasures)  
    fireballGroup = pygame.sprite.Group()
    allSprites = pygame.sprite.OrderedUpdates(scoreKeeper, highScoreKeeper, playerLives, startPortal, dragon, treasures, player)
    
    # A - Action (broken into ALTER steps)
     
    # A - Assign values
    clock = pygame.time.Clock()
    keepGoing = True
    endGame = False
    livesRemaining = lives
    visibleEndPortal = False
    treasuresRemaining = 10
    fireballCooldown = 0
     
    # L - Loop
    while keepGoing:
     
        # T - Timer
        clock.tick(30)
        
        # E - Event handling
        keysPressed = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                endGame = True
                keepGoing = False 
            # Movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    if player not in allSprites:
                        allSprites.add(player)
                        player.reset((startPortal.rect.left, startPortal.rect.bottom))
                        startPortal.toggleImage()
                    player.changeDirection((-8 - level, 0), 1)
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    player.changeDirection((8 + level, 0), 1)
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    player.changeDirection((0, 8 + level), 0)
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    player.changeDirection((0, -8 - level), 0)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    if keysPressed[pygame.K_d] or keysPressed[pygame.K_RIGHT]:
                        player.changeDirection((8 + level, 0), 1)
                    else:
                        player.changeDirection((0, 0), 1)
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    if keysPressed[pygame.K_a] or keysPressed[pygame.K_LEFT]:
                        player.changeDirection((-8 - level, 0), 1)
                    else:
                        player.changeDirection((0, 0), 1)
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    player.changeDirection((0, 0), 0)
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    player.changeDirection((0, 0), 0)   
        
        # Make the Dragon shoot fireballs if it is close to the Player           
        if player.rect.center[0] > dragon.rect.left and player.rect.center[0] < dragon.rect.right:
            if fireballCooldown == 0:
                if dragon.directionFacing == 0:
                    fireball = mySprites.Fireball(2, ((dragon.rect.center[0] + 30, 380), (dragon.rect.center[0] + 30, 30)), level)
                else:
                    fireball = mySprites.Fireball(2, ((dragon.rect.center[0] - 70, 380), (dragon.rect.center[0] - 70, 30)), level)
                allSprites.add(fireball)
                fireballGroup.add(fireball)
                fireballCooldown = 10 
                dragon.setShooting()
                fireballShooting.play()
        
        # Reduce frequency of fireballs being shot
        if fireballCooldown > 0:
            fireballCooldown -= 1
            
        # Check if the player has been killed by a fireball      
        fireballCollisions = pygame.sprite.spritecollide(player, fireballGroup, False)
        for fireball in fireballCollisions:
            fireball.kill()
            player.reset((startPortal.rect.right, startPortal.rect.bottom))
            livesRemaining -= 1
            allSprites.remove(playerLives[livesRemaining])
            allSprites.clear(screen, background)
            allSprites.update()
            allSprites.draw(screen) 
            death.play()
        
        # Check if player has died    
        if livesRemaining == 0:
            endGame = True
            keepGoing = False        
        
        # Check if the Player has colllected a treasure    
        treasureCollisions = pygame.sprite.spritecollide(player, treasures, False)
        for treasure in treasureCollisions:
            scoreKeeper.addScore(treasure.value) 
            treasure.kill()
            treasure.move()
            treasuresRemaining -= 1
            collectTreasure.play()
        
        # Hide the player if they touch the spawn portal   
        if player in allSprites:
            if player.rect.colliderect(startPortal.rect):
                player.rect.left = 700
                allSprites.remove(player)
                startPortal.toggleImage()
        
        # Spawn the end Portal if all of the treasures have been collected    
        if treasuresRemaining == 0:
            endPortal = mySprites.Portal(2, (40, 80))
            allSprites.add(endPortal)
            visibleEndPortal = True
        
        # Transport the player to first stage if the player touches the end portal    
        if visibleEndPortal == True:
            if player.rect.colliderect(endPortal.rect):
                keepGoing = False
            
        # R - Refresh display
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip() 
    
    # Return variables    
    return endGame, scoreKeeper.score, livesRemaining    
    
    
def main():
    '''This function defines the mainline logic for the Dragonfire game.'''
    # D - Display configuration
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Dragonfire") 
    
    # Backgound Music
    pygame.mixer.music.load("soundEffects/backgroundMusic.ogg")
    pygame.mixer.music.play(-1)     
    
    # Load previous highscore
    highScores = open("highScores.txt", "r")
    highScore = int(highScores.read().strip())
    highScores.close()
    
    # Initilize important variables
    endGame = False
    score = 0
    lives = 7
    level = 0
    levelCounter = 0
    
    # Main game loop
    while not endGame:
        # Occasionally increase difficulty
        if levelCounter == 3:
            level += 1
            levelCounter = 0
        else: levelCounter += 1
        
        endGame, score, lives = stageOne(screen, score, highScore, lives, level)
        if endGame == True:
            break
        endGame, score, lives = stageTwo(screen, score, highScore, lives, level)
    
    # Record new highscore    
    if score > highScore:
        highScores = open("highScores.txt", "w")
        highScores.write(str(score))
        highScores.close() 
        
    # Fadeout music
    pygame.mixer.music.fadeout(2000)
    pygame.time.delay(2000)    
       
    # Close the game window 
    pygame.quit()  
    
    
# Call the main function
main()