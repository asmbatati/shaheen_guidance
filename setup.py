from glob import glob
import os

from setuptools import find_packages, setup

package_name = 'shaheen_guidance'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='asmbatati',
    maintainer_email='asmalbatati@hotmail.com',
    description='Rendezvous-point and guidance strategies for drone-to-drone interception.',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'interceptor = shaheen_guidance.interceptor_node:main',
            'guidance = shaheen_guidance.guidance_node:main',
        ],
    },
)
