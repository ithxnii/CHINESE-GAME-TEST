import pygame
import pandas as pd
import random 
import time 

pygame.init()

# set screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("CHINESE TEST")

icon = pygame.image.load("image/icon.png")
pygame.display.set_icon(icon)
background = pygame.image.load("image/background.png")
# set screen ของ show_result
score_backgroung = pygame.image.load("image/scorebackground.png")
frame_image = pygame.image.load("image/scoreframe.png")
replay_button_image = pygame.image.load("image/replay.png").convert_alpha()
quit_button_image = pygame.image.load("image/quit.png").convert_alpha()
#next_level_button_image = pygame.image.load(r"C:/Users/Asus/OneDrive/เดสก์ท็อป/TRY/data_try_python/image/NEXT.png").convert_alpha()

# boazi_image = pygame.image.load(r"C:/Users/Asus/OneDrive/เดสก์ท็อป/TRY/data_try_python/image/baozi.png").convert_alpha()
#fonts
font1 = "fonts/ZCOOLXiaoWei-Regular.ttf"
font2 = "fonts/NotoSansMono-VariableFont_wdth,wght.ttf"
font3 = "fonts/NotoSansThai-VariableFont_wdth,wght.ttf"

font_size22 = 22
font_size30 = 30
font_size38  = 38
font_size75 = 75

font_chinese = pygame.font.Font(font1, font_size30)
font_pinyin =  pygame.font.Font(font2,font_size30)
font_thai =  pygame.font.Font(font3,font_size30)

font_chinese_38 = pygame.font.Font(font1, font_size38)
font_pinyin_38 = pygame.font.Font(font2, font_size38)
font_thai_38 = pygame.font.Font(font3, font_size38)
# font ของ time
font_thai2 = pygame.font.Font(font3,font_size75)

#font ของ show_results
font_chinese22 = pygame.font.Font(font1, font_size22)
font_pinyin22 =  pygame.font.Font(font2,font_size22)
font_thai22 =  pygame.font.Font(font3,font_size22)

#ข้อมูล
hsk3 = r"C:/Users/Asus/OneDrive/เดสก์ท็อป/TRY/data_try_python/hsk3_vocab.csv"
def load_words_from_csv(hsk3):
    df = pd.read_csv(hsk3, encoding='utf-8')
    df['meaning'] = df['meaning'].apply(lambda x: [m.strip() for m in x.split(',')])
    return df.to_dict(orient='records')


words = load_words_from_csv(hsk3)
#print(words)


#ตัวแปรในเกม ใหม่ทั้งหมด
score = 0
question_count = 0
max_questions = 15
time_limit = 30
asked_questions = []
wrong_answers = []


