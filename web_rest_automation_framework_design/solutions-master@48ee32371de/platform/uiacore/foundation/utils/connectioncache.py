#  Copyright 2016 EMC GSE SW Automation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


class ConnectionCache(object):
    """Cache for alive browser connections
    customized version of robot.utils.ConnectionCache and
    Selenium2Library.utils.BrowserCache
    """

    _CONNECTIONS = {}
    _CLOSED = set()
    _CURRENT = None

    def __init__(self, alias_or_index):
        self._identifier = self._construct_unique_key(alias_or_index)

    def register(self, connection, alias_or_index=None):
        if not connection:
            raise ValueError('Invalid connection')

        ConnectionCache._CURRENT = self._identifier \
            if alias_or_index is None \
            else self._construct_unique_key(alias_or_index)

        ConnectionCache._CONNECTIONS[ConnectionCache._CURRENT] = connection

        return ConnectionCache._CURRENT

    def get_connection(self, alias_or_index):
        return ConnectionCache._CONNECTIONS.get(
            self._normalize_alias_or_index(alias_or_index))

    def switch(self, alias_or_index):
        alias_or_index = self._normalize_alias_or_index(alias_or_index)

        if alias_or_index in ConnectionCache._CONNECTIONS:
            ConnectionCache._CURRENT = alias_or_index

        return ConnectionCache._CONNECTIONS.get(ConnectionCache._CURRENT)

    def close(self, alias_or_index=None):
        alias_or_index = self._normalize_alias_or_index(
            alias_or_index) or ConnectionCache._CURRENT

        try:
            self._unregister(alias_or_index)
        except Exception as ex:
            raise ex
        finally:
            if ConnectionCache._CONNECTIONS:
                if alias_or_index == ConnectionCache._CURRENT:
                    ConnectionCache._CURRENT = ConnectionCache._CONNECTIONS.keys()[-1]
            else:
                ConnectionCache._CURRENT = None

    def close_all(self):
        [self.close(key) for key in ConnectionCache._CONNECTIONS]

        ConnectionCache._CLOSED.clear()

    @property
    def current(self):
        return ConnectionCache._CONNECTIONS.get(ConnectionCache._CURRENT)

    def _construct_unique_key(self, alias_or_index):
        alias_or_index = self._normalize_alias_or_index(alias_or_index)

        if alias_or_index in ConnectionCache._CONNECTIONS:
            try:
                self._unregister(alias_or_index)
            except:
                pass

        return alias_or_index or str(len(ConnectionCache._CONNECTIONS))

    def _normalize_alias_or_index(self, alias_or_index):
        return str(alias_or_index).strip() if alias_or_index else None

    def _unregister(self, alias_or_index):
        _conn = ConnectionCache._CONNECTIONS.get(alias_or_index)

        if _conn:
            try:
                _conn.quit()
                ConnectionCache._CLOSED.add(_conn)
            finally:
                self._dispose(alias_or_index)

    def _dispose(self, alias_or_index):
        if alias_or_index in ConnectionCache._CONNECTIONS:
            ConnectionCache._CONNECTIONS[alias_or_index] = None
            del ConnectionCache._CONNECTIONS[alias_or_index]
