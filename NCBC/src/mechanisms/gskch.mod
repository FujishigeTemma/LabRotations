TITLE gskch.mod small conductance calcium-activated potassium channels in granule cell dendrites

COMMENT
SK channel in granule cell dendrites
ENDCOMMENT

UNITS {
  (molar) = (1/liter)
  (mM) = (millimolar)
  (mA) = (milliamp)
  (mV) = (millivolt)
}

NEURON {
  SUFFIX gskch
  USEION sk READ esk WRITE isk VALENCE 1
  USEION nca READ ncai VALENCE 2
  USEION lca READ lcai VALENCE 2
  USEION tca READ tcai VALENCE 2
  RANGE gsk, gskbar, qinf, qtau, isk
}

INDEPENDENT {
  t FROM 0 TO 1 WITH 1 (ms)
}

PARAMETER {
  celsius (degC)
  v (mV)
  dt (ms)
  gskbar (mho/cm2)
  esk  (mV)
  cai (mM)
  ncai (mM)
  lcai (mM)
  tcai (mM)
}

STATE {
  q
}

ASSIGNED {
  isk (mA/cm2)
  gsk (mho/cm2)
  qinf
  qtau (ms)
}

BREAKPOINT {
  SOLVE state
  gsk = gskbar * q*q
  isk = gsk * (v-esk)
}

INITIAL {
  cai = ncai + lcai + tcai  
  rates(cai)
  q = qinf
}

LOCAL q10

PROCEDURE state() {
  cai = ncai + lcai + tcai
  rates(cai)

  q = q + (qinf - q) * (1 - exp(-dt * q10 / qtau) * q10)
}

PROCEDURE rates(cai) {
  LOCAL alpha, beta
  q10 = 3^((celsius - 6.3)/10)
  
  alpha = 1.25e1 * cai * cai
  beta = 0.00025 

  qtau = 1 / (alpha + beta)
  qinf = alpha * qtau
}
