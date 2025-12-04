# train_xgboost.py
"""
Simple training pipeline using NSL-KDD dataset.
Assumptions: You have downloaded NSL-KDD and placed CSVs in ../../data/NSL-KDD/
This script performs minimal preprocessing and trains XGBoost.
"""
import pandas as pd
import numpy as np
from pandas.api.types import is_numeric_dtype
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from xgboost import XGBClassifier
from sklearn.metrics import classification_report
import joblib
import os

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "NSL-KDD"))

def find_data_file(data_dir, base_name):
    for ext in ('.csv', '.txt'):
        p = os.path.join(data_dir, base_name + ext)
        if os.path.exists(p):
            return p
    raise FileNotFoundError(f"Could not find {base_name}.csv or {base_name}.txt in {data_dir}")

TRAIN_FILE = find_data_file(DATA_DIR, "KDDTrain+")
TEST_FILE = find_data_file(DATA_DIR, "KDDTest+")


def load_nslkdd(path):
    # NSL-KDD has 42 columns; if you have raw files, adapt accordingly
    cols = ["duration","protocol_type","service","flag","src_bytes","dst_bytes",
            "land","wrong_fragment","urgent","hot","num_failed_logins","logged_in",
            "num_compromised","root_shell","su_attempted","num_root","num_file_creations",
            "num_shells","num_access_files","num_outbound_cmds","is_host_login","is_guest_login",
            "count","srv_count","serror_rate","srv_serror_rate","rerror_rate","srv_rerror_rate",
            "same_srv_rate","diff_srv_rate","srv_diff_host_rate","dst_host_count","dst_host_srv_count",
            "dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate",
            "dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate",
            "dst_host_rerror_rate","dst_host_srv_rerror_rate","label"]
    # NSL-KDD files are comma-separated; use header=None and skip initial spaces
    df = pd.read_csv(path, names=cols, sep=',', header=None, engine='python', skipinitialspace=True)
    return df


def preprocess(df):
    # target mapping: NSL labels many attack types. For demo create grouped labels
    # If labels are numeric codes (some NSL variants), use them directly
    if is_numeric_dtype(df['label']):
        y_raw = df['label'].astype(int)
        y = y_raw
    else:
        def map_label(l):
            # normalize label strings (strip whitespace, quotes, trailing dot) and lowercase
            s = str(l).strip().strip('"').strip("'")
            if s.endswith('.'):
                s = s[:-1]
            s = s.lower()
            if s == "normal":
                return "normal"
            # grouping: do coarse mapping if needed
            if s in ["back","land","neptune","pod","smurf","teardrop","udpstorm","mailbomb"]:
                return "dos"
            if s in ["satan","ipsweep","nmap","portsweep","mscan","saint"]:
                return "probe"
            if s in ["ftp_write","guess_passwd","imap","multihop","phf","spy","warezclient","warezmaster"]:
                return "r2l"
            if s in ["buffer_overflow","loadmodule","perl","rootkit","httptunnel","ps","xterm"]:
                return "u2r"
            return "other"
        df["label2"] = df["label"].apply(map_label)
        y = df["label2"]

    # Keep all columns except the raw label; convert categorical features to numeric
    X = df.drop(columns=["label", "label2"], errors='ignore').copy()

    # Categorical columns in NSL-KDD: protocol_type, service, flag
    cat_cols = [c for c in ["protocol_type", "service", "flag"] if c in X.columns]
    if len(cat_cols) > 0:
        # Ensure categorical columns are strings and one-hot encode them
        for c in cat_cols:
            X[c] = X[c].astype(str)
        X = pd.get_dummies(X, columns=cat_cols, drop_first=True)

    # Fill missing and coerce any remaining non-numeric values to numeric (NaN -> 0)
    X = X.fillna(0)
    X = X.apply(pd.to_numeric, errors='coerce').fillna(0)

    # scale numeric
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)

    # encode labels
    le = LabelEncoder()
    y_enc = le.fit_transform(y)
    # return feature column names so test data can be reindexed
    feature_columns = list(X.columns)
    return Xs, y_enc, scaler, le, feature_columns


