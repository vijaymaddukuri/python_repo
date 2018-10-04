import pexpect
import sys

#child = pexpect.fdpexpect.fdspawn('dir')
child = pexpect.spawn('ftp 10.0.12.18')
child.expect('Name .*:')
child.sendline('vijay')
child.expect('Password:')
child.sendline('vijay',timeout=120)
i=child.expect(['Login or password incorrect!','ftp>'])

if i==0:
    print "invalid password"
    child.kill(0)
elif i==1:
    child.sendline('ls')
child.expect('ftp>')
print child.after

child.sendline('ls')

child.expect('ftp>')
print child.before
#child.interact()