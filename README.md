# Sistema del servicio comunitario AireUSB

## Groups
- name='administrator', description='Administrators of the application'
- name='coordinator', description='Administrators of a lower level of the application'
- name='air', description='Aireuesebistas'

## Permissions
- group='administrator', name='manage', object='users'
- group='administrator', name='manage', object='hours'
- group='administrator', name='approve', object='hours'
- group='administrator', name='manage', object='catalogs'
- group='coordinator', name='manage', object='users'
- group='coordinator', name='manage', object='hours'
- group='coordinator', name='approve', object='hours'
- group='air', name='manage', object='hours'

## Files

### Models

#### db.py
Holds the database definition and more information about how should the information, seems more like a configuration file

#### menu.py
Configurations, and here we can add menu items to the menu.

### Controllers

#### adminstrator.py
Handles all the adminstrating there is:
- Users
- Catalogs

#### service.py
Handles all things related to the community service:
- Work hours
- Information about the community service

### Views
Must write down the specific ones we want, recommended to extend from the 'layout.html'

### Language
For internationalization, go into 'es.py' and translate everything, to make something pop up there use the global function `T()`, which receives strings and retruns the translated string.

#### Static
Images, CSS, Javascript

#### Private files
For API keys, these files are never served to a client.
