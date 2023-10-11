import enum


class Cases(enum.StrEnum):
    Nominative = 'Именительный'
    """ Именительный """

    Genitive = 'Родительный'
    """ Родительный """

    Dative = 'Дательный'
    """ Дательный """

    Accusative = 'Винительный'
    """ Винительный """

    Instrumental = 'Творительный'
    """ Творительный """

    Prepositional = 'Предложный'
    """ Предложный """