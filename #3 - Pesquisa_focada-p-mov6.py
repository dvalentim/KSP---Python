# Importando as Bibliotecas
import krpc
import time

# Estabece conexão e define o foguete
conexão = krpc.connect(name= 'lançamento',
        address='192.168.1.106')
print('Versão do krpc: ',conexão.krpc.get_status().version)
foguete = conexão.space_center.active_vessel
print('O foguete é:', foguete.name)

# Contagem regressiva
contagem = ["três", "dois", "um"]
for i in range(len(contagem)):
    print(contagem[i])
    time.sleep(1)
print('Lançar')

# Prepara o voo
foguete.auto_pilot.engage()
foguete.control.activate_next_stage()
foguete.control.throttle = 1
foguete.auto_pilot.target_pitch_and_heading(45,90)

# Extraindo Telemetria
altitude = conexão.add_stream(getattr,foguete.flight(),'mean_altitude')
apoastro = conexão.add_stream(getattr,foguete.orbit,'apoapsis_altitude')

# Ativando o próximo estágio
def proximoEstagio(nave):
    estagio = nave.control.current_stage-1
    recursos = nave.resources_in_decouple_stage(estagio, False)
    combSolido = recursos.amount("SolidFuel")
    combLiquid = recursos.amount("LiquidFuel")

    #Ativa o próximo estágio quando acabar o combustível
    if combSolido == 0 and combLiquid == 0:
        nave.control.activate_next_stage()
        print()
        print('Próximo estágio!')
        print()

# Subindo o foguete
while apoastro() < 50000:
    foguete.auto_pilot.target_pitch_and_heading(45,90)
    proximoEstagio(foguete)

foguete.control.throttle = 0 

#Fim do código
print('O código terminou')
