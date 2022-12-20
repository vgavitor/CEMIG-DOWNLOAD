from ast import Try
from distutils.errors import LinkError
import json
from time import sleep
from webbrowser import Chrome
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pprint import pprint
import requests
import pyodbc
from datetime import datetime

server = ''                   
database = '' 
username = ''
password = ''
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)
cursor = cnxn.cursor() # Conexão   OK!!! 

def status():

    var = requests.get("https://atende.cemig.com.br/Login")

    return var.status_code


Data = datetime.now()
mes = int(Data.month) 
mes = mes-1
print(mes)
datas = ('JAN' , 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET')
print(datas[mes])

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
                        server+';DATABASE='+database+';UID='+username+';PWD='+password)
cursor = cnxn.cursor() # Conexão   OK!!!

lista = []

cursor.execute("SELECT [NºInsta],[Ref_ultimo_Mes] FROM [dbo].[LISTA_CEMIG]") #------------LISTA SQL
row = cursor.fetchone()

while row:

    dicionario = {'instala': int(row[0]) , 'com': str(row[1])}
    lista.append(dicionario)
    row = cursor.fetchone()


""" 

for index  in range(len(lista)):
    print(lista[index]['com'])
    print(lista[index]['instala'])

    sleep(1)

sleep(50)  

while row: 

    lista.append(int(row[1]))
    row = cursor.fetchone()

print('lista')
print(len(lista))


abaixo_de = -179 #------------Linhas a se deletar

lista2


while abaixo_de >= 0 : 
    print(len(lista))
    lista.pop(abaixo_de)
    
    abaixo_de = abaixo_de - 1


print(lista) 
 """

while status() != 200:
        sleep(0.5)



navegador = webdriver.Chrome()

error500 = 0
print(lista)

while error500 == 0:

    try:
        navegador.get("https://atende.cemig.com.br/Login") #-------------------Acesso a https://atende.cemig.com.br/Login-----------------------#


    except:
            print('------------------CEMIG N FUNCIONA----------------------')

    else:
        error500 = 1

try:
    element = WebDriverWait(navegador,2 , poll_frequency= 0.5).until(
                EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler")) #------------------VERIFICAR COOK 5 segundos----------------------
                                                    )
