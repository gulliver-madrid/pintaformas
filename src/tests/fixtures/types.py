from dataclasses import dataclass, field
from typing import Any, Optional, Sequence, Union

from ...pintaformas.log_pintaformas import log, cat


@dataclass
class DetalleClaseConFallos:
    clase: type
    slots_sin_anotacion: list[str] = field(default_factory=list)

TipoAnotacion= object

def obtener_fallos(clases: Sequence[type]) -> tuple[list[DetalleClaseConFallos], int]:
    clases_con_fallos: list[type] = []
    contador_fallos = 0
    fallos: list[DetalleClaseConFallos] = []
    for clase in clases:
        if clase in clases_con_fallos:
            continue
        slots: Optional[Union[str, list[str], tuple[str]]]
        slots = []
        annotations: dict[str, TipoAnotacion] = {}
        if '__slots__' not in clase.__dict__:
            continue
        clases_mro = clase.mro()
        for mro_clase in clases_mro:
            if mro_clase is not object:
                mro_clase_slots = mro_clase.__dict__.get('__slots__')
                if mro_clase_slots is None:
                    raise AssertionError("Una superclase de {clase.__name__} no define __slots__: {mro_clase.__name__}")
                if isinstance(mro_clase_slots, str):
                    mro_clase_slots = [mro_clase_slots]
                assert isinstance(mro_clase_slots, (list, tuple)), mro_clase_slots
                slots.extend(mro_clase_slots)
        for mro_clase in clases_mro:
            if mro_clase is not object:
                mro_clase_annotations = mro_clase.__dict__.get('__annotations__')
                if mro_clase_annotations is None:
                    continue
                assert isinstance(mro_clase_annotations, dict), (mro_clase, mro_clase_annotations)
                annotations.update(mro_clase_annotations)

        detalle_clase_con_fallos = None
        for slot in slots:
            # print("Revisando", slot)
            if slot not in annotations:
                if not detalle_clase_con_fallos:
                    detalle_clase_con_fallos = DetalleClaseConFallos(clase)
                assert detalle_clase_con_fallos
                detalle_clase_con_fallos.slots_sin_anotacion.append(slot)
                contador_fallos += 1
        for annotation in annotations:
            if annotation not in slots:
                # TODO: hacer que no se detenga al primer fallo
                msj = f"El atributo {annotation} definido en {clase.__name__} no esta incluido en __slots__"
                if "ClassVar" in repr(annotations[annotation]):
                    # Al ser una variable de clase, no se define en __slots__
                    continue
                raise AssertionError(msj)
        if detalle_clase_con_fallos:
            clases_con_fallos.append(clase)
            fallos.append(detalle_clase_con_fallos)
    log.anotar(f"Revisadas {len(clases)} clases", cat.tests)
    return fallos, contador_fallos

# Tests

# Fail


class ClasePruebaFail:
    __slots__ = ('slot_sin_anotacion_en_clase_prueba')


fallos, contador_fallos = obtener_fallos([ClasePruebaFail])
assert contador_fallos == 1
assert fallos[0].slots_sin_anotacion[0] == 'slot_sin_anotacion_en_clase_prueba'

# Ok


class ClasePruebaOk:
    __slots__ = ('slot_con_anotacion_en_clase_prueba')
    slot_con_anotacion_en_clase_prueba: object


fallos, contador_fallos = obtener_fallos([ClasePruebaOk])
assert contador_fallos == 0
assert not fallos
