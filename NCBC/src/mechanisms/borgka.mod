TITLE Borg-Graham type generic K-A channel

NEURON {
  SUFFIX borgka
  USEION k READ ek WRITE ik
  RANGE gkabar, gka, ik
}

UNITS {
  (mA) = (milliamp)
  (mV) = (millivolt)
}

PARAMETER {
  celsius (degC)
  v (mV)
  ek (mV)
  gkabar = .01 (mho/cm2)
  vhalfn = -33.6 (mV)
  vhalfl = -83 (mV)
  a0n = 0.02 (/ms)
  a0l = 0.08 (/ms)
  zetan = -3 (1)
  zetal = 4 (1)
  gmn = 0.6 (1)
  gml = 1 (1)
}

ASSIGNED {
  ik (mA/cm2)
  gka
  ninf
  linf
  ntau (ms)
  ltau (ms)
}

STATE {
  n
  l
}

INITIAL {
  rates(v)

  n = ninf
  l = linf
}

BREAKPOINT {
  SOLVE states METHOD cnexp
  gka = gkabar * n * l
  ik = gka * (v - ek)
}

DERIVATIVE states {
  rates(v)

  n' = (ninf - n) / ntau
  l' = (linf - l) / ltau
}

FUNCTION alpha(v (mV), vhalf (mV), zeta (1)) {
  alpha = exp(1e-3 * zeta * (v - vhalf) * 9.648e4 / (8.315 * (273.16 + celsius)))
}

PROCEDURE rates(v (mV)) {
  LOCAL a, q10
  q10 = 3 ^ ((celsius - 30) / 10)

  a = alpha(v, vhalfn, zetan)
  ninf = 1 / (1 + a)
  ntau = 1 / (q10 * a0n * (1 + a))

  a = alpha(v, vhalfl, zetal)
  linf = 1 / (1 + a)
  ltau = 1 / (q10 * a0l * (1 + a))
}