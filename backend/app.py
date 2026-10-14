from flask import Flask, render_template
from flask_cors import CORS
from pathlib import Path

from src.routes.bar_finder import bar_finder_bp
from src.routes.cocktail_creator import cocktail_creator_bp
from src.routes.cocktail_of_the_day import cocktail_of_the_day_bp
from src.routes.feed import feed_bp
from src.routes.search_cocktails import search_cocktails_bp
from src.routes.trending_cocktails import trending_cocktails_bp
from src.routes.user_accounts import user_accounts_bp

from pathlib import Path

template_dir = Path(__file__).resolve().parent.parent / "frontend" / "templates"

app = Flask(__name__, template_folder=str(template_dir))

CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/")
def home():
    return render_template("index.html")

app.register_blueprint(bar_finder_bp)
app.register_blueprint(cocktail_creator_bp)
app.register_blueprint(cocktail_of_the_day_bp)
app.register_blueprint(feed_bp)
app.register_blueprint(search_cocktails_bp)
app.register_blueprint(trending_cocktails_bp)
app.register_blueprint(user_accounts_bp)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)