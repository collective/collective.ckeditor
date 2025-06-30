from zope.component import getUtility
from plone.registry.interfaces import IRegistry
import pprint
from Products.Five import BrowserView


class ImportMap(BrowserView):

    def render(self):
        registry = getUtility(IRegistry)
        importmap = pprint.pformat(registry['plone.importmap']).replace("'", '"')
        result = f"""
        <script type="importmap">
    {{
	    "imports": 
        {importmap}
    }}
        </script>"""
        return result




