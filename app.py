from flask import Flask, render_template, redirect, url_for, request

# render_template - нужен для то чтобы ваша страница html отобразилась корреткно
# redirect - нам понадобится для обработки запросы формы где мы перенаприм пользователя на страницу админ панели
# url_for - вспомогательна библиотека для того чтобы сделать правильный переход по ссылке в нашем случеш мы будем ссылаться на adm_panel
# request - обработчик запросов GET/POST и дргуих 

app = Flask(__name__)

@app.route('/')
def hello_world():
  # Загрузка и отображение главной страницы (hello)
  return render_template('hello.html')

@app.route('/button')
def about():
  return render_template('button.html')

@app.route('/user/<username>')
def show_user_profile(username):
  return f'User {username}'

@app.route('/hello/<name>')
def hello(name):
  return render_template('hello.html', name=name)
  
if __name__ == '__main__':
  app.run(debug=True) # http://127.0.0.1:5000/
  # from waitress import serve
  # serve(app, host='127.0.0.1', port=8080)