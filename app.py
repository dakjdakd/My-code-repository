from flask import Flask, render_template, jsonify
from forest_ai_town.main import run_simulation
import time
import os

# 获取当前文件的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, 
    static_folder=os.path.join(current_dir, 'static'),  # 使用绝对路径
    template_folder=os.path.join(current_dir, 'templates')  # 使用绝对路径
)

# 打印静态文件夹路径，用于调试
print(f"Static folder path: {app.static_folder}")

simulation = run_simulation()

@app.route('/')
def index():
    # 使用simulation中的实际聊天记录
    chat_messages = simulation.chat_history
    return render_template('index.html', messages=chat_messages)

@app.route('/update')
def update():
    chat_messages = simulation.step()
    return jsonify({
        'messages': chat_messages
    })

if __name__ == '__main__':
    app.run(debug=True) 