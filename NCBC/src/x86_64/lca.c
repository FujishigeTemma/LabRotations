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
 
#define nrn_init _nrn_init__lca
#define _nrn_initial _nrn_initial__lca
#define nrn_cur _nrn_cur__lca
#define _nrn_current _nrn_current__lca
#define nrn_jacob _nrn_jacob__lca
#define nrn_state _nrn_state__lca
#define _net_receive _net_receive__lca 
#define rate rate__lca 
#define state state__lca 
 
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
#define glcabar _p[0]
#define glcabar_columnindex 0
#define ilca _p[1]
#define ilca_columnindex 1
#define m _p[2]
#define m_columnindex 2
#define cai _p[3]
#define cai_columnindex 3
#define cao _p[4]
#define cao_columnindex 4
#define Dm _p[5]
#define Dm_columnindex 5
#define glca _p[6]
#define glca_columnindex 6
#define elca _p[7]
#define elca_columnindex 7
#define _g _p[8]
#define _g_columnindex 8
#define _ion_elca	*_ppvar[0]._pval
#define _ion_ilca	*_ppvar[1]._pval
#define _ion_dilcadv	*_ppvar[2]._pval
#define _ion_cai	*_ppvar[3]._pval
#define _ion_cao	*_ppvar[4]._pval
 
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
 static void _hoc_KTF(void);
 static void _hoc_alp(void);
 static void _hoc_bet(void);
 static void _hoc_efun(void);
 static void _hoc_ghk(void);
 static void _hoc_h2(void);
 static void _hoc_rate(void);
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
 "setdata_lca", _hoc_setdata,
 "KTF_lca", _hoc_KTF,
 "alp_lca", _hoc_alp,
 "bet_lca", _hoc_bet,
 "efun_lca", _hoc_efun,
 "ghk_lca", _hoc_ghk,
 "h2_lca", _hoc_h2,
 "rate_lca", _hoc_rate,
 0, 0
};
#define KTF KTF_lca
#define _f_bet _f_bet_lca
#define _f_alp _f_alp_lca
#define alp alp_lca
#define bet bet_lca
#define efun efun_lca
#define ghk ghk_lca
#define h2 h2_lca
 extern double KTF( double );
 extern double _f_bet( double );
 extern double _f_alp( double );
 extern double alp( double );
 extern double bet( double );
 extern double efun( double );
 extern double ghk( double , double , double );
 extern double h2( double );
 /* declare global and static user variables */
#define ki ki_lca
 double ki = 0.001;
#define matu matu_lca
 double matu = 0;
#define minf minf_lca
 double minf = 0;
#define tfa tfa_lca
 double tfa = 1;
#define usetable usetable_lca
 double usetable = 1;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 "usetable_lca", 0, 1,
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "ki_lca", "mM",
 "matu_lca", "ms",
 "glcabar_lca", "mho/cm2",
 "ilca_lca", "mA/cm2",
 0,0
};
 static double delta_t = 0.01;
 static double m0 = 0;
 static double v = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 "ki_lca", &ki_lca,
 "tfa_lca", &tfa_lca,
 "minf_lca", &minf_lca,
 "matu_lca", &matu_lca,
 "usetable_lca", &usetable_lca,
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
 
