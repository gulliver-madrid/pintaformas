
from ...tipos import Color, CodigoAreaPF
from ... import cfg
from .area import Area
from ..capas.capa import Capa
from ...general.control_cambios import ControlDeCambios
from ..capas.capas_area_dibujo import CapasAreaDibujo



class AreaDibujo(Area):
    __slots__ = ('fondo', 'capas', 'capas_internas', 'control_cambios')
    capas_internas: list[Capa]
    fondo: Color
    capas: CapasAreaDibujo
    control_cambios: ControlDeCambios

    def __init__(self, capas_area_dibujo: CapasAreaDibujo, control_cambios: ControlDeCambios):
        self._codigo = CodigoAreaPF.area_dibujo
        self.surface = None
        self.fondo = Color(cfg.COLOR_FONDO)
        self.capas = capas_area_dibujo
        self.capas_internas = capas_area_dibujo.todas
        self.control_cambios = control_cambios


    def reestablecer_fondo(self) -> None:
        assert self.surface
        self.surface.fill(self.fondo)
