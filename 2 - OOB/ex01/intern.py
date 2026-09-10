class Intern:
    def __init__(self, name: str = "My name? I’m nobody, an intern, I have no name." ):
        self.Name = name

    def __str__(self): #dunder method, défini comment l'objet doit s'afficher en str
        return self.Name

    class Coffee:
        def __str__(self):
            return "This is the worst coffee you ever tasted."

    def work(self):
        raise Exception("I’m just an intern, I can’t do that...")

    def make_coffee(self):
        return self.Coffee()

if __name__ == '__main__':
    anonymous = Intern()
    mark = Intern("Mark")

    print(anonymous.__str__())
    print(mark.__str__())

    print(mark.make_coffee())
    try :
        print(anonymous.work())
    except Exception as e:
        print(e)