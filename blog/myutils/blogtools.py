import re


def calculate_time_read(content):
    """Based on research, the average adult reads 200-250 words in one minute. Hence we divide the post by 200"""
    content = str(content)
    count_of_words = len(re.findall('[a-zA-Z_]+', content))
    return int(count_of_words / 200)
