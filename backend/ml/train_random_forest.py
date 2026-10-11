import pandas as pd
import os
import joblib


from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report



BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)



DATASET = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "ml_training_dataset.csv"
)


MODEL_PATH = os.path.join(
    BASE_DIR,
    "backend",
    "ml",
    "models",
    "rf_model.pkl"
)



df = pd.read_csv(
    DATASET
)



X = df.drop(
    "Risk_Label",
    axis=1
)


y = df[
    "Risk_Label"
]



X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,
    test_size=0.2,
    random_state=42

)



model = RandomForestClassifier(

    n_estimators=200,

    max_depth=10,

    random_state=42

)



print("Training Random Forest...")


model.fit(

    X_train,

    y_train

)



prediction = model.predict(
    X_test
)



print(
    "Accuracy:",
    accuracy_score(
        y_test,
        prediction
    )
)


print(
    classification_report(
        y_test,
        prediction
    )
)



# Feature importance

importance = pd.DataFrame({

    "Feature":
    X.columns,

    "Importance":
    model.feature_importances_

})


print(
    importance.sort_values(
        by="Importance",
        ascending=False
    )
)



os.makedirs(

    os.path.dirname(MODEL_PATH),

    exist_ok=True

)



joblib.dump(

    model,

    MODEL_PATH

)



print(
    "Random Forest saved"
)

print(
    MODEL_PATH
)