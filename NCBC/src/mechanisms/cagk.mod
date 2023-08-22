TITLE cagk.mod Calcium activated K channel.

COMMENT
Modified from Moczydlowski and Latorre (1983) J. Gen. Physiol. 82
ENDCOMMENT

NEURON {
  SUFFIX cagk
  USEION nca READ ncai VALENCE 2
  USEION lca READ lcai VALENCE 2
  USEION tca READ tcai VALENCE 2
  USEION k READ ek WRITE ik
  RANGE gkbar, gkca, ik
}

UNITS {
  (molar) = (1/liter)
  (mV) = (millivolt)
  (mA) = (milliamp)
  (mM) = (millimolar)
}

UNITS {
  FARADAY = (faraday) (kilocoulombs)
  R = 8.313424 (joule/degC)
}

PARAMETER {
  celsius (degC)
  v (mV)
  ek (mV)
  cai = 5.e-5 (mM)
  gkbar = .01 (mho/cm2)
  d1 = .84
  d2 = 1.
  k1 = .48e-3 (mM)
  k2 = .13e-6 (mM)
  abar = .28 (/ms)
  bbar = .48 (/ms)
  st = 1 (1)
  lcai (mV)
  ncai (mV)
  tcai (mV)
}

ASSIGNED {
  ik (mA/cm2)
  gkca (mho/cm2)
  oinf
  otau (ms)
}

STATE {
  o
}

INITIAL {
  cai = ncai + lcai + tcai
  rates(v, cai)

  o = oinf
}

BREAKPOINT {
  SOLVE state METHOD cnexp
  gkca = gkbar * o^st
  ik = gkca * (v - ek)
}

DERIVATIVE state {
  rates(v, cai)

  o' = (oinf - o) / otau
}

FUNCTION alpha(v (mV), c (mM)) (1/ms) {
  alpha = c * abar/(c + expTerm(k1,d1,v))
}

FUNCTION beta(v (mV), c (mM)) (1/ms) {
  beta = bbar/(1 + c / expTerm(k2,d2,v))
}

FUNCTION expTerm(k (mM), d, v (mV)) (mM) {
  expTerm = k * exp(-2 * d * FARADAY * v / R / (273.15 + celsius))
}

PROCEDURE rates(v (mV), cai (mM)) {
  LOCAL a, b

  a = alpha(v, cai)
  b = beta(v, cai)

  otau = 1 / (a + b)
  oinf = a * otau
}