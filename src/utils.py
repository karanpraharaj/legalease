import re

def parse_console_log(text):
    # Pattern to match the custom timestamp and text
    pattern = r"\[(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})\]\s*(.*)"
    matches = re.finditer(pattern, text, re.MULTILINE)

    entries = []
    for match in matches:
        start_time = match.group(1)
        end_time = match.group(2)
        subtitle_text = match.group(3)
        entries.append((start_time, end_time, subtitle_text))
        
    # Merge the subtitle text into a single string
    combined_text = ""
    for entry in entries:
        combined_text += entry[2] + " "

    return combined_text
