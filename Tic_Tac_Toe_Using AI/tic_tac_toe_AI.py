from tkinter import *

# ---------------- WINDOW ----------------
root = Tk()
root.title("Tic Tac Toe")
root.geometry("500x650")
root.config(bg="#f8fafc")

# ---------------- GLOBALS ----------------
buttons = []
current_player = "X"
game_over = False
mode = None

p1_name = ""
p2_name = ""
p1_symbol = "X"
p2_symbol = "O"

# Player colors (IMPORTANT FIX)
p1_color = "#2563eb"   # Blue (YOU)
p2_color = "#dc2626"   # Red (Opponent)

x_score = 0
o_score = 0
draw_score = 0

# ---------------- COLORS ----------------
bg_color = "#f8fafc"
btn_color = "#e2e8f0"
hover_color = "#cbd5f5"
text_color = "#000000"

# ---------------- LOGIC ----------------
def get_board():
    return [btn["text"] if btn["text"] != "" else " " for btn in buttons]

def win_check(b, c):
    combos = [(0,1,2),(3,4,5),(6,7,8),
              (0,3,6),(1,4,7),(2,5,8),
              (0,4,8),(2,4,6)]
    return any(b[a]==b[b1]==b[c1]==c for a,b1,c1 in combos)

def is_draw(b):
    return " " not in b

# ---------------- SMART AI ----------------
def ai_move():
    board = get_board()

    # 1. WIN
    for i in range(9):
        if board[i] == " ":
            board[i] = p2_symbol
            if win_check(board, p2_symbol):
                board[i] = " "
                return i
            board[i] = " "

    # 2. BLOCK
    for i in range(9):
        if board[i] == " ":
            board[i] = p1_symbol
            if win_check(board, p1_symbol):
                board[i] = " "
                return i
            board[i] = " "

    # 3. CENTER
    if board[4] == " ":
        return 4

    # 4. CORNERS
    for i in [0,2,6,8]:
        if board[i] == " ":
            return i

    # 5. ANY
    for i in range(9):
        if board[i] == " ":
            return i

# ---------------- SCORE ----------------
def update_score(winner):
    global x_score, o_score, draw_score

    if winner == p1_symbol:
        x_score += 1
    elif winner == p2_symbol:
        o_score += 1
    else:
        draw_score += 1

    score_label.config(
        text=f"{p1_symbol}: {x_score}   {p2_symbol}: {o_score}   Draw: {draw_score}"
    )

# ---------------- GAME ----------------
def on_click(i):
    global current_player, game_over

    if game_over or buttons[i]["text"] != "":
        return

    # Player move
    buttons[i]["text"] = current_player
    buttons[i]["fg"] = p1_color if current_player == p1_symbol else p2_color

    board = get_board()

    # WIN
    if win_check(board, current_player):
        winner = p1_name if current_player == p1_symbol else p2_name
        status.config(text=f"{winner} Wins 🎉")
        update_score(current_player)
        game_over = True
        return

    # DRAW
    if is_draw(board):
        status.config(text="Draw 🤝")
        update_score("Draw")
        game_over = True
        return

    # SWITCH
    current_player = p2_symbol if current_player == p1_symbol else p1_symbol

    # AI TURN
    if mode == "AI" and current_player == p2_symbol:
        status.config(text="Computer thinking...")
        root.after(300, ai_turn)
    else:
        turn_name = p1_name if current_player == p1_symbol else p2_name
        status.config(text=f"{turn_name}'s Turn ({current_player})")

def ai_turn():
    global current_player, game_over

    if game_over:
        return

    move = ai_move()
    if move is None:
        return

    buttons[move]["text"] = p2_symbol
    buttons[move]["fg"] = p2_color

    board = get_board()

    if win_check(board, p2_symbol):
        status.config(text="Computer Wins 🤖")
        update_score(p2_symbol)
        game_over = True
        return

    if is_draw(board):
        status.config(text="Draw 🤝")
        update_score("Draw")
        game_over = True
        return

    current_player = p1_symbol
    status.config(text=f"{p1_name}'s Turn ({p1_symbol})")

