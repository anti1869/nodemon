from setuptools import setup, find_packages


def readme():
    with open('README.rst', 'r') as f:
        return f.read()


version = __import__('nodemon').get_version()

setup(
    name='nodemon',
    version=version,
    description='Webservice node monitoring tool',
    long_description=readme(),
    url='https://github.com/anti1869/nodemon',
    author='Dmitry Litvinenko',
    author_email='anti1869@gmail.com',
    packages=['nodemon', 'nodemon.groups', 'nodemon.web'],
    scripts=['nodemon/bin/monitor.py'],
    include_package_data=True,
    install_requires=[
        'mysqlclient',
        'web.py>=0.37',
    ],
    license='MIT',
    zip_safe=False)

print "************************************************************"
print "Hey, type 'monitor.py --install' to do initial configuration"
print "************************************************************"