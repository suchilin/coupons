# coding=utf-8
from __future__ import print_function, unicode_literals, with_statement, division

from os import path, system, listdir, sys, mkdir
import re
from django.apps import apps
#from django.conf import settings
# VIEW CONSTS
from django.forms import model_to_dict



view_templates = {
'list':"""class List%(model)sView(ListView):
    model = %(model)s
    template_name = '%(lower_model)s/list.html'""",
'details':"""class Detail%(model)sView(UpdateView):
    model = %(model)s
    form_class = %(model)sForm
    template_name = '%(lower_model)s/details.html'""",
'create':"""class Create%(model)sView(CreateView):
    model = %(model)s
    form_class = %(model)sForm
    template_name = '%(lower_model)s/create.html'""",
'update':"""class Update%(model)sView(UpdateView):
    model = %(model)s
    form_class = %(model)sForm
    template_name = '%(lower_model)s/update.html'""",
'delete':"""class Delete%(model)sView(DeleteView):
    model = %(model)s
    success_url = reverse_lazy('%(lower_model)s_list')
    template_name='%(lower_model)s/delete.html'"""
}

# MODELS CONSTS

MODEL_TEMPLATE = """

class %s(models.Model):
    %s
    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse_lazy('%s_list')

    class Meta:
        ordering = ['-id']"""

IMPORT_MODEL_TEMPLATE = """from %(app)s.models import %(model)s"""

CHARFIELD_TEMPLATE = """%(name)s = models.CharField(max_length=%(length)s, null=%(null)s, blank=%(null)s)"""

TEXTFIELD_TEMPLATE = """%(name)s = models.TextField(null=%(null)s, blank=%(null)s)"""

INTEGERFIELD_TEMPLATE = """%(name)s = models.IntegerField(null=%(null)s, default=%(default)s)"""

DECIMALFIELD_TEMPLATE = """%(name)s = models.DecimalField(max_digits=%(digits)s, decimal_places=%(places)s, null=%(null)s, default=%(default)s)"""

DATETIMEFIELD_TEMPLATE = """%(name)s = models.DateTimeField(null=%(null)s, default=%(default)s)"""

FOREIGNFIELD_TEMPLATE = """%(name)s = models.ForeignKey(%(foreign)s, null=%(null)s, blank=%(null)s)"""

templates_list = {
'list':"""{%% extends "base.html" %%}
{%% load i18n %%}

{%% block page-title %%}%(title)s - {{ %(model)s }} {%% endblock %%}

{%% block content %%}
<h1>{{ %(model)s }}</h1>
<a href="{%% url '%(model)s_add' %%}">{%%trans 'Add' %%} {{ %(model)s }}</a>
<ul>
    {%% for %(model)s in object_list %%}
        <li><a href="{%% url '%(model)s_details' %(model)s.id %%}">{{ %(model)s }}</a>  - <a href="{%% url '%(model)s_update' %(model)s.id %%}">{%% trans 'Update'%%}</a> - <a href="{%% url '%(model)s_delete' %(model)s.id %%}">{%% trans 'Delete' %%}</a></li>
    {%% endfor %%}
</ul>
{%% endblock %%}
""",
'details': """{%% extends "base.html" %%}
{%% load i18n %%}

{%% block page-title %%}%(title)s - {{ %(model)s }} {%% endblock %%}

{%% block content %%}
<h1>{{ %(model)s }}</h1>
%(fields)s
{%% endblock %%}
""",
'delete':"""{%% extends "base.html" %%}
{%% load i18n %%}

{%% block page-title %%} %(model)s - {{ %(model)s }}{%% endblock %%}

{%% block content %%}
<form action="" method="post">{%% csrf_token %%}
    <p>{%% trans 'Are you sure you want to delete' %%} "{{ %(model)s }}"?</p>
    <input type="submit" value="Confirm" />
</form>
{%% endblock %%}
""",
'create':"""{%% extends "base.html" %%}
{%% load i18n %%}

{%% block page-title %%} {%%trans 'Create a' %%} %(model)s{%% endblock %%}

{%% block content %%}
<form action="" method="post">{%% csrf_token %%}
    {{ form.as_p }}
    <input type='submit' value='Save'/>
</form>
{%% endblock %%}
""",
'update':"""{%% extends "base.html" %%}
{%% load i18n %%}

{%% block page-title %%} {%%trans 'Create a' %%} %(model)s - {{ %(model)s }}{%% endblock %%}

{%% block content %%}
<form action="" method="post">{%% csrf_token %%}
    {{ form.as_p }}
    <input type='submit' value='Save'/>
</form>
{%% endblock %%}
"""
}

