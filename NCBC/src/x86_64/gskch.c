/* Created by Language version: 7.7.0 */
/* VECTORIZED */
#define NRN_VECTORIZED 1
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "mech_api.h"
#undef PI
#define nil 0
#include "md1redef.h"
#include "section.h"
#include "nrniv_mf.h"
#include "md2redef.h"
 
#if METHOD3
extern int _method3;
#endif

#if !NRNGPU
#undef exp
#define exp hoc_Exp
extern double hoc_Exp(double);
#endif
 
#define nrn_init _nrn_init__gskch
#define _nrn_initial _nrn_initial__gskch
#define nrn_cur _nrn_cur__gskch
#define _nrn_current _nrn_current__gskch
#define nrn_jacob _nrn_jacob__gskch
#define nrn_state _nrn_state__gskch
#define _net_receive _net_receive__gskch 
#define rates rates__gskch 
#define state state__gskch 
 
#define _threadargscomma_ _p, _ppvar, _thread, _nt,
#define _threadargsprotocomma_ double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt,
#define _threadargs_ _p, _ppvar, _thread, _nt
#define _threadargsproto_ double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt
 	/*SUPPRESS 761*/
	/*SUPPRESS 762*/
	/*SUPPRESS 763*/
	/*SUPPRESS 765*/
	 extern double *getarg();
 /* Thread safe. No static _p or _ppvar. */
 
#define t _nt->_t
#define dt _nt->_dt
#define gskbar _p[0]
#define gskbar_columnindex 0
#define isk _p[1]
#define isk_columnindex 1
#define gsk _p[2]
#define gsk_columnindex 2
#define qinf _p[3]
#define qinf_columnindex 3
#define qtau _p[4]
#define qtau_columnindex 4
#define q _p[5]
#define q_columnindex 5
#define esk _p[6]
#define esk_columnindex 6
#define ncai _p[7]
#define ncai_columnindex 7
#define lcai _p[8]
#define lcai_columnindex 8
#define tcai _p[9]
#define tcai_columnindex 9
#define Dq _p[10]
#define Dq_columnindex 10
#define v _p[11]
#define v_columnindex 11
#define _g _p[12]
#define _g_columnindex 12
#define _ion_esk	*_ppvar[0]._pval
#define _ion_isk	*_ppvar[1]._pval
#define _ion_diskdv	*_ppvar[2]._pval
#define _ion_ncai	*_ppvar[3]._pval
#define _ion_lcai	*_ppvar[4]._pval
#define _ion_tcai	*_ppvar[5]._pval
 
#if MAC
#if !defined(v)
#define v _mlhv
#endif
#if !defined(h)
#define h _mlhh
#endif
#endif
 
#if defined(__cplusplus)
extern "C" {
#endif
 static int hoc_nrnpointerindex =  -1;
 static Datum* _extcall_thread;
 static Prop* _extcall_prop;
 /* external NEURON variables */
 extern double celsius;
 /* declaration of user functions */
 static void _hoc_rates(void);
 static void _hoc_state(void);
 static int _mechtype;
extern void _nrn_cacheloop_reg(int, int);
extern void hoc_register_prop_size(int, int, int);
extern void hoc_register_limits(int, HocParmLimits*);
extern void hoc_register_units(int, HocParmUnits*);
extern void nrn_promote(Prop*, int, int);
extern Memb_func* memb_func;
 
#define NMODL_TEXT 1
#if NMODL_TEXT
static const char* nmodl_file_text;
static const char* nmodl_filename;
extern void hoc_reg_nmodl_text(int, const char*);
extern void hoc_reg_nmodl_filename(int, const char*);
#endif

 extern void _nrn_setdata_reg(int, void(*)(Prop*));
 static void _setdata(Prop* _prop) {
 _extcall_prop = _prop;
 }
 static void _hoc_setdata() {
 Prop *_prop, *hoc_getdata_range(int);
 _prop = hoc_getdata_range(_mechtype);
   _setdata(_prop);
 hoc_retpushx(1.);
}
 /* connect user functions to hoc names */
 static VoidFunc hoc_intfunc[] = {
 "setdata_gskch", _hoc_setdata,
 "rates_gskch", _hoc_rates,
 "state_gskch", _hoc_state,
 0, 0
};
 #define _zq10 _thread[0]._pval[0]
 /* declare global and static user variables */
 static int _thread1data_inuse = 0;
static double _thread1data[1];
#define _gth 1
#define cai_gskch _thread1data[0]
#define cai _thread[_gth]._pval[0]
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "cai_gskch", "mM",
 "gskbar_gskch", "mho/cm2",
 "isk_gskch", "mA/cm2",
 "gsk_gskch", "mho/cm2",
 "qtau_gskch", "ms",
 0,0
};
 static double delta_t = 1;
 static double q0 = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 "cai_gskch", &cai_gskch,
 0,0
};
 static DoubVec hoc_vdoub[] = {
 0,0,0
};
 static double _sav_indep;
 static void nrn_alloc(Prop*);
