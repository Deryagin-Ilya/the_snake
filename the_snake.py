"""random module."""
from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Basic class for objects."""

    def __init__(self=None):
        """Initialize basic atributes for GameObject."""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Abstract method used later."""
        pass


class Apple(GameObject):
    """Describe apple and actions with it."""

    def __init__(self):
        """Apply color of an apple, call randomize_position."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Set apple's random position on a grid."""
        self.position = (randint(0, SCREEN_WIDTH * GRID_SIZE),
                         randint(0, SCREEN_HEIGHT * GRID_SIZE))

    def draw(self):
        """Draw apple on a grid."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Describe snake and its actions."""

    def __init__(self):
        """Initialize snake's initial state."""
        super().__init__()
        self.body_color = (0, 255, 0)
        self.length = 1
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]

    def update_direction(self):
        """Update snake's moving direction."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Return snake head position (first element in positions)."""
        return self.positions[0]

    def move(self):
        """Make a new snake's position by adding a new head in positions list.

        If snake didn't enlarged, remove the last element.
        """
        self.get_head_position()
        new_head = (self.positions[0][0] + self.direction[0] * GRID_SIZE,
                    self.positions[0][1] + self.direction[1] * GRID_SIZE)
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Draw snake on a screen, removing trace."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Reset snake in initial state."""
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.length = 1
        self.direction = RIGHT


def handle_keys(game_object):
    """Process key pressing to change snake's direction."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Initialize main code of the game."""
    # Инициализация PyGame:
    pygame.init()

    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        head_position = snake.get_head_position()
        if head_position in snake.positions[1:]:
            snake.reset()
        snake.draw()
        apple.draw()
        pygame.display.update()
        # Тут опишите основную логику игры.


if __name__ == '__main__':
    main()
