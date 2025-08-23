import sys
import re
import datetime

print(sys.platform)
print(sys.version)
print(sys.path)
print(type(sys.path))
sys.path.insert(0,'E:\\path_test')
print(sys.path)
print(sys.modules.get('datetime'))