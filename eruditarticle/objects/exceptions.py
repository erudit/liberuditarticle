class LiberuditarticleError(Exception):
    """Base exception for liberuditarticle"""
    pass


class MissingXMLElementError(LiberuditarticleError):
    """Raised when missing element from xml tree"""
    def __init__(self, element_name):
        self.element_name = element_name
        super().__init__("The element '%s' could not be found in the xml tree" % self.element_name)


class InvalidTypercError(LiberuditarticleError):
    """Raised when invalid type of redacteurchef (typerc) is found"""
    def __init__(self, message=None):
        self.message = message
        if message is None:
            self.message = "Invalid value for the typerc argument"
        super().__init__(self.message)


class InvalidOrdseqError(LiberuditarticleError):
    """Raised when invalid ordering number (ordseq) is found"""
    def __init__(self, message=None):
        self.message = message
        if message is None:
            self.message = "Invalid value for the ordseq xml element attribute"
        super().__init__(self.message)


class InvalidTitleLevelError(LiberuditarticleError):
    """Raised when invalid title level is found"""
    def __init__(self, message=None):
        self.message = message
        if message is None:
            self.message = "Invalid value for the title level"
        super().__init__(self.message)
