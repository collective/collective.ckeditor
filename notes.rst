Notes for migration CKEditor to P5
==================================

plone/app/z3cform/widget.py - `RichTextWidget.render` :

```
            if not allowed_mime_types or len(allowed_mime_types) <= 1:
                # Display textarea with default widget
                rendered = patextfield_RichTextWidget.render(self)
                # rendered = super(RichTextWidget, self).render()
```

Change `plone allowed_types` in registry 'IMarkupSchema' and remove `x-web-textile`

