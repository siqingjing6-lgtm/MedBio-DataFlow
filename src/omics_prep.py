"""
Omics & Tissue Sampling Calculation Module
Assists researchers in automating sample prep calculations for RNA sequencing and pathology.
"""
from typing import Dict

def calculate_tissue_requirements(section_thickness_um: float, total_sections: int, area_sq_mm: float) -> Dict[str, float]:
    """
    Calculates estimated tissue volume and validates sufficiency for bulk RNA-seq.
    Recommended: minimum 10 sections of 10um thickness with >= 100 mm^2 total surface area.
    """
    total_volume_cubic_mm = (section_thickness_um / 1000.0) * area_sq_mm * total_sections
    
    # Validation threshold for standard bulk RNA extraction
    is_sufficient = total_sections >= 10 and area_sq_mm >= 100.0
    
    return {
        "total_volume_mm3": round(total_volume_cubic_mm, 3),
        "estimated_nucleic_yield_index": round(total_volume_cubic_mm * 1.5, 2), # Empirical yield index
        "qc_passed_for_rnaseq": is_sufficient
    }
