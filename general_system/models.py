from general_system import data_base, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(id_user):
    return Usuario.query.get(int(id_user))


class Usuario(data_base.Model, UserMixin):
    id = data_base.Column(data_base.Integer, primary_key=True)
    username = data_base.Column(data_base.String, nullable=False)
    email = data_base.Column(data_base.String, nullable=False, unique=True)
    password = data_base.Column(data_base.String, nullable=False)
    perf_photo = data_base.Column(data_base.String, default='default.jpg')
    posts = data_base.relationship('Post', backref='autor', lazy=True)
    courses = data_base.Column(data_base.String, nullable=False, default='')

    def count_posts(self):
        return len(self.posts)


class Post(data_base.Model):
    id = data_base.Column(data_base.Integer, primary_key=True)
    title = data_base.Column(data_base.String, nullable=False)
    bory_text = data_base.Column(data_base.Text, nullable=False)
    date_create = data_base.Column(data_base.DateTime, nullable=False, default=datetime.utcnow)
    id_user = data_base.Column(data_base.Integer, data_base.ForeignKey('usuario.id'), nullable=False)
    status = data_base.Column(data_base.String, nullable=False)
