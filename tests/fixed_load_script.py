# pylint: skip-file
import pkg_resources


def fixed_load_script(self, command, **options):
    """Patched load_script to fix bug in pytest_console_scripts, from
       https://github.com/kvas-it/pytest-console-scripts, PR suggestion to make this
       file redundant can be found at:
       https://github.com/kvas-it/pytest-console-scripts/pull/48
    """
    entry_points = list(pkg_resources.iter_entry_points('console_scripts',
                                                        command))
    if entry_points:
        def console_script():
            s = entry_points[0].load()
            return s()

        return console_script

    script_path = self._locate_script(command, **options)

    def exec_script():
        with open(script_path, 'rt', encoding='utf-8') as script:
            compiled = compile(script.read(), str(script), 'exec', flags=0)
            exec(compiled, {'__name__': '__main__'})
        return 0

    return exec_script
