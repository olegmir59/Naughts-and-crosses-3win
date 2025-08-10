import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random

window = tk.Tk()
window.title("Крестики-нолики")
window.geometry("1280x1280")  # Увеличили размер окна, чтобы уместить игровое поле и фон

current_player = "X"
buttons = []
player1_score = 0
player2_score = 0
max_wins = 3  # Количество побед для победы в серии
game_mode = "player_vs_player"  # Режим игры: player_vs_player или player_vs_computer

# Загрузка фона
background_image = Image.open("Фон.jpg")
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(window, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

def check_winner():
    for i in range(3):
        if buttons[i][0]["text"] == buttons[i][1]["text"] == buttons[i][2]["text"] != "":
            return True
        if buttons[0][i]["text"] == buttons[1][i]["text"] == buttons[2][i]["text"] != "":
            return True
    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] != "":
        return True
    if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] != "":
        return True
    return False

def is_board_full():
    for row in buttons:
        for button in row:
            if button['text'] == "":
                return False
    return True

def on_click(row, col):
    global current_player
    if buttons[row][col]['text'] != "":
        return
    buttons[row][col]['text'] = current_player
    if check_winner():
        messagebox.showinfo("Игра окончена", f"Игрок {current_player} победил!")
        update_score(current_player)
        if player1_score == max_wins or player2_score == max_wins:
            messagebox.showinfo("Игра окончена", f"Игрок {current_player} выиграл серию!")
            window.quit()
        else:
            reset_game()
    elif is_board_full():
        messagebox.showinfo("Игра окончена", "Ничья!")
        reset_game()
    else:
        if game_mode == "player_vs_computer" and current_player == "X":
            computer_move()
        else:
            current_player = "O" if current_player == "X" else "X"

def computer_move():
    global current_player
    # Алгоритм минимакс с альфа-бета отсечением
    best_move = None
    best_score = -float('inf')
    for i in range(3):
        for j in range(3):
            if buttons[i][j]['text'] == "":
                buttons[i][j]['text'] = "O"
                score = minimax(buttons, 0, False, -float('inf'), float('inf'))
                buttons[i][j]['text'] = ""
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    buttons[best_move[0]][best_move[1]]['text'] = "O"
    if check_winner():
        messagebox.showinfo("Игра окончена", "Компьютер победил!")
        update_score("O")
        if player1_score == max_wins or player2_score == max_wins:
            messagebox.showinfo("Игра окончена", f"Игрок {current_player} выиграл серию!")
            window.quit()
        else:
            reset_game()
    elif is_board_full():
        messagebox.showinfo("Игра окончена", "Ничья!")
        reset_game()
    else:
        current_player = "X"

def minimax(buttons, depth, is_maximizing, alpha, beta):
    if check_winner():
        if is_maximizing:
            return -1
        else:
            return 1
    if is_board_full():
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if buttons[i][j]['text'] == "":
                    buttons[i][j]['text'] = "O"
                    score = minimax(buttons, depth + 1, False, alpha, beta)
                    buttons[i][j]['text'] = ""
                    best_score = max(best_score, score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if buttons[i][j]['text'] == "":
                    buttons[i][j]['text'] = "X"
                    score = minimax(buttons, depth + 1, True, alpha, beta)
                    buttons[i][j]['text'] = ""
                    best_score = min(best_score, score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break
        return best_score

def update_score(winner):
    global player1_score, player2_score
    if winner == "X":
        player1_score += 1
    elif winner == "O":
        player2_score += 1
    score_label.config(text=f"X: {player1_score}   O: {player2_score}")

def reset_game():
    global current_player
    current_player = "X"
    for row in buttons:
        for button in row:
            button['text'] = ""

def choose_game_mode():
    global game_mode
    choice = messagebox.askyesno("Выбор режима игры", "Вы хотите играть с компьютером?")
    if choice:
        game_mode = "player_vs_computer"
    else:
        game_mode = "player_vs_player"

# Создание кнопок
for i in range(3):
    row = []
    for j in range(3):
        btn = tk.Button(window, text="", font=("Arial", 20), width=5, height=2, command=lambda r=i, c=j: on_click(r, c))
        btn.grid(row=i, column=j+10)  # Переместили кнопки на 300 точек вправо
        row.append(btn)
    buttons.append(row)

# Кнопка сброса
reset_button = tk.Button(window, text="Сброс", font=("Arial", 14), command=reset_game)
reset_button.grid(row=3, column=10, columnspan=3)

# Счетчик побед
score_label = tk.Label(window, text=f"X: {player1_score}   O: {player2_score}", font=("Arial", 14))
score_label.grid(row=4, column=10, columnspan=3)

# Выбор режима игры
choose_game_mode()

window.mainloop()