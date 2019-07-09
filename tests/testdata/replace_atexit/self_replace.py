import sys
import os
from iquail.helper import misc

src = sys.argv[1]
dest = sys.argv[2]

src_content = "SRC"
dest_content = "DEST"

with open(src, "w") as f:
    f.write(src_content)

with open(dest, "w") as f:
    f.write(dest_content)

misc.replace_atexit(dest, src)
