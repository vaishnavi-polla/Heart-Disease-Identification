# Heart Disease Identification Using Machine Learning

## 📌 Project Overview

Heart Disease Identification is a web-based application developed using Python and Flask. The system uses a trained machine learning classification model to identify whether a patient is likely to have heart disease based on selected health-related input parameters.

The application provides a simple interface for users to enter patient information, obtain a prediction, and view their previous prediction records. An administrator can also securely access patient records and view statistical information through the admin dashboard.

## 🎯 Objectives

- To develop a web-based heart disease identification system.
- To use machine learning for classification of heart disease cases.
- To provide a simple and user-friendly interface.
- To store patient prediction records using MySQL.
- To provide an admin dashboard for viewing patient records and statistics.

## 🛠️ Technologies Used

- Python
- Flask
- HTML
- CSS
- JavaScript
- Pandas
- NumPy
- Scikit-learn
- Joblib
- MySQL
- MySQL Workbench

## 🤖 Machine Learning Models

The following classification algorithms were evaluated:

| Model | Accuracy |
|---|---:|
| Logistic Regression | 91.67% |
| K-Nearest Neighbors (KNN) | 90.00% |
| Random Forest | 88.33% |
| Decision Tree | 78.33% |

Logistic Regression achieved the highest accuracy in the project and was selected as the final model.

## 📊 Dataset

The project uses the **Cleveland Heart Disease Dataset**, a commonly used dataset for developing and evaluating machine learning models for heart disease classification.

The dataset contains patient health-related attributes that are used as input features for prediction.

### Dataset Features

The main attributes used in the project include:

* **Age** – Age of the patient
* **Sex** – Gender of the patient
* **Chest Pain Type** – Type of chest pain experienced
* **Resting Blood Pressure** – Resting blood pressure of the patient
* **Cholesterol** – Serum cholesterol level
* **Fasting Blood Sugar** – Fasting blood sugar measurement
* **Resting ECG** – Resting electrocardiographic results
* **Maximum Heart Rate** – Maximum heart rate achieved
* **Exercise-Induced Angina** – Whether exercise induces angina
* **Oldpeak** – ST depression induced by exercise
* **Slope** – Slope of the peak exercise ST segment
* **CA** – Number of major vessels
* **Thal** – Thalassemia-related test result

### Data Preparation

Before training the machine learning models, the dataset was cleaned and prepared for analysis. After data cleaning, **297 records** were used for developing and evaluating the classification models.

The prepared data was then used to train and compare multiple classification algorithms, with **Logistic Regression** achieving the highest accuracy of **91.67%**.
### Target Variable

The target variable represents the presence or absence of heart disease in a patient.

* **0 – No Heart Disease:** The patient is classified as not having heart disease.
* **1 – Heart Disease:** The patient is classified as having heart disease.

The machine learning models use the patient health attributes as input features and predict the corresponding target value. The final Logistic Regression model is used by the application to generate the prediction result.

## 🧪 Training and Testing

The cleaned dataset was divided into **training and testing sets** using an **80:20 split**.

* **80% of the data** was used for training the machine learning models.
* **20% of the data** was used for testing and evaluating the models.
* **Stratified splitting** was used to maintain the distribution of the target classes.
* A fixed `random_state` was used to ensure reproducible results.

The classification models were trained using the training data and evaluated on the testing data. Their accuracy scores were compared to identify the best-performing model.

Among the evaluated models, **Logistic Regression achieved the highest test accuracy of 91.67%** and was selected as the final model for the application.

The trained model was saved using **Joblib** and integrated with the Flask application for making predictions on new patient input.

## 🔐 Main Features

### User Module

- User login
- Patient information entry
- Heart disease prediction
- Display of prediction result
- Viewing previous patient records
- Logout

### Admin Module

- Admin login
- Admin dashboard
- View patient records
- View statistical information
- View prediction-related charts
- Logout

## 🗄️ Database

MySQL is used to store patient prediction records.

Database:

text
heartcare

## Website Preview

### Home Page
![Home Page](docs/images/home.png)

### Login Page
![Login Page](docs/images/login.png)

### Prediction Page
![Prediction Page](docs/images/predication1.png)
### Result Page
![Result Page](docs/images/result.png)