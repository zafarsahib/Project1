from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)

from functools import wraps

from models import (
    db,
    User,
    Pet
)


app = Flask(__name__)


app.config["SECRET_KEY"] = "mysecretkey"


app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///pet_adoption.db"
)


app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(
    app
)


login_manager = LoginManager()


login_manager.init_app(
    app
)


login_manager.login_view = "login"



@login_manager.user_loader
def load_user(
    user_id
):

    return db.session.get(
        User,
        int(user_id)
    )



def admin_required(function):

    @wraps(function)

    @login_required
    def wrapper(
        *args,
        **kwargs
    ):

        if current_user.role != "Admin":

            flash(
                "Admin access required."
            )

            return redirect(
                url_for(
                    "dashboard"
                )
            )


        return function(
            *args,
            **kwargs
        )


    return wrapper



with app.app_context():

    db.create_all()



@app.route("/")
def home():

    return render_template(
        "home.html"
    )



@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()


        email = request.form.get(
            "email",
            ""
        ).strip()


        password = request.form.get(
            "password",
            ""
        )


        if not username or not email or not password:

            flash(
                "All fields are required."
            )


            return render_template(
                "register.html"
            )


        existing_username = User.query.filter_by(
            username=username
        ).first()


        if existing_username:

            flash(
                "Username already exists."
            )


            return render_template(
                "register.html"
            )


        existing_email = User.query.filter_by(
            email=email
        ).first()


        if existing_email:

            flash(
                "Email already exists."
            )


            return render_template(
                "register.html"
            )


        user = User(

            username=username,

            email=email,

            role="User"

        )


        user.set_password(
            password
        )


        db.session.add(
            user
        )


        db.session.commit()


        flash(
            "Account created successfully."
        )


        return redirect(
            url_for(
                "login"
            )
        )


    return render_template(
        "register.html"
    )



@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()


        password = request.form.get(
            "password",
            ""
        )


        user = User.query.filter_by(
            username=username
        ).first()



        if user is None or not user.check_password(
            password
        ):

            flash(
                "Invalid username or password."
            )


            return render_template(
                "login.html"
            )


        login_user(
            user
        )


        flash(
            "Logged in successfully."
        )


        if user.role == "Admin":

            return redirect(
                url_for(
                    "admin_dashboard"
                )
            )


        return redirect(
            url_for(
                "dashboard"
            )
        )


    return render_template(
        "login.html"
    )



@app.route(
    "/dashboard"
)
@login_required
def dashboard():

    return render_template(
        "dashboard.html"
    )



@app.route(
    "/admin"
)
@admin_required
def admin_dashboard():

    return render_template(
        "admin_dashboard.html"
    )



@app.route(
    "/logout",
    methods=["POST"]
)
@login_required
def logout():

    logout_user()


    flash(
        "Logged out successfully."
    )


    return redirect(
        url_for(
            "home"
        )
    )



if __name__ == "__main__":

    app.run(
        debug=True
    )