# A101 Computational Mechanisms

## Partial Deifferential Equation
Differential equations involving derivetives with respect to multiple variables (time, space etc...).

- $\mu$: unkoown variables, function of $D$ independent variables ($\mu=\mu(x_1, x_2,...,x_D)$)
- g: Data
- $P(\mu,g)=0$
    - The PDE has order $Q$, if $Q$ is tge highest order of the partial derivative.
    - If the PDE is a linear function of $\mu$ and its derivatives, then PDE is **linear**, otherwise it's non-linear.
    - If all the terms of the PDE are function of $\mu$ or it derivatives, then the PDE is **homogeneous**, otherwise non-homogeneous.

### Examples
- Transport Eq: $\frac{\partial\mu}{\partial t} + \nabla(B\mu)=0$
    - 1st order
    - linear
    - homogeneuous
- Poisson Eq: $\nabla^2\mu=g$
    - 2nd order
    - linear
    - non-homogeneous
- Heat Eq: $\frac{\partial\mu}{\partial t} - \nabla\mu=g$
    - 2nd order
    - linear
    - non-homogeneous
- Wave Eq: $\frac{\partial^2\mu}{\partial^2 t}-\nabla^2\mu=0$
    - 2nd order
    - linear
    - homogeneous
- Burger's Eq: $\frac{\partial\mu}{\partial t}+\mu\frac{\partial\mu}{\partial x}=0$
    - 1st order
    - non-linear
    - homogeneous

## 

A function $\tilde{\mu}=\tilde{\mu}(x)$ is a solution of the PDE, if substituting it in the equation, makes the PDE an identity.

Exact PDE: $P(\mu,f)=0$
↓ Numerical Discreation
Apporoximate PDE: $P_N(\mu_N,g_N)=0$

where N is an integer defining the dimension of the approximate problem.

The method is **convergent** if $||\mu-\mu_N|| → 0$ for $N→\inf$
The method is **consistent** if $P_N(\mu,g)-P(\mu,g)→0$ for $N→\inf$
The method is **stable** if small perturbation of the data, the result is a small perturbation of the solution.

### Lax-Richtmyer theorem
If a method is consistent, then it is convergent if and only if it is stable.

## Numerical differentiation

Let's consider a function $\mu$ abd its derivertive that are single-valued, finite and continuous function of $x$.
We use **Taylor expansion**.

$$
U(x+h) = U(x) + h\frac{\partial\mu}{\partial x}  + \frac{h^2}{2!}\frac{\partial^2\mu}{\partial^2 x} +... = \sum \frac{h^k}{k!}U^k(x)
$$
$$
U(x-h) = U(x) - h\frac{\partial\mu}{\partial x}  + \frac{h^2}{2!}\frac{\partial^2\mu}{\partial^2 x} -... = \sum \frac{(-h)^k}{k!}U^k(x)
$$

### 1st order
Forward difference
$$
U'(x) = \frac{U(x+h)-U(x)}{h} + \mathcal{O}(h)
$$
Backward difference
$$
U'(x) = \frac{U(x)-U(x-h)}{h} + \mathcal{O}(h)
$$
Central difference (more precise; intuitively)
$$
U'(x) = \frac{U(x+h)-U(x-h)}{2h} + \mathcal{O}(h^2)
$$

### 2nd order
Central difference
$$
U''(x) = \frac{U(x+h)-2U(x)+(x-h)}{h^2} + \mathcal{O}(h^2)
$$

# Linear System

Consider $Ax=b$
- $A$ is a matrix of size $n\times n$ with elements $a_{ij}$
- $x$ is a vector of size $n$ (unknown)
- $b$ is a vector of size $n$

The goal here is to find $x$.
A solution exists if and only if $A$ is non **singular**.

The Cramer rule give the solution to the linear system.
$$
x_i = \frac{det(A_i)}{det(A)}
$$

TODO: definition of $A_i$

But computation cost of Cramer rule is too high (Three determinants need to be computed for a system of size $n$).

## Direct Methods
- Methods for rehieh the solution is obtained within a finite number of operations.
- They produce exact solution.
- The only error present is due to woonding.


## Iterative Methods (1) 
- The solution is obtained (in theory) only with an infinite number of steps.
- We intherited an error by chosing a number of operations.

### LU decomposition/factorization

$A = LU$

## Iterative Methods (2)
- Good for large problems and for non-linear equations.
- In order to 


### Basic Form
$$
x^{k+1} = Bx^k + g
$$

$B$ and $g$ must satisfy the condition below.

$$
\begin{align}
x &= Bx + g \\
A^{-1}b &= B\left(A^{-1}b\right)+g & \because x = A^{-1}b \\
g &= (I-B)A^{-1}b
\end{align}
$$

# TODO

# Linear Convection
$$
\frac{\partial u}{\partial t} + c\frac{\partial u}{\partial x} = 0
$$

Here, $c$ is the constant parameter (phiysical meaning: transport velocity).

Initial condition: $u(x,t=0) = u_0(x)$ \
$u(x, t=\tau) = u_0(x-c\tau)$

The initical profile is transported with a velocity $c$ (=shifted to the right). At time $t=\tau$, the initial profile is displaced by $c\tau$.

## Discretization
Let's consider a grid with $\Delta x$ and $\Delta t$. \
$x_i = i\Delta x \quad i=0,1,...$ \
$t^n = N\Delta t \quad n=0,1,...$ \
Then, the solution $u(x,t)$ is approximated by $U_i^n = U(x_i, t^N)$

