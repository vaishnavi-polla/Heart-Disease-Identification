from dotenv import load_dotenv
import os
load_dotenv()
from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import joblib
import pandas as pd
import mysql.connector
import os


app = Flask(__name__)


# ==================================================
# FLASK SECRET KEY
# ==================================================

app.secret_key = "heart_disease_identifier_secret_key"


# ==================================================
# LOAD TRAINED MODEL
# ==================================================

model = joblib.load("heart_model.pkl")


# ==================================================
# MYSQL DATABASE CONNECTION
# ==================================================

def get_db_connection():

    connection = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",

        # ------------------------------------------------
        # PUT YOUR MYSQL PASSWORD HERE
        # ------------------------------------------------
        password=os.getenv("MYSQL_PASSWORD"),
        database="heartcare",
        connection_timeout=5,
        use_pure=True
    )

    return connection


# ==================================================
# HOME PAGE
# ==================================================

@app.route("/")
def home():

    return render_template("index.html")


# ==================================================
# LOGIN SELECTION PAGE
# ==================================================

@app.route("/login")
def login():

    return render_template("login.html")


# ==================================================
# PATIENT LOGIN
# ==================================================

@app.route("/patient-login", methods=["GET", "POST"])
def patient_login():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        connection = None
        cursor = None

        try:

            connection = get_db_connection()

            cursor = connection.cursor(dictionary=True)

            cursor.execute(
                """
                SELECT id, username, password
                FROM users
                WHERE username = %s
                """,
                (username,)
            )

            user = cursor.fetchone()

            # ------------------------------------------
            # CHECK USERNAME AND PASSWORD
            # ------------------------------------------

            if user:

                try:

                    password_correct = check_password_hash(
                        user["password"],
                        password
                    )

                except ValueError:

                    password_correct = False

            else:

                password_correct = False

            # ------------------------------------------
            # LOGIN SUCCESS
            # ------------------------------------------

            if password_correct:

                session.clear()

                session["user_logged_in"] = True
                session["user_id"] = user["id"]
                session["username"] = user["username"]

                print(
                    "User logged in:",
                    user["username"]
                )

                return redirect(
                    url_for("user_dashboard")
                )

            # ------------------------------------------
            # LOGIN FAILED
            # ------------------------------------------

            return render_template(
                "patient_login.html",
                error="Invalid username or password."
            )

        except mysql.connector.Error as error:

            print(
                "Patient login database error:",
                error
            )

            return render_template(
                "patient_login.html",
                error="Unable to connect to database."
            )

        finally:

            if cursor:

                cursor.close()

            if connection:

                connection.close()

    return render_template(
        "patient_login.html"
    )


    # ------------------------------------------
    # CHECK USER LOGIN
    # ------------------------------------------

    if not session.get("user_logged_in"):

        return redirect(
            url_for("patient_login")
        )


    user_id = session.get("user_id")

    username = session.get("username")


    connection = None
    cursor = None


    try:

        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )


        # ------------------------------------------
        # GET THIS USER'S RECORDS ONLY
        # ------------------------------------------

        cursor.execute(
            """
            SELECT
                id,
                age,
                sex,
                cp,
                trestbps,
                chol,
                fbs,
                restecg,
                thalach,
                exang,
                oldpeak,
                slope,
                ca,
                thal,
                prediction,
                created_at
            FROM patient_records
            WHERE user_id = %s
            ORDER BY id DESC
            """,
            (user_id,)
        )


        records = cursor.fetchall()


        # ------------------------------------------
        # OPEN USER DASHBOARD
        # ------------------------------------------

        return render_template(
            "user_dashboard.html",
            username=username,
            records=records
        )


    except mysql.connector.Error as error:

        print(
            "Dashboard database error:",
            error
        )

        return "Unable to load dashboard."


    finally:

        if cursor:

            cursor.close()


        if connection:

            connection.close()


