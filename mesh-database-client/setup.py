from setuptools import setup

setup(
   name='mesh_database_client',
   version='1.0',
   license='MIT',
   description='Conects to NYC Mesh install database',
   author='Andy Baumgar & Andrew Dickinson',
   author_email='support@nycmesh.net',
   url = 'https://github.com/nycmeshnet/nycmesh-support-bot',
   packages=['mesh_database_client'],
   install_requires=["google_api_python_client","google_auth_oauthlib","googlemaps","numpy","pandas","python-dotenv"],
   classifiers=[
   'Development Status :: 4 - Beta',
   'Intended Audience :: Developers',
   'Topic :: Software Development :: Build Tools',
   'License :: OSI Approved :: MIT License',
   'Programming Language :: Python :: 3',
   ],
)