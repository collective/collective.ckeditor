from Products.Five import BrowserView
from collective.ckeditor import LOG


class ForceEditorView(BrowserView):
    """ based on
    https://plone.org/products/tinymce/documentation/how-to/how-to-set-tinymce-as-default-editor-for-current-users/
    """

    def __call__(self):
        pm = self.context.portal_membership
        # Comma separated member IDs
        userids = self.request.get('userids', None)
        new_editor = self.request.get('editor', '').strip()
        if userids is None:
            userids = pm.listMemberIds()
        else:
            userids = userids.split(',')

        available = self.context.portal_properties.site_properties.available_editors
        if new_editor != '' and new_editor not in available:
            return u'Editor %s is not supported by site_properties.available_editors: %s' % (new_editor, available)

        total_members = len(userids)
        total = 0
        for memberId in userids:
            member = pm.getMemberById(memberId)
            if member:
                editor = member.getProperty('wysiwyg_editor', None)
                if editor != new_editor:
                    total += 1
                    member.setMemberProperties({'wysiwyg_editor': new_editor})
                    if new_editor:
                        LOG.info('%s: Editor %s has been set.', memberId, new_editor)
                    else:
                        LOG.info('%s: Default editor has been set', memberId)
        if new_editor:
            return u'Editor %s has been set for %d members out of %d' % (new_editor, total, total_members)
        else:
            return u'Default editor has been set for %d members out of %d.' % (total, total_members)
