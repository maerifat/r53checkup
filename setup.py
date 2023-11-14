from setuptools import setup, find_packages


VERSION = '1.2.34'
DESCRIPTION = 'Checkup all route53 records distributed across yours accounts in aws org.'
LONG_DESCRIPTION = 'This python tool collects DNS records from AWS Route53 across multiple accounts using AWS SSO (Single Sign-On) and provides various options for listing, filtering, storing and analyzing the data.'

# Setting up
setup(
    name="r53checkup",
    version=VERSION,
    author="maerifat (Maerifat Majeed)",
    author_email="<maerifat@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['termcolor', 'boto3', 'openpyxl', 'ipaddress', 'dnspython'],
    keywords=['python', 'route53', 'excel', 'sso', 'aws', 'aws org', 'subdomains', 'dangling' , 'certificates'],
    entry_points={
        'console_scripts': [
            'r53checkup = scripts.r53checkup:main',
        ],
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

