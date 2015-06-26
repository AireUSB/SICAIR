# -*- coding: utf-8 -*-

def index():
    if auth.has_permission('manage', 'hours'):
        redirect('list_hours')
    message = T("Hello world")
    return locals()

@auth.requires_permission('manage', 'hours')
def list_hours():
    btn = lambda row: A("Edit", _href=URL('manage_hour', args=row.id))
    db.work_hour.edit = Field.Virtual(btn)
    rows = db(db.work_hour).select()
    headers = [T("Quantity"), T("Description"), T("Approved"), T("Edit")]
    fields = ['quantity', 'description', 'approved']

    form = None
    total_hours = None
    approved_hours = None
    if auth.has_membership('air'):
        rows = db(db.work_hour.student==auth.user_id).select()
        total_hours = 0
        approved_hours = 0
        for row in rows:
            total_hours += int(row.quantity)
            if (row.approved):
                approved_hours += int(row.quantity)
        db.work_hour.student.default = auth.user_id
        form = SQLFORM(db.work_hour).process()
        if form.accepted:
            session.flash = T("Hours added, wait for approval")
            redirect(URL())
    if auth.has_permission('approve', 'hours'):
        name = lambda row: row.student.first_name + ' ' + row.student.last_name
        apr = lambda row: [A(T('Change'), _href=URL('toggle_hour', args=row.id)), A(name(row), _href=URL('administrator', 'manage_user', args=[row.student.id]))]
        headers = headers + [T("Approve"), T("Student")]
    else:
        apr = lambda row: []
    table = TABLE(THEAD(TR(*[B(header) for header in headers])),
                  TBODY(*[TR(*[TD(row[field]) for field in fields] + [btn(row)] + apr(row)) \
                        for row in rows]))
    table["_class"] = "table table-striped table-bordered table-condensed"
    return dict(table=table, form=form, total_hours=total_hours, approved_hours=approved_hours)

@auth.requires_permission('manage', 'hours')
def manage_hour():
    hour_id = request.args(0) or redirect(URL('list_hours'))
    hour = db.work_hour(hour_id)
    if not hour:
        session.flash = T('Invalid work houts')
        redirect(URL('list_hours'))
    if hour.approved:
        db.work_hour.quantity.writable = False
    form = SQLFORM(db.work_hour, hour_id, deletable=not hour.approved).process()
    return dict(form=form)

@auth.requires_permission('approve', 'hours')
def toggle_hour():
    hour_id = request.args[0]
    hour = db.work_hour(hour_id)
    if not hour:
        session.flash = T('Impossible to toggle that hour')
        redirect(ULR('list_hours'))
    db(db.work_hour.id == hour_id).update(approved=not hour.approved)
    redirect(URL('list_hours'))
