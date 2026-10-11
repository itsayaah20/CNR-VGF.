import pandas as pd
import os
import joblib

from sklearn.model_selection import train_test_split

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix
)


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


RF_MODEL = os.path.join(
    BASE_DIR,
    "backend",
    "ml",
    "models",
    "rf_model.pkl"
)


XGB_MODEL = os.path.join(
    BASE_DIR,
    "backend",
    "ml",
    "models",
    "xgb_model.pkl"
)



df = pd.read_csv(DATASET)



X = df.drop(
    "Risk_Label",
    axis=1
)


y = df["Risk_Label"]



X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)



models = {

    "Random Forest":
    joblib.load(RF_MODEL),


    "XGBoost":
    joblib.load(XGB_MODEL)

}



results = []



for name, model in models.items():


    prediction = model.predict(
        X_test
    )


    probability = model.predict_proba(
        X_test
    )[:,1]


    results.append({

        "Model": name,

        "Accuracy":
        accuracy_score(
            y_test,
            prediction
        ),


        "Precision":
        precision_score(
            y_test,
            prediction
        ),


        "Recall":
        recall_score(
            y_test,
            prediction
        ),


        "F1_score":
        f1_score(
            y_test,
            prediction
        ),


        "ROC_AUC":
        roc_auc_score(
            y_test,
            probability
        )

    })


    print("\n====================")
    print(name)
    print("====================")


    print(
        confusion_matrix(
            y_test,
            prediction
        )
    )



result = pd.DataFrame(
    results
)



OUTPUT = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "model_comparison.csv"
)


result.to_csv(
    OUTPUT,
    index=False
)


print("\nModel comparison saved:")
print(OUTPUT)


print(result)