from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, desc
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired
from sqlalchemy.engine import ScalarResult
import requests


# THE DATABASE
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ratings-collection.db"

API_KEY = "f84bd283f269ae39390fd22e875d5941"

Bootstrap5(app)
db.init_app(app)


# THE TABLE
class Ratings_List(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, unique=True)
    ranking: Mapped[int] = mapped_column(nullable=True)
    image_url: Mapped[str] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(unique=True, nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)
    rating: Mapped[float] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=False)
    review: Mapped[str] = mapped_column(nullable=True)


with app.app_context():
    db.create_all()


class EditMovieRatingReviewForm(FlaskForm):
    new_rating = FloatField("Your rating out of 10, e.g  7.5", validators=[DataRequired()])
    review = StringField("Your review", validators=[DataRequired()])
    submit = SubmitField("Edit")


class AddMovieForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    submit = SubmitField("Submit")


def get_data_from_database():
    """Read all records from database"""
    with app.app_context():
        ratings_dict_list = []
        err_string = "Error"
        try:
            result = db.session.execute(db.select(Ratings_List).order_by(Ratings_List.rating))
        except:
            return err_string
        else:
            all_ratings = result.scalars().all()
            if all_ratings:
                for rating in all_ratings:
                    rating_dict = {
                        "id": rating.id,
                        "ranking": rating.ranking,
                        "url": rating.image_url,
                        "title": rating.title,
                        "year": rating.year,
                        "rating": rating.rating,
                        "description": rating.description,
                        "review": rating.review
                    }
                    ratings_dict_list.append(rating_dict)
                return ratings_dict_list
            else:
                return False


@app.route("/")
def home():
    """
    The main page for the app. Checks if there are movies in the database, if not, redirects to /add. If there are movies, it renders the index.html template, passing the list of movies to the template.
    """
    data = get_data_from_database()
    if data == "Error" or data == False:
        print("redirecting...")
        return redirect(url_for("add"))
    else:
        with app.app_context():
            for i in range(len(data), 0, -1):
                movie_to_update = db.session.execute(
                    db.select(Ratings_List).where(Ratings_List.title == data[len(data) - i]["title"])).scalar()
                movie_to_update.ranking = i
                db.session.commit()
    return render_template("index.html", ratings=data)


@app.route("/add", methods=["GET", "POST"])
def add():
    """
    This route is for adding movies to the database. 
    It first renders an "add.html" template with a form to enter the movie title.
    Once the form is submitted, it makes a GET request to the The Movie Database API to search for movies with the given title.
    It then renders a "select.html" template with a list of movies found, with their titles, descriptions, image URLs and release years.
    The user can then select a movie from this list, and it will be added to the database.
    """
    form = AddMovieForm()
    value = form.title.data

    if form.validate_on_submit():
        api_url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}"
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZDM2MjcxM2YxNDJiODQ0OGFiNjIwMTM1ZDMzZjA1MSIsIm5iZiI6MTcyNTU1NDY0Mi41OTA0MTYsInN1YiI6IjY2ZDlkOTVhMWUwMzA1MTZjYTJhMDc5YyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.mb1f0BGvBzEl7CeV1LXIxGvapbAVZ7CIyUm3_b724HY"
        }
        params = {
            "query": value
        }
        response = requests.get(api_url, headers=headers, params=params)
        movie_ids = [mi["id"] for mi in response.json()["results"]]
        # print(movie_ids)
        movie_titles = [mt["title"] for mt in response.json()["results"]]
        movie_descriptions = [md["overview"] for md in response.json()["results"]]
        movie_image_urls = [f'https://image.tmdb.org/t/p/w500/{mi["poster_path"]}' for mi in response.json()["results"]]
        # print(movie_image_urls)
        movie_years = [my["release_date"].split("-")[0] for my in response.json()["results"]]

        final_list = list(zip(movie_ids, movie_titles, movie_descriptions, movie_image_urls, movie_years))
        # print(final_list)
        return render_template("select.html", final_list=final_list)
    else:
        return render_template("add.html", form=form, values=value)


