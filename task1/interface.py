from pythonosc import udp_client

import pygame
import socket
import select

PREV_AUDIO = "produced_sound.wav"
FULLSCREEN = False

pygame.init()

if FULLSCREEN:
    screen_info = pygame.display.Info()
    WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h
    screen_flags = pygame.FULLSCREEN
else:
    WIDTH = 1024
    HEIGHT = 512
    screen_flags = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT), screen_flags)
pygame.display.set_caption("Jungle Lab")


pygame.mixer.init()

clock = pygame.time.Clock()
running = True

# Wireless initialization
# ESP32_ADDR = ("192.168.0.137", 6101)
ESP32_ADDR = ("192.168.0.228", 6101)
HOST_ADDR = ("0.0.0.0", 6100)
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(HOST_ADDR)
udp_socket.setblocking(False)

osc_client = udp_client.SimpleUDPClient("127.0.0.1", 57120)


class Button:
    def __init__(self, x, y, width, height, text, callback, color=(1, 129, 129), text_color=(255, 255, 255), alt_text=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.Font(None, 36)
        self.alt_text = alt_text

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

description_text = ""

def record_new():
    global description_text
    if pygame.mixer.get_busy():
        pygame.mixer.stop()
    
    description_text = "Recording..."
    udp_socket.sendto("R".encode(), ESP32_ADDR)
    osc_client.send_message("/start_record", None)
    
prev_button = Button(WIDTH//6, HEIGHT*5//6, 300, 50, "Listen to Previous", play_prev_sound, alt_text="Listen to previously saved soundscape")
record_button = Button((WIDTH*5//6)- 300, HEIGHT*5//6, 300, 50, "Record New", record_new, alt_text="Start recording new soundscape with junglebox")
title_text = "Jungle Lab"
bg_img = pygame.image.load("jungle.jpg")
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

clickable_elements = [prev_button, record_button]

def record_done():
    global description_text
    description_text = "Recording done. Listen to previous or create new one."
    osc_client.send_message("/stop_record", None)

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

def get_text_offset(coords, text, font):
    font_size = font.size(text)
    return (coords[0] - font_size[0]//2 , coords[1] - font_size[1]//2)

while running:
    readable, _, _ = select.select([udp_socket], [], [], 0.1)

    for sock in readable:
         data, _ = sock.recvfrom(1024)
         if data.decode("utf-8") == "D":
             record_done()

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

            if is_hovered:
                cursor = pygame.SYSTEM_CURSOR_HAND 
            else:
                cursor = pygame.SYSTEM_CURSOR_ARROW
    
            pygame.mouse.set_cursor(cursor)

    # screen.fill((1, 129, 129))
    screen.blit(bg_img, (0, 0))

    # Define font and text content
    font = pygame.font.Font("fonts/jungle_monkey.ttf", 36)
    
    # Draw the text element on the screen
    title_text_pos = get_text_offset((WIDTH//2, HEIGHT*2//5), title_text, font)
    description_text_pos = get_text_offset((WIDTH//2, HEIGHT*4//6), description_text, font)
    draw_text(title_text, font, (223, 223, 96), title_text_pos[0], title_text_pos[1])
    draw_text(description_text, font, (192, 192, 192), description_text_pos[0], description_text_pos[1])
    prev_button.draw()
    record_button.draw()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
udp_socket.close()