def game_loop():
    global score, question_count, wrong_answers
    user_input = ""
    


    while question_count < max_questions:
        current_word = random.choice(words)
        while current_word in asked_questions:
            current_word =  random.choice(words)
    
        asked_questions.append(current_word)
        chinese_word = current_word['word']
        chinese_pinyin = current_word['pinyin']
        correct_answer = current_word['meaning']
        answered = False
        start_time = time.time()
        user_input = ""
   # user_input = "" #newNew

        while time_limit > 0 and not answered:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                 pygame.quit()
                 exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        correct_answers = correct_answer
                        
                        if user_input in correct_answers:
                            score += 1
                            show_correct_answer()
                            question_count += 1
                            answered = True
                    
                        else:
                            wrong_answers.append((chinese_word, chinese_pinyin, correct_answer))
                            show_wrong_answer(chinese_word, chinese_pinyin, correct_answer)
                            question_count += 1
                            answered = True
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    else:
                        user_input += event.unicode
                
            time_left = time_limit - (time.time() - start_time)
            screen.fill((255, 255, 255))
            screen.blit(background,(0, 0))

            thai_text = font_thai_38.render("ความหมายของ ", True, (0, 0, 0) )
            chinese_text = font_chinese_38.render(chinese_word, True, (0, 0, 0))
            pinyin_text = font_thai_38.render(f"({chinese_pinyin})", True, (0, 0, 0))
            
            screen.blit(thai_text,(130, 80))
            screen.blit(chinese_text, (130 + thai_text.get_width(), 80))
            screen.blit(pinyin_text, (130 + thai_text.get_width() + chinese_text.get_width(), 80))

            if time_left > 20 :
                circle_color = (0, 128, 0)
            elif time_left > 10 :
                circle_color = (255, 255, 0)
            else :
                circle_color = (255, 0, 0)

            pygame.draw.circle(screen, circle_color, (100, 480), 72)

            timer_text = font_thai2.render(f"{max(0, int(time_left))}", True, (0, 0, 0))
            screen.blit(timer_text, (100 - timer_text.get_width() // 2, 480 - timer_text.get_height()//2))

            answer_text = font_thai_38.render(f"คำตอบ : {user_input}", True, (0, 0, 0))
            screen.blit(answer_text, (130,190))

            if time_left <= 0:
                screen.fill((225, 0, 0))
                time_up_text = font_thai.render(f"หมดเวลา", True, (255, 255, 255))
                screen.blit(time_up_text, (50,350))
                time_up_text2 = font_thai.render(f"คำตอบที่ถูกคือ : {','.join(correct_answer)}", True, (255, 255, 255) )
                screen.blit(time_up_text2, (50,400))
                pygame.display.update()
                time.sleep(3)
                question_count += 1
                break
            pygame.display.update()
    
    show_results()

def show_correct_answer():
    screen.fill((0, 255, 0))
    correct_text = font_thai_38.render("ถูกต้อง!", True, (0, 0, 0))
    screen.blit(correct_text, (340, 280))
    pygame.display.update()
    time.sleep(1)
    

def show_wrong_answer(chinese, pinyin, correct):
    screen.fill((255, 0, 0))
    wrong_text = font_thai.render(f"คำตอบคือ : ", True, (255, 255, 255))
    wrong_text2 = font_thai.render(f"{','.join(correct)}", True, (255, 255, 255))
    screen.blit(wrong_text, (50, 350))
    screen.blit(wrong_text2, (50 + wrong_text.get_width(), 350))
    pygame.display.update() 
    time.sleep(1)
    

def show_results():
    screen.blit(score_backgroung, (0, 0))
    
    screen.blit(frame_image, (260,8))

    result_text = font_thai.render(f"คะแนน : {score}/{max_questions}", True, (0, 0, 0))
    screen.blit(result_text, (300,26))

    if wrong_answers:
        start_y = 100
        for i in range(0, len(wrong_answers), 2):
            if i < len(wrong_answers):
                chinese1, pinyin1, correct1 = wrong_answers[i]
                wrong_chinese_text1 = font_chinese22.render(f"{i+1}. {chinese1}", True, (0, 0, 0))
                wrong_pinyin_text1 = font_pinyin22.render(f"   {pinyin1}", True, (0, 0, 0))
                correct_text1 = font_thai22.render(f"    {','.join(correct1)}", True, (0, 0, 0))

                screen.blit(wrong_chinese_text1, (30, start_y))
                screen.blit(wrong_pinyin_text1, (100, start_y))
                screen.blit(correct_text1, (230, start_y))

            if i + 1 < len(wrong_answers):
                chinese2, pinyin2, correct2 = wrong_answers[i + 1]
                wrong_chinese_text2 = font_chinese22.render(f"{i + 2}. {chinese2}", True, (0, 0, 0))
                wrong_pinyin_text2 = font_pinyin22.render(f"   {pinyin2}", True, (0, 0, 0))
                correct_text2 = font_thai22.render(f"   {','.join(correct2)}", True, (0, 0, 0))

                screen.blit(wrong_chinese_text2, (410, start_y))
                screen.blit(wrong_pinyin_text2, (480, start_y))
                screen.blit(correct_text2, (630, start_y))

            start_y += 40

    screen.blit(replay_button_image, (100, 510))
    screen.blit(quit_button_image, (500, 510))
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 100 < mouse_x < 100 + replay_button_image.get_width() and 510 < mouse_y < 510 + replay_button_image.get_height():
                    restart_game()
                
                elif 500 < mouse_x < 550 + quit_button_image.get_width() and 510 < mouse_y < 510 + quit_button_image.get_height():
                    quit_game()
                
def restart_game():
    reset_game()
    return

def quit_game():
    pygame.quit()
    exit()

def reset_game():
    global score, question_count, asked_questions, wrong_answers
    score = 0
    question_count = 0
    asked_questions = []
    wrong_answers = []
    game_loop()



    pygame.display.update()
    time.sleep(300)
    pygame.quit() 
game_loop()

    


    





                






