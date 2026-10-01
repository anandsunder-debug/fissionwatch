"""Generic planar flight integrator with an external-force interface.

For research reproducibility this model separates aerodynamics/inertia from any
force-generation mechanism. A caller may supply measured or externally computed
force/moment histories without embedding propulsion construction or combustion.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Optional
import numpy as np

@dataclass
class FlightState:
    x: float=0.0; y: float=0.0; vx: float=0.0; vy: float=0.0; theta: float=0.0; omega: float=0.0

@dataclass(frozen=True)
class FlightParameters:
    mass: float
    inertia: float
    rho: float=1.225
    gravity: float=9.81
    area: float=1e-4
    cd: float=0.5
    cl: float=0.0

def _rhs(state,p,force_moment):
    v=np.hypot(state.vx,state.vy)
    drag=0.5*p.rho*p.cd*p.area*v
    fx=-drag*state.vx; fy=-drag*state.vy
    lift=0.5*p.rho*p.cl*p.area*v*v
    if v>1e-12:
        fx += -lift*state.vy/v; fy += lift*state.vx/v
    ext_f=np.asarray(force_moment[:2],dtype=float)
    ext_m=float(force_moment[2])
    return np.array([state.vx,state.vy,(fx+ext_f[0])/p.mass,(fy+ext_f[1])/p.mass-state.theta*0+p.gravity*-1.0,state.omega,ext_m/p.inertia])

def simulate(initial: FlightState, p: FlightParameters, times, external_force: Optional[Callable[[float,FlightState],tuple]]=None):
    """Integrate with RK4. external_force returns (Fx,Fy,M); defaults to zero."""
    t=np.asarray(times,dtype=float)
    if len(t)<2 or np.any(np.diff(t)<=0): raise ValueError("times must be increasing")
    z=np.array([initial.x,initial.y,initial.vx,initial.vy,initial.theta,initial.omega],dtype=float)
    out=np.empty((len(t),6)); out[0]=z
    def deriv(tt,zz):
        s=FlightState(*zz); fm=external_force(tt,s) if external_force else (0.0,0.0,0.0)
        return _rhs(s,p,fm)
    for i in range(1,len(t)):
        dt=t[i]-t[i-1]; ti=t[i-1]
        k1=deriv(ti,z); k2=deriv(ti+dt/2,z+dt*k1/2); k3=deriv(ti+dt/2,z+dt*k2/2); k4=deriv(ti+dt,z+dt*k3)
        z += dt*(k1+2*k2+2*k3+k4)/6; out[i]=z
    return out
