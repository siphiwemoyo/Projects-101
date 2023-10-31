import colorsys
import random
import pygame
import math
import cv2

#define blob class

class Blob:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.r = random.randint(1000,2000) # increase the size of the blobs
        self.xspeed = random.uniform(-30,30) #increases the speed of the blobs
        self.yspeed = random.uniform(-30,30) #increases the speed of the blobs

    def update(self):
        self.x += self.xspeed
        self.y += self.yspeed
        if self.x > width or self.x < 0:
            self.xspeed *= -1
        if self.y > height or self.y < 0:
            self.yspeed *= -1

# Initialize Pygame
pygame.init()

# Set the dimensions of the canvas
width, height = 500, 1000
screen = pygame.display.set_mode((width, height))

# Create a list to store blobs
blobs = [Blob(random.uniform(0, width), random.uniform(0, height)) for _ in range(10)]

# Define the video recording settings
frame_rate = 60       # Adjust as needed
frame_size = (200, 200)         # Use the dimensions of your canvas

# Initialize the video recording
pygame.display.set_caption("Blob Animation")  # Set a window title
recording = False
recording_filename = "/Users/siphiwe/Downloads/blobanimation.mp4"  # Set the filename and extension
recording_start_frame = 0
recording_end_frame = 600  # Set the number of frames to record

# Create a video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use the appropriate codec
video_writer = cv2.VideoWriter(recording_filename, fourcc, frame_rate, frame_size)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not recording and pygame.mouse.get_pressed()[0]:
            recording = True
        if recording:
           if recording_start_frame <= pygame.time.get_ticks() // 1000 <= recording_end_frame:
               frame = pygame.surfarray.array3d(screen)
               frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
               video_writer.write(frame)
        if pygame.time.get_ticks() // 1000 > recording_end_frame:
            recording = False
            video_writer.release()
            pygame.quit()
        else:
            pygame.display.flip()

    screen.fill((51, 51, 51))

    for x in range(width):
        for y in range(height):
            pixel_sum = 0
            for blob in blobs:
                xdif = x - blob.x
                ydif = y - blob.y
                d = math.sqrt(xdif * xdif + ydif * ydif)
                pixel_sum += 10 * blob.r / d
            
            # Convert HSB color to RGB
            r, g, b = colorsys.hsv_to_rgb(pixel_sum / 360, 1, 1)
            r, g, b = int(r * 255), int(g * 255), int(b * 255)

            pygame.draw.rect(screen, (r, g, b), (x, y, 1, 1))

    for blob in blobs:
        blob.update()

    pygame.display.flip()

# Quit Pygame
pygame.quit()

