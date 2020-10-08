"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib
from os import path
from subprocess import call


# Get the long description from the README file
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

# Base application info
base_rdnn = 'com.github.hezral'
app_name = 'enigmatic'
app_id = base_rdnn + '.' + app_name
app_url = 'https://github.com/hezral/' + app_name
saythanks_url = 'https://saythanks.io/to/adihezral%40gmail.com'

# Setup file paths for data files
prefix = '/usr'
prefix_data = path.join(prefix, 'share')
install_path = path.join(prefix_data, app_id)
icon_path = 'icons/hicolor'
icon_sizes = ['16','24','32','48','64','128']
icon_scalable = prefix_data + '/icons/hicolor/scalable/apps'

# Setup install data list
# install_data = [(prefix_data + '/metainfo', ['data/' + app_id + '.appdata.xml']),
#                 (prefix_data + '/applications', ['data/' + app_id + '.desktop']),
#                 # (prefix_data + '/contractor', ['data/' + app_id + '.contract']),
#                 # (prefix_data + 'glib-2.0/schemas',['data/' + app_id + '.gschema.xml']),
#                 (install_path,['data/' + app_id + '.gresource']),
#                 (install_path,[app_name + '/application.py']),
#                 (install_path,[app_name + '/window.py']),
#                 (install_path,[app_name + '/about.py']),
#                 (install_path,[app_name + '/constants.py']),
#                 (icon_scalable,['data/icons/128/' + app_id + '.svg'])]

# Add icon data files to install data list
# for size in icon_sizes:
#     prefix_size = size + 'x' + size
#     prefix_size2x = size + 'x' + size + '@2'
#     icon_dir = path.join(prefix_data, icon_path, prefix_size, 'apps')
#     icon_dir2x = path.join(prefix_data, icon_path, prefix_size2x, 'apps')
#     icon_file = 'data/icons/' + size + '/' + app_id + '.svg'
#     file = (icon_dir, [icon_file])
#     file2x = (icon_dir2x, [icon_file])
#     install_data.append(file)
#     install_data.append(file2x)

# # Post install commands
# class PostInstallCommand(install):
#     """Post-installation for installation mode."""
#     def run(self):
#         install.run(self)
#         # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
#         prefix = '/usr'
#         datadir = path.join(prefix, 'share')

#         if not destdir:
#             print('Updating icon cache...')
#             call(['gtk-update-icon-cache', '-qtf', path.join(datadir, 'icons', 'hicolor')])
#             # print("Installing new Schemas")
#             # call(['glib-compile-schemas', path.join(datadir, 'glib-2.0/schemas')])

setup(
    name=app_name,  # Required
    license='GNU GPL3',
    version='1.0.0',  # Required
    description='Automate your file and folder management',  # Optional
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    url=app_url,  # Optional
    author='Adi Hezral',  # Optional
    author_email='hezral@gmail.com',  # Optional
    packages=[app_name],
    python_requires='>=3.6, <4',
    install_requires=[
        'six',
        'utilitybelt',
        'pyseltongue'
    ],  # Optional
    scripts=[app_id],
    # data_files=install_data,  # Optional
    # cmdclass={
    #     'install': PostInstallCommand,
    # }
)