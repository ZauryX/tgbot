import telebot

# Создаем экземпляр бота и указываем токен вашего бота
bot = telebot.TeleBot('YOUR_BOT_TOKEN')

# Игровое поле
game_board = [[' ' for _ in range(3)] for _ in range(3)]
current_player = 'X'  # Игрок, совершающий текущий ход

# Обработчик команды /start или /help
@bot.message_handler(commands=['start', 'help'])
def send_instructions(message):
    instructions = "Привет! Давай сыграем в крестики-нолики!\n" \
                   "Для того, чтобы сделать ход, используй координаты клетки.\n" \
                   "Например, для выбора клетки в верхнем левом углу, отправь '00'.\n" \
                   "Приятной игры!"
    bot.reply_to(message, instructions)

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global current_player

    if message.text == '/start' or message.text == '/help':
        return

    if message.text.isdigit() and len(message.text) == 2:
        row = int(message.text[0])
        col = int(message.text[1])

        if row < 0 or row >= 3 or col < 0 or col >= 3:
            bot.reply_to(message, "Неверные координаты! Попробуй еще раз.")
            return

        if game_board[row][col] != ' ':
            bot.reply_to(message, "Клетка уже занята! Попробуй еще раз.")
            return

        game_board[row][col] = current_player
        print_game_board()

        if check_winner():
            bot.reply_to(message, f"Поздравляю! Игрок {current_player} победил!")
            reset_game()
            return

        if check_draw():
            bot.reply_to(message, "Ничья! Игра окончена.")
            reset_game()
            return

        current_player = 'O' if current_player == 'X' else 'X'
        bot.reply_to(message, f"Ходит игрок {current_player}")
    else:
        bot.reply_to(message, "Неверный формат ввода! Попробуй еще раз.")

# Проверка наличия победителя
def check_winner():
    # Проверка строк и столбцов
    for i in range(3):
        if game_board[i][0] == game_board[i][1] == game_board[i][2] != ' ':
            return True
        if game_board[0][i] == game_board[1][i] == game_board[2][i] != ' ':
            return True

    # Проверка диагоналей
    if game_board[0][0] == game_board[1][1] == game_board[2][2] != ' ':
        return True
    if game_board[0][2] == game_board[1][1] == game_board[2][0] != ' ':
        return True

    return False

# Проверка наличия ничьей
def check_draw():
    for row in game_board:
        if ' ' in row:
            return False
    return True

# Вывод игрового поля в чат
def print_game_board():
    board = '\n---------\n'.join([' | '.join(row) for row in game_board])
    bot.send_message(chat_id=YOUR_CHAT_ID, text=board)

# Сброс игры
def reset_game():
    global game_board, current_player
    game_board = [[' ' for _ in range(3)] for _ in range(3)]
    current_player = 'X'

# Запускаем бота
bot.polling()
