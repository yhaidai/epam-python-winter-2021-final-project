from setuptools import setup, find_packages

setup(
    name='Department App',
    version='1.0',
    author='Yaroslav Haidai',
    author_email='yhaidai@ukr.net',
    description='Web application to manage employees and departments using '
                'web service',
    url='https://github.com/yhaidai/epam-python-winter-2021-final-project',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask==2.0.0',
        'Flask-Classy==0.6.10',
        'Flask-Migrate==3.0.0',
        'Flask-RESTful==0.3.8',
        'Flask-SQLAlchemy==2.5.1',
        'marshmallow-sqlalchemy==0.25.0',
        'mysql-connector-python==8.0.25',
    ]
)
