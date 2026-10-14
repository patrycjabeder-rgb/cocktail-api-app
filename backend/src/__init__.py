from flask import Flask
from src.routes.bar_finder import bar_finder_bp
from src.routes.cocktail_of_the_day import cocktail_of_the_day_bp
from src.routes.feed import feed_bp
from src.routes.search_cocktails import search_cocktails_bp
from src.routes.user_accounts import user_accounts_bp
from src.routes.cocktail_creator import cocktail_creator_bp
from src.routes.trending_cocktails import trending_cocktails_bp

def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)

    app.register_blueprint(bar_finder_bp)
    app.register_blueprint(cocktail_of_the_day_bp)
    app.register_blueprint(feed_bp)
    app.register_blueprint(search_cocktails_bp)
    app.register_blueprint(user_accounts_bp)
    app.register_blueprint(cocktail_creator_bp)
    app.register_blueprint(trending_cocktails_bp)

    return app
