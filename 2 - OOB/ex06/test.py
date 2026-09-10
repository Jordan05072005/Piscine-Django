#!/usr/bin/python3
"""
Tests pour la classe Page, réécrits pour coller strictement au cahier
des charges :

- Html : exactement un Head, puis un Body (dans cet ordre).
- Head : uniquement un Title, rien d'autre.
- Body / Div : uniquement H1, H2, Div, Table, Ul, Ol, Span, Text.
  (P n'est PAS autorisé ici — erreur dans une version précédente de
  ce fichier de tests, corrigée ci-dessous.)
- Title, H1, H2, Li, Th, Td : uniquement un unique Text.
- P : uniquement des Text.
- Span : uniquement des Text ou des P.
- Ul / Ol : au moins un Li, uniquement des Li.
- Tr : au moins un Th ou Td, uniquement des Th OU des Td (exclusif).
- Table : uniquement des Tr.
- Tout noeud dont le type n'est pas dans la liste autorisée
  (html, head, body, title, meta, img, table, th, tr, td, ul, ol,
  li, h1, h2, p, div, span, hr, br, Text) rend l'arbre invalide.

Adapte les imports au nom réel de tes modules si besoin.
"""

import os
import tempfile
import unittest

from elem import Elem, Text
from elements import (
    Html, Head, Body, Title, Meta, Img,
    Table, Th, Tr, Td,
    Ul, Ol, Li,
    H1, H2, P, Div, Span, Hr, Br,
)
from Page import Page


def build_valid_page():
    return Html([
        Head([
            Title(Text("Titre")),
        ]),
        Body(content=[
            H1(Text("Titre principal")),
            H2(Text("Sous-titre")),
            Div(content=[
                Span(Text("Un span")),
            ]),
            Ul([Li(Text("item 1")), Li(Text("item 2"))]),
            Ol([Li(Text("étape 1"))]),
            Table([
                Tr([Th(Text("Nom")), Th(Text("Âge"))]),
                Tr([Td(Text("Alice")), Td(Text("30"))]),
            ]),
            Span(Text("texte direct autorisé")),
            Text("texte brut directement dans le Body"),
        ]),
    ])


# ---------------------------------------------------------------------
# Html : exactement Head puis Body
# ---------------------------------------------------------------------
class TestCheckHtml(unittest.TestCase):
    def test_valid_head_then_body(self):
        html = Html([Head(), Body()])
        self.assertTrue(Page.check_html(html))

    def test_invalid_order_reversed(self):
        html = Html([Body(), Head()])
        self.assertFalse(Page.check_html(html))

    def test_invalid_missing_body(self):
        html = Html([Head()])
        self.assertFalse(Page.check_html(html))

    def test_invalid_extra_child(self):
        html = Html([Head(), Body(), Div()])
        self.assertFalse(Page.check_html(html))

    def test_invalid_wrong_types(self):
        html = Html([Div(), Span(Text("x"))])
        self.assertFalse(Page.check_html(html))


# ---------------------------------------------------------------------
# Head : uniquement un Title, rien d'autre
# ---------------------------------------------------------------------
class TestCheckHead(unittest.TestCase):
    def test_valid_head_with_title(self):
        head = Head([Title(Text("Titre"))])
        self.assertTrue(Page.check_head(head))

    def test_invalid_head_with_two_titles(self):
        head = Head([Title(Text("A")), Title(Text("B"))])
        self.assertFalse(Page.check_head(head))

    def test_invalid_head_with_meta(self):
        head = Head([Meta(attr={"charset": "UTF-8"})])
        self.assertFalse(Page.check_head(head))

    def test_invalid_head_with_title_and_meta(self):
        head = Head([Title(Text("Titre")), Meta(attr={"charset": "UTF-8"})])
        self.assertFalse(Page.check_head(head))


# ---------------------------------------------------------------------
# Body / Div : uniquement H1, H2, Div, Table, Ul, Ol, Span, Text
# ---------------------------------------------------------------------
class TestCheckBodyDiv(unittest.TestCase):
    def test_valid_body_allowed_types(self):
        body = Body(content=[
            H1(Text("t")), H2(Text("s")), Div(),
            Table([]), Ul([Li(Text("a"))]), Ol([Li(Text("b"))]),
            Span(Text("s")), Text("texte brut"),
        ])
        self.assertTrue(Page.check_body_div(body))

    def test_invalid_body_with_p(self):
        # P n'est PAS dans la liste autorisée pour Body/Div
        body = Body(content=[P(Text("un paragraphe"))])
        self.assertFalse(Page.check_body_div(body))

    def test_invalid_body_with_img(self):
        body = Body(content=[Img(attr={"src": "x.jpg"})])
        self.assertFalse(Page.check_body_div(body))

    def test_invalid_body_with_title(self):
        body = Body(content=[Title(Text("intrus"))])
        self.assertFalse(Page.check_body_div(body))

    def test_div_follows_same_rule_as_body(self):
        div_valid = Div(content=[Span(Text("ok"))])
        div_invalid = Div(content=[P(Text("interdit"))])
        self.assertTrue(Page.check_body_div(div_valid))
        self.assertFalse(Page.check_body_div(div_invalid))


