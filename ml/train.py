import pandas as pd
from sklearn.model_selection import train_test_split
# from sklearn.pipeline import Pipeline
# from sklearn.compose import ColumnTransformer
# from sklearn.impute import SimpleImputer
# from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBRegressor
import pickle

# Constants
DATA_FILE = 'properties.csv'
TARGET_COLUMN = 'price'
REMOVE_COLUMN = ['id', 'subproperty_type', 'region', 'province', 'locality', 'equipped_kitchen', 'fl_furnished', 'fl_open_fire', 'fl_terrace', 'fl_garden', 'fl_swimming_pool', 'fl_floodzone', 'state_building', 'primary_energy_consumption_sqm', 'heating_type', 'fl_double_glazing', 'cadastral_income', 'latitude', 'longitude']


def load_data(file_path):
    """Load data from CSV file."""
    df = pd.read_csv(file_path)
    return df

def preprocess_data(df):
    """Preprocess data: handle missing values, encode categorical variables."""
    X = df.drop(columns=[TARGET_COLUMN] + REMOVE_COLUMN)
    y = df[TARGET_COLUMN]

    # Separate numeric and categorical columns
    numeric_cols = X.select_dtypes(include=['float64']).columns
    categorical_cols = X.select_dtypes(exclude=['float64']).columns

    # Fill missing values in numeric columns with median
    X[numeric_cols] = X[numeric_cols].fillna(X[numeric_cols].median())

    # One-hot encode categorical columns
    X = pd.get_dummies(X, columns=categorical_cols, drop_first=True)

    return X, y

def train_model(X_train, y_train):
    """Train XGBoost model."""
    xgb_model = XGBRegressor(
        n_estimators=200,        # Increase number of trees
        max_depth=8,             # Increase maximum tree depth
        learning_rate=0.1       # Reduce learning rate
        # subsample=0.8,           # Use subsample of training instances
        # colsample_bytree     # Use subsample of features
        # reg_lambda=1,            # L2 regularization
        # reg_alpha=0.5            # L1 regularization
    )
    xgb_model.fit(X_train, y_train)
    return xgb_model

def save_model(model, file_path):
    """Save the trained model."""
    print("Saving trained model to:", file_path)  # for debugging
    with open(file_path, 'wb') as f:
        pickle.dump(model, f)


def main():
    # Load data
    df = load_data(DATA_FILE)

      # Preprocess data
    X, y = preprocess_data(df)

    # Split data into train and test sets
    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=67)

    # Train model
    model = train_model(X_train, y_train)

    # Save model
    save_model(model, 'trained_model.pkl')
    print("Trained model saved successfully!")

if __name__ == "__main__":
    main()
