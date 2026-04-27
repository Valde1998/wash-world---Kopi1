from flask import Flask, request, jsonify, render_template, session 
from flask_cors import CORS
from icecream import ic
import uuid
import time
import x

ic.configureOutput(prefix=f"_____ | ", includeContext=True)

app = Flask(__name__)
app.secret_key = "wash-world-secret-key"
CORS(app)

##############################
@app.get("/")
def index():
    return jsonify({
        "status": "ok",
        "message": "Wash World backend connected"
    }), 200


##############################
@app.get("/api-locations")
def get_locations():
    try:
        # Fake data først. Senere skifter vi det til database.
        return jsonify({
            "locations": [
                {
                    "location_pk": "1",
                    "name": "Wash World Køge",
                    "address": "Køge",
                    "queue": 3,
                    "status": "open"
                },
                {
                    "location_pk": "2",
                    "name": "Wash World Ishøj",
                    "address": "Ishøj",
                    "queue": 6,
                    "status": "open"
                },
                {
                    "location_pk": "3",
                    "name": "Wash World Roskilde",
                    "address": "Roskilde",
                    "queue": 1,
                    "status": "open"
                }
            ]
        }), 200

    except Exception as ex:
        ic(ex)
        return str(ex), 500
    finally:
        pass


##############################
@app.get("/api-users")
def get_users():
    try:
        db, cursor = x.db()

        q = "SELECT * FROM users"
        cursor.execute(q)

        rows = cursor.fetchall()

        return jsonify({"users": rows}), 200

    except Exception as ex:
        ic(ex)
        return str(ex), 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.post("/api-sign-up")
def sign_up():
    try:
        user_first_name = x.validate_user_first_name()
        user_last_name = x.validate_user_last_name()
        user_email = x.validate_email(request.form.get("user_email", ""))
        user_password = x.validate_user_password(request.form.get("user_password", ""))

        user_pk = uuid.uuid4().hex
        user_created_at = int(time.time())

        db, cursor = x.db()

        q = """
            INSERT INTO users
            (user_pk, user_first_name, user_last_name, user_email, user_password, user_created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(q, (
            user_pk,
            user_first_name,
            user_last_name,
            user_email,
            user_password,
            user_created_at
        ))

        db.commit()

        return jsonify({
            "message": "User created",
            "user_pk": user_pk
        }), 201

    except Exception as ex:
        ic(ex)

        if "company_exception user_first_name" in str(ex):
            return f"First name must be {x.USER_FIRST_NAME_MIN} to {x.USER_FIRST_NAME_MAX} characters", 400

        if "company_exception user_last_name" in str(ex):
            return f"Last name must be {x.USER_LAST_NAME_MIN} to {x.USER_LAST_NAME_MAX} characters", 400

        if "company_exception email" in str(ex):
            return "Invalid email", 400

        if "company_exception user_password" in str(ex):
            return f"Password must be {x.USER_PASSWORD_MIN} to {x.USER_PASSWORD_MAX} characters", 400

        return str(ex), 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.post("/api-login")
def login():
    try:
        user_email = x.validate_email(request.form.get("user_email", ""))
        user_password = x.validate_user_password(request.form.get("user_password", ""))

        db, cursor = x.db()

        q = """
            SELECT user_pk, user_first_name, user_last_name, user_email
            FROM users
            WHERE user_email = %s AND user_password = %s
        """

        cursor.execute(q, (user_email, user_password))
        user = cursor.fetchone()

        if not user:
            return "Invalid email or password", 401

        session["user"] = user

        return jsonify({
            "message": "Login successful",
            "user": user
        }), 200

    except Exception as ex:
        ic(ex)

        if "company_exception email" in str(ex):
            return "Invalid email", 400

        if "company_exception user_password" in str(ex):
            return f"Password must be {x.USER_PASSWORD_MIN} to {x.USER_PASSWORD_MAX} characters", 400

        return str(ex), 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.post("/api-logout")
def logout():
    try:
        session.clear()
        return jsonify({"message": "Logged out"}), 200

    except Exception as ex:
        ic(ex)
        return str(ex), 500
    finally:
        pass


##############################
@app.get("/api-me")
def me():
    try:
        if "user" not in session:
            return "Not logged in", 401

        return jsonify({
            "user": session["user"]
        }), 200

    except Exception as ex:
        ic(ex)
        return str(ex), 500
    finally:
        pass