/* Created by Language version: 7.7.0 */
/* NOT VECTORIZED */
#define NRN_VECTORIZED 0
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
 
#define nrn_init _nrn_init__borgka
#define _nrn_initial _nrn_initial__borgka
#define nrn_cur _nrn_cur__borgka
#define _nrn_current _nrn_current__borgka
#define nrn_jacob _nrn_jacob__borgka
#define nrn_state _nrn_state__borgka
#define _net_receive _net_receive__borgka 
#define rates rates__borgka 
#define states states__borgka 
 
#define _threadargscomma_ /**/
#define _threadargsprotocomma_ /**/
#define _threadargs_ /**/
#define _threadargsproto_ /**/
 	/*SUPPRESS 761*/
	/*SUPPRESS 762*/
	/*SUPPRESS 763*/
	/*SUPPRESS 765*/
	 extern double *getarg();
 static double *_p; static Datum *_ppvar;
 
#define t nrn_threads->_t
#define dt nrn_threads->_dt
#define gkabar _p[0]
#define gkabar_columnindex 0
#define ik _p[1]
#define ik_columnindex 1
#define gka _p[2]
#define gka_columnindex 2
#define n _p[3]
#define n_columnindex 3
#define l _p[4]
#define l_columnindex 4
#define ek _p[5]
#define ek_columnindex 5
#define Dn _p[6]
#define Dn_columnindex 6
#define Dl _p[7]
#define Dl_columnindex 7
#define _g _p[8]
#define _g_columnindex 8
#define _ion_ek	*_ppvar[0]._pval
#define _ion_ik	*_ppvar[1]._pval
#define _ion_dikdv	*_ppvar[2]._pval
 
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
 /* external NEURON variables */
 extern double celsius;
 /* declaration of user functions */
 static void _hoc_rateL(void);
 static void _hoc_rateN(void);
 static void _hoc_rates(void);
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
 _p = _prop->param; _ppvar = _prop->dparam;
 }
 static void _hoc_setdata() {
 Prop *_prop, *hoc_getdata_range(int);
 _prop = hoc_getdata_range(_mechtype);
   _setdata(_prop);
 hoc_retpushx(1.);
}
 /* connect user functions to hoc names */
 static VoidFunc hoc_intfunc[] = {
 "setdata_borgka", _hoc_setdata,
 "rateL_borgka", _hoc_rateL,
 "rateN_borgka", _hoc_rateN,
 "rates_borgka", _hoc_rates,
 0, 0
};
#define rateL rateL_borgka
#define rateN rateN_borgka
 extern double rateL( double );
 extern double rateN( double );
 /* declare global and static user variables */
#define a0n a0n_borgka
 double a0n = 0.02;
#define a0l a0l_borgka
 double a0l = 0.08;
#define gml gml_borgka
 double gml = 1;
#define gmn gmn_borgka
 double gmn = 0.6;
#define linf linf_borgka
 double linf = 0;
#define ninf ninf_borgka
 double ninf = 0;
#define taun taun_borgka
 double taun = 0;
#define taul taul_borgka
 double taul = 0;
#define vhalfl vhalfl_borgka
 double vhalfl = -83;
#define vhalfn vhalfn_borgka
 double vhalfn = -33.6;
#define zetal zetal_borgka
 double zetal = 4;
#define zetan zetan_borgka
 double zetan = -3;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "vhalfn_borgka", "mV",
 "vhalfl_borgka", "mV",
 "a0l_borgka", "/ms",
 "a0n_borgka", "/ms",
 "zetan_borgka", "1",
 "zetal_borgka", "1",
 "gmn_borgka", "1",
 "gml_borgka", "1",
 "gkabar_borgka", "mho/cm2",
 "ik_borgka", "mA/cm2",
 0,0
};
 static double delta_t = 0.01;
 static double l0 = 0;
 static double n0 = 0;
 static double v = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 "vhalfn_borgka", &vhalfn_borgka,
 "vhalfl_borgka", &vhalfl_borgka,
 "a0l_borgka", &a0l_borgka,
 "a0n_borgka", &a0n_borgka,
 "zetan_borgka", &zetan_borgka,
 "zetal_borgka", &zetal_borgka,
 "gmn_borgka", &gmn_borgka,
 "gml_borgka", &gml_borgka,
 "taul_borgka", &taul_borgka,
 "taun_borgka", &taun_borgka,
 "ninf_borgka", &ninf_borgka,
 "linf_borgka", &linf_borgka,
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
static void _ode_map(int, double**, double**, double*, Datum*, double*, int);
static void _ode_spec(NrnThread*, _Memb_list*, int);
static void _ode_matsol(NrnThread*, _Memb_list*, int);
 
