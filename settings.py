from decouple import config


class Settings:
    PROJECTS_DIR = config('PROJECTS_DIR', default='~/projects')