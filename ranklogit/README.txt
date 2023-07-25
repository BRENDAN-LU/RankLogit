--------------------------------------------------------------------------------

ranklogit only uses the standard Python library, and has no required package 
dependencies. However, it does contain a C-extension, so it requires CPython, 
and a C compiler. 

One can build the extension by manually compiling the .c file in this directory,
taking care to use the same compiler, and compiler settings, as those which
were used to build Python on your system. 

https://docs.python.org/3/extending/extending.html

You can also add further optimization flags. For example, when we compile 
ranklogit on Windows, we can successfully build an extension with MSVC, and 
/arch:AVX2, /fp:fast and /Qpar flags enabled. On our testing, these do not 
seem to affect the correctness of the model (i.e., notable floating point
errors). 

But, the default compilation settings for Python are already very performant, so 
the effect of such additional optimization flags are likely to negligible.

--------------------------------------------------------------------------------

More simply, one can install Cython; i.e. 
    'pip install Cython'

You still need the appropriate compiler installed on your system, but no longer 
need to manually compile 'things'. 

In this case, one can just invoke
    'python setup.py build_ext --inplace'
in this ranklogit directory to automatically compile a Python extension. 

In terms of compilers...for windows - install MSVC, and for Linux - install GCC. 
If, despite these, compilation issue persist, the Python docs (linked above) 
will have all the most up-to-date details.

https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html

Windows MSVC people may also want to decomment the 'extra_compile_args' argument 
in the setup.py file for some extra optimization flags, at your own risk...

--------------------------------------------------------------------------------

As of benchmarking on July 2023, using analagous Numpy methods and structures
is markedly slower, due to their clunky overhead. We can pass data into C, 
through Cython, just by manually indexing and copying the values from lists. 

If one were to deal with data, whereby the number of categories becomes large 
enough for Numpy to offer perforamance gains, it is likely that ranklogit will
be an unusable model elsewhere, as permuting such large numbers of tied ranks 
will be infeasibly slow, even at C-speed. 

--------------------------------------------------------------------------------