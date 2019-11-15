from setuptools import setup

setup(
    name='puppetsshfp',
    version='0.1.1',
    description='Toolie for bridging Puppet SSHFP records into PowerDNS.',
    author='Olivier van der Toorn',
    author_email='oliviervdtoorn@gmail.com',
    packages=['puppetsshfp'],
    install_requires=['python-powerdns', 'pypuppetdb'],
)
