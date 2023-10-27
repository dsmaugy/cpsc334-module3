import pygame
import socket
import select

PREV_AUDIO = "bingus.wav"

pygame.init()

screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h
# screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

screen_width = 1024
screen_height = 512
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jungle Lab")


pygame.mixer.init()

clock = pygame.time.Clock()
running = True

# Wireless initialization
ESP32_ADDR = ("192.168.0.137", 6101)
HOST_ADDR = ("0.0.0.0", 6100)
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(HOST_ADDR)
udp_socket.setblocking(False)

class Button:
    def __init__(self, x, y, width, height, text, callback, color=(0, 128, 255), text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.Font(None, 36)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def invoke_callback(self):
        self.callback()

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)

current_sound = pygame.mixer.Sound(PREV_AUDIO)
def play_prev_sound():
    if not pygame.mixer.get_busy():
        current_sound = pygame.mixer.Sound(PREV_AUDIO)
        current_sound.play()

def record_new():
    if pygame.mixer.get_busy():
        pygame.mixer.stop()

    udp_socket.sendto("R".encode(), ESP32_ADDR)

    
prev_button = Button(200, 200, 200, 50, "Listen to Previous", play_prev_sound)
record_button = Button(600, 200, 200, 50, "Record New", record_new)
title_text = "Jungle Player"

clickable_elements = [prev_button, record_button]


def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

while running:
    readable, _, _ = select.select([udp_socket], [], [], 0.1)

    just_finished_new_recording = False
    for sock in readable:
         data, _ = sock.recvfrom(1024)
         if data.decode("utf-8") == "DONE":
             just_finished_new_recording = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                for elem in clickable_elements:
                    if elem.is_clicked(event.pos):
                        elem.invoke_callback()
                        break
        elif event.type == pygame.MOUSEMOTION:
            is_hovered = False
            for elem in clickable_elements:
                if elem.is_hovered(event.pos):
                    is_hovered = True
                    break
            cursor = pygame.SYSTEM_CURSOR_HAND if is_hovered else pygame.SYSTEM_CURSOR_ARROW
            pygame.mouse.set_cursor(cursor)

    screen.fill("purple")

    # Define font and text content
    font = pygame.font.Font("fonts/jungle_monkey.ttf", 36)

    # Draw the text element on the screen
    draw_text(title_text, font, (0, 0, 0), 100, 100)
    prev_button.draw()
    record_button.draw()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
udp_socket.close()