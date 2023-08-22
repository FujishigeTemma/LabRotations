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
 
#define nrn_init _nrn_init__ichan2
#define _nrn_initial _nrn_initial__ichan2
#define nrn_cur _nrn_cur__ichan2
#define _nrn_current _nrn_current__ichan2
#define nrn_jacob _nrn_jacob__ichan2
#define nrn_state _nrn_state__ichan2
#define _net_receive _net_receive__ichan2 
#define rates rates__ichan2 
#define state state__ichan2 
 
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
#define gnatbar _p[0]
#define gnatbar_columnindex 0
#define gkfbar _p[1]
#define gkfbar_columnindex 1
#define gksbar _p[2]
#define gksbar_columnindex 2
#define gl _p[3]
#define gl_columnindex 3
#define el _p[4]
#define el_columnindex 4
#define gnat _p[5]
#define gnat_columnindex 5
#define gkf _p[6]
#define gkf_columnindex 6
#define gks _p[7]
#define gks_columnindex 7
#define inat _p[8]
#define inat_columnindex 8
#define ikf _p[9]
#define ikf_columnindex 9
#define iks _p[10]
#define iks_columnindex 10
#define il _p[11]
#define il_columnindex 11
#define mtau _p[12]
#define mtau_columnindex 12
#define htau _p[13]
#define htau_columnindex 13
#define nftau _p[14]
#define nftau_columnindex 14
#define nstau _p[15]
#define nstau_columnindex 15
#define minf _p[16]
#define minf_columnindex 16
#define hinf _p[17]
#define hinf_columnindex 17
#define nfinf _p[18]
#define nfinf_columnindex 18
#define nsinf _p[19]
#define nsinf_columnindex 19
#define m _p[20]
#define m_columnindex 20
#define h _p[21]
#define h_columnindex 21
#define nf _p[22]
#define nf_columnindex 22
#define ns _p[23]
#define ns_columnindex 23
#define enat _p[24]
#define enat_columnindex 24
#define ekf _p[25]
#define ekf_columnindex 25
#define eks _p[26]
#define eks_columnindex 26
#define Dm _p[27]
#define Dm_columnindex 27
#define Dh _p[28]
#define Dh_columnindex 28
#define Dnf _p[29]
#define Dnf_columnindex 29
#define Dns _p[30]
#define Dns_columnindex 30
#define v _p[31]
#define v_columnindex 31
#define _g _p[32]
#define _g_columnindex 32
#define _ion_enat	*_ppvar[0]._pval
#define _ion_inat	*_ppvar[1]._pval
#define _ion_dinatdv	*_ppvar[2]._pval
#define _ion_ekf	*_ppvar[3]._pval
#define _ion_ikf	*_ppvar[4]._pval
#define _ion_dikfdv	*_ppvar[5]._pval
#define _ion_eks	*_ppvar[6]._pval
#define _ion_iks	*_ppvar[7]._pval
#define _ion_diksdv	*_ppvar[8]._pval
 
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
 static void _hoc_vtrap(void);
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
 "setdata_ichan2", _hoc_setdata,
 "rates_ichan2", _hoc_rates,
 "state_ichan2", _hoc_state,
 "vtrap_ichan2", _hoc_vtrap,
 0, 0
};
#define vtrap vtrap_ichan2
 extern double vtrap( _threadargsprotocomma_ double , double );
 #define _zq10 _thread[0]._pval[0]
 /* declare global and static user variables */
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "gnatbar_ichan2", "mho/cm2",
 "gkfbar_ichan2", "mho/cm2",
 "gksbar_ichan2", "mho/cm2",
 "gl_ichan2", "mho/cm2",
 "el_ichan2", "mV",
 "gnat_ichan2", "mho/cm2",
 "gkf_ichan2", "mho/cm2",
 "gks_ichan2", "mho/cm2",
 "inat_ichan2", "mA/cm2",
 "ikf_ichan2", "mA/cm2",
 "iks_ichan2", "mA/cm2",
 "il_ichan2", "mA/cm2",
 "mtau_ichan2", "ms",
 "htau_ichan2", "ms",
 "nftau_ichan2", "ms",
 "nstau_ichan2", "ms",
 0,0
};
 static double delta_t = 1;
 static double h0 = 0;
 static double m0 = 0;
 static double ns0 = 0;
 static double nf0 = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
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
"ichan2",
 "gnatbar_ichan2",
 "gkfbar_ichan2",
 "gksbar_ichan2",
 "gl_ichan2",
 "el_ichan2",
 0,
 "gnat_ichan2",
 "gkf_ichan2",
 "gks_ichan2",
 "inat_ichan2",
 "ikf_ichan2",
 "iks_ichan2",
 "il_ichan2",
 "mtau_ichan2",
 "htau_ichan2",
 "nftau_ichan2",
 "nstau_ichan2",
 "minf_ichan2",
 "hinf_ichan2",
 "nfinf_ichan2",
 "nsinf_ichan2",
 0,
 "m_ichan2",
 "h_ichan2",
 "nf_ichan2",
 "ns_ichan2",
 0,
 0};
 static Symbol* _nat_sym;
 static Symbol* _kf_sym;
 static Symbol* _ks_sym;
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
 	_p = nrn_prop_data_alloc(_mechtype, 33, _prop);
 	/*initialize range parameters*/
 	gnatbar = 0;
 	gkfbar = 0;
 	gksbar = 0;
 	gl = 0;
 	el = 0;
 	_prop->param = _p;
 	_prop->param_size = 33;
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 9, _prop);
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 prop_ion = need_memb(_nat_sym);
 nrn_promote(prop_ion, 0, 1);
 	_ppvar[0]._pval = &prop_ion->param[0]; /* enat */
 	_ppvar[1]._pval = &prop_ion->param[3]; /* inat */
 	_ppvar[2]._pval = &prop_ion->param[4]; /* _ion_dinatdv */
 prop_ion = need_memb(_kf_sym);
 nrn_promote(prop_ion, 0, 1);
 	_ppvar[3]._pval = &prop_ion->param[0]; /* ekf */
 	_ppvar[4]._pval = &prop_ion->param[3]; /* ikf */
 	_ppvar[5]._pval = &prop_ion->param[4]; /* _ion_dikfdv */
 prop_ion = need_memb(_ks_sym);
 nrn_promote(prop_ion, 0, 1);
 	_ppvar[6]._pval = &prop_ion->param[0]; /* eks */
 	_ppvar[7]._pval = &prop_ion->param[3]; /* iks */
 	_ppvar[8]._pval = &prop_ion->param[4]; /* _ion_diksdv */
 
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

 void _ichan2_reg() {
	int _vectorized = 1;
  _initlists();
 	ion_reg("nat", 1.0);
 	ion_reg("kf", 1.0);
 	ion_reg("ks", 1.0);
 	_nat_sym = hoc_lookup("nat_ion");
 	_kf_sym = hoc_lookup("kf_ion");
 	_ks_sym = hoc_lookup("ks_ion");
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 2);
  _extcall_thread = (Datum*)ecalloc(1, sizeof(Datum));
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
  hoc_register_prop_size(_mechtype, 33, 9);
  hoc_register_dparam_semantics(_mechtype, 0, "nat_ion");
  hoc_register_dparam_semantics(_mechtype, 1, "nat_ion");
  hoc_register_dparam_semantics(_mechtype, 2, "nat_ion");
  hoc_register_dparam_semantics(_mechtype, 3, "kf_ion");
  hoc_register_dparam_semantics(_mechtype, 4, "kf_ion");
  hoc_register_dparam_semantics(_mechtype, 5, "kf_ion");
  hoc_register_dparam_semantics(_mechtype, 6, "ks_ion");
  hoc_register_dparam_semantics(_mechtype, 7, "ks_ion");
  hoc_register_dparam_semantics(_mechtype, 8, "ks_ion");
 	hoc_register_cvode(_mechtype, _ode_count, 0, 0, 0);
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 ichan2 /Users/temma/ghq/LabRotations/NCBC/src/mechanisms/ichan2.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
 static double FARADAY = 96520.0;
 static double R = 8.3134;
 /*Top LOCAL _zq10 */
