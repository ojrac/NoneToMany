from django import template

from base import matched_inclusion_tag

register = template.Library()

@matched_inclusion_tag(register, 'form.html')
def form(type='', id='', action='', method='', header='', description='', width="480", enctype='application/x-www-form-urlencoded'):
    return {
            'type': type,
            'id': id,
            'action': action,
            'method': method,
            'description': description,
            'width': width,
            'enctype': enctype,
        }

