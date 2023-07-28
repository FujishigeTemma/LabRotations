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
 
#define nrn_init _nrn_init__ccanl
#define _nrn_initial _nrn_initial__ccanl
#define nrn_cur _nrn_cur__ccanl
#define _nrn_current _nrn_current__ccanl
#define nrn_jacob _nrn_jacob__ccanl
#define nrn_state _nrn_state__ccanl
#define _net_receive _net_receive__ccanl 
#define integrate integrate__ccanl 
 
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
#define catau _p[0]
#define catau_columnindex 0
#define caiinf _p[1]
#define caiinf_columnindex 1
#define cai _p[2]
#define cai_columnindex 2
#define eca _p[3]
#define eca_columnindex 3
#define inca _p[4]
#define inca_columnindex 4
#define ilca _p[5]
#define ilca_columnindex 5
#define itca _p[6]
#define itca_columnindex 6
#define enca _p[7]
#define enca_columnindex 7
#define elca _p[8]
#define elca_columnindex 8
#define etca _p[9]
#define etca_columnindex 9
#define ncai _p[10]
#define ncai_columnindex 10
#define Dncai _p[11]
#define Dncai_columnindex 11
#define lcai _p[12]
#define lcai_columnindex 12
#define Dlcai _p[13]
#define Dlcai_columnindex 13
#define tcai _p[14]
#define tcai_columnindex 14
#define Dtcai _p[15]
#define Dtcai_columnindex 15
#define v _p[16]
#define v_columnindex 16
#define _g _p[17]
#define _g_columnindex 17
#define _ion_ncai	*_ppvar[0]._pval
#define _ion_inca	*_ppvar[1]._pval
#define _ion_enca	*_ppvar[2]._pval
#define _style_nca	*((int*)_ppvar[3]._pvoid)
#define _ion_lcai	*_ppvar[4]._pval
#define _ion_ilca	*_ppvar[5]._pval
#define _ion_elca	*_ppvar[6]._pval
#define _style_lca	*((int*)_ppvar[7]._pvoid)
#define _ion_tcai	*_ppvar[8]._pval
#define _ion_itca	*_ppvar[9]._pval
#define _ion_etca	*_ppvar[10]._pval
#define _style_tca	*((int*)_ppvar[11]._pvoid)
 
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
 static void _hoc_ktf(void);
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
 "setdata_ccanl", _hoc_setdata,
 "ktf_ccanl", _hoc_ktf,
 0, 0
};
#define ktf ktf_ccanl
 extern double ktf( _threadargsproto_ );
 /* declare global and static user variables */
#define cao cao_ccanl
 double cao = 2;
#define depth depth_ccanl
 double depth = 200;
#define ica ica_ccanl
 double ica = 0;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "depth_ccanl", "nm",
 "cao_ccanl", "mM",
 "ica_ccanl", "mA/cm2",
 "catau_ccanl", "ms",
 "caiinf_ccanl", "mM",
 "cai_ccanl", "mM",
 "eca_ccanl", "mV",
 0,0
};
 static double delta_t = 1;
 static double lcai0 = 0;
 static double ncai0 = 0;
 static double tcai0 = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 "depth_ccanl", &depth_ccanl,
 "cao_ccanl", &cao_ccanl,
 "ica_ccanl", &ica_ccanl,
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
 