def preprocess_with_reference(df, feature_columns, scaler=None):
    """Prepare dataframe using a reference list of feature columns (from training).
    This ensures test data has same columns (one-hot columns) as train.
    If `scaler` is provided, it will be used to transform; otherwise a new scaler is fit.
    Returns Xs, y_enc (if label present), scaler_used
    """
    # target mapping same as preprocess
    def map_label(l):
        s = str(l).strip().strip('"').strip("'")
        if s.endswith('.'):
            s = s[:-1]
        s = s.lower()
        if s == "normal":
            return "normal"
        if s in ["back","land","neptune","pod","smurf","teardrop","udpstorm","mailbomb"]:
            return "dos"
        if s in ["satan","ipsweep","nmap","portsweep","mscan","saint"]:
            return "probe"
        if s in ["ftp_write","guess_passwd","imap","multihop","phf","spy","warezclient","warezmaster"]:
            return "r2l"
        if s in ["buffer_overflow","loadmodule","perl","rootkit","httptunnel","ps","xterm"]:
            return "u2r"
        return "other"

    if 'label' in df.columns:
        if is_numeric_dtype(df['label']):
            y = df['label'].astype(int)
        else:
            df['label2'] = df['label'].apply(map_label)
            y = df['label2']
    else:
        y = None

    X = df.drop(columns=['label','label2'], errors='ignore').copy()
    cat_cols = [c for c in ['protocol_type','service','flag'] if c in X.columns]
    if len(cat_cols) > 0:
        for c in cat_cols:
            X[c] = X[c].astype(str)
        X = pd.get_dummies(X, columns=cat_cols, drop_first=True)

    X = X.fillna(0)
    X = X.apply(pd.to_numeric, errors='coerce').fillna(0)

    # Reindex to feature_columns, filling missing with 0
    X = X.reindex(columns=feature_columns, fill_value=0)

    if scaler is None:
        scaler = StandardScaler()
        Xs = scaler.fit_transform(X)
    else:
        Xs = scaler.transform(X)

    if y is not None:
        le = LabelEncoder()
        y_enc = le.fit_transform(y)
    else:
        y_enc = None
    return Xs, y_enc, scaler


def main():
    print("Loading dataset...")
    train = load_nslkdd(TRAIN_FILE)
    test = load_nslkdd(TEST_FILE)
    # debug: show raw label varieties present in the loaded files
    try:
        print("Train label sample unique:", train['label'].unique()[:20])
        print(train['label'].value_counts().head(10))
    except Exception as e:
        print("Could not inspect raw labels:", e)
    X_train, y_train, scaler, le, feature_columns = preprocess(train)
    X_test, y_test, _ = preprocess_with_reference(test, feature_columns, scaler=scaler)  # reuse scaler from train

    # If preprocessing produced a single class only, abort with helpful message
    if len(np.unique(y_train)) < 2:
        raise RuntimeError("Training labels contain a single class after mapping. Check your NSL-KDD files and label column formatting (e.g., trailing '.' characters).")

    print("Training XGBoost...")
    # Ensure labels are integer numpy array
    y_train = np.array(y_train)
    # Print debug info about labels/features
    print(f"X_train.shape={getattr(X_train,'shape',None)}, y_train.shape={getattr(y_train,'shape',None)}")
    print(f"y_train dtype={y_train.dtype}, unique={np.unique(y_train)[:10]}")
    # Ensure integer labels for classifier
    try:
        y_train = y_train.astype(int)
    except Exception:
        print("Warning: could not cast y_train to int; using original dtype")

    # Choose objective based on number of classes
    n_classes = len(np.unique(y_train))
    print(f"Detected {n_classes} classes")
    if n_classes <= 2:
        objective = 'binary:logistic'
        model = XGBClassifier(objective=objective, eval_metric='logloss', n_jobs=4)
    else:
        objective = 'multi:softprob'
        model = XGBClassifier(objective=objective, num_class=n_classes, eval_metric='mlogloss', n_jobs=4)

    try:
        model.fit(X_train, y_train)
    except Exception as e:
        print("Model fit failed. Debug info:")
        print(f"model params: objective={model.get_params().get('objective')}, num_class={model.get_params().get('num_class')}")
        print(f"y_train unique values: {np.unique(y_train)}")
        raise

    preds = model.predict(X_test)
    print(classification_report(y_test, preds, target_names=le.classes_))

    os.makedirs(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "model")), exist_ok=True)
    joblib.dump(model, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "model", "xgb_model.joblib")))
    joblib.dump(le, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "model", "xgb_model.le.joblib")))
    joblib.dump(scaler, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "model", "xgb_scaler.joblib")))
    print("Saved model to ../model/xgb_model.joblib")

if __name__ == "__main__":
    main()
