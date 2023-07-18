from setuptools import Extension, setup
from Cython.Build import cythonize

extensions = [
    Extension(
        "_utils",
        sources = ["_utils.pyx", "src/utils.c"],
        language = "c",
    )
]

setup(
    ext_modules = cythonize(
        extensions,
        compiler_directives = {"language_level": "3"}
    )
)
