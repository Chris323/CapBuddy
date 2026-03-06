import sys, os

def get_base_dir():
    #Returns the correct base directory whether running as .exe or script.
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.abspath(".")

def get_resource_path(relative_path):
    #For read-only assets like icons — points to bundled files.
    base = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base, relative_path)

def get_writable_path(relative_path):
    #For writable locations like screenshots — points next to the .exe.
    return os.path.join(get_base_dir(), relative_path)