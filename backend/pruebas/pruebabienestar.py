from fastapi.testclient import TestClient
from sqlalchemy import text
from app.core.database import SessionLocal
from app.main import app

c = TestClient(app)
c.headers["Authorization"] = "Bearer " + c.post(
    "/api/auth/login", json={"nomusu": "admin", "clausu": "admin123"}
).json()["token"]
fallos = []

def check(nombre, resp, esperado, campo=None, valor=None):
    ok = resp.status_code == esperado
    if ok and campo is not None:
        ok = resp.json().get(campo) == valor
    print(("OK   " if ok else "FALLO"), nombre, resp.status_code, "" if ok else resp.text[:300])
    if not ok:
        fallos.append(nombre)
    return resp

def contar(tabla):
    with SessionLocal() as s:
        return s.execute(text(f"select count(*) from {tabla}")).scalar()

antes = contar("ctrl_cita")

# ---- servicios
r = check("listar servicios", c.get("/api/servicios"), 200); assert len(r.json()) == 3
check("servicio duplicado", c.post("/api/servicios", json={"nomserv": "Psicología"}), 409)
r = check("crear servicio", c.post("/api/servicios", json={"nomserv": "Nutrición", "descserv": "Control nutricional"}), 201)
nuevoserv = r.json()["codserv"]
check("editar servicio", c.put(f"/api/servicios/{nuevoserv}", json={"nomserv": "Nutrición clínica"}), 200, "nomserv", "Nutrición clínica")
check("servicio con personal no se elimina", c.delete("/api/servicios/1"), 409)
check("servicio inexistente", c.get("/api/servicios/99"), 404)

# ---- personal
check("listar personal", c.get("/api/personal"), 200)
base = {"nomper": "Ana", "apeper": "Rojas", "dniper": "71000001", "corrper": "ana@udh.edu.pe", "cargoper": "Nutricionista", "codserv": nuevoserv}
check("DNI inválido", c.post("/api/personal", json={**base, "dniper": "123"}), 422)
check("servicio inexistente", c.post("/api/personal", json={**base, "codserv": 99}), 404)
r = check("crear personal", c.post("/api/personal", json=base), 201); nuevoper = r.json()["codper"]
check("DNI repetido", c.post("/api/personal", json={**base, "corrper": "otra@udh.edu.pe"}), 409)
check("correo repetido", c.post("/api/personal", json={**base, "dniper": "71000002"}), 409)
check("editar personal", c.put(f"/api/personal/{nuevoper}", json={**base, "cargoper": "Jefa de nutrición"}), 200, "cargoper", "Jefa de nutrición")
check("servicio con personal ahora no se elimina", c.delete(f"/api/servicios/{nuevoserv}"), 409)
check("eliminar personal", c.delete(f"/api/personal/{nuevoper}"), 204)
check("eliminar servicio", c.delete(f"/api/servicios/{nuevoserv}"), 204)
check("personal con citas no se elimina", c.delete("/api/personal/1"), 409)

# ---- citas (p04)
r = check("listar citas", c.get("/api/citas"), 200); print("   total:", len(r.json()), "| primera:", r.json()[0]["estudiante"]["apeest"], r.json()[0]["horacita"])
assert all(x["codest"] == 1 for x in c.get("/api/citas?codest=1").json())
assert all(x["estcita"] == "PROGRAMADA" for x in c.get("/api/citas?estcita=PROGRAMADA").json())
nueva = {"codest": 4, "codper": 2, "fechcita": "2026-12-01", "horacita": "10:00:00", "modcita": "VIRTUAL", "motcita": "Control"}
check("estudiante inexistente", c.post("/api/citas", json={**nueva, "codest": 99}), 404)
check("profesional inexistente", c.post("/api/citas", json={**nueva, "codper": 99}), 404)
check("fecha pasada", c.post("/api/citas", json={**nueva, "fechcita": "2020-01-01"}), 422)
check("modalidad inválida", c.post("/api/citas", json={**nueva, "modcita": "TELEFONO"}), 422)
r = check("horario ocupado", c.post("/api/citas", json={**nueva, "codper": 1, "fechcita": "2026-11-20", "horacita": "09:00:00"}), 409); print("   ", r.json())
r = check("registrar cita", c.post("/api/citas", json=nueva), 201, "estcita", "PROGRAMADA"); cita = r.json()["codcita"]
check("mismo horario otra vez", c.post("/api/citas", json=nueva), 409)
check("cancelar", c.put(f"/api/citas/{cita}/estado", json={"estcita": "CANCELADA"}), 200, "estcita", "CANCELADA")
check("cancelar de nuevo", c.put(f"/api/citas/{cita}/estado", json={"estcita": "NO_ASISTIO"}), 409)
check("estado no permitido", c.put(f"/api/citas/{cita}/estado", json={"estcita": "ATENDIDA"}), 422)
check("cita con atención no se elimina", c.delete("/api/citas/1"), 409)
check("eliminar cita cancelada", c.delete(f"/api/citas/{cita}"), 204)
check("cita inexistente", c.get(f"/api/citas/{cita}"), 404)

