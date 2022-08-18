import os
from shutil import copyfile
from pathlib import Path

from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem
from slugify import slugify

from settings import Settings


class SlvsWorkspaceManagerApp:
    def __init__(self, projects_dir):
        self.projects_dir = projects_dir
        self.current_project = None
        self.exit = False

    @property
    def project_dir(self) -> Path:
        return Path(f'{self.projects_dir}/{self.current_project.name}')

    def run(self):
        while True:
            menu = ConsoleMenu('Workspace Manager', show_exit_option=False)
            if self.current_project is None:
                self.make_menu_projects(menu)
            else:
                self.make_menu_files(menu)

            menu.show()
            if self.exit:
                break

    def create_project(self):
        project_name = input('Enter project name: \n>')
        project_slug = slugify(project_name)
        project_path = Path(self.projects_dir + '/' + project_slug)
        project_path.mkdir(parents=True, exist_ok=True)

    def select_project(self, project):
        self.current_project = project

    @staticmethod
    def select_file(file):
        cwd = os.getcwd()
        os.chdir(Path(file).parent)
        os.system(f'solvespace {file}')
        os.chdir(cwd)

    def scan_projects(self):
        projects = [x for x in Path(self.projects_dir).iterdir() if x.is_dir()]

        project_items = []
        for project in projects:
            item = FunctionItem(project.name,
                                self.select_project,
                                args=[project],
                                should_exit=True)
            project_items.append(item)

        return project_items

    def scan_files(self):
        files = [x for x in self.project_dir.iterdir()
                 if x.is_file() and x.suffix == '.slvs']

        file_items = []
        for file in files:
            item = FunctionItem(file.name,
                                self.select_file,
                                args=[file])
            file_items.append(item)

        return file_items

    def make_menu_projects(self, menu):
        create_project_item = FunctionItem('>>> Create Project',
                                           self.create_project,
                                           should_exit=True)
        menu.append_item(create_project_item)

        exit_item = FunctionItem('<<< Exit',
                                 self.exit_app, should_exit=True)
        menu.append_item(exit_item)

        project_items = self.scan_projects()
        for item in project_items:
            menu.append_item(item)

        return menu

    def _create_file(self):
        file_name = input('Enter file name: \n>')
        file_slug = slugify(file_name)
        file_path = self.project_dir / Path(f'{file_slug}.slvs')
        empty_file_path = Path('assets/empty.slvs')
        copyfile(empty_file_path, file_path)

    def make_menu_files(self, menu):
        create_file_item = FunctionItem('>>> Create File',
                                        self._create_file,
                                        should_exit=True)
        menu.append_item(create_file_item)

        back_to_projects_item = FunctionItem('<< Back to projects',
                                             self._back_to_projects,
                                             should_exit=True)
        menu.append_item(back_to_projects_item)

        files_items = self.scan_files()
        for item in files_items:
            menu.append_item(item)

        return menu

    def _back_to_projects(self):
        self.current_project = None

    def exit_app(self):
        self.exit = True


def main():
    app = SlvsWorkspaceManagerApp(projects_dir=Settings.PROJECTS_DIR)
    app.run()


if __name__ == '__main__':
    main()