except:

    print('------------------SEM COOK----------------------')
    
    while status() != 200:
        sleep(0.5)
        print(status())
    print(status())     
    navegador.find_element_by_name('Acesso').send_keys('')#------------CREA,
    navegador.find_element_by_name('Senha').send_keys('')#------------SENHA,
    sleep(0.5)
    usuario = navegador.find_element_by_id('divRecaptcha').click()#------------clicar no 'NÃO SOU O ROBO'

    sleep(10)

    while status() != 200:
        sleep(1)
        print(status())

    
    print(status()) 
    navegador.switch_to.new_window('tab')#------------TROCAR DE TELA
    navegador.get("https://atende.cemig.com.br/Login") 
    sleep(1)

    for index  in range(len(lista)):#------------------PARA o ITEM DA LISTA FAÇA----------------------


        if datas[mes] != lista[index+1]['com']:
            
            print('Data Diferentes')

            print(datas[mes])
            print(lista[index+1]['com'])
            print(lista[index+1]['instala'])#------------------ITENS DA LISTA A SER PESQUISADO INDEX E O NUMERO DA INSTALAÇÂO----------------------

            n_ins= str(lista[index+1]['instala'])
            print(n_ins)
            while status() != 200:
                sleep(0.5)
                print(status())
            print(status()) 
            sleep(2)
        
            try:
                element = WebDriverWait(navegador,100 , poll_frequency= 0.5).until(
                EC.element_to_be_clickable((By.NAME, "NumeroInstalacao"))
                                                        )
            except:
                sleep(1)
                print('----FALHO NA HORA DE PROCURAR A INSTALAÇÂO-------')
                navegador.find_element_by_id("dropdownSelecionarInstalacao").click()#------------------ABRIR ABA DE FINALIZAR ----------------------
                sleep(0.5)
                navegador.find_element_by_id('btnEncerrarSessao').click()  #------------------ENCERRAR SESSÂO -------------------
                print('encerrou SESSÃO')



            else:
                while status() != 200:
                    sleep(1)
                    print(status())
                print(status())              
                navegador.find_element_by_name('NumeroInstalacao').send_keys(lista[index+1]['instala'])#------------------VAI COLOCAR O NUMERO DA INStALAÇÃO ---------------------
                sleep(0.5)
                navegador.find_element_by_id('pesquisaInstalacaoTop').click()
                print(status()) 
                
                sleep(5)
                while status() != 200:
                    sleep(0.5)
                    print(status())

                print(status())     

                try:
                    navegador.get("https://atende.cemig.com.br/ConsultarDebitos") 
                            
                except:
                    while status() != 200:
                        sleep(0.5)
                        print(status())
                    print(status()) 

                    sleep(1)
                    navegador.find_element_by_id("dropdownSelecionarInstalacao").click()#------------------ABRIR ABA DE FINALIZAR ----------------------
                    sleep(0.5)
                    navegador.find_element_by_id('btnEncerrarSessao').click()  #------------------ENCRRAQR SESSÂO --------------------
                    print('encerrou SESSÃO')


                else:
                    sleep(3)
                    try:
                        
                        navegador.find_element_by_xpath("//tr[contains(td, '"+n_ins+"')]")
                    
                    except:
                        
                        print('-----------------------AQUIIIIII---------------------------------------------')
                        try:
                            element = WebDriverWait(navegador,8 , poll_frequency= 0.5).until(
                            EC.element_to_be_clickable((By.ID, "dropdownSelecionarInstalacao"))
                                        )
                            print('------------------ESPERANDO O BOTÂO DA INSTaÇAO PARA ENCeRRAR-----------')

                        except:

                            tamanho1 =  navegador.find_element_by_xpath("//tr[contains(td, '"+n_ins+"')]")
                            tamanho =   len(tamanho1.find_elements_by_link_text('Baixar PDF'))

                            print(tamanho)  
                            print('------------------------------------------------------------------------------')
                            while status() != 200:
                                sleep(0.5)
                                print(status())
                            print(status())

                            try:
                                navegador.get("https://atende.cemig.com.br/ViabilidadeFornecimento") 
                            
                            except:
                                    error500 = 0

                                    while error500 == 0:

                                        try:
                                            navegador.get("https://atende.cemig.com.br/Login") #-------------------Acesso a https://atende.cemig.com.br/Login-----------------------#


                                        except:
                                                print('------------------CEMIG N FUNCIONA----------------------')

                                        else:
                                            error500 = 1


                                    sleep(3)
                                    navegador.find_element_by_name('NumeroInstalacao').send_keys(lista[index+1])#------------------VAI COLOCAR O NUMERO DA INStALAÇÃO --------------------
                                    sleep(0.5)
                                    navegador.find_element_by_id('pesquisaInstalacaoTop').click()
                                    sleep(5)
                                    navegador.find_element_by_id("dropdownSelecionarInstalacao").click()#------------------ABRIR ABA DE FINALIZAR ----------------------
                                    sleep(0.5)
                                    navegador.find_element_by_id('btnEncerrarSessao').click()  #------------------ENCRRAQR SESSÂO --------------------
                                    print('encerrou SESSÃO')

                            else:

                                try:
                                    element = WebDriverWait(navegador,8 , poll_frequency= 0.5).until(
                                    EC.element_to_be_clickable((By.ID, "dropdownSelecionarInstalacao"))
                                                )
                                    print('------------------ESPERANDO O BOTÂO DA INSTaÇAO PARA ENCeRRAR-----------') 
                                    
                                except:
                                        print('------------------nâo achou a caixa para filalizar sessão-----------') 
                                else:
                                    sleep(3)
                                    navegador.find_element_by_id("dropdownSelecionarInstalacao").click()#------------------ABRIR ABA DE FINALIZAR -------------------
                                    sleep(0.5)
                                    navegador.find_element_by_id('btnEncerrarSessao').click()  #------------------ENCRRAQR SESSÂO --------------------
                                    print('encerrou SESSÃO')

                        else:

                            sleep(1)
                            while status() != 200:
                                    sleep(0.1)
                                    print(status())
                            print(status())
                            print('VAI CLICAR NA CAIXA DE SELECIONAR INSTALAÇÂO')
                            navegador.find_element_by_id("dropdownSelecionarInstalacao").click()#------------------ABRIR ABA DE FINALIZAR ---------------------
                            sleep(0.5)
                            navegador.find_element_by_id('btnEncerrarSessao').click()  #------------------ENCRRAQR SESSÂO ---------------------
                            print('encerrou SESSÃO 2')


                    else:#   ------------------VAI BAIXAR----------------------

                        tamanho1 =  navegador.find_element_by_xpath("//tr[contains(td, '"+n_ins+"')]")
                        tamanho =   len(tamanho1.find_elements_by_link_text('Baixar PDF'))

                        print(tamanho)
                        print('--------------------------------------------------------------------------------------------------------------------------------------------------------')

                        if tamanho == 1:
                            
                            while status() != 200:
                                sleep(0.5)
                                print(status())
                            

                            tamanho1.find_elements_by_link_text('Baixar PDF')[0].click()
                                
                                                        
                        try:
                            element = WebDriverWait(navegador,8 , poll_frequency= 0.5).until(
                            EC.element_to_be_clickable((By.ID, "dropdownSelecionarInstalacao"))
                                        )
                            print('------------------ESPERANDO O BOTÂO DA INSTaÇAO PARA ENCeRRAR-----------')

                        except:

            
                            while status() != 200:
                                sleep(0.5)
                                print(status())
                            print(status())

                            try:
                                navegador.get("https://atende.cemig.com.br/ViabilidadeFornecimento") 
                            
                            except:
                                    error500 = 0

                                    while error500 == 0:

                                        try:
                                            navegador.get("https://atende.cemig.com.br/Login") #-------------------Acesso a https://atende.cemig.com.br/Login-----------------------#


                                        except:
                                                print('------------------CEMIG N FUNCIONA----------------------')

                                        else:
                                            error500 = 1


                                    sleep(3)
                                    navegador.find_element_by_name('NumeroInstalacao').send_keys(lista[index+1])#------------------VAI COLOCAR O NUMERO DA INStALAÇÃO -----------------
                                    sleep(0.5)
                                    navegador.find_element_by_id('pesquisaInstalacaoTop').click()
                                    sleep(5)
                                    navegador.find_element_by_id("dropdownSelecionarInstalacao").click()#------------------ABRIR ABA DE FINALIZAR ---------------
                                    sleep(0.5)
                                    navegador.find_element_by_id('btnEncerrarSessao').click()  #------------------ENCRRAQR SESSÂO --------------------
                                    print('encerrou SESSÃO')

                            else:

                                try:
                                    element = WebDriverWait(navegador,8 , poll_frequency= 0.5).until(
                                    EC.element_to_be_clickable((By.ID, "dropdownSelecionarInstalacao"))
                                                )
                                    print('------------------ESPERANDO O BOTÂO DA INSTaÇAO PARA ENCeRRAR-----------') 
                                    
                                except:
                                        print('------------------nâo achou a caixa para filalizar sessão-----------') 
                                else:
                                    sleep(3)
                                    navegador.find_element_by_id("dropdownSelecionarInstalacao").click()#------------------ABRIR ABA DE FINALIZAR ---------------------
                                    sleep(0.5)
                                    navegador.find_element_by_id('btnEncerrarSessao').click()  #------------------ENCRRAQR SESSÂO ---------------------
                                    print('encerrou SESSÃO')

                        else:

                            sleep(3)
                            while status() != 200:
                                    sleep(0.1)
                                    print(status())
                            print(status())
                            print('VAI CLICAR NA CAIXA DE SELECIONAR INSTALAÇÂO')
                            navegador.find_element_by_id("dropdownSelecionarInstalacao").click()#------------------ABRIR ABA DE FINALIZAR ----------------------
                            sleep(0.5)
                            navegador.find_element_by_id('btnEncerrarSessao').click()  #------------------ENCRRAQR SESSÂO ----------------------
                            print('encerrou SESSÃO 2')
            
        else:
         print('Já possui conta baixada para o mês atual')

                    


