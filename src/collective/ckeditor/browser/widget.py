from plone.app.textfield.widget import RichTextWidget


def ckeditor_richtextwidget_render(widget):
    return RichTextWidget.render(widget)