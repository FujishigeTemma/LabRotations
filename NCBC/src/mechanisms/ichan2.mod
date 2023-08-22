TITLE ichan2.mod

COMMENT
the effect of conductivity change in soma.
ENDCOMMENT

NEURON { 
  SUFFIX ichan2
  USEION nat READ enat WRITE inat VALENCE 1
  USEION kf READ ekf WRITE ikf VALENCE 1
  USEION ks READ eks WRITE iks VALENCE 1
  NONSPECIFIC_CURRENT il
  RANGE gnat, gkf, gks, gnatbar, gkfbar, gksbar, gl, el, minf, mtau, hinf, htau, nfinf, nftau, inat, ikf, nsinf, nstau, iks
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
  celsius (degC)
  v (mV)
  dt (ms)
  enat (mV)
  gnatbar (mho/cm2)
  ekf (mV)
  gkfbar (mho/cm2)
  eks (mV)
  gksbar (mho/cm2)
  gl (mho/cm2)
  el (mV)
}

ASSIGNED {
  gnat (mho/cm2) 
  gkf (mho/cm2)
  gks (mho/cm2)

  inat (mA/cm2)
  ikf (mA/cm2)
  iks (mA/cm2)
  il (mA/cm2)

  mtau (ms)
  htau (ms)
  nftau (ms)
  nstau (ms)

  minf
  hinf
  nfinf
  nsinf
}

STATE {
  m
  h
  nf
  ns
}

BREAKPOINT {
  SOLVE state
  gnat = gnatbar * m * m * m * h  
  inat = gnat * (v - enat)
  gkf = gkfbar * nf * nf * nf * nf
  ikf = gkf * (v-ekf)
  gks = gksbar * ns * ns * ns * ns
  iks = gks * (v-eks)
  il = gl * (v-el)
}

INITIAL {
  rates(v)
  
  m = minf
  h = hinf
  nf = nfinf
  ns = nsinf
}

LOCAL q10

PROCEDURE state() {
  rates(v)

  m = m + (minf - m) * (1 - exp(-dt * q10 / mtau))
  h = h + (hinf - h) * (1 - exp(-dt * q10 / htau))
  nf = nf + (nfinf - nf) * (1 - exp(-dt * q10 / nftau))
  ns = ns + (nsinf - ns) * (1 - exp(-dt * q10 / nstau))
}

:Call once to initialize inf at resting v.
PROCEDURE rates(v) {
  LOCAL alpha, beta, sum
  q10 = 3^((celsius - 6.3)/10)

  :"m" sodium activation system - act and inact cross at -40
  :"m" is the activation gate for the sodium current. It is voltage-dependent.
  alpha = -0.3 * vtrap((v + 60 - 17), -5)
  beta = 0.3 * vtrap((v + 60 - 45), 5)
  sum = alpha + beta        
  mtau = 1 / sum
  minf = alpha / sum

  :"h" sodium inactivation system
  :"h" is the inactivation gate for the sodium current. It is also voltage-dependent.
  alpha = 0.23 / exp((v + 60 + 5) / 20)
  beta = 3.33 / (1 + exp((v + 60 - 47.5) / -10))
  sum = alpha + beta
  htau = 1 / sum 
  hinf = alpha / sum 

  :"ns" sKDR activation system
  :"ns" is the activation gate for the slow Potassium (K) Rectifier current. It is voltage-dependent.
  alpha = -0.028 * vtrap((v + 65 - 35), -6)
  beta = 0.1056 / exp((v + 65 - 10) / 40)
  sum = alpha + beta        
  nstau = 1 / sum
  nsinf = alpha / sum

  :"nf" fKDR activation system
  :"nf" is the activation gate for the fast Potassium (K) Rectifier current. It is voltage-dependent.
  alpha = -0.07 * vtrap((v + 65 - 47), -6)
  beta = 0.264 / exp((v + 65 - 22) / 40)
  sum = alpha + beta        
  nftau = 1 / sum
  nfinf = alpha / sum
}

FUNCTION vtrap(x, y) {
  if (fabs(x / y) < 1e-6) {
    vtrap = y * (1 - x / y / 2)
  } else {
    vtrap = x / (exp(x / y) - 1)
  }
}