#define _cvode_ieq _ppvar[12]._i
 static void _ode_matsol_instance1(_threadargsproto_);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"ccanl",
 "catau_ccanl",
 "caiinf_ccanl",
 "cai_ccanl",
 0,
 "eca_ccanl",
 0,
 0,
 0};
 static Symbol* _nca_sym;
 static Symbol* _lca_sym;
 static Symbol* _tca_sym;
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
 	_p = nrn_prop_data_alloc(_mechtype, 18, _prop);
 	/*initialize range parameters*/
 	catau = 9;
 	caiinf = 5e-05;
 	cai = 5e-05;
 	_prop->param = _p;
 	_prop->param_size = 18;
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 13, _prop);
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 prop_ion = need_memb(_nca_sym);
 nrn_check_conc_write(_prop, prop_ion, 1);
 nrn_promote(prop_ion, 3, 3);
 	_ppvar[0]._pval = &prop_ion->param[1]; /* ncai */
 	_ppvar[1]._pval = &prop_ion->param[3]; /* inca */
 	_ppvar[2]._pval = &prop_ion->param[0]; /* enca */
 	_ppvar[3]._pvoid = (void*)(&(prop_ion->dparam[0]._i)); /* iontype for nca */
 prop_ion = need_memb(_lca_sym);
 nrn_check_conc_write(_prop, prop_ion, 1);
 nrn_promote(prop_ion, 3, 3);
 	_ppvar[4]._pval = &prop_ion->param[1]; /* lcai */
 	_ppvar[5]._pval = &prop_ion->param[3]; /* ilca */
 	_ppvar[6]._pval = &prop_ion->param[0]; /* elca */
 	_ppvar[7]._pvoid = (void*)(&(prop_ion->dparam[0]._i)); /* iontype for lca */
 prop_ion = need_memb(_tca_sym);
 nrn_check_conc_write(_prop, prop_ion, 1);
 nrn_promote(prop_ion, 3, 3);
 	_ppvar[8]._pval = &prop_ion->param[1]; /* tcai */
 	_ppvar[9]._pval = &prop_ion->param[3]; /* itca */
 	_ppvar[10]._pval = &prop_ion->param[0]; /* etca */
 	_ppvar[11]._pvoid = (void*)(&(prop_ion->dparam[0]._i)); /* iontype for tca */
 
}
 static void _initlists();
  /* some states have an absolute tolerance */
 static Symbol** _atollist;
 static HocStateTolerance _hoc_state_tol[] = {
 0,0
};
 static void _thread_mem_init(Datum*);
 static void _thread_cleanup(Datum*);
 static void _update_ion_pointer(Datum*);
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
extern void _nrn_thread_table_reg(int, void(*)(double*, Datum*, Datum*, NrnThread*, int));
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 void _ccanl_reg() {
	int _vectorized = 1;
  _initlists();
 	ion_reg("nca", 2.0);
 	ion_reg("lca", 2.0);
 	ion_reg("tca", 2.0);
 	_nca_sym = hoc_lookup("nca_ion");
 	_lca_sym = hoc_lookup("lca_ion");
 	_tca_sym = hoc_lookup("tca_ion");
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 5);
  _extcall_thread = (Datum*)ecalloc(4, sizeof(Datum));
  _thread_mem_init(_extcall_thread);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
     _nrn_thread_reg(_mechtype, 1, _thread_mem_init);
     _nrn_thread_reg(_mechtype, 0, _thread_cleanup);
     _nrn_thread_reg(_mechtype, 2, _update_ion_pointer);
 #if NMODL_TEXT
  hoc_reg_nmodl_text(_mechtype, nmodl_file_text);
  hoc_reg_nmodl_filename(_mechtype, nmodl_filename);
#endif
  hoc_register_prop_size(_mechtype, 18, 13);
  hoc_register_dparam_semantics(_mechtype, 0, "nca_ion");
  hoc_register_dparam_semantics(_mechtype, 1, "nca_ion");
  hoc_register_dparam_semantics(_mechtype, 2, "nca_ion");
  hoc_register_dparam_semantics(_mechtype, 3, "#nca_ion");
  hoc_register_dparam_semantics(_mechtype, 4, "lca_ion");
  hoc_register_dparam_semantics(_mechtype, 5, "lca_ion");
  hoc_register_dparam_semantics(_mechtype, 6, "lca_ion");
  hoc_register_dparam_semantics(_mechtype, 7, "#lca_ion");
  hoc_register_dparam_semantics(_mechtype, 8, "tca_ion");
  hoc_register_dparam_semantics(_mechtype, 9, "tca_ion");
  hoc_register_dparam_semantics(_mechtype, 10, "tca_ion");
  hoc_register_dparam_semantics(_mechtype, 11, "#tca_ion");
  hoc_register_dparam_semantics(_mechtype, 12, "cvodeieq");
 	nrn_writes_conc(_mechtype, 0);
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 ccanl /Users/temma/ghq/LabRotations/NCBC/src/mechanisms/ccanl.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
 static double FARADAY = 96520.0;
 static double R = 8.3134;
static int _reset;
static char *modelname = "ccanl.mod";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
 
#define _deriv1_advance _thread[0]._i
#define _dith1 1
#define _recurse _thread[2]._i
#define _newtonspace1 _thread[3]._pvoid
 
static int _ode_spec1(_threadargsproto_);
/*static int _ode_matsol1(_threadargsproto_);*/
 static int _slist2[3];
  static int _slist1[3], _dlist1[3];
 static int integrate(_threadargsproto_);
 
