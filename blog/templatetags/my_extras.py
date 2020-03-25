"""
    name='my_extras',
    project='Ideabank'
    date='12/30/2019',
    author='Oshodi Kolapo',
"""
import re
from django import template
import random

register = template.Library()


@register.filter(name='calculate_time_read')
def calculate_time_read(content):
    """Based on research, the average adult reads 200-250 words in one minute. Hence we divide the post by 200"""
    content = str(content)
    count2 = len(content.split())
    # count_of_words = len(re.findall('\w+', content))
    minutes = int(count2 / 200)
    if minutes == 0:
        return 1
    else:
        return minutes


@register.filter(name='rand_css')
def rand_css(content):
    class_list = ['secondary', 'success', 'danger', 'warning', 'info', 'dark', 'primary']
    return random.choice(class_list)
