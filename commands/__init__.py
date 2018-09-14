import os


def _get_submodules():
    parts = __name__.split('.')
    result = ''

    for i in range(len(parts) - 1):
        result += parts[i] + '.'

    return result


__all__ = [os.path.splitext(f)[0] for f in os.listdir(os.path.dirname(__file__)) if
           not f.startswith('__') and f != os.path.basename(__file__) and f.endswith(".py")]


def get_all_commands():
    raise NotImplemented