/*CVODE*/
 static int _ode_spec1 (double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt) {int _reset = 0; {
   Dncai = - ( inca ) / depth / FARADAY * ( 1e7 ) + ( caiinf / 3.0 - ncai ) / catau ;
   Dlcai = - ( ilca ) / depth / FARADAY * ( 1e7 ) + ( caiinf / 3.0 - lcai ) / catau ;
   Dtcai = - ( itca ) / depth / FARADAY * ( 1e7 ) + ( caiinf / 3.0 - tcai ) / catau ;
   }
 return _reset;
}
 static int _ode_matsol1 (double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt) {
 Dncai = Dncai  / (1. - dt*( ( ( ( - 1.0 ) ) ) / catau )) ;
 Dlcai = Dlcai  / (1. - dt*( ( ( ( - 1.0 ) ) ) / catau )) ;
 Dtcai = Dtcai  / (1. - dt*( ( ( ( - 1.0 ) ) ) / catau )) ;
  return 0;
}
 /*END CVODE*/
 
static int integrate (double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt) {int _reset=0; int error = 0;
 { double* _savstate1 = _thread[_dith1]._pval;
 double* _dlist2 = _thread[_dith1]._pval + 3;
 int _counte = -1;
 if (!_recurse) {
 _recurse = 1;
 {int _id; for(_id=0; _id < 3; _id++) { _savstate1[_id] = _p[_slist1[_id]];}}
 error = nrn_newton_thread(_newtonspace1, 3,_slist2, _p, integrate, _dlist2, _ppvar, _thread, _nt);
 _recurse = 0; if(error) {abort_run(error);}}
 {
   Dncai = - ( inca ) / depth / FARADAY * ( 1e7 ) + ( caiinf / 3.0 - ncai ) / catau ;
   Dlcai = - ( ilca ) / depth / FARADAY * ( 1e7 ) + ( caiinf / 3.0 - lcai ) / catau ;
   Dtcai = - ( itca ) / depth / FARADAY * ( 1e7 ) + ( caiinf / 3.0 - tcai ) / catau ;
   {int _id; for(_id=0; _id < 3; _id++) {
if (_deriv1_advance) {
 _dlist2[++_counte] = _p[_dlist1[_id]] - (_p[_slist1[_id]] - _savstate1[_id])/dt;
 }else{
_dlist2[++_counte] = _p[_slist1[_id]] - _savstate1[_id];}}}
 } }
 return _reset;}
 
double ktf ( _threadargsproto_ ) {
   double _lktf;
 _lktf = ( 1000.0 ) * R * ( celsius + 273.15 ) / ( 2.0 * FARADAY ) ;
   
return _lktf;
 }
 
static void _hoc_ktf(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 _r =  ktf ( _p, _ppvar, _thread, _nt );
 hoc_retpushx(_r);
}
 
static int _ode_count(int _type){ return 3;}
 
static void _ode_spec(NrnThread* _nt, _Memb_list* _ml, int _type) {
   double* _p; Datum* _ppvar; Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
  ncai = _ion_ncai;
  inca = _ion_inca;
  enca = _ion_enca;
  ncai = _ion_ncai;
  lcai = _ion_lcai;
  ilca = _ion_ilca;
  elca = _ion_elca;
  lcai = _ion_lcai;
  tcai = _ion_tcai;
  itca = _ion_itca;
  etca = _ion_etca;
  tcai = _ion_tcai;
     _ode_spec1 (_p, _ppvar, _thread, _nt);
  _ion_enca = enca;
  _ion_ncai = ncai;
  _ion_elca = elca;
  _ion_lcai = lcai;
  _ion_etca = etca;
  _ion_tcai = tcai;
 }}
 
static void _ode_map(int _ieq, double** _pv, double** _pvdot, double* _pp, Datum* _ppd, double* _atol, int _type) { 
	double* _p; Datum* _ppvar;
 	int _i; _p = _pp; _ppvar = _ppd;
	_cvode_ieq = _ieq;
	for (_i=0; _i < 3; ++_i) {
		_pv[_i] = _pp + _slist1[_i];  _pvdot[_i] = _pp + _dlist1[_i];
		_cvode_abstol(_atollist, _atol, _i);
	}
 	_pv[0] = &(_ion_ncai);
 	_pv[1] = &(_ion_lcai);
 	_pv[2] = &(_ion_tcai);
 }
 
static void _ode_matsol_instance1(_threadargsproto_) {
 _ode_matsol1 (_p, _ppvar, _thread, _nt);
 }
 
