# =====================================================================
# PROYECTO BASE DE DATOS 2
# Sistema de gestión de becas y bienestar universitario
# Motor: MySQL 8.0.16+ (necesario para que los CHECK se apliquen)
# =====================================================================

drop database if exists dbbecasbienestar;
create database dbbecasbienestar character set utf8mb4;
use dbbecasbienestar;

# ---------------------------------------------------------------------
# 1. ESTRUCTURA ACADÉMICA
# ---------------------------------------------------------------------
create table Facultad (
    codfac int auto_increment primary key,
    nomfac varchar(100) not null unique
);

create table Escuela (
    codesc int auto_increment primary key,
    nomesc varchar(100) not null,
    codfac int not null,
    unique (nomesc, codfac),
    foreign key (codfac) references Facultad(codfac)
);

create table Estudiante (
    codest int auto_increment primary key,
    nomest varchar(50) not null,
    apeest varchar(50) not null,
    dniest char(8) not null unique,
    correst varchar(100) not null unique,
    cicest tinyint not null check (cicest>=1 and cicest<=14),
    fnacest date not null,
    direst varchar(150),
    codesc int not null,
    foreign key (codesc) references Escuela(codesc)
);

# ---------------------------------------------------------------------
# 2. BIENESTAR: SERVICIOS Y PERSONAL
# ---------------------------------------------------------------------
create table Servicio (
    codserv int auto_increment primary key,
    nomserv varchar(100) not null unique,
    descserv text
);

create table Personal (
    codper int auto_increment primary key,
    nomper varchar(50) not null,
    apeper varchar(50) not null,
    dniper char(8) not null unique,
    corrper varchar(100) not null unique,
    cargoper varchar(50) not null,
    codserv int not null,
    foreign key (codserv) references Servicio(codserv)
);

# ---------------------------------------------------------------------
# 3. CITAS, ATENCIONES Y SEGUIMIENTO DE CASOS
# ---------------------------------------------------------------------
create table Cita (
    codcita int auto_increment primary key,
    fechcita date not null,
    horacita time not null,
    modcita varchar(15) not null
        check (modcita in ('PRESENCIAL', 'VIRTUAL')),
    motcita varchar(200),
    estcita varchar(15) not null default 'PROGRAMADA'
        check (estcita in ('PROGRAMADA', 'ATENDIDA', 'CANCELADA', 'NO_ASISTIO')),
    codest int not null,
    codper int not null,  # un profesional no puede tener dos citas a la misma fecha y hora
    unique (codper, fechcita, horacita),
    foreign key (codest) references Estudiante(codest),
    foreign key (codper) references Personal(codper)
);

# Relación 1:1 con Cita
create table Atencion (
    codaten int auto_increment primary key,
    resumaten text not null,
    recomaten text,
    nivelaten varchar(10) not null
        check (nivelaten in ('BAJO', 'MEDIO', 'ALTO', 'CRITICO')),
    reqseg tinyint(1) not null default 0,
    codcita int not null unique,
    foreign key (codcita) references Cita(codcita)
);

create table SeguimientoCaso (
    codseg int auto_increment primary key,
    fechseg date not null,
    descseg text not null,
    estseg varchar(15) not null default 'ABIERTO'
        check (estseg in ('ABIERTO', 'EN_PROCESO', 'CERRADO')),
    fechprox date,
    codaten int not null,
    check (fechprox is null or fechprox >= fechseg),
    foreign key (codaten) references Atencion(codaten)
);

create table FichaPsicologica (
    codfic int auto_increment primary key,
    fechaper date not null,
    motfic text not null,
    antfic text,
    diagfic text,
    planfic text,
    estfic varchar(10) not null default 'ABIERTA'
        check (estfic in ('ABIERTA', 'CERRADA')),
    codest int not null,
    codperresp int not null,
    foreign key (codest) references Estudiante(codest),
    foreign key (codperresp) references Personal(codper)
);

# ---------------------------------------------------------------------
# 4. BECAS: CATÁLOGO, REGLAS Y REQUISITOS
# ---------------------------------------------------------------------
create table Beca (
    codbeca int auto_increment primary key,
    nombeca varchar(100) not null unique,
    tipobeca varchar(50) not null,
    descbeca text,
    porcbeca decimal(5,2) not null check (porcbeca > 0 and porcbeca <= 100),
    estbeca varchar(10) not null default 'ACTIVA'
        check (estbeca in ('ACTIVA', 'INACTIVA'))
);

