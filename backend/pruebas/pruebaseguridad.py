from fastapi.testclient import TestClient
import random
from app.main import app

FECHA = f"2030-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"

c = TestClient(app)
fallos = []


def check(nombre, obtenido, esperado):
    ok = obtenido == esperado
    print("OK   " if ok else "FALLA", nombre, "" if ok else f"-> {obtenido} (esperado {esperado})")
    if not ok:
        fallos.append(nombre)


def entrar(usuario, clave):
    return c.post("/api/auth/login", json={"nomusu": usuario, "clausu": clave})


def cab(r):
    return {"Authorization": "Bearer " + r.json()["token"]}


# ---- login
check("sin token: 401", c.get("/api/becas").status_code, 401)
check("token falso: 401", c.get("/api/becas", headers={"Authorization": "Bearer a.b"}).status_code, 401)
check("clave mala: 401", entrar("admin", "mala").status_code, 401)
check("usuario inexistente: 401", entrar("nadie", "x").status_code, 401)
r = entrar("admin", "admin123")
check("admin entra", r.status_code, 200)
adm = cab(r)
check("admin rol", r.json()["rolusu"], "ADMIN")
r = entrar("70123456", "70123456")  # Ana Quispe, codest 1
check("estudiante entra", r.status_code, 200)
est = cab(r)
check("estudiante lleva su codest", r.json()["codest"], 1)
check("yo", c.get("/api/auth/yo", headers=est).json()["codest"], 1)
# token manipulado
tok = r.json()["token"]
cuerpo, firma = tok.split(".")
check("token alterado: 401", c.get("/api/becas", headers={"Authorization": f"Bearer {cuerpo}x.{firma}"}).status_code, 401)

# ---- administrador puede todo
for ruta in ["/api/becas", "/api/auditoria/citas", "/api/reportes/bienestar/casosriesgo", "/api/atenciones", "/api/fichas", "/api/personal"]:
    check(f"admin GET {ruta}", c.get(ruta, headers=adm).status_code, 200)

# ---- estudiante: permitido
for ruta in ["/api/becas", "/api/convocatorias", "/api/servicios", "/api/personal", "/api/becas/1",
             "/api/postulaciones?codest=1", "/api/citas?codest=1", "/api/becasotorgadas?codest=1",
             "/api/atenciones?codest=1", "/api/atenciones/riesgo/1", "/api/postulaciones/conteo/1"]:
    check(f"est GET {ruta}", c.get(ruta, headers=est).status_code, 200)

# ---- estudiante: prohibido
for ruta in ["/api/postulaciones", "/api/postulaciones?codest=2", "/api/citas", "/api/becasotorgadas", "/api/atenciones",
             "/api/atenciones/riesgo/2", "/api/postulaciones/conteo/2", "/api/fichas", "/api/auditoria/citas",
             "/api/reportes/becas/otorgadas", "/api/reportes/bienestar/casosriesgo", "/api/busquedas/estudiantes?apellido=Q"]:
    check(f"est GET {ruta} prohibido", c.get(ruta, headers=est).status_code, 403)
check("est no crea becas", c.post("/api/becas", headers=est, json={}).status_code, 403)
check("est no evalua", c.put("/api/postulaciones/1/evaluacion", headers=est, json={}).status_code, 403)
check("est no otorga", c.post("/api/becasotorgadas", headers=est, json={}).status_code, 403)
check("est no registra atencion", c.post("/api/atenciones", headers=est, json={}).status_code, 403)

