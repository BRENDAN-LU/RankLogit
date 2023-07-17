from setuptools import Extension, setup
from Cython.Build import cythonize

extensions = [
    Extension(
        "test1",
        sources = ["src/_rankpermute.pyx", "src/rankpermute.c"],
        language = "c",
    )
]

setup(
    ext_modules = cythonize(
        extensions,
        compiler_directives = {"language_level": "3"}
    )
)