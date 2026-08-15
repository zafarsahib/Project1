
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
    Pet,
    AdoptionRequest
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
    pets = Pet.query.order_by(
        Pet.id.desc()
    ).all()

    return render_template(
        "home.html",
        pets=pets
    )


@app.route("/browse-pets")
def browse_pets():
    search = request.args.get(
        "search",
        ""
    ).strip()

    species = request.args.get(
        "species",
        ""
    )

    age = request.args.get(
        "age",
        ""
    )

    status = request.args.get(
        "status",
        ""
    )

    page = request.args.get(
        "page",
        1,
        type=int
    )

    if page < 1:
        page = 1

    pets_query = Pet.query

    if search:
        pets_query = pets_query.filter(
            Pet.name.ilike(f"%{search}%")
        )

    if species:
        pets_query = pets_query.filter_by(
            species=species
        )

    if status:
        pets_query = pets_query.filter_by(
            status=status
        )

    if age == "under1":
        pets_query = pets_query.filter(
            Pet.age < 1
        )
    elif age == "1to3":
        pets_query = pets_query.filter(
            Pet.age.between(1, 3)
        )
    elif age == "4plus":
        pets_query = pets_query.filter(
            Pet.age >= 4
        )

    pagination = pets_query.order_by(
        Pet.id.desc()
    ).paginate(
        page=page,
        per_page=8,
        error_out=False
    )

    pets = pagination.items

    return render_template(
        "browse_pets.html",
        pets=pets,
        pagination=pagination,
        search=search,
        species=species,
        age=age,
        status=status
    )


@app.route("/pet/<int:pet_id>")
def pet_details(
    pet_id
):
    pet = db.session.get(
        Pet,
        pet_id
    )

    if pet is None:
        flash(
            "Pet not found."
        )

        return redirect(
            url_for(
                "browse_pets"
            )
        )

    user_request = None

    if current_user.is_authenticated:
        user_request = AdoptionRequest.query.filter_by(
            user_id=current_user.id,
            pet_id=pet.id
        ).order_by(
            AdoptionRequest.id.desc()
        ).first()

    return render_template(
        "pet_details.html",
        pet=pet,
        user_request=user_request
    )