def reset_game():
    global current_player, game_over

    current_player = p1_symbol
    game_over = False

    for b in buttons:
        b.config(text="", state=NORMAL, bg=btn_color)

    status.config(text=f"{p1_name}'s Turn ({p1_symbol})")

# ---------------- UI ----------------
def on_hover(e):
    e.widget.config(bg=hover_color)

def on_leave(e):
    e.widget.config(bg=btn_color)

def create_board():
    global buttons
    buttons = []

    for i in range(9):
        btn = Button(root,
                     text="",
                     font=("Arial", 28, "bold"),
                     width=6,
                     height=3,
                     bg=btn_color,
                     fg=text_color,
                     bd=0,
                     command=lambda i=i: on_click(i))

        btn.grid(row=i//3 + 2, column=i%3, padx=10, pady=10)
        btn.bind("<Enter>", on_hover)
        btn.bind("<Leave>", on_leave)

        buttons.append(btn)

# ---------------- START ----------------
def start_game():
    for w in root.winfo_children():
        w.destroy()

    Label(root,
          text="Tic Tac Toe",
          font=("Arial", 26, "bold"),
          bg=bg_color, fg=text_color).grid(row=0, column=0, columnspan=3)

    global score_label
    score_label = Label(root,
        text=f"{p1_symbol}: 0   {p2_symbol}: 0   Draw: 0",
        font=("Arial", 14, "bold"),
        bg=bg_color, fg=text_color)
    score_label.grid(row=1, column=0, columnspan=3)

    create_board()

    global status
    status = Label(root,
        text=f"{p1_name}'s Turn ({p1_symbol})",
        font=("Arial", 16, "bold"),
        bg=bg_color, fg=text_color)
    status.grid(row=5, column=0, columnspan=3)

    Button(root,
           text="Restart",
           font=("Arial", 14),
           command=reset_game,
           bg="#cbd5f5").grid(row=6, column=0, columnspan=3, pady=10)

# ---------------- SETUP ----------------
def show_setup(selected):
    global mode
    mode = selected

    for w in root.winfo_children():
        w.destroy()

    Label(root, text="Setup Game",
          font=("Arial", 20, "bold"),
          bg=bg_color, fg=text_color).pack(pady=20)

    p1 = Entry(root, font=("Arial", 14))
    p1.pack(pady=5)
    p1.insert(0, "Player 1")

    p2 = Entry(root, font=("Arial", 14))
    p2.pack(pady=5)

    if mode == "AI":
        p2.insert(0, "Computer")
    else:
        p2.insert(0, "Player 2")

    symbol = StringVar(value="X")

    Radiobutton(root, text="X", variable=symbol, value="X",
                bg=bg_color, fg=text_color).pack()

    Radiobutton(root, text="O", variable=symbol, value="O",
                bg=bg_color, fg=text_color).pack()

    def start():
        global p1_name, p2_name, p1_symbol, p2_symbol

        p1_name = p1.get()
        p2_name = p2.get()

        p1_symbol = symbol.get()
        p2_symbol = "O" if p1_symbol == "X" else "X"

        start_game()

    Button(root,
           text="Start Game",
           font=("Arial", 14),
           bg="#cbd5f5",
           command=start).pack(pady=20)

# ---------------- MENU ----------------
Label(root,
      text="Tic Tac Toe",
      font=("Arial", 28, "bold"),
      bg=bg_color, fg=text_color).pack(pady=40)

Button(root,
       text="Player vs Player",
       font=("Arial", 14),
       command=lambda: show_setup("PVP"),
       bg="#e2e8f0").pack(pady=10)

Button(root,
       text="Player vs Computer",
       font=("Arial", 14),
       command=lambda: show_setup("AI"),
       bg="#e2e8f0").pack(pady=10)

root.mainloop()