static void  nrn_init(NrnThread*, _Memb_list*, int);
static void nrn_state(NrnThread*, _Memb_list*, int);
 static void nrn_cur(NrnThread*, _Memb_list*, int);
static void  nrn_jacob(NrnThread*, _Memb_list*, int);
 
static int _ode_count(int);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"gskch",
 "gskbar_gskch",
 0,
 "isk_gskch",
 "gsk_gskch",
 "qinf_gskch",
 "qtau_gskch",
 0,
 "q_gskch",
 0,
 0};
 static Symbol* _sk_sym;
 static Symbol* _nca_sym;
 static Symbol* _lca_sym;
 static Symbol* _tca_sym;
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
 	_p = nrn_prop_data_alloc(_mechtype, 13, _prop);
 	/*initialize range parameters*/
 	gskbar = 0;
 	_prop->param = _p;
 	_prop->param_size = 13;
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 6, _prop);
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 prop_ion = need_memb(_sk_sym);
 nrn_promote(prop_ion, 0, 1);
 	_ppvar[0]._pval = &prop_ion->param[0]; /* esk */
 	_ppvar[1]._pval = &prop_ion->param[3]; /* isk */
 	_ppvar[2]._pval = &prop_ion->param[4]; /* _ion_diskdv */
 prop_ion = need_memb(_nca_sym);
 nrn_promote(prop_ion, 1, 0);
 	_ppvar[3]._pval = &prop_ion->param[1]; /* ncai */
 prop_ion = need_memb(_lca_sym);
 nrn_promote(prop_ion, 1, 0);
 	_ppvar[4]._pval = &prop_ion->param[1]; /* lcai */
 prop_ion = need_memb(_tca_sym);
 nrn_promote(prop_ion, 1, 0);
 	_ppvar[5]._pval = &prop_ion->param[1]; /* tcai */
 
}
 static void _initlists();
 static void _thread_mem_init(Datum*);
 static void _thread_cleanup(Datum*);
 static void _update_ion_pointer(Datum*);
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
extern void _nrn_thread_table_reg(int, void(*)(double*, Datum*, Datum*, NrnThread*, int));
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 void _gskch_reg() {
	int _vectorized = 1;
  _initlists();
 	ion_reg("sk", 1.0);
 	ion_reg("nca", 2.0);
 	ion_reg("lca", 2.0);
 	ion_reg("tca", 2.0);
 	_sk_sym = hoc_lookup("sk_ion");
 	_nca_sym = hoc_lookup("nca_ion");
 	_lca_sym = hoc_lookup("lca_ion");
 	_tca_sym = hoc_lookup("tca_ion");
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 3);
  _extcall_thread = (Datum*)ecalloc(2, sizeof(Datum));
  _thread_mem_init(_extcall_thread);
  _thread1data_inuse = 0;
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
     _nrn_thread_reg(_mechtype, 1, _thread_mem_init);
     _nrn_thread_reg(_mechtype, 0, _thread_cleanup);
     _nrn_thread_reg(_mechtype, 2, _update_ion_pointer);
 #if NMODL_TEXT
  hoc_reg_nmodl_text(_mechtype, nmodl_file_text);
  hoc_reg_nmodl_filename(_mechtype, nmodl_filename);
