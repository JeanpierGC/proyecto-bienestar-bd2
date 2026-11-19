use dbbecasbienestar;

# f1: cantidad de postulaciones de un estudiante
delimiter $$
create function f1(id int) returns int deterministic
begin
return(select count(codpost) from postulacion where codest=id);
end;
$$
delimiter ;
select f1(1);

# f2: promedio de seguimiento de una beca otorgada
delimiter $$
create function f2(id int) returns decimal(5,2) deterministic
begin
return(select round(avg(promsegb),2) from seguimientobeca where codotor=id);
end;
$$
delimiter ;
select f2(1);

# f3: edad del estudiante en años
delimiter $$
create function f3(id int) returns int deterministic
begin
return(select timestampdiff(year,fnacest,now()) from estudiante where codest=id);
end;
$$
delimiter ;
select f3(1);

# f4: mensaje segun el estado de una postulacion
delimiter $$
create function f4(id int) returns varchar(100) deterministic
begin
declare est varchar(15);
declare msg varchar(100);
set est=(select estpost from postulacion where codpost=id);
set msg=(case est
when 'REGISTRADA' then 'Postulación registrada, falta evaluar'
when 'EN_EVALUACION' then 'Postulación en evaluación'
when 'APROBADA' then 'Postulación aprobada, puede otorgarse la beca'
when 'RECHAZADA' then 'Postulación rechazada'
else 'No existe la postulación'
end);
return msg;
end;
$$
delimiter ;
select f4(1);

# f5: nivel de vigilancia de un estudiante segun sus atenciones de riesgo
delimiter $$
create function f5(id int) returns varchar(100) deterministic
begin
declare c,ce int;
set ce=(select count(codest) from estudiante where codest=id);
set c=(select count(codaten) from atencion a join cita ci on a.codcita=ci.codcita
where ci.codest=id and (nivelaten='ALTO' or nivelaten='CRITICO'));
if ce=0 then
return 'Estudiante no existe';
else
if c=0 then
return 'Sin casos de riesgo';
elseif c<3 then
return 'Requiere vigilancia';
else
return 'Requiere atención prioritaria';
end if; end if;
end;
$$
delimiter ;
select f5(4);

# f6: cupos disponibles de una convocatoria (cupos menos postulaciones aprobadas)
delimiter $$
create function f6(id int) returns int deterministic
begin
return(select cupconv-(select count(codpost) from postulacion p
where p.codconv=id and p.estpost='APROBADA')
from convocatoria where codconv=id);
end;
$$
delimiter ;
select f6(2);
