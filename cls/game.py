import pygame
import extra_files.game_constants as game_constants


class Game:
    def __init__(self, screen: pygame.Surface, states: dict, start_state: str)-> None:
        """__init__ constructor"""
        self.screen = screen
        self.states = states
        self.state_name = start_state

        self.done = False
        self.clock = pygame.time.Clock()
        self.fps = game_constants.FPS
        self.state = self.states.get(self.state_name, None)

    def event_loop(self)-> None:
        """This function handles the game event loop"""
        for event in pygame.event.get():
            self.state.get_event(event)

    def flip_state(self)-> None:
        """This function flips the state assumed on the game"""
        current_state = self.state_name
        next_state = self.state.next_state
        self.state.done = False
        self.state_name = next_state
        persistent = self.state.persist
        self.state = self.states.get(self.state_name, None)
        self.state.startup(persistent)

    def update(self, dt: int)-> None:
        """This function updates.."""
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(dt)

    def draw(self)-> None:
        """This function draws.."""
        self.state.draw(self.screen)

    def run(self)-> None:
        """This function runs the game"""
        while not self.done:
            dt = self.clock.tick(self.fps * 2 if self.state_name == "SPLASH" else self.fps)
            self.event_loop()

            if self.state_name == "GAMEPLAY":
                self.state.handle_paddle_movement()
                self.state.ball.move()
                self.state.handle_collision()
                self.state.score_handling()
                self.state.winner_handling()

            self.update(dt)
            self.draw()
            pygame.display.update()