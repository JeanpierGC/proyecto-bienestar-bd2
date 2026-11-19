use dbbecasbienestar;

# p01: registrar una postulacion (valida estudiante, convocatoria abierta y en fechas,
# duplicado y las reglas de la beca: promedio minimo e ingreso familiar maximo)
delimiter $$
create procedure p01 (p1 int,p2 int,p3 decimal(4,2),p4 decimal(10,2))
begin
declare ce,c int;
declare e varchar(15);
declare fi,ff date;
declare m,i decimal(8,2);
set ce=(select count(codest) from estudiante where codest=p1);
set c=(select count(codpost) from postulacion where codest=p1 and codconv=p2);
set e=(select estconv from convocatoria where codconv=p2);
set fi=(select fechinconv from convocatoria where codconv=p2);
set ff=(select fechfinconv from convocatoria where codconv=p2);
set m=(select valreg from regla r join convocatoria cv on r.codbeca=cv.codbeca
where cv.codconv=p2 and r.nomreg='Promedio mínimo');
set i=(select valreg from regla r join convocatoria cv on r.codbeca=cv.codbeca
where cv.codconv=p2 and r.nomreg='Ingreso familiar máximo');
if ce=0 then
select 'El estudiante no existe' mensaje;
elseif e is null then
select 'La convocatoria no existe' mensaje;
elseif e='CERRADA' or e='EN_EVALUACION' then
select 'La convocatoria no está abierta' mensaje;
elseif date(now())<fi or date(now())>ff then
select 'La convocatoria está fuera de fechas' mensaje;
elseif c>0 then
select 'El estudiante ya postuló a esta convocatoria' mensaje;
elseif m is not null and p3<m then
select 'No cumple el promedio mínimo de la beca' mensaje;
elseif i is not null and p4>i then
select 'Supera el ingreso familiar máximo de la beca' mensaje;
else
insert into postulacion(fechpost,prompost,ingfampost,estpost,codest,codconv)
values(now(),p3,p4,'REGISTRADA',p1,p2);
select 'Postulación registrada' mensaje;
end if;
end;$$
delimiter ;
call p01(8,2,14.00,1100);

# p02: evaluar una postulacion (puntaje, estado y evaluador); no aprueba si ya no hay cupos
delimiter $$
create procedure p02 (p1 int,p2 decimal(5,2),p3 varchar(15),p4 int)
begin
declare cv,cu,ap int;
set cv=(select codconv from postulacion where codpost=p1);
set cu=(select cupconv from convocatoria where codconv=cv);
set ap=(select count(codpost) from postulacion
where codconv=cv and estpost='APROBADA' and codpost<>p1);
if cv is null then
select 'La postulación no existe' mensaje;
elseif p3='APROBADA' and ap>=cu then
select 'No quedan cupos en la convocatoria' mensaje;
else
update postulacion
set puntpost=p2,estpost=p3,fecheval=now(),codpereval=p4
where codpost=p1;
select 'Postulación evaluada' mensaje;
end if;
end;$$
delimiter ;
call p02(4,75.00,'APROBADA',4);

# p03: otorgar beca a una postulacion aprobada
delimiter $$
create procedure p03 (p1 int,p2 date,p3 date)
begin
declare c int;
declare e varchar(15);
set e=(select estpost from postulacion where codpost=p1);
set c=(select count(codotor) from becaotorgada where codpost=p1);
if e is null then
select 'La postulación no existe' mensaje;
elseif e='APROBADA' and c=0 then
insert into becaotorgada(fechotor,fechiniotor,fechfinotor,estotor,codpost)
values(now(),p2,p3,'VIGENTE',p1);
select 'Beca otorgada' mensaje;
elseif c>0 then
select 'La postulación ya tiene una beca otorgada' mensaje;
else
select 'La postulación no está aprobada' mensaje;
end if;
end;$$
delimiter ;
call p03(4,'2026-11-20','2027-05-20');

# p04: registrar una cita si el profesional esta libre en ese horario
delimiter $$
create procedure p04 (p1 int,p2 int,p3 date,p4 time,p5 varchar(15),p6 varchar(200))
begin
declare c int;
set c=(select count(codcita) from cita
where codper=p2 and fechcita=p3 and horacita=p4);
if c>0 then
select 'El profesional ya tiene una cita en ese horario' mensaje;
else
insert into cita(fechcita,horacita,modcita,motcita,estcita,codest,codper)
values(p3,p4,p5,p6,'PROGRAMADA',p1,p2);
select 'Cita registrada' mensaje;
end if;
end;$$
delimiter ;
call p04(3,3,'2026-11-25','08:00:00','PRESENCIAL','Orientación académica');

# p05: registrar la atencion de una cita y marcar la cita como atendida
delimiter $$
create procedure p05 (p1 int,p2 text,p3 text,p4 varchar(10),p5 tinyint)
begin
declare c int;
declare e varchar(15);
set e=(select estcita from cita where codcita=p1);
set c=(select count(codaten) from atencion where codcita=p1);
if e is null then
select 'La cita no existe' mensaje;
elseif c>0 then
select 'La cita ya tiene una atención registrada' mensaje;
elseif e='CANCELADA' or e='NO_ASISTIO' then
select 'La cita no fue atendida' mensaje;
else
insert into atencion(resumaten,recomaten,nivelaten,reqseg,codcita)
values(p2,p3,p4,p5,p1);
update cita set estcita='ATENDIDA' where codcita=p1;
select 'Atención registrada' mensaje;
end if;
end;$$
delimiter ;
call p05(5,'Buena evolución','Continuar con las sesiones','BAJO',0);

# p06: buscar estudiantes por apellido
delimiter $$
create procedure p06 (p1 varchar(50))
begin
select * from estudiante where apeest like concat(p1,'%');
end;$$
delimiter ;
call p06('Quis');

# p07: top 10 de becas con mas postulaciones en un año
delimiter $$
create procedure p07 (a int)
begin
select nombeca 'beca',count(codpost) 'cant. postulaciones',year(fechpost)'año post.'
from beca b join convocatoria c on b.codbeca=c.codbeca
join postulacion p on c.codconv=p.codconv
where year(fechpost)=a
group by nombeca, year(fechpost)
order by count(codpost) desc limit 10;
end;$$
delimiter ;
call p07(2026);
