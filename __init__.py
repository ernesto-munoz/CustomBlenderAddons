import sys
import importlib

bl_info = {
    'name': 'AoKumai',
    'category': 'All',
    'version': (0, 0, 1),
    'blender': (2, 79, 0)
}

modules_names = [
    'lorenz_attractor_operator'
]


modules_full_names = {}
for current_module_name in modules_names:
    modules_full_names[current_module_name] = ('{}.{}'.format(__name__, current_module_name))

for current_module_full_name in modules_full_names.values():
    if current_module_name in sys.modules:
        importlib.reload(sys.modules[current_module_name])
    else:
        globals()[current_module_full_name] = importlib.import_module(current_module_full_name)
        setattr(globals()[current_module_full_name], 'modules_names', modules_full_names)

def register():
    for current_module_name in modules_full_names.values():
        if current_module_name in sys.modules:
            if hasattr(sys.modules[current_module_name], 'register'):
                sys.modules[current_module_name].register()

def unregister():
    for current_module_name in modules_full_names.values():
        if current_module_name in sys.modules:
            if hasattr(sys.modules[current_module_name], 'unregister'):
                sys.modules[current_module_name].unregister()

if __name__ == '__main__':
    register()