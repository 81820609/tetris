# import random
from tracemalloc import start

import pygame
from attr import s

import constant as c
from frame import *

pygame.font.init()
# pygame.mixer.init()
# file_name = 'music\lost_boy.mp3'
# pygame.mixer.music.load(file_name)


s_width = c.s_width
s_height = c.s_height


score_dic = c.score_dic


def main(win):

      locked_positions = {}
      grid = create_grid(locked_positions)

      change_piece = False
      hold_state = False
      event_count = 0
      run = True
      current_group = get_shapes()
      next_group = get_shapes()
      shapes_index = 0
      next_index = 1
      current_piece = current_group[shapes_index]
      next_piece = current_group[next_index]
      hold_piece = 0
      
      clock = pygame.time.Clock()
      score = 0
      delay_time = 0
      time_delay = 200
      fall_time = 0
      fall_speed = 0.27
      current_speed = fall_speed
      level_time = 0
      last_score = max_score()
      level = 0
      move_time = 0
      move_speed = 0.03
      long_press = {'down':False,'left':False,'right':False}
      # print(last_score)

      while run:
            
            # pygame.time.wait(16)
            grid = create_grid(locked_positions)
            fall_time += clock.get_rawtime()
            level_time += clock.get_rawtime()
            clock.tick(100)
            # print(fall_time)
            # print(clock.get_fps)
            # print(fall_speed,fall_time,level_time)
            
            

            if level_time/1000 >= 10:
                  level_time = 0
                  if fall_speed > 0.15:
                        fall_speed -= level


            if fall_time/1000 >= fall_speed:
                  fall_time = 0                  
                  current_piece.y += 1
                  if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                        current_piece.y -= 1                        
                        change_piece = True
            
            
                        


            for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                        run = False
                        pygame.display.quit()
                        quit()

                  if event.type == pygame.KEYDOWN:
                        
                        if event.key == pygame.K_LEFT:
                              long_press['left'] = True
                                                           

                              # print(move_time) 
                              current_piece.x -= 1
                              if not(valid_space(current_piece,grid)):
                                    current_piece.x += 1

                        if event.key == pygame.K_RIGHT:
                              long_press['right'] = True
                              current_piece.x += 1
                              if not(valid_space(current_piece,grid)):
                                    current_piece.x -= 1
                              
                        
                        if event.key == pygame.K_DOWN:
                              long_press['down'] = True
                              current_piece.y += 1
                              if not(valid_space(current_piece,grid)):
                                    current_piece.y -= 1

                        if event.key == pygame.K_UP:
                              current_piece.rotation += 1
                              if not(valid_space(current_piece,grid)):
                                    current_piece.rotation -= 1

                        if event.key == pygame.K_z:
                              current_piece.rotation -= 1
                              if not(valid_space(current_piece,grid)):
                                    current_piece.rotation += 1

                        if event.key == pygame.K_SPACE:
                              current_piece.y += 1
                              while valid_space(current_piece, grid) and current_piece.y > 0:
                                    current_piece.y += 1
                              current_piece.y -= 1
                              change_piece = True
                              # current_speed = fall_speed
                              # fall_speed = 0.00001
                        if event.key == pygame.K_c:
                              if hold_piece == 0:
                                    hold_piece = current_piece
                                    change_piece = True
                                    hold_state = True
                                    # shapes_index = next_index
                                    # next_index += 1
                                    # if next_index == 7:
                                    #       current_group = next_group
                                    #       next_group = get_shapes()
                                    # next_index = next_index % 7
                                    # # print(next_index)
                                    # current_piece = next_piece
                                    # next_piece = current_group[next_index]
                              else:
                                    hold_piece, current_piece = current_piece, hold_piece
                                    current_piece.x, current_piece.y = 5,0
                                    
                                    
                  if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT:
                              long_press['left'] = False
                              delay_time = 0
                              

                        if event.key == pygame.K_RIGHT:
                              long_press['right'] = False
                              delay_time = 0

                        if event.key == pygame.K_DOWN:
                              long_press['down'] = False
                              delay_time = 0
                        # move_time = 0
                        

            if long_press['left']:
                  move_time += clock.get_rawtime()
                  delay_time += clock.get_rawtime()
                  if delay_time >= time_delay:
                        if move_time/1000 >= move_speed:
                              move_time = 0
                              current_piece.x -= 1
                              if not(valid_space(current_piece,grid)):
                                    current_piece.x += 1

                  # print(delay_time, move_time)


            if long_press['right']:
                  move_time += clock.get_rawtime()
                  delay_time += clock.get_rawtime()
                  if delay_time >= time_delay:
                        if move_time/1000 >= move_speed:
                              move_time = 0
                              current_piece.x += 1
                              if not(valid_space(current_piece,grid)):
                                    current_piece.x -= 1

            if long_press['down']:
                  move_time += clock.get_rawtime()
                  delay_time += clock.get_rawtime()
                  if delay_time >= time_delay:
                        if move_time/1000 >= move_speed:
                              move_time = 0
                              current_piece.y += 1
                              if not(valid_space(current_piece,grid)):
                                    current_piece.y -= 1

            
            shape_pos = convert_shape_format(current_piece)
            # print(shape_pos)

            draw_predict(locked_positions,shape_pos,grid)

            for i in range(len(shape_pos)):
                  x, y = shape_pos[i]
                  if y > -1:
                        grid[y][x] = current_piece.color

            

            if change_piece:
                  if hold_state == False:
                        for pos in shape_pos:
                              p = (pos[0],pos[1])
                              locked_positions[p] = current_piece.color

                  hold_state = False

                  shapes_index = next_index
                  next_index += 1
                  if next_index == 7:
                        current_group = next_group
                        next_group = get_shapes()
                  next_index = next_index % 7
                  # print(next_index)
                  current_piece = next_piece
                  next_piece = current_group[next_index]
                  change_piece = False
                  score += score_dic[clear_rows(grid, locked_positions)]
                  # fall_speed = current_speed
                  

            
            draw_window(win,grid)
            draw_next_shapes(current_group,next_group,win,5,next_index)
            draw_hold_piece(win, hold_piece)
            draw_score(win,score,last_score)
            print(current_piece.x, current_piece.y)
            pygame.display.update()

            if check_lost(locked_positions):
                  draw_middle_text(win, 'You Lost!', 60, (255,255,255))
                  # pygame.mixer.music.stop()
                  pygame.display.update()
                  pygame.time.delay(1500)
                  run = False
                  update_score(score)
    
           
            

def main_menu(win):
      run = True
      
      while run:
            win.fill((0,0,0))
            draw_middle_text(win,'Press Any Key To Play', 60, (255,255,255))
            pygame.display.update()
            for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                        run = False
                        
                  elif event.type == pygame.KEYDOWN:
                        # pygame.mixer.music.play(-1,0,0)
                        main(win)
                        
      
      pygame.display.quit()
                  
         

win = pygame.display.set_mode((s_width,s_height))
pygame.display.set_caption('Tetris')
main_menu(win)