# ==================================================
# USER REGISTRATION
# ==================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"].strip()
        password = request.form["password"]

        # ------------------------------------------
        # BASIC VALIDATION
        # ------------------------------------------

        if not username or not password:

            return render_template(
                "register.html",
                error="Username and password are required."
            )

        if len(username) < 3:

            return render_template(
                "register.html",
                error="Username must contain at least 3 characters."
            )

        if len(password) < 6:

            return render_template(
                "register.html",
                error="Password must contain at least 6 characters."
            )

        # ------------------------------------------
        # HASH PASSWORD
        # ------------------------------------------

        password_hash = generate_password_hash(
            password
        )

        connection = None
        cursor = None

        try:

            connection = get_db_connection()

            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO users
                (
                    username,
                    password
                )
                VALUES
                (
                    %s,
                    %s
                )
                """,
                (
                    username,
                    password_hash
                )
            )

            connection.commit()

            print(
                "User registered successfully:",
                username
            )

            return redirect(
                url_for("patient_login")
            )

        except mysql.connector.IntegrityError:

            return render_template(
                "register.html",
                error="Username already exists."
            )

        except mysql.connector.Error as error:

            print("Registration error:", error)

            return render_template(
                "register.html",
                error="Registration failed. Please try again."
            )

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    return render_template("register.html")




    # ==================================================
# USER DASHBOARD
# ==================================================

@app.route("/user-dashboard")
def user_dashboard():

    # ------------------------------------------
    # LOGIN PROTECTION
    # ------------------------------------------

    if not session.get("user_logged_in"):

        return redirect(
            url_for("patient_login")
        )


    # ------------------------------------------
    # GET LOGGED-IN USER DETAILS
    # ------------------------------------------

    user_id = session.get("user_id")
    username = session.get("username")


    connection = None
    cursor = None


    try:

        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )


        # ------------------------------------------
        # GET USER'S OWN RECORDS
        # ------------------------------------------

        cursor.execute(
            """
            SELECT
                id,
                age,
                sex,
                cp,
                trestbps,
                chol,
                fbs,
                restecg,
                thalach,
                exang,
                oldpeak,
                slope,
                ca,
                thal,
                prediction,
                created_at
            FROM patient_records
            WHERE user_id = %s
            ORDER BY id DESC
            """,
            (user_id,)
        )


        records = cursor.fetchall()


        # ------------------------------------------
        # COUNT USER RECORDS
        # ------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM patient_records
            WHERE user_id = %s
            """,
            (user_id,)
        )


        result = cursor.fetchone()

        total_records = result["total"]


        # ------------------------------------------
        # OPEN USER DASHBOARD
        # ------------------------------------------

        return render_template(
            "user_dashboard.html",
            username=username,
            records=records,
            total_records=total_records
        )


    # ------------------------------------------
    # DATABASE ERROR
    # ------------------------------------------

    except mysql.connector.Error as error:

        print(
            "User dashboard database error:",
            error
        )

        return "Unable to load user dashboard."


    # ------------------------------------------
    # CLOSE DATABASE
    # ------------------------------------------

    finally:

        if cursor:

            cursor.close()


        if connection:

            connection.close()
# ==================================================
# USER PROFILE
# ==================================================

@app.route("/profile")
def profile():

    if not session.get("user_logged_in"):

        return redirect(
            url_for("patient_login")
        )

    user_id = session.get("user_id")

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT id, username
            FROM users
            WHERE id = %s
            """,
            (user_id,)
        )

        user = cursor.fetchone()

        if not user:

            session.clear()

            return redirect(
                url_for("patient_login")
            )

        return render_template(
            "profile.html",
            user=user
        )

    except mysql.connector.Error as error:

        print(
            "Profile database error:",
            error
        )

        return "Unable to load profile."

    finally:

        if cursor:

            cursor.close()

        if connection:

            connection.close()
# ==================================================
# MY RECORDS
# ==================================================

@app.route("/my-records")
def my_records():

    if not session.get("user_logged_in"):

        return redirect(
            url_for("patient_login")
        )

    user_id = session.get("user_id")

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT
                id,
                age,
                sex,
                trestbps,
                chol,
                thalach,
                prediction,
                created_at
            FROM patient_records
            WHERE user_id = %s
            ORDER BY id DESC
            """,
            (user_id,)
        )

        records = cursor.fetchall()

        return render_template(
            "my_records.html",
            records=records
        )

    except mysql.connector.Error as error:

        print(
            "My records database error:",
            error
        )

        return "Unable to load your records."

    finally:

        if cursor:

            cursor.close()

        if connection:

            connection.close()

# ==================================================
# ADMIN LOGIN
# ==================================================

