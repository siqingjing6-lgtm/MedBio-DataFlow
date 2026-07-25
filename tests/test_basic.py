from src.omics_prep import calculate_tissue_requirements

def test_tissue_qc():
    result = calculate_tissue_requirements(10, 10, 100)
    assert result["qc_passed_for_rnaseq"] is True
    
    result_fail = calculate_tissue_requirements(5, 2, 50)
    assert result_fail["qc_passed_for_rnaseq"] is False
