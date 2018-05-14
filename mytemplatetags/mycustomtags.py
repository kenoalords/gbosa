from django import template

register = template.Library()
register.filter('is_flagged', is_flagged)

def is_flagged(value, args):
    if value == True:
        return 'is-flagged'
