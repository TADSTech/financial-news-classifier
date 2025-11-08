from setuptools import setup, find_packages

setup(
    name='financial-news-classifier',
    version='0.1.0',
    description='Classify sentiment of financial news using transformers',
    author='TADS Tech',
    author_email='info@tads-tech.com',
    url='https://github.com/TADSTech/financial-news-classifier',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'torch>=1.13.0',
        'transformers>=4.25.0',
        'huggingface-hub>=0.13.0',
        'pandas>=1.3.0',
        'scikit-learn>=1.0.0',
        'typer>=0.9.0',
        'rich>=13.0.0',
        'gradio>=3.50.0',          # Gradio web interface
        'feedparser>=6.0.0',
        'tqdm>=4.60.0',
        'python-dotenv>=0.19.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'black>=22.0.0',
            'flake8>=4.0.0',
        ],
        'gpu': [
            'torch[cuda]>=1.13.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'fnc=cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Text Processing :: Linguistic',
    ],
    python_requires='>=3.10',
    project_urls={
        'Bug Reports': 'https://github.com/TADSTech/financial-news-classifier/issues',
        'Documentation': 'https://github.com/TADSTech/financial-news-classifier#readme',
    },
)