@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form["username"].strip()
        password = request.form["password"]

        # ------------------------------------------
        # ADMIN CREDENTIALS
        # ------------------------------------------

        if (
            username == "admin"
            and password == "admin123"
        ):

            session.clear()

            session["admin_logged_in"] = True

            return redirect(
                url_for("admin_dashboard")
            )

        else:

            return render_template(
                "admin_login.html",
                error="Invalid username or password"
            )

    return render_template(
        "admin_login.html"
    )


# ==================================================
# ADMIN DASHBOARD
# ==================================================

@app.route("/admin")
def admin_dashboard():

    if not session.get("admin_logged_in"):

        return redirect(
            url_for("login")
        )

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        cursor = connection.cursor()

        # ------------------------------------------
        # ALL PATIENT RECORDS
        # ------------------------------------------

        cursor.execute(
            """
            SELECT
                id,
                age,
                sex,
                cp,
                trestbps,
                chol,
                fbs,
                restecg,
                thalach,
                exang,
                oldpeak,
                slope,
                ca,
                thal,
                prediction,
                created_at
            FROM patient_records
            ORDER BY id ASC
            """
        )

        patients = cursor.fetchall()

        # ------------------------------------------
        # TOTAL PATIENTS
        # ------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM patient_records
            """
        )

        total_patients = cursor.fetchone()[0]

        # ------------------------------------------
        # POSITIVE CASES
        # ------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM patient_records
            WHERE prediction = 'Positive'
            """
        )

        positive_cases = cursor.fetchone()[0]

        # ------------------------------------------
        # NEGATIVE CASES
        # ------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM patient_records
            WHERE prediction = 'Negative'
            """
        )

        negative_cases = cursor.fetchone()[0]

        # ------------------------------------------
        # PREDICTION DATA
        # ------------------------------------------

        cursor.execute(
            """
            SELECT
                prediction,
                COUNT(*)
            FROM patient_records
            GROUP BY prediction
            """
        )

        prediction_data = cursor.fetchall()

        # ------------------------------------------
        # AGE DATA
        # ------------------------------------------

        cursor.execute(
            """
            SELECT
                age,
                COUNT(*)
            FROM patient_records
            GROUP BY age
            ORDER BY age
            """
        )

        age_data = cursor.fetchall()

        return render_template(
            "admin_dashboard.html",
            patients=patients,
            total_patients=total_patients,
            positive_cases=positive_cases,
            negative_cases=negative_cases,
            prediction_data=prediction_data,
            age_data=age_data
        )

    except mysql.connector.Error as error:

        print(
            "Admin dashboard error:",
            error
        )

        return "Unable to load admin dashboard."

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==================================================
# STATISTICS
# ==================================================

@app.route("/statistics")
def statistics():

    if not session.get("admin_logged_in"):

        return redirect(
            url_for("login")
        )

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        cursor = connection.cursor()

        # ------------------------------------------
        # TOTAL PATIENTS
        # ------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM patient_records
            """
        )

        total_patients = cursor.fetchone()[0]

        # ------------------------------------------
        # POSITIVE CASES
        # ------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM patient_records
            WHERE prediction = 'Positive'
            """
        )

        positive_cases = cursor.fetchone()[0]

        # ------------------------------------------
        # NEGATIVE CASES
        # ------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM patient_records
            WHERE prediction = 'Negative'
            """
        )

        negative_cases = cursor.fetchone()[0]

        # ------------------------------------------
        # PERCENTAGES
        # ------------------------------------------

        if total_patients > 0:

            positive_percentage = round(
                (positive_cases / total_patients) * 100,
                2
            )

            negative_percentage = round(
                (negative_cases / total_patients) * 100,
                2
            )

        else:

            positive_percentage = 0
            negative_percentage = 0

        # ------------------------------------------
        # AVERAGE AGE
        # ------------------------------------------

        cursor.execute(
            """
            SELECT AVG(age)
            FROM patient_records
            """
        )

        average_age_result = cursor.fetchone()[0]

        if average_age_result is not None:

            average_age = round(
                average_age_result,
                2
            )

        else:

            average_age = 0

        # ------------------------------------------
        # MAXIMUM AGE
        # ------------------------------------------

        cursor.execute(
            """
            SELECT MAX(age)
            FROM patient_records
            """
        )

        maximum_age = cursor.fetchone()[0]

        if maximum_age is None:
            maximum_age = 0

        # ------------------------------------------
        # MINIMUM AGE
        # ------------------------------------------

        cursor.execute(
            """
            SELECT MIN(age)
            FROM patient_records
            """
        )

        minimum_age = cursor.fetchone()[0]

        if minimum_age is None:
            minimum_age = 0

        return render_template(
            "statistics.html",
            total_patients=total_patients,
            positive_cases=positive_cases,
            negative_cases=negative_cases,
            positive_percentage=positive_percentage,
            negative_percentage=negative_percentage,
            average_age=average_age,
            maximum_age=maximum_age,
            minimum_age=minimum_age
        )

    except mysql.connector.Error as error:

        print(
            "Statistics error:",
            error
        )

        return "Unable to load statistics."

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==================================================
# CHARTS
# ==================================================

