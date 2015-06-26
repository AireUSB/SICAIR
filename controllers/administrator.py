# -*- coding: utf-8 -*-

@auth.requires_permission('manage', 'users')
def index():
    redirect(URL('list_users'))

@auth.requires_permission('manage', 'users')
def pending_users():
    rows = db(db.auth_user.registration_key=='pending').select()
    session.last_visited_url = request.url
    return locals()

@auth.requires_permission('manage', 'users')
def modify_user():
    user = db.auth_user(request.args(1,cast=int))
    action = request.args(0)
    redirect_url = session.get('last_visited_url', URL('index'))
    if (not action) or (not user) or (action not in ['authorize', 'disable']):
        session.flash = T('Invalid modification')
        redirect(redirect_url)
    if action == 'authorize':
        db(db.auth_user.id == user.id).update(registration_key='')
    elif action == 'disable':
        db(db.auth_user.id == user.id).update(registration_key='disabled')
    redirect(redirect_url)

@auth.requires_permission('manage', 'users')
def list_users():
    session.last_visited_url = request.url
    row_status = {'pending' : T('Pending'), '': T('Active'), 'disabled': T('Disabled')}
    row_change = {'pending' : 'authorize', '': 'disable', 'disabled': 'authorize'}
    btn = lambda row: A("Edit", _href=URL('manage_user', args=row.auth_user.id))
    mod_url = lambda row: URL( 'modify_user', args=[row_change[row.registration_key], row.id] )
    tog = lambda row: [A(row_status[row.registration_key], _href=mod_url(row))]
    db.auth_user.edit = Field.Virtual(btn)
    rows = db(db.auth_user).select()
    headers = [T("ID"), T("USB ID"), T("Name"), T("Last Name"), T("Email"), T("Edit"), T("Status")]
    fields = ['id', 'usbid', 'first_name', 'last_name', "email", "edit"]
    table = TABLE(THEAD(TR(*[B(header) for header in headers])),
                  TBODY(*[TR(*[TD(row[field]) for field in fields] + tog(row)) \
                        for row in rows]))
    table["_class"] = "table table-striped table-bordered table-condensed"
    return dict(table=table)

@auth.requires_permission('manage', 'users')
def manage_user():
    user_id = request.args(0) or redirect(URL('list_users'))
    # db.auth_user.password.readable = db.auth_user.password.writable = False
    form = SQLFORM(db.auth_user, user_id).process()
    membership_panel = LOAD(request.controller,
                            'manage_membership.html',
                             args=[user_id],
                             ajax=True)
    return dict(form=form,membership_panel=membership_panel)

@auth.requires_permission('manage', 'users')
def manage_membership():
    user_id = request.args(0) or redirect(URL('list_users'))
    db.auth_membership.user_id.default = int(user_id)
    db.auth_membership.user_id.writable = False
    form = SQLFORM.grid(db.auth_membership.user_id == user_id,
                       args=[user_id],
                       searchable=False,
                       details=False,
                       selectable=False,
                       csv=False,
                       user_signature=False)
    return form

@auth.requires_permission('manage', 'catalogs')
def catalogs():
    catalogs = {}
    catalogs[T('Bachelor Degrees')] = SQLFORM.grid(db.bachelor_degree)
    #catalogs[T('Data Base Name')] = SQLFORM.grid(db.data_base_name)
    return locals()
