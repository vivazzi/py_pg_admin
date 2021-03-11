import os
from os.path import join, dirname
from subprocess import check_output

from settings import PG_ADMIN_VERSION

ROOT_DIR = dirname(__file__)


def get_pgadmin_path(env_path, pg_admin_dir):
    lib_path = join(env_path, 'lib')
    python_dir = check_output(['ls', lib_path]).decode('utf-8').strip()
    return join(lib_path, python_dir, 'site-packages', pg_admin_dir)


def _get_python_path():
    return check_output(['pipenv', '--py']).decode('utf-8').strip().replace('\n', '')


python_path = _get_python_path()


def _get_pg_admin_major_version():
    return PG_ADMIN_VERSION.split('.')[0]


pg_admin_major_version = _get_pg_admin_major_version()


def _get_pg_admin_folder():
    return f'pgadmin{pg_admin_major_version}'


pg_admin_folder = _get_pg_admin_folder()


def get_saved_versions():
    pip_files_for_pg_admin_dir = join(ROOT_DIR, 'pip_files_for_pg_admin')
    return ', '.join(os.listdir(pip_files_for_pg_admin_dir))
