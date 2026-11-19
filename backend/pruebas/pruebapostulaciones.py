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

def auditoria(tabla):
    with SessionLocal() as s:
        return s.execute(text(f"select count(*) from {tabla}")).scalar()

antes = {t: auditoria(t) for t in ("ctrl_postu", "ctrl_otor")}

# ---- lectura
r = check("listar postulaciones", c.get("/api/postulaciones"), 200)
datos = r.json()
print("   total:", len(datos), "| primera:", datos[0]["estudiante"]["apeest"], "|", datos[0]["mensajeestado"], "| otorgada:", datos[0]["otorgada"])
check("filtro por estudiante", c.get("/api/postulaciones?codest=1"), 200)
assert all(p["codest"] == 1 for p in c.get("/api/postulaciones?codest=1").json())
assert all(p["estpost"] == "APROBADA" for p in c.get("/api/postulaciones?estpost=APROBADA").json())
check("conteo f1", c.get("/api/postulaciones/conteo/1"), 200, "cantidad", 1)
check("obtener inexistente", c.get("/api/postulaciones/999"), 404)
check("personal", c.get("/api/personal"), 200)

# ---- registrar (p01)
check("estudiante inexistente", c.post("/api/postulaciones", json={"codest": 99, "codconv": 3, "prompost": 15, "ingfampost": 900}), 404)
check("convocatoria inexistente", c.post("/api/postulaciones", json={"codest": 7, "codconv": 99, "prompost": 15, "ingfampost": 900}), 404)
check("convocatoria cerrada", c.post("/api/postulaciones", json={"codest": 7, "codconv": 1, "prompost": 18, "ingfampost": 900}), 409)
check("duplicada", c.post("/api/postulaciones", json={"codest": 5, "codconv": 3, "prompost": 15, "ingfampost": 900}), 409)
r = check("promedio insuficiente", c.post("/api/postulaciones", json={"codest": 1, "codconv": 3, "prompost": 10, "ingfampost": 900}), 409)
print("   ", r.json())
check("promedio fuera de rango", c.post("/api/postulaciones", json={"codest": 1, "codconv": 3, "prompost": 25, "ingfampost": 900}), 422)
check("ingreso negativo", c.post("/api/postulaciones", json={"codest": 1, "codconv": 3, "prompost": 15, "ingfampost": -1}), 422)
r = check("registrar válida", c.post("/api/postulaciones", json={"codest": 7, "codconv": 3, "prompost": 14.5, "ingfampost": 900}), 201, "estpost", "REGISTRADA")
nueva = r.json()["codpost"]
print("   nueva:", nueva, r.json()["mensajeestado"], r.json()["estudiante"]["apeest"])
check("conteo tras registrar", c.get("/api/postulaciones/conteo/7"), 200, "cantidad", 1)

# ---- requisitos presentados
r = check("requisitos de la postulación", c.get(f"/api/postulaciones/{nueva}/requisitos"), 200)
reqs = r.json(); print("   ", [(x["nomreq"], x["estdoc"]) for x in reqs])
primero = reqs[0]["codreq"]
r = check("presentar requisito", c.put(f"/api/postulaciones/{nueva}/requisitos/{primero}", json={"estdoc": "PENDIENTE"}), 200, "estdoc", "PENDIENTE")
check("revisar requisito", c.put(f"/api/postulaciones/{nueva}/requisitos/{primero}", json={"estdoc": "OBSERVADO", "obsdoc": "Foto borrosa"}), 200, "estdoc", "OBSERVADO")
check("estado de documento inválido", c.put(f"/api/postulaciones/{nueva}/requisitos/{primero}", json={"estdoc": "XX"}), 422)
check("requisito ajeno a la beca", c.put(f"/api/postulaciones/{nueva}/requisitos/999", json={"estdoc": "PENDIENTE"}), 409)
estados = {x["codreq"]: x["estdoc"] for x in c.get(f"/api/postulaciones/{nueva}/requisitos").json()}
assert estados[primero] == "OBSERVADO", estados
check("quitar requisito", c.delete(f"/api/postulaciones/{nueva}/requisitos/{primero}"), 204)
assert c.get(f"/api/postulaciones/{nueva}/requisitos").json()[0]["estdoc"] is None

# ---- evaluar (p02)
check("evaluador inexistente", c.put(f"/api/postulaciones/{nueva}/evaluacion", json={"puntpost": 80, "estpost": "APROBADA", "codpereval": 99}), 404)
check("estado de evaluación inválido", c.put(f"/api/postulaciones/{nueva}/evaluacion", json={"puntpost": 80, "estpost": "REGISTRADA", "codpereval": 1}), 422)
r = check("evaluar", c.put(f"/api/postulaciones/{nueva}/evaluacion", json={"puntpost": 80, "estpost": "APROBADA", "codpereval": 1}), 200, "estpost", "APROBADA")
print("   ", r.json()["mensajeestado"], "| evaluador:", r.json()["evaluador"]["nomper"], "| fecheval:", r.json()["fecheval"])
check("no se elimina una evaluada", c.delete(f"/api/postulaciones/{nueva}"), 409)

