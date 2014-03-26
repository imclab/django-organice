#!/usr/bin/env python
#
# Copyright 2014 Peter Bittner <django@bittner.it>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Setup script for starting a django Organice project.
"""
from organice.management.settings import DjangoModuleManager, DjangoSettingsManager
from stat import S_IRUSR, S_IWUSR, S_IXUSR, S_IRGRP, S_IXGRP, S_IROTH, S_IXOTH
from subprocess import call
import os
import sys


def startproject():
    """
    Starts a new django Organice project by first generating a Django project
    using ``django-admin.py``, and then modifying the project settings.
    """
    usage_descr = 'django Organice setup. Start getting organiced! ' \
                  'Your collaboration platform starts here.'

    if sys.version_info < (2, 7):
        from optparse import OptionParser  # Deprecated since version 2.7

        parser = OptionParser(description=usage_descr)
        (options, args) = parser.parse_args()
        if len(args) != 1:
            parser.error('Please specify a projectname')
        projectname = args[0]
    else:
        from argparse import ArgumentParser  # New since version 2.7

        parser = ArgumentParser(description=usage_descr)
        parser.add_argument('projectname', help='name of project to create')
        args = parser.parse_args()
        projectname = args.projectname

    mode0755 = S_IRUSR | S_IWUSR | S_IXUSR | S_IRGRP | S_IXGRP | S_IROTH | S_IXOTH
    profiles = ('develop', 'staging', 'production')
    filenames = ('__init__', 'common') + profiles

    print('Generating project %s ...' % projectname)
    code = call(['django-admin.py', 'startproject', projectname, '.'])
    if code != 0:
        return code
    os.chmod('manage.py', mode0755)

    print('Creating directories ...')
    os.mkdir('media')
    os.mkdir('static')
    os.mkdir('templates')
    os.mkdir(os.path.join(projectname, 'settings'))

    print('Converting settings to deployment profiles (%s) ...' % ', '.join(profiles))
    os.rename(os.path.join(projectname, 'settings.py'),
              os.path.join(projectname, 'settings', 'common.py'))

    settings = DjangoSettingsManager(projectname, *filenames)
    settings.append_lines('__init__',
                          '"""',
                          'Modularized settings generated by django Organice setup. http://organice.io',
                          'This solution follows the second recommendation from',
                          'http://www.sparklewise.com/django-settings-for-production-and-development-best-practices/',
                          '"""',
                          'from .develop import *')
    for prof in profiles:
        settings.append_lines(prof,
                              '# Django project settings for %s environment' % prof.capitalize(),
                              '',
                              'from .common import *')

    # out-of-the-box Django values relevant for deployment
    settings.move_var('common', profiles, 'DEBUG')
    settings.move_var('common', profiles, 'TEMPLATE_DEBUG')
    settings.move_var('common', profiles, 'ALLOWED_HOSTS')
    settings.move_var('common', profiles, 'DATABASES')
    settings.move_var('common', profiles, 'SECRET_KEY')
    settings.move_var('common', profiles, 'WSGI_APPLICATION')
    settings.insert_lines('common',
                          'import os',
                          'PROJECT_PATH = os.sep.join(__file__.split(os.sep)[:-3])')
    settings.set_value('common', 'MEDIA_URL', "'/media/'")
    settings.set_value('common', 'MEDIA_ROOT', "os.path.join(PROJECT_PATH, 'media')")
    settings.set_value('common', 'STATIC_ROOT', "os.path.join(PROJECT_PATH, 'static')")
    settings.set_value('common', 'USE_I18N', False)
    settings.set_value('staging', 'DEBUG', False)
    settings.set_value('production', 'DEBUG', False)

    print('Configuring development database ...')
    DEV_DATABASES = """{
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(PROJECT_PATH, '%s.sqlite'),  # path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',  # Set to empty string for default.
    }
}""" % projectname
    settings.set_value('develop', 'DATABASES', DEV_DATABASES)

    # configuration for included packages
    adding_settings_for = 'Adding settings for %s ...'

    print(adding_settings_for % 'installed apps')
    settings.delete_var('common', 'INSTALLED_APPS')
    settings.append_lines('common',
                          'INSTALLED_APPS = (',
                          "    'django.contrib.auth',",
                          "    'django.contrib.comments',",
                          "    'django.contrib.contenttypes',",
                          "    'django.contrib.sessions',",
                          "    'django.contrib.sites',",
                          "    'django.contrib.messages',",
                          "    'django.contrib.staticfiles',",
                          "    'django.contrib.admin',",
                          "    'organice',",
                          "    'cms',",
                          "    'mptt',",
                          "    'menus',",
                          "    'south',",
                          "    'sekizai',",
                          "    'reversion',",
                          "    'cms.plugins.text',",
                          "    'cms.plugins.picture',",
                          "    'cms.plugins.link',",
                          "    'cms.plugins.teaser',",
                          "    'cms.plugins.file',",
                          "    'cms.plugins.video',",
                          "    'cms.plugins.flash',",
                          "    'cms.plugins.googlemap',",
                          "    'cms.plugins.inherit',",
                          "    'cmsplugin_contact',",
                          "    'cmsplugin_zinnia',",
                          "    'tagging',",
                          "    'emencia.django.newsletter',",
                          "    'tinymce',",
                          "    'simple_links',",
                          "    'zinnia',",
                          "    'allauth',",
                          "    'allauth.account',",
                          "    'allauth.socialaccount',",
                          "#    'allauth.socialaccount.providers.amazon',",
                          "#    'allauth.socialaccount.providers.angellist',",
                          "#    'allauth.socialaccount.providers.bitbucket',",
                          "#    'allauth.socialaccount.providers.bitly',",
                          "#    'allauth.socialaccount.providers.dropbox',",
                          "#    'allauth.socialaccount.providers.facebook',",
                          "#    'allauth.socialaccount.providers.flickr',",
                          "#    'allauth.socialaccount.providers.feedly',",
                          "#    'allauth.socialaccount.providers.github',",
                          "#    'allauth.socialaccount.providers.google',",
                          "#    'allauth.socialaccount.providers.instagram',",
                          "#    'allauth.socialaccount.providers.linkedin',",
                          "#    'allauth.socialaccount.providers.linkedin_oauth2',",
                          "#    'allauth.socialaccount.providers.openid',",
                          "#    'allauth.socialaccount.providers.persona',",
                          "#    'allauth.socialaccount.providers.soundcloud',",
                          "#    'allauth.socialaccount.providers.stackexchange',",
                          "#    'allauth.socialaccount.providers.tumblr',",
                          "#    'allauth.socialaccount.providers.twitch',",
                          "#    'allauth.socialaccount.providers.twitter',",
                          "#    'allauth.socialaccount.providers.vimeo',",
                          "#    'allauth.socialaccount.providers.vk',",
                          "#    'allauth.socialaccount.providers.weibo',",
                          ')')

    print(adding_settings_for % 'user profiles and authentication')
    settings.append_lines('common',
                          'AUTHENTICATION_BACKENDS = (',
                          "    'django.contrib.auth.backends.ModelBackend',",
                          "    'allauth.account.auth_backends.AuthenticationBackend',",
                          ')')
    settings.set_value('common', 'LOGIN_REDIRECT_URL', '/')
    settings.set_value('common', 'EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
    settings.set_value('common', 'SERVER_EMAIL', 'noreply@example.com')

    print(adding_settings_for % 'django CMS')
    settings.delete_var('common', 'MIDDLEWARE_CLASSES')
    settings.append_lines('common',
                          'MIDDLEWARE_CLASSES = (',
                          "    'django.middleware.common.CommonMiddleware',",
                          "    'django.middleware.doc.XViewMiddleware',",
                          "    'solid_i18n.middleware.SolidLocaleMiddleware',",
                          "    'django.middleware.csrf.CsrfViewMiddleware',",
                          "    'django.contrib.sessions.middleware.SessionMiddleware',",
                          "    'django.contrib.messages.middleware.MessageMiddleware',",
                          "    'django.contrib.auth.middleware.AuthenticationMiddleware',",
                          "    'cms.middleware.page.CurrentPageMiddleware',",
                          "    'cms.middleware.user.CurrentUserMiddleware',",
                          "    'cms.middleware.toolbar.ToolbarMiddleware',",
                          "    'cms.middleware.language.LanguageCookieMiddleware',",
                          ')')
    # must be set both in order to make solid_i18n work properly
    settings.set_value('common', 'LANGUAGE_CODE', """'en-us'
LANGUAGES = (
    ('en-us', 'English (United States)'),
)""")
    settings.set_value('common', 'CMS_USE_TINYMCE', 'False')
    settings.append_lines('common',
                          'CMS_TEMPLATES = (',
                          "    ('cms_base.html', 'Template for normal content pages'),",
                          "    ('cms_bookmarks.html', 'Template for the bookmarks page'),",
                          ')')
    settings.delete_var('common', 'TEMPLATE_DIRS')
    settings.append_lines('common',
                          'TEMPLATE_DIRS = (',
                          "    # Don't forget to use absolute paths, not relative paths.",
                          "    os.path.join(PROJECT_PATH, 'templates'),",
                          "    os.path.join(PROJECT_PATH, 'templates', 'zinnia'),",
                          ')')
    settings.delete_var('common', 'TEMPLATE_LOADERS')
    settings.append_lines('common',
                          'TEMPLATE_LOADERS = (',
                          "    'django.template.loaders.filesystem.Loader',",
                          "    'django.template.loaders.app_directories.Loader',",
                          "    'apptemplates.Loader',",
                          ')')
    settings.append_lines('common',
                          'TEMPLATE_CONTEXT_PROCESSORS = (',
                          "    'django.contrib.auth.context_processors.auth',",
                          "    'django.core.context_processors.i18n',",
                          "    'django.core.context_processors.request',",
                          "    'django.core.context_processors.media',",
                          "    'django.core.context_processors.static',",
                          "    'allauth.account.context_processors.account',",
                          "    'allauth.socialaccount.context_processors.socialaccount',",
                          "    'cms.context_processors.media',",
                          "    'sekizai.context_processors.sekizai',",
                          "    'organice.context_processors.expose',",
                          ')')

    print(adding_settings_for % 'Emencia Newsletter')
    settings.append_lines('common',
                          "NEWSLETTER_DEFAULT_HEADER_SENDER = 'Your Organization <newsletter@your.domain>'",
                          'NEWSLETTER_USE_TINYMCE = True',
                          'NEWSLETTER_TEMPLATES = [',
                          "    { 'title': 'Sample template for newsletter',",
                          "      'src': '/media/newsletter/templates/sample-template.html',",
                          "      'description': 'Newsletter template tabular sample' },",
                          ']',
                          'TINYMCE_DEFAULT_CONFIG = {',
                          "    'height': 450,",
                          "    'width': 800,",
                          "    'convert_urls': False,",
                          "    'plugins': 'table,paste,searchreplace,template,advlist,autolink,autosave',",
                          "    'template_templates': NEWSLETTER_TEMPLATES,",
                          "    'theme': 'advanced',",
                          "    'theme_advanced_toolbar_location': 'top',",
                          "    'theme_advanced_buttons1': 'template,|,formatselect,' \\",
                          "        '|,bold,italic,underline,strikethrough,|,undo,redo,' \\",
                          "        '|,justifyleft,justifycenter,justifyright,justifyfull,' \\",
                          "        '|,bullist,numlist,dt,dd,|,outdent,indent,|,blockquote',",
                          "    'theme_advanced_buttons2': 'tablecontrols,|,forecolor,backcolor,' \\",
                          "        '|,hr,image,anchor,link,unlink,|,visualaid,code',",
                          "    'theme_advanced_resizing': True,",
                          '}')

    print(adding_settings_for % 'Zinnia Blog')
    settings.append_lines('common',
                          '# use plugin system of django-cms in blog entries',
                          "ZINNIA_ENTRY_BASE_MODEL = 'cmsplugin_zinnia.placeholder.EntryPlaceholder'",
                          "ZINNIA_WYSIWYG = 'wymeditor'")
    settings.append_lines('common',
                          'SOUTH_MIGRATION_MODULES = {',
                          '    # integration of EntryPlaceholder (django CMS) into Zinnia',
                          "    'zinnia': 'organice.migrations.zinnia',",
                          '}')

    settings.save_files()

    print('Configuring project URLs ...')
    gen_by_comment = '# generated by django Organice'
    project = DjangoModuleManager(projectname)
    project.add_file('urls', lines=(gen_by_comment, 'from organice.urls import urlpatterns'))
    project.save_files()

    suggest_editing = ('ADMINS', 'TIME_ZONE', 'LANGUAGE_CODE', 'LANGUAGES', 'EMAIL_BACKEND', 'SERVER_EMAIL')
    suggest_adding = ()
    print('Done. Enjoy your organiced day!' + os.linesep)

    print('Please visit file `%s` and edit or add the variables: %s' %
          (settings.get_file('common').name, ', '.join(suggest_editing + suggest_adding)))
    print('Please visit file `%s` and configure your development database in: %s' %
          (settings.get_file('develop').name, 'DATABASES'))
    print('See https://docs.djangoproject.com/en/1.5/ref/settings/ for details.' + os.linesep)

    print('To initialize your development database run: `python manage.py syncdb --migrate`')
    print('You can then run your development server with: `python manage.py runserver`')


if __name__ == "__main__":
    startproject()
