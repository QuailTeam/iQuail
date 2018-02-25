from quail.FtpSolution import FtpSolution
from quail.LocalSolution import LocalSolution
import os

s = FtpSolution('mafreebox.freebox.fr', 21, 'Disque dur','autres', 'OpenHardwareMonitor')
# s = LocalSolution('OpenHardwareMonitor')
s.open()

for x in s.walk():
    print(x)

s.get_file(os.path.join("tructest\\subdir", "test.txt"))

print(s._tmpdir)
