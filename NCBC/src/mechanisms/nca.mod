TITLE nca.mod  

COMMENT
the effect of conductivity change in soma
ENDCOMMENT

NEURON { 
  SUFFIX nca
  USEION nca READ enca WRITE inca VALENCE 2 
  RANGE gnca, gncabar, cinf, ctau, dinf, dtau, inca
}

UNITS {
  (mA) =(milliamp)
  (mV) =(millivolt)
  (uF) = (microfarad)
  (molar) = (1/liter)
  (nA) = (nanoamp)
  (mM) = (millimolar)
  (um) = (micron)
}

UNITS {
  FARADAY = 96520 (coul)
  R = 8.3134  (joule/degC)
}

INDEPENDENT {
  t FROM 0 TO 100 WITH 100 (ms)
}

PARAMETER {
  celsius
  v (mV) 
  dt (ms) 
  gncabar (mho/cm2)
}

ASSIGNED {
  gnca (mho/cm2)
  inca (mA/cm2)
  enca (mV)
  cinf dinf
  ctau (ms)
  dtau (ms) 
  cexp
  dexp      
}

STATE {
  c
  d
}


BREAKPOINT {
  SOLVE states
  gnca = gncabar * c * c * d
  inca = gnca * (v - enca)
}

INITIAL {
  rates(v)

  c = cinf
  d = dinf
}

LOCAL q10

PROCEDURE states() {
  rates(v)

  c = c + (cinf-c) * (1 - exp(-dt*q10/ctau))
  d = d + (dinf-d) * (1 - exp(-dt*q10/dtau))
}

PROCEDURE rates(v) {
  LOCAL alpha, beta, sum
  q10 = 3^((celsius - 6.3)/10)

  : "c" NCa activation system
  alpha = -0.19 * vtrap(v - 19.88, -10)
  beta = 0.046 * exp(-v / 20.73)
  sum = alpha + beta        
  ctau = 1 / sum
  cinf = alpha / sum

  : "d" NCa inactivation system
  alpha = 0.00016 / exp(-v / 48.4)
  beta = 1 / (exp((-v + 39) / 10) + 1)
  sum = alpha + beta        
  dtau = 1 / sum
  dinf = alpha / sum
}

FUNCTION vtrap(x, y) {  :Traps for 0 in denominator of rate eqns.
  if (fabs(x / y) < 1e-6) {
    vtrap = y * (1  -  x / y /2)
  }else{  
    vtrap = x / (exp(x / y) - 1)
  }
}
