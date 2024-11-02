import copy

#lista de usuarios
user1 = ["Jenny", "ahorro", 50000, 45]
user2 = ["Anderson", "corriente", 2000, 67]
user3 = ["Jenny", "ahorro", 500000, 45]
user4 = ["Anderson", "corriente", 70000, 67]

def depositar(usuario, monto):
    usuario[2] += monto 
    return usuario[2]

def retirar(usuario, monto):
    if usuario[2] >= monto:
        usuario[2] -= monto
        return usuario[2]
    return "Fondos insuficientes"

def transferir(usuario, monto, usuario_destino):
    if monto <= 0:
        return "Monto inválido"
    if usuario[2] < monto:
        return "Fondos insuficientes"
    usuario[2] -= monto
    usuario_destino[2] += monto
    return (usuario[2], usuario_destino[2])
    return "Fondos insuficientes"

#diccionario de usuarios
reg_vnzl = {123: user1, 456: user2}
reg_pan = {123: user3, 456: user4}

#diccionario de bancos
reg_P = {'vnzl': reg_vnzl, 'pan': reg_pan}

#menu de inicio y seleccion de banco
while True:
    banco = input("selecciona el banco, vnzl o pan: ")
    if banco in reg_P:
        print("bienvenido al banco: ", banco)
        usuario = int(input("ingrese su clave de usuario: "))
        if usuario in reg_vnzl:
            print("""usuario encontrado. 
            Bienvenido que deseas hacer?
            1. estado de cuenta
            2. deposito
            3. retiro
            4. transferencia
            """)
            opcion = int(input("ingrese una opcion: "))
            if usuario == 123:
                if opcion == 1:
                    print("estado de cuenta: ", user1[2])
                    print("quieres realizar otra operacion?")
                    print("1. si")
                    print("2. no")
                    opcion2 = int(input("ingrese una opcion: "))
                    if opcion2 == 1:
                        continue
                    elif opcion2 == 2:
                        break
                elif opcion == 2:
                    monto = int(input("ingrese el monto a depositar: "))
                    deposito = user1[2] + monto
                    print("usted ha depositado: ", monto)
                    print("saldo actual: ", deposito)
                    print("quieres realizar otra operacion?")
                    print("1. si")
                    print("2. no")
                    opcion2 = int(input("ingrese una opcion: "))
                    if opcion2 == 1:
                        continue
                    elif opcion2 == 2:
                        break
                elif opcion == 3:
                    monto = int(input("ingrese el monto a retirar: "))
                    saldo_restante = user1[2] - monto
                    print("retiro: ", monto)
                    print("saldo actual: ", saldo_restante)
                    print("quieres realizar otra operacion?")
                    print("1. si")
                    print("2. no")
                    opcion2 = int(input("ingrese una opcion: "))
                    if opcion2 == 1:
                        continue
                    elif opcion2 == 2:
                        break
                elif opcion == 4:
                    monto = int(input("ingrese el monto a transferir: "))
                    usuario_destino = str(input("ingrese el usuario de destino: "))
                    transferencia = user1[2] - monto
                    print("Has transferido: ", monto)
                    print("saldo actual: ", transferencia)
                    print("quieres realizar otra operacion?")
                    print("1. si")
                    print("2. no")
                    opcion2 = int(input("ingrese una opcion: "))
                    if opcion2 == 1:
                        continue
                    elif opcion2 == 2:
                        break
                else:
                    print("opcion no valida")
            
            elif usuario == 456:
                if opcion == 1:
                    print("estado de cuenta: ", user2[2])
                    print("quieres realizar otra operacion?")
                    print("1. si")
                    print("2. no")
                    opcion2 = int(input("ingrese una opcion: "))
                    if opcion2 == 1:
                        continue
                    elif opcion2 == 2:
                        break
                elif opcion == 2:
                    monto = int(input("ingrese el monto a depositar: "))
                    deposito = user2[2] + monto
                    print("usted ha depositado: ", monto)
                    print("saldo actual: ", deposito)
                    print("quieres realizar otra operacion?")
                    print("1. si")
                    print("2. no")
                    opcion2 = int(input("ingrese una opcion: "))
                    if opcion2 == 1:
                        continue
                    elif opcion2 == 2:
                        break
                elif opcion == 3:
                    monto = int(input("ingrese el monto a retirar: "))
                    saldo_restante = user2[2] - monto
                    print("retiro: ", monto)    
                    print("saldo actual: ", saldo_restante)
                    print("quieres realizar otra operacion?")
                    print("1. si")
                    print("2. no")
                    opcion2 = int(input("ingrese una opcion: "))
                    if opcion2 == 1:
                        continue
                    elif opcion2 == 2:
                        break
                elif opcion == 4:
                    monto = int(input("ingrese el monto a transferir: "))
                    usuario_destino = str(input("ingrese el usuario de destino: "))
                    transferencia = user2[2] - monto
                    print("Has transferido: ", monto)
                    print("saldo actual: ", transferencia)
                    print("quieres realizar otra operacion?")
                    print("1. si")
                    print("2. no")
                    opcion2 = int(input("ingrese una opcion: "))
                    if opcion2 == 1:
                        continue
                    elif opcion2 == 2:
                        break
                else:
                    print("opcion no valida, escoja una opcion del menu")   
    elif banco in reg_pan:
        if banco in reg_P:
            print("bienvenido al banco: ", banco)
            usuario = int(input("ingrese su clave de usuario: "))
            if usuario in reg_pan:
                print("""usuario encontrado. 
                Bienvenido que deseas hacer?
                1. estado de cuenta
                2. deposito
                3. retiro
                4. transferencia
                """)
                opcion = int(input("ingrese una opcion: "))
            if usuario == 123:
                if opcion == 1:
                    print("estado de cuenta: ", user3[2])
                    print("quieres realizar otra operacion?")
                    print("1. si")
                    print("2. no")
                    opcion2 = int(input("ingrese una opcion: "))
                    if opcion2 == 1:
                        continue
                    elif opcion2 == 2:
                        break
                elif opcion == 2:
                    monto = int(input("ingrese el monto a depositar: "))
                    deposito = user3[2] + monto
                    print("usted ha depositado: ", monto)
                    print("saldo actual: ", deposito)
                    print("quieres realizar otra operacion?")
                    print("1. si")
                    print("2. no")
                    opcion2 = int(input("ingrese una opcion: "))
                    if opcion2 == 1:
                        continue
                    elif opcion2 == 2:
                        break
                elif opcion == 3:
                    monto = int(input("ingrese el monto a retirar: "))
                    saldo_restante = user3[2] - monto
                    print("retiro: ", monto)
                    print("saldo actual: ", saldo_restante)
                    print("quieres realizar otra operacion?")
                    print("1. si")
                    print("2. no")
                    opcion2 = int(input("ingrese una opcion: "))
                    if opcion2 == 1:
                        continue
                    elif opcion2 == 2:
                        break
                elif opcion == 4:
                    monto = int(input("ingrese el monto a transferir: "))
                    usuario_destino = str(input("ingrese el usuario de destino: "))
                    transferencia = user3[2] - monto
                    print("Has transferido: ", monto)
                    print("saldo actual: ", transferencia)
                    print("quieres realizar otra operacion?")
                    print("1. si")
                    print("2. no")
                    opcion2 = int(input("ingrese una opcion: "))
                    if opcion2 == 1:
                        continue
                    elif opcion2 == 2:
                        break
                else:
                    print("opcion no valida")

            elif usuario == 456:
                if opcion == 1:
                    print("estado de cuenta: ", user4[2])
                    print("quieres realizar otra operacion?")
                    print("1. si")
                    print("2. no")
                    opcion2 = int(input("ingrese una opcion: "))
                    if opcion2 == 1:
                        continue
                    elif opcion2 == 2:
                        break
                elif opcion == 2:
                    monto = int(input("ingrese el monto a depositar: "))
                    deposito = user4[2] + monto
                    print("usted ha depositado: ", monto)
                    print("saldo actual: ", deposito)
                    print("quieres realizar otra operacion?")
                    print("1. si")
                    print("2. no")
                    opcion2 = int(input("ingrese una opcion: "))
                    if opcion2 == 1:
                        continue
                    elif opcion2 == 2:
                        break
                elif opcion == 3:
                    monto = int(input("ingrese el monto a retirar: "))
                    saldo_restante = user4[2] - monto
                    print("retiro: ", monto)    
                    print("saldo actual: ", saldo_restante)
                    print("quieres realizar otra operacion?")
                    print("1. si")
                    print("2. no")
                    opcion2 = int(input("ingrese una opcion: "))
                    if opcion2 == 1:
                        continue
                    elif opcion2 == 2:
                        break
                elif opcion == 4:
                    monto = int(input("ingrese el monto a transferir: "))
                    usuario_destino = str(input("ingrese el usuario de destino: "))
                    transferencia = user4[2] - monto
                    print("Has transferido: ", monto)
                    print("saldo actual: ", transferencia)
                    print("quieres realizar otra operacion?")
                    print("1. si")
                    print("2. no")
                    opcion2 = int(input("ingrese una opcion: "))
                    if opcion2 == 1:
                        continue
                    elif opcion2 == 2:
                        break
                else:
                    print("opcion no valida, escoja una opcion del menu")
        else:
            print("usuario no encontrado")
else:
    print("banco no encontrado")

def estado_cuenta(usuario):
    return usuario[2]
def deposito(usuario, monto):
    usuario[2] += monto
    return usuario[2]
def retiro(usuario, monto):
    if monto > usuario[2]:
        return "Fondos insuficientes"
    else:
        usuario[2] -= monto
        return usuario[2]
def transferencia(usuario, monto, usuario_destino):
    if monto > usuario[2]:
        return "Fondos insuficientes"
    else:
        usuario[2] -= monto
        usuario_destino[2] += monto
        return usuario[2], usuario_destino[2]
def menu():
    print("1. Estado de cuenta")
    print("2. Deposito")
    print("3. Retiro")
    print("4. Transferencia")
    print("5. Salir")
    return int(input("Ingrese una opcion: "))
def main():
    while True:
        print("Bienvenido al sistema de gestion de cuentas")
        print("Seleccione una opcion:")
        print("1. VNL")
        print("2. PAN")
        print("3. Salir")
        opcion = int(input("Ingrese una opcion: "))
        if opcion == 1:
            print("Usted selecciono la opcion 1")

