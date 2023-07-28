TITLE gap.mod

NEURON {
  POINT_PROCESS gap
  NONSPECIFIC_CURRENT i
  RANGE r, i, delay
  POINTER v_pair
}

PARAMETER {
  v (millivolt)
  v_pair (millivolt)
  r = 1e10 (megohm)
  delay (ms)
}

ASSIGNED {
  i (nanoamp)
}

BREAKPOINT {
  if (t > delay) {
    i = (v - v_pair)/r
  } else {
    i = 0
  }
}