# ---- otorgar (p03)
check("otorgar inexistente", c.post("/api/becasotorgadas", json={"codpost": 999, "fechiniotor": "2026-12-01", "fechfinotor": "2027-06-01"}), 404)
check("otorgar con fechas inválidas", c.post("/api/becasotorgadas", json={"codpost": nueva, "fechiniotor": "2027-06-01", "fechfinotor": "2026-12-01"}), 422)
check("otorgar a rechazada", c.post("/api/becasotorgadas", json={"codpost": 2, "fechiniotor": "2026-12-01", "fechfinotor": "2027-06-01"}), 409)
r = check("otorgar", c.post("/api/becasotorgadas", json={"codpost": nueva, "fechiniotor": "2026-12-01", "fechfinotor": "2027-06-01"}), 201, "estotor", "VIGENTE")
otor = r.json()["codotor"]; print("   otorgada:", otor, r.json()["postulacion"]["convocatoria"]["beca"]["nombeca"])
check("otorgar de nuevo", c.post("/api/becasotorgadas", json={"codpost": nueva, "fechiniotor": "2026-12-01", "fechfinotor": "2027-06-01"}), 409)
check("no se reevalúa una otorgada", c.put(f"/api/postulaciones/{nueva}/evaluacion", json={"puntpost": 10, "estpost": "RECHAZADA", "codpereval": 1}), 409)
check("la postulación muestra su beca", c.get(f"/api/postulaciones/{nueva}"), 200)
assert c.get(f"/api/postulaciones/{nueva}").json()["otorgada"]["codotor"] == otor

# ---- seguimiento de beca
check("seguimientos vacíos", c.get(f"/api/becasotorgadas/{otor}/seguimientos"), 200)
base = {"fechsegb": "2027-01-15", "promsegb": 15, "cumsegb": True, "obssegb": "Cumple", "codperresp": 2}
check("responsable inexistente", c.post(f"/api/becasotorgadas/{otor}/seguimientos", json={**base, "codperresp": 99}), 404)
check("promedio de seguimiento inválido", c.post(f"/api/becasotorgadas/{otor}/seguimientos", json={**base, "promsegb": 21}), 422)
r = check("registrar seguimiento", c.post(f"/api/becasotorgadas/{otor}/seguimientos", json=base), 201)
seg1 = r.json()["codsegb"]
check("segundo seguimiento", c.post(f"/api/becasotorgadas/{otor}/seguimientos", json={**base, "fechsegb": "2027-02-15", "promsegb": 17}), 201)
r = check("promedio f2", c.get(f"/api/becasotorgadas/{otor}"), 200, "promedioseguimiento", 16.0)
print("   seguimientos:", r.json()["cantseguimientos"])
check("no se elimina con seguimientos", c.delete(f"/api/becasotorgadas/{otor}"), 409)
check("seguimiento de otra beca", c.delete(f"/api/becasotorgadas/1/seguimientos/{seg1}"), 409)
check("cambiar estado", c.put(f"/api/becasotorgadas/{otor}/estado", json={"estotor": "SUSPENDIDA"}), 200, "estotor", "SUSPENDIDA")
check("estado inválido", c.put(f"/api/becasotorgadas/{otor}/estado", json={"estotor": "X"}), 422)
check("listar otorgadas", c.get("/api/becasotorgadas"), 200)

# ---- reportes
r = check("v01 por estudiante", c.get("/api/reportes/postulaciones/porestudiante"), 200); print("   ", r.json()[:2])
r = check("v05 promedios por beca", c.get("/api/reportes/postulaciones/promediosbeca"), 200); print("   ", r.json())

# ---- limpieza: eliminar una postulación REGISTRADA
r = check("registrar para eliminar", c.post("/api/postulaciones", json={"codest": 2, "codconv": 3, "prompost": 13, "ingfampost": 500}), 201)
borrar = r.json()["codpost"]
c.put(f"/api/postulaciones/{borrar}/requisitos/{primero}", json={"estdoc": "PENDIENTE"})
check("eliminar registrada (con documentos)", c.delete(f"/api/postulaciones/{borrar}"), 204)
check("ya no existe", c.get(f"/api/postulaciones/{borrar}"), 404)

# ---- triggers de auditoría disparados por la API
despues = {t: auditoria(t) for t in antes}
print("   auditoría:", antes, "->", despues)
assert despues["ctrl_postu"] > antes["ctrl_postu"] and despues["ctrl_otor"] > antes["ctrl_otor"]
print("\nFALLOS:", fallos or "ninguno")
