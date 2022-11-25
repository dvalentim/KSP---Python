import time
import krpc

# estabelece conexão
conn = krpc.connect(
    name='Procura Apoastro',
    address='192.168.1.106')
print(conn.krpc.get_status().version)

#Atribui o objeto foguete ativo a variável foguete
foguete = conn.space_center.active_vessel

#Variáveis que devem ser editadas para outros resultados
ang_final = 10
apoastro_final = 74000
#apoastro_final = 40000
altitude_orbital = 70000
#altitude_orbital = 45000
direção = 90



#Contagem Regressiva
contagem = ["Trê", "Dois", "Um"]

for i in range(len(contagem)):
    print(contagem[i])
    time.sleep(1)
print('Lançar!')

#Aceleração no máximo e ligando o próximo estágeio
foguete.auto_pilot.engage()
foguete.auto_pilot.target_roll = direção
foguete.auto_pilot.target_pitch_and_heading(90, direção)
foguete.control.throttle = 1
foguete.control.activate_next_stage()

#Preparando o Stream
altitude = conn.add_stream(getattr, foguete.flight(), 'mean_altitude')
heading = foguete.flight().heading
apoastro = conn.add_stream(getattr, foguete.orbit, 'apoapsis_altitude')
periastro = conn.add_stream(getattr, foguete.orbit, 'periapsis_altitude')


#Flight State
fase_ascenção = True
fase_preparo = False
queima_orbital = False
print('apoastro1', foguete.orbit.apoapsis)
print('apoastro2: ', apoastro())


while fase_ascenção or fase_preparo or queima_orbital:
    
    estagio = foguete.control.current_stage-1
    recursos = foguete.resources_in_decouple_stage(estagio)
    comb_liq = conn.add_stream(recursos.amount, 'LiquidFuel')
    comb_solid = conn.add_stream(recursos.amount, 'SolidFuel')
    empuxo =  foguete.available_thrust
    g =  conn.add_stream(getattr,foguete.orbit.body,'surface_gravity')
    peso = foguete.mass
    twr = empuxo/((g())*(peso))
    
    #combustivel = comb_liq()
    
    #Fase da ascenção
    if fase_ascenção:
        foguete.auto_pilot.target_roll = direção
        ang = 90-((90-ang_final)/apoastro_final)*apoastro()
        foguete.auto_pilot.target_pitch_and_heading(ang, direção)
        
        if altitude() > 10000 and altitude() < 35000:
            if twr != 0:
                a = 1/twr #aceleração do foguete parametrizada pelo twr
            foguete.control.throttle = 2*a
        if altitude() > 35000:
            foguete.control.throttle = 1

        #Mudança de estágio
        if comb_solid() < 0.1:
            if comb_liq() < 0.1:
                foguete.control.activate_next_stage()

        #MECO
        if apoastro() >= apoastro_final:
            foguete.control.throttle = 0
            foguete.auto_pilot.target_pitch_and_heading(0, direção)
            time.sleep(0.5)
            if comb_liq() < 1 and estagio >= 1:
                foguete.control.activate_next_stage()

            time.sleep(0.1)
            #caso exista SAE
            if foguete.control.sas:
                foguete.control.sas = True
                foguete.control.sas_mode = conn.space_center.SASMode.prograde

            fase_ascenção = False
            fase_preparo = True
    
    #Fase de preparop para órbita
    elif fase_preparo:
        if altitude() > altitude_orbital:
            fase_preparo = False
            queima_orbital = True
            foguete.control.sas = False
            foguete.control.throttle = 1
    elif queima_orbital:
        foguete.auto_pilot.target_pitch_and_heading(0, direção)

        #SECO
        pr=periastro()
        #if apoastro() >= 74000 and pr > 70000:
        if pr > 70000:
            a=periastro()
            foguete.control.throttle = 0
            queima_orbital = False

        #Aciona o próximo estágio,caso não exista mais combustível.
        if comb_liq() < 0.1 and estagio >= 1:
            foguete.control.activate_next_stage()

#O pilotoaltomático desliga
foguete.auto_pilot.disengage()
time.sleep(5)

#Indica o fim do código
print('fim do código')
