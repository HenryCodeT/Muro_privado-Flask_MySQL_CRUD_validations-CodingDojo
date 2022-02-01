from wall_app import app
from wall_app.controllers import login_registration_controller,messages_controller

if __name__ == "__main__":
    app.run(debug=True)