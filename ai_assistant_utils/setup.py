from setuptools import setup, find_packages

setup(
    name="ai_assistant_utils",
    version="0.1.0",
    description="A helper library for AI web assistant tasks",
    author="Student Name",
    packages=find_packages(),
    install_requires=[
        # Add dependencies here if needed, e.g., 'google-generativeai'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
