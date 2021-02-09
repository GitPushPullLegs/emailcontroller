from setuptools import setup


setup(
    name='emailcontroller',
    version='0.0.3',
    description='A python library to facilitate email sending and reading.',
    url='https://github.com/GitPushPullLegs/emailcontroller',
    author='Joe Aguilar',
    author_email='jose.aguilar.6694@gmail.com',
    license='GNU General Public License',
    packages=['emailcontroller'],
    install_requires=['imapclient', 'pyzmail36'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Windows',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)