# ---- atenciones (p05)
r = check("listar atenciones", c.get("/api/atenciones"), 200); print("   total:", len(r.json()), "| seguimientos de la primera:", [x["cantseguimientos"] for x in r.json()])
check("atención de cita inexistente", c.post("/api/atenciones", json={"codcita": 999, "resumaten": "x", "nivelaten": "BAJO"}), 404)
check("cita ya atendida", c.post("/api/atenciones", json={"codcita": 1, "resumaten": "x", "nivelaten": "BAJO"}), 409)
check("nivel inválido", c.post("/api/atenciones", json={"codcita": 6, "resumaten": "x", "nivelaten": "GRAVE"}), 422)
check("resumen vacío", c.post("/api/atenciones", json={"codcita": 6, "resumaten": "", "nivelaten": "BAJO"}), 422)
r = c.post("/api/citas", json={**nueva, "fechcita": "2026-12-02"}); citacancelada = r.json()["codcita"]
c.put(f"/api/citas/{citacancelada}/estado", json={"estcita": "CANCELADA"})
check("cita cancelada no se atiende", c.post("/api/atenciones", json={"codcita": citacancelada, "resumaten": "x", "nivelaten": "BAJO"}), 409)
c.delete(f"/api/citas/{citacancelada}")
check("riesgo f5 antes", c.get("/api/atenciones/riesgo/5"), 200, "nivel", "Sin casos de riesgo")
r = check("registrar atención", c.post("/api/atenciones", json={"codcita": 6, "resumaten": "Ansiedad por exámenes", "recomaten": "Sesiones semanales", "nivelaten": "ALTO", "reqseg": True}), 201, "nivelaten", "ALTO")
aten = r.json()["codaten"]; print("   atención:", aten, "| cita", r.json()["cita"]["codcita"])
check("la cita quedó atendida", c.get("/api/citas/6"), 200, "estcita", "ATENDIDA")
check("riesgo f5 después", c.get("/api/atenciones/riesgo/5"), 200, "nivel", "Requiere vigilancia")
check("riesgo de estudiante inexistente", c.get("/api/atenciones/riesgo/99"), 404)
check("atención duplicada", c.post("/api/atenciones", json={"codcita": 6, "resumaten": "x", "nivelaten": "BAJO"}), 409)

# ---- seguimiento de caso
r = check("seguimientos de la atención 1", c.get("/api/seguimientoscaso?codaten=1"), 200); assert len(r.json()) == 2
check("atención inexistente", c.get("/api/seguimientoscaso?codaten=99"), 404)
seg = {"codaten": aten, "fechseg": "2026-11-16", "descseg": "Primera sesión", "estseg": "ABIERTO", "fechprox": "2026-11-23"}
check("atención que no requiere seguimiento", c.post("/api/seguimientoscaso", json={**seg, "codaten": 3}), 409)
check("próxima sesión anterior", c.post("/api/seguimientoscaso", json={**seg, "fechprox": "2026-11-01"}), 422)
check("cerrado con próxima sesión", c.post("/api/seguimientoscaso", json={**seg, "estseg": "CERRADO"}), 422)
r = check("crear seguimiento", c.post("/api/seguimientoscaso", json=seg), 201, "estseg", "ABIERTO"); codseg = r.json()["codseg"]
check("pasar a en proceso", c.put(f"/api/seguimientoscaso/{codseg}", json={"fechseg": "2026-11-16", "descseg": "Primera sesión", "estseg": "EN_PROCESO", "fechprox": "2026-11-30"}), 200, "estseg", "EN_PROCESO")
check("cerrar", c.put(f"/api/seguimientoscaso/{codseg}", json={"fechseg": "2026-11-16", "descseg": "Alta", "estseg": "CERRADO"}), 200, "estseg", "CERRADO")
r = check("la atención cuenta su seguimiento", c.get(f"/api/atenciones/{aten}"), 200, "cantseguimientos", 1)
check("eliminar seguimiento", c.delete(f"/api/seguimientoscaso/{codseg}"), 204)
check("seguimiento inexistente", c.delete(f"/api/seguimientoscaso/{codseg}"), 404)

# ---- fichas psicológicas
r = check("listar fichas", c.get("/api/fichas"), 200); assert len(r.json()) == 2
assert all(x["codest"] == 1 for x in c.get("/api/fichas?codest=1").json())
ficha = {"fechaper": "2026-11-10", "motfic": "Estrés académico", "codest": 4, "codperresp": 2}
check("falta el motivo", c.post("/api/fichas", json={k: v for k, v in ficha.items() if k != "motfic"}), 422)
check("estudiante inexistente", c.post("/api/fichas", json={**ficha, "codest": 99}), 404)
check("responsable inexistente", c.post("/api/fichas", json={**ficha, "codperresp": 99}), 404)
check("cerrar sin diagnóstico", c.post("/api/fichas", json={**ficha, "estfic": "CERRADA"}), 409)
r = check("crear ficha (diagnóstico y plan vacíos)", c.post("/api/fichas", json=ficha), 201, "estfic", "ABIERTA"); codfic = r.json()["codfic"]
check("cerrar sin plan", c.put(f"/api/fichas/{codfic}", json={**ficha, "diagfic": "Ansiedad leve", "estfic": "CERRADA"}), 409)
check("completar y cerrar", c.put(f"/api/fichas/{codfic}", json={**ficha, "diagfic": "Ansiedad leve", "planfic": "Técnicas de relajación", "estfic": "CERRADA"}), 200, "estfic", "CERRADA")
check("eliminar ficha", c.delete(f"/api/fichas/{codfic}"), 204)

# ---- reportes
r = check("v03 citas por profesional", c.get("/api/reportes/bienestar/citasprofesional"), 200); print("   ", r.json()[:2])
r = check("v04 casos de riesgo", c.get("/api/reportes/bienestar/casosriesgo"), 200); print("   ", r.json())

despues = contar("ctrl_cita"); print("   auditoría de citas:", antes, "->", despues)
assert despues > antes
print("\nFALLOS:", fallos or "ninguno")