# ---------------------------------------------------------------------
# Title, H1, H2, Li, Th, Td : uniquement un unique Text
# ---------------------------------------------------------------------
class TestCheckUniqueText(unittest.TestCase):
    def test_valid_single_text(self):
        for cls in (Title, H1, H2, Li, Th, Td):
            with self.subTest(cls=cls):
                elem = cls(Text("valeur"))
                self.assertTrue(Page.check_unique_text(elem))

    def test_invalid_multiple_text(self):
        li = Li([Text("a"), Text("b")])
        self.assertFalse(Page.check_unique_text(li))

    def test_invalid_non_text_child(self):
        th = Th([Span(Text("x"))])
        self.assertFalse(Page.check_unique_text(th))


# ---------------------------------------------------------------------
# P : uniquement des Text
# ---------------------------------------------------------------------
class TestCheckContainText(unittest.TestCase):
    def test_valid_p_single_text(self):
        p = P(Text("un paragraphe"))
        self.assertTrue(Page.check_contain_text(p))

    def test_valid_p_multiple_text(self):
        p = P([Text("phrase 1"), Text("phrase 2")])
        self.assertTrue(Page.check_contain_text(p))

    def test_invalid_p_with_span(self):
        p = P([Span(Text("x"))])
        self.assertFalse(Page.check_contain_text(p))

    def test_invalid_p_with_div(self):
        p = P([Div()])
        self.assertFalse(Page.check_contain_text(p))


# ---------------------------------------------------------------------
# Span : uniquement des Text ou des P
# ---------------------------------------------------------------------
class TestCheckSpan(unittest.TestCase):
    def test_valid_span_with_text(self):
        span = Span(Text("texte"))
        self.assertTrue(Page.check_span(span))

    def test_valid_span_with_p(self):
        span = Span([P(Text("paragraphe"))])
        self.assertTrue(Page.check_span(span))

    def test_valid_span_with_text_and_p(self):
        span = Span([Text("a"), P(Text("b"))])
        self.assertTrue(Page.check_span(span))

    def test_invalid_span_with_div(self):
        span = Span([Div()])
        self.assertFalse(Page.check_span(span))

    def test_invalid_span_with_h1(self):
        span = Span([H1(Text("intrus"))])
        self.assertFalse(Page.check_span(span))


# ---------------------------------------------------------------------
# Ul / Ol : au moins un Li, uniquement des Li
# ---------------------------------------------------------------------
class TestCheckUlOl(unittest.TestCase):
    def test_valid_ul(self):
        ul = Ul([Li(Text("a")), Li(Text("b"))])
        self.assertTrue(Page.check_ul_ol(ul))

    def test_valid_ol(self):
        ol = Ol([Li(Text("1"))])
        self.assertTrue(Page.check_ul_ol(ol))

    def test_invalid_empty_ul(self):
        ul = Ul()
        ul.content = []
        self.assertFalse(Page.check_ul_ol(ul))

    def test_invalid_ul_with_span(self):
        ul = Ul([Li(Text("a")), Span(Text("intrus"))])
        self.assertFalse(Page.check_ul_ol(ul))


# ---------------------------------------------------------------------
# Tr : au moins un Th ou Td, uniquement Th OU Td (mutuellement exclusifs)
# ---------------------------------------------------------------------
class TestCheckTr(unittest.TestCase):
    def test_valid_tr_only_th(self):
        tr = Tr([Th(Text("Nom")), Th(Text("Âge"))])
        self.assertTrue(Page.check_tr(tr))

    def test_valid_tr_only_td(self):
        tr = Tr([Td(Text("Alice")), Td(Text("30"))])
        self.assertTrue(Page.check_tr(tr))

    def test_invalid_tr_mixed_th_and_td(self):
        tr = Tr()
        tr.content = [Th(Text("Nom")), Td(Text("Alice"))]
        self.assertFalse(Page.check_tr(tr))

    def test_invalid_tr_empty(self):
        tr = Tr()
        tr.content = []
        self.assertFalse(Page.check_tr(tr))

    def test_invalid_tr_wrong_type(self):
        tr = Tr()
        tr.content = [Span(Text("a"))]
        self.assertFalse(Page.check_tr(tr))


