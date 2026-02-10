import pandas as pd
import re

def parse_text(text):
    """Parse the text column to extract company, description, category, and tags"""
    if pd.isna(text) or not isinstance(text, str):
        return None, None, None, []
    # remove more then 2 whitespaces
    text = ' '.join(text.split())  # Normalize whitespace
    # remove special chars except [&,-]
    text = re.sub(r'[^\w\s&,\-]', '', text)
    
    text = text.replace(', &', ' &')  
    text = text.replace(', .jpg,', ',,')  
    text = text.replace(', Inc.', ' Inc.') 
    # Split by comma
    parts = [part.strip() for part in text.split(',')]
    
    # Extract components
    company = parts[0] if len(parts) > 0 else None
    description = parts[1] if len(parts) > 1 else None
    category = parts[2] if len(parts) > 2 else None
    tags = parts[3:] if len(parts) > 3 else []

    # if category has more words then description do a switch -> value of category goes to description but only if category has more then 2 words (except & or 'and')
    if description and category:
        # Count words excluding '&' and 'and'
        desc_words = [word for word in description.split() if word.lower() not in ['&', 'and']]
        cat_words = [word for word in category.split() if word.lower() not in ['&', 'and']]
        
        if len(cat_words) > len(desc_words) and len(cat_words) > 2:
            description, category = category, description
    
    # Clean up empty values
    tags = [tag for tag in tags if tag and tag.strip()]
    
    # Filter tags: if word length > 3, move to description
    filtered_tags = []
    tags_to_add_to_description = []
    
    for tag in tags:
        word_count = len(tag.split())
        # Filter out tags with characters other than word chars, hyphens, underscores
        if not re.match(r'^[\w\-_\s]+$', tag):
            continue
        
        if word_count > 3:
            tags_to_add_to_description.append(tag)
        else:
            filtered_tags.append(tag)
    
    # Add long tags to description with comma separation
    if tags_to_add_to_description:
        if description:
            description = description + ", " + ", ".join(tags_to_add_to_description)
        else:
            description = ", ".join(tags_to_add_to_description)
    
    tags = filtered_tags

    # Filter out tags with invalid characters
    tags = [tag for tag in tags if re.match(r'^[\w\-_\s]+$', tag)]
    
    return company, description, category, tags


def normalize_single_tag(tag):
    """Normalisiert einen einzelnen Tag für besseren Vergleich"""
    if not tag:
        return ''
    
    # Convert to string and lowercase
    normalized = str(tag).lower().strip()
    
    # Remove special characters (keep only word chars and spaces)
    normalized = re.sub(r'[^\w\s]', '', normalized)
    
    # Reduce multiple spaces to single space
    normalized = re.sub(r'\s+', ' ', normalized)
    
    # Replace spaces with underscores
    normalized = normalized.replace(' ', '_')
    
    return normalized


def normalize_tags(tags):
    """Normalisiert namen für besseren Vergleich"""
    if not tags:
        return ''
    
    tagsList = str(tags).strip().split(',')
    tagsList = [normalize_single_tag(tag) for tag in tagsList]
    # Filter out empty tags
    tagsList = [tag for tag in tagsList if tag]
    return ','.join(tagsList)