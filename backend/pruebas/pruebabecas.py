from fastapi.testclient import TestClient
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

# --- reportes (vistas y procedimiento)
r = check("v02 otorgadas", c.get("/api/reportes/becas/otorgadas"), 200)
print("   ", r.json())
r = check("v06 cupos", c.get("/api/reportes/becas/cuposconv"), 200)
print("   ", r.json())
r = check("p07 ranking 2026", c.get("/api/reportes/becas/ranking?anio=2026"), 200)
print("   ", r.json())
check("p07 sin anio", c.get("/api/reportes/becas/ranking"), 422)
# segunda llamada seguida (comprueba que el CALL no deja la conexión desincronizada)
check("p07 otra vez", c.get("/api/reportes/becas/ranking?anio=2026"), 200)
check("becas tras call", c.get("/api/becas"), 200)

# --- becas
r = check("listar becas", c.get("/api/becas"), 200)
print("   ", [(b["nombeca"], b["porcbeca"], len(b["reglas"]), len(b["requisitos"])) for b in r.json()])
check("obtener beca 1", c.get("/api/becas/1"), 200, "nombeca", "Beca Excelencia Académica")
check("beca inexistente", c.get("/api/becas/99"), 404)
b = check("crear beca", c.post("/api/becas", json={"nombeca": "Beca Cultural", "tipobeca": "Cultural", "porcbeca": 25.5}), 201, "estbeca", "ACTIVA").json()
check("beca duplicada", c.post("/api/becas", json={"nombeca": "Beca Cultural", "tipobeca": "Cultural", "porcbeca": 10}), 409)
check("porcentaje 150", c.post("/api/becas", json={"nombeca": "X", "tipobeca": "Y", "porcbeca": 150}), 422)
check("actualizar beca", c.put(f"/api/becas/{b['codbeca']}", json={"nombeca": "Beca Cultural", "tipobeca": "Cultural", "porcbeca": 30, "estbeca": "INACTIVA"}), 200, "estbeca", "INACTIVA")

# --- requisitos
q = check("crear requisito", c.post("/api/requisitos", json={"nomreq": "Carta de motivación"}), 201).json()
check("requisito duplicado", c.post("/api/requisitos", json={"nomreq": "Carta de motivación"}), 409)
r = check("asignar requisitos", c.put(f"/api/becas/{b['codbeca']}/requisitos", json={"codreq": [1, q["codreq"]]}), 200)
print("   ", [x["nomreq"] for x in r.json()["requisitos"]])
check("requisito inexistente", c.put(f"/api/becas/{b['codbeca']}/requisitos", json={"codreq": [1, 77]}), 404)
check("requisito asignado no se borra", c.delete(f"/api/requisitos/{q['codreq']}"), 409)
check("quitar requisitos", c.put(f"/api/becas/{b['codbeca']}/requisitos", json={"codreq": []}), 200)
check("borrar requisito libre", c.delete(f"/api/requisitos/{q['codreq']}"), 204)

# --- reglas
g = check("crear regla", c.post("/api/reglas", json={"nomreg": "Promedio mínimo", "opreg": ">=", "valreg": 14, "codbeca": b["codbeca"]}), 201).json()
check("operador invalido", c.post("/api/reglas", json={"nomreg": "x", "opreg": "!=", "valreg": 1, "codbeca": 1}), 422)
check("regla beca inexistente", c.post("/api/reglas", json={"nomreg": "x", "opreg": ">", "valreg": 1, "codbeca": 99}), 404)
check("filtrar reglas por beca", c.get(f"/api/reglas?codbeca={b['codbeca']}"), 200)
check("actualizar regla", c.put(f"/api/reglas/{g['codreg']}", json={"nomreg": "Promedio mínimo", "opreg": ">=", "valreg": 15, "codbeca": b["codbeca"]}), 200, "valreg", 15.0)

# --- convocatorias
base = {"nomconv": "Convocatoria Cultural 2027-I", "perioconv": "2027-I", "fechinconv": "2027-03-01", "fechfinconv": "2027-04-01", "cupconv": 4, "codbeca": 2}
v = check("crear convocatoria", c.post("/api/convocatorias", json=base), 201, "cuposdisponibles", 4).json()
check("fechas invertidas", c.post("/api/convocatorias", json={**base, "fechfinconv": "2027-02-01"}), 422)
check("beca inactiva", c.post("/api/convocatorias", json={**base, "codbeca": b["codbeca"]}), 409)
check("beca inexistente", c.post("/api/convocatorias", json={**base, "codbeca": 99}), 404)
r = check("listar convocatorias", c.get("/api/convocatorias"), 200)
print("   ", [(x["nomconv"], x["cuposdisponibles"]) for x in r.json()])
check("filtrar por beca", c.get("/api/convocatorias?codbeca=2"), 200)
check("actualizar convocatoria", c.put(f"/api/convocatorias/{v['codconv']}", json={**base, "cupconv": 6}), 200, "cuposdisponibles", 6)
check("convocatoria con postulaciones no se borra", c.delete("/api/convocatorias/2"), 409)
check("borrar convocatoria libre", c.delete(f"/api/convocatorias/{v['codconv']}"), 204)

# --- limpieza
check("beca con convocatorias no se borra", c.delete("/api/becas/1"), 409)
check("borrar beca nueva (con su regla)", c.delete(f"/api/becas/{b['codbeca']}"), 204)
print("\nRESULTADO:", "TODO OK" if not fallos else f"FALLARON {fallos}")
