import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Self Driving Car AI")

clock = pygame.time.Clock()

# car coordinates
x = 375
y = 287.5

running = True
while running:

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        x += 3

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False


    screen.fill((255, 255, 255))

    # car represented by a rectangle
    pygame.draw.rect(screen, "red", [x, y, 50, 25], 0)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