# Reglas de aplicación. Ejemplo: promedio >= 14  ->  nomreg='Promedio mínimo', opreg='>=', valreg=14
create table Regla (
    codreg int auto_increment primary key,
    nomreg varchar(100) not null,
    opreg varchar(2) not null
        check (opreg in ('>=', '<=', '>', '<', '=')),
    valreg decimal(8,2) not null,
    descreg text,
    codbeca int not null,
    foreign key (codbeca) references Beca(codbeca)
);

create table Requisito (
    codreq int auto_increment primary key,
    nomreq varchar(100) not null unique,
    descreq text
);

# N:M Beca - Requisito
create table RequisitoBeca (
    codreq int not null,
    codbeca int not null,
    primary key (codreq, codbeca),
    foreign key (codreq) references Requisito(codreq),
    foreign key (codbeca) references Beca(codbeca)
);

create table Convocatoria (
    codconv int auto_increment primary key,
    nomconv varchar(100) not null,
    perioconv varchar(10) not null,  # ej. 2026-II
    fechinconv date not null,
    fechfinconv date not null,
    cupconv int not null check (cupconv > 0),
    estconv varchar(15) not null default 'ABIERTA'
        check (estconv in ('ABIERTA', 'CERRADA', 'EN_EVALUACION')),
    codbeca int not null,
    check (fechfinconv >= fechinconv),
    foreign key (codbeca) references Beca(codbeca)
);

# ---------------------------------------------------------------------
# 5. POSTULACIÓN, OTORGAMIENTO Y SEGUIMIENTO DE BECA
# ---------------------------------------------------------------------
create table Postulacion (
    codpost int auto_increment primary key,
    fechpost date not null,
    prompost decimal(4,2) not null check (prompost>=0 and prompost<=20),
    ingfampost decimal(10,2) not null check (ingfampost >= 0),
    estpost varchar(15) not null default 'REGISTRADA'
        check (estpost in ('REGISTRADA', 'EN_EVALUACION', 'APROBADA', 'RECHAZADA')),
    puntpost decimal(5,2) check (puntpost >= 0),
    fecheval date,
    obspost text,
    codest int not null,
    codconv int not null,
    codpereval int null,  # evaluador: se asigna después  # un estudiante postula una sola vez por convocatoria
    unique (codest, codconv),
    check (fecheval is null or fecheval >= fechpost),
    foreign key (codest) references Estudiante(codest),
    foreign key (codconv) references Convocatoria(codconv),
    foreign key (codpereval) references Personal(codper)
);

# N:M Postulacion - Requisito (atributos de la relación "Presenta")
create table RequisitoPostulacion (
    codreq int not null,
    codpost int not null,
    fechpres date not null,
    obsdoc varchar(255),
    estdoc varchar(12) not null default 'PENDIENTE'
        check (estdoc in ('PENDIENTE', 'APROBADO', 'OBSERVADO', 'RECHAZADO')),
    primary key (codreq, codpost),
    foreign key (codreq) references Requisito(codreq),
    foreign key (codpost) references Postulacion(codpost)
);

# Relación 1:1 con Postulacion
create table BecaOtorgada (
    codotor int auto_increment primary key,
    fechotor date not null,
    fechiniotor date not null,
    fechfinotor date not null,
    estotor varchar(12) not null default 'VIGENTE'
        check (estotor in ('VIGENTE', 'FINALIZADA', 'REVOCADA', 'SUSPENDIDA')),
    codpost int not null unique,
    check (fechfinotor > fechiniotor),
    foreign key (codpost) references Postulacion(codpost)
);

create table SeguimientoBeca (
    codsegb int auto_increment primary key,
    fechsegb date not null,
    promsegb decimal(4,2) not null check (promsegb>=0 and promsegb<=20),
    cumsegb tinyint(1) not null,  # 1 = cumple condiciones, 0 = no cumple
    obssegb text,
    codotor int not null,
    codperresp int not null,
    foreign key (codotor) references BecaOtorgada(codotor),
    foreign key (codperresp) references Personal(codper)
);
