import os
import cherrypy
import json
import subprocess
import shlex

import splunk, splunk.util
import splunk.appserver.mrsparkle.controllers as controllers
from splunk.appserver.mrsparkle.lib.decorators import expose_page
from splunk.appserver.mrsparkle.lib.routes import route
from splunk.appserver.mrsparkle.lib import jsonresponse, util, cached

class TerminalController(controllers.BaseController):

    def render_template(self, template_path, template_args = {}):
        template_args['appList'] = self.get_app_manifest()
        return super(TerminalController, self).render_template(template_path, template_args)
    def get_app_manifest(self):
        output = cached.getEntities('apps/local', search=['disabled=false','visible=true'], count=-1)
        return output 
        
    @expose_page(must_login=True, methods=['GET'])
    @route('/', methods=['GET'])
    def view(self, **kwargs):
        
        app = cherrypy.request.path_info.split('/')[3]

        return self.render_template('/%s:/templates/terminal.html' % app, dict(app=app))

    
    @expose_page(must_login=True, methods=['POST'])
    @route('/', methods=['POST'])
    def process(self, **kwargs):
        command = kwargs.get('command')
        splitCommand = shlex.split(command) if os.name == 'posix' else command.split(' ')
       
        if not command:
            error = "No command"
            return self.render_json(dict(success=False, payload=error)) 
        
        try:
            output = subprocess.check_output(splitCommand, shell=True)
           
            if output:
				payload = output
				return self.render_json(dict(success=True, payload=payload))
            else:
				return self.render_json(dict(success=False, payload='Command failed.'))

        except Exception, e:
            return self.render_json(dict(success=False, payload=str(e)))