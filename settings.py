try:
    import local_settings
except ImportError:
    import local_settings_sample as local_settings

PG_ADMIN_VERSION = getattr(local_settings, 'PG_ADMIN_VERSION', ['pgadmin4', '5.0'])
