import contextlib

class Transaction:
    def __init__(self, conn):
        self.conn = conn
        self.xid = conn._start_transaction()

    def commit(self):
        self.conn._commit_transaction(self.xid)

    def rollback(self):
        self.conn._rollback_transaction(self.xid)

@contextlib.contextmanager
def start_transaction(connection):
    tx = Transaction(connection)

    try:
        yield tx
    except:
        tx.rollback()
        raise
    tx.commit()

from training.Python_basics.context_manager import Connection

conn = Connection()
try:
    with start_transaction(conn) as tx:
        x = 1 + 1
        raise ValueError()
        y = x+2
        print('transaction 0 = ', x, y)
except ValueError:
    print('Transaction 0 failed')
# xact = Transaction(conn)
#
# xact.commit()
#
# xact.rollback()
