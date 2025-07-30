import tkinter as tk
from tkinter import messagebox, simpledialog
import time
import random
import threading
import os
from PIL import Image, ImageTk
import io

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ModuleNotFoundError:
    OLLAMA_AVAILABLE = False

def open_chatbot(self):
    self.chat_window = tk.Toplevel(self.root)
    self.chat_window.title("Chatbot")
    self.chat_window.geometry("500x550")
    
    
    try:
        bg_image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "background.jpg")
        if os.path.exists(bg_image_path):
            # Load and resize the image
            bg_image = Image.open(bg_image_path)
            bg_image = bg_image.resize((500, 550), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            
            # Create a canvas with the image
            self.bg_canvas = tk.Canvas(self.chat_window, width=500, height=550)
            self.bg_canvas.pack(fill="both", expand=True)
            self.bg_canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
            
            # Create a frame on top of the canvas for content
            content_frame = tk.Frame(self.bg_canvas, bg='black')
            content_frame.configure(bg='black', bd=0, highlightthickness=0)
            content_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)
            
            chat_label = tk.Label(
                content_frame, 
                text=f"Hi {self.user_name}, I am Evelyn!\nAsk me anything.",
                font=("Arial", 12),
                bg='black',
                fg='white'
            )
            chat_label.pack(pady=10)
        else:
            # Fallback if image doesn't exist
            chat_label = tk.Label(
                self.chat_window, 
                text=f"Hi {self.user_name}, I am Evelyn!\nAsk me anything.",
                font=("Arial", 12)
            )
            chat_label.pack(pady=10)
            content_frame = self.chat_window
    except Exception as e:
        print(f"Error loading background image: {e}")
        chat_label = tk.Label(
            self.chat_window, 
            text=f"Hi {self.user_name}, I am Evelyn!\nAsk me anything.",
            font=("Arial", 12)
        )
        chat_label.pack(pady=10)
        content_frame = self.chat_window

    # Frame for chat history and scrollbar
    chat_frame = tk.Frame(content_frame, bg='black')
    chat_frame.pack(fill="both", expand=True, padx=10, pady=(0,10))

    self.chat_history = tk.Text(
        chat_frame, 
        width=60, 
        height=25, 
        font=("Arial", 12), 
        bg="#101010", 
        fg="white",
        state="disabled", 
        wrap="word"
    )
    self.chat_history.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(chat_frame, command=self.chat_history.yview)
    scrollbar.pack(side="right", fill="y")
    self.chat_history['yscrollcommand'] = scrollbar.set

    # Frame for entry and send button
    entry_frame = tk.Frame(content_frame, bg='black')
    entry_frame.pack(fill="x", padx=10, pady=(0,10))

    self.chat_entry = tk.Entry(entry_frame, width=45, bg='#202020', fg='white', insertbackground='white')
    self.chat_entry.pack(side="left", fill="x", expand=True, padx=(0,5))
    self.chat_entry.focus_set()
    self.chat_entry.bind("<Return>", self.send_message)

    send_button = tk.Button(entry_frame, text="Send", command=self.send_message, bg='#303030', fg='white')
    send_button.pack(side="right")

def send_message(self, event=None):
    user_input = self.chat_entry.get().strip()
    if not user_input:
        messagebox.showwarning("Evelyn", "Please enter a message.")
        return

    # Display user message
    self.chat_history.config(state="normal")
    self.chat_history.insert(tk.END, f"You: {user_input}\n")
    self.chat_history.config(state="disabled")
    self.chat_history.see(tk.END)

    self.chat_entry.delete(0, tk.END)

    def fetch_response():
        response = self.get_chatbot_response(user_input)
        self.chat_history.config(state="normal")
        self.chat_history.insert(tk.END, f"Evelyn: {response}\n\n")
        self.chat_history.config(state="disabled")
        self.chat_history.see(tk.END)

    threading.Thread(target=fetch_response, daemon=True).start()


ROCK = "Rock"
PAPER = "Paper"
SCISSORS = "Scissors"

WINNING_MSG = "You win!"
LOSE_MSG = "You lose!"
TIE_MSG = "It's a tie!"
SCISSORS_BEATS_PAPER_MSG = "Kainchi kagaj ke upar gire, ya kagaj kainchi pe katna toh kagaj ko hi hai!"
ROCK_BEATS_SCISSORS_MSG = "pathar ko kaat sake aesi koi kainchi nahin bani!"
PAPER_BEATS_ROCK_MSG = "Paper covers rock, just like you covers your emotion when seeing her!"

