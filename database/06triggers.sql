use dbbecasbienestar;

# ---------- auditoria de postulacion ----------
# crear una tabla con campos similares a la tabla a auditar
create table ctrl_postu(
idctrl int auto_increment primary key,
codpostc varchar(30),
estpostc varchar(30),
prompostc varchar(30),
codestc varchar(30),
codconvc varchar(30),
fechacc datetime,
tipoacc varchar(20));

delimiter $$
create trigger tr_insPostu after insert on dbbecasbienestar.postulacion for each row
begin
# new --> datos nuevos del registro insertado
insert into ctrl_postu(codpostc,estpostc,prompostc,codestc,codconvc,fechacc,tipoacc)
values(new.codpost,new.estpost,new.prompost,new.codest,new.codconv,now(),'INSERCION');
end;$$
delimiter ;

delimiter $$
create trigger tr_delPostu before delete on dbbecasbienestar.postulacion for each row
begin
# old ---> datos del registro que se va a eliminar
insert into ctrl_postu(codpostc,estpostc,prompostc,codestc,codconvc,fechacc,tipoacc)
values(old.codpost,old.estpost,old.prompost,old.codest,old.codconv,now(),'ELIMINACION');
end;$$
delimiter ;

delimiter $$
create trigger tr_upPostu after update on dbbecasbienestar.postulacion for each row
begin
# new --> datos nuevos, old ---> datos anteriores
insert into ctrl_postu(codpostc,estpostc,prompostc,codestc,codconvc,fechacc,tipoacc)
values(concat(old.codpost,'-',new.codpost),concat(old.estpost,'-',new.estpost),
concat(old.prompost,'-',new.prompost),concat(old.codest,'-',new.codest),
concat(old.codconv,'-',new.codconv),now(),'ACTUALIZACION');
end;$$
delimiter ;

# ---------- auditoria de beca otorgada ----------
# crear una tabla con campos similares a la tabla a auditar
create table ctrl_otor(
idctrl int auto_increment primary key,
codotorc varchar(30),
fechiniotorc varchar(30),
fechfinotorc varchar(30),
estotorc varchar(30),
codpostc varchar(30),
fechacc datetime,
tipoacc varchar(20));

delimiter $$
create trigger tr_insOtor after insert on dbbecasbienestar.becaotorgada for each row
begin
# new --> datos nuevos del registro insertado
insert into ctrl_otor(codotorc,fechiniotorc,fechfinotorc,estotorc,codpostc,fechacc,tipoacc)
values(new.codotor,new.fechiniotor,new.fechfinotor,new.estotor,new.codpost,now(),'INSERCION');
end;$$
delimiter ;

delimiter $$
create trigger tr_delOtor before delete on dbbecasbienestar.becaotorgada for each row
begin
# old ---> datos del registro que se va a eliminar
insert into ctrl_otor(codotorc,fechiniotorc,fechfinotorc,estotorc,codpostc,fechacc,tipoacc)
values(old.codotor,old.fechiniotor,old.fechfinotor,old.estotor,old.codpost,now(),'ELIMINACION');
end;$$
delimiter ;

delimiter $$
create trigger tr_upOtor after update on dbbecasbienestar.becaotorgada for each row
begin
# new --> datos nuevos, old ---> datos anteriores
insert into ctrl_otor(codotorc,fechiniotorc,fechfinotorc,estotorc,codpostc,fechacc,tipoacc)
values(concat(old.codotor,'-',new.codotor),concat(old.fechiniotor,'-',new.fechiniotor),
concat(old.fechfinotor,'-',new.fechfinotor),concat(old.estotor,'-',new.estotor),
concat(old.codpost,'-',new.codpost),now(),'ACTUALIZACION');
end;$$
delimiter ;

# ---------- auditoria de cita ----------
# crear una tabla con campos similares a la tabla a auditar
create table ctrl_cita(
idctrl int auto_increment primary key,
codcitac varchar(30),
fechcitac varchar(30),
horacitac varchar(30),
estcitac varchar(30),
codestc varchar(30),
codperc varchar(30),
fechacc datetime,
tipoacc varchar(20));

delimiter $$
create trigger tr_insCita after insert on dbbecasbienestar.cita for each row
begin
# new --> datos nuevos del registro insertado
insert into ctrl_cita(codcitac,fechcitac,horacitac,estcitac,codestc,codperc,fechacc,tipoacc)
values(new.codcita,new.fechcita,new.horacita,new.estcita,new.codest,new.codper,now(),'INSERCION');
end;$$
delimiter ;

delimiter $$
create trigger tr_delCita before delete on dbbecasbienestar.cita for each row
begin
# old ---> datos del registro que se va a eliminar
insert into ctrl_cita(codcitac,fechcitac,horacitac,estcitac,codestc,codperc,fechacc,tipoacc)
values(old.codcita,old.fechcita,old.horacita,old.estcita,old.codest,old.codper,now(),'ELIMINACION');
end;$$
delimiter ;

delimiter $$
create trigger tr_upCita after update on dbbecasbienestar.cita for each row
begin
# new --> datos nuevos, old ---> datos anteriores
insert into ctrl_cita(codcitac,fechcitac,horacitac,estcitac,codestc,codperc,fechacc,tipoacc)
values(concat(old.codcita,'-',new.codcita),concat(old.fechcita,'-',new.fechcita),
concat(old.horacita,'-',new.horacita),concat(old.estcita,'-',new.estcita),
concat(old.codest,'-',new.codest),concat(old.codper,'-',new.codper),now(),'ACTUALIZACION');
end;$$
delimiter ;
