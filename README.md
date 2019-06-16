# N-Body Inelastic Collisions and Gravity

**[website here]**(http://jasontung.me/physics_project/)

## what is this

click and drag to create balls with the initial velocity represented by the black arrow

hit go to run the simulation once youve populated the screen with some number of bodies

the interactions that proceed will either be completely inelastic collisions or gravity depending on the mode selected in the upper left

further instructions/specifications provided on the site.

both simulations are pausable and resumable with the pause/resume buttons.

the mass of each particle will be set by taking the value of the mass input on the upper right prior to creating the particle.

every particle has some set of tracked variables displayed in a table on the right.

## limitations

gravity vectors are absolutely massive because of how it scales with r^2.
I have to freeze the balls once they collide in the gravity simulation because otherwise they'd shoot into infinity due to the limitations of what a bound is in SVG/JS. 

the simulations also somewhat break if you move the mouse of of the canvas--seek trouble and you'll find it.
