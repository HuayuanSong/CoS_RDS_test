import pygame
import random

# Initialize PyGame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Screen dimensions
WIDTH, HEIGHT = 1024, 768

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Reliable Digit Span Test")
font = pygame.font.SysFont(None, 55)
input_font = pygame.font.SysFont(None, 40)

def show_message(message):
    text = font.render(message, True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.fill(WHITE)
    screen.blit(text, text_rect)
    pygame.display.flip()

def run_test(forward=True):
    sequence_length = 2
    attempts = 0
    score = 0
    
    while attempts < 2:
        sequence = [str(random.randint(0, 9)) for _ in range(sequence_length)]
        for digit in sequence:
            show_message(digit)
            pygame.time.wait(1000)

        input_sequence = ""
        prompt = "Input forwards:" if forward else "Input backwards:"
        show_message(prompt)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return 0
                if event.type == pygame.KEYDOWN:
                    if event.unicode.isdigit():
                        input_sequence += event.unicode
                        show_message(prompt + " " + input_sequence)
                    if event.key == pygame.K_RETURN:
                        if not forward:
                            sequence = sequence[::-1]
                        if input_sequence == ''.join(sequence):
                            score += 1
                            if score > 1:
                                score = 1
                        attempts += 1
                        if attempts == 2:
                            if score > 0:
                                sequence_length += 1
                                score = 0
                                attempts = 0
                            else:
                                return sequence_length - 1
                        running = False
                        
    return sequence_length - 1

def main():
    data_file_num = ""
    show_message("Enter data file number:")
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.unicode.isdigit():
                    data_file_num += event.unicode
                    show_message("Enter data file number: " + data_file_num)
                if event.key == pygame.K_RETURN and data_file_num:
                    forward_score = run_test(forward=True)
                    backward_score = run_test(forward=False)
                    total_score = forward_score + backward_score
                    show_message(f"Your score is {total_score}.")
                    with open(f"data_{data_file_num}.txt", "w") as f:
                        f.write(f"Score: {total_score}\n")
                    pygame.time.wait(3000)
                    running = False

if __name__ == "__main__":
    main()
