from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
from datetime import datetime
from db import db

app = Flask(__name__)
app.config['SECRET_KEY'] = '121212'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

data = db()

data.new_chat()

chatID = -1


class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username


@login_manager.user_loader
def load_user(user_id):
    user_data = data.select_user(user_id)
    if user_data:
        return User(id=user_data[0], username=user_data[1])
    return None


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "Passwords do not match. Please try again."
        data.insert_user(username=username, password=password)
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_data = data.get_user(username=username, password=password)
        if user_data:
            user = User(id=user_data[0], username=user_data[1])
            login_user(user)
            return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/index')
@login_required
def index():
    sender = current_user.username
    # Получение всех сообщений из базы данных
    chats = data.get_all_chats(sender=sender)
    return render_template('chat.html', messages=chats)  # словарь [chat_id]сообщения в формате JSONB


@app.route('/<chatId>')
@login_required
def chat(chatId):
    chat_data = data.get_chat(chatId=format(chatId))
    chat_data_final = []
    print("!!", chat_data)
    if chat_data:
        for i in chat_data:
            chat_data_final.append((i[0],i[2]))
    print(chat_data_final)
    global chatID
    chatID = chatId
    return render_template('index.html', messages=chat_data_final)  # сообщения в формате JSONB


@app.route('/send_message', methods=['POST'])
def send_message():
    # Получение данных из формы
    sender = current_user.username
    content = request.form['content']

    # Получение текущего времени
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Вставка сообщения в базу данных
    data.insert_message(sender=sender, content=content, timestamp=timestamp, chatid=chatID)

    # Перенаправление на главную страницу
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)