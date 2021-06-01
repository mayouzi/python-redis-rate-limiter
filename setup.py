from setuptools import setup, find_packages


setup(
    name="redis-rate-limiter",
    version="0.1",
    description="rate limiter with Redis",
    author="mayor",
    url="https://github.com/mayouzi",
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Utilities',
    ],
    install_requires=[
        "redis>=3.5.3",
        "six>=1.16.0"
    ],
    python_requires='>=3.6',
    zip_safe=False,
)
