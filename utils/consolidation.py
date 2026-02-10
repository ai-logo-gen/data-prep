import pandas as pd
import re
from collections import defaultdict
import random
from consolidation_maps import get_consolidated_map
from text import normalize_single_tag

# Get the merged consolidation map
consolidation_map = get_consolidated_map()

def normalize_category(category):
    """Normalisiert Kategorienamen für besseren Vergleich"""
    return re.sub(r'[^\w\s]', '', category.lower().strip()).replace('_', ' ')

def consolidate_categories(df):
    """Konsolidiert ähnliche Kategorien basierend auf der consolidation_map
    
    Args:
        df: DataFrame mit einer 'category' Spalte und optional einer 'tags' Spalte
    
    Returns:
        df: DataFrame mit ersetzten Kategorien basierend auf der consolidation_map
            Wenn eine 'tags' Spalte vorhanden ist, wird der konsolidierte Kategorie-Key
            zu den Tags hinzugefügt (falls er nicht bereits vorhanden ist und nicht 'unclassified' ist)
        unmatched_categories: Liste der Kategorien, die nicht gemappt werden konnten
        consolidation_mapping: Dictionary mit {consolidated_category: {'count': int, 'original_categories': [list]}}
    """
    # Create reverse mapping from original categories to consolidated categories
    category_to_main = {}
    for main_cat, variations in consolidation_map.items():
        for variation in variations:
            category_to_main[variation] = main_cat
    
    # Track unmatched categories and consolidation mapping
    unmatched_categories = []
    consolidation_mapping = defaultdict(lambda: {'count': 0, 'original_categories': []})
    
    def map_category(category):
        """Map a single category to its consolidated form"""
        if pd.isna(category):
            return category
        
        original_category = str(category)
        
        # Normalize the category
        normalized = normalize_category(original_category)
        
        # Debug: randomly enable debug output for categories
        # debug_category = random.random() < 0.10  # 10% chance to enable debug output
        # if debug_category:
        #     print(f"DEBUG: Processing '{original_category}' -> normalized: '{normalized}'")
        
        # 1. Exact match
        if normalized in category_to_main:
            consolidated = category_to_main[normalized]
            # if debug_category:
            #     print(f"DEBUG: Exact match found: '{normalized}' -> '{consolidated}'")
            consolidation_mapping[consolidated]['count'] += 1
            if original_category not in consolidation_mapping[consolidated]['original_categories']:
                consolidation_mapping[consolidated]['original_categories'].append(original_category)
            return consolidated
        
        # 2. Partial string matching
        best_match = None
        max_overlap = 0
        
        for norm_cat, main_cat in category_to_main.items():
            overlap = 0
            norm_words = set(normalized.split())
            cat_words = set(norm_cat.split())
            
            # Only proceed if there are actual words to compare
            if not norm_words or not cat_words:
                continue
            
            # Common words (must have at least one common word)
            common_words = norm_words.intersection(cat_words)
            if common_words:
                # Calculate Jaccard similarity (intersection over union)
                union_words = norm_words.union(cat_words)
                overlap = len(common_words) / len(union_words)
            
            # Substring matching (more strict - must be significant portion)
            if len(norm_cat) >= 3 and len(normalized) >= 3:  # Minimum length check
                if (norm_cat in normalized and len(norm_cat) / len(normalized) > 0.7) or \
                   (normalized in norm_cat and len(normalized) / len(norm_cat) > 0.7):
                    overlap = max(overlap, 0.9)  # High confidence for good substring matches
            
            # Only accept matches with significant overlap and avoid weak matches
            if overlap > max_overlap and overlap > 0.5:  # Increased threshold from 0.3 to 0.5
                max_overlap = overlap
                best_match = main_cat
        
        if best_match:
            # if debug_category:
            #     print(f"DEBUG: Partial match found: '{normalized}' -> '{best_match}' (overlap: {max_overlap:.3f})")
            consolidation_mapping[best_match]['count'] += 1
            if original_category not in consolidation_mapping[best_match]['original_categories']:
                consolidation_mapping[best_match]['original_categories'].append(original_category)
            return best_match
        
        # If no match found, track as unmatched and keep the original category
        # if debug_category:
        #     print(f"DEBUG: No match found for '{normalized}', keeping original")
        if original_category not in unmatched_categories:
            unmatched_categories.append(original_category)
        consolidation_mapping[original_category]['count'] += 1
        if original_category not in consolidation_mapping[original_category]['original_categories']:
            consolidation_mapping[original_category]['original_categories'].append(original_category)
        return original_category
    
    # Create a copy of the DataFrame and apply the mapping
    result_df = df.copy()
    
    # Check if tags column exists
    has_tags = 'tags' in result_df.columns
    
    # Apply category mapping and update tags if present
    def process_row(row):
        original_category = row['category']
        consolidated_category = map_category(original_category)
        
        # Update the category
        row['category'] = consolidated_category
        
        # Add consolidated category to tags only if the category actually changed
        if (has_tags and 
            consolidated_category != 'unclassified' and 
            normalize_category(str(consolidated_category)) != normalize_category(str(original_category))):
            
            current_tags = row.get('tags', '')
            if pd.isna(current_tags):
                current_tags = ''
            
            # Parse existing tags
            existing_tags = [tag.strip() for tag in str(current_tags).split(',') if tag.strip()]
            
            # Add consolidated category if not already present
            if consolidated_category not in existing_tags:
                existing_tags.append(normalize_single_tag(original_category))
                row['tags'] = ', '.join(existing_tags)

                # Random debug output (1% chance)
                if random.random() < 0.01:
                    print(f"DEBUG TAG ADD: '{original_category}' -> '{consolidated_category}' | Tags: {existing_tags}")
            
        return row
    
    # Apply the processing to each row
    result_df = result_df.apply(process_row, axis=1)
    
    return result_df, unmatched_categories, dict(consolidation_mapping)