CHALLENGER = "Challenger"
DEFENDER = "Defender"
EMPTY = ""

CHALLENGER_QUOTES = [
    "You're unstoppable, Challenger!",
    "You've got this, Challenger! Keep going!",
    "Challenger, the challenge is yours to win!"
]
DEFENDER_QUOTES = [
    "Excellent defense, Defender!",
    "Well played, Defender! Victory is near!",
    "Your strategy is flawless, Defender!"
]

class OSPrototype:
    def __init__(self, root):
        self.root = root
        self.root.title("Prototype OS")
        self.user_name = ""
        self.startup_screen()

    def startup_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.geometry("400x200")
        label = tk.Label(self.root, text="Enter your name:")
        label.pack(pady=10)
        
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack(pady=5)
        self.name_entry.focus_set()
        self.root.bind("<Return>", self.main_interface)
        
        submit_button = tk.Button(self.root, text="Submit", command=self.main_interface)
        submit_button.pack(pady=10)

    def main_interface(self, event=None):
        self.user_name = self.name_entry.get().strip()
        if not self.user_name:
            messagebox.showerror("Error", "Please enter a name.")
            return
        
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Set window properties
        self.root.geometry("800x600")
        self.root.title("Stylish Python OS Interface")
        
        # Load background image
        try:
            bg_image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "background.jpg")
            if os.path.exists(bg_image_path):
                bg_image = Image.open(bg_image_path)
                bg_image = bg_image.resize((800, 600), Image.LANCZOS)
                self.bg_photo = ImageTk.PhotoImage(bg_image)
                
                # Create a canvas with the image
                self.bg_canvas = tk.Canvas(self.root, width=800, height=600, highlightthickness=0)
                self.bg_canvas.pack(fill="both", expand=True)
                self.bg_canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
                
                # Create a dark overlay for the clock (navy blue with border)
                clock_frame = tk.Frame(self.bg_canvas, bg='#0a1428', bd=0)
                clock_frame.place(x=500, y=70, width=240, height=40, anchor="center")
                clock_frame.configure(highlightbackground="#1a3a5a", highlightthickness=1)
                
                # Create clock display
                self.clock_label = tk.Label(clock_frame, text="", font=("Arial", 14, "bold"), 
                                          bg='#0a1428', fg="#ffffff")
                self.clock_label.pack(fill="both", expand=True)
                self.update_time()
                
                # Create quote display with cyan text
                quote_frame = tk.Frame(self.bg_canvas, bg='#000000', bd=0, highlightthickness=0)
                quote_frame.place(relx=0.5, y=120, width=500, height=30, anchor="center")
                
                self.quote_label = tk.Label(quote_frame, text="", font=("Arial", 12), 
                                           bg='#000000', fg="#00cccc")
                self.quote_label.pack(fill="both", expand=True)
                self.update_quote()
                
                # Create stylish buttons on the left side
                buttons = ["Utilities", "Games", "About Us", "Open Chatbot"]
                y_position = 260
                
                for btn in buttons:
                    btn_frame = tk.Frame(self.bg_canvas, bg='#0a1428', bd=0)
                    btn_frame.place(x=130, y=y_position, width=160, height=50, anchor="center")
                    btn_frame.configure(highlightbackground="#1a3a5a", highlightthickness=1)
                    
                    button = tk.Button(btn_frame, text=btn, font=("Arial", 12, "bold"),
                                     bg='#0a1428', fg="white", bd=0, activebackground="#1a3a5a",
                                     activeforeground="white", cursor="hand2",
                                     command=lambda b=btn: self.handle_button(b))
                    button.pack(fill="both", expand=True)
                    y_position += 70
            else:
                # Fallback if image doesn't exist
                self.default_interface()
        except Exception as e:
            print(f"Error loading background image: {e}")
            self.default_interface()
    
    def default_interface(self):
        """Fallback interface if the stylish one fails"""
        self.root.geometry("600x400")
        left_frame = tk.Frame(self.root, bg="gray", width=150, height=400)
        left_frame.pack(side="left", fill="y")
        
        buttons = ["Games", "Utilities", "About Us", "Exit"]
        for btn in buttons:
            button = tk.Button(left_frame, text=btn, width=15, height=2, 
                               command=lambda b=btn: self.handle_button(b))
            button.pack(pady=5)

        self.clock_label = tk.Label(self.root, text="", bg="lightgray", width=40, height=4)
        self.clock_label.pack(pady=10)
        self.update_time()
        
        chat_button = tk.Button(self.root, text="Open Chatbot", command=self.open_chatbot)
        chat_button.pack(pady=10)
        
        self.quote_label = tk.Label(self.root, text="", bg="lightgray", width=40, height=3)
        self.quote_label.pack(pady=5)
        self.update_quote()

    def handle_button(self, button_name):
        if button_name == "Exit":
            self.root.quit()
        elif button_name == "Utilities":
            self.open_utilities()
        elif button_name == "About Us":
            self.show_about_us()
        elif button_name == "Open Chatbot":
            self.open_chatbot()
        else:
            self.open_games()

    def open_games(self):
        self.games_window = tk.Toplevel(self.root)
        self.games_window.title("Games")
        self.games_window.geometry("400x300")

        buttons = [
            ("Rock, Paper, Scissors", self.open_rock_paper_scissors),
            ("Tic Tac Toe", self.open_tic_tac_toe),
            ("Number Guessing Game", self.open_number_guessing_game)
        ]
        
        for text, command in buttons:
            btn = tk.Button(self.games_window, text=text, width=20, command=command)
            btn.pack(pady=5)

    def open_rock_paper_scissors(self):
        self.rock_paper_scissors_window = tk.Toplevel(self.root)
        self.rock_paper_scissors_window.title("Rock, Paper, Scissors")

        intro_label = tk.Label(self.rock_paper_scissors_window, text="Let's play Rock, Paper, Scissors!", font=("Helvetica", 14))
        intro_label.pack()

        self.result_label = tk.Label(self.rock_paper_scissors_window, text="Choose an option below to start the game.", font=("Helvetica", 12))
        self.result_label.pack()

        rock_button = tk.Button(self.rock_paper_scissors_window, text="Rock", width=20, command=lambda: self.start_rock_paper_scissors(ROCK))
        rock_button.pack(pady=5)

        paper_button = tk.Button(self.rock_paper_scissors_window, text="Paper", width=20, command=lambda: self.start_rock_paper_scissors(PAPER))
        paper_button.pack(pady=5)

        scissors_button = tk.Button(self.rock_paper_scissors_window, text="Scissors", width=20, command=lambda: self.start_rock_paper_scissors(SCISSORS))
        scissors_button.pack(pady=5)

        quit_button = tk.Button(self.rock_paper_scissors_window, text="Quit", width=20, command=self.rock_paper_scissors_window.destroy)
        quit_button.pack(pady=20)

    def start_rock_paper_scissors(self, user_choice):
        evelyn_choice = random.choice([ROCK, PAPER, SCISSORS])
        if user_choice == evelyn_choice:
            result = TIE_MSG
        elif user_choice == ROCK and evelyn_choice == SCISSORS:
            result = WINNING_MSG + "\n" + ROCK_BEATS_SCISSORS_MSG
        elif user_choice == PAPER and evelyn_choice == ROCK:
            result = WINNING_MSG + "\n" + PAPER_BEATS_ROCK_MSG
        elif user_choice == SCISSORS and evelyn_choice == PAPER:
            result = WINNING_MSG + "\n" + SCISSORS_BEATS_PAPER_MSG
        else:
            result = LOSE_MSG
        self.result_label.config(text=f"You chose: {user_choice}\nEvelyn chose: {evelyn_choice}\n{result}")

    def open_tic_tac_toe(self):
        self.tic_tac_toe_window = tk.Toplevel(self.root)
        self.tic_tac_toe_window.title("Tic Tac Toe")

        self.game_board = [EMPTY] * 9
        self.current_turn = CHALLENGER

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for row in range(3):
            for col in range(3):
                self.buttons[row][col] = tk.Button(self.tic_tac_toe_window, text="", font=("Arial", 40), width=5, height=2,
                                                  command=lambda r=row, c=col: self.make_move(r, c))
                self.buttons[row][col].grid(row=row, column=col)

    def make_move(self, row, col):
        index = row * 3 + col
        if self.game_board[index] == EMPTY:
            if self.current_turn == CHALLENGER:
                self.game_board[index] = "X"
            else:
                self.game_board[index] = "O"

            self.buttons[row][col].config(text=self.game_board[index])

            if self.check_for_winner(self.current_turn):
                messagebox.showinfo("Game Over", f"{self.current_turn} wins!\nMotivation: {self.get_quote(self.current_turn)}")
                self.reset_game()
            elif EMPTY not in self.game_board:
                messagebox.showinfo("Game Over", "It's a tie!")
                self.reset_game()
            else:
                self.current_turn = CHALLENGER if self.current_turn == DEFENDER else DEFENDER

    def check_for_winner(self, player):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for condition in win_conditions:
            if self.game_board[condition[0]] == self.game_board[condition[1]] == self.game_board[condition[2]] != EMPTY:
                return True
        return False

    def get_quote(self, player):
        if player == CHALLENGER:
            return CHALLENGER_QUOTES[0]
        else:
            return DEFENDER_QUOTES[0]

    def reset_game(self):
        self.game_board = [EMPTY] * 9
        self.current_turn = CHALLENGER
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text="")

    def open_number_guessing_game(self):
        self.number_guessing_game_window = tk.Toplevel(self.root)
        self.number_guessing_game_window.title("Number Guessing Game")

        welcome_label = tk.Label(self.number_guessing_game_window, text="Welcome to the Number Guessing Game!", font=("Arial", 16))
        welcome_label.pack(pady=10)

        self.result_label = tk.Label(self.number_guessing_game_window, text="Guess a number between 1 and 100.", font=("Arial", 12))
        self.result_label.pack(pady=5)

        self.attempts_label = tk.Label(self.number_guessing_game_window, text="Attempts: 0", font=("Arial", 12))
        self.attempts_label.pack(pady=5)

        guess_label = tk.Label(self.number_guessing_game_window, text="Enter your guess:")
        guess_label.pack(pady=5)

        self.guess_entry = tk.Entry(self.number_guessing_game_window)
        self.guess_entry.pack(pady=5)

        check_button = tk.Button(self.number_guessing_game_window, text="Check Guess", command=self.check_guess)
        check_button.pack(pady=10)

        start_button = tk.Button(self.number_guessing_game_window, text="Start New Game", command=self.start_game)
        start_button.pack(pady=10)

    def start_game(self):
        self.target_number = random.randint(1, 100)
        self.attempts = 0
        self.result_label.config(text="Guess a number between 1 and 100.")
        self.attempts_label.config(text="Attempts: 0")
        self.guess_entry.delete(0, tk.END)

    def check_guess(self):
        try:
            guess = int(self.guess_entry.get())
            self.attempts += 1
            if guess < self.target_number:
                self.result_label.config(text="Too low! Try again.")
            elif guess > self.target_number:
                self.result_label.config(text="Too high! Try again.")
            else:
                self.result_label.config(text=f"Correct! You guessed the number in {self.attempts} attempts.")
        except ValueError:
            self.result_label.config(text="Please enter a valid number.")
        self.attempts_label.config(text=f"Attempts: {self.attempts}")

    def open_snake_game(self):
        messagebox.showinfo("Snake Game", "Snake Game feature coming soon!")

    def open_chatbot(self):
        self.chat_window = tk.Toplevel(self.root)
        self.chat_window.title("Chatbot")
        self.chat_window.geometry("500x550")
        
        try:
            bg_image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "background.jpg")
            if os.path.exists(bg_image_path):
                # Load and resize the image
                bg_image = Image.open(bg_image_path)
                bg_image = bg_image.resize((500, 550), Image.LANCZOS)
                self.bg_photo = ImageTk.PhotoImage(bg_image)
                
                # Create a canvas with the image
                self.bg_canvas = tk.Canvas(self.chat_window, width=500, height=550)
                self.bg_canvas.pack(fill="both", expand=True)
                self.bg_canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
                
                # Create a frame on top of the canvas for content
                content_frame = tk.Frame(self.bg_canvas, bg='black')
                content_frame.configure(bg='black', bd=0, highlightthickness=0)
                content_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)
                
                chat_label = tk.Label(
                    content_frame, 
                    text=f"Hi {self.user_name}, I am Evelyn!\nAsk me anything.",
                    font=("Arial", 12),
                    bg='black',
                    fg='white'
                )
                chat_label.pack(pady=10)
            else:
                # Fallback if image doesn't exist
                chat_label = tk.Label(
                    self.chat_window, 
                    text=f"Hi {self.user_name}, I am Evelyn!\nAsk me anything.",
                    font=("Arial", 12)
                )
                chat_label.pack(pady=10)
                content_frame = self.chat_window
        except Exception as e:
            print(f"Error loading background image: {e}")
            chat_label = tk.Label(
                self.chat_window, 
                text=f"Hi {self.user_name}, I am Evelyn!\nAsk me anything.",
                font=("Arial", 12)
            )
            chat_label.pack(pady=10)
            content_frame = self.chat_window

        # Frame for chat history and scrollbar
        chat_frame = tk.Frame(content_frame, bg='black')
        chat_frame.pack(fill="both", expand=True, padx=10, pady=(0,10))

        self.chat_history = tk.Text(
            chat_frame, 
            width=60, 
            height=25, 
            font=("Arial", 12), 
            bg="#101010", 
            fg="white",
            state="disabled", 
            wrap="word"
        )
        self.chat_history.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(chat_frame, command=self.chat_history.yview)
        scrollbar.pack(side="right", fill="y")
        self.chat_history['yscrollcommand'] = scrollbar.set

        # Frame for entry and send button
        entry_frame = tk.Frame(content_frame, bg='black')
        entry_frame.pack(fill="x", padx=10, pady=(0,10))

        self.chat_entry = tk.Entry(entry_frame, width=45, bg='#202020', fg='white', insertbackground='white')
        self.chat_entry.pack(side="left", fill="x", expand=True, padx=(0,5))
        self.chat_entry.focus_set()
        self.chat_entry.bind("<Return>", self.send_message)

        send_button = tk.Button(entry_frame, text="Send", command=self.send_message, bg='#303030', fg='white')
        send_button.pack(side="right")

    def send_message(self, event=None):
        user_input = self.chat_entry.get().strip()
        if not user_input:
            messagebox.showwarning("Evelyn", "Please enter a message.")
            return

        # Display user message
        self.chat_history.config(state="normal")
        self.chat_history.insert(tk.END, f"You: {user_input}\n")
        self.chat_history.config(state="disabled")
        self.chat_history.see(tk.END)

        self.chat_entry.delete(0, tk.END)

        def fetch_response():
            response = self.get_chatbot_response(user_input)
            self.chat_history.config(state="normal")
            self.chat_history.insert(tk.END, f"Evelyn: {response}\n\n")
            self.chat_history.config(state="disabled")
            self.chat_history.see(tk.END)

        threading.Thread(target=fetch_response, daemon=True).start()

    def get_chatbot_response(self, query):
        if not OLLAMA_AVAILABLE:
            return "Chatbot functionality is unavailable because the 'ollama' module is not installed."
        try:
            response = ollama.generate(model='phi3', prompt=query)
            return response.get('response', "I'm not sure about that. Can you rephrase?")
        except Exception as e:
            return f"Error: {e}"
            
    def update_time(self):
        current_time = time.strftime("%H:%M:%S | %d-%m-%Y")
        self.clock_label.config(text=current_time)
        self.root.after(1000, self.update_time)
    
    def update_quote(self):
        quotes = [
            "Great things never come from comfort zones.",
            "The only way to do great work is to love what you do.",₹
            "Every moment is a fresh beginning.",
            "The purpose of our lives is to be happy.",
            "Dream big, work hard, stay focused."
        ]
        self.quote_label.config(text=random.choice(quotes))
        self.root.after(10000, self.update_quote)
        
    def show_about_us(self):
        about_window = tk.Toplevel(self.root)
        about_window.title("About Us")
        about_window.geometry("450x200")
        
        about_text = ("This advanced multifunctional chatbot is developed by Tarish Sen,"
                      "Hemanshu and Bhisham Thakur, students of the 4th semester, Computer Engineering, "
                      "Government Polytechnic Sundernagar. Designed to enhance user experience, the chatbot "
                      "offers a range of interactive features, including games,user friendly weather updates and much more.")
        
        about_label = tk.Label(about_window, text=about_text, wraplength=400, justify="left", padx=10, pady=10)
        about_label.pack()

    # Utility Functions
    def open_utilities(self):
        utilities_window = tk.Toplevel(self.root)
        utilities_window.title("Utilities")
        utilities_window.geometry("400x300")

        buttons = [
            ("Calculator", self.open_calculator),
            ("Age Finder", self.open_age_finder),
            ("Weather", self.open_weather)
        ]
        
        for text, command in buttons:
            btn = tk.Button(utilities_window, text=text, width=20, command=command)
            btn.pack(pady=5)
    
    def open_calculator(self):
        os.system("calc" if os.name == "nt" else "gnome-calculator")

    def open_age_finder(self):
        birth_year = simpledialog.askinteger("Age Finder", "Enter your birth year:")
        if birth_year:
            age = time.localtime().tm_year - birth_year
            messagebox.showinfo("Age Finder", f"You are {age} years old!")

    
    
    def open_weather(self):
        funny_weather = [
            "It's raining cats and dogs! ",
            "Perfect weather to code! ",
            "Storm incoming! Stay safe! ",
            "Sun's out! Time for a snack! "
        ]
        messagebox.showinfo("Weather", random.choice(funny_weather))

if __name__ == "__main__":
    root = tk.Tk()
    app = OSPrototype(root)
    root.mainloop()
