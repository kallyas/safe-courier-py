from api import create_app, db, jwt
# from flask_script import Manager
from flask_swagger_ui import get_swaggerui_blueprint
from flask_migrate import MigrateCommand


app = create_app()

SWAGGER_URL = '/api/v1/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = 'https://api-v3.safe-courier.ml/v2/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Safe courier application"
    },
)

app.register_blueprint(swaggerui_blueprint)

# manager = Manager(app)
# manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    db.create_all(app=create_app())
    app.run()