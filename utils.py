import os
from os.path import join, dirname
from subprocess import check_output

from settings import PG_ADMIN_VERSION

ROOT_DIR = dirname(__file__)


def get_env_path():
    return join(ROOT_DIR, '.venv')


def _get_pg_admin_major_version():
    return PG_ADMIN_VERSION[0].replace('pgadmin', '')


pg_admin_major_version = _get_pg_admin_major_version()


def _get_pg_admin_script_name():
    return f'pgadmin{pg_admin_major_version}'


pg_admin_script_name = _get_pg_admin_script_name()


def get_pgadmin_path():
    lib_path = join(get_env_path(), 'lib')
    python_dir = check_output(['ls', lib_path]).decode('utf-8').strip()
    return join(lib_path, python_dir, 'site-packages', pg_admin_script_name)


def _get_python_path():
    return join(get_env_path(), 'bin', 'python')


python_path = _get_python_path()


def get_saved_versions():
    pip_files_for_pg_admin_dir = join(ROOT_DIR, 'pip_files_for_pg_admin')
    res = ''
    for product_name in os.listdir(pip_files_for_pg_admin_dir):
        versions = ', '.join(os.listdir(join(pip_files_for_pg_admin_dir, product_name)))
        res += f'{product_name}: {versions}\n'

    return res