#endif
  hoc_register_prop_size(_mechtype, 13, 6);
  hoc_register_dparam_semantics(_mechtype, 0, "sk_ion");
  hoc_register_dparam_semantics(_mechtype, 1, "sk_ion");
  hoc_register_dparam_semantics(_mechtype, 2, "sk_ion");
  hoc_register_dparam_semantics(_mechtype, 3, "nca_ion");
  hoc_register_dparam_semantics(_mechtype, 4, "lca_ion");
  hoc_register_dparam_semantics(_mechtype, 5, "tca_ion");
 	hoc_register_cvode(_mechtype, _ode_count, 0, 0, 0);
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 gskch /Users/temma/ghq/LabRotations/NCBC/src/mechanisms/gskch.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
 /*Top LOCAL _zq10 */
static int _reset;
static char *modelname = "gskch.mod small conductance calcium-activated potassium channels in granule cell dendrites";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
static int rates(_threadargsprotocomma_ double);
static int state(_threadargsproto_);
 
static int  state ( _threadargsproto_ ) {
   cai = ncai + lcai + tcai ;
   rates ( _threadargscomma_ cai ) ;
   q = q + ( qinf - q ) * ( 1.0 - exp ( - dt * _zq10 / qtau ) * _zq10 ) ;
    return 0; }
 
static void _hoc_state(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 _r = 1.;
 state ( _p, _ppvar, _thread, _nt );
 hoc_retpushx(_r);
}
 
static int  rates ( _threadargsprotocomma_ double _lcai ) {
   double _lalpha , _lbeta ;
 _zq10 = pow( 3.0 , ( ( celsius - 6.3 ) / 10.0 ) ) ;
   _lalpha = 1.25e1 * _lcai * _lcai ;
   _lbeta = 0.00025 ;
   qtau = 1.0 / ( _lalpha + _lbeta ) ;
   qinf = _lalpha * qtau ;
    return 0; }
 
static void _hoc_rates(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 _r = 1.;
 rates ( _p, _ppvar, _thread, _nt, *getarg(1) );
 hoc_retpushx(_r);
}
 
static int _ode_count(int _type){ hoc_execerror("gskch", "cannot be used with CVODE"); return 0;}
 
static void _thread_mem_init(Datum* _thread) {
   _thread[0]._pval = (double*)ecalloc(1, sizeof(double));
  if (_thread1data_inuse) {_thread[_gth]._pval = (double*)ecalloc(1, sizeof(double));
 }else{
 _thread[_gth]._pval = _thread1data; _thread1data_inuse = 1;
 }
 }
 
static void _thread_cleanup(Datum* _thread) {
   free((void*)(_thread[0]._pval));
  if (_thread[_gth]._pval == _thread1data) {
   _thread1data_inuse = 0;
  }else{
   free((void*)_thread[_gth]._pval);
  }
 }
 extern void nrn_update_ion_pointer(Symbol*, Datum*, int, int);
 static void _update_ion_pointer(Datum* _ppvar) {
   nrn_update_ion_pointer(_sk_sym, _ppvar, 0, 0);
   nrn_update_ion_pointer(_sk_sym, _ppvar, 1, 3);
   nrn_update_ion_pointer(_sk_sym, _ppvar, 2, 4);
   nrn_update_ion_pointer(_nca_sym, _ppvar, 3, 1);
   nrn_update_ion_pointer(_lca_sym, _ppvar, 4, 1);
   nrn_update_ion_pointer(_tca_sym, _ppvar, 5, 1);
 }

static void initmodel(double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt) {
  int _i; double _save;{
  q = q0;
 {
   cai = ncai + lcai + tcai ;
   rates ( _threadargscomma_ cai ) ;
   q = qinf ;
   }
 
}
}

static void nrn_init(NrnThread* _nt, _Memb_list* _ml, int _type){
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; double _v; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 v = _v;
  esk = _ion_esk;
  ncai = _ion_ncai;
  lcai = _ion_lcai;
  tcai = _ion_tcai;
 initmodel(_p, _ppvar, _thread, _nt);
 }
}

static double _nrn_current(double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt, double _v){double _current=0.;v=_v;{ {
   gsk = gskbar * q * q ;
   isk = gsk * ( v - esk ) ;
   }
 _current += isk;

} return _current;
}

static void nrn_cur(NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; int* _ni; double _rhs, _v; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
  esk = _ion_esk;
  ncai = _ion_ncai;
  lcai = _ion_lcai;
  tcai = _ion_tcai;
 _g = _nrn_current(_p, _ppvar, _thread, _nt, _v + .001);
 	{ double _disk;
  _disk = isk;
 _rhs = _nrn_current(_p, _ppvar, _thread, _nt, _v);
  _ion_diskdv += (_disk - isk)/.001 ;
 	}
 _g = (_g - _rhs)/.001;
  _ion_isk += isk ;
#if CACHEVEC
  if (use_cachevec) {
	VEC_RHS(_ni[_iml]) -= _rhs;
  }else
#endif
  {
	NODERHS(_nd) -= _rhs;
  }
 
}
 
}

