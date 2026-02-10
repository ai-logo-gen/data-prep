# difficulties in amazing_logo_v4061622
# value: "Simple elegant logo for Play, ""Altar Boyz"", pop Advertising People band boy Sunrise Silhouette technology, Theater, successful vibe, minimalist, thought-provoking, abstract, recognizable, relatable, sharp, vector art, even edges"
# amazing_logo_v4151950
# value: "Simple elegant logo for WFDF, World Ultimate and Guts Championships 2008, Athletes, grey purple disc black person transparent running orange action sans pink blue layers sport colour serif catching green red rainbow frisbee yellow jumping ultimate player throwing, Sports, successful vibe, minimalist, thought-provoking, abstract, recognizable, relatable, sharp, vector art, even edges"

from text import parse_text  # Adjust import based on your actual module structure

def test_parse_text():
    """Test parse_text function with multiple examples."""
    
    # List of test examples
    test_examples = [
        'Simple elegant logo for Play, ""Altar Boyz"", pop Advertising People band boy Sunrise Silhouette technology, Theater, successful vibe, minimalist, thought-provoking, abstract, recognizable, relatable, sharp, vector art, even edges',
        'Simple elegant logo for WFDF, World Ultimate and Guts Championships 2008, Athletes, grey purple disc black person transparent running orange action sans pink blue layers sport colour serif catching green red rainbow frisbee yellow jumping ultimate player throwing, Sports, successful vibe, minimalist, thought-provoking, abstract, recognizable, relatable, sharp, vector art, even edges'
    ]
    
    for i, example_text in enumerate(test_examples, 1):
        print(f"\n--- Test Example {i} ---")
        print(f"Input text: {example_text}")
        print(f"Input length: {len(example_text)}")
        
        try:
            result = parse_text(example_text) # company, description, category, tags
            print(f"Parse result: {result}")
            print(f"Result type: {type(result)}")
            
        except Exception as e:
            print(f"Error occurred: {e}")
            print(f"Error type: {type(e)}")

if __name__ == "__main__":
    test_parse_text()