static int _reset;
static char *modelname = "ichan2.mod";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
static int rates(_threadargsprotocomma_ double);
static int state(_threadargsproto_);
 
static int  state ( _threadargsproto_ ) {
   rates ( _threadargscomma_ v ) ;
   m = m + ( minf - m ) * ( 1.0 - exp ( - dt * _zq10 / mtau ) ) ;
   h = h + ( hinf - h ) * ( 1.0 - exp ( - dt * _zq10 / htau ) ) ;
   nf = nf + ( nfinf - nf ) * ( 1.0 - exp ( - dt * _zq10 / nftau ) ) ;
   ns = ns + ( nsinf - ns ) * ( 1.0 - exp ( - dt * _zq10 / nstau ) ) ;
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
 
static int  rates ( _threadargsprotocomma_ double _lv ) {
   double _lalpha , _lbeta , _lsum ;
 _zq10 = pow( 3.0 , ( ( celsius - 6.3 ) / 10.0 ) ) ;
   _lalpha = - 0.3 * vtrap ( _threadargscomma_ ( _lv + 60.0 - 17.0 ) , - 5.0 ) ;
   _lbeta = 0.3 * vtrap ( _threadargscomma_ ( _lv + 60.0 - 45.0 ) , 5.0 ) ;
   _lsum = _lalpha + _lbeta ;
   mtau = 1.0 / _lsum ;
   minf = _lalpha / _lsum ;
   _lalpha = 0.23 / exp ( ( _lv + 60.0 + 5.0 ) / 20.0 ) ;
   _lbeta = 3.33 / ( 1.0 + exp ( ( _lv + 60.0 - 47.5 ) / - 10.0 ) ) ;
   _lsum = _lalpha + _lbeta ;
   htau = 1.0 / _lsum ;
   hinf = _lalpha / _lsum ;
   _lalpha = - 0.028 * vtrap ( _threadargscomma_ ( _lv + 65.0 - 35.0 ) , - 6.0 ) ;
   _lbeta = 0.1056 / exp ( ( _lv + 65.0 - 10.0 ) / 40.0 ) ;
   _lsum = _lalpha + _lbeta ;
   nstau = 1.0 / _lsum ;
   nsinf = _lalpha / _lsum ;
   _lalpha = - 0.07 * vtrap ( _threadargscomma_ ( _lv + 65.0 - 47.0 ) , - 6.0 ) ;
   _lbeta = 0.264 / exp ( ( _lv + 65.0 - 22.0 ) / 40.0 ) ;
   _lsum = _lalpha + _lbeta ;
   nftau = 1.0 / _lsum ;
   nfinf = _lalpha / _lsum ;
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
 
double vtrap ( _threadargsprotocomma_ double _lx , double _ly ) {
   double _lvtrap;
 if ( fabs ( _lx / _ly ) < 1e-6 ) {
     _lvtrap = _ly * ( 1.0 - _lx / _ly / 2.0 ) ;
     }
   else {
     _lvtrap = _lx / ( exp ( _lx / _ly ) - 1.0 ) ;
     }
   
return _lvtrap;
 }
 
static void _hoc_vtrap(void) {
  double _r;
   double* _p; Datum* _ppvar; Datum* _thread; NrnThread* _nt;
   if (_extcall_prop) {_p = _extcall_prop->param; _ppvar = _extcall_prop->dparam;}else{ _p = (double*)0; _ppvar = (Datum*)0; }
  _thread = _extcall_thread;
  _nt = nrn_threads;
 _r =  vtrap ( _p, _ppvar, _thread, _nt, *getarg(1) , *getarg(2) );
 hoc_retpushx(_r);
}
 
static int _ode_count(int _type){ hoc_execerror("ichan2", "cannot be used with CVODE"); return 0;}
 
static void _thread_mem_init(Datum* _thread) {
   _thread[0]._pval = (double*)ecalloc(1, sizeof(double));
 }
 
static void _thread_cleanup(Datum* _thread) {
   free((void*)(_thread[0]._pval));
 }
 extern void nrn_update_ion_pointer(Symbol*, Datum*, int, int);
 static void _update_ion_pointer(Datum* _ppvar) {
   nrn_update_ion_pointer(_nat_sym, _ppvar, 0, 0);
   nrn_update_ion_pointer(_nat_sym, _ppvar, 1, 3);
   nrn_update_ion_pointer(_nat_sym, _ppvar, 2, 4);
   nrn_update_ion_pointer(_kf_sym, _ppvar, 3, 0);
   nrn_update_ion_pointer(_kf_sym, _ppvar, 4, 3);
   nrn_update_ion_pointer(_kf_sym, _ppvar, 5, 4);
   nrn_update_ion_pointer(_ks_sym, _ppvar, 6, 0);
   nrn_update_ion_pointer(_ks_sym, _ppvar, 7, 3);
   nrn_update_ion_pointer(_ks_sym, _ppvar, 8, 4);
 }

static void initmodel(double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt) {
  int _i; double _save;{
  h = h0;
  m = m0;
  ns = ns0;
  nf = nf0;
 {
   rates ( _threadargscomma_ v ) ;
   m = minf ;
   h = hinf ;
   nf = nfinf ;
   ns = nsinf ;
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
  enat = _ion_enat;
  ekf = _ion_ekf;
  eks = _ion_eks;
 initmodel(_p, _ppvar, _thread, _nt);
   }
}

static double _nrn_current(double* _p, Datum* _ppvar, Datum* _thread, NrnThread* _nt, double _v){double _current=0.;v=_v;{ {
   gnat = gnatbar * m * m * m * h ;
   inat = gnat * ( v - enat ) ;
   gkf = gkfbar * nf * nf * nf * nf ;
   ikf = gkf * ( v - ekf ) ;
   gks = gksbar * ns * ns * ns * ns ;
   iks = gks * ( v - eks ) ;
   il = gl * ( v - el ) ;
   }
 _current += inat;
 _current += ikf;
 _current += iks;
 _current += il;

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
  enat = _ion_enat;
  ekf = _ion_ekf;
  eks = _ion_eks;
 _g = _nrn_current(_p, _ppvar, _thread, _nt, _v + .001);
 	{ double _diks;
 double _dikf;
 double _dinat;
  _dinat = inat;
  _dikf = ikf;
  _diks = iks;
 _rhs = _nrn_current(_p, _ppvar, _thread, _nt, _v);
  _ion_dinatdv += (_dinat - inat)/.001 ;
  _ion_dikfdv += (_dikf - ikf)/.001 ;
  _ion_diksdv += (_diks - iks)/.001 ;
 	}
 _g = (_g - _rhs)/.001;
  _ion_inat += inat ;
  _ion_ikf += ikf ;
  _ion_iks += iks ;
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
  enat = _ion_enat;
  ekf = _ion_ekf;
  eks = _ion_eks;
 {  { state(_p, _ppvar, _thread, _nt); }
  }   }}

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
static const char* nmodl_filename = "/Users/temma/ghq/LabRotations/NCBC/src/mechanisms/ichan2.mod";
static const char* nmodl_file_text = 
  "TITLE ichan2.mod\n"
  "\n"
  "COMMENT\n"
  "the effect of conductivity change in soma.\n"
  "ENDCOMMENT\n"
  "\n"
  "NEURON { \n"
  "  SUFFIX ichan2\n"
  "  USEION nat READ enat WRITE inat VALENCE 1\n"
  "  USEION kf READ ekf WRITE ikf VALENCE 1\n"
  "  USEION ks READ eks WRITE iks VALENCE 1\n"
  "  NONSPECIFIC_CURRENT il\n"
  "  RANGE gnat, gkf, gks, gnatbar, gkfbar, gksbar, gl, el, minf, mtau, hinf, htau, nfinf, nftau, inat, ikf, nsinf, nstau, iks\n"
  "}\n"
  "\n"
  "UNITS {\n"
  "  (mA) =(milliamp)\n"
  "  (mV) =(millivolt)\n"
  "  (uF) = (microfarad)\n"
  "  (molar) = (1/liter)\n"
  "  (nA) = (nanoamp)\n"
  "  (mM) = (millimolar)\n"
  "  (um) = (micron)\n"
  "}\n"
  "\n"
  "UNITS {\n"
  "  FARADAY = 96520 (coul)\n"
  "  R = 8.3134  (joule/degC)\n"
  "}\n"
  "\n"
  "INDEPENDENT {\n"
  "  t FROM 0 TO 100 WITH 100 (ms)\n"
  "}\n"
  "\n"
  "PARAMETER {\n"
  "  celsius (degC)\n"
  "  v (mV)\n"
  "  dt (ms)\n"
  "  enat (mV)\n"
  "  gnatbar (mho/cm2)\n"
  "  ekf (mV)\n"
  "  gkfbar (mho/cm2)\n"
  "  eks (mV)\n"
  "  gksbar (mho/cm2)\n"
  "  gl (mho/cm2)\n"
  "  el (mV)\n"
  "}\n"
  "\n"
  "ASSIGNED {\n"
  "  gnat (mho/cm2) \n"
  "  gkf (mho/cm2)\n"
  "  gks (mho/cm2)\n"
  "\n"
  "  inat (mA/cm2)\n"
  "  ikf (mA/cm2)\n"
  "  iks (mA/cm2)\n"
  "  il (mA/cm2)\n"
  "\n"
  "  mtau (ms)\n"
  "  htau (ms)\n"
  "  nftau (ms)\n"
  "  nstau (ms)\n"
  "\n"
  "  minf\n"
  "  hinf\n"
  "  nfinf\n"
  "  nsinf\n"
  "}\n"
  "\n"
  "STATE {\n"
  "  m\n"
  "  h\n"
  "  nf\n"
  "  ns\n"
  "}\n"
  "\n"
  "BREAKPOINT {\n"
  "  SOLVE state\n"
  "  gnat = gnatbar * m * m * m * h  \n"
  "  inat = gnat * (v - enat)\n"
  "  gkf = gkfbar * nf * nf * nf * nf\n"
  "  ikf = gkf * (v-ekf)\n"
  "  gks = gksbar * ns * ns * ns * ns\n"
  "  iks = gks * (v-eks)\n"
  "  il = gl * (v-el)\n"
  "}\n"
  "\n"
  "INITIAL {\n"
  "  rates(v)\n"
  "  \n"
  "  m = minf\n"
  "  h = hinf\n"
  "  nf = nfinf\n"
  "  ns = nsinf\n"
  "}\n"
  "\n"
  "LOCAL q10\n"
  "\n"
  "PROCEDURE state() {\n"
  "  rates(v)\n"
  "\n"
  "  m = m + (minf - m) * (1 - exp(-dt * q10 / mtau))\n"
  "  h = h + (hinf - h) * (1 - exp(-dt * q10 / htau))\n"
  "  nf = nf + (nfinf - nf) * (1 - exp(-dt * q10 / nftau))\n"
  "  ns = ns + (nsinf - ns) * (1 - exp(-dt * q10 / nstau))\n"
  "}\n"
  "\n"
  ":Call once to initialize inf at resting v.\n"
  "PROCEDURE rates(v) {\n"
  "  LOCAL alpha, beta, sum\n"
  "  q10 = 3^((celsius - 6.3)/10)\n"
  "\n"
  "  :\"m\" sodium activation system - act and inact cross at -40\n"
  "  :\"m\" is the activation gate for the sodium current. It is voltage-dependent.\n"
  "  alpha = -0.3 * vtrap((v + 60 - 17), -5)\n"
  "  beta = 0.3 * vtrap((v + 60 - 45), 5)\n"
  "  sum = alpha + beta        \n"
  "  mtau = 1 / sum\n"
  "  minf = alpha / sum\n"
  "\n"
  "  :\"h\" sodium inactivation system\n"
  "  :\"h\" is the inactivation gate for the sodium current. It is also voltage-dependent.\n"
  "  alpha = 0.23 / exp((v + 60 + 5) / 20)\n"
  "  beta = 3.33 / (1 + exp((v + 60 - 47.5) / -10))\n"
  "  sum = alpha + beta\n"
  "  htau = 1 / sum \n"
  "  hinf = alpha / sum \n"
  "\n"
  "  :\"ns\" sKDR activation system\n"
  "  :\"ns\" is the activation gate for the slow Potassium (K) Rectifier current. It is voltage-dependent.\n"
  "  alpha = -0.028 * vtrap((v + 65 - 35), -6)\n"
  "  beta = 0.1056 / exp((v + 65 - 10) / 40)\n"
  "  sum = alpha + beta        \n"
  "  nstau = 1 / sum\n"
  "  nsinf = alpha / sum\n"
  "\n"
  "  :\"nf\" fKDR activation system\n"
  "  :\"nf\" is the activation gate for the fast Potassium (K) Rectifier current. It is voltage-dependent.\n"
  "  alpha = -0.07 * vtrap((v + 65 - 47), -6)\n"
  "  beta = 0.264 / exp((v + 65 - 22) / 40)\n"
  "  sum = alpha + beta        \n"
  "  nftau = 1 / sum\n"
  "  nfinf = alpha / sum\n"
  "}\n"
  "\n"
  "FUNCTION vtrap(x, y) {\n"
  "  if (fabs(x / y) < 1e-6) {\n"
  "    vtrap = y * (1 - x / y / 2)\n"
  "  } else {\n"
  "    vtrap = x / (exp(x / y) - 1)\n"
  "  }\n"
  "}\n"
  ;
#endif