#define _cvode_ieq _ppvar[3]._i
 static void _ode_matsol_instance1(_threadargsproto_);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"borgka",
 "gkabar_borgka",
 0,
 "ik_borgka",
 "gka_borgka",
 0,
 "n_borgka",
 "l_borgka",
 0,
 0};
 static Symbol* _k_sym;
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
 	_p = nrn_prop_data_alloc(_mechtype, 9, _prop);
 	/*initialize range parameters*/
 	gkabar = 0.01;
 	_prop->param = _p;
 	_prop->param_size = 9;
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 4, _prop);
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 prop_ion = need_memb(_k_sym);
 nrn_promote(prop_ion, 0, 1);
 	_ppvar[0]._pval = &prop_ion->param[0]; /* ek */
 	_ppvar[1]._pval = &prop_ion->param[3]; /* ik */
 	_ppvar[2]._pval = &prop_ion->param[4]; /* _ion_dikdv */
 
}
 static void _initlists();
  /* some states have an absolute tolerance */
 static Symbol** _atollist;
 static HocStateTolerance _hoc_state_tol[] = {
 0,0
};
 static void _update_ion_pointer(Datum*);
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
extern void _nrn_thread_table_reg(int, void(*)(double*, Datum*, Datum*, NrnThread*, int));
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 void _borgka_reg() {
	int _vectorized = 0;
  _initlists();
 	ion_reg("k", -10000.);
 	_k_sym = hoc_lookup("k_ion");
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 0);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
     _nrn_thread_reg(_mechtype, 2, _update_ion_pointer);
 #if NMODL_TEXT
  hoc_reg_nmodl_text(_mechtype, nmodl_file_text);
  hoc_reg_nmodl_filename(_mechtype, nmodl_filename);
#endif
  hoc_register_prop_size(_mechtype, 9, 4);
  hoc_register_dparam_semantics(_mechtype, 0, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 1, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 2, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 3, "cvodeieq");
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 borgka /Users/temma/ghq/LabRotations/NCBC/src/mechanisms/borgka.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
static int _reset;
static char *modelname = "Borg-Graham type generic K-A channel";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
static int rates(double);
 
static int _ode_spec1(_threadargsproto_);
/*static int _ode_matsol1(_threadargsproto_);*/
 static int _slist1[2], _dlist1[2];
 static int states(_threadargsproto_);
 
double rateN (  double _lv ) {
   double _lrateN;
 _lrateN = exp ( 1e-3 * zetan * ( _lv - vhalfn ) * 9.648e4 / ( 8.315 * ( 273.16 + celsius ) ) ) ;
   
return _lrateN;
 }
 
static void _hoc_rateN(void) {
  double _r;
   _r =  rateN (  *getarg(1) );
 hoc_retpushx(_r);
}
 
double rateL (  double _lv ) {
   double _lrateL;
 _lrateL = exp ( 1e-3 * zetal * ( _lv - vhalfl ) * 9.648e4 / ( 8.315 * ( 273.16 + celsius ) ) ) ;
   
return _lrateL;
 }
 
static void _hoc_rateL(void) {
  double _r;
   _r =  rateL (  *getarg(1) );
 hoc_retpushx(_r);
}
 
