import random
from typing import Tuple
import numpy as np
import pygame

pygame.init()
SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

w, h = SCREEN.get_size()


class Slider:
    def __init__(self, pos: tuple, name: str, size=(9, 200), max_v=100, min_v=0, init_value=0, text_xo=0, color=WHITE) -> None:
        self.pos = pos
        self.grabber_size = size[0]
        self.value = init_value
        self.size = size
        self.name = name
        self.max_value = max_v
        self.min_value = min_v
        self.text_xo = text_xo
        self.on_focus = 0
        self.color = color
        self.slider_selected = False
        
        yo = self.pos[1]+5
        yf = self.pos[1]+self.size[1]
        self.grabber_pos = [self.pos[0], int(
            (((self.value-(min_v))/(max_v-min_v))*(yo-yf)+yf))]
        self.grabber_body = pygame.Rect(*self.pos, self.size[0], self.size[0])

    def slide_it(self, mouse_pos: tuple):

        if self.grabber_body.collidepoint(mouse_pos) or self.on_focus:
            self.on_focus = 1
        else:
            self.on_focus = 0

        yf = self.pos[1]+self.size[1]
        yo = self.pos[1]+5
        if self.on_focus:
            mouse_y = mouse_pos[1]
            if mouse_y < yo:
                mouse_y = yo
            elif mouse_y > yf:
                mouse_y = yf
            self.grabber_pos[1] = mouse_y
        self.value = (((self.grabber_pos[1]-(yf))/(yo-yf))*(
            self.max_value-self.min_value)+self.min_value)  # temp equality

    def draw(self, screen):
        pygame.draw.line(screen, (100, 100, 100), (
            self.pos[0], self.pos[1]-5), (self.pos[0], self.pos[1]+self.size[1]+10), 3)
        if self.on_focus:
            pygame.draw.circle(screen, self.color,
                               self.grabber_pos, self.grabber_size)
        else:
            pygame.draw.circle(screen, (225, 225, 200),
                               self.grabber_pos, self.grabber_size)

        self.grabber_body = pygame.draw.circle(
            screen, (155, 155, 155), self.grabber_pos, self.grabber_size, 2)

        screen_print(screen, self.name, WHITE,
                     (self.pos[0]-self.text_xo), (self.pos[1]+self.size[1]+15), size=15)
        screen_print(screen, f"{int(self.value): 03d}", WHITE,
                     (self.pos[0]-40), (self.grabber_pos[1]-9), size=15)


class Fish:
    def __init__(self, x: int, y: int, species="Blues", color=YELLOW, size=5) -> None:
        self.vec = pygame.Vector2(
            ((random.choice(np.linspace(-1, 1, 201))), (random.choice(np.linspace(-1, 1, 201)))))
        self.speed = random.choice(np.linspace(1, 10, 20))
        self.vec = pygame.math.Vector2.normalize(self.vec)
        self.body = None
        self.color = color
        self.pos = (x, y)
        self.size = size
        self.species = species

    def draw(self, screen):
        self.body = pygame.draw.polygon(screen, self.color, ((self.pos+pygame.math.Vector2.rotate(self.vec*self.size, 90)),
                                        self.pos+self.vec*self.size*3, (self.pos+pygame.math.Vector2.rotate(self.vec*self.size, -90))))
        
        #self.body = pygame.draw.circle(screen, self.color, self.pos, self.size)

    def debug(self, screen, s_range=100, debug=False, alt_activation=False):
        if debug or alt_activation:
            dbg_vec = (self.vec)*s_range
            for i in range(-1*sight_angle, 0, 2):
                pygame.draw.line(screen, (5, 25, 0), self.pos,
                                 (self.pos+pygame.math.Vector2.rotate(dbg_vec, i)), 5)
            for i in range(0, sight_angle+1, 2):
                pygame.draw.line(screen, (5, 25, 0), self.pos,
                                 (self.pos+pygame.math.Vector2.rotate(dbg_vec, i)), 5)


