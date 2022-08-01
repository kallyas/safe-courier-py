from api import create_app, db, jwt
# from flask_script import Manager
from flask_migrate import MigrateCommand


app = create_app()

# manager = Manager(app)
# manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    db.create_all(app=create_app())
    app.run()