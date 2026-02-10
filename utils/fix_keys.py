import re

# Read the file
with open('consolidation_maps.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace pattern: 'word word word': [ with 'word_word_word': [
# This regex finds quoted strings with spaces followed by ': [' and replaces all spaces with underscores
pattern = r"'([^']*\s[^']*)': \["

def replace_spaces_in_key(match):
    key_with_spaces = match.group(1)
    key_with_underscores = key_with_spaces.replace(' ', '_')
    return f"'{key_with_underscores}': ["

# Apply the replacement
new_content = re.sub(pattern, replace_spaces_in_key, content)

# Write back to file
with open('consolidation_maps.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Replacement completed!')