static void _ode_matsol(NrnThread* _nt, _Memb_list* _ml, int _type) {
   double* _p; Datum* _ppvar; Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
  ncai = _ion_ncai;
  inca = _ion_inca;
  enca = _ion_enca;
  ncai = _ion_ncai;
  lcai = _ion_lcai;
  ilca = _ion_ilca;
  elca = _ion_elca;
  lcai = _ion_lcai;
  tcai = _ion_tcai;
  itca = _ion_itca;
  etca = _ion_etca;
  tcai = _ion_tcai;
 _ode_matsol_instance1(_threadargs_);
 }}
 
static void _thread_mem_init(Datum* _thread) {
   _thread[_dith1]._pval = (double*)ecalloc(6, sizeof(double));
   _newtonspace1 = nrn_cons_newtonspace(3);
 }
 
static void _thread_cleanup(Datum* _thread) {
   free((void*)(_thread[_dith1]._pval));
   nrn_destroy_newtonspace(_newtonspace1);
 }
 extern void nrn_update_ion_pointer(Symbol*, Datum*, int, int);
 static void _update_ion_pointer(Datum* _ppvar) {
   nrn_update_ion_pointer(_nca_sym, _ppvar, 0, 1);
   nrn_update_ion_pointer(_nca_sym, _ppvar, 1, 3);
   nrn_update_ion_pointer(_nca_sym, _ppvar, 2, 0);
   nrn_update_ion_pointer(_lca_sym, _ppvar, 4, 1);
   nrn_update_ion_pointer(_lca_sym, _ppvar, 5, 3);
   nrn_update_ion_pointer(_lca_sym, _ppvar, 6, 0);
   nrn_update_ion_pointer(_tca_sym, _ppvar, 8, 1);
   nrn_update_ion_pointer(_tca_sym, _ppvar, 9, 3);
   nrn_update_ion_pointer(_tca_sym, _ppvar, 10, 0);
 }

static void initmodel(double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt) {
  int _i; double _save;{
 {
   ncai = caiinf / 3.0 ;
   lcai = caiinf / 3.0 ;
   tcai = caiinf / 3.0 ;
   cai = caiinf ;
   eca = 130.0 ;
   enca = eca ;
   elca = eca ;
   etca = eca ;
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
  ncai = _ion_ncai;
  inca = _ion_inca;
  enca = _ion_enca;
  ncai = _ion_ncai;
  lcai = _ion_lcai;
  ilca = _ion_ilca;
  elca = _ion_elca;
  lcai = _ion_lcai;
  tcai = _ion_tcai;
  itca = _ion_itca;
  etca = _ion_etca;
  tcai = _ion_tcai;
 initmodel(_p, _ppvar, _thread, _nt);
  _ion_enca = enca;
  _ion_ncai = ncai;
  nrn_wrote_conc(_nca_sym, (&(_ion_ncai)) - 1, _style_nca);
  _ion_elca = elca;
  _ion_lcai = lcai;
  nrn_wrote_conc(_lca_sym, (&(_ion_lcai)) - 1, _style_lca);
  _ion_etca = etca;
  _ion_tcai = tcai;
  nrn_wrote_conc(_tca_sym, (&(_ion_tcai)) - 1, _style_tca);
}
}

static double _nrn_current(double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt, double _v){double _current=0.;v=_v;{
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
double _dtsav = dt;
if (secondorder) { dt *= 0.5; }
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
  ncai = _ion_ncai;
  inca = _ion_inca;
  enca = _ion_enca;
  ncai = _ion_ncai;
  lcai = _ion_lcai;
  ilca = _ion_ilca;
  elca = _ion_elca;
  lcai = _ion_lcai;
  tcai = _ion_tcai;
  itca = _ion_itca;
  etca = _ion_etca;
  tcai = _ion_tcai;
 {  _deriv1_advance = 1;
 derivimplicit_thread(3, _slist1, _dlist1, _p, integrate, _ppvar, _thread, _nt);
_deriv1_advance = 0;
     if (secondorder) {
    int _i;
    for (_i = 0; _i < 3; ++_i) {
      _p[_slist1[_i]] += dt*_p[_dlist1[_i]];
    }}
 } {
   cai = ncai + lcai + tcai ;
   eca = ktf ( _threadargs_ ) * log ( cao / cai ) ;
   enca = eca ;
   elca = eca ;
   etca = eca ;
   }
  _ion_enca = enca;
  _ion_ncai = ncai;
  _ion_elca = elca;
  _ion_lcai = lcai;
  _ion_etca = etca;
  _ion_tcai = tcai;
}}
 dt = _dtsav;
}