static void nrn_jacob(NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml];
#if CACHEVEC
  if (use_cachevec) {
	VEC_D(_ni[_iml]) += _g;
  }else
#endif
  {
     _nd = _ml->_nodelist[_iml];
	NODED(_nd) += _g;
  }
 
}
 
}

static void nrn_state(NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; double _v = 0.0; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
 _nd = _ml->_nodelist[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 v=_v;
{
  esk = _ion_esk;
  ncai = _ion_ncai;
  lcai = _ion_lcai;
  tcai = _ion_tcai;
 {  { state(_p, _ppvar, _thread, _nt); }
  } }}

}

static void terminal(){}

static void _initlists(){
 double _x; double* _p = &_x;
 int _i; static int _first = 1;
  if (!_first) return;
_first = 0;
}

#if defined(__cplusplus)
} /* extern "C" */
#endif

#if NMODL_TEXT
static const char* nmodl_filename = "/Users/temma/ghq/LabRotations/NCBC/src/mechanisms/gskch.mod";
static const char* nmodl_file_text = 
  "TITLE gskch.mod small conductance calcium-activated potassium channels in granule cell dendrites\n"
  "\n"
  "COMMENT\n"
  "SK channel in granule cell dendrites\n"
  "ENDCOMMENT\n"
  "\n"
  "UNITS {\n"
  "  (molar) = (1/liter)\n"
  "  (mM) = (millimolar)\n"
  "  (mA) = (milliamp)\n"
  "  (mV) = (millivolt)\n"
  "}\n"
  "\n"
  "NEURON {\n"
  "  SUFFIX gskch\n"
  "  USEION sk READ esk WRITE isk VALENCE 1\n"
  "  USEION nca READ ncai VALENCE 2\n"
  "  USEION lca READ lcai VALENCE 2\n"
  "  USEION tca READ tcai VALENCE 2\n"
  "  RANGE gsk, gskbar, qinf, qtau, isk\n"
  "}\n"
  "\n"
  "INDEPENDENT {\n"
  "  t FROM 0 TO 1 WITH 1 (ms)\n"
  "}\n"
  "\n"
  "PARAMETER {\n"
  "  celsius (degC)\n"
  "  v (mV)\n"
  "  dt (ms)\n"
  "  gskbar (mho/cm2)\n"
  "  esk  (mV)\n"
  "  cai (mM)\n"
  "  ncai (mM)\n"
  "  lcai (mM)\n"
  "  tcai (mM)\n"
  "}\n"
  "\n"
  "STATE {\n"
  "  q\n"
  "}\n"
  "\n"
  "ASSIGNED {\n"
  "  isk (mA/cm2)\n"
  "  gsk (mho/cm2)\n"
  "  qinf\n"
  "  qtau (ms)\n"
  "}\n"
  "\n"
  "BREAKPOINT {\n"
  "  SOLVE state\n"
  "  gsk = gskbar * q*q\n"
  "  isk = gsk * (v-esk)\n"
  "}\n"
  "\n"
  "INITIAL {\n"
  "  cai = ncai + lcai + tcai  \n"
  "  rates(cai)\n"
  "  q = qinf\n"
  "}\n"
  "\n"
  "LOCAL q10\n"
  "\n"
  "PROCEDURE state() {\n"
  "  cai = ncai + lcai + tcai\n"
  "  rates(cai)\n"
  "\n"
  "  q = q + (qinf - q) * (1 - exp(-dt * q10 / qtau) * q10)\n"
  "}\n"
  "\n"
  "PROCEDURE rates(cai) {\n"
  "  LOCAL alpha, beta\n"
  "  q10 = 3^((celsius - 6.3)/10)\n"
  "  \n"
  "  alpha = 1.25e1 * cai * cai\n"
  "  beta = 0.00025 \n"
  "\n"
  "  qtau = 1 / (alpha + beta)\n"
  "  qinf = alpha * qtau\n"
  "}\n"
  ;
#endif
