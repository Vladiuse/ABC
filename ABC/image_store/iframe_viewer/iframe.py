from bs4 import BeautifulSoup


class DomFixxer:
    """Изменение верстки сайта"""

    @staticmethod
    def add_css(soup, css_text):
        """Добавить стили на сайт"""
        styles_tag = soup.new_tag('style')
        styles_tag.string = css_text
        soup.html.body.append(styles_tag)

    @staticmethod
    def add_js(soup, js_text):
        """Добавить скрипт на сайт"""
        script_tag = soup.new_tag("script")
        script_tag.string = js_text
        soup.html.body.append(script_tag)

    @staticmethod
    def add_base_tag(soup, url):
        """Добавить тэг base или замена его href"""
        base = soup.find('base')
        if base:
            base.extract()
        new_base = soup.new_tag('base')
        new_base['href'] = url
        soup.html.head.insert(0, new_base)


class Land:
    TYPES_REL = ['shortcut icon', 'icon', 'apple-touch-icon', 'apple-touch-icon-precomposed', 'image/x-icon']

    def __init__(self, source_text, url, *, parser='html5lib', escape_chars=False):
        self.source_text = Land.re_escape_html_chars(source_text) if escape_chars else source_text
        self.url = url
        self.soup = BeautifulSoup(self.source_text, parser)
        self.human_text = None
        self.img_doubles = None

        self.add_jquery()

    def get_no_protocol_url(self):
        return self.url.replace('http://', '')

    def add_jquery(self):
        new_tag = self.soup.new_tag('script')
        new_tag['src'] = 'https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js'
        self.soup.html.head.append(new_tag)


    def _get_title(self):
        """найти title сайта"""
        title = self.soup.find('title')
        return title.text

    def _is_video_tag_on_site(self):
        """Есть ли на сайте тэг video"""
        if self.soup.find_all('video'):
            return True

    def get_favicon_links(self, add_base_url=True):
        links = self.soup.find_all('link')
        links = list(filter(self.is_favicon_links, links))
        if add_base_url:
            for l in links:
                if not l['href'].startswith('http'):
                    l['href'] = Land.get_url_for_base_tag(self.url) + l['href']
                yield str(l)

    @staticmethod
    def is_favicon_links(link):
        res = []
        for attr in ['rel', 'type']:
            try:
                a = link[attr]
                if isinstance(a, str):
                    res.append(a)
                if isinstance(a, list):
                    res.extend(a)
            except KeyError:
                pass
        for attr in res:
            if attr in Land.TYPES_REL:
                return True

    @property
    def scripts(self):
        for script in self.soup.find_all('script'):
            yield str(script)

    @staticmethod
    def re_escape_html_chars(html_text):
        chars = [('&copy;', '©'), ('&#8211;', '-'), ('&#8220;', '“'), ('&#8221;', '”'), ('&#39;', "'"), ('&nbsp;', ' '),
                 ('&quot;', '"'),
                 ('&apos;', "'"),
                 ('&&', '@@'), ('&', '&amp;&amp;'), ('@@', '&&')]
        for char, chat_to in chars:
            html_text = html_text.replace(char, chat_to)
        print(len(html_text), 're_escape')
        return html_text

    @staticmethod
    def escape_html_for_iframe(html_text):
        chars = [
            # ('&', '&amp;&amp;'),
            ('"', '&quot;'), ("'", '&apos;')]
        for char, chat_to in chars:
            html_text = html_text.replace(char, chat_to)
        return html_text

    @staticmethod
    def get_url_for_base_tag(url):
        if '?' in url:
            url = url.split('?')[0]
        if not url.endswith('/'):
            url += '/'
        return url

    def add_style_tag(self, style_text):
        DomFixxer.add_css(self.soup, style_text)

    def add_script_tag(self, scritp_text):
        DomFixxer.add_js(self.soup, scritp_text)

    def add_base_tag(self):
        url_base_tag = self.get_url_for_base_tag(self.url)
        DomFixxer.add_base_tag(self.soup, url_base_tag)


    def drop_tags_from_dom(self, elems_ids):
        for id in elems_ids:
            elem = self.soup.find(id=id)
            if elem:
                elem.decompose()

    def get_human_land_text(self):
        clean_land_text = self.soup.text
        clean_land_text += ' ' + self.title
        inputs = self.soup.find_all('input')
        placeholders_text = ['']
        for inpt in inputs:
            try:
                placeholder = inpt['placeholder']
                placeholders_text.append(placeholder)
            except KeyError:
                pass
        placeholders_text = ' '.join(placeholders_text)
        clean_land_text += placeholders_text
        return clean_land_text

    @property
    def title(self):
        return self._get_title()

    def is_yam_script(self):
        yam_link = 'https://mc.yandex.ru/metrika'
        for script in self.scripts:
            if yam_link in script:
                return True

    def __str__(self):
        return str(self.soup)
