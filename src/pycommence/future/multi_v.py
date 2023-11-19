import sys

if sys.version_info >= (3, 10):
    import pycommence.future.ge310 as pc
else:
    import pycommence.future.lt310 as pc

print(pc.api_func())
