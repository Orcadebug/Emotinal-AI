import json
import os
# Requires: pip install datasets
from datasets import load_dataset

def prepare_data():
    print("Downloading Datasets...")
    try:
        # Load DailyDialog (using agentlans version which is standard parquet)
        print("Loading DailyDialog...")
        daily_dialog = load_dataset("agentlans/li2017dailydialog")
        
        # Load Cornell Movie Dialogs (using mylesmharrison version which is parquet)
        print("Loading Cornell Movie Dialogs...")
        cornell_dialog = load_dataset("mylesmharrison/cornell-movie-dialog")
    except Exception as e:
        print(f"Error loading datasets: {e}")
        print("Please ensure you have 'datasets' installed: pip install datasets")
        return

    output_file = "merged_training_data.jsonl"
    
    print("Processing Datasets...")
    with open(output_file, 'w') as f:
        # 1. Process DailyDialog (Casual, daily life)
        print("Processing DailyDialog...")
        for i, item in enumerate(daily_dialog['train']):
            if i >= 5000: 
                break
            
            # agentlans/li2017dailydialog uses 'conversations' list with 'from' and 'value'
            if 'conversations' in item:
                conversation = item['conversations']
                # Skip system prompt if present
                start_idx = 0
                if conversation and conversation[0].get('from') == 'system':
                    start_idx = 1
                
                for j in range(start_idx, len(conversation) - 1):
                    # Ensure alternating human/gpt or just take adjacent turns
                    msg1 = conversation[j]
                    msg2 = conversation[j+1]
                    
                    # Simple extraction
                    if 'value' in msg1 and 'value' in msg2:
                        # Filter out very short turns
                        if len(msg1['value'].split()) < 2 or len(msg2['value'].split()) < 2:
                            continue
                            
                        entry = {
                            "prompt": msg1['value'],
                            "completion": msg2['value']
                        }
                        f.write(json.dumps(entry) + "\n")

        # 2. Process Cornell Movie Dialogs
        print("Processing Cornell Movie Dialogs...")
        # Heuristic: Iterate and pair adjacent utterances if they belong to the same conversation/movie
        # The HF dataset structure can be variable, so we try to adapt.
        
        previous_utterance = None
        previous_movie_id = None
        
        # We'll limit to 5000 pairs to keep it fast
        cornell_count = 0
        
        for i, item in enumerate(cornell_dialog['train']):
            if cornell_count >= 5000:
                break
                
            current_text = None
            current_movie_id = None
            
            # Attempt to extract text and ID based on common structures
            if 'utterance' in item and 'text' in item['utterance']:
                current_text = item['utterance']['text']
            elif 'text' in item:
                current_text = item['text']
                
            if 'movieID' in item:
                current_movie_id = item['movieID']
            
            # If we found text, try to pair it
            if current_text:
                # If we have a previous utterance from the same movie (and ideally same conversation)
                # We assume adjacent lines in the dataset are often conversational if from same movie
                if previous_utterance and previous_movie_id == current_movie_id:
                    entry = {
                        "prompt": previous_utterance,
                        "completion": current_text
                    }
                    f.write(json.dumps(entry) + "\n")
                    cornell_count += 1
                    
                    # Reset to avoid chaining too much (A->B, B->C is okay, but let's be simple)
                    # Actually, A->B, B->C is good for flow.
                    
                previous_utterance = current_text
                previous_movie_id = current_movie_id
            else:
                # If structure doesn't match, reset
                previous_utterance = None
        
    print("Injecting rude/casual examples from style.jsonl...")
    if os.path.exists("style.jsonl"):
        with open("style.jsonl", 'r') as style_f:
            style_data = style_f.read()
            with open(output_file, 'a') as out_f:
                out_f.write(style_data)
                if not style_data.endswith('\n'):
                    out_f.write('\n')
    
    print(f"Data preparation complete. Saved to {output_file}")
    print("NOTE: Cornell Movie Dialogs support is added but requires the dataset to be loadable via 'datasets'.")

if __name__ == "__main__":
    prepare_data()
