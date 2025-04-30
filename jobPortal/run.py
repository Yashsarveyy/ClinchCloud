from app import create_app, db

app = create_app()

if __name__ == '__main__':
    # Ensure the instance folder exists
    import os
    os.makedirs('instance', exist_ok=True)

    # Create all tables defined in your models
    with app.app_context():
        db.create_all()  

    # Launch the server
    app.run(debug=True)