#define _cvode_ieq _ppvar[5]._i
 static void _ode_matsol_instance1(_threadargsproto_);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"lca",
 "glcabar_lca",
 0,
 "ilca_lca",
 0,
 "m_lca",
 0,
 0};
 static Symbol* _lca_sym;
 static Symbol* _ca_sym;
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
 	_p = nrn_prop_data_alloc(_mechtype, 9, _prop);
 	/*initialize range parameters*/
 	glcabar = 0;
 	_prop->param = _p;
 	_prop->param_size = 9;
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 6, _prop);
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 prop_ion = need_memb(_lca_sym);
 nrn_promote(prop_ion, 0, 1);
 	_ppvar[0]._pval = &prop_ion->param[0]; /* elca */
 	_ppvar[1]._pval = &prop_ion->param[3]; /* ilca */
 	_ppvar[2]._pval = &prop_ion->param[4]; /* _ion_dilcadv */
 prop_ion = need_memb(_ca_sym);
 nrn_promote(prop_ion, 1, 0);
 	_ppvar[3]._pval = &prop_ion->param[1]; /* cai */
 	_ppvar[4]._pval = &prop_ion->param[2]; /* cao */
 
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

 void _lca_reg() {
	int _vectorized = 0;
  _initlists();
 	ion_reg("lca", 2.0);
 	ion_reg("ca", 2.0);
 	_lca_sym = hoc_lookup("lca_ion");
 	_ca_sym = hoc_lookup("ca_ion");
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 0);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
     _nrn_thread_reg(_mechtype, 2, _update_ion_pointer);
 #if NMODL_TEXT
  hoc_reg_nmodl_text(_mechtype, nmodl_file_text);
  hoc_reg_nmodl_filename(_mechtype, nmodl_filename);
#endif
  hoc_register_prop_size(_mechtype, 9, 6);
  hoc_register_dparam_semantics(_mechtype, 0, "lca_ion");
  hoc_register_dparam_semantics(_mechtype, 1, "lca_ion");
  hoc_register_dparam_semantics(_mechtype, 2, "lca_ion");
  hoc_register_dparam_semantics(_mechtype, 3, "ca_ion");
  hoc_register_dparam_semantics(_mechtype, 4, "ca_ion");
  hoc_register_dparam_semantics(_mechtype, 5, "cvodeieq");
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 lca /Users/temma/ghq/LabRotations/NCBC/src/mechanisms/lca.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
 static double FARADAY = 96520.0;
 static double R = 8.3134;
 static double KTOMV = .0853;
 static double *_t_alp;
 static double *_t_bet;
static int _reset;
static char *modelname = "l-calcium channel";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
static int rate(double);
 
static int _ode_spec1(_threadargsproto_);
/*static int _ode_matsol1(_threadargsproto_);*/
 static int _slist1[1], _dlist1[1];
 static int state(_threadargsproto_);
 static double _n_bet(double);
 static double _n_alp(double);
 
double h2 (  double _lcai ) {
   double _lh2;
 _lh2 = ki / ( ki + _lcai ) ;
   
return _lh2;
 }
 
static void _hoc_h2(void) {
  double _r;
   _r =  h2 (  *getarg(1) );
 hoc_retpushx(_r);
}
 
double ghk (  double _lv , double _lci , double _lco ) {
   double _lghk;
 double _lnu , _lf ;
 _lf = KTF ( _threadargscomma_ celsius ) / 2.0 ;
   _lnu = _lv / _lf ;
   _lghk = - _lf * ( 1. - ( _lci / _lco ) * exp ( _lnu ) ) * efun ( _threadargscomma_ _lnu ) ;
   
return _lghk;
 }
 
static void _hoc_ghk(void) {
  double _r;
   _r =  ghk (  *getarg(1) , *getarg(2) , *getarg(3) );
 hoc_retpushx(_r);
}
 
double KTF (  double _lcelsius ) {
   double _lKTF;
 _lKTF = ( ( 25. / 293.15 ) * ( _lcelsius + 273.15 ) ) ;
   
return _lKTF;
 }
 
static void _hoc_KTF(void) {
  double _r;
   _r =  KTF (  *getarg(1) );
 hoc_retpushx(_r);
}
 
double efun (  double _lz ) {
   double _lefun;
 if ( fabs ( _lz ) < 1e-4 ) {
     _lefun = 1.0 - _lz / 2.0 ;
     }
   else {
     _lefun = _lz / ( exp ( _lz ) - 1.0 ) ;
     }
   
return _lefun;
 }
 
