import os
import shutil
import sys
import getopt
from colorama import Fore, Style
from os.path import join, exists

from settings import PG_ADMIN_VERSION
from utils import get_pgadmin_path, python_path, pg_admin_folder, ROOT_DIR, pg_admin_major_version, get_saved_versions


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


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
                    f'Detail documentation see at README.md'
                )
                exit(0)
            else:
                assert False, '("{}", "{}"): unhandled option'.format(p, v)

        env_path = join(ROOT_DIR, '.venv')

        pgadmin_path = get_pgadmin_path(env_path, pg_admin_folder)

        print(f'--- pgAdmin pre-install  ---\n\n'
              f'Run steps:\n')

        print(f'1. To install packages, input in terminal:\n'
              f'{Style.BRIGHT}{Fore.GREEN}pipenv sync{Style.RESET_ALL}\n')

        if not exists(env_path):
            os.makedirs(env_path)

        if not exists(join(ROOT_DIR, 'Pipfile')):
            # copy Pipfile according to PG_ADMIN_VERSION
            pip_files_for_pg_admin_dir = join(ROOT_DIR, 'pip_files_for_pg_admin')
            pg_admin_version_dir = join(pip_files_for_pg_admin_dir, PG_ADMIN_VERSION)
            if not exists(pg_admin_version_dir):
                sys.exit(f'There is not Pipfile for pgAdmin version {PG_ADMIN_VERSION}.\n\n'
                         f'Choose saved PG_ADMIN_VERSION for settings.py: {get_saved_versions()}\n'
                         f'Or create new Pipfile with specified pgAdmin wheel version. '
                         f'Look at available wheel version at https://ftp.postgresql.org/pub/pgadmin/. '
                         f'See docs how create Pipfile at https://github.com/vivazzi/py_pg_admin\n'
                         f'Pipfile examples: {pip_files_for_pg_admin_dir}')

            shutil.copyfile(join(pip_files_for_pg_admin_dir, PG_ADMIN_VERSION, 'Pipfile'), join(ROOT_DIR, 'Pipfile'))
            shutil.copyfile(join(pip_files_for_pg_admin_dir, PG_ADMIN_VERSION, 'Pipfile.lock'), join(ROOT_DIR, 'Pipfile.lock'))
        else:
            print(f'{Fore.YELLOW}WARNING: It is used existed Pipfile and set parameter '
                  f'PG_ADMIN_VERSION == {PG_ADMIN_VERSION} can be different from the parameter in Pipfile. '
                  f'Be sure that your Pipfile contains pgAdmin package.{Style.RESET_ALL}\n')

        print(f'2. To set your pgAdmin, input in terminal and follow instructions:\n'
              f'{Style.BRIGHT}{Fore.GREEN}{python_path} {Style.BRIGHT}{Fore.GREEN}{pgadmin_path}/setup.py{Style.RESET_ALL}\n')

        print(f'After setup you can run pgAdmin in terminal:\n'
              f'{python_path} {pgadmin_path}/pgAdmin{pg_admin_major_version}.py\n'
              f'But go step 3 for create terminal command and icon.\n')

        print(f'3. Run in terminal:\n'
              f'{Style.BRIGHT}{Fore.GREEN}sudo python3 post_install{Style.RESET_ALL}\n')

    except Usage as err:
        print(err.msg, file=sys.stderr)
        print('for help use --help', file=sys.stderr)
