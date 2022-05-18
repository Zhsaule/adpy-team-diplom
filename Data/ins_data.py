from sqlalchemy import *
# from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
# from sqlalchemy import MetaData
from Data.auth_db import password
# from auth_db import password

Base = declarative_base()
engine = create_engine("postgresql+psycopg2://postgres:" + password + "@localhost:5432/vkinder")
metadata = MetaData(bind=engine)
print(engine)


class Users(Base):
    __table__ = Table('users', metadata, autoload=True)


class UserClient(Base):
    __table__ = Table('Users/Client', metadata, autoload=True)


class Favorite(Base):
    __table__ = Table('favoriteclients', metadata, autoload=True)


class Propose(Base):
    __table__ = Table('propose', metadata, autoload=True)


class UsersPropose(Base):
    __table__ = Table('Users/Propose', metadata, autoload=True)


# ins_data(event.user_id, age, sex, city)


def ins_data(user_id, user_age, user_gender, user_city):
    conn = engine.connect()
    sel = select(Users).where(Users.user_id == user_id)
    if conn.execute(sel).fetchall():
        upd = update(Users).where(Users.user_id == user_id).values(
            user_age=user_age,
            user_gender=user_gender,
            user_city=user_city
        )
        conn.execute(upd)
    else:
        ins = insert(Users).values(
            user_id=user_id,
            user_age=user_age,
            user_gender=user_gender,
            user_city=user_city
        )
        conn.execute(ins)


def ins_fav_data(user_id, client_id, client_name, client_surname, client_link, client_photos):
    conn = engine.connect()
    sel = select(Favorite).where(Favorite.client_id == client_id)
    if conn.execute(sel).fetchall():
        return
    else:
        ins = insert(Favorite).values(
            client_id=client_id,
            client_name=client_name,
            client_surname=client_surname,
            client_link=client_link,
            client_photos=client_photos
        )
        conn.execute(ins)
        ins_user_client(user_id, client_id)
        print('add to favorite')


def ins_user_client(user_id, fav_client_id):
    conn = engine.connect()
    ins = insert(UserClient).values(
        user_id=user_id,
        favoriteclient_id=fav_client_id
    )
    conn.execute(ins)


def ins_propose_data(user_id, client_id):
    conn = engine.connect()
    sel = select(Propose).where(Propose.p_client_id == client_id)
    if conn.execute(sel).fetchall():
        return
    else:
        ins = insert(Propose).values(
            p_client_id=client_id
        )
        conn.execute(ins)
        ins_user_prop(user_id, client_id)
        print('add to proposal')


def ins_user_prop(user_id, client_id):
    conn = engine.connect()
    ins = insert(UsersPropose).values(
        user_id=user_id,
        prop_client_id=client_id
    )
    conn.execute(ins)


def sel_prop_data(user_id):
    conn = engine.connect()
    user_prop = UsersPropose.__table__
    sel = select(user_prop).where(user_prop.c.user_id == user_id)
    res = conn.execute(sel)
    res_list = ([i[1] for i in res])
    return res_list


# conn = engine.connect()
# print(sel_prop_data('18245417'))
# s = user_prop.select()
# res = conn.execute(s)
# row = res.fetchall()
# print(row)
