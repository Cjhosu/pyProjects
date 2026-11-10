def register_blueprints(app):
    from routes.dashboard import bp as dashboard_bp
    from routes.materials import bp as materials_bp
    from routes.products import bp as products_bp
    from routes.production import bp as production_bp

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(materials_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(production_bp)
