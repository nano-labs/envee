#!/usr/bin/env python
"""Environment veriables helpers."""

import os
import json


class SmartEnvironmentDict(dict):

    def __init__(self, *args, **kwargs):
        self.parent = kwargs.pop("parent", None)
        self.variable_name = kwargs.pop("key", None)
        self.raw_value = kwargs.pop("raw_value", None)
        dict.__init__(self, *args, **kwargs)

    def __getitem__(self, key):
        value = dict.__getitem__(self, key)
        if isinstance(value, dict):
            return self.__class__(value, key=key, parent=self)
        elif isinstance(value, list):
            return SmartEnvironmentList(value, key=key, parent=self)
        return value

    def get(self, key, failover=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return failover

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)
        self._write()

    def _write(self):
        if not self.parent:
            os.environ[self.variable_name] = json.dumps(self)
        else:
            self.parent[self.variable_name] = self


class SmartEnvironmentList(list):

    def __init__(self, *args, **kwargs):
        self.parent = kwargs.pop("parent", None)
        self.variable_name = kwargs.pop("key", None)
        self.raw_value = kwargs.pop("raw_value", None)
        list.__init__(self, *args, **kwargs)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.__class__(
                [self[i] for i in xrange(*key.indices(len(self)))],
                key=self.variable_name, parent=self.parent
            )
        value = list.__getitem__(self, key)
        if isinstance(value, dict):
            return SmartEnvironmentDict(value, key=key, parent=self)
        elif isinstance(value, list):
            return self.__class__(value, key=key, parent=self)
        return value

    def _write(self):
        if not self.parent:
            os.environ[self.variable_name] = json.dumps(self)
        else:
            self.parent[self.variable_name] = self

    def __setitem__(self, key, value):
        list.__setitem__(self, key, value)
        self._write()

    def append(self, item):
        list.append(self, item)
        self._write()


class Envee:

    def all(self):
        return dict(os.environ)

    def __getattribute__(self, attr):
        try:
            return super().__getattribute__(attr)
        except AttributeError:
            value = os.getenv(attr)
            if value is not None:
                return self._magic_cast(attr, value)

    def __setattr__(self, attr, value):
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        else:
            value = str(value)
        os.environ[attr] = value

    @staticmethod
    def _magic_cast(attr, value):
        if value.lower() in ["true", "t", "1"]:
            return True
        elif value.lower() in ["false", "f", "0"]:
            return False
        elif value.lower() in ["null", "none"]:
            return None

        elif value.isdigit():
            return int(value)

        try:
            return float(value)
        except ValueError:
            pass

        try:
            data = json.loads(value)
            if isinstance(data, dict):
                return SmartEnvironmentDict(data, raw_value=value, key=attr)
            if isinstance(data, list):
                return SmartEnvironmentList(data, key=attr)

        except json.JSONDecodeError:
            pass

        return value


envee = Envee()
