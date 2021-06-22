import numpy as np
from pystrict import strict
from PySDM.initialisation import spectral_sampling as spec_sampling
from PySDM.physics import si, Formulae, spectra, constants as const


@strict
class Settings:
    def __init__(self, dt: float, n_sd: int, n_substep: int,
                 kappa: float,
                 surface_tension: str = 'CompressedFilm',
                 spectral_sampling: spec_sampling.SpectralSampling = spec_sampling.Logarithmic):
        self.formulae = Formulae(surface_tension=surface_tension)

        self.t_max = (400 + 196) * si.s
        self.output_interval = 10 * si.s
        self.dt = dt

        self.w = .5 * si.m / si.s
        self.g = 10 * si.m / si.s**2

        self.n_sd = n_sd
        self.n_substep = n_substep

        self.p0 = 950 * si.mbar
        self.T0 = 285.2 * si.K
        pv0 = .95 * self.formulae.saturation_vapour_pressure.pvs_Celsius(self.T0 - const.T0)
        self.q0 = const.eps * pv0 / (self.p0 - pv0)
        self.kappa = kappa

        self.cloud_radius_range = (
                .5 * si.micrometre,
                25 * si.micrometre
        )

        self.mass_of_dry_air = 44

        # note: rho is not specified in the paper
        rho0 = 1

        self.r_dry, self.n_in_dv = spectral_sampling(
            spectrum=spectra.Lognormal(
                norm_factor=566 / si.cm**3 / rho0 * self.mass_of_dry_air,
                m_mode=.08 * si.um / 2,
                s_geom=2
            )
        ).sample(n_sd)
        
        self.dry_radius_bins_edges = np.logspace(np.log10(.01 * si.um), np.log10(1 * si.um), 51, endpoint=True) / 2
        self.wet_radius_bins_edges = np.logspace(np.log10(.1 * si.um), np.log10(10 * si.um), 51, endpoint=True) / 2


    @property
    def nt(self):
        nt = self.t_max / self.dt
        assert nt == int(nt)
        return int(nt)

    @property
    def steps_per_output_interval(self) -> int:
        return int(self.output_interval / self.dt)
