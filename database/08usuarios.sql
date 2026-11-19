use dbbecasbienestar;

# ---------- usuarios del sistema (login con roles) ----------
# ADMIN no tiene estudiante; ESTUDIANTE siempre apunta a un estudiante
create table Usuario(
codusu int auto_increment primary key,
nomusu varchar(30) not null unique,
clausu varchar(200) not null,
rolusu varchar(12) not null check (rolusu in ('ADMIN','ESTUDIANTE')),
estusu varchar(10) not null default 'ACTIVO' check (estusu in ('ACTIVO','INACTIVO')),
codest int unique,
foreign key (codest) references Estudiante(codest),
check ((rolusu='ADMIN' and codest is null) or (rolusu='ESTUDIANTE' and codest is not null)));
