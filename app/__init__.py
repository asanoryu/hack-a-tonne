from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS



app = Flask(__name__, static_url_path='/static')
CORS(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)


from app import routes, models, errors

# db.create_all()
# # add_point_column_sql="ALTER TABLE `adimatch`.`event` DROP `where`;"
# db.engine.execute(add_point_column_sql)
# add_point_column_sql="ALTER TABLE `adimatch`.`event` ADD COLUMN `where` POINT NOT NULL AFTER `user_id`;"
# db.engine.execute(add_point_column_sql)
