from setuptools import setup

'''
安装说明
python setup.py build
python setup.py install
'''

setup(
    name='PyMongoLab',
    version='1.0.1',
    packages=['task', 'util'],
    url='',
    license='MIT',
    author='favccxx',
    author_email='',
    description='A Restful project based on mongodb build with python',

    # 项目依赖
    install_requires=[
        'flask>=1.0.2',
        'flask_cors>=',
        'pymongo>=3.7.2',
        'apscheduler>=3.0.7',        
    ],
)
