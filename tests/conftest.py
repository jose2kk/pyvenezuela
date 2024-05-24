"""CNE Fixtures"""

import pytest

from pyvenezuela.schemas import cne as cne_schemas


def build_cne_persona_model(**kwargs) -> cne_schemas.CNEPersonaModel:
    params = dict(
        id="V-27100100",
        full_name="First Second Third Fourth",
        state="EDO. ZULIA",
        municipality="MP. MARACAIBO",
        parish="PQ. CHIQUINQUIRA",
        voting_center="COLEGIO LA EPIFANIA",
        voting_center_address="MI CALLE A LA IZQUIERDA",
    )

    params.update(kwargs=kwargs)
    return cne_schemas.CNEPersonaModel.model_validate(params)


@pytest.fixture
def cne_persona_model() -> cne_schemas.CNEPersonaModel:
    return build_cne_persona_model()


def build_query_id_response_text(cne_persona: cne_schemas.CNEPersonaModel) -> str:
    return """
        <!--<a href="../../registro_electoral/impugnacionrenovacion.pdf" target="_blank"> DESCARGA LA PLANILLA</a>-->
        <table width="0" bgcolor="#90c1e2" border="0" cellpadding="1" cellspacing="1"><tr><td>
        <table width="-4" bgcolor="#ffffff" border="0" cellpadding="0" cellspacing="0"><tr><td>
        <table class="re_titulo_contenido"><tr><td class="re_titulo_contenido_texto">REGISTRO ELECTORAL - CONSULTA DE DATOS</td>
        <td align="center" width="30"><a href="javascript:ocultar_consulta_re();">
        <img src="/web/imagen/cerrar.png" border="0" width="20"></a></td>
        </tr><tr><td class="re_titulo_contenido_linea" colspan="10"/></td></tr>
        </table></td></tr><tr><td height="10"></td></tr><tr><td>
        <tr width="100%" border="0" cellspacing="0" cellpadding="0"><tr><td>
        <table width="100%" border="0" cellspacing="0" cellpadding="0">
        <tr><td colspan="2" bgcolor="#00387b" height="28" align="center"><font color="#FFFFFF">
        <b>DATOS DEL ELECTOR</b></font></td></tr><tr><td colspan="2"><table cellpadding="2" width="530"><tr>
        <td align="left"><b><font color="#00387b">Cédula:</font></b></td><td align="left">V-{id}</td>
        </tr><tr><td align="left"><b><font color="#00387b">Nombre:</font></b></td>
        <td align="left"><b>{full_name}</b></td></tr><tr>
        <td align="left"><b><font color="#00387b">Estado:</font></b></td><td align="left">{state}</td>
        </tr><tr><td align="left"><b><font color="#00387b">Municipio:</font></b></tdsta['descripcion'] = $s_res['descripcion'];>
        <td align="left">{municipality}</td></tr><tr><td align="left"><b><font color="#00387b">Parroquia:</font></b></td>
        <td align="left">{parish}</td></tr><tr><td align="left"><b><font color="#00387b">Centro:</font></b></td>
        <td align="left"><font color="#0000FF">{voting_center}</font></td></tr><tr>
        <td align="left"><b><font color="#00387b">Dirección:</font></b></td>
        <td align="left"><font color="#0000FF">{voting_center_address}</font></td>
        </tr></table><table cellpadding="2" width="530"><tr><!--<td colspan="2" bgcolor="#00387b" height="28" width="230" align="center"><font color="#FFFFFF"><b> VOTA en la Elección Constituyente </b></font></td>-->
        </tr><tr><!--<td align="left"><font color="#FF0000"> <center> TERRITORIAL </center></font> </td>-->
        </tr></table><table align="center" width="100%" bgcolor="#ffffff"><tr><td align="center" colspan="2"><b></b></td>
        </tr><br></table></td></tr><tr><td colspan="10"><hr></td></tr><tr bgcolor="#e4ebf3"><td colspan="10" align="center">
        <table><tr align="center"><td><a href="/web/registro_electoral/imprimir_datos_elector.php?nacionalidad=V&cedula=20726224" target="_blank"><img src="/web/imagen/impresora.png" border="0"></a></td>
        <td valign="middle"><a href="/web/registro_electoral/imprimir_datos_elector.php?nacionalidad=V&cedula=20726224" target="_blank">Impresión de Consulta de Datos</a></td>
        </tr></table></td></tr></table></td></tr></table>
    """.format(
        id=cne_persona.id.split("-")[1],
        full_name=cne_persona.full_name,
        state=cne_persona.state,
        municipality=cne_persona.municipality,
        parish=cne_persona.parish,
        voting_center=cne_persona.voting_center,
        voting_center_address=cne_persona.voting_center_address,
    )


