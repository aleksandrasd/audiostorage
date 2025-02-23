def convert_seconds_to_hms(seconds):
    # Calculate hours, minutes, and seconds
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    # Return the formatted string
    return f"{hours:02}:{minutes:02}:{seconds:02}"