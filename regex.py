import doctest, pep8


class Regex_Tree:
    """Skeleton of all regex classes, designed so that our
    other classes only require a slightly modified init method.

    Precondition: It is assumed that that the Tree will have a maximum
    arity of 2. It is possible to create a subclass where this isn't the
    case, but you would have to overwrite the __repr__ and __str__ methods.
    """

    def __init__(self: 'Regex_Tree', children: list=None,
                       value: object=None, name: str="Regex Tree"):
        """Create a node with value and any number of children."""
        self.__name = name  # allows for easy repr inheritance
        self.__value = value
        if not children:
            #we need to put an empty string in the list so that our repr
            #method doesn't cause exceptions.
            self.__children = ['']
        else:
            self.__children = children[:]

    @property
    def name(self) -> str:
        """Returns the name of the tree.

        >>> test = Regex_Tree()
        >>> test.name
        'Regex Tree'
        """
        return self.__name

    @property
    def value(self) -> object:
        """Returns the value of the node.

        >>> test = Regex_Tree([],'.')
        >>> test.value
        '.'
        """
        return self.__value

    @property
    def children(self) -> list:
        """Returns a list of the tree children.

        >>> test = Regex_Tree(["1", "2"], '.')
        >>> test.children
        ['1', '2']
        """
        return self.__children

    def __repr__(self: 'Regex_Tree') -> str:
        """Return representation of Regex Tree that can be copied and
        pasted into the console to create an identical regex.

        >>> test = Regex_Tree(["1", "2"], '.')
        >>> test
        Regex Tree(['1', '2'])
        """
        return "{0}({1})".format(self.name, repr(self.children))

    def __str__(self: 'Regex_Tree') -> str:
        """
        Returns string form of the Regex.

        >>> test = Regex_Tree(['1','2'], '+')
        >>> print(test)
        (1+2)
        >>> test2 = Regex_Tree([test], '-')
        >>> print(test2)
        (1+2)-
        """
        #Checking for length allows the str method to be inherited
        if len(self.children) == 2:
            return "({0}{1}{2})".format(str(self.children[0]),
                                        self.value, str(self.children[1]))
        elif len(self.children) == 1:
            return str(self.children[0]) + str(self.value)
        else:
            #We should only end up here if someone made an invalid regex.
            raise ImproperFormatException

    def __contains__(self: 'Regex_Tree', value: object) -> bool:
        """True if the specified value exists in our regex.

        >>> test = Regex_Tree(['1','2'], '+')
        >>> '2' in test
        True
        >>> 'e' in test
        False
        """
        return (self.value == value or
                any([value in t for t in self.children]))

    def __eq__(self: "Regex_Tree", other: "Regex_Tree") -> bool:
        """
        True if a tree matches another tree.

        >>> test = Regex_Tree(['1','2'], '+')
        >>> test2 = Regex_Tree(['1','2'], '+')
        >>> test == test2
        True
        >>> test3 = Regex_Tree(['2','1'], '+')
        >>> test == test3
        False
        """
        if self.children == other.children and self.value == other.value:
            return True
        return False


class Star(Regex_Tree):

    def __init__(self: "Tree", children: list=None,
                 value: str="*", name: str="Star"):
        """
        Initializes a Star regex.

        >>> star = Star(["1"])
        >>> star
        Star(['1'])
        >>> print(star)
        1*
        """
        super().__init__(children, value, name)


class Bar(Regex_Tree):

    def __init__(self: "Bar", children: list=None,
                 value: str="|", name: str="Bar"):
        """
        Initializes a Line regex.

        >>> bar = Bar(["1", "2"])
        >>> bar
        Bar(['1', '2'])
        >>> print(bar)
        (1|2)
        """
        super().__init__(children, value, name)


class Dot(Regex_Tree):

    def __init__(self: "Dot", children: list=None,
                 value: str=".", name: str="Dot"):
        """
        Initializes a Dot regex.

        >>> dot = Dot(["1", "2"])
        >>> dot
        Dot(['1', '2'])
        >>> print(dot)
        (1.2)
        """
        super().__init__(children, value, name)


class ImproperFormatException(Exception):
    pass

if __name__ == '__main__':
    doctest.testmod(verbose=True)
