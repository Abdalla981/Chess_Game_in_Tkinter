from tkinter import *
import chess
import chess.svg
import chess.pgn
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
from PIL import Image, ImageTk
from tkinter.filedialog import asksaveasfilename
from datetime import date

class Chess_Game():
    def __init__(self, root):
        self.root = root
        self.game_frame = Frame(self.root)
        self.start_frame = Frame(self.root)
        self.result = 0
        
        # set board and pgn moves
        self.board = chess.Board()
        self.pgn_moves = chess.pgn.Game()

        # init screen
        self.root.bind("<Escape>", self.exit)
        self.start_screen()
    
    def game_screen(self):
        self.start_frame.destroy()
        self.game_frame = Frame(self.root)
        self.game_frame.pack()

        # Canvas
        self.canvas = Canvas(self.game_frame, width=800, height=800)
        self.canvas.grid(row=0, columnspan = 2)
        self.text = StringVar()
        self.text.set("Input your move then click Enter!\nClick on Control to restart the game!\nClick on Escape to close the Game!")

        # Input
        self.in_label = Label(self.game_frame, text="Your move : ", font=("helvetica", 24))
        self.in_label.grid(row = 1, column=0, pady=10)
        self.user_move = Entry(self.game_frame, width=30)
        self.user_move.grid(row = 1, column=1, pady=10, padx=60)

        # Buttons
        self.btn_restart = Button(self.game_frame, text="New Game", font=("helvetica", 18), command=self.start_screen, width=30)
        self.btn_restart.grid(row=2, column=0, pady=5)
        self.btn_start = Button(self.game_frame, text="Download Game", font=("helvetica", 18), command=self.download, width=30)
        self.btn_start.grid(row=2, column=1, pady=5)

        # Game Message
        self.message = Label(self.game_frame, textvariable=self.text, font=("helvetica", 18))
        self.message.grid(row=3, columnspan=2, pady=10)

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        root.geometry("825x1000")
        # root.resizable(width=False, height=False)
        self.update_canvas()

        #Bind keys
        self.user_move.bind("<Return>", self.player_move)
        self.user_move.bind("<Control_L>", self.undo)
        self.user_move.focus_set()

    def start_screen(self):
        self.game_frame.destroy()
        self.board.reset()
        self.start_frame = Frame(self.root)
        self.start_frame.pack()
        root.title("Chess Game")
        
        # Row 1 (Player Names => Label)
        self.white_label = Label(self.start_frame, text="White Name:", font=("helvetica", 18))
        self.white_label.grid(row=0, column=0, pady=(30,0))
        self.black_label = Label(self.start_frame, text="Black Name:", font=("helvetica", 18))
        self.black_label.grid(row=0, column=1, pady=(30,0))
        
        # Row 2 (Player Names => Entries)
        self.white_name = Entry(self.start_frame, width=30)
        self.white_name.grid(row=1, column=0)
        self.black_name = Entry(self.start_frame, width=30)
        self.black_name.grid(row=1, column=1)

        # Row 3 (Labels)
        self.event_label = Label(self.start_frame, text="Event:", font=("helvetica", 18))
        self.event_label.grid(row=2, column=0, pady=(20,0))
        self.round_label = Label(self.start_frame, text="Round:", font=("helvetica", 18))
        self.round_label.grid(row=2, column=1, pady=(20,0))

        # Row 4 (Entries)
        self.event_name = Entry(self.start_frame, width=30)
        self.event_name.grid(row=3, column=0)
        self.round_number = Entry(self.start_frame, width=30)
        self.round_number.grid(row=3, column=1)

        # Row 5 (Labels)
        self.time_label = Label(self.start_frame, text="Time (in sec):", font=("helvetica", 18))
        self.time_label.grid(row=5, column=0, pady=(20,0))

        # Row 6 (Entries)
        self.time_number = Entry(self.start_frame, width=30)
        self.time_number.grid(row=6, column=0)
        self.start_btn = Button(self.start_frame, text="Start Game", width=30, command=self.on_start)
        self.start_btn.grid(row=6, column=1)

        # Row 7 (Message)
        self.input_state = Label(self.start_frame, text="Please Input all Fields!", font=("helvetica", 18))
        self.input_state.grid(row=7, columnspan=2)
        self.input_state.grid_forget()
        root.geometry("700x280")
        self.white_name.focus_set()

    def on_start(self):
        self.white = self.white_name.get()
        self.black = self.black_name.get()
        self.event = self.event_name.get()
        self.time = self.time_number.get()
        self.round = self.round_number.get()
        if self.white == "" or self.black == "" or self.event == "" or self.time == "":
            self.input_state.grid(row=7, columnspan=2)
        else:
            self.game_screen()

    def update_canvas(self):
        with open("temp.svg", "w") as f1:
            f1.write(chess.svg.board(board=self.board,size=800))
            drawing = svg2rlg("temp.svg")
            renderPM.drawToFile(drawing, "temp.png", fmt="PNG")
        img = ImageTk.PhotoImage(Image.open("temp.png"))  
        self.canvas.image_names = img 
        self.canvas.create_image(0, 0, anchor=NW, image=img) 
    
    def exit(self, event):
        self.root.destroy()

    def undo(self, event):
        self.user_move.delete(0, "end")
        self.board.reset()
        self.update_canvas()

    def player_move(self, event):
        move = self.user_move.get()
        self.user_move.delete(0, "end")
        try:
            self.text.set("Input your move then click Enter!\nClick on Control to restart the game!\nClick on Escape to close the Game!")
            self.board.push_san(move)
            self.update_canvas()
        except:
            self.text.set("Please input a valid move!")
        if self.game_ended() == 1:
            self.user_move.grid_forget()
            if self.board.turn:
                self.text.set("The winner is Black")
            else:
                self.text.set("The winner is White")
        elif self.game_ended() > 1:
            self.user_move.grid_forget()
            self.text.set("It's a draw!!!")

    def game_ended(self):
        if self.board.is_checkmate():
            self.result = 1
            return 1
        if self.board.is_stalemate():
            self.result = 2
            return 2
        if self.board.is_insufficient_material():
            self.result = 3
            return 3
        else:
            self.result = 0
            return 0

    def termination_message(self):
        temrination_text = ""
        if self.result == 0:
            temrination_text = "Game not terminated yet"
        elif self.result == 1:
            if self.board.turn:
                temrination_text = "Black won by checkmate"
            else:
                temrination_text = "White won by checkmate"
        elif self.result == 2:
            temrination_text = "Game is stalemate"
        else:
            temrination_text = "Game has insufficient material"
        return temrination_text
    
    def download(self):
        filepath = asksaveasfilename(
            defaultextension="pgn",
            filetypes=[("PGN Files", "*.pgn"), ("All Files", "*.*")]
        )
        if filepath:
            self.pgn_moves = self.pgn_moves.from_board(board=self.board)
            today = date.today().strftime('%Y.%m.%d')
            self.pgn_moves.headers["Event"] = self.event
            self.pgn_moves.headers["White"] = self.white
            self.pgn_moves.headers["Black"] = self.black
            self.pgn_moves.headers["TimeControl"] = self.time
            self.pgn_moves.headers["Round"] = self.round
            self.pgn_moves.headers["Termination"] = self.termination_message()
            self.pgn_moves.headers["Date"] = today
            del self.pgn_moves.headers["Site"]
            with open(filepath, "w") as output_file:
                exporter = chess.pgn.FileExporter(output_file)
                self.pgn_moves.accept(exporter)
        else:
            return

root = Tk()
Chess_Game(root)
root.mainloop()