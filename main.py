import tkinter as tk
from tkinter import messagebox

window = tk.Tk()
window.title("Крестики-нолики")
window.geometry("300x350")

current_player = "X"
player1_score = 0
player2_score = 0

buttons = []


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
        reset_game()
    elif is_board_full():
        messagebox.showinfo("Игра окончена", "Ничья!")
        reset_game()
    else:
        current_player = "O" if current_player == "X" else "X"


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


def choose_player():
    global current_player
    choice = messagebox.askyesno("Выбор игрока", "Вы хотите играть крестиками?")
    if choice:
        current_player = "X"
    else:
        current_player = "O"


# Создание кнопок
for i in range(3):
    row = []
    for j in range(3):
        btn = tk.Button(window, text="", font=("Arial", 20), width=5, height=2, command=lambda r=i, c=j: on_click(r, c))
        btn.grid(row=i, column=j)
        row.append(btn)
    buttons.append(row)

# Кнопка сброса
reset_button = tk.Button(window, text="Сброс", font=("Arial", 14), command=reset_game)
reset_button.grid(row=3, column=0, columnspan=3)

# Счетчик побед
score_label = tk.Label(window, text=f"X: {player1_score}   O: {player2_score}", font=("Arial", 14))
score_label.grid(row=4, column=0, columnspan=3)

# Выбор игрока
choose_player()

window.mainloop()