static void terminal(){}

static void _initlists(){
 double _x; double* _p = &_x;
 int _i; static int _first = 1;
  if (!_first) return;
 _slist1[0] = ncai_columnindex;  _dlist1[0] = Dncai_columnindex;
 _slist1[1] = lcai_columnindex;  _dlist1[1] = Dlcai_columnindex;
 _slist1[2] = tcai_columnindex;  _dlist1[2] = Dtcai_columnindex;
 _slist2[0] = lcai_columnindex;
 _slist2[1] = ncai_columnindex;
 _slist2[2] = tcai_columnindex;
_first = 0;
}

#if defined(__cplusplus)
} /* extern "C" */
#endif

#if NMODL_TEXT
static const char* nmodl_filename = "/Users/temma/ghq/LabRotations/NCBC/src/mechanisms/ccanl.mod";
static const char* nmodl_file_text = 
  "TITLE ccanl.mod\n"
  "\n"
  "COMMENT\n"
  "  calcium accumulation into a volume of area*depth next to the\n"
  "  membrane with a decay (time constant tau) to resting level\n"
  "  given by the global calcium variable cai0_ca_ion\n"
  "ENDCOMMENT\n"
  "\n"
  "NEURON {\n"
  "  SUFFIX ccanl\n"
  "  USEION nca READ ncai, inca, enca WRITE enca, ncai VALENCE 2\n"
  "  USEION lca READ lcai, ilca, elca WRITE elca, lcai VALENCE 2\n"
  "  USEION tca READ tcai, itca, etca WRITE etca, tcai VALENCE 2\n"
  "  RANGE caiinf, catau, cai, ncai, lcai,tcai, eca, elca, enca, etca\n"
  "}\n"
  "\n"
  "UNITS {\n"
  "  (mV) = (millivolt)\n"
  "  (molar) = (1/liter)\n"
  "  (mM) = (milli/liter)\n"
  "  (mA) = (milliamp)\n"
  "  FARADAY = 96520 (coul)\n"
  "  R = 8.3134  (joule/degC)\n"
  "}\n"
  "\n"
  "INDEPENDENT {t FROM 0 TO 100 WITH 100 (ms)}\n"
  "\n"
  "PARAMETER {\n"
  "  celsius = 6.3 (degC)\n"
  "  depth = 200 (nm)  : assume volume = area*depth\n"
  "  catau = 9 (ms)\n"
  "  caiinf = 50.e-6 (mM)\n"
  "  cao = 2 (mM)\n"
  "  ica (mA/cm2)\n"
  "  inca (mA/cm2)\n"
  "  ilca (mA/cm2)\n"
  "  itca (mA/cm2)\n"
  "  cai= 50.e-6 (mM)\n"
  "}\n"
  "\n"
  "ASSIGNED {\n"
  "  enca (mV)\n"
  "  elca (mV)\n"
  "  etca (mV)\n"
  "  eca (mV)\n"
  "}\n"
  "\n"
  "STATE {\n"
  "  ncai (mM)\n"
  "  lcai (mM)\n"
  "  tcai (mM)\n"
  "}\n"
  "\n"
  "INITIAL {\n"
  "  ncai=caiinf/3\n"
  "  lcai=caiinf/3\n"
  "  tcai=caiinf/3\n"
  "  cai = caiinf  \n"
  "  eca = 130  :ktf() * log(cao/caiinf)  \n"
  "  enca = eca\n"
  "  elca = eca\n"
  "  etca = eca\n"
  "}\n"
  "\n"
  "\n"
  "BREAKPOINT {\n"
  "  SOLVE integrate METHOD derivimplicit\n"
  "  cai = ncai+lcai+tcai  \n"
  "  eca = ktf() * log(cao/cai)  \n"
  "  enca = eca\n"
  "  elca = eca\n"
  "  etca = eca\n"
  "}\n"
  "\n"
  "DERIVATIVE integrate {\n"
  "  ncai' = -(inca)/depth/FARADAY * (1e7) + (caiinf/3 - ncai)/catau\n"
  "  lcai' = -(ilca)/depth/FARADAY * (1e7) + (caiinf/3 - lcai)/catau\n"
  "  tcai' = -(itca)/depth/FARADAY * (1e7) + (caiinf/3 - tcai)/catau\n"
  "}\n"
  "\n"
  "FUNCTION ktf() (mV) {\n"
  "  ktf = (1000)*R*(celsius +273.15)/(2*FARADAY)\n"
  "} \n"
  ;
#endif
