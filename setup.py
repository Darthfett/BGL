'''
Install with `python -m pip install ./BGL`
'''
from distutils.core import setup

setup(name='BoardGameLibrary',
      version='0.0.1',
      description='Board Game Library',
      author='Casey Kuball',
      author_email='darthfett@gmail.com',
      packages=[
        'bgl',
        'samples',
        'samples.Monopoly'
      ],
      install_requires=[
        'pyglet>=1.2.3',
        'docopt>=0.6.2',
        # Install pydotplus instead?
        # 'pydot2>=1.0.33', # Install here: https://github.com/nlhepler/pydot.git
      ],
     )