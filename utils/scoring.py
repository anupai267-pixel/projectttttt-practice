def calculate_sustainability_score(category, condition):
    base_scores = {
        'Electronics': 70,
        'Books': 85,
        'Clothing': 80,
        'Furniture': 90,
        'Accessories': 75,
        'Sports': 75,
        'Other': 65
    }
    
    condition_multipliers = {
        'Used': 1.0,
        'Fair': 0.95,
        'Good': 0.90,
        'Like New': 0.85,
        'New': 0.70
    }
    
    cat_score = base_scores.get(category, 70)
    cond_mult = condition_multipliers.get(condition, 0.85)
    
    # Calculate score weighted towards reusable lifecycle saving
    raw_score = cat_score * cond_mult
    final_score = min(98, max(45, int(raw_score)))
    return final_score