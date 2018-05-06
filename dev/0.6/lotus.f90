!-------------------------------------------------------!
!----------------- 2D Cylinder Array -------------------!
!-------------------------------------------------------!
! 7 cylinders
! Re= 100
! Investigation into the range of g* for Cl cancelation
! Grid size:
!   x: [-5DG,15DG]
!   y: [-5DG,5DG]
!-------------------------------------------------------!
program array
  use fluidMod,   only: fluid
  use bodyMod,    only: body
  use mympiMod!,   only: init_mympi,mympi_end,mympi_rank
  use gridMod,    only: xg,composite
  use imageMod,   only: display
  use geom_shape!, only: cylinder,operator(.and.),pi
  implicit none
!
! -- physcial parameters
  integer,parameter :: rows = 1          ! number of rows (not include center)
  real,parameter    :: g_star = 0.6      ! nondimensional spacing
  real,parameter    :: aoa = 0           ! angle of attack
  real,parameter    :: Re_D = 100        ! Reynolds number based on diameter
!
! -- numerical parameters
  real,parameter    :: D = 32            ! resolution (points per diameter)
  real,parameter    :: finish = 300      ! number of timesteps to run (finish = timesteps*DG)
  integer           :: b(3) = (/16,1,1/) ! blocks. Product MUST be equal to number of cores (16 CORES)
  logical           :: root              ! root processor
!
! -- derived values (don't touch)
  real,parameter    :: nu = D/Re_D   ! nondimensional viscosity
  real,parameter    :: DG = (2.*rows*(1.+g_star)+1.)*D  ! group diameter
  integer :: n(3),m(3)               ! number of points & number of points per block
!
! -- utils
  logical           :: kill          !ends simulation in all running cores & writes the output
  real,parameter    :: dtPrint = 1.  ! print rate
!
! -- variables
  type(fluid) :: flow                    ! fluid object
  type(body)  :: bodies                  ! body object
  real :: dt, t1, pforce(2), vforce(2), U
!
! -- Initialize MPI (if MPI is OFF, b is set to 1)
  call init_mympi(2,set_blocks=b)
  root = mympi_rank()==0
!
! -- Initialize grid (might need to adjust these parameters later)
!TWO DIMENSIONAL SIMULATIONS ARE RUN WHEN THE NUMBER OF CELLS IN Z IS 0 OR 1.
  n = composite(DG*(/8,2,0/), prnt=root)
  call xg(1)%stretch(n(1), -5*DG, -0.6*DG, 0.6*DG, 15*DG, h_max=15., prnt=root)
  call xg(2)%stretch(n(2), -5*DG, -0.6*DG, 0.6*DG, 5*DG, prnt=root)
!
! -- Initialize array
   bodies = make_array(aoa)
!
! -- Initialize fluid
  m = n/b           ! number of points per block!!
  call flow%init(m, bodies, V=(/1.,0.,0./), nu=nu)
  if(root) print *, '-- init complete --'
!
! -- Time update loop
  !do while (flow%time<finish*T*D)
  do while (flow%time<finish*DG)!*T*D)
     dt = flow%dt                       ! time step
     t1 = flow%time+dt                  ! time at the end of this step
     call flow%update()                 ! update N-S
!
! -- measure and print force coefficients
     pforce = -2.*bodies%pforce(flow%pressure)/D
     vforce = 2.*nu*bodies%vforce(flow%velocity)/D
     if(root) write(9,'(f19.0,f8.4,4e16.8)') t1/D,dt,pforce,vforce
     if(root) flush(9)
!
! -- print time left and generate picture of the flow periodically
!    period of printing from dtPrint
     if(mod(t1,dtPrint*DG)<dt) then
       if(root) print "('Time:',f8.3,'. Time remaining:',f8.3)",t1/DG,finish-t1/DG
      !  call flow%write()
       call display(flow%velocity%vorticity_z(),'vorticity', box = int((/-DG,-DG,6*DG,2*DG/)))!,lim=4./DG)
     end if
!
!    check if .kill file has been created, if so end the simulation
    !  inquire(file=".kill", exist=kill)
    !  if (kill) then
    !    exit
    !  end if
  end do
  call flow%write()
  call mympi_end()
contains
!
! -- make an array of cylinders with group diameter DG
  type(set) function make_array(aoa)
    real,intent(in) :: aoa
    integer,parameter :: n(4) = (/6,13,19,25/)
    real,parameter    :: R = 0.5*DG-0.5*D
    real    :: theta,xc,yc
    integer :: i,j
    make_array = place_cyl(0.,0.)
    do j=1,rows
       do i=1,n(j)
          theta = 2.*pi*(i-1.)/real(n(j))+aoa
          xc = R*sin(theta)*real(j)/rows
          yc = R*cos(theta)*real(j)/rows
          make_array = make_array.or.place_cyl(xc,yc)
       end do
    end do
  end function make_array
  type(cylinder) function place_cyl(xc,yc)
    real,intent(in) :: xc,yc
    place_cyl = cylinder(1,1,3,0.5*D,center=(/xc,yc,0./))
  end function place_cyl
end program array
