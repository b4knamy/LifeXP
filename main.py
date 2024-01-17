from flask import Flask, render_template, url_for, redirect, request, flash, make_response
from project_utils import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user, login_manager, login_required, LoginManager, AnonymousUserMixin



#       FLASK APP CONFIG
app = Flask(__name__, static_folder="static", template_folder="templates")



    #       LOGIN CONFIG
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "sucess"
login_manager.anonymous_user = AnonymousUserMixin

@login_manager.user_loader
def load_user(user_id):
    return User(db_execute(f'SELECT * FROM user WHERE id = {user_id};', 'GET').fetchone())


#       PAGES'S LOGIC  
 
@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        # Informations got by entry from the user
        password = request.form.get('password')
        email = request.form.get('email')

        # checking if the user password is equal
        is_an_user = db_execute(f"SELECT * FROM user WHERE email = '{email}'", 'GET').fetchone()

        if is_an_user == None:

            flash('Email incorreto, tente novamente.')

        else:

            user_logged = User(is_an_user)
            if check_password_hash(pwhash=user_logged.password, password=password):

                login_user(user_logged)

                return redirect(url_for('homepage'))
            else:

                flash('Seu senha está incorreta, tente novamente!')

    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():

    if request.method == 'POST':

        name = request.form.get('name')
        nickname = request.form.get('nickname')
        email = request.form.get('email')
        password = request.form.get('password')

        hashed_password = generate_password_hash(password=password, salt_length=16)
        
        new_user = db_execute(f'SELECT * FROM user WHERE email = "{email}";', 'GET').fetchone()

        if new_user == None:

            db_execute(f"INSERT INTO user (name, nickname, email, password, identifier, created_at) VALUES ('{name}', '{nickname}', '{email}', '{hashed_password}', '{create_identifier(12)}', '{time_now(mode='register')}');")

            return redirect(url_for('login'))
        else:
            flash('Esse email já está sendo usado.')

    return render_template('register.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/homepage')
@login_required
def homepage():
    posts_list = []
    posts = db_execute('SELECT * FROM post', 'GET').fetchall()
    for post in posts:
        
        new_post = Post(
                id=post[0],
                user_id=post[1],
                titulo=post[2],
                texto=post[3],
                created_at=post[4],
                identifier=post[5],
                was_edited=post[6],
                current_user_id=current_user.id,
                get_lod='GET'
            )
        posts_list.append(new_post)

    current_user_identifier = db_execute(f"SELECT identifier FROM user WHERE id = {current_user.id};", 'GET').fetchone()[0]
    return render_template('listofposts.html', showname=showname, all_posts=posts_list, current_user_identifier=current_user_identifier)


@app.route('/myposts')
@login_required
def myposts():
        
        all_posts = db_execute(f'SELECT * FROM post WHERE user_id = {current_user.id}', 'GET').fetchall()

        result = []
        for post in all_posts:
                
            new_post = Post(
                        id=post[0],
                        user_id=post[1],
                        titulo=post[2],
                        texto=post[3],
                        created_at=post[4],
                        identifier=post[5],
                        was_edited=post[6],
                        current_user_id=current_user.id,
                        get_lod='GET'
                    )
            result.append(new_post)

        return render_template('showing_user_posts.html', user_posts=result,  showname=showname)

@app.route('/makepost', methods=['GET', 'POST'])
@login_required
def makepost():

    if request.method == 'POST':
        
        title = request.form.get('title')
        texto = request.form.get('story')
        db_execute(f'INSERT INTO post (user_id, titulo, texto, created_at, identifier) VALUES ({current_user.id}, "{title}", "{texto}", "{time_now()}", "{create_identifier(10)}");')
        
        
        return redirect(url_for('homepage'))


    return render_template('makepost.html')


@app.route('/post/<identifier>', methods=['GET'])
@login_required
def post(identifier):
    # GETTING THE MAIN POST DATA

    current_post = db_execute(f'SELECT * FROM post WHERE identifier = "{identifier}"', 'GET').fetchone()
    main_post = Post(
                id=current_post[0],
                user_id=current_post[1],
                titulo=current_post[2],
                texto=current_post[3],
                created_at=current_post[4],
                identifier=current_post[5],
                was_edited=current_post[6],
                current_user_id=current_user.id,
                get_lod='GET',
                for_post='GET'
            )
    # GETTING THE MAIN POST DATA          ---END

    # CHECKING IF THE CURRENT USER IS FOLLOWING THE POST OWNER

    if db_execute(f'SELECT * FROM follow WHERE following_id = {current_user.id} and followed_id = {main_post.user.id}', 'GET').fetchone() == None:
        is_already_followed = False
    else:
        is_already_followed = True

    
    

    # CHECKING IF THE CURRENT USER IS FOLLOWING THE POST OWNER       ---END

    return render_template('posts.html', post=main_post, is_following=is_already_followed, showname=showname)



