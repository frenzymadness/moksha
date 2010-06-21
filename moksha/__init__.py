# This file is part of Moksha.
# Copyright (C) 2008-2010  Red Hat, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__import__('pkg_resources').declare_namespace(__name__)

from paste.registry import StackedObjectProxy

# The central feed cache, used by the Feed widget.
feed_cache = None

# A dict-like persistent backing store
feed_storage = None

# All loaded moksha applications
_apps = None

# All loaded ToscaWidgets
_widgets = None

# All WSGI applications
wsgiapps = None

# All loaded moksha menus
menus = None

# Per-request topic callbacks registered by rendered live widgets
livewidgets = StackedObjectProxy(name="livewidgets")

def get_widget(name):
    """ Get a widget instance by name """
    if _widgets:
        return _widgets[name]['widget']

def get_widgets():
    """ Return a dictionary of all widgets """
    from pkg_resources import iter_entry_points
    return _widgets or [widget.load() for widget in iter_entry_points('moksha.widget')]

def get_app(name):
    """ Get an app controller by name """
    return _apps[name]['controller']

def shutdown():
    """ Called when Moksha shuts down """
    try:
        if feed_storage:
            feed_storage.close()
    except AttributeError:
        pass

def global_resources():
    """ Returns a rendered Moksha Global Resource Widget.

    This widget contains all of the resources and widgets on the
    `moksha.global` entry-point.  To use it, simply do this at the bottom of
    your master template::

        ${tmpl_context.moksha_global_resources()}

    """
    import tg
    from moksha.api.widgets.global_resources import global_resources as globs
    if tg.config.default_renderer == 'genshi':
        # There's Got To Be A Better Way!
        from genshi import unescape, Markup
        return Markup(unescape(Markup(globs)))
    elif tg.config.default_renderer == 'mako':
        return globs()
    else:
        # If this gets called, and explodes, then you need to add support
        # for your templating engine here.
        return globs()
