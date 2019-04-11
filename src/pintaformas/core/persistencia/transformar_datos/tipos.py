from typing import  Union

DiccionarioStrObject = dict[str, object]
DatosNormalizadosDiccionario = DiccionarioStrObject
DatosNormalizadosLista = list[DiccionarioStrObject]
DatosNormalizadosUniversales = Union[DatosNormalizadosDiccionario, DatosNormalizadosLista]
