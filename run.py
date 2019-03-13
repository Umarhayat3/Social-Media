# Social-Media/run.py

# importing some bultin libraries
from config import app, db, request, Response, json
from models import User, Post, Comment, React


@app.route('/')
def index():
    user = User.query.filter_by(user_name="user_name_1").first()
    print(type(user.comment))
    # c = Comment.query.filter_by(user.id)
    for c in user.comment:
        print(c.content)
    return "<h1> Welcome to home <h1>"


@app.route('/register', methods=['POST'])
def user_registeration():
    user_info = request.get_json()
    user_obj = User(user_name=user_info["user_name"], first_name=user_info["first_name"],
                    last_name=user_info["last_name"], email=user_info["email"])
    db.session.add(user_obj)
    db.session.commit()
    return '<h1> Successfull! <h1>'


@app.route('/post', methods=['POST', 'PUT', 'DELETE'])
def post():
    try:
        post_data = request.get_json()
        if request.method == 'POST' or request.method == 'PUT':
            if request.method == 'POST':
                get_user = User.query.filter_by(user_name=post_data["user_name"]).first()
                post_obj = Post(user=get_user, content=post_data["content"])
            elif request.method == 'PUT':               # :update

                post_obj = Post.query.filter_by(id=post_data["id"]).first()
                post_obj.content = post_data["content"]
            db.session.add(post_obj)
            db.session.commit()
        elif request.method == 'DELETE':
            post_obj = Post.query.filter_by(id=post_data["id"]).first()
            db.session.delete(post_obj)
            db.session.commit()
    except KeyError:
        print("Bad format!")

    return '<h1> Successfull! <h1>'


@app.route('/comment', methods=['POST', 'PUT', 'DELETE'])
def comment():
    update_data = request.get_json()

    dct = {"msg": "Successfull!"}
    try:
        if request.method == 'POST' or request.method == 'PUT':
            if request.method == 'POST':

                get_user = User.query.filter_by(user_name=update_data["user_name"]).first()
                get_post = Post.query.filter_by(id=update_data["post_id"]).first()
                comment_obj = Comment(user=get_user, post=get_post, content=update_data["content"])

            elif request.method == 'PUT':               # :update

                comment_obj = Comment.query.filter_by(id=update_data["id"]).first()
                comment_obj.content = update_data["content"]

            db.session.add(comment_obj)
            db.session.commit()
        elif request.method == 'DELETE':

            comment_obj = Comment.query.filter_by(id=update_data["id"]).first()
            db.session.delete(comment_obj)
            db.session.commit()
    except KeyError:
        print("Bad format!")

    json_obj = json.dumps(dct)
    return Response(json_obj, mimetype="application/json")


@app.route('/react', methods=['POST'])
def react():
    react_data = request.get_json()
    get_user = User.query.filter_by(user_name=react_data["user_name"]).first()
    get_post = Post.query.filter_by(id=react_data["post_id"]).first()
    react_obj = React(user=get_user, post=get_post, reaction=react_data["reaction"])
    db.session.add(react_obj)
    db.session.commit()
    return '<h1> Successfull! <h1>'


@app.route('/search', methods=['GET'])
def Search():
    search_result = {}

    if request.args.get("username"):
        users_list = User.query.filter_by(user_name=request.args.get("username")).all()

        for user in users_list:
            search_result = user.profile()

    elif request.args.get("content"):
        posts_list = Post.query.filter_by(content=request.args.get("content")).distinct().all()
        comments_list = Comment.query.filter_by(content=request.args.get("content")).distinct().all()
        search_result = {"posts": [], "comments": []}

        for post_item in posts_list:
            search_result['posts'].append(post_item.info())

        for comment_item in comments_list:
            search_result['comments'].append(comment_item.detail())

    json_obj = json.dumps(search_result)
    return Response(json_obj, mimetype="application/json")


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
