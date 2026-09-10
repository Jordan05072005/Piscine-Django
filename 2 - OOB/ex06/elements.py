from elem import Elem, Text


class Html(Elem):
    def __init__(self, content=None, attr=None, tag_type='double'):
        super().__init__(tag='html', attr=attr, content=content, tag_type=tag_type)


class Head(Elem):
    def __init__(self, content=None, attr=None, tag_type='double'):
        super().__init__(tag='head', attr=attr, content=content, tag_type=tag_type)

class Body(Elem):
    def __init__(self, content=None, attr=None, tag_type='double' ):
        super().__init__(tag='body', attr=attr, content=content, tag_type=tag_type)

class Title(Elem):
    def __init__(self, content=None, attr=None, tag_type='double' ):
        super().__init__(tag='title', attr=attr, content=content, tag_type=tag_type)

class Meta(Elem):
    def __init__(self, content=None, attr=None, tag_type='simple' ):
        super().__init__(tag='meta', attr=attr, content=content, tag_type=tag_type)

class Img(Elem):
    def __init__(self, content=None, attr=None, tag_type='simple' ):
        super().__init__(tag='img', attr=attr, content=content, tag_type=tag_type)

class Table(Elem):
    def __init__(self, content=None, attr=None, tag_type='double' ):
        super().__init__(tag='table', attr=attr, content=content, tag_type=tag_type)

class Th(Elem):
    def __init__(self, content=None, attr=None, tag_type='double' ):
        super().__init__(tag='th', attr=attr, content=content, tag_type=tag_type)

class Tr(Elem):
    def __init__(self, content=None, attr=None, tag_type='double' ):
        super().__init__(tag='tr', attr=attr, content=content, tag_type=tag_type)

class Td(Elem):
    def __init__(self, content=None, attr=None, tag_type='double' ):
        super().__init__(tag='td', attr=attr, content=content, tag_type=tag_type)

class Ul(Elem):
    def __init__(self, content=None, attr=None, tag_type='double' ):
        super().__init__(tag='ul', attr=attr, content=content, tag_type=tag_type)

class Ol(Elem):
    def __init__(self, content=None, attr=None, tag_type='double' ):
        super().__init__(tag='ol', attr=attr, content=content, tag_type=tag_type)

class Li(Elem):
    def __init__(self, content=None, attr=None, tag_type='double' ):
        super().__init__(tag='li', attr=attr, content=content, tag_type=tag_type)

class H1(Elem):
    def __init__(self, content=None, attr=None, tag_type='double' ):
        super().__init__(tag='h1', attr=attr, content=content, tag_type=tag_type)

class H2(Elem):
    def __init__(self, content=None, attr=None, tag_type='double' ):
        super().__init__(tag='h2', attr=attr, content=content, tag_type=tag_type)

class P(Elem):
    def __init__(self, content=None, attr=None, tag_type='double' ):
        super().__init__(tag='p', attr=attr, content=content, tag_type=tag_type)

class Div(Elem):
    def __init__(self, content=None, attr=None, tag_type='double' ):
        super().__init__(attr=attr, content=content, tag_type=tag_type)

class Span(Elem):
    def __init__(self, content=None, attr=None, tag_type='double' ):
        super().__init__(tag='span', attr=attr, content=content, tag_type=tag_type)

class Hr(Elem):
    def __init__(self, content=None, attr=None, tag_type='simple' ):
        super().__init__(tag='hr', attr=attr, content=content, tag_type=tag_type)

class Br(Elem):
    def __init__(self, content=None, attr=None, tag_type='simple' ):
        super().__init__(tag='br', attr=attr, content=content, tag_type=tag_type)


if __name__ == '__main__':
    print( Html( [Head(), Body()] ) )
    print("\n\n\n")
    print(
        Html(
            [Head(
                Title(Text('"Hello ground!"'))),
            Body(
                [H1(Text('"Oh no, not again!"')),
                Img(attr={"src": "http://i.imgur.com/pfp3T.jpg"})
                ]
            )]
        ) )
    page = Html([
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
    print("\n\n\n")
    print(page)