$$
\frac{\partial u}{\partial t} \approx \frac{U_i^{n+1}-U_i^n}{\Delta t}
$$

### Forward Difference
$$
\frac{\partial u}{\partial x} \approx \frac{U_{i}^n-U_{i-1}^n}{\Delta x}
$$

Substituting these into the PDE, we get
$$
\frac{U_i^{n+1}-U_i^n}{\Delta t} + c\frac{U_{i}^n-U_{i-1}^n}{\Delta x} = 0
$$

Rearranging the equation, we get
$$
U_i^{n+1} = U_i^n - \frac{c\Delta t}{\Delta x}(U_{i}^n-U_{i-1}^n)
$$

### Backward Difference
Similarly, we can get
$$
U_i^{n+1} = U_i^n - \frac{c\Delta t}{\Delta x}(U_{i+1}^n-U_{i}^n)
$$

### Central Difference
And also, we can get
$$
U_i^{n+1} = U_i^n - \frac{c\Delta t}{2\Delta x}(U_{i+1}^n-U_{i-1}^n)
$$

# Diffusion Equation
$$
\frac{\partial u}{\partial t} = \nu\frac{\partial^2 u}{\partial x^2} \quad \nu > 0
$$

Here, $\nu$ is the constant parameter (physical meaning: diffusion coefficient).

The initial profile is diffused with a velocity $\nu$.

## Discretization
$$
\frac{\partial u}{\partial t} \approx \frac{U_i^{N+1}-U_i^N}{\Delta t}
$$
$$
\frac{\partial^2 u}{\partial x^2} \approx \frac{U_{i+1}^N-2U_i^N+U_{i-1}^N}{\Delta x^2}
$$

Substituting these into the PDE, we get
$$
\frac{U_i^{N+1}-U_i^N}{\Delta t} = \nu\frac{U_{i+1}^N-2U_i^N+U_{i-1}^N}{\Delta x^2}
$$

Rearranging the equation, we get
$$
U_i^{N+1} = U_i^n + \frac{\nu\Delta t}{\Delta x^2}(U_{i+1}^N-2U_i^N+U_{i-1}^N)
$$

# Burger's Equation
$$
\frac{\partial u}{\partial t} + u\frac{\partial u}{\partial x} = \nu\frac{\partial^2 u}{\partial x^2}
$$

# Variations of the methods

## Explicit Method
- In the explicit method, the solution at the current time step is directly computed using the known values from the previous time step.
- The solution at each grid point is updated independently using the values from the previous time step.
- The explicit method is straightforward to implement and computationally efficient.
- However, the explicit method is subject to stability constraints, such as the Courant-Friedrichs-Lewy (CFL) condition, which limits the maximum allowable time step size to ensure numerical stability.
- If the time step exceeds the stability limit, the solution can become unstable and diverge.
- Explicit methods are often used when the PDEs are not stiff and the time step required for stability is not too small.

## Implicit Method
- In the implicit method, the solution at the current time step is computed using both the known values from the previous time step and the unknown values at the current time step.
- The implicit method involves solving a system of equations at each time step, where the unknowns are coupled.
- The implicit method is more complex to implement compared to the explicit method because it requires solving a system of equations.
- However, the implicit method has better stability properties and allows for larger time steps without compromising numerical stability.
- The implicit method is unconditionally stable for many problems, meaning that the time step size is not limited by stability constraints.
- Implicit methods are preferred when dealing with stiff PDEs or when the explicit method requires extremely small time steps for stability.

## List of methods
- Forward Euler Method (Explicit)
  - $\Delta U = \mathcal{O}(\Delta t, \Delta x^2)$
- Backward Euler Method (Implicit)
  - $\Delta U = \mathcal{O}(\Delta t, \Delta x^2)$
- Crank-Nicolson Method (Implicit)
  - $\Delta U = \mathcal{O}(\Delta t^2, \Delta x^2)$
- Adams-Bashforth Method (Explicit)
  - $\Delta U = \mathcal{O}(\Delta t^p, \Delta x^2)$ (p: order of the method)

# Stability
Numerical stability is a crucial aspect of computational methods as it ensures that the numerical solution does not diverge over time and converges to the true solution. The stability conditions for various methods are as follows:

- Forward Euler Method:
  - The time step $\Delta t$ must be sufficiently small.
  - Specifically, the stability condition is $\Delta t ≤ \frac{(\Delta x)^2}{2\nu}$ for the diffusion equation.
- Backward Euler Method:
  - Unconditionally stable, regardless of the time step size.
  - However, large time steps may lead to reduced accuracy, so choosing an appropriate step size is necessary.
- Crank-Nicolson Method:
  - Unconditionally stable, regardless of the time step size.
  - Possesses intermediate properties between the Forward and Backward Euler methods, with second-order accuracy.
  - For nonlinear problems, iterative methods may be required, potentially increasing computational costs.
- Adams-Bashforth Method:
  - An explicit multi-step method where stability depends on the time step size.
  - For the second-order Adams-Bashforth method, the stability condition is $\Delta t ≤ \frac{2\nu}{c^2}$ for the linear convection equation.
  - Higher-order Adams-Bashforth methods have more complex stability regions.

It is important to note that these stability conditions may vary depending on the nature of the problem (e.g., diffusion equation, advection equation) and the spatial discretization method employed (e.g., finite difference method, finite element method). 