/*CVODE*/
 static int _ode_spec1 () {_reset=0;
 {
   rates ( _threadargscomma_ v ) ;
   Dn = ( ninf - n ) / taun ;
   Dl = ( linf - l ) / taul ;
   }
 return _reset;
}
 static int _ode_matsol1 () {
 rates ( _threadargscomma_ v ) ;
 Dn = Dn  / (1. - dt*( ( ( ( - 1.0 ) ) ) / taun )) ;
 Dl = Dl  / (1. - dt*( ( ( ( - 1.0 ) ) ) / taul )) ;
  return 0;
}
 /*END CVODE*/
 static int states () {_reset=0;
 {
   rates ( _threadargscomma_ v ) ;
    n = n + (1. - exp(dt*(( ( ( - 1.0 ) ) ) / taun)))*(- ( ( ( ninf ) ) / taun ) / ( ( ( ( - 1.0 ) ) ) / taun ) - n) ;
    l = l + (1. - exp(dt*(( ( ( - 1.0 ) ) ) / taul)))*(- ( ( ( linf ) ) / taul ) / ( ( ( ( - 1.0 ) ) ) / taul ) - l) ;
   }
  return 0;
}
 
static int  rates (  double _lv ) {
   double _lalpha , _lq10 ;
 _lq10 = pow( 3.0 , ( ( celsius - 30.0 ) / 10.0 ) ) ;
   _lalpha = rateN ( _threadargscomma_ _lv ) ;
   ninf = 1.0 / ( 1.0 + _lalpha ) ;
   taun = 1.0 / ( _lq10 * a0n * ( 1.0 + _lalpha ) ) ;
   _lalpha = rateL ( _threadargscomma_ _lv ) ;
   linf = 1.0 / ( 1.0 + _lalpha ) ;
   taul = 1.0 / ( _lq10 * a0l * ( 1.0 + _lalpha ) ) ;
    return 0; }
 
static void _hoc_rates(void) {
  double _r;
   _r = 1.;
 rates (  *getarg(1) );
 hoc_retpushx(_r);
}
 
static int _ode_count(int _type){ return 2;}
 
static void _ode_spec(NrnThread* _nt, _Memb_list* _ml, int _type) {
   Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
  ek = _ion_ek;
     _ode_spec1 ();
  }}
 
static void _ode_map(int _ieq, double** _pv, double** _pvdot, double* _pp, Datum* _ppd, double* _atol, int _type) { 
 	int _i; _p = _pp; _ppvar = _ppd;
	_cvode_ieq = _ieq;
	for (_i=0; _i < 2; ++_i) {
		_pv[_i] = _pp + _slist1[_i];  _pvdot[_i] = _pp + _dlist1[_i];
		_cvode_abstol(_atollist, _atol, _i);
	}
 }
 
static void _ode_matsol_instance1(_threadargsproto_) {
 _ode_matsol1 ();
 }
 
static void _ode_matsol(NrnThread* _nt, _Memb_list* _ml, int _type) {
   Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
  ek = _ion_ek;
 _ode_matsol_instance1(_threadargs_);
 }}
 extern void nrn_update_ion_pointer(Symbol*, Datum*, int, int);
 static void _update_ion_pointer(Datum* _ppvar) {
   nrn_update_ion_pointer(_k_sym, _ppvar, 0, 0);
   nrn_update_ion_pointer(_k_sym, _ppvar, 1, 3);
   nrn_update_ion_pointer(_k_sym, _ppvar, 2, 4);
 }

static void initmodel() {
  int _i; double _save;_ninits++;
 _save = t;
 t = 0.0;
{
  l = l0;
  n = n0;
 {
   rates ( _threadargscomma_ v ) ;
   n = ninf ;
   l = linf ;
   }
  _sav_indep = t; t = _save;

}
}

static void nrn_init(NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; double _v; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
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
  ek = _ion_ek;
 initmodel();
 }}

static double _nrn_current(double _v){double _current=0.;v=_v;{ {
   gka = gkabar * n * l ;
   ik = gka * ( v - ek ) ;
   }
 _current += ik;

} return _current;
}

static void nrn_cur(NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; int* _ni; double _rhs, _v; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
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
  ek = _ion_ek;
 _g = _nrn_current(_v + .001);
 	{ double _dik;
  _dik = ik;
 _rhs = _nrn_current(_v);
  _ion_dikdv += (_dik - ik)/.001 ;
 	}
 _g = (_g - _rhs)/.001;
  _ion_ik += ik ;
#if CACHEVEC
  if (use_cachevec) {
	VEC_RHS(_ni[_iml]) -= _rhs;
  }else
#endif
  {
	NODERHS(_nd) -= _rhs;
  }
 
}}