URL_CONTENT = """from django.urls import path
from %(app)s import views


urlpatterns = [

        path('%(lower_model)s/', views.List%(model)sView.as_view(), name='%(lower_model)s_list'),
        path('%(lower_model)s/<int:pk>', views.Detail%(model)sView.as_view(), name='%(lower_model)s_details'),
        path('%(lower_model)s/add', views.Create%(model)sView.as_view(), name='%(lower_model)s_add'),
        path('%(lower_model)s/update/<int:pk>', views.Update%(model)sView.as_view(), name='%(lower_model)s_update'),
        path('%(lower_model)s/delete/<int:pk>', views.Delete%(model)sView.as_view(), name='%(lower_model)s_delete'),
    ]
"""

URL_EXISTS_CONTENT = """
        path('%(lower_model)s/', views.List%(model)sView.as_view(), name='%(lower_model)s_list'),
        path('%(lower_model)s/<int:pk>', views.Detail%(model)sView.as_view(), name='%(lower_model)s_details'),
        path('%(lower_model)s/add', views.Create%(model)sView.as_view(), name='%(lower_model)s_add'),
        path('%(lower_model)s/update/<int:pk>', views.Update%(model)sView.as_view(), name='%(lower_model)s_update'),
        path('%(lower_model)s/delete/<int:pk>', views.Delete%(model)sView.as_view(), name='%(lower_model)s_delete'),
"""

ADMIN_CONTENT = """admin.site.register(models.%(model)s)
"""

FORM_CONTENT = """
class %(model)sForm(forms.ModelForm):
    class Meta:
        model = models.%(model)s
        exclude = ('id', )
"""

TESTS_CONTENT = """

from %(app)s.models import %(model)s


class %(model)sTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_user')

    def tearDown(self):
        self.user.delete()

    def test_list(self):
        response = self.client.get(reverse('%(lower_model)s-list'))
        self.failUnlessEqual(response.status_code, 200)

    def test_crud(self):
        # Create new instance
        response = self.client.post(reverse('%(lower_model)s-list'), {})
        self.assertContains(response, '"success": true')

        # Read instance
        items = %(model)s.objects.all()
        self.failUnlessEqual(items.count(), 1)
        item = items[0]
        response = self.client.get(reverse('%(lower_model)s-details', kwargs={'id': item.id}))
        self.failUnlessEqual(response.status_code, 200)

        # Update instance
        response = self.client.post(reverse('%(lower_model)s-details', kwargs={'id': item.id}), {})
        self.assertContains(response, '"success": true')

        # Delete instance
        response = self.client.post(reverse('%(lower_model)s-delete', kwargs={'id': item.id}), {})
        self.assertContains(response, '"success": true')
        items = %(model)s.objects.all()
        self.failUnlessEqual(items.count(), 0)

"""