@app.route(
    "/adopt/<int:pet_id>",
    methods=["GET", "POST"]
)
@login_required
def adopt_pet(
    pet_id
):
    pet = db.session.get(
        Pet,
        pet_id
    )

    if pet is None:
        flash(
            "Pet not found."
        )

        return redirect(
            url_for(
                "browse_pets"
            )
        )

    if current_user.role == "Admin":
        flash(
            "Administrators cannot submit adoption requests."
        )

        return redirect(
            url_for(
                "pet_details",
                pet_id=pet.id
            )
        )

    if pet.status == "Adopted":
        flash(
            "This pet has already been adopted."
        )

        return redirect(
            url_for(
                "pet_details",
                pet_id=pet.id
            )
        )

    existing_request = AdoptionRequest.query.filter_by(
        user_id=current_user.id,
        pet_id=pet.id
    ).filter(
        AdoptionRequest.status.in_(
            ["Pending", "Approved"]
        )
    ).first()

    if existing_request:
        if existing_request.status == "Pending":
            flash(
                "You already have a pending adoption request for this pet."
            )
        else:
            flash(
                "You have already been approved to adopt this pet."
            )

        return redirect(
            url_for(
                "pet_details",
                pet_id=pet.id
            )
        )

    if request.method == "POST":
        comments = request.form.get(
            "comments",
            ""
        ).strip()

        adoption_request = AdoptionRequest(
            user_id=current_user.id,
            pet_id=pet.id,
            comments=comments,
            status="Pending"
        )

        db.session.add(
            adoption_request
        )

        db.session.commit()

        flash(
            "Adoption request submitted successfully."
        )

        return redirect(
            url_for(
                "dashboard"
            )
        )

    return render_template(
        "adoption_request.html",
        pet=pet
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
    adoption_requests = AdoptionRequest.query.filter_by(
        user_id=current_user.id
    ).order_by(
        AdoptionRequest.id.desc()
    ).all()

    total_requests = len(adoption_requests)

    pending_requests = sum(
        1 for request in adoption_requests
        if request.status == "Pending"
    )

    approved_requests = sum(
        1 for request in adoption_requests
        if request.status == "Approved"
    )

    rejected_requests = sum(
        1 for request in adoption_requests
        if request.status == "Rejected"
    )

    return render_template(
        "dashboard.html",
        adoption_requests=adoption_requests,
        total_requests=total_requests,
        pending_requests=pending_requests,
        approved_requests=approved_requests,
        rejected_requests=rejected_requests
    )


@app.route(
    "/admin"
)
@admin_required
def admin_dashboard():
    adoption_requests = AdoptionRequest.query.filter_by(
        status="Pending"
    ).order_by(
        AdoptionRequest.request_date.desc()
    ).all()

    return render_template(
        "admin_dashboard.html",
        adoption_requests=adoption_requests
    )

@app.route(
    "/admin/pets/add",
    methods=["GET", "POST"]
)
@admin_required
def add_pet():
    if request.method == "POST":
        name = request.form.get(
            "name",
            ""
        ).strip()

        species = request.form.get(
            "species",
            ""
        ).strip()

        breed = request.form.get(
            "breed",
            ""
        ).strip()

        age = request.form.get(
            "age",
            ""
        ).strip()

        gender = request.form.get(
            "gender",
            ""
        ).strip()

        description = request.form.get(
            "description",
            ""
        ).strip()

        image = request.form.get(
            "image",
            ""
        ).strip()

        if not name or not species or not breed or not age or not gender:
            flash(
                "Please complete all required fields."
            )

            return render_template(
                "add_pet.html"
            )

        try:
            age = int(age)
        except ValueError:
            flash(
                "Age must be a valid number."
            )

            return render_template(
                "add_pet.html"
            )

        if age < 0:
            flash(
                "Age cannot be negative."
            )

            return render_template(
                "add_pet.html"
            )

        pet = Pet(
            name=name,
            species=species,
            breed=breed,
            age=age,
            gender=gender,
            description=description,
            status="Available",
            image=image,
            user_id=current_user.id
        )

        db.session.add(
            pet
        )

        db.session.commit()

        flash(
            "Pet added successfully."
        )

        return redirect(
            url_for(
                "admin_dashboard"
            )
        )

    return render_template(
        "add_pet.html"
    )

@app.route(
    "/admin/adoption/approve/<int:request_id>",
    methods=["POST"]
)
@admin_required
def approve_adoption(
    request_id
):
    adoption_request = db.session.get(
        AdoptionRequest,
        request_id
    )

    if adoption_request is None:
        flash(
            "Adoption request not found."
        )

        return redirect(
            url_for(
                "admin_dashboard"
            )
        )

    if adoption_request.status != "Pending":
        flash(
            "This adoption request has already been processed."
        )

        return redirect(
            url_for(
                "admin_dashboard"
            )
        )

    pet = adoption_request.pet

    adoption_request.status = "Approved"

    pet.status = "Adopted"

    other_requests = AdoptionRequest.query.filter(
        AdoptionRequest.pet_id == pet.id,
        AdoptionRequest.id != adoption_request.id,
        AdoptionRequest.status == "Pending"
    ).all()

    for other_request in other_requests:
        other_request.status = "Rejected"

    db.session.commit()

    flash(
        "Adoption request approved successfully."
    )

    return redirect(
        url_for(
            "admin_dashboard"
        )
    )

@app.route(
    "/admin/pets"
)
@admin_required
def manage_pets():
    pets = Pet.query.order_by(
        Pet.id.desc()
    ).all()

    adopted_by = {}

    approved_requests = AdoptionRequest.query.filter_by(
        status="Approved"
    ).all()

    for adoption_request in approved_requests:
        adopted_by[adoption_request.pet_id] = (
            adoption_request.user.username
        )

    return render_template(
        "manage_pets.html",
        pets=pets,
        adopted_by=adopted_by
    )

@app.route(
    "/admin/pets/edit/<int:pet_id>",
    methods=["GET", "POST"]
)
@admin_required
def edit_pet(
    pet_id
):
    pet = db.session.get(
        Pet,
        pet_id
    )

    if pet is None:
        flash(
            "Pet not found."
        )

        return redirect(
            url_for(
                "manage_pets"
            )
        )

    if request.method == "POST":
        name = request.form.get(
            "name",
            ""
        ).strip()

        species = request.form.get(
            "species",
            ""
        ).strip()

        breed = request.form.get(
            "breed",
            ""
        ).strip()

        age = request.form.get(
            "age",
            ""
        ).strip()

        gender = request.form.get(
            "gender",
            ""
        ).strip()

        description = request.form.get(
            "description",
            ""
        ).strip()

        image = request.form.get(
            "image",
            ""
        ).strip()

        if not name or not species or not breed or not age or not gender:
            flash(
                "Please complete all required fields."
            )

            return render_template(
                "edit_pet.html",
                pet=pet
            )

        try:
            age = int(age)
        except ValueError:
            flash(
                "Age must be a valid number."
            )

            return render_template(
                "edit_pet.html",
                pet=pet
            )

        if age < 0:
            flash(
                "Age cannot be negative."
            )

            return render_template(
                "edit_pet.html",
                pet=pet
            )

        pet.name = name
        pet.species = species
        pet.breed = breed
        pet.age = age
        pet.gender = gender
        pet.description = description
        pet.image = image

        db.session.commit()

        flash(
            "Pet updated successfully."
        )

        return redirect(
            url_for(
                "manage_pets"
            )
        )

    return render_template(
        "edit_pet.html",
        pet=pet
    )

@app.route(
    "/admin/pets/delete/<int:pet_id>",
    methods=["POST"]
)
@admin_required
def delete_pet(
    pet_id
):
    pet = db.session.get(
        Pet,
        pet_id
    )

    if pet is None:
        flash(
            "Pet not found."
        )

        return redirect(
            url_for(
                "manage_pets"
            )
        )

    if pet.status != "Available":
        flash(
            "Only available pets can be deleted."
        )

        return redirect(
            url_for(
                "manage_pets"
            )
        )

    existing_request = AdoptionRequest.query.filter_by(
        pet_id=pet.id
    ).first()

    if existing_request:
        flash(
            "This pet cannot be deleted because it has adoption request history."
        )

        return redirect(
            url_for(
                "manage_pets"
            )
        )

    db.session.delete(
        pet
    )

    db.session.commit()

    flash(
        "Pet deleted successfully."
    )

    return redirect(
        url_for(
            "manage_pets"
        )
    )

@app.route(
    "/admin/users"
)
@admin_required
def manage_users():
    users = User.query.order_by(
        User.id.asc()
    ).all()

    return render_template(
        "manage_users.html",
        users=users
    )

@app.route(
    "/admin/adoption/reject/<int:request_id>",
    methods=["POST"]
)
@admin_required
def reject_adoption(
    request_id
):
    adoption_request = db.session.get(
        AdoptionRequest,
        request_id
    )

    if adoption_request is None:
        flash(
            "Adoption request not found."
        )

        return redirect(
            url_for(
                "admin_dashboard"
            )
        )

    if adoption_request.status != "Pending":
        flash(
            "This adoption request has already been processed."
        )

        return redirect(
            url_for(
                "admin_dashboard"
            )
        )

    adoption_request.status = "Rejected"

    db.session.commit()

    flash(
        "Adoption request rejected successfully."
    )

    return redirect(
        url_for(
            "admin_dashboard"
        )
    )


# Logout
# The navbar uses an <a href=""> link, which sends a GET request.
# Therefore this route accepts GET instead of POST.

@app.route("/logout")
@login_required
def logout():
    logout_user()

    flash(
        "Logged out successfully.",
        "success"
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