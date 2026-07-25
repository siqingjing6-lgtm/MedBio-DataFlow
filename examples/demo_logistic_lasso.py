import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.clinical_stats import BioFeatureSelector
from src.omics_prep import calculate_tissue_requirements

def main():
    print("=== MedBio-DataFlow Automated Pipeline Demo ===")
    
    # 1. Omics Sample QC Check
    print("\n--- 1. RNA-Seq Tissue Sampling QC ---")
    qc_result = calculate_tissue_requirements(section_thickness_um=10, total_sections=12, area_sq_mm=110.0)
    print(f"Sampling QC Result: {qc_result}")

    # 2. LASSO Feature Selection
    print("\n--- 2. Clinical Feature Selection (LASSO) ---")
    data_path = os.path.join(os.path.dirname(__file__), "sample_data.csv")
    selector = BioFeatureSelector(data_path)
    
    features = ["age", "tumor_size", "biomarker_A", "biomarker_B", "biomarker_C"]
    target = "lymph_node_meta"
    
    selected_features = selector.run_lasso_screening(target_col=target, feature_cols=features)
    print(f"Selected High-Value Features: {selected_features}")
    
    # 3. Logistic Regression Modeling
    if selected_features:
        print("\n--- 3. Multivariable Logistic Regression Model ---")
        model_results = selector.build_logistic_model(target_col=target, selected_features=list(selected_features.keys()))
        print(f"Model Odds Ratios: {model_results['odds_ratios']}")
        print(f"Model Accuracy: {model_results['accuracy']}")

if __name__ == "__main__":
    main()
