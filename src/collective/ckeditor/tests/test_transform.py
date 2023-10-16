import unittest


class TestReplaceUids(unittest.TestCase):

    def testFindTagImg(self):
        from collective.ckeditor.transforms import ck_ruid_to_url
        # single quotes
        text = "<img src='resolveuid/abcdef' />'"
        tags, unique = ck_ruid_to_url.find_tags_with_resolveuid(text)
        self.assertEquals(len(tags), 1)
        self.assertEquals(tags[0], ("<img src='resolveuid/abcdef' />",
                                    'abcdef', 'resolveuid/abcdef'))
        self.assertEquals(len(unique), 1)
        self.assertEquals(unique, set(["abcdef"]))
        # double quotes
        text = '<img src="resolveuid/abcdef" />'
        tags, unique = ck_ruid_to_url.find_tags_with_resolveuid(text)
        self.assertEquals(len(tags), 1)
        self.assertEquals(tags[0], ('<img src="resolveuid/abcdef" />',
                                    'abcdef', 'resolveuid/abcdef'))
        self.assertEquals(len(unique), 1)
        self.assertEquals(unique, set(["abcdef"]))

    def testFindTagA(self):
        from collective.ckeditor.transforms import ck_ruid_to_url
        # single quotes
        text = "<a href='resolveuid/abcdef'>Link</a>"
        tags, unique = ck_ruid_to_url.find_tags_with_resolveuid(text)
        self.assertEquals(len(tags), 1)
        self.assertEquals(tags[0], ("<a href='resolveuid/abcdef'>",
                                    'abcdef', 'resolveuid/abcdef'))
        self.assertEquals(len(unique), 1)
        self.assertEquals(unique, set(["abcdef"]))
        # double quotes
        text = '<a href="resolveuid/abcdef">Link</a>'
        tags, unique = ck_ruid_to_url.find_tags_with_resolveuid(text)
        self.assertEquals(len(tags), 1)
        self.assertEquals(tags[0], ('<a href="resolveuid/abcdef">',
                                    'abcdef', 'resolveuid/abcdef'))
        self.assertEquals(len(unique), 1)
        self.assertEquals(unique, set(["abcdef"]))

    def testFindTagEmbed(self):
        from collective.ckeditor.transforms import ck_ruid_to_url
        # single quotes
        text = "<embed src='resolveuid/abcdef' />"
        tags, unique = ck_ruid_to_url.find_tags_with_resolveuid(text)
        self.assertEquals(len(tags), 1)
        self.assertEquals(tags[0], ("<embed src='resolveuid/abcdef' />",
                                    'abcdef', 'resolveuid/abcdef'))
        self.assertEquals(len(unique), 1)
        self.assertEquals(unique, set(["abcdef"]))
        # double quotes
        text = '<embed src="resolveuid/abcdef" />'
        tags, unique = ck_ruid_to_url.find_tags_with_resolveuid(text)
        self.assertEquals(len(tags), 1)
        self.assertEquals(tags[0], ('<embed src="resolveuid/abcdef" />',
                                    'abcdef', 'resolveuid/abcdef'))
        self.assertEquals(len(unique), 1)
        self.assertEquals(unique, set(["abcdef"]))

    def testFindTagWithStyle(self):
        from collective.ckeditor.transforms import ck_ruid_to_url
        # single quotes
        text = (
            "<div style='background-image=url(resolveuid/abcdef);'>"
            "content</div>"
            )
        tags, unique = ck_ruid_to_url.find_tags_with_resolveuid(text)
        self.assertEquals(len(tags), 1)
        self.assertEquals(
            tags[0],
            ("<div style='background-image=url(resolveuid/abcdef);'>",
             'abcdef', 'resolveuid/abcdef')
        )
        self.assertEquals(len(unique), 1)
        self.assertEquals(unique, set(["abcdef"]))
        # double quotes
        text = (
            '<div style="background-image=url(resolveuid/abcdef);">'
            "content</div>"
            )
        tags, unique = ck_ruid_to_url.find_tags_with_resolveuid(text)
        self.assertEquals(len(tags), 1)
        self.assertEquals(
            tags[0],
            ('<div style="background-image=url(resolveuid/abcdef);">',
             'abcdef', 'resolveuid/abcdef')
        )
        self.assertEquals(len(unique), 1)
        self.assertEquals(unique, set(["abcdef"]))

    def testFindTagWithMoreStyle(self):
        from collective.ckeditor.transforms import ck_ruid_to_url
        # single quotes
        text = (
            "<div style='border-color: red; "
            "background-image=url(resolveuid/abcdef);'>"
            "content</div>"
            )
        tags, unique = ck_ruid_to_url.find_tags_with_resolveuid(text)
        self.assertEquals(len(tags), 1)
        self.assertEquals(
            tags[0],
            ("<div style='border-color: red; "
             "background-image=url(resolveuid/abcdef);'>",
             'abcdef', 'resolveuid/abcdef')
        )
        self.assertEquals(len(unique), 1)
        self.assertEquals(unique, set(["abcdef"]))
        # double quotes
        text = (
            '<div style="border-color: red; '
            'background-image=url(resolveuid/abcdef);">'
            "content</div>"
            )
        tags, unique = ck_ruid_to_url.find_tags_with_resolveuid(text)
        self.assertEquals(len(tags), 1)
        self.assertEquals(
            tags[0],
            ('<div style="border-color: red; '
             'background-image=url(resolveuid/abcdef);">',
             'abcdef', 'resolveuid/abcdef')
        )
        self.assertEquals(len(unique), 1)
        self.assertEquals(unique, set(["abcdef"]))

    def testFindTagWithEvenMoreStyle(self):
        from collective.ckeditor.transforms import ck_ruid_to_url
        # single quotes
        text = (
            "<div style='border-color: red; "
            "background-image=url(resolveuid/abcdef); "
            "border-style:solid'>"
            "content</div>"
            )
        tags, unique = ck_ruid_to_url.find_tags_with_resolveuid(text)
        self.assertEquals(len(tags), 1)
        self.assertEquals(
            tags[0],
            ("<div style='border-color: red; "
             "background-image=url(resolveuid/abcdef); "
             "border-style:solid'>",
             'abcdef', 'resolveuid/abcdef')
        )
        self.assertEquals(len(unique), 1)
        self.assertEquals(unique, set(["abcdef"]))
        # double quotes
        text = (
            '<div style="border-color: red; '
            'background-image=url(resolveuid/abcdef); '
            'border-style:solid">'
            "content</div>"
            )
        tags, unique = ck_ruid_to_url.find_tags_with_resolveuid(text)
        self.assertEquals(len(tags), 1)
        self.assertEquals(
            tags[0],
            ('<div style="border-color: red; '
             'background-image=url(resolveuid/abcdef); '
             'border-style:solid">',
             'abcdef', 'resolveuid/abcdef')
        )
        self.assertEquals(len(unique), 1)
        self.assertEquals(unique, set(["abcdef"]))

    def testMakeUid(self):
        from collective.ckeditor.transforms import ck_ruid_to_url
        unique = set(['abcdef'])

        def mocked(uid):
            return '/Plone/ABCDEF'

        uid_to_absolute_url = ck_ruid_to_url.make_uid_to_absolute_url(
            unique, compute_url=mocked)
        self.assertEquals(uid_to_absolute_url, dict(abcdef='/Plone/ABCDEF'))

    def testReplaceResolveUid(self):
        from collective.ckeditor.transforms import ck_ruid_to_url

        def mocked(uid):
            return '/Plone/ABCDEF'

        original = "<a href='resolveuid/abcdef'>Link</a>"
        final = ck_ruid_to_url.replace_resolveuid_urls_with_absolute_urls(
            original, compute_url=mocked)
        self.assertEquals(final, "<a href='/Plone/ABCDEF'>Link</a>")

        original = "<img src='resolveuid/abcdef' />"
        final = ck_ruid_to_url.replace_resolveuid_urls_with_absolute_urls(
            original, compute_url=mocked)
        self.assertEquals(final, "<img src='/Plone/ABCDEF' />")

        original = (
            "<div style='border-color: red; "
            "background-image=url(resolveuid/abcdef); "
            "border-style:solid'>"
            "content</div>"
            )
        final = ck_ruid_to_url.replace_resolveuid_urls_with_absolute_urls(
            original, compute_url=mocked)
        self.assertEquals(
            final,
            "<div style='border-color: red; "
            "background-image=url(/Plone/ABCDEF); "
            "border-style:solid'>content</div>")
