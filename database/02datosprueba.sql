use dbbecasbienestar;

# datos de prueba: estructura academica
insert into Facultad(nomfac) values
('Ingeniería'),
('Ciencias de la Salud'),
('Ciencias Empresariales');

insert into Escuela(nomesc,codfac) values
('Ingeniería de Sistemas e Informática',1),
('Ingeniería Civil',1),
('Psicología',2),
('Enfermería',2),
('Administración',3);

insert into Estudiante(nomest,apeest,dniest,correst,cicest,fnacest,direst,codesc) values
('Ana','Quispe Rojas','70123456','ana.quispe@udh.edu.pe',5,'2004-03-12','Jr. Dos de Mayo 120',1),
('Luis','Mendoza Vega','70234567','luis.mendoza@udh.edu.pe',7,'2003-07-25','Av. Universitaria 450',1),
('María','Torres Díaz','70345678','maria.torres@udh.edu.pe',3,'2005-01-30','Jr. Abtao 310',3),
('Carlos','Huaman Cruz','70456789','carlos.huaman@udh.edu.pe',9,'2002-11-08','Av. Los Portales 78',2),
('Rosa','Salazar León','70567890','rosa.salazar@udh.edu.pe',4,'2004-09-17','Jr. Huallayco 215',4),
('Pedro','Villanueva Ramos','70678901','pedro.villanueva@udh.edu.pe',6,'2003-05-02','Av. Esteban Pavletich 90',5),
('Lucía','Gamarra Ortiz','70789012','lucia.gamarra@udh.edu.pe',2,'2005-12-21','Jr. Prado 188',3),
('Jorge','Paredes Lazo','70890123','jorge.paredes@udh.edu.pe',8,'2002-08-14','Jr. Bolívar 402',1);

# datos de prueba: bienestar
insert into Servicio(nomserv,descserv) values
('Psicología','Atención psicológica individual'),
('Orientación','Orientación vocacional y académica'),
('Servicio Social','Evaluación socioeconómica y apoyo social');

insert into Personal(nomper,apeper,dniper,corrper,cargoper,codserv) values
('Elena','Ríos Campos','40111222','elena.rios@udh.edu.pe','Psicóloga',1),
('Marco','Soto Landa','40222333','marco.soto@udh.edu.pe','Psicólogo',1),
('Carmen','Aliaga Paz','40333444','carmen.aliaga@udh.edu.pe','Orientadora',2),
('Raúl','Chávez Mori','40444555','raul.chavez@udh.edu.pe','Asistente social',3);

insert into Cita(fechcita,horacita,modcita,motcita,estcita,codest,codper) values
('2026-10-05','09:00:00','PRESENCIAL','Ansiedad por exámenes','ATENDIDA',1,1),
('2026-10-05','10:00:00','VIRTUAL','Problemas familiares','ATENDIDA',4,1),
('2026-10-07','11:00:00','PRESENCIAL','Orientación vocacional','ATENDIDA',7,3),
('2026-10-12','15:00:00','PRESENCIAL','Estrés académico','ATENDIDA',2,2),
('2026-11-20','09:00:00','VIRTUAL','Seguimiento','PROGRAMADA',1,1),
('2026-11-22','10:00:00','PRESENCIAL','Primera consulta','PROGRAMADA',5,2);

insert into Atencion(resumaten,recomaten,nivelaten,reqseg,codcita) values
('Ansiedad leve ante exámenes','Técnicas de respiración','MEDIO',1,1),
('Conflicto familiar con impacto en estudios','Derivar a servicio social','ALTO',1,2),
('Duda entre dos carreras','Test vocacional','BAJO',0,3),
('Estrés alto y problemas de sueño','Plan semanal de terapia','CRITICO',1,4);

insert into SeguimientoCaso(fechseg,descseg,estseg,fechprox,codaten) values
('2026-10-19','Mejora parcial','EN_PROCESO','2026-11-20',1),
('2026-10-20','Visita social programada','ABIERTO','2026-11-03',2),
('2026-10-26','Sesión de seguimiento','ABIERTO','2026-11-09',4),
('2026-10-30','Caso resuelto','CERRADO',null,1);

