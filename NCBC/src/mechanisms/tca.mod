TITLE T-calcium channel From Migliore CA3

COMMENT
T-type calcium channel
ENDCOMMENT

NEURON {
  SUFFIX cat
  USEION tca READ etca WRITE itca VALENCE 2
  USEION ca READ cai, cao VALENCE 2
  RANGE gcatbar, cai, itca, etca
}

UNITS {
  (mA) = (milliamp)
  (mV) = (millivolt)
}

UNITS {
  FARADAY = 96520 (coul)
  R = 8.3134 (joule/degC)
  KTOMV = .0853 (mV/degC)
}

PARAMETER {
  v (mV)
  celsius (degC)
  gcatbar=.003 (mho/cm2)
  cai (mM)
  cao (mM)
}

ASSIGNED {
  itca (mA/cm2)
  gcat (mho/cm2)
  etca (mV)
}

STATE {
  m
  h 
}

INITIAL {
  m = minf(v)
  h = hinf(v)
}

BREAKPOINT {
  SOLVE states METHOD cnexp

  gcat = gcatbar * m * m * h
  itca = gcat * ghk(v, cai, cao)
}

DERIVATIVE states { :exact when v held constant
  m' = (minf(v) - m) / m_tau(v)
  h' = (hinf(v) - h) / h_tau(v)
}


FUNCTION ghk(v(mV), ci(mM), co(mM)) (mV) {
  LOCAL nu,f

  f = KTF(celsius) / 2
  nu = v / f
  ghk = -f * (1. - (ci / co) * exp(nu)) * efun(nu)
}

FUNCTION KTF(celsius (DegC)) (mV) {
  KTF = ((25. / 293.15) * (celsius + 273.15))
}


FUNCTION efun(z) {
  if (fabs(z) < 1e-4) {
    efun = 1 - z/2
  } else {
    efun = z / (exp(z) - 1)
  }
}

FUNCTION hinf(v(mV)) {
  LOCAL a,b
  TABLE FROM -150 TO 150 WITH 200

  a = 1.e-6 * exp(-v / 16.26)
  b = 1 / (exp((-v + 29.79) / 10) + 1)

  hinf = a / (a + b)
}

FUNCTION minf(v(mV)) {
  LOCAL a,b
  TABLE FROM -150 TO 150 WITH 200

  a = 0.2 * (-1.0 * v + 19.26) / (exp((-1.0 * v + 19.26) / 10.0) - 1.0)
  b = 0.009 * exp(-v / 22.03)

  minf = a / (a + b)
}

FUNCTION m_tau(v(mV)) (ms) {
  LOCAL a,b
  TABLE FROM -150 TO 150 WITH 200

  a = 0.2 * (-1.0 * v + 19.26) / (exp((-1.0 * v + 19.26) / 10.0) - 1.0)
  b = 0.009*exp(-v/22.03)

  m_tau = 1/(a+b)
}

FUNCTION h_tau(v(mV)) (ms) {
  LOCAL a,b
  TABLE FROM -150 TO 150 WITH 200

  a = 1.e-6 * exp(-v / 16.26)
  b = 1 / (exp((-v + 29.79) / 10.) + 1.)

  h_tau = 1 / (a + b)
}
