# Pytest needs an __init__.py file in this directory and in the parent directory.
# However, it's not possible to have an __init__.py file in the parent directory because
# `alibi-detect` is not a valid package name.
# Therefore, to avoid pytest name clashes with other packages, we renamed this directory
# from `test` to `tests_alibi_explain`.
