class Estados():
    APROBADO = ('APRO','Aprobado')
    AGENDADO = ('AGEN','Agendado')
    CONFIRMADO = ('CONF','Confirmado')
    CANCELADO = ('CANC','Cancelado')
    PENDIENTE = ('PEND','Pendiente')
    RECHAZADO = ('RECH','Rechazado')
    RECIBIDO = ('RECI','Recibido')
    SOLICITADO = ('SOLI','Solicitado')
    POR_SOLICITAR = ('PSOL','Por Solicitar')
    
    ESTADOS_AGENDA_PROC = [
        PENDIENTE,
        CONFIRMADO,
        CANCELADO,
    ]

    ESTADOS_CAMA = [
        AGENDADO,
        PENDIENTE,
    ]

    ESTADOS_SALA = [
        AGENDADO,
        PENDIENTE,
    ]

    ESTADOS_DOCUMENTO_ADJ=[
        PENDIENTE,
        RECIBIDO,
        APROBADO,
        RECHAZADO,
    ]

    ESTADOS_ESPECIALISTA=[
        PENDIENTE,
        AGENDADO,
    ]

    ESTADOS_AGENDA_MAT=[
        POR_SOLICITAR,
        SOLICITADO,
        RECIBIDO,
    ]

    ESTADOS_AGENDA_EQU = [
        AGENDADO,
        PENDIENTE,
    ]

class TiposID:
    TIPOS_ID=[
        ('RC','Registro Civil'),
        ('TI','Tarjeta de identidad'),
        ('CC','Cédula de ciudadanía'),
        ('CE','Cédula de extranjería'),
        ('PA','Pasaporte'),
        ('MS','Menor sin identificación'),
        ('AS','Adulto sin identidad'),
    ]

class TiposProcedimiento:
    TIPOS_PROC=[
        ('CMA','Cirugia mayor'),
        ('CME','Cirugia menor'),
        ('CAM','Cirugia ambulatoria'),
    ]