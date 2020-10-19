from flask import Flask


# 创建Flask应用对象
app = Flask(__name__)


if __name__ == '__main__':
    app.run(port=8899)
    # manager.run()
