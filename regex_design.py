import doctest, pep8


class Regex_Tree:
    """Skeleton of all regex classes, designed so that our
    other classes only require a slightly modified init method.

    Preconditions:
        - Maximum arity is 2
        - Children are only '0', '1', '2', 'e', or another valid Regex_Tree.
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
        #repr self.children works recursively if self.children contains
        #another Regex_Tree
        return "{0}({1})".format(self.name, repr(self.children))

##    def __str__(self: 'Regex_Tree') -> str:
##        """
##        Returns string form of the Regex.
##
##        >>> test = Regex_Tree(['1','2'], '+')
##        >>> print(test)
##        (1+2)
##        >>> test2 = Regex_Tree([test], '-')
##        >>> print(test2)
##        (1+2)-
##        """
##        #Checking for length allows the str method to be inherited
##        if len(self.children) == 2:
##            return "({0}{1}{2})".format(str(self.children[0]),
##                                        self.value, str(self.children[1]))
##        elif len(self.children) == 1:
##            return str(self.children[0]) + str(self.value)
##        else:
##            #We should only end up here if someone made an invalid regex.
##            raise ImproperFormatException

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
        #This works recursively if self.children and/or other.children
        #contains additional Regex_Trees
        if self.children == other.children and self.value == other.value:
            return True
        return False

#All three of the next classes are designed to simply be specific instances
#of Regex_Tree, keeping in mind that when string comparison time comes, they
#will need to have different properties.

class Star(Regex_Tree):
    """
    Precondition: Only contains 1 child.
    """

    def __init__(self: "Tree", children: list,
                 value: str="*", name: str="Star"):
        """
        Initializes a Star regex.

        >>> star = Star(["1"])
        >>> star
        Star(['1'])
        """
        super().__init__(children, value, name)


class Bar(Regex_Tree):

    """
    Precondition: Contains 2 Children
    """

    def __init__(self: "Bar", children: list,
                 value: str="|", name: str="Bar"):
        """
        Initializes a Line regex.

        >>> bar = Bar(["1", "2"])
        >>> bar
        Bar(['1', '2'])
        """
        super().__init__(children, value, name)


class Dot(Regex_Tree):

    """
    Precondition: Contains 2 children.
    """

    def __init__(self: "Dot", children: list,
                 value: str=".", name: str="Dot"):
        """
        Initializes a Dot regex.

        >>> dot = Dot(["1", "2"])
        >>> dot
        Dot(['1', '2'])
        """
        super().__init__(children, value, name)


class ImproperFormatException(Exception):
    pass

if __name__ == '__main__':
    doctest.testmod(verbose=True)
