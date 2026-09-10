#!/usr/bin/python3
from curses.ascii import alt


class Text(str):
    """
    A Text class to represent a text you could use with your HTML elements.

    Because directly using str class was too mainstream.
    """

    def __str__(self):
        """
        Do you really need a comment to understand this method?..
        """
        result = super().__str__()
        if result == '&':
            result = result.replace('&', '&amp;')
        if result == '<':
            result = result.replace('<', '&lt;')
        if result == '>':
            result = result.replace('>', '&gt;')
        if result == '"':
            result = result.replace('"', '&quot;')
        result = result.replace('\n', '\n<br />\n')
        return result

class Elem:
    """
    Elem will permit us to represent our HTML elements.
    """
    class ValidationError(Exception):
        pass

    def render(self, depth = 0):
        self.depth = depth
        return self.__str__()

    def __init__(self, tag='div', attr=None, content=None, tag_type='double'):
        """
        __init__() method.

        Obviously.
        """
        self.tag = tag
        self.attr = attr
        self.content = []
        if type(content) == list:
            for elem in content:
               self.add_content(elem)
        elif content is not None:
            self.add_content(content)
        self.tag_type = tag_type
        self.depth = 0


    def __str__(self):
        """
        The __str__() method will permit us to make a plain HTML representation
        of our elements.
        Make sure it renders everything (tag, attributes, embedded
        elements...).
        """
        result = ''
        if self.tag_type == 'double':
            result = f'''<{self.tag}{self.__make_attr()}>{self.__make_content()}</{self.tag}>'''
        elif self.tag_type == 'simple':
            result = f'''<{self.tag} {self.__make_attr()}/>'''
        return result

    def __make_attr(self):
        """
        Here is a function to render our elements attributes.
        """
        if self.attr is None:
            return ''

        result = ''
        for pair in sorted(self.attr.items()):
            result += ' ' + str(pair[0]) + '="' + str(pair[1]) + '"'
        return result

    def __make_content(self):
        """
        Here is a method to render the content, including embedded elements.
        """

        if self.content is None or len(self.content) == 0:
            return ''

        result = '\n'
        for elem in self.content:
            if isinstance(elem, Elem):
                result += f"{'  ' * (self.depth + 1)}{elem.render(self.depth + 1)}\n"
            else:
                result += f"{'  ' * (self.depth + 1)}{elem}\n"
        return result + '  ' * self.depth

    def add_content(self, content):
        if not Elem.check_type(content):
            raise Elem.ValidationError
        if type(content) == list:
            self.content += [elem for elem in content if elem != Text('')]
        elif content != Text(''):
            self.content.append(content)

    @staticmethod
    def check_type(content):
        """
        Is this object a HTML-compatible Text instance or a Elem, or even a
        list of both?
        """
        return (isinstance(content, Elem) or type(content) == Text or
                (type(content) == list and all([type(elem) == Text or
                                                isinstance(elem, Elem)
                                                for elem in content])))


if __name__ == '__main__':
    print(Elem())
    print(
        Elem(tag='html', content=[
            Elem(tag="head", content=[
                Elem(tag="title", attr={}, content=[
                    Text('"Hello ground!"')
                ])]),
            Elem(tag="body", content=[
                Elem(tag="h1", content=[
                    Text('"Oh no, not again!"')
                ]),
                Elem(tag="img", attr={"src": "http://i.imgur.com/pfp3T.jpg"}, tag_type="simple")
            ])
        ])
    )
