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