static void _hoc_efun(void) {
  double _r;
   _r =  efun (  *getarg(1) );
 hoc_retpushx(_r);
}
 static double _mfac_alp, _tmin_alp;
 static void _check_alp();
 static void _check_alp() {
  static int _maktable=1; int _i, _j, _ix = 0;
  double _xi, _tmax;
  if (!usetable) {return;}
  if (_maktable) { double _x, _dx; _maktable=0;
   _tmin_alp =  - 150.0 ;
   _tmax =  150.0 ;
   _dx = (_tmax - _tmin_alp)/200.; _mfac_alp = 1./_dx;
   for (_i=0, _x=_tmin_alp; _i < 201; _x += _dx, _i++) {
    _t_alp[_i] = _f_alp(_x);
   }
  }
 }

 double alp(double _lv){ _check_alp();
 return _n_alp(_lv);
 }

 static double _n_alp(double _lv){ int _i, _j;
 double _xi, _theta;
 if (!usetable) {
 return _f_alp(_lv); 
}
 _xi = _mfac_alp * (_lv - _tmin_alp);
 if (isnan(_xi)) {
  return _xi; }
 if (_xi <= 0.) {
 return _t_alp[0];
 }
 if (_xi >= 200.) {
 return _t_alp[200];
 }
 _i = (int) _xi;
 return _t_alp[_i] + (_xi - (double)_i)*(_t_alp[_i+1] - _t_alp[_i]);
 }

 
double _f_alp (  double _lv ) {
   double _lalp;
 _lalp = 15.69 * ( - 1.0 * _lv + 81.5 ) / ( exp ( ( - 1.0 * _lv + 81.5 ) / 10.0 ) - 1.0 ) ;
   
return _lalp;
 }
 
static void _hoc_alp(void) {
  double _r;
    _r =  alp (  *getarg(1) );
 hoc_retpushx(_r);
}
 static double _mfac_bet, _tmin_bet;
 static void _check_bet();
 static void _check_bet() {
  static int _maktable=1; int _i, _j, _ix = 0;
  double _xi, _tmax;
  if (!usetable) {return;}
  if (_maktable) { double _x, _dx; _maktable=0;
   _tmin_bet =  - 150.0 ;
   _tmax =  150.0 ;
   _dx = (_tmax - _tmin_bet)/200.; _mfac_bet = 1./_dx;
   for (_i=0, _x=_tmin_bet; _i < 201; _x += _dx, _i++) {
    _t_bet[_i] = _f_bet(_x);
   }
  }
 }

 double bet(double _lv){ _check_bet();
 return _n_bet(_lv);
 }

 static double _n_bet(double _lv){ int _i, _j;
 double _xi, _theta;
 if (!usetable) {
 return _f_bet(_lv); 
}
 _xi = _mfac_bet * (_lv - _tmin_bet);
 if (isnan(_xi)) {
  return _xi; }
 if (_xi <= 0.) {
 return _t_bet[0];
 }
 if (_xi >= 200.) {
 return _t_bet[200];
 }
 _i = (int) _xi;
 return _t_bet[_i] + (_xi - (double)_i)*(_t_bet[_i+1] - _t_bet[_i]);
 }

 
double _f_bet (  double _lv ) {
   double _lbet;
 _lbet = 0.29 * exp ( - _lv / 10.86 ) ;
   
return _lbet;
 }
 
static void _hoc_bet(void) {
  double _r;
    _r =  bet (  *getarg(1) );
 hoc_retpushx(_r);
}
 
/*CVODE*/
 static int _ode_spec1 () {_reset=0;
 {
   rate ( _threadargscomma_ v ) ;
   Dm = ( minf - m ) / matu ;
   }
 return _reset;
}
 static int _ode_matsol1 () {
 rate ( _threadargscomma_ v ) ;
 Dm = Dm  / (1. - dt*( ( ( ( - 1.0 ) ) ) / matu )) ;
  return 0;
}
 /*END CVODE*/
 static int state () {_reset=0;
 {
   rate ( _threadargscomma_ v ) ;
    m = m + (1. - exp(dt*(( ( ( - 1.0 ) ) ) / matu)))*(- ( ( ( minf ) ) / matu ) / ( ( ( ( - 1.0 ) ) ) / matu ) - m) ;
   }
  return 0;
}
 