@app.route('/change_post/<identifier>', methods=['POST'])
@login_required
def change_post(identifier):
    
    if request.method == 'POST':

        new_title = request.form.get('title')
        new_story = request.form.get('story')

        db_execute(f"UPDATE post SET titulo = '{new_title}', texto = '{new_story}' WHERE identifier = '{identifier}';")

        return redirect(url_for('post', identifier=identifier))

@app.route('/delete-post/<identifier>', methods=["GET"])
@login_required
def delete_post(identifier):
    db_execute(f'DELETE FROM post WHERE identifier = "{identifier}"')

    return redirect(url_for('myposts'))

@app.route('/delete-comment/<identifier>/<answer_identifier>/<mode>')
@login_required
def delete_comment(identifier, answer_identifier, mode):
    
    if mode == 'pa':
        db_execute(f'DELETE FROM post_comment WHERE identifier = "{answer_identifier}";')

    if mode == 'psa':
        db_execute(f'DELETE FROM post_answer WHERE identifier = "{answer_identifier}";')

    return redirect(url_for('post', identifier=identifier))






@app.route('/comment/<identifier>/<mode>/<answer_identifier>', methods=['POST'])
@login_required
def comment(identifier, mode, answer_identifier):
    if request.method == 'POST':
        text = request.form.get('answer')
        if len(text) >= 1:

        

            if mode == 'c':
                post_id = db_execute(f'SELECT id FROM post WHERE identifier = "{identifier}"', 'GET').fetchone()[0]

                db_execute(f'INSERT INTO post_comment (user_id, post_id, texto, created_at, identifier, was_edited) VALUES ({current_user.id}, {post_id},"{text}", "{time_now()}", "{create_identifier(8)}", "false");')

            if mode == 'ec':
                
                db_execute(f'UPDATE post_comment SET texto = "{text}", was_edited = "true" WHERE identifier = "{answer_identifier}"')

            if mode == 'ea':

                db_execute(f'UPDATE post_answer SET texto = "{text}", was_edited = "true" WHERE identifier = "{answer_identifier}"')

            if mode == 'a':

                post_answer_id = db_execute(f'SELECT id FROM post_comment WHERE identifier = "{answer_identifier}"', 'GET').fetchone()[0]

                db_execute(f'INSERT INTO post_answer (user_id, comment_id, texto, created_at, identifier, was_edited) VALUES ({current_user.id}, {post_answer_id}, "{text}", "{time_now()}", "{create_identifier(6)}" , "false");')
        
        return redirect(url_for('post', identifier=identifier))









@app.route('/profile/follow/<identifier>', methods=['POST'])
@app.route('/post/follow/<identifier>', methods=['POST'])
@login_required
def follow(identifier):
        
        followed_user_id = db_execute(f"SELECT id FROM user WHERE identifier = '{identifier}';", 'GET').fetchone()[0]

        is_already_followed = db_execute(f'SELECT * FROM follow WHERE followed_id = {followed_user_id} and following_id = {current_user.id};', 'GET').fetchone()

        if is_already_followed == None:

            db_execute(f'INSERT INTO follow (following_id, followed_id) VALUES ({current_user.id}, {followed_user_id});')

            return "success", 200
        
        db_execute(f'DELETE FROM follow WHERE followed_id = {followed_user_id} and following_id = {current_user.id}')

        return "success", 200

@app.route('/post/lod/<identifier>/<mode>', methods=['POST'])
@login_required
def lod(identifier, mode):
        
        identifier_size = len(identifier)
        if identifier_size == 6:
            data = db_execute(f'SELECT id, user_id FROM post_answer WHERE identifier = "{identifier}";', 'GET').fetchone()
            id = data[0]
            id_user_loded = data[1]

            table = 'lod_answer'
            column_name = 'answer_id'
            

        elif identifier_size == 8:
            data = db_execute(f'SELECT id, user_id FROM post_comment WHERE identifier = "{identifier}";', 'GET').fetchone()
            id = data[0]
            id_user_loded = data[1]
            table = 'lod_comment'
            column_name = 'comment_id'

        elif identifier_size == 10:
            data = db_execute(f'SELECT id, user_id FROM post WHERE identifier = "{identifier}";', 'GET').fetchone()
            id = data[0]
            id_user_loded = data[1]
            table = 'lod_post'
            column_name = 'post_id'


        
        is_lod = db_execute(f'SELECT user_id, {column_name}, like, dislike FROM {table} WHERE user_id = {current_user.id} and {column_name} = {id};', 'GET').fetchone()

        if is_lod == None:

            if mode == 'like':
                    db_execute(f'INSERT INTO {table} (user_id, {column_name}, user_loded, like, dislike) VALUES ({current_user.id}, {id}, {id_user_loded}, 1, 0);')

            elif mode == 'dislike':
                    print('dislikeiii???')
                    db_execute(f'INSERT INTO {table} (user_id, {column_name}, user_loded,  like, dislike) VALUES ({current_user.id}, {id}, {id_user_loded}, 0, 1);')

        else:

            if mode == 'like':

                if is_lod[2] == 1:
                    if is_lod[3] == 0:
                        db_execute(f'DELETE FROM {table} WHERE user_id = {current_user.id} and {column_name} = {id};')
                    else:
                        db_execute(f'UPDATE {table} SET like = 0 WHERE user_id = {current_user.id} and {column_name} = {id};')
                else:
                    db_execute(f'UPDATE {table} SET like = 1 WHERE user_id = {current_user.id} and {column_name} = {id};')

            elif mode == 'dislike':
                    
                if is_lod[3] == 1:
                    if is_lod[2] == 0:
                        db_execute(f'DELETE FROM {table} WHERE user_id = {current_user.id} and {column_name} = {id};')
                    else:
                        db_execute(f'UPDATE {table} SET dislike = 0 WHERE user_id = {current_user.id} and {column_name} = {id};')
                else:
                    db_execute(f'UPDATE {table} SET dislike = 1 WHERE user_id = {current_user.id} and {column_name} = {id};')

        return "sucess", 200
        
