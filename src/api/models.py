from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship
import datetime

db = SQLAlchemy()

## imagina una red social en la que los usuarios pueden participar en eventos además de todo lo típico de una red social.
## no hagáis caso a las profile picture, en caso de que el usuario este logged tendría que tener foto

class Event_comments(db.Model): ##aqui tendriamos los comentarios de los eventos
    id = db.Column(db.Integer, primary_key=True) ##primary de la tabla
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), ##usuario que comenta
                        nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), ##evento que comenta
                         nullable=False)
    comment = db.Column(db.String(), unique=False, nullable=False) ##comentario
    creation_date = db.Column(DateTime, nullable=False, unique=False, ##fecha de creacion
                              default=datetime.datetime.utcnow())

    def __repr__(self):
        return f'<Event_comments {self.id}>'

    def serialize(self):
        user_data = User_Data.query.filter_by(user_id=self.user_id).first()
        user_data = user_data.serialize()
        image = Image.query.get(user_data["profile_picture"])
        return {
            "id": self.id,
            "user_id": self.user_id,
            "event_id": self.event_id,
            "comment": self.comment,
            "creation_date": self.creation_date,
            "user_name": user_data["name"],
            "profile_picture": image.image
        }


class Post_comments(db.Model): ## esta seria lo mismo pero para los post de la red social
    id = db.Column(db.Integer, primary_key=True) ## id de la tabla
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), ##usuario que hace el comentario
                        nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), ##post ene le que se hace la interaccion
                        nullable=False)
    comment = db.Column(db.String(), unique=False, nullable=False) ## comentario
    creation_date = db.Column(DateTime, nullable=False, unique=False, ## fecha creacion
                              default=datetime.datetime.utcnow())

    def __repr__(self):
        return f'<Post_comments {self.id}>'

    def serialize(self):
        user_data = User_Data.query.filter_by(user_id=self.user_id).first()
        user_data = user_data.serialize()
        image = Image.query.get(user_data["profile_picture"])
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "comment": self.comment,
            "creation_date": self.creation_date,
            "user_name": user_data["name"],
            "profile_picture": image.image
        }


class Group_participation(db.Model): ##tabla en caso de que un grupo entero de usuarios quiera hacer/participar en un evento
    id = db.Column(db.Integer, primary_key=True)##id de la tabla
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),##id del usuario 
                        nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'),##id del grupo de usuarios
                         nullable=False)

    def __repr__(self):
        return f'<Group_participation {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "group_id": self.group_id
        }


class Event_participation(db.Model):##tabla para comprobar si un único usuario participa en un evento
    id = db.Column(db.Integer, primary_key=True)##id de la tabla
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),##id del usuario
                        nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'),##id del evento
                         nullable=False)

    def __repr__(self):
        return f'<Event_participation {self.id}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "event_id": self.event_id
        }

    def return_event(self):
        event = Event.query.get(self.event_id)
        return (event.serialize())


class Form_friendship(db.Model):## tabla para el formulario de añadir amigo
    id = db.Column(db.Integer, primary_key=True) ##id de la tabla
    main_friend_id = db.Column(db.Integer, db.ForeignKey('user.id'), ##usuario que manda solicitud
                               nullable=False)
    secondary_friend_id = db.Column(db.Integer, db.ForeignKey('user.id'),##usuario que recibe solicitud
                                    nullable=False)

    def __repr__(self):
        return f'<Form_friendship {self.id}>'

    def serialize_list_friend(self):
        profile_picture = None
        favorite = User_Data.query.filter_by(
            user_id=self.secondary_friend_id).first()
        if favorite.profile_picture is not None:
            favorite_profile_picture = Image.query.get(
                favorite.profile_picture)
            profile_picture = favorite_profile_picture.image

        return {
            "id": self.id,
            "main_friend_id": self.main_friend_id,
            "secondary_friend_id": self.secondary_friend_id,
            "profilePicture": profile_picture,
            "friend_name": favorite.name,
            "friend_last_name": favorite.last_name,
            "address": favorite.address
        }

    def serialize_delete(self):
        profile_picture = None
        user = User_Data.query.filter_by(
            user_id=self.secondary_friend_id).first()
        if user.profile_picture is not None:
            user_profile_picture = Image.query.get(user.profile_picture)
            profile_picture = user_profile_picture.image
        return {
            "id": self.id,
            "main_friend_id": self.main_friend_id,
            "secondary_friend_id": self.secondary_friend_id,
            "profilePicture": profile_picture,
            "friend_name": user.name,
            "friend_last_name": user.last_name,
            "address": user.address
        }

    def serialize(self):
        return {
            "id": self.id,
            "main_friend_id": self.main_friend_id,
            "secondary_friend_id": self.secondary_friend_id
        }


