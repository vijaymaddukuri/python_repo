

import winpexpect
child = winpexpect.winspawn('ssh %s@%s' % ('root','10.100.1.1'))

