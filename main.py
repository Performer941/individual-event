from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from models import db
from views import index_blu, passport_blu, detail_blu, user_blu

# 创建Flask应用对象
app = Flask(__name__)

# 加载配置
app.config.from_pyfile("config.ini")

# 创建蓝图，且注册到app
app.register_blueprint(index_blu)
app.register_blueprint(passport_blu)
app.register_blueprint(detail_blu)
app.register_blueprint(user_blu)

# 初始化数据库
db.init_app(app)

# 添加数据库迁移等工具
manager = Manager(app)
# 生成migrate对象 用来数据库迁移
migrate = Migrate(app, db)
# 添加db命令
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    # app.run(port=5000)
    manager.run()