insert into FichaPsicologica(fechaper,motfic,antfic,diagfic,planfic,estfic,codest,codperresp) values
('2026-10-05','Ansiedad ante exámenes','Sin antecedentes',null,null,'ABIERTA',1,1),
('2026-10-12','Estrés académico y falta de sueño','Episodios previos','Estrés agudo','Terapia semanal de 8 sesiones','ABIERTA',2,2);

# datos de prueba: becas
insert into Beca(nombeca,tipobeca,descbeca,porcbeca,estbeca) values
('Beca Excelencia Académica','Académica','Para estudiantes con alto rendimiento',100.00,'ACTIVA'),
('Beca Socioeconómica','Socioeconómica','Apoyo por situación económica',70.00,'ACTIVA'),
('Beca Deportiva','Deportiva','Para deportistas destacados',50.00,'ACTIVA');

insert into Regla(nomreg,opreg,valreg,descreg,codbeca) values
('Promedio mínimo','>=',16,'Promedio ponderado mínimo',1),
('Promedio mínimo','>=',13,'Promedio ponderado mínimo',2),
('Ingreso familiar máximo','<=',2000,'Ingreso familiar mensual en soles',2),
('Promedio mínimo','>=',12,'Promedio ponderado mínimo',3);

insert into Requisito(nomreq,descreq) values
('DNI','Copia del documento de identidad'),
('Constancia de matrícula','Constancia del ciclo vigente'),
('Certificado de notas','Certificado de notas del último ciclo'),
('Declaración jurada de ingresos','Ingresos del grupo familiar');

insert into RequisitoBeca(codreq,codbeca) values
(1,1),(2,1),(3,1),
(1,2),(2,2),(4,2),
(1,3),(2,3);

insert into Convocatoria(nomconv,perioconv,fechinconv,fechfinconv,cupconv,estconv,codbeca) values
('Convocatoria Excelencia 2026-II','2026-II','2026-08-01','2026-09-30',5,'CERRADA',1),
('Convocatoria Socioeconómica 2026-II','2026-II','2026-08-01','2026-12-31',10,'ABIERTA',2),
('Convocatoria Deportiva 2026-II','2026-II','2026-08-15','2026-12-15',3,'ABIERTA',3);

insert into Postulacion(fechpost,prompost,ingfampost,estpost,puntpost,fecheval,obspost,codest,codconv,codpereval) values
('2026-08-10',17.50,1800,'APROBADA',88.00,'2026-09-05',null,1,1,3),
('2026-08-12',15.20,1200,'RECHAZADA',60.00,'2026-09-06','Promedio insuficiente',2,1,3),
('2026-08-20',14.80,900,'APROBADA',82.00,'2026-09-10',null,3,2,4),
('2026-08-22',13.50,1500,'EN_EVALUACION',null,null,null,4,2,4),
('2026-09-01',12.50,2500,'REGISTRADA',null,null,null,5,3,null),
('2026-09-03',16.00,1700,'APROBADA',90.00,'2026-09-15',null,6,3,3);

insert into RequisitoPostulacion(codreq,codpost,fechpres,obsdoc,estdoc) values
(1,1,'2026-08-10',null,'APROBADO'),
(2,1,'2026-08-10',null,'APROBADO'),
(3,1,'2026-08-10',null,'APROBADO'),
(1,3,'2026-08-20',null,'APROBADO'),
(2,3,'2026-08-20',null,'APROBADO'),
(4,3,'2026-08-20',null,'APROBADO'),
(1,4,'2026-08-22',null,'PENDIENTE'),
(4,4,'2026-08-22','Falta firma','OBSERVADO');

insert into BecaOtorgada(fechotor,fechiniotor,fechfinotor,estotor,codpost) values
('2026-09-06','2026-09-10','2027-03-10','VIGENTE',1),
('2026-09-12','2026-09-15','2027-03-15','VIGENTE',3),
('2026-09-16','2026-09-20','2027-03-20','VIGENTE',6);

insert into SeguimientoBeca(fechsegb,promsegb,cumsegb,obssegb,codotor,codperresp) values
('2026-10-15',17.20,1,'Mantiene el promedio',1,3),
('2026-10-20',12.80,0,'Promedio por debajo del mínimo',2,4),
('2026-10-22',16.40,1,null,3,3);