static int  rate (  double _lv ) {
   double _la ;
 _la = alp ( _threadargscomma_ _lv ) ;
   matu = 1.0 / ( tfa * ( _la + bet ( _threadargscomma_ _lv ) ) ) ;
   minf = tfa * _la * matu ;
    return 0; }
 
static void _hoc_rate(void) {
  double _r;
   _r = 1.;
 rate (  *getarg(1) );
 hoc_retpushx(_r);
}
 
static int _ode_count(int _type){ return 1;}
 
static void _ode_spec(NrnThread* _nt, _Memb_list* _ml, int _type) {
   Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
  elca = _ion_elca;
  cai = _ion_cai;
  cao = _ion_cao;
     _ode_spec1 ();
  }}
 
static void _ode_map(int _ieq, double** _pv, double** _pvdot, double* _pp, Datum* _ppd, double* _atol, int _type) { 
 	int _i; _p = _pp; _ppvar = _ppd;
	_cvode_ieq = _ieq;
	for (_i=0; _i < 1; ++_i) {
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
  elca = _ion_elca;
  cai = _ion_cai;
  cao = _ion_cao;
 _ode_matsol_instance1(_threadargs_);
 }}
 extern void nrn_update_ion_pointer(Symbol*, Datum*, int, int);
 static void _update_ion_pointer(Datum* _ppvar) {
   nrn_update_ion_pointer(_lca_sym, _ppvar, 0, 0);
   nrn_update_ion_pointer(_lca_sym, _ppvar, 1, 3);
   nrn_update_ion_pointer(_lca_sym, _ppvar, 2, 4);
   nrn_update_ion_pointer(_ca_sym, _ppvar, 3, 1);
   nrn_update_ion_pointer(_ca_sym, _ppvar, 4, 2);
 }

static void initmodel() {
  int _i; double _save;_ninits++;
 _save = t;
 t = 0.0;
{
  m = m0;
 {
   rate ( _threadargscomma_ v ) ;
   m = minf ;
   
/*VERBATIM*/
	cai=_ion_cai;
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
  elca = _ion_elca;
  cai = _ion_cai;
  cao = _ion_cao;
 initmodel();
 }}

static double _nrn_current(double _v){double _current=0.;v=_v;{ {
   glca = glcabar * m * m * h2 ( _threadargscomma_ cai ) ;
   ilca = glca * ghk ( _threadargscomma_ v , cai , cao ) ;
   }
 _current += ilca;

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
  elca = _ion_elca;
  cai = _ion_cai;
  cao = _ion_cao;
 _g = _nrn_current(_v + .001);
 	{ double _dilca;
  _dilca = ilca;
 _rhs = _nrn_current(_v);
  _ion_dilcadv += (_dilca - ilca)/.001 ;
 	}
 _g = (_g - _rhs)/.001;
  _ion_ilca += ilca ;
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
  elca = _ion_elca;
  cai = _ion_cai;
  cao = _ion_cao;
 { error =  state();
 if(error){fprintf(stderr,"at line 55 in file lca.mod:\n	SOLVE state METHOD cnexp\n"); nrn_complain(_p); abort_run(error);}
 } }}

}

static void terminal(){}

static void _initlists() {
 int _i; static int _first = 1;
  if (!_first) return;
   _t_alp = makevector(201*sizeof(double));
   _t_bet = makevector(201*sizeof(double));
 _slist1[0] = m_columnindex;  _dlist1[0] = Dm_columnindex;
_first = 0;
}