@app.route('/profile/<identifier>', methods=['POST', 'GET'])
@login_required
def profile(identifier):
    error = None
    get_user = db_execute(f'SELECT * FROM user WHERE identifier = "{identifier}";', 'GET').fetchone()

    user = User(get_user, get_info='GET')
    
    if db_execute(f'SELECT * FROM follow WHERE following_id = {current_user.id} and followed_id = {user.id}', 'GET').fetchone() == None:
        is_already_followed = False
    else:
        is_already_followed = True


    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        nickname = request.form.get('nickname')
        password = request.form.get('password')
        new_password = request.form.get('new_password')
        image = request.form.get('image')

        if len(password) > 0  or len(new_password) > 0:

            if check_password_hash(pwhash=current_user.password, password=password):
                new_hashed_password = generate_password_hash(new_password)
                print(new_password, password, new_hashed_password, '===========================================================')
                

                if current_user.email == email:
                    db_execute(f'UPDATE user SET name = "{nome}", nickname = "{nickname}", password = "{new_hashed_password}", image = "{image}" WHERE id = {current_user.id};')

                    print('PASSEI SEM EMAIL COM PASSWORD')

                    return redirect(url_for("profile", identifier=current_user.identifier))

                if db_execute(f'SELECT email FROM user WHERE email = "{email}"', 'GET').fetchone() == None:

                    db_execute(f'UPDATE user SET name = "{nome}", nickname = "{nickname}", email = "{email}", password = "{new_hashed_password}", image = "{image}" WHERE id = {current_user.id};')

                    print('PASSEI NO EMAIL COM PASSWORD')
                else:
                    flash('Este email já está sendo usado!')
                    
                return redirect(url_for("profile", identifier=current_user.identifier))
            else:
                flash('Senha atual incorreta!')
                return redirect(url_for("profile", identifier=current_user.identifier))

        
        
        if current_user.email == email:
            db_execute(f'UPDATE user SET name = "{nome}", nickname = "{nickname}", image = "{image}" WHERE id = {current_user.id};')

            print('PASSEI NO SEM EMAIL E  SEM PASSWORD')

            return redirect(url_for("profile", identifier=current_user.identifier))

        if db_execute(f'SELECT email FROM user WHERE email = "{email}"', 'GET').fetchone() == None:
            print(email, '===========================')
            db_execute(f'UPDATE user SET name = "{nome}", nickname = "{nickname}", email = "{email}", image = "{image}" WHERE id = {current_user.id};')

            print('PASSEI NO EMAIL SEM PASSWORD')

            return redirect(url_for("profile", identifier=current_user.identifier))
        else:
            flash('Este email já está sendo usado!')


    return render_template('profile.html', user=user, is_following=is_already_followed, error=error)


@app.route('/post/save_post/<identifier>', methods=['POST'])
@login_required
def saving_post(identifier):
    post_id = db_execute(f'SELECT id FROM post WHERE identifier = "{identifier}";', 'GET').fetchone()[0]

    is_already_saved = db_execute(f'SELECT * FROM save_post WHERE user_id = {current_user.id} and post_id = {post_id};', 'GET').fetchone()

    if is_already_saved == None:
        db_execute(f'INSERT INTO save_post (user_id, post_id) VALUES ({current_user.id}, {post_id})')
    else:
        db_execute(f'DELETE FROM save_post WHERE user_id = {current_user.id} and post_id = {post_id};')

    return 'sucess', 200

@app.route('/saved_posts')
@login_required
def saved_post(): 

    all_save_post = db_execute(f'SELECT post_id FROM save_post WHERE user_id = {current_user.id}', 'GET').fetchall()

    result = []
    for post_id in all_save_post:
        get_post = db_execute(f'SELECT * FROM post WHERE id = {post_id[0]}', 'GET').fetchone()

        result.append(Post(
                id=get_post[0],
                user_id=get_post[1],
                titulo=get_post[2],
                texto=get_post[3],
                created_at=get_post[4],
                identifier=get_post[5],
                was_edited=get_post[6],
                current_user_id=current_user.id,
                get_lod='GET'
            ))

    return render_template('save_post.html', save_post=result, showname=showname)


#   RUNNING THE APP IF IS MAIN
if __name__ == '__main__':
    app.secret_key = 'LXproject'
    app.run()