else:

    print('------------------COM COOK----------------------')
    
    while status() != 200:
        sleep(0.5)
        print(status())
    print(status())

    usuario = navegador.find_element_by_id('onetrust-accept-btn-handler').click()
    navegador.find_element_by_name('Acesso').send_keys('')#------------CREA,
    navegador.find_element_by_name('Senha').send_keys('')#------------SENHA,
    sleep(0.5)
    usuario = navegador.find_element_by_id('divRecaptcha').click()#------------clicar no 'NÃO SOU O ROBO'

    sleep(10)

    while status() != 200:
        sleep(0.5)
        print(status())
    print(status())

    navegador.switch_to.new_window('tab')#------------TROCAR DE TELA
    navegador.get("https://atende.cemig.com.br/Login")

    sleep(1)

    for index  in range(len(lista)):#------------------PARA o ITEM DA LISTA FAÇA----------------------

        if datas[mes] != lista[index+1]['com']:
            
            print('Data Diferentes')

            print(datas[mes])
            print(lista[index+1]['com'])
            print(lista[index+1]['instala'])#------------------ITENS DA LISTA A SER PESQUISADO INDEX E O NUMERO DA INSTALAÇÂO----------------------

            n_ins= str(lista[index+1]['instala'])

            while status() != 200:
                sleep(0.5)
                print(status())
            print(status())

            try:
                element = WebDriverWait(navegador,10 , poll_frequency= 0.5).until(
                EC.element_to_be_clickable((By.NAME, "NumeroInstalacao"))
                                                        )
            except:
                print('----FALHO NA HORA DE PROCURAR A INSTALAÇÂO-------')
                navegador.get("https://atende.cemig.com.br/Login") 
                sleep(3)


            else:
                    
                while status() != 200:
                    sleep(0.5)
                    print(status())
                print(status())

            
                navegador.find_element_by_name('NumeroInstalacao').send_keys(lista[index+1]['instala'])#------------------VAI COLOCAR O NUMERO DA INStALAÇÃO 2----------------------
                sleep(0.5)
                navegador.find_element_by_id('pesquisaInstalacaoTop').click()

                sleep(5)

                while status() != 200:
                    sleep(0.5)
                    print(status())
                print(status())



                try:
                    navegador.get("https://atende.cemig.com.br/ConsultarDebitos") 
                                                
                except:
                    while status() != 200:
                        sleep(0.5)
                        print(status())
                        
                    print(status())
                    navegador.get("https://atende.cemig.com.br/Login")
                    sleep(3)
                    print('ESPERANDO 5')

                    print('encerrou SESSÃO')

                else:
                    sleep(3)
                    try:
                        navegador.find_element_by_xpath("//tr[contains(td, '"+n_ins+"')]")
                    
                    except:

                        print('---------------------------AQUIIIIII---------------------------------------------')

                        try:
                            element = WebDriverWait(navegador,8 , poll_frequency= 0.5).until(
                            EC._element_if_visible((By.ID, "dropdownSelecionarInstalacao"))
                                        )
                            print('------------------ESPERANDO O BOTÂO DA INSTaÇAO PARA ENCeRRAR-----------')

                        except:

            
                            while status() != 200:
                                sleep(0.5)
                                print(status())
                            print(status())

                            try:
                                navegador.get("https://atende.cemig.com.br/ViabilidadeFornecimento") 
                            
                            except:
                                    error500 = 0

                                    while error500 == 0:

                                        try:
                                            navegador.get("https://atende.cemig.com.br/Login") #-------------------Acesso a https://atende.cemig.com.br/Login-----------------------#


                                        except:
                                                print('------------------CEMIG N FUNCIONA----------------------')

                                        else:
                                            error500 = 1


                                    sleep(3)
                                    navegador.find_element_by_name('NumeroInstalacao').send_keys(lista[index+372])#------------------VAI COLOCAR O NUMERO DA INStALAÇÃO 2---------------------
                                    sleep(0.5)
                                    navegador.find_element_by_id('pesquisaInstalacaoTop').click()
                                    sleep(3)
                                    navegador.find_element_by_id("dropdownSelecionarInstalacao").click()#------------------ABRIR ABA DE FINALIZAR 2----------------------
                                    sleep(0.5)
                                    navegador.find_element_by_id('btnEncerrarSessao').click()  #------------------ENCRRAQR SESSÂO 2 ----------------------
                                    print('encerrou SESSÃO')

                            else:

                                try:
                                    element = WebDriverWait(navegador,8 , poll_frequency= 0.5).until(
                                    EC.element_to_be_clickable((By.ID, "dropdownSelecionarInstalacao"))
                                                )
                                    print('------------------ESPERANDO O BOTÂO DA INSTaÇAO PARA ENCeRRAR-----------') 
                                    
                                except:
                                        print('------------------nâo achou a caixa para filalizar sessão-----------') 
                                else:
                                    sleep(3)
                                    navegador.find_element_by_id("dropdownSelecionarInstalacao").click()#------------------ABRIR ABA DE FINALIZAR 2----------------------
                                    sleep(0.5)
                                    navegador.find_element_by_id('btnEncerrarSessao').click()  #------------------ENCRRAQR SESSÂO 2----------------------
                                    print('encerrou SESSÃO')

                        else:

                            sleep(3)
                            while status() != 200:
                                    sleep(0.1)
                                    print(status())
                            print(status())
                            print('VAI CLICAR NA CAIXA DE SELECIONAR INSTALAÇÂO')
                            navegador.find_element_by_id("dropdownSelecionarInstalacao").click()#------------------ABRIR ABA DE FINALIZAR 2----------------------
                            sleep(0.5)
                            navegador.find_element_by_id('btnEncerrarSessao').click()  #------------------ENCRRAQR SESSÂO 2----------------------
                            print('encerrou SESSÃO 2')


                    else:#   ------------------VAI BAIXAR----------------------

                        tamanho1 =  navegador.find_element_by_xpath("//tr[contains(td, '"+n_ins+"')]")
                        tamanho =      len(tamanho1.find_elements_by_link_text('Baixar PDF'))
                        print(tamanho)
                        print('--------------------analisar aqui----------------------------------------')


                        if tamanho == 1:
                            
                            while status() != 200:
                                sleep(0.5)
                                print(status())

                            tamanho1.find_elements_by_link_text('Baixar PDF')[0].click()  #-----------------AQUI N FUNCIONA click branco
                                
                                                        
                        try:
                            element = WebDriverWait(navegador,8 , poll_frequency= 0.5).until(
                            EC.element_to_be_clickable((By.ID, "dropdownSelecionarInstalacao"))
                                        )
                            print('------------------ESPERANDO O BOTÂO DA INSTaÇAO PARA ENCeRRAR-----------')

                        except:

            
                            while status() != 200:
                                sleep(0.5)
                                print(status())
                            print(status())

                            try:
                                navegador.get("https://atende.cemig.com.br/ViabilidadeFornecimento") 
                            
                            except:
                                    error500 = 0

                                    while error500 == 0:

                                        try:
                                            navegador.get("https://atende.cemig.com.br/Login") #-------------------Acesso a https://atende.cemig.com.br/Login-----------------------#


                                        except:
                                                print('------------------CEMIG N FUNCIONA----------------------')

                                        else:
                                            error500 = 1


                                    sleep(3)
                                    navegador.find_element_by_name('NumeroInstalacao').send_keys(lista[index+1])#------------------VAI COLOCAR O NUMERO DA INStALAÇÃO 2---------------------
                                    sleep(0.5)
                                    navegador.find_element_by_id('pesquisaInstalacaoTop').click()
                                    sleep(3)
                                    navegador.find_element_by_id("dropdownSelecionarInstalacao").click()#------------------ABRIR ABA DE FINALIZAR 2----------------------
                                    sleep(0.5)
                                    navegador.find_element_by_id('btnEncerrarSessao').click()  #------------------ENCRRAQR SESSÂO 2 ----------------------
                                    print('encerrou SESSÃO')

                            else:

                                try:
                                    element = WebDriverWait(navegador,8 , poll_frequency= 0.5).until(
                                    EC.element_to_be_clickable((By.ID, "dropdownSelecionarInstalacao"))
                                                )
                                    print('------------------ESPERANDO O BOTÂO DA INSTaÇAO PARA ENCeRRAR-----------') 
                                    
                                except:
                                        print('------------------nâo achou a caixa para filalizar sessão-----------') 
                                else:
                                    sleep(3)
                                    navegador.find_element_by_id("dropdownSelecionarInstalacao").click()#------------------ABRIR ABA DE FINALIZAR 2----------------------
                                    sleep(0.5)
                                    navegador.find_element_by_id('btnEncerrarSessao').click()  #------------------ENCRRAQR SESSÂO 2----------------------
                                    print('encerrou SESSÃO')

                        else:

                            sleep(3)
                            while status() != 200:
                                    sleep(0.1)
                                    print(status())
                            print(status())
                            print('VAI CLICAR NA CAIXA DE SELECIONAR INSTALAÇÂO')
                            navegador.find_element_by_id("dropdownSelecionarInstalacao").click()#------------------ABRIR ABA DE FINALIZAR 2----------------------
                            sleep(0.5)
                            navegador.find_element_by_id('btnEncerrarSessao').click()  #------------------ENCRRAQR SESSÂO 2----------------------
                            print('encerrou SESSÃO 2')
    
        else:
          print('Já possui conta baixada para o mês atual')