from typing import TYPE_CHECKING, Protocol, TypeVar

from ..core.ajustes_generales import AjustesGenerales
from ..core.general.app_protocol import AppProtocol
from ..core.general.medidor_tiempo import MedidorTiempo
from .metacomponentes import MetaComponentes


App = TypeVar('App', bound=AppProtocol, covariant=True)


class ConstructorAppProtocol(Protocol[App]):
    medidor_tiempo: MedidorTiempo

    def crear_app(self, titulo: str) -> App:
        ...


class ProgramaProtocol(Protocol[App]):
    def __init__(self,
            ajustes: AjustesGenerales,
            metacomponentes: MetaComponentes,
            constructor_app: ConstructorAppProtocol[App]
            ) -> None:
            ...

    def ejecutar_programa(self) -> None:
        ...


if TYPE_CHECKING:
    # Al ser covariante, puede pasarse el generico de la derivada donde se espera al generico de la base.
    # Es decir, donde se espera el constructor de una base, puede pasarse el constructor de una derivada.
    class AppBase(AppProtocol):
        ...

    class AppDerivada(AppBase):
        ...

    app_base: AppBase
    app_derivada: AppDerivada

    class ConstructorAppBase(ConstructorAppProtocol[AppBase]):
        ...

    constructor_app_base: ConstructorAppBase
    constructor_app_base_protocol: ConstructorAppProtocol[AppBase]
    constructor_app_base_protocol = constructor_app_base  # cumple el protocolo

    constructor_app_derivada: ConstructorAppProtocol[AppDerivada]
    constructor_app_base_protocol = constructor_app_derivada  # covariante, lo contrario no se cumple

    programa_base: ProgramaProtocol[AppBase]
    programa_derivada: ProgramaProtocol[AppDerivada]
    programa_base = programa_derivada  # covariante, lo contrario no se cumple
