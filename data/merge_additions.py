import json
import os

OUTPUT_DIR = "digital-organism/data"

def create_additions_only():
    print("Merging new additions only...")
    files_to_merge = [
        os.path.join(OUTPUT_DIR, "pivot.jsonl"),
        os.path.join(OUTPUT_DIR, "system_instruction.jsonl"),
        os.path.join(OUTPUT_DIR, "refusal.jsonl")
    ]
    
    final_data = []
    for filepath in files_to_merge:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                for line in f:
                    final_data.append(json.loads(line))
            print(f"Loaded {filepath}")
        else:
            print(f"Warning: {filepath} not found, skipping.")
            
    # Shuffle
    import random
    random.shuffle(final_data)
    
    final_path = os.path.join(OUTPUT_DIR, "new_additions_only.jsonl")
    with open(final_path, 'w') as f:
        for entry in final_data:
            json.dump(entry, f)
            f.write('\n')
            
    print(f"Created new_additions_only.jsonl with {len(final_data)} examples.")

if __name__ == "__main__":
    create_additions_only()