class Obstacle:
    def __init__(self, size: tuple, pos: tuple, color=RED) -> None:
        self.size = size
        self.bkp_size = size
        self.pos = pos 
        self.center = ((pos[0]+size[0])/2,(pos[1]+size[1])/2)
        self.body = pygame.Rect(pos[0],pos[1], size[0], size[1])
        #self.body = pygame.Surface()
        self.color = color
        self.on_focus = 0
    
    def draw(self, screen):
        self.body = pygame.draw.rect(screen, self.color, (self.pos, self.size))
        self.center = ((self.pos[0]+self.size[0])/2,(self.pos[1]+self.size[1])/2)

    def grab_it(self, mouse_pos, scroll):
        if self.body.collidepoint(mouse_pos) or self.on_focus:
            self.on_focus = 1
        else:
            self.on_focus = 0
        
        scroll -= 5
        if self.on_focus:
            self.pos = (mouse_pos[0]-self.size[0]/2, mouse_pos[1]-self.size[1]/2)
            if scroll:
                self.size = self.bkp_size[0]+scroll, self.bkp_size[1]+scroll
            else:
                self.bkp_size = self.size


def screen_print(screen, text: str, color: tuple, x: int, y: int, size=30, font="Arial"):
    text_font = pygame.font.SysFont(font, size)
    text_body = text_font.render(text, False, color)
    screen.blit(text_body, (x, y))


def draw_world_border(screen, color=RED, draw_it=True):
    if draw_it:
        pygame.draw.polygon(
            screen, color, [(1, 1), (w-1, 1), (w-1, h-1), (1, h-1)], 1)


def move(obj):
    obj.pos = obj.pos + obj.vec*obj.speed


def rotate(obj, dir: str, angle: int):
    if dir == "cw":
        obj.vec = pygame.math.Vector2.rotate(obj.vec, angle)
    elif dir == "ccw":
        obj.vec = pygame.math.Vector2.rotate(obj.vec, -angle)


clock = pygame.time.Clock()
n_bodies = 100

all_Fishs = []
for i in range(n_bodies):
    all_Fishs.append(Fish(random.randint(10, w-10), random.randint(10, h-10),
                     species="Blues", color=YELLOW))  # nome da especie só precisa ser diferente msm
    
choosen = random.choice(range(len(all_Fishs)))

all_obstacles = []

all_sliders = {"s_angle": Slider((w-50, 30), "sight angle", max_v=179, init_value=100, min_v=20, text_xo=35, color=GREEN),
               "s_range": Slider((w-150, 30), "sight range", max_v=200, init_value=100, min_v=20, text_xo=35, color=GREEN),
               "separation": Slider((w-50, 330), "separation", max_v=10, text_xo=30, color=RED),
               "alignment": Slider((w-150, 330), "alignment", max_v=10, text_xo=30),
               "cohesion": Slider((w-250, 330), "cohesion", max_v=10, text_xo=30, color=PURPLE),
               "speed": Slider((w-250, 30), "avg speed", max_v=100, init_value=50, text_xo=30, color=YELLOW)}


