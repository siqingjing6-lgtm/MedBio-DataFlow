"""
Clinical Statistics & Biomarker Screening Module
Automates logistic regression and LASSO feature selection for clinical datasets.
"""
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression, LassoCV
from sklearn.preprocessing import StandardScaler
from typing import List, Dict, Any

class BioFeatureSelector:
    def __init__(self, data_path: str):
        self.data = pd.read_csv(data_path)
        self.scaler = StandardScaler()

    def run_lasso_screening(self, target_col: str, feature_cols: List[str]) -> Dict[str, float]:
        """
        Runs LASSO regression with cross-validation to select high-value clinical features.
        """
        X = self.data[feature_cols].fillna(self.data[feature_cols].median())
        y = self.data[target_col]
        
        X_scaled = self.scaler.fit_transform(X)
        
        # Lasso regression with 5-fold cross validation for clinical screening
        lasso = LassoCV(cv=5, random_state=42, max_iter=10000).fit(X_scaled, y)
        
        selected_features = {}
        for feature, coef in zip(feature_cols, lasso.coef_):
            if abs(coef) > 0.0:
                selected_features[feature] = round(float(coef), 4)
                
        return selected_features

    def build_logistic_model(self, target_col: str, selected_features: List[str]) -> Dict[str, Any]:
        """
        Builds a multivariable logistic regression model and returns odds ratios (OR).
        """
        X = self.data[selected_features].fillna(self.data[selected_features].median())
        y = self.data[target_col]
        
        clf = LogisticRegression(penalty='l2', solver='lbfgs', max_iter=1000)
        clf.fit(X, y)
        
        odds_ratios = np.exp(clf.coef_[0])
        
        results = {
            "intercept": round(float(clf.intercept_[0]), 4),
            "odds_ratios": {feat: round(float(or_val), 4) for feat, or_val in zip(selected_features, odds_ratios)},
            "accuracy": round(float(clf.score(X, y)), 4)
        }
        return results
