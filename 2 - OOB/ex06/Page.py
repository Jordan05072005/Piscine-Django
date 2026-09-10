from elem import Elem
from elements import *

class Page:
    def __init__(self, page: Elem):
        self.page = page
        pass

    def __str__(self):
        return ("<!DOCTYPE html>\n" if isinstance(self.page, Html) else "") + self.page.__str__()

    def write_to_file(self, filename):
        with open(filename, 'w') as f:
            f.write(self.__str__())

    def is_valid(self, element: Elem = None):
        valid = True
        if element is None:
            element = self.page

        if isinstance(element, Text):
            return True

        if not isinstance(element, (Html, Head, Body, Title, Meta, Img, Table, Th, Tr, Td , Ul, Ol, Li, H1, H2, P, Div, Span, Hr, Br, Text)):
            return False

        for elem in element.content:
            if elem:
                valid = self.is_valid(elem) and valid
            if not valid:
                return valid
            if isinstance(elem, Html):
                valid = self.check_html(elem)
            elif isinstance(elem, Head):
                valid = self.check_head(elem)
            elif isinstance(elem, (Body, Div)):
                valid = self.check_body_div(elem)
            elif isinstance(elem, (Title, H1, H2, Li, Th, Td)):
                valid = self.check_unique_text(elem)
            elif isinstance(elem, P):
                valid = self.check_contain_text(elem)
            elif isinstance(elem, Span):
                valid = self.check_span(elem)
            elif isinstance(elem, (Ul, Ol)):
                valid = self.check_ul_ol(elem)
            elif isinstance(elem, Tr):
                valid = self.check_tr(elem)
            elif isinstance(elem, Table):
                valid = self.check_table(elem)
        return valid

    @staticmethod
    def check_html(elem: Html):
        if len(elem.content) != 2 or not isinstance(elem.content[0], Head) or not isinstance(elem.content[1], Body):
            return False
        return True

    @staticmethod
    def check_head(elem: Head):
        if len(elem.content) > 1 or (len(elem.content) != 0 and not isinstance(elem.content[0], Title)):
            return False
        return True

    @staticmethod
    def check_body_div(elem: Body | Div):
        for content in elem.content:
            if not isinstance(content, (H1, H2, Div, Table, Ul, Ol, Span, Text)):
                return False
        return True

    @staticmethod
    def check_unique_text(elem: Elem):
        if len(elem.content) > 1 or (len(elem.content) != 0 and not isinstance(elem.content[0], Text)):
            return False
        return True

    @staticmethod
    def check_contain_text(elem: Elem):
        for content in elem.content:
            if not isinstance(content, Text):
                return False
        return True

    @staticmethod
    def check_span(elem: Span):
        for content in elem.content:
            if not isinstance(content, Text) and not isinstance(content, P):
                return False
        return True

    @staticmethod
    def check_ul_ol(elem: Ul | Ol):
        if len(elem.content) < 1:
            return False
        for content in elem.content:
            if not isinstance(content, Li) :
                return False
        return True

    @staticmethod
    def check_tr(elem: Tr):
        if len(elem.content) < 1:
            return False
        if not isinstance(elem.content[0], (Td, Th)):
            return False
        type_ = type(elem.content[0])
        for content in elem.content:
            if not isinstance(content, type_):
                return False
        return True

    @staticmethod
    def check_table(elem: Table):
        for content in elem.content:
            if not isinstance(content, Tr):
                return False
        return True


if __name__ == '__main__':
    page_var = Html([
        Head([
            Meta(attr={"charset": "UTF-8"}),
            Meta(attr={"name": "viewport", "content": "width=device-width, initial-scale=1.0"}),
            Title(Text("Page de test complète")),
        ]),
        Body(
            attr={"class": "main", "id": "page"},
            content=[
                H1(Text("Oh no, not again!")),
                P(Text('Un paragraphe avec des caractères spéciaux : <, >, &, "')),

                Div(
                    attr={"class": "container"},
                    content=[
                        H2(Text("Une section")),
                        P(Text("Texte sur plusieurs lignes")),
                        Span(Text("Un span inline")),
                        Br(),
                        Span(Text("Et un second span après un retour à la ligne")),
                    ],
                ),

                Ul([
                    Li(Text("Premier élément")),
                    Li(Text("Deuxième élément")),
                ]),
                Ol([
                    Li(Text("Étape 1")),
                    Li(Text("Étape 2")),
                ]),

                Table([
                    Tr([Th(Text("Nom")), Th(Text("Âge"))]),
                    Tr([Td(Text("Alice")), Td(Text("30"))]),
                    Tr([Td(Text("Bob")), Td(Text("25"))]),
                ]),

                Hr(),

                Img(attr={"src": "http://i.imgur.com/pfp3T.jpg", "alt": "image"}),

                Div(attr={"class": "empty"}),  # content=None
                P(Text("")),                   # Text vide

                Div(
                    attr={"class": "footer"},
                    content=[Span(Text("Pied de page"))],
                ),
            ],
        ),
    ])
    page = Page(page_var)
    print(page)
    page.write_to_file("test.html")
    page.write_to_file("test.template")



