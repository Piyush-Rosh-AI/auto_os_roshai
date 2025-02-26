from setuptools import find_packages, setup

package_name = 'py_data_collection'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='roshai',
    maintainer_email='piyush.tailor@rosh.ai',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'data_collection = py_data_collection.data_collection:main',
            'data_publishing = py_data_collection.data_publishing:main',
            'make_map = py_data_collection.make_map:main',
            'vehicle_data_collection = py_data_collection.vehicle_data_collection:main',
            'vehicle_data_publishing = py_data_collection.vehicle_data_publishing:main',
        ],
    },
)
