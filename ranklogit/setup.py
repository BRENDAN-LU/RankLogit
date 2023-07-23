from setuptools import Extension, setup
from Cython.Build import cythonize

extensions = [
    Extension(
        "_utils",
        sources=["_utils.pyx", "src/sigmapermute.c"],
        language="c",
        extra_compile_args=["/arch:AVX2", "/fp:fast", "/Qpar"],
    )
]

setup(
    ext_modules=cythonize(
        extensions,
        compiler_directives={"language_level": "3"},
    )
)