@app.route("/add-create", methods=["GET", "POST"])
def add_create():
    """
    This route is for adding movies to the database. 
    It first renders an "edit.html" template with a form to enter the movie title, rating and review.
    Once the form is submitted, it makes a GET request to the The Movie Database API to search for the movie with the given title.
    It then renders the same "edit.html" template with the movie's title, image URL, year and description.
    The user can then edit the movie's rating and review.
    """
    data = request.args.get("data")
    api_url = f"https://api.themoviedb.org/3/movie/{data}?api_key={API_KEY}"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZDM2MjcxM2YxNDJiODQ0OGFiNjIwMTM1ZDMzZjA1MSIsIm5iZiI6MTcyNTU1NDY0Mi41OTA0MTYsInN1YiI6IjY2ZDlkOTVhMWUwMzA1MTZjYTJhMDc5YyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.mb1f0BGvBzEl7CeV1LXIxGvapbAVZ7CIyUm3_b724HY"
    }
    response = requests.get(api_url, headers=headers)
    movie_title = response.json()["original_title"]
    image_url = f"https://image.tmdb.org/t/p/w500/{response.json()['poster_path']}"
    year = response.json()["release_date"].split("-")[0]
    description = response.json()["overview"]

    with app.app_context():
        new_movie = Ratings_List(
            image_url=image_url,
            title=movie_title,
            year=year,
            description=description,
            ranking=0,
            rating=0,
            review="",

        )
        existing_book = Ratings_List.query.filter_by(title=movie_title).first()
        if existing_book:
            pass
        else:
            db.session.add(new_movie)
            db.session.commit()

        form = EditMovieRatingReviewForm()
        values = [
            form.new_rating.data, form.review.data]
        if form.validate_on_submit():
            with app.app_context():
                movie_to_update = db.session.execute(
                    db.select(Ratings_List).where(Ratings_List.title == movie_title)).scalar()
                movie_to_update.rating = values[0]
                movie_to_update.review = values[1]
                db.session.commit()
                print(movie_to_update.rating, movie_to_update.review)
                return redirect(url_for("home"))
        else:
            return render_template("edit.html", form=form, values=values)


@app.route("/edit", methods=["GET", "POST"])
def edit():
    """
    The route for the edit page. If the request method is POST, it validates the form, updates the movie with the given id and redirects to the home page.
    If the request method is GET, or the form is invalid, it renders the edit.html template, passing the form and the values of the form fields as arguments.
    """
    form = EditMovieRatingReviewForm()
    values = [
        form.new_rating.data, form.review.data
    ]
    if request.method == "POST":
        if form.validate_on_submit():
            with app.app_context():
                movie_id = request.args.get("id")
                movie_to_update = db.get_or_404(Ratings_List, movie_id)
                movie_to_update.rating = values[0]
                movie_to_update.review = values[1]
                db.session.commit()
                return redirect(url_for("home"))
        else:
            return render_template("edit.html", form=form, values=values)
    else:
        return render_template("edit.html", form=form, values=values)


@app.route("/delete", methods=["GET", "POST"])
def delete():
    """
    The route for the delete page. If the request method is POST, it validates the form, deletes the movie with the given id and redirects to the home page.
    If the request method is GET, or the form is invalid, it renders the delete.html template, passing the form and the values of the form fields as arguments.
    """
    with app.app_context():
        movie_id = request.args.get("id")
        movie_to_delete = db.get_or_404(Ratings_List, movie_id)
        db.session.delete(movie_to_delete)
        db.session.commit()
        return redirect(url_for("home"))


@app.route("/select", methods=["GET", "POST"])
def select():
    return render_template("select.html")


if __name__ == '__main__':
    app.run(debug=True)