@app.route("/charts")
def charts():

    if not session.get("admin_logged_in"):

        return redirect(
            url_for("login")
        )

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        cursor = connection.cursor()

        # ------------------------------------------
        # PREDICTION DATA
        # ------------------------------------------

        cursor.execute(
            """
            SELECT
                prediction,
                COUNT(*)
            FROM patient_records
            GROUP BY prediction
            """
        )

        prediction_data = cursor.fetchall()

        # ------------------------------------------
        # AGE DATA
        # ------------------------------------------

        cursor.execute(
            """
            SELECT
                age,
                COUNT(*)
            FROM patient_records
            GROUP BY age
            ORDER BY age ASC
            """
        )

        age_data = cursor.fetchall()

        # ------------------------------------------
        # SEX DATA
        # ------------------------------------------

        cursor.execute(
            """
            SELECT
                sex,
                COUNT(*)
            FROM patient_records
            GROUP BY sex
            ORDER BY sex
            """
        )

        sex_data = cursor.fetchall()

        # ------------------------------------------
        # CHEST PAIN DATA
        # ------------------------------------------

        cursor.execute(
            """
            SELECT
                cp,
                COUNT(*)
            FROM patient_records
            GROUP BY cp
            ORDER BY cp
            """
        )

        cp_data = cursor.fetchall()

        return render_template(
            "charts.html",
            prediction_data=prediction_data,
            age_data=age_data,
            sex_data=sex_data,
            cp_data=cp_data
        )

    except mysql.connector.Error as error:

        print(
            "Charts error:",
            error
        )

        return "Unable to load charts."

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==================================================
# ADMIN ABSTRACT
# ==================================================

@app.route('/abstract')
def abstract():
    return render_template('abstract.html')


# ==================================================
# ADMIN FUTURE TOPICS
# ==================================================

@app.route('/future')
def future():
    return render_template('future.html')


# ==================================================
# UPLOAD DATASET
# ==================================================

@app.route(
    "/admin/upload-dataset",
    methods=["GET", "POST"]
)
def upload_dataset():

    if not session.get("admin_logged_in"):

        return redirect(
            url_for("login")
        )

    if request.method == "POST":

        if "dataset" not in request.files:

            return render_template(
                "upload_dataset.html",
                error="Please select a dataset."
            )

        file = request.files["dataset"]

        if file.filename == "":

            return render_template(
                "upload_dataset.html",
                error="Please select a dataset."
            )

        # ------------------------------------------
        # ALLOW CSV FILES
        # ------------------------------------------

        if not file.filename.lower().endswith(".csv"):

            return render_template(
                "upload_dataset.html",
                error="Only CSV files are allowed."
            )

        # ------------------------------------------
        # CREATE DATASET FOLDER
        # ------------------------------------------

        dataset_folder = "dataset"

        os.makedirs(
            dataset_folder,
            exist_ok=True
        )

        filepath = os.path.join(
            dataset_folder,
            file.filename
        )

        file.save(filepath)

        print(
            "Dataset uploaded:",
            filepath
        )

        return render_template(
            "upload_dataset.html",
            success="Dataset uploaded successfully."
        )

    return render_template(
        "upload_dataset.html"
    )


# ==================================================
# TRAIN MODEL PAGE
# ==================================================

@app.route("/admin/train")
def train_model_page():

    if not session.get("admin_logged_in"):

        return redirect(
            url_for("login")
        )

    return render_template(
        "train.html"
    )


