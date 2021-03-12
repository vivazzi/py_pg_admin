import os
import shutil
import sys
import getopt
from colorama import Fore, Style
from os.path import join, exists

from settings import PG_ADMIN_VERSION
from utils import python_path, ROOT_DIR, pg_admin_major_version, get_saved_versions, get_env_path, pg_admin_script_name


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def _get_python_version():
    # try get version from Pipfile
    with open(join(ROOT_DIR, 'Pipfile')) as f:
        for line in f:
            line.strip()
            if line.startswith('python_version'):
                parts = line.strip().split(' ')
                if len(parts) >= 3:
                    version = parts[2].replace('"', '')
                    version_parts = version.split('.')
                    if len(version_parts) >= 2:
                        return f'{version_parts[0]}.{version_parts[1]}'

    return '[python_version]'


def get_pgadmin_path_from_pipfile():
    lib_path = join(get_env_path(), 'lib')

    return join(lib_path, f'python{_get_python_version()}', 'site-packages', pg_admin_script_name)


if __name__ == '__main__':
    try:
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'h',
                                       ['help', ])

        except getopt.error as msg:
            raise Usage(msg)

        for p, v in opts:
            if p in ('-h', '--help'):
                print(
                    f'--- pgAdmin pre-install ---\n\n'
                    f'In local_settings.py you can set PG_ADMIN_VERSION (now is {PG_ADMIN_VERSION})\n'
                    f'You can use saved versions : {get_saved_versions()}\n\n'
                    f'See detail documentation in README.md'
                )
                exit(0)
            else:
                assert False, '("{}", "{}"): unhandled option'.format(p, v)

        env_path = get_env_path()

        print(f'--- pgAdmin pre-install  ---\n\n'
              f'Run steps:\n')

        print(f'1. To install packages, input in terminal:\n'
              f'{Style.BRIGHT}{Fore.GREEN}pipenv sync{Style.RESET_ALL}\n')

        if not exists(env_path):
            os.makedirs(env_path)

        if not exists(join(ROOT_DIR, 'Pipfile')):
            # copy Pipfile according to PG_ADMIN_VERSION
            pip_files_for_pg_admin_dir = join(ROOT_DIR, 'pip_files_for_pg_admin')
            pg_admin_version_dir = join(pip_files_for_pg_admin_dir, PG_ADMIN_VERSION[0], PG_ADMIN_VERSION[1])
            if not exists(pg_admin_version_dir):
                print(f'{Fore.RED}There is not Pipfile for pgAdmin version {Style.BRIGHT}{PG_ADMIN_VERSION[0]}: {PG_ADMIN_VERSION[1]}{Style.NORMAL}.\n\n'
                      f'Choose saved PG_ADMIN_VERSION for settings.py:\n{get_saved_versions()}\n'
                      f'Or create new Pipfile with specified pgAdmin version. '
                      f'Look at available wheel version at https://ftp.postgresql.org/pub/pgadmin/. '
                      f'See docs how create Pipfile at https://github.com/vivazzi/py_pg_admin\n'
                      f'Pipfile examples: {pip_files_for_pg_admin_dir}{Style.RESET_ALL}')

                sys.exit(1)

            shutil.copyfile(join(pip_files_for_pg_admin_dir, PG_ADMIN_VERSION[0], PG_ADMIN_VERSION[1], 'Pipfile'), join(ROOT_DIR, 'Pipfile'))
            shutil.copyfile(join(pip_files_for_pg_admin_dir, PG_ADMIN_VERSION[0], PG_ADMIN_VERSION[1], 'Pipfile.lock'), join(ROOT_DIR, 'Pipfile.lock'))
        else:
            print(f'{Fore.YELLOW}WARNING: It is used existed Pipfile and set parameter '
                  f'PG_ADMIN_VERSION == {PG_ADMIN_VERSION} can be different from the parameter in Pipfile. '
                  f'Make sure that your Pipfile contains pgAdmin package.{Style.RESET_ALL}\n')

        pgadmin_path = get_pgadmin_path_from_pipfile()
        print(f'2. To set your pgAdmin, input in terminal and follow instructions:\n'
              f'{Style.BRIGHT}{Fore.GREEN}{python_path} {Style.BRIGHT}{Fore.GREEN}{pgadmin_path}/setup.py{Style.RESET_ALL}\n')

        print(f'After setup you can run pgAdmin in terminal:\n'
              f'{python_path} {pgadmin_path}/pgAdmin{pg_admin_major_version}.py\n'
              f'But go step 3 for create terminal command and icon.\n')

        print(f'3. Run in terminal:\n'
              f'{Style.BRIGHT}{Fore.GREEN}sudo python3 post_install.py{Style.RESET_ALL}\n')

    except Usage as err:
        print(err.msg, file=sys.stderr)
        print('for help use --help', file=sys.stderr)
