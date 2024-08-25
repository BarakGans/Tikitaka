from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QMessageBox 
from PyQt5.QtGui import QFont

class TicTacToe(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Game Tic Tac Toe')
        self.setGeometry(500, 200, 300, 300)
        self.current_player = 'X'
        self.board = [''] * 9
        self.buttons = [QPushButton('', self) for _ in range(9)]
        for i, button in enumerate(self.buttons):
            button.setFixedSize(150, 150)
            button.setFont(QFont('Arial', 80))
            button.clicked.connect(self.onButtonClick)
        
        layout = QGridLayout()
        for i in range(3):
            for j in range(3):
                layout.addWidget(self.buttons[i * 3 + j], i, j)
        self.setLayout(layout)

    def check_winner(self):
        winning_combinations = [(0,1,2), (3,4,5), (6,7,8),
                                (0,3,6), (1,4,7), (2,5,8),
                                (0,4,8), (2,4,6)]
        
        for menang in winning_combinations:
            if self.board[menang[0]] == self.board[menang[1]] == self.board[menang[2]] != '':
                return True
        return False
    
    def check_draw(self):
        return '' not in self.board

    def onButtonClick(self):
        sender = self.sender()
        idx = self.buttons.index(sender)
        if self.board[idx] == '' and not self.check_winner() and not self.check_draw():
            self.board[idx] = self.current_player
            sender.setText(self.current_player)
            if self.check_winner():
                QMessageBox.information(self, 'Game Over', f'Player {self.current_player} Menang!')
                self.reset_game()
            elif self.check_draw():
                QMessageBox.information(self, 'Game Over', 'Permainan Seri!!')
                self.reset_game()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                self.update_button_color()
    
    def reset_game(self):
        self.current_player = 'X'
        self.board = [''] * 9
        for button in self.buttons:
            button.setText('')
            button.setStyleSheet('')

    def update_button_color(self):
        for i, button in enumerate(self.buttons):
            if self.board[i] == 'X':
                button.setStyleSheet('background-color : lightblue;')
            elif self.board[i] == 'O':
                button.setStyleSheet('background-color : lightcoral;')

app = QApplication([])
game = TicTacToe()
game.show()
app.exec_()