from flask_login import UserMixin
from random import randint
from datetime import datetime, timedelta, timezone
import psycopg2


def create_identifier(length):
    words, new_identifier = 'A a B b C c D d E e F f G g H h I i J j K k L l M m N n O 1 2 3 4 5 6 7 8 9 o P p Q q R r S s T t U u V v X x W w Y y Z z 1 2 3 4 5 6 7 8 9'.split(' '), ''
    for _ in range(0, length):
        num  = randint(0, len(words) - 1)
        new_identifier = new_identifier + words[num]
        
    if length == 6:
        is_equal = db_execute(f"SELECT identifier FROM post_answer WHERE identifier = '{new_identifier}';", 'GET', 'one')

        if is_equal == None:
            return new_identifier
        
    elif length == 8:
        is_equal = db_execute(f"SELECT identifier FROM post_answer WHERE identifier = '{new_identifier}';", 'GET', 'one')
        if is_equal == None:
            return new_identifier
        
    elif length == 10:

        is_equal = db_execute(f"SELECT identifier FROM post WHERE identifier = '{new_identifier}';", 'GET', 'one')
        if is_equal == None:
            return new_identifier
        
    elif length == 12:
        is_equal = db_execute(f"SELECT identifier FROM users WHERE identifier = '{new_identifier}';", 'GET', 'one')

        if is_equal == None:
            return new_identifier 

    return create_identifier(length=length)


def time_now(mode=None):
    
    month = datetime.strftime('%B')
    months = {'January': 'jan', 'February': 'fev', 'March': 'mar', 'April': 'abr', 'May': 'mai', 'June': 'jun', 'July': 'jul',
            ' August': 'ago', 'September': 'set','October': 'out', 'November': 'nov', 'December': 'dec'}

    if mode == 'register':
        acc_created_at = datetime.strftime(f'Membro desde %d, {months[f"{month}"]} de %Y. ')
        return acc_created_at
    
    data = datetime.now().astimezone(timezone(timedelta(hours=-3))).strftime(f'ás %H:%Mhrs - %d, {months[f"{month}"]} %Y')
    return data


def db_execute(comando: str, get: str = None, mode=None):

    with psycopg2.connect(database='railway', host='roundhouse.proxy.rlwy.net', user='postgres', port=37045, password='ACDBcFaD23aEAC1gCdFac4e4a-6aEd3c') as db:
        cursor = db.cursor()
        if get == 'GET':
            cursor.execute(comando)
            if mode == 'all':
                data = cursor.fetchall()
            elif mode == 'one':
                data = cursor.fetchone()
            return data
        
        cursor.execute(comando)


class User(UserMixin):

    def __init__(self, user_info: tuple, get_info = None, get_lod = None):
        self.id = user_info[0]
        self.name = user_info[1]
        self.nickname = user_info[2]
        self.email = user_info[3]
        self.password = user_info[4]
        self.identifier = user_info[5]
        self.created_at = user_info[6]
        self.image = user_info[7]
        if get_info == 'GET':
            self.info = {
                'likes': len(db_execute(f"""SELECT likes FROM (SELECT likes FROM lod_post WHERE user_loded = {self.id} UNION ALL
SELECT likes FROM lod_comment WHERE user_loded = {self.id} UNION ALL
SELECT likes FROM lod_answer WHERE user_loded = {self.id}) WHERE likes = 1;""", 'GET', 'all')),
                'dislikes': len(db_execute(f"""SELECT dislikes FROM (SELECT dislikes FROM lod_post WHERE user_loded = {self.id} UNION ALL
SELECT dislikes FROM lod_comment WHERE user_loded = {self.id} UNION ALL
SELECT dislikes FROM lod_answer WHERE user_loded = {self.id}) WHERE dislikes = 1;""", 'GET', 'all')),
                'posts': len(db_execute(f'SELECT id FROM post WHERE user_id = {self.id};', 'GET', 'all')),
                'follows': len(db_execute(f'SELECT followed_id FROM follow WHERE followed_id = {self.id}', 'GET', 'all')),
            }

