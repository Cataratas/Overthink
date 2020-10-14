import pickle
import os
import json
import sys
import win32api
# import pygame
from Modules import ptext, pygame_textinput
from Functions import draw, Button, centerprint, Languages, Question, Time, window, printt, pdf, pdfPageCount, createImageFromPDF
from Games import tictactoe, minesweeper, maze, sudoku, memory, hangman
from Variables import *

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Overthink")
pygame.display.set_icon(pygame.image.load("icon.png"))
screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
fps = 25


def mainmenu():
    Start = Button(Language.list[0], "bBlue", (407, 42))
    Options = Button(Language.list[28], "Blue"); Exit = Button(Language.list[8], "Blue")

    while True:
        mouse = pygame.mouse.get_pos()
        sw, sh = screen.get_size()

        for event in pygame.event.get():
            window(event)

            if Exit.click(event): sys.exit()
            elif Start.click(event): menuselect()
            elif Options.click(event): languagemenu()

        screen.fill(white)

        draw('./Layout/Logo.png', sw//2-300, sh*.1)

        Start.show(mouse, sw//2-204, sh//2)
        Options.show(mouse, sw//2-204, sh//2+55), Exit.show(mouse, sw//2+8, sh//2+55)

        pygame.display.update(), clock.tick(fps)


def languagemenu():
    Return = Button(Language.list[1], "Salmon"); Apply = Button(Language.list[29], "Green")
    EN = Button("English", "Blue"); PT = Button("Português", "Blue"); ES = Button("Español", "Blue")

    config["idiom"] = None

    while True:
        mouse = pygame.mouse.get_pos()
        sw, sh = screen.get_size()

        for event in pygame.event.get():
            window(event)

            if EN.click(event): config["idiom"] = "en"
            elif PT.click(event): config["idiom"] = "pt"
            elif ES.click(event): config["idiom"] = "es"

            elif Apply.click(event) and config["idiom"] is not None:
                exec("Language.{}()".format(config["idiom"]))
                with open("config.json", "w") as C:
                    json.dump(config, C)
                mainmenu()

            elif Return.click(event): mainmenu()

        screen.fill(white)

        centerprint(Language.list[34], sw//2-235, sh*.2, 470, 25, black, font24)

        Return.show(mouse, 30, sh-80), Apply.show(mouse, sw-225, sh-80)
        EN.show(mouse, sw//2-317, sh//2-50, pressed=config["idiom"] == "en")
        PT.show(mouse, sw//2-97, sh//2-50, pressed=config["idiom"] == "pt")
        ES.show(mouse, sw//2+122, sh//2-50, pressed=config["idiom"] == "es")

        pygame.display.update(), clock.tick(fps)


def menuselect():
    global Quiz, life, coin, x, resettime, quiz_file, score, total

    Return = Button(Language.list[1], "Salmon"); Play = Button(Language.list[7], "Green")
    Right = Button(Language.list[3], "Orange"); Left = Button(Language.list[2], "Orange")
    Delete = Button(Language.list[4], "Blue"); Edit = Button(Language.list[6], "Blue")
    Create = Button(Language.list[5], "Blue")

    files = [f.replace(".pkl", "") for f in os.listdir("./Quizzes") if f.endswith(".pkl")]
    resettime, active, page, buttons = True, -1, 0, []

    while True:
        mouse = pygame.mouse.get_pos(); pages = len(files) / 10
        sw, sh = screen.get_size()

        for event in pygame.event.get():
            window(event)

            if Play.click(event, active != -1) and active != -1:
                with open("./Quizzes/{}.pkl".format(files[active]), "rb") as f:
                    Quiz, life, coin, x, total, life2, score, coin2 = pickle.load(f)
                if life2 != 0: life = life2
                if coin2 != 0: coin = coin2
                quiz_file = files[active]
                menuquest()

            elif Right.click(event, page + 1 != pages and page + 1 < pages != 0): page += 1
            elif Left.click(event, page != 0 and pages != 0): page -= 1

            elif Delete.click(event, active != -1):
                confirmationmenu(files[active])
                files = [f.replace(".pkl", "") for f in os.listdir("./Quizzes") if f.endswith(".pkl")]
                active = -1

            elif Return.click(event): mainmenu()
            elif Edit.click(event, active != -1): menueditor(files[active])
            elif Create.click(event): menueditor()

            for i in range(len(buttons)):
                if buttons[i].click(event): active = i + page * 10

        if page >= pages: page -= 1
        screen.fill(white)

        x, y, first, second, buttons = sw//2-500, sh//2-180, True, False, []

        for i in range(10):
            i += page * 10

            if len(files) - page * 10 <= 5:
                x = sw//2-250
                if first: first = False
                else: y += 60
            else:
                if second: x += 536
                if not second and i - page * 10 != 0:
                    x = sw//2-500; y += 60
                second = not second

            try:
                with open("./Quizzes/{}.pkl".format(files[i]), "rb") as f:
                    Quiz, life, coin, x1, total, life2, score, coin2 = pickle.load(f)
                if x1 != 0 or (coin2 != coin and coin2 != 0) or (life2 != 0 and life2 != life): buttons.append(Button(files[i], "File2", (501, 42)))
                else: buttons.append(Button(files[i], "File", (501, 42)))
                buttons[i - page * 10].show(mouse, x, y, pressed=active == i)
            except IndexError: break

        Return.show(mouse, 30, sh-80), Create.show(mouse, sw-655, sh-80), Delete.show(mouse, sw-870, sh-80, active != -1)
        Edit.show(mouse, sw-440, sh-80, active != -1), Play.show(mouse, sw-225, sh - 80, active != -1)
        Right.show(mouse, sw-225, sh-135, page + 1 != pages and page + 1 < pages != 0), Left.show(mouse, 30, sh-135, page != 0 and pages != 0)

        pygame.display.update(), clock.tick(fps)


def confirmationmenu(File="0", giveup=False):
    if not giveup: name = Language.list[4]
    else: name = Language.list[14]
    Delete = Button(name, "Blue"); Cancel = Button(Language.list[30], "Blue")

    while True:
        mouse = pygame.mouse.get_pos()
        sw, sh = screen.get_size()

        for event in pygame.event.get():
            window(event)

            if Delete.click(event):
                if not giveup: os.remove("./Quizzes/{}.pkl".format(File)); return
                else: endmenu(False)
            elif Cancel.click(event): return

        screen.fill(white)

        if not giveup:
            centerprint(Language.list[31], sw//2-235, sh*.2, 470, 25, black, font24)
            centerprint(Language.list[32].format(File), sw//2-235, sh*.2+35, 470, 25, black, font24)
        else:
            centerprint(Language.list[35], sw//2-235, sh*.2, 470, 25, black, font24)

        Delete.show(mouse, sw//2-205, sh//2), Cancel.show(mouse, sw//2+10, sh//2)

        pygame.display.update(), clock.tick(fps)


def menueditor(File=None):
    Previous = Button(Language.list[2], "Orange"); Next = Button(Language.list[3], "Orange")
    Create = Button(Language.list[9], "Blue"); Delete = Button(Language.list[10], "Blue")
    SaveExit = Button(Language.list[11], "Green"); Exit = Button(Language.list[8], "Salmon")
    PrintMenu = Button(Language.list[36], "Blue")

    LifeB = [Button(" ", "Life", (31, 31)), Button(" ", "Life", (31, 31))]
    CoinB = [Button(" ", "Coin", (31, 31)), Button(" ", "Coin", (31, 31))]

    A = Button(" ", "Correct", (47, 42)); B = Button(" ", "Correct", (47, 42))
    C = Button(" ", "Correct", (47, 42)); D = Button(" ", "Correct", (47, 42))

    NameRect, QuestionRect = pygame.Rect(34, 30, 501, 43), pygame.Rect(21, 168, 1239, 255)
    ARect, BRect = pygame.Rect(43, 446, 512, 75), pygame.Rect(43, 535, 512, 75)
    CRect, DRect = pygame.Rect(666, 446, 512, 75), pygame.Rect(666, 535, 512, 75)

    Files = [f.replace(".pkl", "").lower() for f in os.listdir("./Quizzes") if f.endswith(".pkl")]
    Buttons, page, active, correct, save = [], 0, 0, None, False
    AAnswer, BAnswer, CAnswer, DAnswer = None, None, None, None
    Name, TQuestion, PFile = None, None, File

    if File:
        with open("./Quizzes/{}.pkl".format(File), "rb") as f:
            Quiz, life, coin, temp0, temp1, temp2, temp3, temp4 = pickle.load(f)
            if File.lower() in Files: del Files[Files.index(File.lower())]
    else:
        Quiz, life, coin = [Question("", ["", "", "", "", correct])], 10, 2
        temp0, temp1, temp2, temp3, temp4 = 0, len(Quiz), 0, 0, 0

    while True:
        mouse = pygame.mouse.get_pos(); events = pygame.event.get()
        sw, sh = screen.get_size(); pages = len(Quiz) / 10

        for event in events:
            window(event)

            if Exit.click(event): menuselect()

            elif LifeB[0].click(event, life > 1): life -= 1
            elif LifeB[1].click(event, life < 999): life += 1
            elif CoinB[0].click(event, coin > 0): coin -= 1
            elif CoinB[1].click(event, coin < 25): coin += 1

            elif Previous.click(event, page != 0 and pages != 0): page -= 1
            elif Next.click(event, page + 1 != pages and page + 1 < pages != 0): page += 1

            elif Create.click(event):
                active = len(Quiz); page = int(pages)
                Quiz.append(Question("", ["", "", "", "", None]))
                TQuestion, AAnswer, BAnswer, CAnswer, DAnswer, correct = None, None, None, None, None, None

            elif Delete.click(event, len(Quiz) > 1):
                del Quiz[active]
                if active > 0: active -= 1
                if active != 0: correct = Quiz[active].answer[-1]
                if (len(Quiz) % 10) == 0 and page > 0: page -= 1
                if active < page * 10: page -= 1
                TQuestion, AAnswer, BAnswer, CAnswer, DAnswer = None, None, None, None, None

            elif SaveExit.click(event, save and Name.get_text().lower() not in Files):
                File = Name.get_text()
                with open("./Quizzes/{}.pkl".format(File), "wb") as f:
                    pickle.dump([Quiz, life, coin, temp0, len(Quiz)-temp0, temp2, temp3, temp4], f)
                if PFile != File and PFile is not None: os.remove("./Quizzes/{}.pkl".format(PFile))
                menuselect()

            elif PrintMenu.click(event, save): printmenu(Name.get_text(), Quiz)

            elif A.click(event): correct = "a"
            elif B.click(event): correct = "b"
            elif C.click(event): correct = "c"
            elif D.click(event): correct = "d"

            for i in range(len(Buttons)):
                if Buttons[i].click(event) and active != i + page * 10:
                    active = i + page * 10
                    TQuestion, AAnswer, BAnswer, CAnswer, DAnswer, correct = None, None, None, None, None, None
                    break

        screen.fill(white)

        Buttons = []

        if (len(Quiz) % 10) != 0: x = sw//2-30 * (len(Quiz[page * 10:page * 10 + 10]))
        else: x = sw//2-30 * 10

        for i in range(10):
            i += page * 10
            if i < len(Quiz):
                Buttons.append(Button("{}".format(i + 1), "sBlue", (47, 42)))
                Buttons[i - page * 10].show(mouse, x, sh*.035+80, pressed=active == i)
                x += 60
            else: break

        if File is not None and Name is None:
            Name = pygame_textinput.TextInput(input_string=File, message=Language.list[12], rect=NameRect, click=True, font_size=26, font_family="./Fonts/berlin-sans-fb-demi-bold.ttf", text_color=white, cursor_color=white, contain=True)
        elif File is None and Name is None:
            Name = pygame_textinput.TextInput(message=Language.list[12], rect=NameRect, click=True, font_size=26, font_family="./Fonts/berlin-sans-fb-demi-bold.ttf", text_color=white, cursor_color=white, contain=True)

        QuestionRect.x = sw//2-620; QuestionRect.y = sh*.24
        ARect.x = sw//2-600; ARect.y = sh*.24+275
        BRect.x = sw//2-600; BRect.y = sh*.24+365
        CRect.x = sw//2+20; CRect.y = sh*.24+275
        DRect.x = sw//2+20; DRect.y = sh*.24+365

        draw("./Layout/Answer Background.png", ARect.x, ARect.y), draw("./Layout/Answer Background.png", BRect.x, BRect.y)
        draw("./Layout/Answer Background.png", CRect.x, CRect.y), draw("./Layout/Answer Background.png", DRect.x, DRect.y)
        draw("./Layout/Question Background.png", QuestionRect.x, QuestionRect.y)
        draw("./Buttons/File 2.png", 30, 25), screen.blit(Name.get_surface(), (40, 31))
        draw("./Layout/Life 2.png", 571, 25), centerprint(life, 634, 37, 128, 30, red)
        draw("./Layout/Coin 2.png", 799, 22), centerprint(coin, 863, 36, 128, 30, yellow)

        if TQuestion is None: TQuestion = pygame_textinput.TextInput(input_string=Quiz[active].question, message=Language.list[27], rect=QuestionRect, click=True, font_size=18, font_family="./Fonts/myriad-pro-8.otf",
                                                                     text_color=gray2, cursor_color=gray2, lines=True, limit=2000)
        if AAnswer is None: AAnswer = pygame_textinput.TextInput(input_string=Quiz[active].answer[0], message=Language.list[13], rect=ARect, click=True, font_size=18, font_family="./Fonts/myriad-pro-8.otf",
                                                                 text_color=gray2, cursor_color=gray2, lines=True, limit=250)
        if BAnswer is None: BAnswer = pygame_textinput.TextInput(input_string=Quiz[active].answer[1], message=Language.list[13], rect=BRect, click=True, font_size=18, font_family="./Fonts/myriad-pro-8.otf",
                                                                 text_color=gray2, cursor_color=gray2, lines=True, limit=250)
        if CAnswer is None: CAnswer = pygame_textinput.TextInput(input_string=Quiz[active].answer[2], message=Language.list[13], rect=CRect, click=True, font_size=18, font_family="./Fonts/myriad-pro-8.otf",
                                                                 text_color=gray2, cursor_color=gray2, lines=True, limit=250)
        if DAnswer is None: DAnswer = pygame_textinput.TextInput(input_string=Quiz[active].answer[3], message=Language.list[13], rect=DRect, click=True, font_size=18, font_family="./Fonts/myriad-pro-8.otf",
                                                                 text_color=gray2, cursor_color=gray2, lines=True, limit=250)
        if correct is None: correct = Quiz[active].answer[-1]

        screen.blit(TQuestion.get_surface(), (QuestionRect.x+4, QuestionRect.y+4))
        screen.blit(AAnswer.get_surface(), (ARect.x+4, ARect.y)); screen.blit(BAnswer.get_surface(), (BRect.x+4, BRect.y))
        screen.blit(CAnswer.get_surface(), (CRect.x+4, CRect.y)); screen.blit(DAnswer.get_surface(), (DRect.x+4, DRect.y))

        Quiz[active].answer[0], Quiz[active].answer[1] = AAnswer.get_text(), BAnswer.get_text()
        Quiz[active].answer[2], Quiz[active].answer[3] = CAnswer.get_text(), DAnswer.get_text()
        Quiz[active].answer[-1], Quiz[active].question = correct, TQuestion.get_text()

        for i in range(len(Quiz)):
            save = False
            if Name.get_text() == "": break
            if Quiz[i].question == "": break
            if "" in Quiz[i].answer: break
            if Quiz[i].answer[-1] is None: break
            if File in Files: break
            save = True

        Exit.show(mouse, 30, sh-80), Delete.show(mouse, sw - 655, sh - 80, len(Quiz) > 1), Create.show(mouse, sw-440, sh-80)
        SaveExit.show(mouse, sw-225, sh-80, save and Name.get_text().lower() not in Files)
        Previous.show(mouse, 30, sh*.035+80, page != 0 and pages != 0)
        Next.show(mouse, sw-225, sh*.035+80, page + 1 != pages and page + 1 < pages != 0)
        PrintMenu.show(mouse, sw-870, sh-80, save)

        LifeB[0].show(mouse, 634, 38, life > 1), LifeB[1].show(mouse, 732, 37, life < 999, mirror=True)
        CoinB[0].show(mouse, 861, 37, coin > 0), CoinB[1].show(mouse, 959, 38, coin < 25, mirror=True)

        A.show(mouse, sw//2-70, sh*.24+290, pressed=correct == "a"), B.show(mouse, sw//2-70, sh*.24+380, pressed=correct == "b")
        C.show(mouse, sw//2+550, sh*.24+290, pressed=correct == "c"), D.show(mouse, sw//2+550, sh*.24+380, pressed=correct == "d")

        Name.update(events), TQuestion.update(events), AAnswer.update(events), BAnswer.update(events), CAnswer.update(events), DAnswer.update(events)

        pygame.display.update(), clock.tick(fps)


def printmenu(File, Quiz):
    Return = Button(Language.list[1], "Salmon"); Print = Button(Language.list[36], "Blue")
    Column1 = Button(" ", "Correct", (47, 42)); Column2 = Button(" ", "Correct", (47, 42))
    Answer1 = Button(" ", "Correct", (47, 42)); Answer2 = Button(" ", "Correct", (47, 42))
    All1 = Button(" ", "Correct", (47, 42))
    Page1 = Button(" ", "Page", (107, 42)); Page2 = Button(" ", "Page", (107, 42))
    Page3 = Button(" ", "Page", (107, 42)); Page4 = Button(" ", "Page", (107, 42))

    column, feedback, allQuestions = True, False, True
    page, Buttons, change, paperpage, pagecount = 0, [], True, 0, 0
    Active = [True for i in range(len(Quiz))]

    try: os.remove("./Layout/Preview 0.png"), os.remove("./Layout/Preview 1.png")
    except FileNotFoundError: pass
    createImageFromPDF("Quiz.pdf", paperpage)

    while True:
        mouse, pages = pygame.mouse.get_pos(), len(Quiz) / 27
        sw, sh = screen.get_size()
        if change:
            pdf(File, Quiz, Active, feedback, column, Language)
            pagecount = pdfPageCount("Quiz.pdf")
            createImageFromPDF("Quiz.pdf", paperpage)
            change = False

        for i in range(len(Active)):
            if not Active[i]: allQuestions = False; break
            if Active[i]: allQuestions = True

        for event in pygame.event.get():
            window(event)

            if Return.click(event): return
            elif Print.click(event): win32api.ShellExecute(0, "open", "Quiz.pdf", None,  ".",  0)
            elif Column1.click(event) and not column or Column2.click(event) and column: column = not column; change = True
            elif Answer1.click(event) and not feedback or Answer2.click(event) and feedback: feedback = not feedback; change = True

            elif All1.click(event) and not allQuestions:
                allQuestions, change = not allQuestions, True
                if allQuestions: Active = [True for i in range(len(Quiz))]

            elif Page1.click(event, page > 0): page -= 1
            elif Page2.click(event, page + 1 != pages and page + 1 < pages != 0): page += 1
            elif Page3.click(event, paperpage > 0): paperpage -= 2; createImageFromPDF("Quiz.pdf", paperpage)
            elif Page4.click(event, paperpage + 1 != pagecount and paperpage + 2 < pagecount != 0): paperpage += 2; createImageFromPDF("Quiz.pdf", paperpage)

            for i in range(len(Buttons)):
                if Buttons[i].click(event): Active[i+page*27] = not Active[i+page*27]; change = True

        screen.fill(white)

        draw("./Buttons/File 2.png", 30, 25), centerprint(File, 30, 25, 501, 42)
        printt(Language.list[37], sw//2-520, sh//2-230), printt(Language.list[38], sw//2-270, sh//2-230)
        printt(Language.list[39], sw//2-520, sh//2-175), printt(Language.list[40], sw//2-270, sh//2-175)
        printt(Language.list[41], sw//2-520, sh//2-120)

        pygame.draw.rect(screen, black, (sw//2+30, sh//2-255, 265, 375), 1), pygame.draw.rect(screen, black, (sw//2+305, sh//2-255, 265, 375), 1)
        centerprint("{} / {}".format(paperpage+1, pagecount), sw//2+40, sh//2-280, 20, 20, black)
        odd = True
        if pagecount % 2 != 0 and pagecount < paperpage+2: odd = False
        if odd: centerprint("{} / {}".format(paperpage+2, pagecount), sw//2+540, sh//2-280, 20, 20, black)

        preview0 = pygame.transform.scale(pygame.image.load("./Layout/Preview 0.png"), (263, 372))
        screen.blit(preview0, (sw//2+31, sh//2-253))
        try:
            preview1 = pygame.transform.scale(pygame.image.load("./Layout/Preview 1.png"), (263, 372))
            if odd: screen.blit(preview1, (sw//2+306, sh//2-253))
        except FileNotFoundError: pass

        Buttons, x, y, counter = [], sw//2-580, sh//2-55, 0
        for i in range(27):
            i += page * 27

            if counter == 9:
                x, counter = sw//2-580, 0
                y += 55

            try:
                Buttons.append(Button(str(i + 1), "sBlue", (47, 42)))
                Buttons[i - page * 27].show(mouse, x, y, Active[i])
            except IndexError: break

            x += 60
            counter += 1

        Return.show(mouse, 30, sh-80), Print.show(mouse, sw-225, sh-80)
        Column1.show(mouse, sw//2-580, sh//2-240, pressed=column), Column2.show(mouse, sw//2-330, sh//2-240, pressed=not column)
        Answer1.show(mouse, sw//2-580, sh//2-185, pressed=feedback), Answer2.show(mouse, sw//2-330, sh//2-185, pressed=not feedback)
        All1.show(mouse, sw//2-580, sh//2-130, pressed=allQuestions)
        Page1.show(mouse, sw//2-580, sh//2+160, page > 0), Page2.show(mouse, sw//2-160, sh//2+160, page + 1 != pages and page + 1 < pages != 0, mirror=True)
        Page3.show(mouse, sw//2+30, sh//2+160, paperpage > 0), Page4.show(mouse, sw//2+460, sh//2+160, paperpage + 1 != pagecount and paperpage + 2 < pagecount != 0, mirror=True)

        pygame.display.update(), clock.tick(fps)


def menuquest(reset=True):
    global user, y, digit, x, life, coin, Rect, score, Timer, a, b, c, d, total

    Skip = Button(Language.list[15], "Yellow"); Exit = Button(Language.list[8], "Salmon")
    Games = Button(Language.list[16], "Yellow"); GiveUp = Button(Language.list[14], "Salmon")
    A = Button(" ", "Answer", (512, 75)); B = Button(" ", "Answer", (512, 75))
    C = Button(" ", "Answer", (512, 75)); D = Button(" ", "Answer", (512, 75))

    if reset: Timer = Time()
    ABCD, alternatives, state, correct = [A, B, C, D], ["a", "b", "c", "d"], [True, True, True, True], False

    while True:
        mouse = pygame.mouse.get_pos()
        sw, sh = screen.get_size()

        A.set_text(Quiz[x].answer[0]); B.set_text(Quiz[x].answer[1])
        C.set_text(Quiz[x].answer[2]); D.set_text(Quiz[x].answer[3])

        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                if event.w < 1280: event.w = 1280
                if event.h < 720: event.h = 720
                pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            for i in range(4):
                if ABCD[i].click(event, state[i]):
                    if Quiz[x].check(alternatives[i]): correct = True
                    else: life -= 1; state[i] = False

            if Skip.click(event, coin > 0):
                coin -= 1; Timer.reset(); total -= 1
                state = [True, True, True, True]
                x += 1
                if x >= len(Quiz): endmenu(True)

            elif GiveUp.click(event): confirmationmenu(giveup=True)
            elif Exit.click(event) or event.type == pygame.QUIT:
                with open("./Quizzes/{}.pkl".format(quiz_file), "rb") as f:
                    Quiz1, life1, coin1, temp0, temp1, temp2, temp3, temp4 = pickle.load(f)
                with open("./Quizzes/{}.pkl".format(quiz_file), "wb") as f:
                    pickle.dump([Quiz1, life1, coin1, x, total, life, score, coin], f)
                if event.type == pygame.QUIT: sys.exit()
                else: mainmenu()
            elif Games.click(event): minigames()

        if correct:
            score += 1; Timer.reset(); total -= 1
            state = [True, True, True, True]
            x += 1
            if x >= len(Quiz): endmenu(True)
            correct = False

        if life <= 0: endmenu(False)

        screen.fill(white)

        draw('./Layout/Life.png', 30, 28), centerprint(life, 72, 34, 85, 40, red)
        draw('./Layout/Score.png', 189, 25), centerprint(score, 222, 33, 85, 40, prismarine)
        draw('./Layout/Coin.png', 341, 24), centerprint(coin, 387, 33, 80, 40, yellow)
        draw('./Layout/Remaining.png', 497, 28), centerprint(total, 517, 34, 85, 40, darkgray)
        draw('./Layout/Time.png', sw-185, 30), centerprint(Timer.get_time(), sw-162, 34, 130, 40, brown)
        ptext.draw(Quiz[x].question, centerx=sw//2, top=sh*.24-55, color=black, width=1220, align="center", fontname="./Fonts/myriad-pro-8.otf", fontsize=18)

        font = "./Fonts/myriad-pro-8.otf"
        Games.show(mouse, sw-225, sh-80), GiveUp.show(mouse, 30, sh-80), Skip.show(mouse, sw-440, sh-80, coin > 0), Exit.show(mouse, 245, sh-80)
        A.show(mouse, sw//2-532, sh*.24+245, state[0], lh=0.9, fontname=font, f_size=18), B.show(mouse, sw//2-532, sh*.24+335, state[1], lh=0.9, fontname=font, f_size=18)
        C.show(mouse, sw//2+20, sh*.24+245, state[2], lh=0.9, fontname=font, f_size=18), D.show(mouse, sw//2+20, sh*.24+335, state[3], lh=0.9, fontname=font, f_size=18)

        pygame.display.update(), Timer.update(), clock.tick(fps)


def minigames():
    global coin

    TicTacToe = Button(Language.list[21], "Blue"); Hangman = Button(Language.list[22], "Blue"); Minesweeper = Button(Language.list[23], "Blue")
    Maze = Button(Language.list[24], "Blue"); Sudoku = Button(Language.list[25], "Blue"); Memory = Button(Language.list[26], "Blue")
    Return = Button(Language.list[1], "Salmon")

    while True:
        mouse = pygame.mouse.get_pos()
        sw, sh = screen.get_size()

        for event in pygame.event.get():
            window(event)

            if Return.click(event): menuquest(False)

            elif TicTacToe.click(event) and tictactoe(): coin += 1; return
            elif Minesweeper.click(event) and minesweeper(): coin += 1; return
            elif Hangman.click(event) and hangman(config["idiom"]): coin += 1; return
            elif Maze.click(event) and maze(): coin += 1; return
            elif Sudoku.click(event) and sudoku(): coin += 1; return
            elif Memory.click(event) and memory(): coin += 1; return

        screen.fill(white)

        centerprint(Language.list[33], sw//2-235, sh*.2, 470, 25, black, font24)

        TicTacToe.show(mouse, sw//2-317, sh//2-55), Hangman.show(mouse, sw//2-97, sh//2-55), Minesweeper.show(mouse, sw//2+122, sh//2-55)
        Maze.show(mouse, sw//2-317, sh//2), Sudoku.show(mouse, sw//2-97, sh//2), Memory.show(mouse, sw//2+122, sh//2)
        Return.show(mouse, 30, sh-80)

        pygame.display.update(), Timer.update(), clock.tick(fps)


def endmenu(victory):
    global Quiz, life, coin, x, total, score
    Again = Button(Language.list[17], "bBlue", (407, 42)); Start = Button(Language.list[18], "bBlue", (407, 42))

    with open("./Quizzes/{}.pkl".format(quiz_file), "rb") as f:
        Quiz1, life1, coin1, temp0, temp1, temp2, temp3, temp4 = pickle.load(f)
    with open("./Quizzes/{}.pkl".format(quiz_file), "wb") as f:
        pickle.dump([Quiz1, life1, coin1, 0, len(Quiz), 0, 0, 0], f)

    while True:
        mouse = pygame.mouse.get_pos()
        sw, sh = screen.get_size()

        for event in pygame.event.get():
            window(event)

            if Again.click(event):
                with open("./Quizzes/{}.pkl".format(quiz_file), "rb") as f:
                    Quiz, life, coin, x, total, life2, score, coin2 = pickle.load(f)
                if life2 != 0: life = life2
                if coin2 != 0: coin = coin2
                menuquest()

            elif Start.click(event): mainmenu()

        screen.fill(white)

        if victory: draw("./Layout/Victory.png", sw//2-288, sh*.1+45), centerprint(Language.list[19], sw//2-225, sh*.1+45, 451, 74, font=font36)
        else: draw("./Layout/Defeat.png", sw//2-288, sh*.1+45), centerprint(Language.list[20], sw//2-225, sh*.1+45, 451, 74, font=font36)
        draw("./Layout/Score Result.png", sw//2-177, sh*.1+140), centerprint("{} / {}".format(score, len(Quiz)), sw//2-147, sh*.1+140, 296, 39)

        Again.show(mouse, sw//2-204, sh//2), Start.show(mouse, sw//2-204, sh//2+55)

        pygame.display.update(), clock.tick(fps)


Language = Languages()
config = json.load(open("config.json", "r"))
exec("Language.{}()".format(config["idiom"]))
mainmenu()
