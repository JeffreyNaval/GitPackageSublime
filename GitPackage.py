import sublime, sublime_plugin, os

class GitPackageCommand(sublime_plugin.WindowCommand):

	s = None
	packageList = []

	defaultPath = "C:\\Program Files (x86)\\Git\\bin;C:\\Program Files\\Git\\bin"
	packagesPlaceholder = {"Folder Name": "git://github.com/your-repository.git"}

	def __init__(self, *args, **kwargs):
		super(GitPackageCommand, self).__init__(*args, **kwargs)
		s = sublime.load_settings('GitPackage.sublime-settings')
		if not s.has('git_path'):
			s.set('git_path',self.defaultPath)
		if not s.has('packages'):
			s.set('packages', self.packagesPlaceholder)
		sublime.save_settings('GitPackage.sublime-settings')

	def run(self, *args, **kwargs):
		self.s = sublime.load_settings('GitPackage.sublime-settings')
		self.list_packages()

	def list_packages(self):
		packages = self.s.get('packages')
		self.packageList = []

		if not packages:
			self.s.set('packages', self.packagesPlaceholder)
			sublime.save_settings('GitPackage.sublime-settings')
			packages = self.s.get('packages')

		for name, url in packages.iteritems():
			self.packageList.append([name, url])

		self.window.show_quick_panel(self.packageList,
									 self.set_package_location)

	def set_package_location(self, index):
		if (index > -1):
			git_url = self.packageList[index][1]
			folder_name = self.packageList[index][0]
			working_dir = os.path.join(sublime.packages_path(), folder_name)
			path = self.s.get('git_path')
			if not path:
				self.s.set('git_path', self.defaultPath)
				sublime.save_settings('GitPackage.sublime-settings')
				path = self.s.get('git_path')

			if os.path.exists(working_dir):
				self.window.run_command(
					'exec',
					{ 'cmd':['git','pull',git_url,'master'],
					  'working_dir':working_dir,
					  'path': path
					})
			else:
				self.window.run_command(
					'exec',
					{ 'cmd':['git','clone',git_url,folder_name],
					  'working_dir':sublime.packages_path(),
					  'path': path
					})