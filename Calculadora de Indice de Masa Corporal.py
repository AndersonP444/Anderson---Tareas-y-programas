peso = float(input('Digite su peso en kg: '))
estatura = float(input('Digite su altura en mts: '))
imc = peso / estatura**2
imc2 = round(imc, 2)
print("Tu Indice de Masa Corporal es:", imc2)

while peso < 0 or estatura < 0:
  peso = int(float(input('Digite su peso en kg: ')))
  estatura = int(float(input('Digite su altura en mts: ')))
if imc < 18.5:
  print("se considera peso insuficiente")
elif imc < 24.9:
  print("se considera saludable")
elif imc < 29.9:
  print("se considera sobrepeso")
elif imc < 39.9:
  print("se considera obesidad")
elif imc >= 40:
  print("se considera obesidad morbida")