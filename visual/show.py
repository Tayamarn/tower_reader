"""
 Pygame base template for opening a window

 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/

 Explanation video: http://youtu.be/vRB_983kUMc
"""
import os
import sys
import traceback

import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 153, 0)
YELLOW = (255, 239, 0)
DARK_GREEN = (0, 204, 0)
RED = (255, 0, 0)
MKVTCH_STRING = u' \u043c\u043a\u0412\u0442\u00b7\u0447'

# LABEL_COLOR = (255, 60, 0)
LABEL_COLOR = (0x1b, 0x1b, 0xb3)

DATA_FILE = os.path.join(os.path.dirname(__file__), 'config')
LOG_FILE = os.path.join(os.path.dirname(__file__), 'show.log')

BATTERY_TEN_PERCENT = 79

def real_val_to_battery_coord(val):
    if val <= 0:
        return 0
    elif val <= 1:
        return int(val * BATTERY_TEN_PERCENT)
    elif val <= 10:
        return int((val - 1) / 9 * BATTERY_TEN_PERCENT * 2) + BATTERY_TEN_PERCENT
    elif val <= 40:
        return int((val - 10) / 30 * BATTERY_TEN_PERCENT * 2) + BATTERY_TEN_PERCENT * 3
    elif val <= 100:
        return int((val - 40) / 60 * BATTERY_TEN_PERCENT * 2) + BATTERY_TEN_PERCENT * 5
    else:
        return int((val - 100) / 150 * BATTERY_TEN_PERCENT * 3) + BATTERY_TEN_PERCENT * 7


def paint_battery(screen, val):
    if val == 0:
        return
    if val > 850:
        val = 850
    start_x, start_y = 305, 105
    y_stop = 390
    pygame.draw.rect(screen, DARK_GREEN, [start_x, start_y, min(val, 10 * BATTERY_TEN_PERCENT), y_stop])
    if val > 10 * BATTERY_TEN_PERCENT:
        pygame.draw.rect(screen, DARK_GREEN, [start_x, 185, min(val, 850), 230])
    pygame.draw.rect(screen, GREEN, [start_x, start_y, min(val, 7 * BATTERY_TEN_PERCENT), y_stop])
    pygame.draw.rect(screen, YELLOW, [start_x, start_y, min(val, 5 * BATTERY_TEN_PERCENT), y_stop])
    pygame.draw.rect(screen, ORANGE, [start_x, start_y, min(val, 3 * BATTERY_TEN_PERCENT), y_stop])
    pygame.draw.rect(screen, RED, [start_x, start_y, min(val, BATTERY_TEN_PERCENT), y_stop])


def main():
    try:
        pygame.init()

        # Set the width and height of the screen [width, height]
        screen_size = (1400, 700)
        screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)

        pygame.display.set_caption("STEM-games")

        # Loop until the user clicks the close button.
        done = False

        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()
        # font = pygame.font.SysFont('Arial', 60)
        font = pygame.font.Font(None, 60)

        # -------- Main Program Loop -----------
        while not done:
            # --- Main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    if pygame.key.get_pressed()[310] and pygame.key.get_pressed()[pygame.K_w]:
                        done = True
                # elif event.type == pygame.KEYUP:
                #     print("User let go of a key.")
                # elif event.type == pygame.MOUSEBUTTONDOWN:
                #     print("User pressed a mouse button")

            # --- Game logic should go here

            # --- Screen-clearing code goes here

            # Here, we clear the screen to white. Don't put other drawing commands
            # above this, or they will be erased with this command.
            try:
                with open(DATA_FILE, 'r') as f:
                    lines = map(lambda x: x.strip(), f.readlines())
                    # print(lines[0])
                    # print(unicode(lines[0]))
                    if 'fi' in lines:
                        return
                    if len(lines) != 2:
                        pass
                    team_name, val = lines
                    val = float(val)
                    team_name = team_name.decode('utf8')
            except ValueError as e:
                print(e)
                pass

            # If you want a background image, replace this clear with blit'ing the
            # background image.
            screen.fill(WHITE)
            label = font.render(team_name, 1, LABEL_COLOR)
            label2 = font.render(str(round(float(val), 1)) + MKVTCH_STRING, 1, LABEL_COLOR)
            screen.blit(label, (screen_size[0] / 2 - label.get_width() / 2, 50))
            screen.blit(label2, (screen_size[0] / 2 - label2.get_width() / 2, 520))

            # --- Drawing code should go here
            pygame.draw.rect(screen, BLACK, [300, 100, 800, 400])
            pygame.draw.rect(screen, BLACK, [1100, 180, 60, 240])
            pygame.draw.rect(screen, WHITE, [305, 105, 790, 390])
            pygame.draw.rect(screen, WHITE, [1095, 185, 60, 230])

            paint_battery(screen, real_val_to_battery_coord(val))

            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            # --- Limit to 60 frames per second
            clock.tick(60)
    except Exception as e:
        with open(LOG_FILE, 'a') as log:
            log.write(str(sys.exc_info()) + '\n' + traceback.print_exc() + '\n\n')
        print(e)
    finally:
        # Close the window and quit.
        pygame.quit()

if __name__ == '__main__':
    main()
