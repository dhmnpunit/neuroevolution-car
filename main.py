import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Self Driving Car AI")

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    screen.fill((255, 255, 255))

    pygame.draw.rect(screen, "red", [200, 200, 50, 25], 0)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
