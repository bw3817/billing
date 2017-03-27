#----------------------------------------------------------------------
# Author:          Brian Wolf
# Date:            2009.06.16
# Module:          RowData.py
# Description:     Generic data object.
#
# Modifications:
#
#
#----------------------------------------------------------------------


from types import *


class RowData(object):
    def __init__(self, obj=None, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

        if obj.__class__.__name__ in ('RowTuple','NamedTuple','KeyedTuple'):
            self._objectify(obj)
            self.__repr__ = obj.__repr__
        elif obj.__class__.__name__ == 'RowProxy':
            self._objectify(obj)
            for item in obj.items():
                setattr(self, item[0], item[1])
        elif self._hasParentClass(obj, 'Base'):
            self._objectify(obj)
            self.__repr__ = obj.__repr__
        elif obj is DictType:
            self._dict2obj(dct)

    def _hasParentClass(self, obj, classname):
        #for cls in obj.__class__.__bases__:
        for cls in type(obj).mro():
            if cls.__name__ == classname:
                return True
        return False

    def _dict2obj(self, dct):
        for key,value in dct.items():
            setattr(self, key, value)

    def _objectify(self, obj):
        for field in dir(obj):
            value = getattr(obj, field)

            # fields types to skip
            if field[:1] == '_': continue
            if field == 'metadata': continue
            #if type(value) in (BuiltinFunctionType, BuiltinMethodType, MethodType, InstanceType): continue

            # handle these types
            if self._hasParentClass(value, 'Base'):
                self._objectify(value)
            else:
                setattr(self, field, value)
