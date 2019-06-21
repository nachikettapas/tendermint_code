from abc import ABCMeta, abstractmethod

class LogOperation:
        __metaclass__ = ABCMeta

        @abstractmethod
        def createLog(self, _id, _senderpk, _receiverpk, _data):
                pass

        @abstractmethod
        def queryLog(self, _id, _senderpk=None, _receiverpk=None, _data=None):
                pass