def analyze_categories(df):
    """Analysiert die ursprünglichen Kategorien um Muster zu erkennen"""
    print("Top 50 ursprüngliche Kategorien:")
    print(df.head(50).to_string(index=False))
    
    # Kategorien nach Häufigkeit der Wörter
    word_freq = defaultdict(int)
    for category in df['category']:
        words = normalize_category(category).split()
        for word in words:
            if len(word) > 2:  # Ignoriere sehr kurze Wörter
                word_freq[word] += 1
    
    print(f"\nHäufigste Wörter in Kategorienamen:")
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    for word, freq in sorted_words[:30]:
        print(f"  {word}: {freq}")

def map_category_to_main(category):
    """Map a single category (original or consolidated) to one of 10 main categories."""
    if pd.isna(category):
        return 'other'

    cat = normalize_category(str(category))

    grouped_map = {
        'real_estate_construction': [
            'real_estate_residential', 'real_estate_commercial', 'real_estate_development',
            'construction_general', 'construction_home', 'construction_specialty', 'construction_materials'
        ],
        'food_beverage': [
            'restaurant_dining', 'cafe_coffee', 'bar_nightlife', 'brewery_alcohol', 'catering_events',
            'food_production', 'grocery_retail', 'beverage_general'
        ],
        'tech': [
            'software_development', 'web_digital', 'it_services', 'telecommunications', 'fintech_crypto',
            'data_analytics', 'tech_hardware'
        ],
        'health': [
            'healthcare_general', 'dental_services', 'medical_specialty', 'wellness_fitness',
            'mental_health', 'veterinary'
        ],
        'education': [
            'education_k12', 'higher_education', 'training_development', 'educational_services'
        ],
        'retail_hospitality': [
            'retail_general', 'ecommerce_online', 'hotels_lodging', 'hospitality_services',
            'fashion_apparel', 'home_goods'
        ],
        'professional_financial_legal': [
            'financial_services', 'accounting_tax', 'insurance_services', 'legal_services',
            'consulting_business', 'marketing_advertising'
        ],
        'manufacturing_transport': [
            'manufacturing_general', 'automotive_transport', 'vehicle_sales', 'transportation_services',
            'import_export', 'chemical_materials', 'energy_utilities'
        ],
        'entertainment_sports_media': [
            'music_industry', 'film_video', 'arts_culture', 'entertainment_venues', 'sports_recreation',
            'gaming_entertainment', 'media_publishing'
        ],
        'other': ['unclassified']
    }

    explicit_map = {}
    for main_cat, keys in grouped_map.items():
        for key in keys:
            explicit_map[normalize_category(key)] = main_cat

    if cat in explicit_map:
        return explicit_map[cat]

    keyword_buckets = {
        'real_estate_construction': ['real', 'estate', 'property', 'construction', 'builder', 'developer', 'contractor', 'housing', 'residential', 'commercial'],
        'food_beverage': ['restaurant', 'cafe', 'coffee', 'bar', 'beer', 'brewery', 'food', 'grocery', 'catering', 'beverage', 'deli', 'bakery'],
        'tech': ['software', 'web', 'digital', 'it', 'tech', 'data', 'analytics', 'cloud', 'saas', 'blockchain', 'crypto', 'ai', 'machine', 'telecom', 'telecommunications'],
        'health': ['health', 'medical', 'clinic', 'dental', 'vet', 'veterinary', 'wellness', 'fitness', 'therapy', 'hospital', 'med'],
        'education': ['school', 'education', 'academy', 'university', 'college', 'training', 'tutoring', 'learning'],
        'retail_hospitality': ['retail', 'shop', 'store', 'boutique', 'hotel', 'lodging', 'hospitality', 'fashion', 'ecommerce', 'home'],
        'professional_financial_legal': ['finance', 'financial', 'bank', 'accounting', 'insurance', 'legal', 'law', 'consult', 'marketing', 'hr', 'human resources'],
        'manufacturing_transport': ['manufactur', 'factory', 'industrial', 'vehicle', 'automotive', 'transport', 'logistic', 'shipping', 'energy', 'chemical'],
        'entertainment_sports_media': ['music', 'film', 'movie', 'media', 'entertain', 'sport', 'gaming', 'theatre', 'arts'],
        'other': ['community', 'religion', 'government', 'nonprofit', 'charity', 'unclass', 'other', 'misc', 'service']
    }

    for main_cat, keywords in keyword_buckets.items():
        for kw in keywords:
            if kw in cat:
                return main_cat

    return 'other'


def add_main_category_column(df, source_col='category', target_col='category_main'):
    """Add a column to the DataFrame with the main consolidated category."""
    result = df.copy()
    if source_col not in result.columns:
        raise ValueError(f"Source column '{source_col}' not found in dataframe")

    result[target_col] = result[source_col].apply(map_category_to_main)
    return result

