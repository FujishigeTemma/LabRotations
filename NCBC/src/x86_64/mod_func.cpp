#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;
#if defined(__cplusplus)
extern "C" {
#endif

extern void _borgka_reg(void);
extern void _cagk_reg(void);
extern void _ccanl_reg(void);
extern void _gap_reg(void);
extern void _gskch_reg(void);
extern void _hyperde3_reg(void);
extern void _ichan2_reg(void);
extern void _lca_reg(void);
extern void _nca_reg(void);
extern void _tca_reg(void);
extern void _tmgsyn_reg(void);
extern void _vecstim_reg(void);

void modl_reg() {
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");
    fprintf(stderr, " \"borgka.mod\"");
    fprintf(stderr, " \"cagk.mod\"");
    fprintf(stderr, " \"ccanl.mod\"");
    fprintf(stderr, " \"gap.mod\"");
    fprintf(stderr, " \"gskch.mod\"");
    fprintf(stderr, " \"hyperde3.mod\"");
    fprintf(stderr, " \"ichan2.mod\"");
    fprintf(stderr, " \"lca.mod\"");
    fprintf(stderr, " \"nca.mod\"");
    fprintf(stderr, " \"tca.mod\"");
    fprintf(stderr, " \"tmgsyn.mod\"");
    fprintf(stderr, " \"vecstim.mod\"");
    fprintf(stderr, "\n");
  }
  _borgka_reg();
  _cagk_reg();
  _ccanl_reg();
  _gap_reg();
  _gskch_reg();
  _hyperde3_reg();
  _ichan2_reg();
  _lca_reg();
  _nca_reg();
  _tca_reg();
  _tmgsyn_reg();
  _vecstim_reg();
}

#if defined(__cplusplus)
}
#endif
