# EMERGENCY TEMPFILE MODULE RESTORE
import sys
import os
import errno

# Basic tempfile module recreation
class TemporaryFile:
    def __init__(self, mode='w+b', buffering=-1, encoding=None, newline=None, suffix=None, prefix=None, dir=None):
        import tempfile as tf
        self._file = tf.NamedTemporaryFile(mode, buffering, encoding, newline, suffix, prefix, dir, delete=False)
        self.name = self._file.name
    
    def write(self, s):
        return self._file.write(s)
    
    def close(self):
        self._file.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc, value, tb):
        self.close()
        try:
            os.unlink(self.name)
        except:
            pass

def NamedTemporaryFile(mode='w+b', buffering=-1, encoding=None, newline=None, suffix=None, prefix=None, dir=None, delete=True):
    return TemporaryFile(mode, buffering, encoding, newline, suffix, prefix, dir)

# Save this as tempfile.py in Python's Lib directory
tempfile_code = '''
# Emergency tempfile module - basic functionality
import os
import errno

class TemporaryFile:
    def __init__(self, mode='w+b', buffering=-1, encoding=None, newline=None, suffix=None, prefix=None, dir=None):
        self.mode = mode
        self.name = "temp_emergency_file.tmp"
    
    def write(self, s):
        with open(self.name, 'wb') as f:
            f.write(s)
    
    def close(self):
        try:
            os.unlink(self.name)
        except:
            pass

def NamedTemporaryFile(mode='w+b', buffering=-1, encoding=None, newline=None, suffix=None, prefix=None, dir=None, delete=True):
    return TemporaryFile(mode, buffering, encoding, newline, suffix, prefix, dir)
'''

# Try to restore the module
try:
    lib_path = os.path.join(os.path.dirname(sys.executable), "Lib")
    tempfile_path = os.path.join(lib_path, "tempfile.py")
    
    with open(tempfile_path, 'w') as f:
        f.write(tempfile_code)
    
    print(" Emergency tempfile module restored!")
    print("Please reinstall Python properly as soon as possible.")
    
except Exception as e:
    print(f" Could not restore tempfile: {e}")
    print("Please reinstall Python from python.org")