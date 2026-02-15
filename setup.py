"""
Setup script for the sudoku-solver package.
"""

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import os
import sys
import platform


class BuildSharedLib(build_ext):
    """Custom build command to compile the C shared library."""
    
    def run(self):
        """Build the shared library using make."""
        import subprocess
        
        # Build the shared library
        try:
            subprocess.check_call(['make', 'lib'])
        except subprocess.CalledProcessError as e:
            sys.stderr.write(f"Failed to build shared library: {e}\n")
            sys.exit(1)
        
        # Continue with normal extension building
        super().run()
    
    def get_outputs(self):
        """Return the list of files built by this command."""
        outputs = super().get_outputs()
        
        # Add the shared library to the outputs
        system = platform.system()
        if system == 'Windows':
            lib_name = 'libsudoku.dll'
        elif system == 'Darwin':
            lib_name = 'libsudoku.dylib'
        else:
            lib_name = 'libsudoku.so'
        
        lib_path = os.path.join(self.build_lib, lib_name)
        outputs.append(lib_path)
        return outputs


# Read the long description from README
def read_long_description():
    """Read the long description from README.md."""
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ""


setup(
    name='sudoku-solver',
    version='1.0.0',
    author='Hugo Penedones',
    author_email='hpenedones@gmail.com',
    description='A fast sudoku solver using constraint propagation and backtracking',
    long_description=read_long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/hpenedones/sudoku',
    packages=['sudoku', 'sudoku_solver'],
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Games/Entertainment :: Puzzle Games',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: C',
    ],
    keywords='sudoku solver puzzle constraint-propagation backtracking',
    
    # Include the shared library as package data
    package_data={
        '': ['*.so', '*.dylib', '*.dll', 'sudoku.h'],
    },
    include_package_data=True,
    
    # Custom build command
    cmdclass={
        'build_ext': BuildSharedLib,
    },
    
    # Minimal extension to trigger build_ext
    ext_modules=[],
    
    # Project URLs
    project_urls={
        'Bug Reports': 'https://github.com/hpenedones/sudoku/issues',
        'Source': 'https://github.com/hpenedones/sudoku',
    },
)