#if NMODL_TEXT
static const char* nmodl_filename = "/Users/temma/ghq/LabRotations/NCBC/src/mechanisms/lca.mod";
static const char* nmodl_file_text = 
  "TITLE l-calcium channel\n"
  ": l-type calcium channel\n"
  "\n"
  "\n"
  "UNITS {\n"
  "	(mA) = (milliamp)\n"
  "	(mV) = (millivolt)\n"
  "	(molar) = (1/liter)\n"
  "	(mM) = (millimolar)\n"
  "	FARADAY = 96520 (coul)\n"
  "	R = 8.3134 (joule/degC)\n"
  "	KTOMV = .0853 (mV/degC)\n"
  "}\n"
  "\n"
  "PARAMETER {\n"
  "	v (mV)\n"
  "	celsius (degC)\n"
  "	glcabar (mho/cm2)\n"
  "	ki=.001 (mM)\n"
  "	cai (mM)\n"
  "	cao (mM)\n"
  "  tfa=1\n"
  "}\n"
  "\n"
  "\n"
  "NEURON {\n"
  "	SUFFIX lca\n"
  "	USEION lca READ elca WRITE ilca VALENCE 2\n"
  "	USEION ca READ cai, cao VALENCE 2 \n"
  "  RANGE glcabar, cai, ilca, elca\n"
  "  GLOBAL minf,matu\n"
  "}\n"
  "\n"
  "STATE {\n"
  "	m\n"
  "}\n"
  "\n"
  "ASSIGNED {\n"
  "	ilca (mA/cm2)\n"
  "  glca (mho/cm2)\n"
  "  minf\n"
  "  matu (ms)\n"
  "	elca (mV)   \n"
  "}\n"
  "\n"
  "INITIAL {\n"
  "	rate(v)\n"
  "	m = minf\n"
  "	VERBATIM\n"
  "	cai=_ion_cai;\n"
  "	ENDVERBATIM\n"
  "}\n"
  "\n"
  "BREAKPOINT {\n"
  "	SOLVE state METHOD cnexp\n"
  "	glca = glcabar*m*m*h2(cai)\n"
  "	ilca = glca*ghk(v,cai,cao)\n"
  "\n"
  "}\n"
  "\n"
  "FUNCTION h2(cai(mM)) {\n"
  "	h2 = ki/(ki+cai)\n"
  "}\n"
  "\n"
  "\n"
  "FUNCTION ghk(v(mV), ci(mM), co(mM)) (mV) {\n"
  "  LOCAL nu,f\n"
  "\n"
  "  f = KTF(celsius)/2\n"
  "  nu = v/f\n"
  "  ghk=-f*(1. - (ci/co)*exp(nu))*efun(nu)\n"
  "}\n"
  "\n"
  "FUNCTION KTF(celsius (DegC)) (mV) {\n"
  "  KTF = ((25./293.15)*(celsius + 273.15))\n"
  "}\n"
  "\n"
  "\n"
  "FUNCTION efun(z) {\n"
  "	if (fabs(z) < 1e-4) {\n"
  "		efun = 1 - z/2\n"
  "	}else{\n"
  "		efun = z/(exp(z) - 1)\n"
  "	}\n"
  "}\n"
  "\n"
  "FUNCTION alp(v(mV)) (1/ms) {\n"
  "	TABLE FROM -150 TO 150 WITH 200\n"
  "	alp = 15.69*(-1.0*v+81.5)/(exp((-1.0*v+81.5)/10.0)-1.0)\n"
  "}\n"
  "\n"
  "FUNCTION bet(v(mV)) (1/ms) {\n"
  "	TABLE FROM -150 TO 150 WITH 200\n"
  "	bet = 0.29*exp(-v/10.86)\n"
  "}\n"
  "\n"
  "DERIVATIVE state {  \n"
  "  rate(v)\n"
  "  m' = (minf - m)/matu\n"
  "}\n"
  "\n"
  "PROCEDURE rate(v (mV)) { :callable from hoc\n"
  "  LOCAL a\n"
  "  a = alp(v)\n"
  "  matu = 1/(tfa*(a + bet(v)))\n"
  "  minf = tfa*a*matu\n"
  "}\n"
  ;
#endif