# ==================================================
# TEST MODEL PAGE
# ==================================================

@app.route("/admin/test")
def test_model_page():

    if not session.get("admin_logged_in"):

        return redirect(
            url_for("login")
        )

    return render_template(
        "test.html"
    )



# ==================================================
# PATIENT PREDICTION PAGE
# ==================================================

@app.route("/predictor")
def predictor():

    # ------------------------------------------
    # USER MUST LOGIN FIRST
    # ------------------------------------------

    if not session.get("user_logged_in"):

        return redirect(
            url_for("patient_login")
        )

    return render_template(
        "predictor.html"
    )
    # ------------------------------------------
    # USER MUST LOGIN FIRST
    # ------------------------------------------

    if not session.get("user_logged_in"):

        return redirect(
            url_for("patient_login")
        )

    return render_template(
        "predictor.html"
    )


# ==================================================
# PREDICTION + MYSQL STORAGE
# ==================================================
# ==================================================
# PREDICTION + MYSQL STORAGE
# ==================================================

# ==================================================
# PREDICT HEART DISEASE
# ==================================================

@app.route("/predict", methods=["POST"])
def predict():

    # ------------------------------------------
    # USER LOGIN CHECK
    # ------------------------------------------

    if not session.get("user_logged_in"):
        return redirect(
            url_for("patient_login")
        )

    # ------------------------------------------
    # GET USER ID
    # ------------------------------------------

    user_id = session.get("user_id")

    if not user_id:
        return redirect(
            url_for("patient_login")
        )

    connection = None
    cursor = None

    try:

        # ------------------------------------------
        # GET DATA FROM FORM
        # ------------------------------------------

        age = float(
            request.form["age"]
        )

        sex = float(
            request.form["sex"]
        )

        cp = float(
            request.form["cp"]
        )

        trestbps = float(
            request.form["trestbps"]
        )

        chol = float(
            request.form["chol"]
        )

        fbs = float(
            request.form["fbs"]
        )

        restecg = float(
            request.form["restecg"]
        )

        thalach = float(
            request.form["thalach"]
        )

        exang = float(
            request.form["exang"]
        )

        oldpeak = float(
            request.form["oldpeak"]
        )

        slope = float(
            request.form["slope"]
        )

        ca = float(
            request.form["ca"]
        )

        thal = float(
            request.form["thal"]
        )


        # ------------------------------------------
        # TERMINAL DISPLAY
        # ------------------------------------------

        print("\n================================")
        print("PATIENT DATA RECEIVED")
        print("================================")

        print("User ID:", user_id)
        print("Username:", session.get("username"))
        print("Age:", age)
        print("Sex:", sex)
        print("Chest Pain:", cp)
        print("Blood Pressure:", trestbps)
        print("Cholesterol:", chol)
        print("Fasting Blood Sugar:", fbs)
        print("Rest ECG:", restecg)
        print("Maximum Heart Rate:", thalach)
        print("Exercise Angina:", exang)
        print("Oldpeak:", oldpeak)
        print("Slope:", slope)
        print("CA:", ca)
        print("Thal:", thal)


        # ------------------------------------------
        # CREATE DATAFRAME
        # ------------------------------------------

        input_data = pd.DataFrame(
            [[
                age,
                sex,
                cp,
                trestbps,
                chol,
                fbs,
                restecg,
                thalach,
                exang,
                oldpeak,
                slope,
                ca,
                thal
            ]],
            columns=model.feature_names_in_
        )


        # ------------------------------------------
        # MODEL PREDICTION
        # ------------------------------------------

        prediction = model.predict(
            input_data
        )

        prediction_value = int(
            prediction[0]
        )

        print("\nPrediction:", prediction_value)


        # ------------------------------------------
        # CONVERT RESULT
        # ------------------------------------------

        if prediction_value == 1:

            result = "Positive"

        else:

            result = "Negative"


        print("Result:", result)


        # ------------------------------------------
        # MYSQL CONNECTION
        # ------------------------------------------

        print("Trying to connect to MySQL...")

        connection = get_db_connection()

        print(
            "MySQL connected:",
            connection.is_connected()
        )

        cursor = connection.cursor()


        # ------------------------------------------
        # SAVE RECORD WITH USER ID
        # ------------------------------------------

        query = """
        INSERT INTO patient_records
        (
            user_id,
            age,
            sex,
            cp,
            trestbps,
            chol,
            fbs,
            restecg,
            thalach,
            exang,
            oldpeak,
            slope,
            ca,
            thal,
            prediction
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
        """


        values = (
            user_id,
            age,
            sex,
            cp,
            trestbps,
            chol,
            fbs,
            restecg,
            thalach,
            exang,
            oldpeak,
            slope,
            ca,
            thal,
            result
        )


        print("\nValues being inserted:")
        print(values)


        # ------------------------------------------
        # INSERT INTO MYSQL
        # ------------------------------------------

        cursor.execute(
            query,
            values
        )

        connection.commit()


        # ------------------------------------------
        # CONFIRM
        # ------------------------------------------

        print(
            "Rows inserted:",
            cursor.rowcount
        )

        print(
            "Patient data saved successfully!"
        )


        # ------------------------------------------
        # SHOW RESULT PAGE
        # ------------------------------------------

        return render_template(
            "result.html",
            prediction=result
        )


    # ------------------------------------------
    # VALUE ERROR
    # ------------------------------------------

    except ValueError as error:

        print(
            "Value Error:",
            error
        )

        return (
            "Please enter valid values for all fields."
        )


    # ------------------------------------------
    # MYSQL ERROR
    # ------------------------------------------

    except mysql.connector.Error as error:

        print(
            "================================"
        )

        print(
            "MYSQL ERROR"
        )

        print(
            "================================"
        )

        print(
            "Error type:",
            type(error).__name__
        )

        print(
            "Error number:",
            error.errno
        )

        print(
            "Error message:",
            error.msg
        )

        print(
            "================================"
        )

        return (
            "Database connection or saving error. "
            "Check the terminal."
        )


    # ------------------------------------------
    # OTHER ERROR
    # ------------------------------------------

    except Exception as error:

        print(
            "================================"
        )

        print(
            "PREDICTION ERROR"
        )

        print(
            "================================"
        )

        print(
            "Error:",
            error
        )

        print(
            "================================"
        )

        return (
            "Something went wrong while processing "
            "your prediction. Check the terminal."
        )


    # ------------------------------------------
    # CLOSE MYSQL
    # ------------------------------------------

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==================================================
# ADMIN PATIENT RECORDS
# ==================================================