debug = 0
b_debug = debug
run = True
wall_repulsion_factor = 3
make_new_obstacle = False
hide_interface = False
while run:

    SCREEN.fill(BLACK)
    draw_world_border(SCREEN)

    if not hide_interface:
        if debug:
            screen_print(SCREEN, f"debug level: {debug}", WHITE, w/2-100, 40)
        screen_print(SCREEN, "press space to change the debug level.",
                    (100, 100, 100), w/2-102, 10, size=11)
        screen_print(SCREEN, "right-click to create obstacles, then scroll to desired size",
                    (100, 100, 100), w/2-140, 22, size=11)
        screen_print(SCREEN, "press 'H' to hide the interface and options.",
                    (100, 100, 100), w/2-107, 33, size=11)
        screen_print(SCREEN, "slide to interact",
                    (100, 100, 100), w-190, 290, size=11)

    sight_angle = int(all_sliders["s_angle"].value)
    sight_range = int(all_sliders["s_range"].value)
    separation_factor = (all_sliders["separation"].value/50)
    alingment_factor = (all_sliders["alignment"].value/50)
    cohesion_factor = (all_sliders["cohesion"].value/50)
    speed_factor = (all_sliders["speed"].value/40)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False        
            
        elif e.type == pygame.MOUSEBUTTONDOWN:
            press_place = pygame.Vector2(*pygame.mouse.get_pos())
            
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                run = False
            if e.key == pygame.K_SPACE:
                # 0: no debug, 1:choosen selected parameter view, 2: choosen all parameters view, 3: all objs all parameters view
                debug = (debug+1) % 4
                if debug == 0:
                    # blend the choosen
                    all_Fishs[choosen].color = all_Fishs[choosen-1].color
                elif debug == 1:
                    # pick new choosen
                    choosen = random.choice(range(len(all_Fishs)))
                    all_Fishs[choosen].color = GREEN
            if e.key == pygame.K_h:
                hide_interface = not hide_interface
                
        mouse_buttons = pygame.mouse.get_pressed()            
        if mouse_buttons[0]:
            prepare_actions = True
            mouse_pos = pygame.Vector2(*pygame.mouse.get_pos())
            if e.type == pygame.MOUSEWHEEL:
                scrolled += e.y*2
                if scrolled < 6:
                    scrolled = 5             
            if not any([obs.body.collidepoint(mouse_pos) for obs in all_obstacles]):
                draw_preview = True
        else:
            for s in all_sliders.values():
                s.on_focus = False
            for o in all_obstacles:
                o.on_focus = False
            prepare_actions = False
            scrolled = 5 
            draw_preview = False
    
    if prepare_actions:
                         
        for s in all_sliders.values():
            s.slide_it(mouse_pos)
        for obs in all_obstacles:
            obs.grab_it(mouse_pos, scrolled)
            
        if draw_preview and not any([s.on_focus for s in all_sliders.values()]):
            new_obstacle_rect = pygame.draw.rect(SCREEN, RED, (mouse_pos[0]-scrolled/2, mouse_pos[1]-scrolled/2, scrolled, scrolled), 2)
            make_new_obstacle = True
            
    elif make_new_obstacle:
        if new_obstacle_rect.w > 6:
            all_obstacles.append(Obstacle((new_obstacle_rect.w, new_obstacle_rect.h), (new_obstacle_rect.x, new_obstacle_rect.y)))
        make_new_obstacle = False

    view_ranges = all_sliders["s_range"].on_focus or all_sliders["s_angle"].on_focus
    for f in all_Fishs:
        if debug == 3:
            f.debug(SCREEN, debug=True, s_range=sight_range,
                    alt_activation=view_ranges)
        elif debug == 2:
            if f == all_Fishs[choosen]:
                f.debug(SCREEN, debug=True, s_range=sight_range)
        elif debug == 1:
            if f == all_Fishs[choosen]:
                f.debug(SCREEN, debug=view_ranges, s_range=sight_range)

    for f in all_Fishs:
        f.speed = speed_factor
        col_dist_lim = sight_range-(f.size)
        turning = 0.8
        move(f)

        # walls
        if f.pos[0] < col_dist_lim:
            if f.vec.y >= 0:
                rotate(f, "ccw", turning+col_dist_lim /
                       (f.pos[0]/wall_repulsion_factor))
            else:
                rotate(f, "cw", turning+col_dist_lim /
                       (f.pos[0]/wall_repulsion_factor))
        elif f.pos[0] > w-col_dist_lim:
            if f.vec.y >= 0:
                rotate(f, "cw", turning+col_dist_lim /
                       ((w-f.pos[0])/wall_repulsion_factor))
            else:
                rotate(f, "ccw", turning+col_dist_lim /
                       ((w-f.pos[0])/wall_repulsion_factor))

        if f.pos[1] < col_dist_lim:
            if f.vec.x >= 0:
                rotate(f, "cw", turning+col_dist_lim /
                       (f.pos[1]/wall_repulsion_factor))
            else:
                rotate(f, "ccw", turning+col_dist_lim /
                       (f.pos[1]/wall_repulsion_factor))
        elif f.pos[1] > h-col_dist_lim:
            if f.vec.x >= 0:
                rotate(f, "ccw", turning+col_dist_lim /
                       ((h-f.pos[1])/wall_repulsion_factor))
            else:
                rotate(f, "cw", turning+col_dist_lim /
                       ((h-f.pos[1])/wall_repulsion_factor))

        average_align_vec = pygame.Vector2((0, 0))
        average_pos_point = pygame.Vector2((0, 0))
        average_sep_vec = pygame.Vector2((0, 0))
        average_vec_len = 0
        neighbours = 0

        for f2 in all_Fishs:
            if f2 != f and f2.species == f.species:
                colli_dist = pygame.math.Vector2.distance_to(f.pos, f2.pos)

                if colli_dist < col_dist_lim:
                    dist_vec = pygame.math.Vector2.normalize(
                        pygame.Vector2((f2.pos[0]-f.pos[0], f2.pos[1]-f.pos[1])))
                    rel_angle = pygame.math.Vector2.angle_to(
                        f.vec, dist_vec) % 360
                    if rel_angle < sight_angle or rel_angle > 360-sight_angle:
                        neighbours += 1
                        # separation handling
                        average_sep_vec += (f.pos-f2.pos) / \
                            (colli_dist/sight_range)

                        # alingment handling
                        average_align_vec += f2.vec

                        # cohesion handling
                        average_pos_point += f2.pos

                        # speed handling
                        average_vec_len += f2.vec.length()

        if neighbours:
            # speed handling:
            average_vec_len /= neighbours
            pygame.math.Vector2.scale_to_length(
                f.vec, f.vec.length()-((f.vec.length()-average_vec_len)/100))

            # cohesion handling
            average_pos_point = average_pos_point/neighbours
            v_size = tuple(average_pos_point-f.pos)
            average_cohe_vec = pygame.math.Vector2.normalize(
                pygame.Vector2(v_size))

            # alignment handling
            average_align_vec = pygame.math.Vector2.normalize(
                average_align_vec/neighbours)

            # separation handling
            average_sep_vec = pygame.math.Vector2.normalize(
                (average_sep_vec/neighbours))

            final_cohe_vec = average_cohe_vec*cohesion_factor
            final_align_vec = average_align_vec*alingment_factor
            final_sep_vec = average_sep_vec*separation_factor

            output_vec = (final_cohe_vec + final_align_vec + final_sep_vec)
            f.vec = pygame.math.Vector2.normalize(f.vec+output_vec)

            if debug == 3:
                pygame.draw.line(SCREEN, WHITE, f.pos,
                                 final_align_vec*200+f.pos, 2)
                pygame.draw.line(SCREEN, PURPLE, f.pos,
                                 final_cohe_vec*200+f.pos, 2)
                pygame.draw.line(SCREEN, RED, f.pos,
                                 final_sep_vec*200+f.pos, 2)
            elif f == all_Fishs[choosen]:
                if debug == 1:
                    if all_sliders["cohesion"].on_focus:
                        pygame.draw.line(SCREEN, PURPLE, f.pos,
                                         final_cohe_vec*200+f.pos, 2)
                    elif all_sliders["alignment"].on_focus:
                        pygame.draw.line(SCREEN, WHITE, f.pos,
                                         final_align_vec*200+f.pos, 2)
                    elif all_sliders["separation"].on_focus:
                        pygame.draw.line(SCREEN, RED, f.pos,
                                         final_sep_vec*200+f.pos, 2)
                elif debug == 2:
                    pygame.draw.line(SCREEN, PURPLE, f.pos,
                                     final_cohe_vec*200+f.pos, 2)
                    pygame.draw.line(SCREEN, WHITE, f.pos,
                                     final_align_vec*200+f.pos, 2)
                    pygame.draw.line(SCREEN, RED, f.pos,
                                     final_sep_vec*200+f.pos, 2)

    if not hide_interface:
        for s in all_sliders.values():
            s.draw(SCREEN)
    for f in all_Fishs:
        f.draw(SCREEN)
    for o in all_obstacles:
        o.draw(SCREEN)

    clock.tick(60)
    pygame.display.flip()

pygame.quit()
