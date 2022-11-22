import sys, os, os.path, re, shutil, string
from distutils.core import setup, Command
from distutils.command.build import build
from distutils.command.install import install
from distutils.spawn import spawn
from glob import glob

systems = \
{
  'T0WmaDataSvc':
  {
    'python': ['T0WmaDataSvc'],
    'data': [],
    'bin': []
  }
}

def get_relative_path():
  return os.path.dirname(os.path.abspath(os.path.join(os.getcwd(), sys.argv[0])))

def define_the_build(self, dist, system_name, patch_x = ''):
  # Expand various sources.
  docroot = "doc/build/html"
  system = systems[system_name]
  datasrc = sum((glob("src/%s" % x) for x in system['data']), [])
  binsrc = sum((glob("bin/%s" % x) for x in system['bin']), [])

  # Specify what to install. We don't use build_ext to build extension,
  # as we have a makefile to build all the rest above anyway. Any c++
  # products we built go into data_files as python just needs to copy them.
  # Headers get special handling, we map them automatically to directories.
  py_version = (string.split(sys.version))[0]
  pylibdir = '%slib/python%s/site-packages' % (patch_x, py_version[0:3])
  dist.py_modules = ['T0WmaDataSvc.__init__']
  dist.packages = system['python']
  dist.data_files = [('%sbin' % patch_x, binsrc)]
  for dir in set(x[4:].rsplit('/', 1)[0] for x in datasrc):
    files = [x for x in datasrc if x.startswith('src/%s/' % dir)]
    dist.data_files.append(('%sdata/%s' % (patch_x, dir), files))
  if os.path.exists(docroot):
    for dirpath, dirs, files in os.walk(docroot):
      dist.data_files.append(("%sdoc%s" % (patch_x, dirpath[len(docroot):]),
                              ["%s/%s" % (dirpath, fname) for fname in files
                               if fname != '.buildinfo']))

class BuildCommand(Command):
  """Build python modules for a specific system."""
  description = \
    "Build python modules for the specified system. The only system possible\n" + \
    "\t\t   at the moment is 'T0WmaDataSvc'. Use with --force to ensure a clean\n" + \
    "\t\t   build of only the requested parts.\n"
  user_options = build.user_options
  user_options.append(('system=', 's', 'build the specified system (default: T0WmaDataSvc)'))
  user_options.append(('skip-docs', None, 'skip documentation'))

  def initialize_options(self):
    self.system = "T0WmaDataSvc"
    self.skip_docs = False

  def finalize_options(self):
    if self.system not in systems:
      print("System %s unrecognised, please use '-s T0WmaDataSvc'" % self.system)
      sys.exit(1)

    # Expand various sources and maybe do the c++ build.
    define_the_build(self, self.distribution, self.system, '')

    # Force rebuild.
    shutil.rmtree("%s/build" % get_relative_path(), True)
    shutil.rmtree("doc/build", True)

  def generate_docs(self):
    if not self.skip_docs:
      os.environ["PYTHONPATH"] = "%s/build/lib:%s" % (os.getcwd(), os.environ["PYTHONPATH"])
      spawn(['make', '-C', 'doc', 'html', 'PROJECT=%s' % "."]) #self.system.lower()])

  def run(self):
    command = 'build'
    if self.distribution.have_run.get(command): return
    cmd = self.distribution.get_command_obj(command)
    cmd.force = self.force
    cmd.ensure_finalized()
    cmd.run()
    self.generate_docs()
    self.distribution.have_run[command] = 1

class InstallCommand(install):
  """Install a specific system."""
  description = \
    "Install a specific system, either 'T0WmaDataSvc'. You can patch an existing\n" + \
    "\t\t   installation instead of normal full installation using the '-p' option.\n"
  user_options = install.user_options
  user_options.append(('system=', 's', 'install the specified system (default: T0WmaDataSvc)'))
  user_options.append(('patch', None, 'patch an existing installation (default: no patch)'))
  user_options.append(('skip-docs', None, 'skip documentation'))

  def initialize_options(self):
    install.initialize_options(self)
    self.system = "T0WmaDataSvc"
    self.patch = None
    self.skip_docs = False

  def finalize_options(self):
    # Check options.
    if self.system not in systems:
      print("System %s unrecognised, please use '-s T0WmaDataSvc'" % self.system)
      sys.exit(1)
    if self.patch and not os.path.isdir("%s/xbin" % self.prefix):
      print("Patch destination %s does not look like a valid location." % self.prefix)
      sys.exit(1)

    # Expand various sources, but don't build anything from c++ now.
    define_the_build(self, self.distribution, self.system, (self.patch and 'x') or '')

    # Whack the metadata name.
    self.distribution.metadata.name = self.system
    assert self.distribution.get_name() == self.system

    # Pass to base class.
    install.finalize_options(self)

    # Mangle paths if we are patching. Most of the mangling occurs
    # already in define_the_build(), but we need to fix up others.
    if self.patch:
      self.install_lib = re.sub(r'(.*)/lib/python(.*)', r'\1/xlib/python\2', self.install_lib)
      self.install_scripts = re.sub(r'(.*)/bin$', r'\1/xbin', self.install_scripts)

  def run(self):
    for cmd_name in self.get_sub_commands():
      cmd = self.distribution.get_command_obj(cmd_name)
      cmd.distribution = self.distribution
      if cmd_name == 'install_data':
        cmd.install_dir = self.prefix
      else:
        cmd.install_dir = self.install_lib
      cmd.ensure_finalized()
      self.run_command(cmd_name)
      self.distribution.have_run[cmd_name] = 1

setup(name = 't0wmadatasvc',
      version = '1.0',
      maintainer_email = 'hn-cms-webInterfaces@cern.ch',
      cmdclass = { 'build_system': BuildCommand,
                   'install_system': InstallCommand },
      package_dir = { 'T0WmaDataSvc': 'src/python' })
