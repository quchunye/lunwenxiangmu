! 简单的 Fortran 程序示例
program hello_fortran
    implicit none
    integer :: sum, i
    
    print *, 'Hello, Fortran!'
    print *, '这是一个简单的 Fortran 程序'
    
    ! 计算 1 到 10 的和
    sum = 0
    do i = 1, 10
        sum = sum + i
    end do
    
    print *, '1 到 10 的和是:', sum
end program hello_fortran