# ---- ownership de recursos por codigo
mias = c.get("/api/postulaciones?codest=1", headers=est).json()
ajenas = c.get("/api/postulaciones?codest=2", headers=adm).json()
check("hay postulaciones propias y ajenas para probar", bool(mias) and bool(ajenas), True)
check("est ve su postulacion", c.get(f"/api/postulaciones/{mias[0]['codpost']}", headers=est).status_code, 200)
check("est no ve postulacion ajena", c.get(f"/api/postulaciones/{ajenas[0]['codpost']}", headers=est).status_code, 403)
check("est no ve requisitos ajenos", c.get(f"/api/postulaciones/{ajenas[0]['codpost']}/requisitos", headers=est).status_code, 403)
check("est no borra ajena", c.delete(f"/api/postulaciones/{ajenas[0]['codpost']}", headers=est).status_code, 403)
check("codigo inexistente pasa y da 404", c.get("/api/postulaciones/9999", headers=est).status_code, 404)
citas = c.get("/api/citas", headers=adm).json()
ajena = next(x for x in citas if x["estudiante"]["codest"] != 1)
check("est no cancela cita ajena", c.put(f"/api/citas/{ajena['codcita']}/estado", headers=est, json={"estcita": "CANCELADA"}).status_code, 403)
atens = c.get("/api/atenciones", headers=adm).json()
ajenaat = next(x for x in atens if x["cita"]["estudiante"]["codest"] != 1)
check("est no ve atencion ajena", c.get(f"/api/atenciones/{ajenaat['codaten']}", headers=est).status_code, 403)
check("est no ve seguimientos ajenos", c.get(f"/api/seguimientoscaso?codaten={ajenaat['codaten']}", headers=est).status_code, 403)
check("est: seguimientoscaso sin codaten", c.get("/api/seguimientoscaso", headers=est).status_code, 403)

# ---- el estudiante crea lo suyo y no lo de otros
conv = c.get("/api/convocatorias", headers=est).json()
abiertas = [x for x in conv if x["estconv"] == "ABIERTA"]
cuerpo = {"codest": 2, "codconv": abiertas[0]["codconv"], "prompost": 15, "ingfampost": 900}
check("est no postula por otro", c.post("/api/postulaciones", headers=est, json=cuerpo).status_code, 403)
check("est no pide cita por otro", c.post("/api/citas", headers=est, json={"codest": 2, "codper": 1, "fechcita": FECHA, "horacita": "09:00", "modcita": "VIRTUAL"}).status_code, 403)
check("est pide su cita", c.post("/api/citas", headers=est, json={"codest": 1, "codper": 1, "fechcita": FECHA, "horacita": "09:00", "modcita": "VIRTUAL"}).status_code, 201)
check("est sin cuerpo valido: 403", c.post("/api/citas", headers=est, content="no json").status_code, 403)

# ---- usuario inactivo
from app.core.database import SessionLocal
from sqlalchemy import text
with SessionLocal() as s:
    s.execute(text("update Usuario set estusu='INACTIVO' where nomusu='70234567'")); s.commit()
check("inactivo no entra", entrar("70234567", "70234567").status_code, 401)
with SessionLocal() as s:
    s.execute(text("update Usuario set estusu='ACTIVO' where nomusu='70234567'")); s.commit()
check("reactivado entra", entrar("70234567", "70234567").status_code, 200)

print("\nFALLOS:", fallos if fallos else "ninguno")

# ---- perfil y cambio de contraseña
fallos2 = []
p = c.get("/api/auth/perfil", headers=est).json()
check("perfil del estudiante trae su escuela y edad (f3)", bool(p["estudiante"]["escuela"]) and p["estudiante"]["edad"] > 0, True)
check("perfil del admin sin estudiante", c.get("/api/auth/perfil", headers=adm).json()["estudiante"], None)
check("clave actual incorrecta: 409", c.put("/api/auth/clave", headers=est, json={"actual": "mala", "nueva": "nueva123"}).status_code, 409)
check("clave nueva corta: 422", c.put("/api/auth/clave", headers=est, json={"actual": "70123456", "nueva": "123"}).status_code, 422)
check("clave nueva igual: 422", c.put("/api/auth/clave", headers=est, json={"actual": "70123456", "nueva": "70123456"}).status_code, 422)
check("cambia la clave", c.put("/api/auth/clave", headers=est, json={"actual": "70123456", "nueva": "nueva123"}).status_code, 204)
check("la clave vieja ya no sirve", entrar("70123456", "70123456").status_code, 401)
check("la nueva sí", entrar("70123456", "nueva123").status_code, 200)
c.put("/api/auth/clave", headers=est, json={"actual": "nueva123", "nueva": "70123456"})
print("\nFALLOS FINALES:", fallos if fallos else "ninguno")
