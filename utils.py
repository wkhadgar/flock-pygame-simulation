import pygame


def screen_print(screen, text: str, color: tuple, x: int, y: int, size=30, font="Arial"):
    text_font = pygame.font.SysFont(font, size)
    text_body = text_font.render(text, False, color)
    screen.blit(text_body, (x, y))
    
def vec_angle(vec, mode=1):
    if mode:
        angle = pygame.math.Vector2.angle_to(pygame.Vector2(1,0), vec)
    else:
        angle = pygame.math.Vector2.angle_to(pygame.Vector2(0,1), vec)
    return ((angle)%360)

def truncate_vec(vec, lim):
    if pygame.math.Vector2.length(vec) > lim:
        pygame.math.Vector2.scale_to_length(vec, lim)
        return vec
    else:
        return vec
    
def vectorize(point_A, point_B):
    vec_dimension = point_B[0]-point_A[0], point_B[1]-point_A[1]
    return pygame.Vector2(vec_dimension)

def seek_flee_LT_vector(LivingThing, target_Group, pursuit=0, flee=False):
        
    for target in target_Group.sprites():
        if pursuit:
            dist_vec = vectorize(LivingThing.pos, target.pos+target.velocity_vec*pursuit)
        else:
            dist_vec = vectorize(LivingThing.pos, target.pos)
            
        if dist_vec.length() <= LivingThing.sight_range:  # its in sight
            if flee:
                if target not in LivingThing.dangers:
                    LivingThing.dangers.add(target)
                    print("located danger")
            else:
                if target not in LivingThing.targets:
                    LivingThing.targets.add(target)
                    print("located target")
                    
        elif flee:
            if target in LivingThing.dangers:
                LivingThing.dangers.remove(target)
        else:
            if target in LivingThing.targets:
                LivingThing.targets.remove(target)    
                
    if flee:
        if len(LivingThing.dangers) > 0:
            if pursuit:
                tgt_will_vec = vectorize(LivingThing.pos, LivingThing.dangers.sprites()[0].pos+LivingThing.dangers.sprites()[0].velocity_vec*pursuit)
            else:
                tgt_will_vec = vectorize(LivingThing.pos, LivingThing.dangers.sprites()[0].pos)
            tgt_will_vec.scale_to_length(LivingThing.max_speed)
            if LivingThing.dangers.sprites()[0] not in target_Group.sprites():
                LivingThing.dangers.remove(LivingThing.dangers.sprites()[0])
        else: 
            tgt_will_vec = LivingThing.velocity_vec   
    else:
        if len(LivingThing.targets) > 0:
            if pursuit:
                tgt_will_vec = vectorize(LivingThing.pos, LivingThing.targets.sprites()[0].pos+LivingThing.targets.sprites()[0].velocity_vec*pursuit)
            else:
                tgt_will_vec = vectorize(LivingThing.pos, LivingThing.targets.sprites()[0].pos)
            tgt_will_vec.scale_to_length(LivingThing.max_speed)
            if LivingThing.targets.sprites()[0] not in target_Group.sprites():
                LivingThing.targets.remove(LivingThing.targets.sprites()[0])
        else: 
            tgt_will_vec = LivingThing.velocity_vec   
        
    if flee:
        return -tgt_will_vec
    else:
        return tgt_will_vec