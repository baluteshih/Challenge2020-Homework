import pygame as pg

from EventManager import *
from Model import GameEngine
import Const


class GraphicalView:
    '''
    Draws the state of GameEngine onto the screen.
    '''
    background = pg.Surface(Const.ARENA_SIZE)

    def __init__(self, ev_manager: EventManager, model: GameEngine):
        '''
        This function is called when the GraphicalView is created.
        For more specific objects related to a game instance
            , they should be initialized in GraphicalView.initialize()
        '''
        self.ev_manager = ev_manager
        ev_manager.register_listener(self)

        self.model = model

        self.screen = pg.display.set_mode(Const.WINDOW_SIZE)
        pg.display.set_caption(Const.WINDOW_CAPTION)
        self.background.fill(Const.BACKGROUND_COLOR)

        self.winner = -1

    def initialize(self):
        '''
        This method is called when a new game is instantiated.
        '''
        pass

    def notify(self, event):
        '''
        Called by EventManager when a event occurs.
        '''
        if isinstance(event, EventInitialize):
            self.initialize()

        elif isinstance(event, EventEveryTick):
            self.display_fps()

            cur_state = self.model.state_machine.peek()
            if cur_state == Const.STATE_MENU: self.render_menu()
            elif cur_state == Const.STATE_PLAY: self.render_play()
            elif cur_state == Const.STATE_STOP: self.render_stop()
            elif cur_state == Const.STATE_ENDGAME: self.render_endgame()

        elif isinstance(event, EventWin):
            self.winner = event.winner

    def display_fps(self):
        '''
        Display the current fps on the window caption.
        '''
        pg.display.set_caption(f'{Const.WINDOW_CAPTION} - FPS: {self.model.clock.get_fps():.2f}')

    def render_menu(self):
        # draw background
        self.screen.fill(Const.BACKGROUND_COLOR)

        # draw text
        font = pg.font.Font(None, 36)
        text_surface = font.render("Press [space] to start ...", 1, pg.Color('gray88'))
        text_center = (Const.ARENA_SIZE[0] / 2, Const.ARENA_SIZE[1] / 2)
        self.screen.blit(text_surface, text_surface.get_rect(center=text_center))

        pg.display.flip()

    def render_play(self):
        # draw background
        self.screen.fill(Const.BACKGROUND_COLOR)

        # draw players
        for player in self.model.players:
            center = list(map(int, player.position))
            pg.draw.circle(self.screen, Const.PLAYER_COLOR[player.player_id], center, Const.PLAYER_RADIUS)

        # draw attacker
        font = pg.font.Font(None, 36)
        text_surface = font.render("Attacker: Player " + str(int(self.model.players[1].attacker == 1)), 1, pg.Color('gray88'))
        text_center = (105, 15)
        self.screen.blit(text_surface, text_surface.get_rect(center=text_center))

        # draw timer
        font = pg.font.Font(None, 36)
        text_surface = font.render("Remain time: " + str(int(self.model.timer // Const.FPS)), 1, pg.Color('gray88'))
        text_center = (695, 15)
        self.screen.blit(text_surface, text_surface.get_rect(center=text_center))

        pg.display.flip()

    def render_stop(self):
        self.screen.fill(Const.BACKGROUND_COLOR)
        
        font = pg.font.Font(None, 50)
        text_surface = font.render("STOP!!!! Press [space] to continue...", 1, pg.Color('gray88'))
        text_center = (Const.ARENA_SIZE[0] / 2, Const.ARENA_SIZE[1] / 2)
        self.screen.blit(text_surface, text_surface.get_rect(center=text_center))

        pg.display.flip()

    def render_endgame(self):
        # draw background
        self.screen.fill(Const.BACKGROUND_COLOR)
        
        font = pg.font.Font(None, 36)
        if self.winner != -1:
            text_surface = font.render("Player " + str(self.winner) + " win!", 1, pg.Color('gray88'))
        else:
            text_surface = font.render("Time up QQ", 1, pg.Color('gray88'))
        text_center = (Const.ARENA_SIZE[0] / 2, Const.ARENA_SIZE[1] / 2)
        self.screen.blit(text_surface, text_surface.get_rect(center=text_center))

        pg.display.flip()