@app.route("/patient-records")
def patient_records():

    # ------------------------------------------
    # ADMIN LOGIN PROTECTION
    # ------------------------------------------

    if not session.get("admin_logged_in"):
        return redirect(
            url_for("login")
        )

    connection = None
    cursor = None

    try:

        # ------------------------------------------
        # CONNECT TO DATABASE
        # ------------------------------------------

        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        # ------------------------------------------
        # GET ALL PATIENT RECORDS
        # ------------------------------------------

        cursor.execute(
            """
            SELECT
                id,
                user_id,
                age,
                sex,
                cp,
                trestbps,
                chol,
                fbs,
                restecg,
                thalach,
                exang,
                oldpeak,
                slope,
                ca,
                thal,
                prediction,
                created_at
            FROM patient_records
            ORDER BY id ASC
            """
        )

        records = cursor.fetchall()

        # ------------------------------------------
        # COUNT ALL RECORDS
        # ------------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM patient_records
            """
        )

        result = cursor.fetchone()

        total_records = result["total"]

        print(
            "ADMIN - TOTAL RECORDS:",
            total_records
        )

        # ------------------------------------------
        # SHOW PATIENT RECORDS
        # ------------------------------------------

        return render_template(
            "patient_records.html",
            records=records,
            total_records=total_records
        )

    except mysql.connector.Error as error:

        print(
            "Patient records database error:",
            error
        )

        return "Unable to load patient records."

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==================================================
# LOGOUT
# ==================================================

@app.route("/logout")
def logout():

    # ------------------------------------------
    # CLEAR EVERYTHING
    # ------------------------------------------

    session.clear()

    return redirect(
        url_for("home")
    )
@app.after_request
def add_no_cache(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# ==================================================
# RUN FLASK APPLICATION
# ==================================================

if __name__ == "__main__":

 app.run(host="localhost", port=5000, debug=True)