class Post:
    def __init__(self, id, user_id, titulo, texto, created_at, identifier, was_edited, current_user_id, get_lod = None, for_post = None):
        self.id = id
        self.user: User = User(db_execute(f'SELECT * FROM users WHERE id = {user_id};', 'GET', 'one'))
        self.titulo = titulo
        self.texto = texto
        self.created_at = created_at
        self.identifier = identifier
        self.was_edited = was_edited
        if get_lod == 'GET':
            self.likes: Lod = Lod(current_user_id=current_user_id, identifier=self.id, table='lod_post', column='post_id', mode='likes')
            self.dislikes: Lod = Lod(current_user_id=current_user_id, identifier=self.id, table='lod_post', column='post_id', mode='dislikes')
        

        if for_post == 'GET':
            self.__comments = db_execute(f'SELECT * FROM post_comment WHERE post_id = {self.id};', 'GET', 'all')
            self.comments = [Comment(
            id=each[0], user_id=each[1], post_id=each[2], text=each[3], created_at=each[4], identifier=each[5], was_edited=each[6], current_user_id=current_user_id
        ) for each in self.__comments]
            if db_execute(f'SELECT post_id FROM save_post WHERE post_id = {self.id} and user_id = {current_user_id};', 'GET', 'one') == None:
                self.is_saved = False
            else:
                self.is_saved = True


class Comment:

    def __init__(self, id, user_id, post_id, text, created_at, was_edited, identifier, current_user_id):
        self.id = id
        self.user: User = User(db_execute(f'SELECT * FROM users WHERE id = {user_id};', 'GET', 'one'))
        self.post = post_id
        self.text = text
        self.created_at = created_at
        self.was_edited = was_edited
        self.identifier = identifier
        self.likes: Lod = Lod(current_user_id=current_user_id, identifier=self.id, table='lod_comment', column='comment_id', mode='likes')
        self.dislikes: Lod = Lod(current_user_id=current_user_id, identifier=self.id, table='lod_comment', column='comment_id', mode='dislikes')
        
        self.__coments_answers = db_execute(f'SELECT * FROM post_answer WHERE comment_id = {self.id}', 'GET', 'all')
        if not self.__coments_answers == []:
            self.answers: list = [Answer(
                id=each[0], user_id=each[1], answer_id=each[2], text=each[3], created_at=each[4], identifier=each[5], was_edited=each[6], current_user_id=current_user_id
            ) for each in self.__coments_answers]
        else:
            self.answers = None
        self.len_answer = len(self.__coments_answers)

        

class Answer:

    def __init__(self, id, user_id, answer_id, text, created_at, identifier, was_edited, current_user_id):
        self.id = id
        self.user: User = User(db_execute(f'SELECT * FROM users WHERE id = {user_id};', 'GET', 'one'))
        self.answer_id = answer_id
        self.text = text
        self.created_at = created_at
        self.identifier = identifier
        self.was_edited = was_edited
        self.likes: Lod = Lod(current_user_id=current_user_id, identifier=self.id, table='lod_answer', column='answer_id', mode='likes')
        self.dislikes: Lod = Lod(current_user_id=current_user_id, identifier=self.id, table='lod_answer', column='answer_id', mode='dislikes')
        

class Lod:

    def __init__(self, current_user_id, identifier, table, mode, column):
        self.length = len(db_execute(f"SELECT {mode} FROM {table} WHERE {mode} = 1 and {column} = '{identifier}';", 'GET', 'all'))

        if db_execute(f"SELECT user_id FROM {table} WHERE {mode} = 1 and user_id = {current_user_id} and {column} = '{identifier}';", 'GET', 'one') == None:
            self.is_liked = False
        else:
            self.is_liked = True
    