static void nrn_jacob(NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
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
 
}}

static void nrn_state(NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; double _v = 0.0; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
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
  ek = _ion_ek;
 { error =  states();
 if(error){fprintf(stderr,"at line 51 in file borgka.mod:\n  SOLVE states METHOD cnexp\n"); nrn_complain(_p); abort_run(error);}
 } }}

}

static void terminal(){}

static void _initlists() {
 int _i; static int _first = 1;
  if (!_first) return;
 _slist1[0] = n_columnindex;  _dlist1[0] = Dn_columnindex;
 _slist1[1] = l_columnindex;  _dlist1[1] = Dl_columnindex;
_first = 0;
}

#if NMODL_TEXT
static const char* nmodl_filename = "/Users/temma/ghq/LabRotations/NCBC/src/mechanisms/borgka.mod";
static const char* nmodl_file_text = 
  "TITLE Borg-Graham type generic K-A channel\n"
  "\n"
  "UNITS {\n"
  "  (mA) = (milliamp)\n"
  "  (mV) = (millivolt)\n"
  "}\n"
  "\n"
  "PARAMETER {\n"
  "  v (mV)\n"
  "  ek (mV)\n"
  "  celsius (degC)\n"
  "  gkabar=.01 (mho/cm2)\n"
  "  vhalfn=-33.6 (mV)\n"
  "  vhalfl=-83 (mV)\n"
  "  a0l=0.08 (/ms)\n"
  "  a0n=0.02 (/ms)\n"
  "  zetan=-3 (1)\n"
  "  zetal=4 (1)\n"
  "  gmn=0.6 (1)\n"
  "  gml=1 (1)\n"
  "}\n"
  "\n"
  "NEURON {\n"
  "  SUFFIX borgka\n"
  "  USEION k READ ek WRITE ik\n"
  "  RANGE gkabar,gka, ik\n"
  "  GLOBAL ninf, linf, taul, taun\n"
  "}\n"
  "\n"
  "STATE {\n"
  "  n\n"
  "  l\n"
  "}\n"
  "\n"
  "INITIAL {\n"
  "  rates(v)\n"
  "  n = ninf\n"
  "  l = linf\n"
  "}\n"
  "\n"
  "ASSIGNED {\n"
  "  ik (mA/cm2)\n"
  "  gka\n"
  "  taul\n"
  "  taun\n"
  "  ninf\n"
  "  linf      \n"
  "}\n"
  "\n"
  "BREAKPOINT {\n"
  "  SOLVE states METHOD cnexp\n"
  "  gka = gkabar*n*l\n"
  "  ik = gka*(v-ek)\n"
  "}\n"
  "\n"
  "FUNCTION rateN(v(mV)) {\n"
  "  rateN = exp(1e-3 * zetan * (v - vhalfn) * 9.648e4 / (8.315 * (273.16 + celsius))) \n"
  "}\n"
  "\n"
  "FUNCTION rateL(v(mV)) {\n"
  "  rateL = exp(1e-3 * zetal * (v - vhalfl) * 9.648e4 / (8.315 * (273.16 + celsius))) \n"
  "}\n"
  "\n"
  "DERIVATIVE states { \n"
  "  rates(v)\n"
  "  n' = (ninf - n) / taun\n"
  "  l' = (linf - l) / taul\n"
  "}\n"
  "\n"
  "PROCEDURE rates(v (mV)) {\n"
  "  LOCAL alpha, q10\n"
  "  q10 = 3 ^ ((celsius - 30) / 10)\n"
  "  alpha = rateN(v)\n"
  "  ninf = 1 / (1 + alpha)\n"
  "  taun = 1 / (q10 * a0n * (1 + alpha))\n"
  "  alpha = rateL(v)\n"
  "  linf = 1 / (1 + alpha)\n"
  "  taul = 1 / (q10 * a0l * (1 + alpha))\n"
  "}\n"
  ;
#endif
