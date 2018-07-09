from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='dewiktionaryparser',
      version='1.1.1',
      description='A Python library for parsing data from the German wiktionary',
      long_description=readme(),
      author='Zsofia Gyarmathy and Karoly Varasdi',
      author_email='gyarmathy.varasdi@gmail.com',
      url='https://github.com/karoly-varasdi/de-wiktionary-parser',
      classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Scientific/Engineering",
        ),
      license='GPLv3',
      data_files = [("dewiktionaryparser_docs", ["LICENSE", "README.md", "LIESMICH.md", "src/sample_script.py"]),
                    ("dewiktionaryparser_docs/docs", ["docs/help_dictionaries.md", "docs/help_python_modules.md", "docs/hilfe_worterbucher.md"])],
      package_dir = {'': 'src'},
      packages=['dewiktionaryparser'],
      install_requires=['ujson', 'prettytable'],
      setup_requires=['ujson', 'prettytable'],
      zip_safe=False)