class User(db.Model): ##tabla de usuario de mi aplicación
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True) ##id del usuario
    email = db.Column(db.String(120), unique=True, nullable=False) ##
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, default=True)

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            
        }


class Group(db.Model): ## tabla para grupos de usuarios
    id = db.Column(db.Integer, primary_key=True) ## id tabla
    name = db.Column(db.String(10), unique=True, nullable=False) #nombre del grupo
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), ## id del usuario que ha creado el grupo
                         nullable=False)
    private = db.Column(db.Boolean(), unique=False) ##grupo privado sí o no

    def __repr__(self):
        return f'<Group {self.name}>'  # representacion de la clase

    def serialize(self):

        return {
            "id": self.id,
            "name": self.name,
            "owner_id": self.owner_id,
            "private": self.private,

            
        }

    def serialize_name(self):
        return {
            "name": self.name
        }


class Event(db.Model): ## tabla de eventos
    id = db.Column(db.Integer, primary_key=True) # id del evento
    name = db.Column(db.String(120), unique=True, nullable=False) # nombre del evento
    start = db.Column(db.String(), unique=False, nullable=False) #fecha y hora de realización del evento
    end = db.Column(db.String(), unique=False, nullable=False) # fecha y hora de finalización del evento
    map = db.Column(db.String(), unique=False, nullable=False) # ubicación del evento ( en este caso con la api de google maps)
    owner_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)
    date = db.Column(db.String(), nullable=False) # fecha del evento
    private = db.Column(db.Boolean(), unique=False)# grupo privado si o no?
    slug = db.Column(db.String(), unique=False, nullable=False) #slug para enlazar información en caso de ser necesario
    description = db.Column(db.String(), unique=False, nullable=False)## descripcion del evento
    origin_lon = db.Column(db.Float(), unique=False, nullable=False) # longitud del evento para ubicación en mapa
    origin_lat = db.Column(db.Float(), unique=False, nullable=False) # latitud del evento para ubicación en mapa
    destination_lon = db.Column(db.Float(), unique=False, nullable=False) # longitud de destino por si quieres dar un paseo o una ruta en moto etc
    destination_lat = db.Column(db.Float(), unique=False, nullable=False)# longitud de destino por si quieres dar un paseo o una ruta en moto etc
    hours = db.Column(db.String(), unique=False, nullable=False) #duracion del evento en horas
    minutes = db.Column(db.String(), unique=False, nullable=False)#duracion del evento en minutos

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "start": self.start,
            "end": self.end,
            "map": self.map,
            "owner_id": self.owner_id,
            "date": self.date,
            "private": self.private,
            "slug": self.slug,
            "description": self.description,
            "origin_lon": self.origin_lon,
            "origin_lat": self.origin_lat,
            "destination_lon": self.destination_lon,
            "destination_lat": self.destination_lat,
            "hours": self.hours,
            "minutes": self.minutes
        }


class User_Data(db.Model): ## informacion del usuario 
    id = db.Column(db.Integer, primary_key=True) ## id tabla
    name = db.Column(db.String(120), unique=False, nullable=False)
    last_name = db.Column(db.String(120), unique=False, nullable=False)
    address = db.Column(db.String(120), unique=False, nullable=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    profile_picture = db.Column(
        db.Integer(), db.ForeignKey('image.id'), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "address": self.address,
            "user_id": self.user_id,
            "profile_picture": self.profile_picture
        }


class Image(db.Model):#tabla para imagen de perfil del usuario
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(), unique=False, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_data_id = db.relationship('User_Data', backref='image', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "image": self.image,
            "owner_id": self.owner_id
        }


class Post(db.Model): # posts de la red social 
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(5000), unique=False, nullable=True)

    created_at = db.Column(DateTime, nullable=False,
                           default=datetime.datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=True)

    def serialize_image(self):
        if self.image_id is None:
            return self.serialize()

        image = Image.query.get(self.image_id)
        image = image.serialize()

        user_data = User_Data.query.filter_by(user_id=self.user_id).first()
        user_profile_picture = None
        if user_data.profile_picture is not None:
            user_profile_picture = Image.query.get(
                user_data.profile_picture).image

        return {
            "id": self.id,
            "text": self.text,
            "image": image["image"],
            "image_id": self.image_id,
            "date": self.created_at,
            "user_id": self.user_id,
            "user_name": user_data.name+" "+user_data.last_name,
            "user_profile_picture": user_profile_picture
        }

    def serialize(self):
        return {
            "id": self.id,
            "text": self.text,

            "date": self.created_at,
            "user_id": self.user_id
        }