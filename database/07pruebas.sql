use dbbecasbienestar;

# ---------- pruebas de triggers: postulacion ----------
insert into postulacion(fechpost,prompost,ingfampost,codest,codconv)
values('2026-11-10',15.00,1300,7,2);
insert into postulacion(fechpost,prompost,ingfampost,codest,codconv)
values('2026-11-11',14.00,1000,2,3);
update postulacion set estpost='EN_EVALUACION' where codest=7 and codconv=2;
update postulacion set prompost=prompost+1 where codconv=3 and estpost='REGISTRADA';
update postulacion set estpost='APROBADA',puntpost=70 where codest=2 and codconv=3;
delete from postulacion where codest=7 and codconv=2;
select * from postulacion;
select * from ctrl_postu;

# ---------- pruebas de triggers: beca otorgada ----------
update becaotorgada set estotor='SUSPENDIDA' where codotor=2;
update becaotorgada set estotor='VIGENTE',fechfinotor='2027-04-15' where codotor=2;
select * from becaotorgada;
select * from ctrl_otor;

# ---------- pruebas de triggers: cita ----------
insert into cita(fechcita,horacita,modcita,motcita,codest,codper)
values('2026-12-01','14:00:00','VIRTUAL','Consulta de prueba',6,2);
update cita set estcita='CANCELADA' where fechcita='2026-12-01' and codper=2;
delete from cita where fechcita='2026-12-01' and codper=2;
select * from cita;
select * from ctrl_cita;

# ---------- pruebas de procedimientos: cada validacion ----------
# p01: estudiante inexistente, convocatoria inexistente, convocatoria cerrada,
# duplicado, promedio bajo, ingreso alto y caso valido
call p01(99,2,15.00,900);
call p01(1,99,15.00,900);
call p01(1,1,18.00,900);
call p01(8,2,14.00,1100);
call p01(5,2,10.00,900);
call p01(5,2,15.00,2500);
call p01(6,2,15.00,1500);
# p02: postulacion inexistente y evaluacion normal
call p02(99,70.00,'APROBADA',4);
call p02(1,65.00,'EN_EVALUACION',4);
# p03: postulacion inexistente, no aprobada y ya otorgada
call p03(99,'2027-01-01','2027-06-30');
call p03(5,'2027-01-01','2027-06-30');
call p03(4,'2027-01-01','2027-06-30');
# p04: profesional ocupado en ese horario
call p04(1,3,'2026-11-25','08:00:00','VIRTUAL','Choque de horario');
# p05: cita inexistente y cita que ya tiene atencion
call p05(99,'x','x','BAJO',0);
call p05(5,'x','x','BAJO',0);

# ---------- pruebas de funciones ----------
select f1(1) 'postulaciones', f3(1) 'edad', f4(1) 'estado', f5(2) 'vigilancia', f6(2) 'cupos';
