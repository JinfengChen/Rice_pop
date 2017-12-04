import os
for i in range(3907573, 3907603):
    cmd = 'qdel %s.torque.int' %(i)
    os.system(cmd)
    print cmd
