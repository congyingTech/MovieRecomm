import os
from app import createApp, db
from app.models import User

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = createApp(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


#make_shell_context将app，db，User集合到dict中传到下面的shell command中作为参数自动创建数据库
def make_shell_context():
    return dict(app=app, db=db, User=User)
#shell 是python xx shell命令行的参数
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('migrate', MigrateCommand)


#为了运行单元测试
@manager.command
def test():
    import unittest
    #unit = unittest.TestLoader()
    #tests= unit.discover('tests') #扫描tests文件夹，用于发现test下所有测试用例，因为会进行全部的扫描，所以test下的init可以是空的
    test = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(test)

if __name__ == '__main__':
    manager.run()


