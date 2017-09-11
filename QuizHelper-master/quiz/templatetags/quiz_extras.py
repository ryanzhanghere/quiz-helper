from django import template

register = template.Library()


@register.filter(name='get')
def get_item(dictionary, key):
    """
    given a dictionary and a key, return corresponding value.
    :param dictionary:
    :param key:
    :return: the value associated with the key
    """
    return dictionary.get(key)
