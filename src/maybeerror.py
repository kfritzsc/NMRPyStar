
_STATUSES = set(['success', 'failure', 'error'])


class MaybeError(object):
    
    def __init__(self, status, value):
        if not status in _STATUSES:
            raise ValueError("invalid MaybeError status: %s" % status)
        self.status = status
        self.value = value
    
    def fmap(self, f):
        if self.status == 'success':
            return MaybeError('success', f(self.value))
        return self
        
    @staticmethod
    def pure(x):
        return MaybeError('success', x)
    
    def ap(self, y):
        if self.status == 'success':
            return y.fmap(self.value)
        return self
        
    def bind(self, f):
        if self.status == 'success':
            return f(self.value)
        return self
        
    @staticmethod
    def error(e):
        return MaybeError('error', e)
        
    def mapError(self, f):
        if self.status == 'error':
            return MaybeError.error(f(self.value))
        return self
        
    def plus(self, other):
        if self.status == 'failure':
            return other
        return self


MaybeError.zero = MaybeError('failure', None)