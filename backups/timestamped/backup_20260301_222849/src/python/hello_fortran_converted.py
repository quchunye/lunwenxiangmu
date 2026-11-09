#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Converted from Fortran code
Conversion time: 2026-03-01 20:25:25
"""

    #  简单的 Fortran 程序示例
def main():  # Converted from Fortran program hello_fortran
# Converted from "implicit none" - Python handles variables dynamically
    # Converted from: integer :: sum, i

    print('Hello, Fortran!')
    print('这是一个简单的 Fortran 程序')

    #  计算 1 到 10 的和
    sum = 0
    for i in range(1, 11):
        sum = sum + i

    print('1 到 10 的和是:', sum)
    pass

if __name__ == "__main__":
    main()