# ---------------------------------------------------------------------
# Table : uniquement des Tr
# ---------------------------------------------------------------------
class TestCheckTable(unittest.TestCase):
    def test_valid_table(self):
        table = Table([
            Tr([Th(Text("Nom"))]),
            Tr([Td(Text("Alice"))]),
        ])
        self.assertTrue(Page.check_table(table))

    def test_valid_empty_table(self):
        # Le cahier des charges n'exige pas de minimum pour Table
        # (contrairement à Ul/Ol/Tr) : "uniquement des Tr" est
        # vrai vacuité sur une liste vide.
        table = Table([])
        self.assertTrue(Page.check_table(table))

    def test_invalid_table_with_td_directly(self):
        table = Table([Td(Text("orphelin"))])
        self.assertFalse(Page.check_table(table))

    def test_invalid_table_with_th_directly(self):
        table = Table([Th(Text("orphelin"))])
        self.assertFalse(Page.check_table(table))


# ---------------------------------------------------------------------
# __str__ et write_to_file
# ---------------------------------------------------------------------
class TestPageStr(unittest.TestCase):
    def test_str_matches_underlying_page(self):
        html = build_valid_page()
        page = Page(html)
        self.assertEqual(str(page), str(html))

    
    def test_str_has_doctype_when_root_is_html(self):
        """
        Le cahier des charges : le HTML affiché via print(page) doit
        être précédé d'un doctype SI le type de l'élément racine est
        Html. Le __str__ actuel de Page ne fait que déléguer à
        self.page.__str__() sans jamais ajouter de doctype -> ce test
        échoue avec le code fourni et sert de repère pour le corriger.
        """
        Page(build_valid_page()).write_to_file("test.html")
        with open("test.html", 'r') as f:
            file = f.read()
            self.assertTrue(str(file).startswith("<!DOCTYPE html>"))

    def test_str_no_doctype_when_root_is_not_html(self):
        page = Page(Div([Span(Text("pas une page complète"))]))
        self.assertFalse(str(page).startswith("<!DOCTYPE"))


class TestWriteToFile(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmpdir.cleanup()

    
    def test_doctype_depends_on_root_type_not_extension(self):
        """
        Cahier des charges : le doctype doit apparaître SI ET SEULEMENT
        SI la racine est un Html -- peu importe le nom/extension du
        fichier. L'implémentation fournie décide en fonction de
        l'extension du fichier ('.html'), pas du type de l'élément
        racine. Donc écrire une page Html dans un fichier ".txt"
        devrait quand même produire un doctype, ce qui échoue ici.
        """
        page = Page(build_valid_page())
        path = os.path.join(self.tmpdir.name, "page.txt")
        page.write_to_file(path)
        with open(path) as f:
            content = f.read()
        self.assertTrue(content.startswith("<!DOCTYPE html>\n"))

    
    def test_no_doctype_for_non_html_root_even_with_html_extension(self):
        """
        Même logique dans l'autre sens : une racine qui n'est pas un
        Html, écrite dans un fichier ".html", ne devrait PAS avoir de
        doctype selon le cahier des charges. L'implémentation fournie
        ajoute le doctype uniquement sur la base de l'extension, donc
        ce cas produit un doctype à tort.
        """
        page = Page(Div([Span(Text("fragment"))]))
        path = os.path.join(self.tmpdir.name, "fragment.html")
        page.write_to_file(path)
        with open(path) as f:
            content = f.read()
        self.assertFalse(content.startswith("<!DOCTYPE"))

    def test_write_produces_file_with_html_content(self):
        page = Page(build_valid_page())
        path = os.path.join(self.tmpdir.name, "test.html")
        page.write_to_file(path)
        with open(path) as f:
            content = f.read()
        self.assertIn("<html>", content)
        self.assertIn("<head>", content)
        self.assertIn("<body", content)


# ---------------------------------------------------------------------
# Rejet des types non autorisés n'importe où dans l'arbre
# ---------------------------------------------------------------------
class TestUnknownTypeRejection(unittest.TestCase):
    """
    "Si pendant le parcours de l'arbre, un noeud n'est pas de type
    html, head, body, title, meta, img, table, th, tr, td, ul, ol, li,
    h1, h2, p, div, span, hr, br ou Text, l'arbre est invalide."

    Ce comportement dépend de is_valid() (parcours de l'arbre), pas
    des check_* pris isolément. Ces tests visent is_valid() une fois
    qu'il descend récursivement dans les enfants -- adapte-les si ta
    version de is_valid() diffère.
    """

    
    def test_valid_full_page_is_valid(self):
        page = Page(build_valid_page())
        self.assertTrue(page.is_valid())

    
    def test_unknown_type_deep_in_tree_is_invalid(self):
        class FakeElem(Elem):
            def __init__(self):
                super().__init__(tag='fake', content=[Text("x")])

        broken = Html([
            Head([Title(Text("Titre"))]),
            Body(content=[Div(content=[FakeElem()])]),
        ])
        page = Page(broken)
        self.assertFalse(page.is_valid())


if __name__ == '__main__':
    unittest.main(verbosity=2)