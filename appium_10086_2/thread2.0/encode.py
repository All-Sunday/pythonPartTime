# @Description: TODO
# @Author https://github.com/All-Sunday All-Sunday
# @Time 2022/6/7 21:20
# @File : encode.py
from distutils.core import setup
from Cython.Build import cythonize

setup(
    # 注意这里推荐使用相对路径，编译出的so文件在引用其他模块时可能会出现路径问题
    # ext_modules=cythonize("license.py")
    # ext_modules=cythonize("seleninm.py")
    ext_modules=cythonize("pandts.py")
)
