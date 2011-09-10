import os

from mako.template import Template
from mako.lookup import TemplateLookup

templating_path = os.path.join(os.path.dirname(__file__), 'templates')
lookup = TemplateLookup([templating_path])

def render(template_name, context=None):
    template = lookup.get_template(template_name)
    context = context  or {}
    return template.render_unicode(**context)
