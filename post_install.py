import os
import shutil
import sys
from colorama import Fore, Style
from subprocess import check_output
from os.path import join, exists

from utils import get_pgadmin_path, pg_admin_script_name, ROOT_DIR, pg_admin_major_version, python_path


if __name__ == '__main__':
    env_path = join(ROOT_DIR, '.venv')

    if not exists(env_path):
        sys.exit(f'{env_path}: virtual environment is not found.\n\n'
                 f'Run in terminal:\n'
                 f'python3 pre_install.py')

    # copy config_local
    pgadmin_path = get_pgadmin_path()

    if not exists(pgadmin_path):
        sys.exit(f'{pgadmin_path}: is not found. It seems that pgAdmin is not installed. Run in terminal:\npython3 pre_install.py')

    shutil.copyfile(join(ROOT_DIR, 'templates/config_local.py'), join(pgadmin_path, 'config_local.py'))

    # create run
    with open(join(ROOT_DIR, 'run.sh'), 'w') as f:
        f.write(f'{python_path} {pgadmin_path}/pgAdmin{pg_admin_major_version}.py')
        check_output(['chmod', '777', join(ROOT_DIR, 'run.sh')])

    # create alias
    if exists(f'/usr/bin/{pg_admin_script_name}'):
        os.remove(f'/usr/bin/{pg_admin_script_name}')
    check_output(['ln', '-s', join(ROOT_DIR, 'run.sh'), f'/usr/bin/{pg_admin_script_name}'])

    # create icon
    icon_path = f'/usr/share/applications/{pg_admin_script_name}.desktop'
    if exists(icon_path):
        os.remove(icon_path)

    icon_img_path = join(ROOT_DIR, 'templates/icon.png')

    pg_admin_name = f'pgAdmin {pg_admin_major_version}'
    with open(icon_path, 'w') as f:
        f.write(
            f'[Desktop Entry]\n'
            f'Name = {pg_admin_name}\n'
            f'Comment = {pg_admin_name}\n'
            f'GenericName = {pg_admin_name}\n'
            f'Keywords=DB;pgadmin;\n'
            f'Exec=/usr/bin/{pg_admin_script_name}\n'
            f'Terminal=true\n'
            f'Type=Application\n'
            f'Icon={icon_img_path}\n'
            f'Categories=Development;DB;'
        )

    print(
        f'Done! Log files, database and other local files is in ~/.pgadmin/ (it is created after login to pgAdmin).\n\n'
        f'To run pgAdmin:\n'
        f'- click icon in {Style.BRIGHT}Menu/Development/{pg_admin_name}{Style.RESET_ALL} (fast method)\n'
        f'- input in terminal: {Style.BRIGHT}{Fore.GREEN}{pg_admin_script_name}{Style.RESET_ALL}\n'
    )