class Scaffold(object):

    def _info(self, msg, indent=0):
        print("{0} {1}".format("\t" * int(indent), msg))

    def __init__(self, app, model, fields):
        self.app = app
        self.model = model
        self.fields = fields
        self.models = apps.all_models[app]
        self.SCAFFOLD_APPS_DIR = './'


    def get_import(self, model):
        for dir in listdir(self.SCAFFOLD_APPS_DIR):
            if path.isdir('{0}{1}'.format(self.SCAFFOLD_APPS_DIR, dir)) \
                    and path.exists('{0}{1}/models.py'.format(self.SCAFFOLD_APPS_DIR, dir)):
                with open('{0}{1}/models.py'.format(self.SCAFFOLD_APPS_DIR, dir), 'r') as fp:
                    # Check if model exists
                    for line in fp.readlines():
                        if 'class {0}(models.Model)'.format(model) in line:
                            # print "Foreign key '%s' was found in app %s..." % (model, dir)
                            return IMPORT_MODEL_TEMPLATE % {'app': dir, 'model': model}
        return None

    def is_imported(self, module_to, model):
        reg_exp = r'^(?=.*%s)(?=.*%s).+$' % (self.app+'.'+module_to, model)
        with open(path.join(self.SCAFFOLD_APPS_DIR, self.app, module_to+'.py'), 'r') as import_file:
            for line in import_file.readlines():
                if re.match(reg_exp, line):
                    return line
        return False

    def add_global_view_imports(self, path):
        # from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
        import_list = list()

        with open(path, 'r') as import_file:
            need_import_generic_views = True
            need_import_urlresolvers = True

            for line in import_file.readlines():
                if 'from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView' in line:
                    need_import_generic_views = False
                if 'from django.urls import reverse_lazy' in line:
                    need_import_urlresolvers = False

            if need_import_generic_views:
                import_list.append(
                    'from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView\n'
                                )
            if need_import_urlresolvers:
                import_list.append(
                    'from django.urls import reverse_lazy'
                        )

        return import_list

    def view_exists(self, view):
        # Check if view already exists
        with open(path.join(self.SCAFFOLD_APPS_DIR, self.app,'views.py'), 'r') as view_file:
            for line in view_file.readlines():
                if 'class {0}('.format(view) in line:
                    return True
        return False


    def create_app(self):
        self._info("    App    ")
        self._info("===========")
        if not path.exists('{0}{1}'.format(self.SCAFFOLD_APPS_DIR, self.app)):
            system('python manage.py startapp {0}'.format(self.app))
            system('mv {0} {1}{2}'.format(self.app, self.SCAFFOLD_APPS_DIR, self.app))
            self._info("create\t{0}{1}".format(self.SCAFFOLD_APPS_DIR, self.app), 1)
        else:
            self._info("exists\t{0}{1}".format(self.SCAFFOLD_APPS_DIR, self.app), 1)

    def create_views(self):
        self._info("   Views   ")
        self._info("===========")
        # Open models.py to read
        view_path = path.join(self.SCAFFOLD_APPS_DIR, self.app, 'views.py')
        # Check if urls.py exists
        if path.exists(view_path):
            self._info('exists\t{0}'.format(view_path), 1)
        else:
            with open(view_path, 'w'):
                self._info('create\t{0}'.format(view_path), 1)

        import_list = list()
        # Add global imports
        import_list.append(''.join(imp for imp in self.add_global_view_imports(view_path)))

        if not path.exists(path.join(self.SCAFFOLD_APPS_DIR, self.app,'forms')):
            system('touch %s/forms.py'%self.app)
        # Add model imports
        models_imports = self.is_imported('models','')
        forms_imports = self.is_imported('forms','')
        if not models_imports:
            models_imports = 'from %s.models import'%self.app
        if not forms_imports:
            forms_imports = 'from %s.forms import'%self.app

        for model in self.models:
            model_name = self.models[model].__name__
            form_name = model_name + 'Form'
            if not self.is_imported('models', model_name):
                if models_imports.endswith('import'):
                    models_imports += ' '+model_name
                else:
                    models_imports += ', ' + model_name
            if not self.is_imported('forms', form_name):
                if forms_imports.endswith('import'):
                    forms_imports += ' '+form_name
                else:
                    forms_imports += ', ' + form_name
        import_list.append(models_imports)
        import_list.append(forms_imports)


        # Check if view already exists
        view_list = []
        for model in self.models:
            model_name = self.models[model].__name__
            view_types = ['list', 'details', 'delete','create','update']
            view_list.append('#===========================%s===========================' % model_name)
            for view in view_types:
                if not self.view_exists("%s%sView"%(view.title(),model_name)):
                    view_list.append(view_templates[view]% {
                    'lower_model': model_name.lower(),
                    'model': model_name,
                })

        # Open views.py to append
        with open(view_path, 'a') as view_file:
            view_file.write(''.join(import_line+'\n' for import_line in import_list))
            for view in view_list:
                if not view.startswith('#'):
                    view_file.write(view+'\n\n\n')
                else:
                    view_file.write(view+'\n')


    def create_templates(self):
        self._info(" Templates ")
        self._info("===========")

        # Check if template dir exists

        if path.exists(path.join(self.SCAFFOLD_APPS_DIR, self.app, 'templates')):
            self._info('exists\t{0}{1}/templates/'.format(self.SCAFFOLD_APPS_DIR, self.app), 1)
        else:
            mkdir("{0}{1}/templates/".format(self.SCAFFOLD_APPS_DIR, self.app))
            self._info('create\t{0}{1}/templates/'.format(self.SCAFFOLD_APPS_DIR, self.app), 1)
        fields_list = '<div>\n'
        # Check if model template dir exists
        for model in self.models:
            model_name = self.models[model].__name__
            template_types = ['list', 'details', 'delete','create', 'update']
            for key, value in model_to_dict(self.models[model]).items():
                if key != 'id':
                    fields_list += '    <div>%s: {{ %s.%s }}</div>\n'%(key.title().replace('_',' '),model,key)
            fields_list += '</div>'
            if path.exists(path.join(self.SCAFFOLD_APPS_DIR, self.app,'templates',model_name.lower())):
                self._info('exists\t{0}{1}/templates/{2}/'.format(self.SCAFFOLD_APPS_DIR, self.app,
                                                                  model_name.lower()), 1)
            else:
                mkdir("{0}{1}/templates/{2}/".format(self.SCAFFOLD_APPS_DIR, self.app,
                                                     model_name.lower()))
                self._info('create\t{0}{1}/templates/{2}/'.format(
                    self.SCAFFOLD_APPS_DIR, self.app, model_name.lower()), 1)

            # Check if list.html exists
            for template_type in template_types:
                if path.exists(path.join(self.SCAFFOLD_APPS_DIR, self.app, 'templates',model_name.lower(), '%s.html'%template_type)):
                    self._info('exists\t{0}{1}/templates/{2}/{3}.html'.format(
                        self.SCAFFOLD_APPS_DIR, self.app, model_name.lower(), template_type), 1)
                else:
                    with open("{0}{1}/templates/{2}/{3}.html".format(self.SCAFFOLD_APPS_DIR, self.app,
                                                                      model_name.lower(), template_type), 'w') as fp:
                        fp.write(templates_list[template_type]% {
                            'model': model_name.lower(),
                            'title': model_name.lower(),
                            'fields':fields_list,
                        })
                    self._info('create\t{0}{1}/templates/{2}/{3}.html'.format(
                        self.SCAFFOLD_APPS_DIR, self.app, model_name.lower(),template_type), 1)
            fields_list = '<div>\n'


    def create_urls(self):
        self._info("    URLs   ")
        self._info("===========")

        # Check if urls.py exists


        for model in self.models:
            new_urls = ''
            model_name = self.models[model].__name__
            if path.exists(path.join(self.SCAFFOLD_APPS_DIR, self.app, 'urls.py')):
                with open(path.join(self.SCAFFOLD_APPS_DIR, self.app, 'urls.py'), 'r') as fp:
                    f_content = fp.read()

                if 'urlpattern' in f_content:
                    with open(path.join(self.SCAFFOLD_APPS_DIR, self.app, 'urls.py'), 'r') as fp:
                        for line in fp.readlines():
                            new_urls += line
                            if 'urlpatterns' in line:
                                        new_urls += URL_EXISTS_CONTENT % {
                                            'app': self.app,
                                            'model': model_name,
                                            'lower_model': model,
                                        }
                    with open(path.join(self.SCAFFOLD_APPS_DIR, self.app, 'urls.py'), 'w') as fp:
                        fp.write(new_urls)
                    self._info('update\t{0}{1}/urls.py'.format(self.SCAFFOLD_APPS_DIR, self.app), 1)
                else:
                    with open(path.join(self.SCAFFOLD_APPS_DIR, self.app, 'urls.py'), 'w') as fp:
                        fp.write(URL_CONTENT % {
                            'app': self.app,
                            'model': self.model,
                            'lower_model': self.model.lower(),
                        })
                    self._info('create\t{0}{1}/urls.py'.format(self.SCAFFOLD_APPS_DIR, self.app), 1)
            else:
                with open(path.join(self.SCAFFOLD_APPS_DIR, self.app, 'urls.py'), 'w') as fp:
                    fp.write(URL_CONTENT % {
                        'app': self.app,
                        'model': self.model,
                        'lower_model': self.model.lower(),
                    })
                self._info('create\t{0}{1}/urls.py'.format(self.SCAFFOLD_APPS_DIR, self.app), 1)

    def create_forms(self):
        self._info("    Forms  ")
        self._info("===========")

        # Check if forms.py exists
        if path.exists(path.join(self.SCAFFOLD_APPS_DIR, self.app, 'forms.py')):
            self._info('exists\t{0}{1}/forms.py'.format(self.SCAFFOLD_APPS_DIR, self.app), 1)
            with open(path.join(self.SCAFFOLD_APPS_DIR, self.app, 'forms.py'), 'r+') as fp:
                content = fp.read()
                fp.seek(0, 0)
                if not 'from django import forms' in content:
                    fp.write("from django import forms".rstrip('\r\n') + '\n')
                if not "from %s import models\n"%self.app in content:
                    fp.write(("from %s import models\n" % self.app).rstrip('\r\n') + '\n')
        else:
            with open(path.join(self.SCAFFOLD_APPS_DIR, self.app, 'forms.py'), 'w') as fp:
                fp.write("from django import forms\n")
                fp.write("from %s import models\n"%self.app)
            self._info('create\t{0}{1}/forms.py'.format(self.SCAFFOLD_APPS_DIR, self.app), 1)

        # Check if form entry already exists
        for model in self.models:
            model_name = self.models[model].__name__
            with open(path.join(self.SCAFFOLD_APPS_DIR, self.app, 'forms.py'), 'r') as fp:
                content = fp.read()
            if "class {0}Form".format(model) in content:
                self._info('exists\t{0}{1}/forms.py\t{2}'.format(
                    self.SCAFFOLD_APPS_DIR, self.app, model), 1)
            else:
                with open(path.join(self.SCAFFOLD_APPS_DIR, self.app, 'forms.py'), 'a') as fp:
                    fp.write(FORM_CONTENT % {'app': self.app, 'model': model_name})
                self._info('added\t{0}{1}/forms.py\t{2}'.format(
                    self.SCAFFOLD_APPS_DIR, self.app, model), 1)


    def create_admin(self):
        self._info("    Admin  ")
        self._info("===========")

        # Check if admin.py exists
        if path.exists(path.join(self.SCAFFOLD_APPS_DIR, self.app, 'admin.py')):
            self._info('exists\t{0}{1}/admin.py'.format(self.SCAFFOLD_APPS_DIR, self.app), 1)
            with open(path.join(self.SCAFFOLD_APPS_DIR, self.app, 'admin.py'), 'r+') as fp:
                content = fp.read()
                fp.seek(0, 0)
                if 'from django.contrib import admin' not in content:
                    fp.write('from django.contrib import admin\n')
                if 'from %s import models'%self.app not in content:
                    fp.write('from %s import models\n'%self.app)
        else:
            with open(path.join(self.SCAFFOLD_APPS_DIR, self.app, 'admin.py'), 'w') as fp:
                fp.write("from django.contrib import admin\n")
            self._info('create\t{0}{1}/admin.py'.format(self.SCAFFOLD_APPS_DIR, self.app), 1)

        # Check if admin entry already exists
        for model in self.models:
            model_name = self.models[model].__name__
            with open(path.join(self.SCAFFOLD_APPS_DIR, self.app, 'admin.py'), 'r') as fp:
                content = fp.read()
            if "admin.site.register({0})".format(model_name) in content:
                self._info('exists\t{0}{1}/admin.py\t{2}'.format(self.SCAFFOLD_APPS_DIR, self.app,
                                                                 self.model.lower()), 1)
            else:
                with open(path.join(self.SCAFFOLD_APPS_DIR, self.app, 'admin.py'), 'a') as fp:
                    fp.write(ADMIN_CONTENT % {'app': self.app, 'model': model_name})
                self._info('added\t{0}{1}/admin.py\t{2}'.format(self.SCAFFOLD_APPS_DIR, self.app,                                                            self.model.lower()), 1)

    def create_tests(self):
        self._info("   Tests   ")
        self._info("===========")

        # Check if tests.py exists
        if path.exists('{0}{1}/tests.py'.format(self.SCAFFOLD_APPS_DIR, self.app)):
            self._info('exists\t{0}{1}/tests.py'.format(self.SCAFFOLD_APPS_DIR, self.app), 1)
            # Check if imports exists:
            import_testcase = True
            import_user = True
            import_reverse = True

            with open("{0}{1}/tests.py".format(self.SCAFFOLD_APPS_DIR, self.app), 'r') as fp:
                for line in fp.readlines():
                    if 'import TestCase' in line:
                        import_testcase = False
                    if 'import User' in line:
                        import_user = False
                    if 'import reverse' in line:
                        import_reverse = False

            with open("{0}{1}/tests.py".format(self.SCAFFOLD_APPS_DIR, self.app), 'a') as fp:
                if import_testcase:
                    fp.write("from django.test import TestCase\n")
                if import_user:
                    fp.write("from django.contrib.auth.models import User\n")
                if import_reverse:
                    fp.write("from django.urls import reverse\n")
        else:
            with open("{0}{1}/tests.py".format(self.SCAFFOLD_APPS_DIR, self.app), 'w') as fp:
                fp.write("from django.test import TestCase\n")
                fp.write("from django.contrib.auth.models import User\n")
                fp.write("from django.urls import reverse\n")
            self._info('create\t{0}{1}/tests.py'.format(self.SCAFFOLD_APPS_DIR, self.app), 1)

        # Check if test class already exists
        with open("{0}{1}/tests.py".format(self.SCAFFOLD_APPS_DIR, self.app), 'r') as fp:
            content = fp.read()
        if "class {0}Test".format(self.model) in content:
            self._info('exists\t{0}{1}/tests.py\t{2}'.format(
                self.SCAFFOLD_APPS_DIR, self.app, self.model.lower()), 1)
        else:
            with open("{0}{1}/tests.py".format(self.SCAFFOLD_APPS_DIR, self.app), 'a') as fp:
                fp.write(TESTS_CONTENT % {
                    'app': self.app,
                    'model': self.model,
                    'lower_model': self.model.lower(),
                })
            self._info('added\t{0}{1}/tests.py\t{2}'.format(self.SCAFFOLD_APPS_DIR, self.app,
                                                            self.model.lower()), 1)

    def run(self):
        print(self.app, self.model, self.fields)
        if not self.app:
            sys.exit("No application name found...")
        if not self.app.isalnum():
            sys.exit("Model name should be alphanumerical...")
        self.create_app()
        if self.model:
            self.create_forms()
            self.create_views()
            self.create_admin()
            self.create_urls()
            self.create_templates()
            # self.create_tests()
