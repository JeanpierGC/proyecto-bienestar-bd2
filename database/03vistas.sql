use dbbecasbienestar;

# v01: cantidad de postulaciones por estudiante y año
create view v01 as
select concat(apeest,' ',nomest)'estudiante',
count(codpost) 'cant. postulaciones',year(fechpost)'año de post'
from estudiante e join postulacion p on e.codest=p.codest
group by concat(apeest,' ',nomest), year(fechpost)
order by count(codpost) desc;
select * from v01;

# v02: becas otorgadas por convocatoria
create view v02 as
select nomconv 'convocatoria',nombeca 'beca',
count(o.codotor) 'cant. becas otorgadas'
from convocatoria c join beca b on c.codbeca=b.codbeca
join postulacion p on c.codconv=p.codconv
join becaotorgada o on p.codpost=o.codpost
group by nomconv, nombeca
order by count(o.codotor) desc;
select * from v02;

# v03: citas por profesional
create view v03 as
select concat(apeper,' ',nomper)'profesional',nomserv 'servicio',
count(codcita) 'cant. citas'
from personal pe join servicio s on pe.codserv=s.codserv
join cita c on pe.codper=c.codper
group by concat(apeper,' ',nomper), nomserv
order by count(codcita) desc;
select * from v03;

# v04: casos de riesgo alto o critico con seguimiento pendiente
create view v04 as
select concat(apeest,' ',nomest)'estudiante',fechcita 'fecha de cita',
nivelaten 'nivel',estseg 'estado seguimiento',fechprox 'próxima fecha'
from estudiante e join cita c on e.codest=c.codest
join atencion a on c.codcita=a.codcita
join seguimientocaso s on a.codaten=s.codaten
where (nivelaten='ALTO' or nivelaten='CRITICO')
and (estseg='ABIERTO' or estseg='EN_PROCESO')
order by fechprox;
select * from v04;

# v05: promedio de seguimiento por beca
create view v05 as
select nombeca 'beca',round(avg(promsegb),2)'promedio de seguimiento',
count(codsegb) 'cant. seguimientos'
from beca b join convocatoria c on b.codbeca=c.codbeca
join postulacion p on c.codconv=p.codconv
join becaotorgada o on p.codpost=o.codpost
join seguimientobeca s on o.codotor=s.codotor
group by nombeca
order by avg(promsegb) desc;
select * from v05;

# v06: postulaciones y aprobadas por convocatoria
create view v06 as
select nomconv 'convocatoria',cupconv 'cupos',
(select count(codpost) from postulacion p
where p.codconv=c.codconv) 'cant. postulaciones',
(select count(codpost) from postulacion p
where p.codconv=c.codconv and p.estpost='APROBADA') 'cant. aprobadas'
from convocatoria c;
select * from v06;
