NEURON {
  ARTIFICIAL_CELL VecStim
}

ASSIGNED {
  currentIndex
  eventTime (ms)
  vectorSpace
}

INITIAL {
  currentIndex = 0
  processElement()
  if (currentIndex > 0) {
      net_send(eventTime - t, 1)
  }
}

NET_RECEIVE (weight) {
  if (flag == 1) {
    net_event(t)
    processElement()
    if (currentIndex > 0) {
      net_send(eventTime - t, 1)
    }
  }
}

VERBATIM
extern double* vector_vec();
extern int vector_capacity();
extern void* vector_arg();
ENDVERBATIM

PROCEDURE processElement() {
VERBATIM    
  { 
    void* vecPointer; 
    int index, size; 
    double* eventTimesPointer;
    
    index = (int)currentIndex;
    
    if (index >= 0) {
      vecPointer = *((void**)(&vectorSpace));
      if (vecPointer) {
        size = vector_capacity(vecPointer);
        eventTimesPointer = vector_vec(vecPointer);
        if (index < size) {
          // Fetch event time at current index and increment index
          eventTime = eventTimesPointer[index];
          currentIndex += 1.;
        } else {
          // Invalid index, reset to -1
          currentIndex = -1.;
        }
      } else {
        // Invalid vector pointer, reset index to -1
        currentIndex = -1.;
      }
    }
  }
ENDVERBATIM
}

PROCEDURE play() {
VERBATIM
  void** vecPointer;
  
  vecPointer = (void**)(&vectorSpace);
  *vecPointer = (void*)0;
  
  if (ifarg(1)) {
    *vecPointer = vector_arg(1);
  }
ENDVERBATIM
}