def build_query_id_response_incomplete_text() -> str:
    return """
        <!--<a href="../../registro_electoral/impugnacionrenovacion.pdf" target="_blank"> DESCARGA LA PLANILLA</a>-->
        <table width="0" bgcolor="#90c1e2" border="0" cellpadding="1" cellspacing="1"><tr><td>
        <table width="-4" bgcolor="#ffffff" border="0" cellpadding="0" cellspacing="0"><tr><td>
        <table class="re_titulo_contenido"><tr><td class="re_titulo_contenido_texto">REGISTRO ELECTORAL - CONSULTA DE DATOS</td>
        <td align="center" width="30"><a href="javascript:ocultar_consulta_re();">
        <img src="/web/imagen/cerrar.png" border="0" width="20"></a></td>
        </tr><tr><td class="re_titulo_contenido_linea" colspan="10"/></td></tr>
        </table></td></tr><tr><td height="10"></td></tr><tr><td>
        <tr width="100%" border="0" cellspacing="0" cellpadding="0"><tr><td>
        <table width="100%" border="0" cellspacing="0" cellpadding="0">
        <tr><td colspan="2" bgcolor="#00387b" height="28" align="center"><font color="#FFFFFF">
        <b>DATOS DEL ELECTOR</b></font></td></tr><tr><td colspan="2"><table cellpadding="2" width="530"><tr>
        <td align="left"><b><font color="#00387b">Cédula:</font></b></td><td align="left">V-{id}</td>
        </tr><tr><td align="left"><b><font color="#00387b">Nombre:</font></b></td>
        <td align="left"><b>{full_name}</b></td></tr><tr>
        <td align="left"><b><font color="#00387b">Estado:</font></b></td><td align="left">{state}</td>
        </tr><tr><td align="left"><b><font color="#00387b">Municipio:</font></b></tdsta['descripcion'] = $s_res['descripcion'];>
        <td align="left">{municipality}</td></tr><tr><td align="left"><b><font color="#00387b">Parroquia:</font></b></td>
        <td align="left">{parish}</td></tr><tr><td align="left"><b><font color="#00387b">Centro:</font></b></td>
        <td align="left"><font color="#0000FF">{voting_center}</font></td></tr><tr>
        <td align="left"><b><font color="#00387b">Dirección:</font></b></td>
        </tr></table><table cellpadding="2" width="530"><tr><!--<td colspan="2" bgcolor="#00387b" height="28" width="230" align="center"><font color="#FFFFFF"><b> VOTA en la Elección Constituyente </b></font></td>-->
        </tr><tr><!--<td align="left"><font color="#FF0000"> <center> TERRITORIAL </center></font> </td>-->
        </tr></table><table align="center" width="100%" bgcolor="#ffffff"><tr><td align="center" colspan="2"><b></b></td>
        </tr><br></table></td></tr><tr><td colspan="10"><hr></td></tr><tr bgcolor="#e4ebf3"><td colspan="10" align="center">
        <table><tr align="center"><td><a href="/web/registro_electoral/imprimir_datos_elector.php?nacionalidad=V&cedula=20726224" target="_blank"><img src="/web/imagen/impresora.png" border="0"></a></td>
        <td valign="middle"><a href="/web/registro_electoral/imprimir_datos_elector.php?nacionalidad=V&cedula=20726224" target="_blank">Impresión de Consulta de Datos</a></td>
        </tr></table></td></tr></table></td></tr></table>
    """.format(
        id="27100100",
        full_name="First Second Third Fourth",
        state="EDO. ZULIA",
        municipality="MP. MARACAIBO",
        parish="PQ. CHIQUINQUIRA",
        voting_center="COLEGIO LA EPIFANIA",
    )
