#Importando as Bibliotecas
import krpc
import time

#Estabece conexão
conexão = krpc.connect(name= 'lançamento',
        address='192.168.1.106')
print('Versão do krpc: ',conexão.krpc.get_status().version)

#imprimindo o nome do foguete
#contagem regressiva
foguete = conexão.space_center.active_vessel
print('O foguete é:', foguete.name)
contagem = ["três", "dois", "um"]
for i in range(len(contagem)):
    print(contagem[i])
    time.sleep(1)
print('Lançar')

#Ativar piloto automático e lançar
foguete.auto_pilot.engage()
foguete.control.activate_next_stage()
foguete.control.throttle = 1

#Extraindo informações do foguete
altitude = conexão.add_stream(getattr,foguete.flight(),'mean_altitude')

#Subindo o foguete
while altitude() < 70000:
    foguete.auto_pilot.target_pitch_and_heading(80,90)
    estagio = foguete.control.current_stage
    estagio = estagio - 2
    recursos = foguete.resources_in_decouple_stage(estagio)
    comb_solid = recursos.amount("SolidFuel")
    if comb_solid == 0 and estagio == 1:
        print('estagio: ', estagio)
        foguete.control.activate_next_stage()
    if altitude() >= 50000:
        foguete.control.throttle = 0 

#Fim do código
print('O código terminou')
