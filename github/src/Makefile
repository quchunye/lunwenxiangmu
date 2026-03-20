FC = ifort

all: supercell

supercell: supercell.f90 structure.o functions.o symmetry.o
	$(FC) -o supercell supercell.f90 structure.o functions.o symmetry.o

functions.o: functions.f90
	$(FC) -c functions.f90

structure.o: structure.f90 functions.o
	$(FC) -c structure.f90

symmetry.o: symmetry.f90 functions.o
	$(FC) -c symmetry.f90

clean:
	rm *.mod *.o supercell
