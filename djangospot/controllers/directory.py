import logging

from pylons import request, response, session, tmpl_context as c, url, app_globals as g
from pylons.decorators import validate
from pylons.controllers.util import abort, redirect

from djangospot.lib.base import BaseController, render

log = logging.getLogger(__name__)

class DirectoryController(BaseController):

    def index(self):
        c.projects = [(k, g.redis.hgetall('project.%s' % k)) for k in g.redis.sort('projects',  0, 10)]
        return render('directory/index.html')

    def details(self):
        c.project_id = request.params['project_id']
        c.project = g.redis.hgetall('project.%s' % c.project_id)
        if not c.project:
            abort(404, '404 Not Found')
        return render('directory/details.html')

    def add(self):
        c.form_result = {}
        c.form_errors = {}
        if request.params:
            schema = ProjectForm()
            try:
                c.form_result = schema.to_python(request.params)
            except formencode.validators.Invalid, error:
                c.form_result = error.value
                c.form_errors = error.error_dict or {}
            else:
                idx = g.redis.incr('next.project.id')
                g.redis.rpush('projects', idx)
                g.redis.hset('project.%s' % idx, 'name', c.form_result['name'])
                g.redis.hset('project.%s' % idx, 'url', c.form_result['url'])
        return render('directory/add.html')

import formencode

class ProjectForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    name = formencode.validators.String(not_empty=True)
    url = formencode.validators.URL(not_empty=True)